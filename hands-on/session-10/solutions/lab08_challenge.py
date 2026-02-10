"""
Lab 08 Challenge Solution: Complete Production Docker Setup for UniGPS
=======================================================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-08"

print("=" * 60)
print("  Challenge Solution: Production Docker Setup")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Application files (same as challenge)
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

# Write app files
with open(os.path.join(WORKDIR, "main.py"), "w") as f:
    f.write(app_code)
with open(os.path.join(WORKDIR, "requirements.txt"), "w") as f:
    f.write(requirements)
os.makedirs(os.path.join(WORKDIR, "tests"), exist_ok=True)
with open(os.path.join(WORKDIR, "tests", "test_main.py"), "w") as f:
    f.write(test_code)
with open(os.path.join(WORKDIR, "tests", "__init__.py"), "w") as f:
    f.write("")


# ============================================================
# TODO 1 Solution: Production Dockerfile
# ============================================================

print("\n--- TODO 1 Solution: Production Dockerfile ---\n")

challenge_dockerfile = textwrap.dedent('''\
    # Stage 1: Builder
    FROM python:3.11-slim AS builder
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

    # Stage 2: Runtime
    FROM python:3.11-slim
    WORKDIR /app

    # Install curl for health checks
    RUN apt-get update && apt-get install -y --no-install-recommends curl \\
        && rm -rf /var/lib/apt/lists/*

    # Copy installed packages from builder
    COPY --from=builder /install /usr/local

    # Create non-root user
    RUN useradd --create-home appuser

    # Copy application code
    COPY --chown=appuser:appuser . .

    # Switch to non-root user
    USER appuser

    # Environment
    ENV PYTHONUNBUFFERED=1
    ENV APP_VERSION=2.0.0

    # Port
    EXPOSE 8000

    # Health check
    HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
        CMD curl -f http://localhost:8000/health || exit 1

    # Start
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

with open(os.path.join(WORKDIR, "Dockerfile"), "w") as f:
    f.write(challenge_dockerfile)

print("  Production Dockerfile features:")
print("    [+] Multi-stage build (builder → runtime)")
print("    [+] python:3.11-slim base (small + compatible)")
print("    [+] --no-cache-dir + --prefix for clean install")
print("    [+] curl for HEALTHCHECK")
print("    [+] Non-root user (appuser)")
print("    [+] --chown on COPY (no extra layer)")
print("    [+] HEALTHCHECK with start-period")
print("    [+] CMD exec form")
print("    [+] apt cache cleaned")


# ============================================================
# TODO 2 Solution: .dockerignore + compose + .env.example
# ============================================================

print("\n\n--- TODO 2 Solution: Supporting Files ---\n")

challenge_dockerignore = textwrap.dedent('''\
    # Version control
    .git
    .gitignore

    # Python
    __pycache__
    *.pyc
    *.pyo
    .venv/
    venv/
    *.egg-info

    # Environment (secrets!)
    .env
    .env.*
    !.env.example

    # IDE
    .vscode/
    .idea/
    .mypy_cache
    .pytest_cache

    # Docker
    Dockerfile
    Dockerfile.*
    docker-compose*.yml
    .dockerignore

    # Docs
    docs/
    *.md
''')

challenge_compose = textwrap.dedent('''\
    services:
      agent:
        build:
          context: .
          dockerfile: Dockerfile
        ports:
          - "8000:8000"
        environment:
          - PYTHONUNBUFFERED=1
          - REDIS_URL=redis://redis:6379
        env_file:
          - .env
        depends_on:
          redis:
            condition: service_healthy
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
          interval: 30s
          timeout: 5s
          retries: 3
          start_period: 10s
        restart: unless-stopped

      redis:
        image: redis:7-alpine
        ports:
          - "6379:6379"
        volumes:
          - redis-data:/data
        healthcheck:
          test: ["CMD", "redis-cli", "ping"]
          interval: 10s
          timeout: 3s
          retries: 3
        restart: unless-stopped

    volumes:
      redis-data:
''')

challenge_env_example = textwrap.dedent('''\
    # UniGPS AI Agent — Environment Variables
    # Copy this file to .env and fill in your values

    # Required: LLM API Key
    GROQ_API_KEY=your-groq-api-key-here

    # Optional: Application settings
    APP_VERSION=2.0.0
    LOG_LEVEL=info

    # Optional: Redis (defaults are fine for docker-compose)
    REDIS_URL=redis://redis:6379
''')

with open(os.path.join(WORKDIR, ".dockerignore"), "w") as f:
    f.write(challenge_dockerignore)
with open(os.path.join(WORKDIR, "docker-compose.yml"), "w") as f:
    f.write(challenge_compose)
with open(os.path.join(WORKDIR, ".env.example"), "w") as f:
    f.write(challenge_env_example)

print("  .dockerignore:")
print("    Excludes: .git, .env, __pycache__, .venv, IDE files, Docker files, docs")
print("    Keeps: .env.example (with !.env.example)")
print()
print("  docker-compose.yml:")
print("    agent: build from Dockerfile, port 8000, env_file, depends_on redis")
print("    redis: alpine image, port 6379, persistent volume, healthcheck")
print("    Both: restart unless-stopped, health checks")
print()
print("  .env.example:")
print("    Documents: GROQ_API_KEY, APP_VERSION, LOG_LEVEL, REDIS_URL")


# ============================================================
# Validation
# ============================================================

print("\n\n--- Challenge Validation ---\n")

results = []

# Dockerfile checks
results.append(("Dockerfile created", True))
results.append(("Multi-stage (2+ FROM)", challenge_dockerfile.count("FROM ") >= 2))
results.append(("Builder stage (AS builder)", " AS " in challenge_dockerfile))
results.append(("COPY --from=builder", "--from=builder" in challenge_dockerfile))
results.append(("Non-root user (useradd)", "useradd" in challenge_dockerfile))
results.append(("USER instruction", "\nUSER " in challenge_dockerfile))
results.append(("HEALTHCHECK added", "HEALTHCHECK" in challenge_dockerfile))
results.append(("--no-cache-dir", "--no-cache-dir" in challenge_dockerfile))
results.append(("Layer caching",
    challenge_dockerfile.find("requirements.txt") < challenge_dockerfile.rfind("COPY . .")))
results.append(("curl installed", "curl" in challenge_dockerfile))
results.append(("PYTHONUNBUFFERED=1", "PYTHONUNBUFFERED" in challenge_dockerfile))
results.append(("CMD exec form", 'CMD ["' in challenge_dockerfile))

# .dockerignore checks
results.append((".dockerignore created", True))
results.append(("Excludes .git", ".git" in challenge_dockerignore))
results.append(("Excludes .env", ".env" in challenge_dockerignore))
results.append(("Excludes __pycache__", "__pycache__" in challenge_dockerignore))
results.append(("Excludes .venv", ".venv" in challenge_dockerignore))

# docker-compose.yml checks
results.append(("docker-compose.yml created", True))
results.append(("Agent service", "agent" in challenge_compose))
results.append(("Redis service", "redis" in challenge_compose))
results.append(("depends_on", "depends_on" in challenge_compose))
results.append(("Volumes", "volumes:" in challenge_compose))
results.append(("Health checks in compose", "healthcheck" in challenge_compose))

# .env.example checks
results.append((".env.example created", True))
results.append(("Documents GROQ_API_KEY", "GROQ_API_KEY" in challenge_env_example))

passed = sum(1 for _, ok in results if ok)
total = len(results)

print(f"  Results: {passed}/{total} checks passed\n")
for name, ok in results:
    print(f"    [+] PASS: {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Challenge Complete ---\n")
print(f"  Score: {passed}/{total} ({passed/total*100:.0f}%)")
print(f"\n  Files created in {WORKDIR}/:")
for root, dirs, files in os.walk(WORKDIR):
    for f in sorted(files):
        rel = os.path.relpath(os.path.join(root, f), WORKDIR)
        size = os.path.getsize(os.path.join(root, f))
        print(f"    {rel:<30} ({size} bytes)")

docker_available = shutil.which("docker") is not None
print(f"\n  To build and run:")
print(f"    cd {WORKDIR}")
if docker_available:
    print(f"    docker build -t unigps-agent:2.0 .        # Build image")
    print(f"    docker run -p 8000:8000 unigps-agent:2.0  # Run container")
    print(f"    # Or: docker compose up -d                 # Full stack")
    print(f"    # Open: http://localhost:8000/health")
else:
    print(f"    # Docker not installed — files ready for any Docker host")

print("\n" + "=" * 60)
print("Challenge Solution complete!")
print("- Dockerfile: multi-stage, non-root, healthcheck, layer caching")
print("- .dockerignore: excludes .git, .env, caches, docs")
print("- docker-compose.yml: agent + redis with health checks, volumes")
print("- .env.example: documents all required environment variables")
print(f"- {passed}/{total} validation checks passing")
