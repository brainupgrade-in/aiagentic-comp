"""
Lab 02 Solution: Writing Dockerfiles for FastAPI
===================================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-02"

print("=" * 50)
print("  Lab 02 Solution: Dockerfiles for FastAPI")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# Create app files
app_code = textwrap.dedent('''\
    """UniGPS AI Agent — FastAPI Application"""
    import os
    from fastapi import FastAPI
    from pydantic import BaseModel, Field

    app = FastAPI(title="UniGPS AI Agent", version="1.0.0")

    class SupportRequest(BaseModel):
        employee_name: str = Field(..., min_length=2, max_length=100)
        request: str = Field(..., min_length=5, max_length=1000)

    class SupportResponse(BaseModel):
        category: str
        response: str

    TEMPLATES = {
        "hr": "Please visit the HR portal or email hr@unigps.in.",
        "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
        "finance": "Please email finance@unigps.in with details.",
        "general": "Your request has been noted. A team member will respond shortly.",
    }

    @app.get("/health")
    async def health():
        return {"status": "healthy", "agent": "ready", "version": "1.0.0"}

    @app.post("/api/support", response_model=SupportResponse)
    async def handle_support(req: SupportRequest):
        text = req.request.lower()
        if any(w in text for w in ["leave", "salary", "hr"]):
            cat = "hr"
        elif any(w in text for w in ["server", "bug", "deploy"]):
            cat = "tech"
        elif any(w in text for w in ["expense", "invoice", "budget"]):
            cat = "finance"
        else:
            cat = "general"
        return SupportResponse(category=cat, response=f"[{cat.upper()}] {TEMPLATES[cat]}")
''')

requirements = textwrap.dedent('''\
    fastapi==0.104.1
    uvicorn[standard]==0.24.0
    pydantic==2.5.0
    langchain-core==0.1.23
    langchain-groq==0.0.3
    langgraph==0.0.26
    python-dotenv==1.0.0
''')

with open(os.path.join(WORKDIR, "main.py"), "w") as f:
    f.write(app_code)
with open(os.path.join(WORKDIR, "requirements.txt"), "w") as f:
    f.write(requirements)


# ============================================================
# TODO 1 Solution: ARG and LABEL
# ============================================================

print("\n--- TODO 1 Solution: ARG and LABEL ---\n")

todo1_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim

    WORKDIR /app

    ARG APP_VERSION=1.0.0

    LABEL maintainer="dev@unigps.in"
    LABEL version="${APP_VERSION}"
    LABEL description="UniGPS AI Agent"

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    ENV APP_VERSION=${APP_VERSION}
    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

has_arg = "ARG" in todo1_dockerfile and "APP_VERSION" in todo1_dockerfile
has_label = "LABEL" in todo1_dockerfile and "maintainer" in todo1_dockerfile.lower()
has_env_from_arg = "ENV APP_VERSION" in todo1_dockerfile

print(f"  [{'PASS' if has_arg else 'FAIL'}] ARG APP_VERSION defined")
print(f"  [{'PASS' if has_label else 'FAIL'}] LABEL maintainer added")
print(f"  [{'PASS' if has_env_from_arg else 'FAIL'}] ENV set from ARG")

with open(os.path.join(WORKDIR, "Dockerfile"), "w") as f:
    f.write(todo1_dockerfile)

print("\n  Key patterns:")
print("    ARG APP_VERSION=1.0.0           ← build-time variable with default")
print("    LABEL version=\"${APP_VERSION}\"   ← use ARG in LABEL")
print("    ENV APP_VERSION=${APP_VERSION}   ← make ARG available at runtime")
print("    docker build --build-arg APP_VERSION=2.0.0 .  ← override at build time")


# ============================================================
# TODO 2 Solution: RAG Dockerfile
# ============================================================

print("\n\n--- TODO 2 Solution: RAG Dockerfile ---\n")

rag_requirements = textwrap.dedent('''\
    fastapi==0.104.1
    uvicorn[standard]==0.24.0
    langchain-core==0.1.23
    chromadb==0.4.22
    sentence-transformers==2.3.1
''')

todo2_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim

    WORKDIR /app

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    RUN mkdir -p /data

    ENV PYTHONUNBUFFERED=1
    ENV TRANSFORMERS_CACHE=/app/.cache/transformers

    EXPOSE 8080

    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
''')

def validate_dockerfile(content):
    checks = []
    lines = content.strip().split("\n")
    stripped = [l.strip() for l in lines]
    checks.append(("Has FROM", any(l.startswith("FROM") for l in stripped)))
    checks.append(("Uses slim base", any("slim" in l for l in stripped if l.startswith("FROM"))))
    checks.append(("Has WORKDIR", any(l.startswith("WORKDIR") for l in stripped)))
    req_idx = next((i for i, l in enumerate(stripped) if "requirements" in l and l.startswith("COPY")), None)
    code_idx = next((i for i, l in enumerate(stripped) if l in ("COPY . .", "COPY . /app")), None)
    checks.append(("Layer caching", req_idx is not None and code_idx is not None and req_idx < code_idx))
    checks.append(("--no-cache-dir", "--no-cache-dir" in content))
    checks.append(("PYTHONUNBUFFERED", "PYTHONUNBUFFERED" in content))
    checks.append(("Has EXPOSE", any(l.startswith("EXPOSE") for l in stripped)))
    checks.append(("CMD exec form", 'CMD ["' in content or "CMD ['" in content))
    return checks

checks = validate_dockerfile(todo2_dockerfile)
has_data_dir = "/data" in todo2_dockerfile
has_cache_env = "TRANSFORMERS_CACHE" in todo2_dockerfile
has_port_8080 = "8080" in todo2_dockerfile

print(f"  [{'PASS' if has_data_dir else 'FAIL'}] /data directory created")
print(f"  [{'PASS' if has_cache_env else 'FAIL'}] TRANSFORMERS_CACHE set")
print(f"  [{'PASS' if has_port_8080 else 'FAIL'}] Port 8080 exposed")

passed = sum(1 for _, ok in checks if ok)
print(f"\n  Standard checks: {passed}/{len(checks)} passed")

with open(os.path.join(WORKDIR, "Dockerfile.rag"), "w") as f:
    f.write(todo2_dockerfile)
with open(os.path.join(WORKDIR, "requirements-rag.txt"), "w") as f:
    f.write(rag_requirements)

print(f"\n  Saved Dockerfile.rag to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 02 Solution complete!")
print("- TODO 1: ARG, LABEL, and ENV for versioning")
print("- TODO 2: RAG Dockerfile with /data dir, TRANSFORMERS_CACHE, port 8080")
