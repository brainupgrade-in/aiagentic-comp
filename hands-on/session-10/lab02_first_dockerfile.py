"""
Lab 02: Writing Dockerfiles for FastAPI
=========================================
Create a proper Dockerfile for a FastAPI + LangGraph agent application.

No Docker installation required — generates and validates Dockerfile content.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-02"

print("=" * 50)
print("  Lab 02: Writing Dockerfiles for FastAPI")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: The FastAPI Application
# ============================================================

print("\n--- Step 1: The FastAPI Application ---\n")

# This is the app we'll containerize
app_code = textwrap.dedent('''\
    """UniGPS AI Agent — FastAPI Application"""
    import os
    from fastapi import FastAPI
    from pydantic import BaseModel, Field

    app = FastAPI(
        title="UniGPS AI Agent",
        version="1.0.0",
        description="Production AI agent with LangGraph",
    )

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
        # Simple keyword classifier (no LLM needed for demo)
        text = req.request.lower()
        if any(w in text for w in ["leave", "salary", "hr"]):
            cat = "hr"
        elif any(w in text for w in ["server", "bug", "deploy"]):
            cat = "tech"
        elif any(w in text for w in ["expense", "invoice", "budget"]):
            cat = "finance"
        else:
            cat = "general"
        return SupportResponse(
            category=cat,
            response=f"[{cat.upper()}] {TEMPLATES[cat]}",
        )
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

print(f"  Created main.py and requirements.txt in {WORKDIR}/")
print(f"  App: FastAPI with /health and /api/support endpoints")
print(f"  Dependencies: {len(requirements.strip().split(chr(10)))} packages")

# ============================================================
# Step 2: Dockerfile Instruction Reference
# ============================================================

print("\n\n--- Step 2: Dockerfile Instructions Reference ---\n")

instructions = [
    ("FROM",    "Set the base image",           "FROM python:3.11-slim"),
    ("WORKDIR", "Set working directory",         "WORKDIR /app"),
    ("COPY",    "Copy files into image",         "COPY requirements.txt ."),
    ("RUN",     "Execute build-time command",    "RUN pip install -r req.txt"),
    ("ENV",     "Set environment variable",      "ENV PYTHONUNBUFFERED=1"),
    ("EXPOSE",  "Document listening port",       "EXPOSE 8000"),
    ("CMD",     "Default runtime command",       'CMD ["uvicorn", "main:app"]'),
    ("ARG",     "Build-time variable",           "ARG APP_VERSION=1.0"),
    ("LABEL",   "Add metadata to image",         'LABEL maintainer="dev@unigps.in"'),
]

print(f"  {'Instruction':<10} {'Purpose':<30} {'Example'}")
print("  " + "-" * 75)
for instr, purpose, example in instructions:
    print(f"  {instr:<10} {purpose:<30} {example}")

# ============================================================
# Step 3: Write a Proper Dockerfile
# ============================================================

print("\n\n--- Step 3: Write a Proper Dockerfile ---\n")

dockerfile = textwrap.dedent('''\
    # ---- Base Image ----
    FROM python:3.11-slim

    # ---- Metadata ----
    LABEL maintainer="dev@unigps.in"
    LABEL description="UniGPS AI Agent"
    LABEL version="1.0.0"

    # ---- Working Directory ----
    WORKDIR /app

    # ---- Dependencies (cached layer) ----
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # ---- Application Code ----
    COPY . .

    # ---- Environment ----
    ENV PYTHONUNBUFFERED=1
    ENV APP_VERSION=1.0.0

    # ---- Port ----
    EXPOSE 8000

    # ---- Entrypoint ----
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

with open(os.path.join(WORKDIR, "Dockerfile"), "w") as f:
    f.write(dockerfile)

print("  Dockerfile structure:")
print()
for i, line in enumerate(dockerfile.strip().split("\n"), 1):
    tag = ""
    stripped = line.strip()
    if stripped.startswith("FROM"):
        tag = " ← base image layer"
    elif stripped.startswith("COPY requirements"):
        tag = " ← cached dependency layer"
    elif stripped.startswith("RUN pip"):
        tag = " ← install packages (cached if req unchanged)"
    elif stripped.startswith("COPY . ."):
        tag = " ← application code (changes often)"
    elif stripped.startswith("CMD"):
        tag = " ← startup command"
    print(f"    {i:>3}: {line}{tag}")

# ============================================================
# Step 4: Validate the Dockerfile
# ============================================================

print("\n\n--- Step 4: Validate Dockerfile ---\n")

def validate_dockerfile(content):
    """Check a Dockerfile for common best practices."""
    checks = []
    lines = content.strip().split("\n")
    stripped = [l.strip() for l in lines]

    # Check 1: Has FROM
    has_from = any(l.startswith("FROM") for l in stripped)
    checks.append(("Has FROM instruction", has_from))

    # Check 2: Uses slim base
    has_slim = any("slim" in l for l in stripped if l.startswith("FROM"))
    checks.append(("Uses slim base image", has_slim))

    # Check 3: Has WORKDIR
    has_workdir = any(l.startswith("WORKDIR") for l in stripped)
    checks.append(("Has WORKDIR set", has_workdir))

    # Check 4: Layer caching (requirements before code)
    req_idx = None
    code_idx = None
    for i, l in enumerate(stripped):
        if "requirements" in l and l.startswith("COPY"):
            req_idx = i
        if l in ("COPY . .", "COPY . /app"):
            code_idx = i
    if req_idx is not None and code_idx is not None:
        checks.append(("Layer caching (requirements before code)", req_idx < code_idx))
    else:
        checks.append(("Layer caching (requirements before code)", False))

    # Check 5: --no-cache-dir
    has_no_cache = "--no-cache-dir" in content
    checks.append(("Uses --no-cache-dir with pip", has_no_cache))

    # Check 6: PYTHONUNBUFFERED
    has_unbuffered = "PYTHONUNBUFFERED" in content
    checks.append(("Sets PYTHONUNBUFFERED=1", has_unbuffered))

    # Check 7: EXPOSE
    has_expose = any(l.startswith("EXPOSE") for l in stripped)
    checks.append(("Has EXPOSE instruction", has_expose))

    # Check 8: CMD exec form
    has_exec_cmd = 'CMD ["' in content or "CMD ['" in content
    checks.append(("Uses CMD exec form (not shell)", has_exec_cmd))

    return checks

checks = validate_dockerfile(dockerfile)
passed = sum(1 for _, ok in checks if ok)
print(f"  Validation Results ({passed}/{len(checks)} passed):\n")
for check_name, ok in checks:
    status = "PASS" if ok else "FAIL"
    icon = "+" if ok else "-"
    print(f"    [{icon}] {status}: {check_name}")


# ============================================================
# TODO 1: Add LABEL and ARG instructions
# ============================================================

print("\n\n--- TODO 1: Add Build Arguments ---\n")

# TODO: Modify this Dockerfile to:
# 1. Add an ARG for APP_VERSION with default "1.0.0"
# 2. Use that ARG in a LABEL instruction
# 3. Use it as an ENV so the app can read it at runtime
# 4. Add a LABEL for "maintainer" with your name

todo1_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim

    WORKDIR /app

    # TODO: Add ARG for APP_VERSION with default "1.0.0"

    # TODO: Add LABEL with maintainer and version

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    COPY . .

    # TODO: Set ENV APP_VERSION from the ARG

    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# Uncomment and complete:
# todo1_dockerfile = textwrap.dedent('''\
#     FROM python:3.11-slim
#
#     WORKDIR /app
#
#     ARG APP_VERSION=1.0.0
#
#     LABEL maintainer="your-name@unigps.in"
#     LABEL version="${APP_VERSION}"
#     LABEL description="UniGPS AI Agent"
#
#     COPY requirements.txt .
#     RUN pip install --no-cache-dir -r requirements.txt
#
#     COPY . .
#
#     ENV APP_VERSION=${APP_VERSION}
#     ENV PYTHONUNBUFFERED=1
#     EXPOSE 8000
#     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ''')

# Validate
has_arg = "ARG" in todo1_dockerfile and "APP_VERSION" in todo1_dockerfile
has_label = "LABEL" in todo1_dockerfile and "maintainer" in todo1_dockerfile.lower()
has_env_from_arg = "ENV APP_VERSION" in todo1_dockerfile

print(f"  [{'PASS' if has_arg else 'TODO'}] ARG APP_VERSION defined")
print(f"  [{'PASS' if has_label else 'TODO'}] LABEL maintainer added")
print(f"  [{'PASS' if has_env_from_arg else 'TODO'}] ENV set from ARG")


# ============================================================
# TODO 2: Create a Dockerfile for a different app
# ============================================================

print("\n\n--- TODO 2: Dockerfile for a RAG Application ---\n")

# TODO: Write a Dockerfile for a RAG (Retrieval-Augmented Generation) app
# that has these additional requirements:
# - Needs chromadb and sentence-transformers packages
# - Needs a /data directory for vector store persistence
# - Should set TRANSFORMERS_CACHE environment variable
# - Should expose port 8080 instead of 8000

rag_requirements = textwrap.dedent('''\
    fastapi==0.104.1
    uvicorn[standard]==0.24.0
    langchain-core==0.1.23
    chromadb==0.4.22
    sentence-transformers==2.3.1
''')

# TODO: Write the Dockerfile content
todo2_dockerfile = ""

# Uncomment:
# todo2_dockerfile = textwrap.dedent('''\
#     FROM python:3.11-slim
#
#     WORKDIR /app
#
#     COPY requirements.txt .
#     RUN pip install --no-cache-dir -r requirements.txt
#
#     COPY . .
#
#     RUN mkdir -p /data
#
#     ENV PYTHONUNBUFFERED=1
#     ENV TRANSFORMERS_CACHE=/app/.cache/transformers
#
#     EXPOSE 8080
#
#     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
# ''')

if todo2_dockerfile:
    checks = validate_dockerfile(todo2_dockerfile)
    has_data_dir = "/data" in todo2_dockerfile
    has_cache_env = "TRANSFORMERS_CACHE" in todo2_dockerfile
    has_port_8080 = "8080" in todo2_dockerfile

    print(f"  [{'PASS' if has_data_dir else 'FAIL'}] /data directory created")
    print(f"  [{'PASS' if has_cache_env else 'FAIL'}] TRANSFORMERS_CACHE set")
    print(f"  [{'PASS' if has_port_8080 else 'FAIL'}] Port 8080 exposed")

    with open(os.path.join(WORKDIR, "Dockerfile.rag"), "w") as f:
        f.write(todo2_dockerfile)
    with open(os.path.join(WORKDIR, "requirements-rag.txt"), "w") as f:
        f.write(rag_requirements)
    print(f"\n  Saved Dockerfile.rag to {WORKDIR}/")
else:
    print("  TODO: Write a Dockerfile for the RAG application")
    print("  Hints:")
    print("    - Start with FROM python:3.11-slim")
    print("    - Create a /data directory with RUN mkdir -p /data")
    print("    - Set TRANSFORMERS_CACHE=/app/.cache/transformers")
    print("    - Expose port 8080")


# ============================================================
# Summary
# ============================================================

print("\n\n--- Lab 02 Summary ---\n")
print("  Key Dockerfile patterns for AI apps:")
print("    1. FROM python:3.11-slim (small but compatible)")
print("    2. COPY requirements.txt first, then pip install (layer caching)")
print("    3. COPY . . last (code changes don't bust dependency cache)")
print("    4. ENV PYTHONUNBUFFERED=1 (logs appear in docker logs)")
print("    5. CMD exec form [\"cmd\", \"arg\"] (proper signal handling)")
print(f"\n  Files in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    print(f"    {f}")
