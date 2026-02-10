"""
Lab 04: Multi-Stage Docker Builds
====================================
Learn multi-stage builds to create smaller, production-ready images.

No Docker installation required — generates and validates Dockerfiles.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-04"

print("=" * 50)
print("  Lab 04: Multi-Stage Docker Builds")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Why Multi-Stage?
# ============================================================

print("\n--- Step 1: Why Multi-Stage Builds? ---\n")

class ImageSizeEstimator:
    """Estimate Docker image sizes for comparison."""

    def __init__(self, name):
        self.name = name
        self.layers = []

    def add(self, description, size_mb):
        self.layers.append({"desc": description, "size_mb": size_mb})

    @property
    def total_mb(self):
        return sum(l["size_mb"] for l in self.layers)

    def display(self):
        print(f"  {self.name}:")
        for l in self.layers:
            bar = "#" * (l["size_mb"] // 20)
            print(f"    {l['desc']:<40} {l['size_mb']:>6} MB  {bar}")
        print(f"    {'TOTAL':<40} {self.total_mb:>6} MB")


# Single-stage: everything in one image
single = ImageSizeEstimator("Single-Stage Image")
single.add("python:3.11-slim base", 150)
single.add("Build tools (gcc, make, headers)", 200)
single.add("pip download cache", 150)
single.add("Compiled wheels & source", 100)
single.add("Installed packages (runtime)", 300)
single.add("Application code", 5)

# Multi-stage: only runtime in final image
multi = ImageSizeEstimator("Multi-Stage Image (final)")
multi.add("python:3.11-slim base", 150)
multi.add("Installed packages (runtime only)", 300)
multi.add("Application code", 5)

single.display()
print()
multi.display()
print()
print(f"  Savings: {single.total_mb - multi.total_mb} MB ({(1 - multi.total_mb/single.total_mb)*100:.0f}% smaller)")
print(f"  Build tools, cache, and source stay in the builder stage!")


# ============================================================
# Step 2: Single-Stage vs Multi-Stage
# ============================================================

print("\n\n--- Step 2: Single vs Multi-Stage Dockerfile ---\n")

single_stage = textwrap.dedent('''\
    # Single-stage: everything in one image
    FROM python:3.11-slim

    WORKDIR /app

    # Install build dependencies (needed for some pip packages)
    RUN apt-get update && apt-get install -y \\
        gcc g++ make \\
        && rm -rf /var/lib/apt/lists/*

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

multi_stage = textwrap.dedent('''\
    # Stage 1: Builder (install everything, compile deps)
    FROM python:3.11-slim AS builder

    WORKDIR /app

    # Install build dependencies
    RUN apt-get update && apt-get install -y \\
        gcc g++ make \\
        && rm -rf /var/lib/apt/lists/*

    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

    # Stage 2: Runtime (only what's needed to run)
    FROM python:3.11-slim

    WORKDIR /app

    # Copy ONLY installed packages from builder (no gcc, no cache)
    COPY --from=builder /install /usr/local

    # Copy application code
    COPY . .

    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

print("  Single-Stage:")
for line in single_stage.strip().split("\n")[:5]:
    print(f"    {line}")
print("    ... (build tools stay in the image)")

print(f"\n  Multi-Stage:")
for line in multi_stage.strip().split("\n")[:6]:
    print(f"    {line}")
print("    ...")
print("    # Stage 2 starts fresh — no build tools!")

# Write files
with open(os.path.join(WORKDIR, "Dockerfile.single"), "w") as f:
    f.write(single_stage)
with open(os.path.join(WORKDIR, "Dockerfile.multi"), "w") as f:
    f.write(multi_stage)


# ============================================================
# Step 3: The COPY --from Pattern
# ============================================================

print("\n\n--- Step 3: COPY --from Pattern ---\n")

print("  The magic of multi-stage: COPY --from=<stage>")
print()
print("  Stage 1 (builder):")
print("    FROM python:3.11-slim AS builder")
print("    RUN pip install --prefix=/install -r requirements.txt")
print("    # /install/ now has all Python packages")
print()
print("  Stage 2 (runtime):")
print("    FROM python:3.11-slim        ← fresh image, no build tools!")
print("    COPY --from=builder /install /usr/local")
print("    # Only the installed packages are copied, nothing else")
print()
print("  What stays in builder (NOT in final image):")
print("    - gcc, g++, make (build tools)")
print("    - pip download cache")
print("    - Source code for compiled packages")
print("    - apt package lists")

# Create app files for a complete example
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
# Step 4: Validate Multi-Stage Dockerfile
# ============================================================

print("\n\n--- Step 4: Validate Multi-Stage Build ---\n")

def validate_multistage(content):
    """Check multi-stage Dockerfile for best practices."""
    checks = []

    # Check 1: Has multiple FROM instructions
    from_count = content.count("\nFROM ") + (1 if content.startswith("FROM ") else 0)
    checks.append(("Has multiple FROM stages", from_count >= 2))

    # Check 2: First stage has AS alias
    checks.append(("Builder stage has AS alias", " AS " in content or " as " in content))

    # Check 3: Uses COPY --from
    checks.append(("Uses COPY --from=builder", "--from=" in content))

    # Check 4: pip install uses --prefix
    checks.append(("pip uses --prefix (isolated install)", "--prefix=" in content))

    # Check 5: Final stage is slim
    lines = content.strip().split("\n")
    last_from = [l for l in lines if l.strip().startswith("FROM")][-1] if lines else ""
    checks.append(("Final stage uses slim base", "slim" in last_from))

    # Check 6: No build tools in final stage
    # Find content after the last FROM
    last_from_idx = content.rfind("\nFROM ")
    if last_from_idx >= 0:
        final_stage = content[last_from_idx:]
        has_build_tools = "apt-get" in final_stage and ("gcc" in final_stage or "make" in final_stage)
        checks.append(("No build tools in final stage", not has_build_tools))
    else:
        checks.append(("No build tools in final stage", True))

    return checks

checks = validate_multistage(multi_stage)
passed = sum(1 for _, ok in checks if ok)
print(f"  Multi-Stage Validation ({passed}/{len(checks)}):\n")
for name, ok in checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 1: Add a test stage
# ============================================================

print("\n\n--- TODO 1: Add a Test Stage ---\n")

# Multi-stage builds can include a test stage too!
# The pattern: builder → tester → runtime
# Tests run during build. If tests fail, the image isn't created.

# TODO: Write a 3-stage Dockerfile:
# Stage 1 (builder): Install dependencies
# Stage 2 (tester): Run tests (RUN python -m pytest tests/)
# Stage 3 (runtime): Copy only what's needed

todo1_dockerfile = ""

# Uncomment:
# todo1_dockerfile = textwrap.dedent('''\
#     # Stage 1: Builder
#     FROM python:3.11-slim AS builder
#     WORKDIR /app
#     COPY requirements.txt .
#     RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
#
#     # Stage 2: Tester (runs during build)
#     FROM python:3.11-slim AS tester
#     WORKDIR /app
#     COPY --from=builder /install /usr/local
#     COPY . .
#     RUN python -m pytest tests/ -v
#
#     # Stage 3: Runtime (only if tests pass)
#     FROM python:3.11-slim
#     WORKDIR /app
#     COPY --from=builder /install /usr/local
#     COPY . .
#     ENV PYTHONUNBUFFERED=1
#     EXPOSE 8000
#     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ''')

if todo1_dockerfile:
    from_count = todo1_dockerfile.count("FROM ")
    has_tester = "tester" in todo1_dockerfile.lower()
    has_pytest = "pytest" in todo1_dockerfile

    print(f"  [{'PASS' if from_count >= 3 else 'FAIL'}] Has 3 stages ({from_count} FROM)")
    print(f"  [{'PASS' if has_tester else 'FAIL'}] Has tester stage")
    print(f"  [{'PASS' if has_pytest else 'FAIL'}] Runs pytest in build")

    with open(os.path.join(WORKDIR, "Dockerfile.3stage"), "w") as f:
        f.write(todo1_dockerfile)
    print(f"\n  Saved Dockerfile.3stage to {WORKDIR}/")
else:
    print("  TODO: Write a 3-stage Dockerfile (builder → tester → runtime)")
    print("  Hint: The tester stage copies from builder, runs tests,")
    print("  and the runtime stage copies from builder (not tester)")


# ============================================================
# TODO 2: Multi-stage for AI with model download
# ============================================================

print("\n\n--- TODO 2: Multi-Stage with Model Download ---\n")

# For AI apps, you might want to download models during build.
# This keeps the download step cached while keeping build tools out.

# TODO: Write a 2-stage Dockerfile that:
# Stage 1 (builder): Install deps AND download a model
# Stage 2 (runtime): Copy packages + cached model, no build tools

todo2_dockerfile = ""

# Uncomment:
# todo2_dockerfile = textwrap.dedent('''\
#     # Stage 1: Builder + Model Download
#     FROM python:3.11-slim AS builder
#     WORKDIR /app
#
#     RUN apt-get update && apt-get install -y gcc g++ \\
#         && rm -rf /var/lib/apt/lists/*
#
#     COPY requirements.txt .
#     RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
#
#     # Download model during build (cached in this layer)
#     ENV TRANSFORMERS_CACHE=/app/models
#     RUN PYTHONPATH=/install/lib/python3.11/site-packages \\
#         python -c "from sentence_transformers import SentenceTransformer; \\
#         SentenceTransformer('all-MiniLM-L6-v2')" || true
#
#     # Stage 2: Runtime
#     FROM python:3.11-slim
#     WORKDIR /app
#
#     COPY --from=builder /install /usr/local
#     COPY --from=builder /app/models /app/models
#     COPY . .
#
#     ENV PYTHONUNBUFFERED=1
#     ENV TRANSFORMERS_CACHE=/app/models
#     EXPOSE 8000
#     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ''')

if todo2_dockerfile:
    has_model_download = "SentenceTransformer" in todo2_dockerfile or "model" in todo2_dockerfile.lower()
    has_model_copy = "--from=builder" in todo2_dockerfile and "model" in todo2_dockerfile.lower()
    has_cache_env = "TRANSFORMERS_CACHE" in todo2_dockerfile

    print(f"  [{'PASS' if has_model_download else 'FAIL'}] Model download in builder stage")
    print(f"  [{'PASS' if has_model_copy else 'FAIL'}] Model copied to runtime stage")
    print(f"  [{'PASS' if has_cache_env else 'FAIL'}] TRANSFORMERS_CACHE set")

    with open(os.path.join(WORKDIR, "Dockerfile.ai-multistage"), "w") as f:
        f.write(todo2_dockerfile)
    print(f"\n  Saved Dockerfile.ai-multistage to {WORKDIR}/")
else:
    print("  TODO: Write a multi-stage Dockerfile with model download")
    print("  Hint: Download models in builder stage, COPY --from=builder to runtime")


# ============================================================
# Summary
# ============================================================

print("\n\n--- Lab 04 Summary ---\n")
print("  Multi-stage build benefits:")
print("    1. Smaller images (no build tools in final image)")
print("    2. Better security (fewer packages = smaller attack surface)")
print("    3. Can include test stage (tests fail → no image created)")
print("    4. AI models can be pre-downloaded and cached")
print("    5. Typical savings: 50-70% smaller images")
print(f"\n  Files in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    print(f"    {f}")
