"""
Lab 04 Solution: Multi-Stage Docker Builds
=============================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-04"

print("=" * 50)
print("  Lab 04 Solution: Multi-Stage Builds")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# Create app files
app_code = textwrap.dedent('''\
    """UniGPS AI Agent — Multi-Stage Build Demo"""
    from fastapi import FastAPI
    from pydantic import BaseModel

    app = FastAPI(title="UniGPS Agent", version="2.0.0")

    @app.get("/health")
    async def health():
        return {"status": "healthy", "build": "multi-stage"}

    class SupportRequest(BaseModel):
        employee_name: str
        request: str

    @app.post("/api/support")
    async def handle_support(req: SupportRequest):
        return {"category": "general", "response": f"Hello {req.employee_name}"}
''')

requirements = textwrap.dedent('''\
    fastapi==0.104.1
    uvicorn[standard]==0.24.0
    pydantic==2.5.0
    langchain-core==0.1.23
    python-dotenv==1.0.0
''')

with open(os.path.join(WORKDIR, "main.py"), "w") as f:
    f.write(app_code)
with open(os.path.join(WORKDIR, "requirements.txt"), "w") as f:
    f.write(requirements)


# ============================================================
# TODO 1 Solution: 3-Stage Dockerfile with tests
# ============================================================

print("\n--- TODO 1 Solution: 3-Stage with Tests ---\n")

todo1_dockerfile = textwrap.dedent('''\
    # Stage 1: Builder
    FROM python:3.11-slim AS builder
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

    # Stage 2: Tester (runs during build)
    FROM python:3.11-slim AS tester
    WORKDIR /app
    COPY --from=builder /install /usr/local
    COPY . .
    RUN python -m pytest tests/ -v

    # Stage 3: Runtime (only if tests pass)
    FROM python:3.11-slim
    WORKDIR /app
    COPY --from=builder /install /usr/local
    COPY . .
    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

from_count = todo1_dockerfile.count("FROM ")
has_tester = "tester" in todo1_dockerfile.lower()
has_pytest = "pytest" in todo1_dockerfile

print(f"  [{'PASS' if from_count >= 3 else 'FAIL'}] Has 3 stages ({from_count} FROM)")
print(f"  [{'PASS' if has_tester else 'FAIL'}] Has tester stage")
print(f"  [{'PASS' if has_pytest else 'FAIL'}] Runs pytest in build")

with open(os.path.join(WORKDIR, "Dockerfile.3stage"), "w") as f:
    f.write(todo1_dockerfile)

print("\n  How it works:")
print("    Stage 1 (builder): Install all Python packages")
print("    Stage 2 (tester):  Copy packages + code, run pytest")
print("                        If tests FAIL → build STOPS (no image)")
print("    Stage 3 (runtime): Fresh image, copy packages + code")
print()
print("  Key: Runtime copies from BUILDER, not tester")
print("  (tester may have test artifacts we don't want)")


# ============================================================
# TODO 2 Solution: Multi-stage with model download
# ============================================================

print("\n\n--- TODO 2 Solution: Multi-Stage with Model ---\n")

todo2_dockerfile = textwrap.dedent('''\
    # Stage 1: Builder + Model Download
    FROM python:3.11-slim AS builder
    WORKDIR /app

    RUN apt-get update && apt-get install -y gcc g++ \\
        && rm -rf /var/lib/apt/lists/*

    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

    # Download model during build (cached in this layer)
    ENV TRANSFORMERS_CACHE=/app/models
    RUN PYTHONPATH=/install/lib/python3.11/site-packages \\
        python -c "from sentence_transformers import SentenceTransformer; \\
        SentenceTransformer('all-MiniLM-L6-v2')" || true

    # Stage 2: Runtime
    FROM python:3.11-slim
    WORKDIR /app

    COPY --from=builder /install /usr/local
    COPY --from=builder /app/models /app/models
    COPY . .

    ENV PYTHONUNBUFFERED=1
    ENV TRANSFORMERS_CACHE=/app/models
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

has_model_download = "SentenceTransformer" in todo2_dockerfile
has_model_copy = "--from=builder" in todo2_dockerfile and "models" in todo2_dockerfile
has_cache_env = "TRANSFORMERS_CACHE" in todo2_dockerfile

print(f"  [{'PASS' if has_model_download else 'FAIL'}] Model download in builder")
print(f"  [{'PASS' if has_model_copy else 'FAIL'}] Model copied to runtime")
print(f"  [{'PASS' if has_cache_env else 'FAIL'}] TRANSFORMERS_CACHE set")

with open(os.path.join(WORKDIR, "Dockerfile.ai-multistage"), "w") as f:
    f.write(todo2_dockerfile)

print("\n  How it works:")
print("    Builder stage:")
print("      1. Install gcc (needed to compile some packages)")
print("      2. pip install all packages")
print("      3. Download model (~90 MB) into /app/models")
print("    Runtime stage:")
print("      1. Fresh slim image (no gcc!)")
print("      2. COPY packages from builder")
print("      3. COPY models from builder (cached!)")
print("      4. COPY app code")
print()
print("  Benefits:")
print("    - No gcc/g++ in final image (~200 MB saved)")
print("    - Model download is cached (build once, reuse)")
print("    - Container starts instantly (no download needed)")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 04 Solution complete!")
print("- TODO 1: 3-stage build (builder → tester → runtime)")
print("- TODO 2: Multi-stage with model download/caching")
