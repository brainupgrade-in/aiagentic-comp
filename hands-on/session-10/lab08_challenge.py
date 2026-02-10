"""
Lab 08 Challenge: Complete Production Docker Setup for UniGPS
================================================================
Combine everything from Labs 01-07 into a production-ready Docker setup.

Your goal: Create a complete, production-quality Docker configuration
for the UniGPS AI Agent that includes ALL best practices.

If Docker is available, you can build and run the entire stack!
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-08"

print("=" * 60)
print("  Challenge: Complete Production Docker Setup")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# The Application (provided — don't modify)
# ============================================================

app_code = textwrap.dedent('''\
    """UniGPS AI Agent — Production Application"""
    import os
    import time
    from datetime import datetime
    from functools import lru_cache
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field

    app = FastAPI(
        title="UniGPS Production Agent API",
        version="2.0.0",
        description="Production-ready AI support agent",
    )

    _start_time = datetime.now()
    _request_count = 0

    TEMPLATES = {
        "hr": "Please visit the HR portal or email hr@unigps.in.",
        "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
        "finance": "Please email finance@unigps.in with details.",
        "general": "Your request has been noted. A team member will respond shortly.",
    }

    class SupportRequest(BaseModel):
        employee_name: str = Field(..., min_length=2, max_length=100)
        request: str = Field(..., min_length=5, max_length=1000)

    class SupportResponse(BaseModel):
        ticket_id: str
        category: str
        response: str
        timing_ms: float

    @lru_cache(maxsize=200)
    def classify(text: str) -> str:
        """Classify request by keywords (cached)."""
        text = text.lower()
        if any(w in text for w in ["leave", "salary", "hr", "vacation", "payroll"]):
            return "hr"
        elif any(w in text for w in ["server", "bug", "deploy", "error", "crash"]):
            return "tech"
        elif any(w in text for w in ["expense", "invoice", "budget", "reimburse"]):
            return "finance"
        return "general"

    @app.get("/health")
    async def health():
        uptime = (datetime.now() - _start_time).total_seconds()
        cache = classify.cache_info()
        return {
            "status": "healthy",
            "agent": "ready",
            "version": os.getenv("APP_VERSION", "2.0.0"),
            "uptime_seconds": round(uptime, 1),
            "total_requests": _request_count,
            "cache_hits": cache.hits,
            "cache_size": cache.currsize,
        }

    @app.post("/api/support", response_model=SupportResponse)
    async def handle_support(req: SupportRequest):
        global _request_count
        _request_count += 1
        start = time.time()

        category = classify(req.request)
        response_text = f"[{category.upper()}] {TEMPLATES[category]}"
        elapsed_ms = (time.time() - start) * 1000

        return SupportResponse(
            ticket_id=f"TKT-{_request_count:04d}",
            category=category,
            response=response_text,
            timing_ms=round(elapsed_ms, 2),
        )

    @app.get("/api/stats")
    async def stats():
        cache = classify.cache_info()
        return {
            "total_requests": _request_count,
            "cache": {
                "hits": cache.hits,
                "misses": cache.misses,
                "size": cache.currsize,
            },
        }
''')

requirements = textwrap.dedent('''\
    fastapi==0.104.1
    uvicorn[standard]==0.24.0
    pydantic==2.5.0
    langchain-core==0.1.23
    langchain-groq==0.0.3
    langgraph==0.0.26
    python-dotenv==1.0.0
    redis==5.0.1
    httpx==0.25.2
''')

test_code = textwrap.dedent('''\
    """Tests for the UniGPS Agent API"""
    from fastapi.testclient import TestClient
    from main import app

    client = TestClient(app)

    def test_health():
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    def test_support_hr():
        resp = client.post("/api/support", json={
            "employee_name": "Priya",
            "request": "I need sick leave for 3 days",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert data["category"] == "hr"
        assert data["ticket_id"].startswith("TKT-")

    def test_support_tech():
        resp = client.post("/api/support", json={
            "employee_name": "Vikram",
            "request": "Production server is down",
        })
        assert resp.status_code == 200
        assert resp.json()["category"] == "tech"

    def test_validation():
        resp = client.post("/api/support", json={
            "employee_name": "P",
            "request": "Hi",
        })
        assert resp.status_code == 422

    def test_stats():
        resp = client.get("/api/stats")
        assert resp.status_code == 200
        assert "cache" in resp.json()
''')

# Write application files
with open(os.path.join(WORKDIR, "main.py"), "w") as f:
    f.write(app_code)
with open(os.path.join(WORKDIR, "requirements.txt"), "w") as f:
    f.write(requirements)
os.makedirs(os.path.join(WORKDIR, "tests"), exist_ok=True)
with open(os.path.join(WORKDIR, "tests", "test_main.py"), "w") as f:
    f.write(test_code)
with open(os.path.join(WORKDIR, "tests", "__init__.py"), "w") as f:
    f.write("")

print(f"\n  Application files created in {WORKDIR}/:")
print(f"    main.py            — FastAPI app with /health, /api/support, /api/stats")
print(f"    requirements.txt   — 9 dependencies")
print(f"    tests/test_main.py — 5 tests")


# ============================================================
# YOUR CHALLENGE: Create ALL Docker files
# ============================================================

print("\n\n" + "=" * 60)
print("  YOUR CHALLENGE")
print("=" * 60)
print()
print("  Create the following 4 files:")
print("    1. Dockerfile          — Multi-stage, non-root, health check")
print("    2. .dockerignore       — Exclude unnecessary files")
print("    3. docker-compose.yml  — Agent + Redis + test runner")
print("    4. .env.example        — Template for required env vars")
print()
print("  Requirements:")
print("    - Multi-stage build (builder → runtime)")
print("    - Non-root user (appuser)")
print("    - HEALTHCHECK instruction")
print("    - Layer caching (requirements before code)")
print("    - .dockerignore excludes .git, .env, __pycache__, etc.")
print("    - docker-compose with agent + redis + health checks")
print("    - .env.example documents required environment variables")

# ============================================================
# TODO 1: Production Dockerfile
# ============================================================

print("\n\n--- TODO 1: Production Dockerfile ---\n")

# TODO: Write a production Dockerfile with ALL best practices:
# - Multi-stage build (builder → runtime)
# - Non-root user
# - HEALTHCHECK
# - Layer caching
# - --no-cache-dir
# - curl for health checks
# - Proper ENV settings

challenge_dockerfile = ""  # Write your Dockerfile here

# Uncomment:
# challenge_dockerfile = textwrap.dedent('''\
#     # Stage 1: Builder
#     FROM python:3.11-slim AS builder
#     WORKDIR /app
#     COPY requirements.txt .
#     RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
#
#     # Stage 2: Runtime
#     FROM python:3.11-slim
#     WORKDIR /app
#
#     # Install curl for health checks
#     RUN apt-get update && apt-get install -y --no-install-recommends curl \\
#         && rm -rf /var/lib/apt/lists/*
#
#     # Copy installed packages from builder
#     COPY --from=builder /install /usr/local
#
#     # Create non-root user
#     RUN useradd --create-home appuser
#
#     # Copy application code
#     COPY --chown=appuser:appuser . .
#
#     # Switch to non-root user
#     USER appuser
#
#     # Environment
#     ENV PYTHONUNBUFFERED=1
#     ENV APP_VERSION=2.0.0
#
#     # Port
#     EXPOSE 8000
#
#     # Health check
#     HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
#         CMD curl -f http://localhost:8000/health || exit 1
#
#     # Start
#     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ''')


# ============================================================
# TODO 2: .dockerignore + docker-compose.yml + .env.example
# ============================================================

print("--- TODO 2: .dockerignore + docker-compose.yml + .env.example ---\n")

challenge_dockerignore = ""    # Write your .dockerignore
challenge_compose = ""         # Write your docker-compose.yml
challenge_env_example = ""     # Write your .env.example

# Uncomment:
# challenge_dockerignore = textwrap.dedent('''\
#     # Version control
#     .git
#     .gitignore
#
#     # Python
#     __pycache__
#     *.pyc
#     *.pyo
#     .venv/
#     venv/
#     *.egg-info
#
#     # Environment (secrets!)
#     .env
#     .env.*
#     !.env.example
#
#     # IDE
#     .vscode/
#     .idea/
#     .mypy_cache
#     .pytest_cache
#
#     # Docker
#     Dockerfile
#     Dockerfile.*
#     docker-compose*.yml
#     .dockerignore
#
#     # Docs
#     docs/
#     *.md
# ''')

# challenge_compose = textwrap.dedent('''\
#     services:
#       agent:
#         build:
#           context: .
#           dockerfile: Dockerfile
#         ports:
#           - "8000:8000"
#         environment:
#           - PYTHONUNBUFFERED=1
#           - REDIS_URL=redis://redis:6379
#         env_file:
#           - .env
#         depends_on:
#           redis:
#             condition: service_healthy
#         healthcheck:
#           test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
#           interval: 30s
#           timeout: 5s
#           retries: 3
#           start_period: 10s
#         restart: unless-stopped
#
#       redis:
#         image: redis:7-alpine
#         ports:
#           - "6379:6379"
#         volumes:
#           - redis-data:/data
#         healthcheck:
#           test: ["CMD", "redis-cli", "ping"]
#           interval: 10s
#           timeout: 3s
#           retries: 3
#         restart: unless-stopped
#
#     volumes:
#       redis-data:
# ''')

# challenge_env_example = textwrap.dedent('''\
#     # UniGPS AI Agent — Environment Variables
#     # Copy this file to .env and fill in your values
#
#     # Required: LLM API Key
#     GROQ_API_KEY=your-groq-api-key-here
#
#     # Optional: Application settings
#     APP_VERSION=2.0.0
#     LOG_LEVEL=info
#
#     # Optional: Redis (defaults are fine for docker-compose)
#     REDIS_URL=redis://redis:6379
# ''')


# ============================================================
# Validation
# ============================================================

print("\n--- Challenge Validation ---\n")

def validate_challenge():
    """Validate all challenge deliverables."""
    results = []

    # Dockerfile checks
    if challenge_dockerfile:
        results.append(("Dockerfile created", True))
        results.append(("Multi-stage (2+ FROM)", challenge_dockerfile.count("FROM ") >= 2))
        results.append(("Builder stage (AS builder)", " AS " in challenge_dockerfile))
        results.append(("COPY --from=builder", "--from=builder" in challenge_dockerfile))
        results.append(("Non-root user (useradd)", "useradd" in challenge_dockerfile))
        results.append(("USER instruction", "\nUSER " in challenge_dockerfile))
        results.append(("HEALTHCHECK added", "HEALTHCHECK" in challenge_dockerfile))
        results.append(("--no-cache-dir", "--no-cache-dir" in challenge_dockerfile))
        results.append(("Layer caching (req before code)",
            challenge_dockerfile.find("requirements.txt") < challenge_dockerfile.rfind("COPY . .")
            if "COPY . ." in challenge_dockerfile else False))
        results.append(("curl installed", "curl" in challenge_dockerfile))
        results.append(("PYTHONUNBUFFERED=1", "PYTHONUNBUFFERED" in challenge_dockerfile))
        results.append(("CMD exec form", 'CMD ["' in challenge_dockerfile))

        with open(os.path.join(WORKDIR, "Dockerfile"), "w") as f:
            f.write(challenge_dockerfile)
    else:
        results.append(("Dockerfile created", False))

    # .dockerignore checks
    if challenge_dockerignore:
        results.append((".dockerignore created", True))
        results.append(("Excludes .git", ".git" in challenge_dockerignore))
        results.append(("Excludes .env", ".env" in challenge_dockerignore))
        results.append(("Excludes __pycache__", "__pycache__" in challenge_dockerignore))
        results.append(("Excludes .venv", ".venv" in challenge_dockerignore or "venv" in challenge_dockerignore))

        with open(os.path.join(WORKDIR, ".dockerignore"), "w") as f:
            f.write(challenge_dockerignore)
    else:
        results.append((".dockerignore created", False))

    # docker-compose.yml checks
    if challenge_compose:
        results.append(("docker-compose.yml created", True))
        results.append(("Agent service defined", "agent" in challenge_compose))
        results.append(("Redis service defined", "redis" in challenge_compose))
        results.append(("depends_on used", "depends_on" in challenge_compose))
        results.append(("Volumes defined", "volumes:" in challenge_compose))
        results.append(("Health checks in compose", "healthcheck" in challenge_compose))

        with open(os.path.join(WORKDIR, "docker-compose.yml"), "w") as f:
            f.write(challenge_compose)
    else:
        results.append(("docker-compose.yml created", False))

    # .env.example checks
    if challenge_env_example:
        results.append((".env.example created", True))
        results.append(("Documents GROQ_API_KEY", "GROQ_API_KEY" in challenge_env_example))

        with open(os.path.join(WORKDIR, ".env.example"), "w") as f:
            f.write(challenge_env_example)
    else:
        results.append((".env.example created", False))

    return results

results = validate_challenge()
passed = sum(1 for _, ok in results if ok)
total = len(results)

print(f"  Results: {passed}/{total} checks passed\n")
for name, ok in results:
    icon = "+" if ok else "-"
    print(f"    [{icon}] {'PASS' if ok else 'TODO'}: {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Challenge Summary ---\n")

grade = passed / total * 100 if total > 0 else 0

if grade >= 90:
    status = "Excellent! Production-ready Docker setup!"
elif grade >= 70:
    status = "Good progress! A few patterns to add."
elif grade >= 40:
    status = "Getting there — review the solution for missing pieces."
else:
    status = "Start with the Dockerfile, then add the other files."

print(f"  Score: {passed}/{total} ({grade:.0f}%)")
print(f"  Status: {status}")

print(f"\n  Files in {WORKDIR}/:")
for root, dirs, files in os.walk(WORKDIR):
    for f in sorted(files):
        rel = os.path.relpath(os.path.join(root, f), WORKDIR)
        size = os.path.getsize(os.path.join(root, f))
        print(f"    {rel:<30} ({size} bytes)")

docker_available = shutil.which("docker") is not None
if docker_available and grade >= 70:
    print(f"\n  Docker detected! Try building:")
    print(f"    cd {WORKDIR}")
    print(f"    docker build -t unigps-agent:2.0 .")
    print(f"    docker run -p 8000:8000 unigps-agent:2.0")
    print(f"    # Open http://localhost:8000/health")
    print(f"    # Or: docker compose up -d (needs all files)")
elif not docker_available:
    print(f"\n  Docker not installed — files are still valid.")
    print(f"  You can build them on any machine with Docker.")
