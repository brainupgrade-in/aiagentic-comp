"""
Lab 06 Solution: Security Hardening
=======================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-06"

print("=" * 50)
print("  Lab 06 Solution: Security Hardening")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# Create app files
health_app = textwrap.dedent('''\
    """UniGPS AI Agent — with health endpoint"""
    import os
    from datetime import datetime
    from fastapi import FastAPI

    app = FastAPI(title="UniGPS Agent", version="2.0.0")
    _start_time = datetime.now()

    @app.get("/health")
    async def health():
        uptime = (datetime.now() - _start_time).total_seconds()
        return {
            "status": "healthy",
            "agent": "ready",
            "version": os.getenv("APP_VERSION", "2.0.0"),
            "uptime_seconds": round(uptime, 1),
        }

    @app.get("/")
    async def root():
        return {"message": "UniGPS AI Agent is running"}
''')

requirements = textwrap.dedent('''\
    fastapi==0.104.1
    uvicorn[standard]==0.24.0
    pydantic==2.5.0
''')

with open(os.path.join(WORKDIR, "main.py"), "w") as f:
    f.write(health_app)
with open(os.path.join(WORKDIR, "requirements.txt"), "w") as f:
    f.write(requirements)


# ============================================================
# TODO 1 Solution: Complete secure Dockerfile
# ============================================================

print("\n--- TODO 1 Solution: Secure Dockerfile ---\n")

todo1_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim AS builder
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

    FROM python:3.11-slim
    WORKDIR /app

    RUN apt-get update && apt-get install -y --no-install-recommends curl \\
        && rm -rf /var/lib/apt/lists/*

    COPY --from=builder /install /usr/local

    RUN useradd --create-home appuser

    COPY --chown=appuser:appuser . .

    USER appuser

    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000

    HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
        CMD curl -f http://localhost:8000/health || exit 1

    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

checks = {
    "curl installed": "curl" in todo1_dockerfile and "apt-get" in todo1_dockerfile,
    "Non-root user created": "useradd" in todo1_dockerfile,
    "File ownership set": "--chown" in todo1_dockerfile,
    "USER instruction": "\nUSER " in todo1_dockerfile,
    "HEALTHCHECK added": "HEALTHCHECK" in todo1_dockerfile,
}

passed = sum(1 for v in checks.values() if v)
print(f"  Security checks ({passed}/{len(checks)}):")
for name, ok in checks.items():
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

with open(os.path.join(WORKDIR, "Dockerfile"), "w") as f:
    f.write(todo1_dockerfile)

print("\n  Security features added:")
print("    1a. curl for health checks (apt-get install, clean cache)")
print("    1b. useradd --create-home appuser")
print("    1c. COPY --chown=appuser:appuser . .")
print("    1d. USER appuser")
print("    1e. HEALTHCHECK --interval=30s --timeout=5s --retries=3")


# ============================================================
# TODO 2 Solution: Security validator
# ============================================================

print("\n\n--- TODO 2 Solution: Security Validator ---\n")

def validate_security(dockerfile_content: str) -> list:
    """Validate Dockerfile for security best practices."""
    checks = []

    # Check 1 (HIGH): Non-root USER
    has_user = "USER " in dockerfile_content and "USER root" not in dockerfile_content
    checks.append(("Non-root USER", has_user, "HIGH"))

    # Check 2 (HIGH): No .env in COPY
    copies_env = any(
        ".env" in l for l in dockerfile_content.split("\n")
        if l.strip().startswith("COPY") and "chown" not in l.lower()
        and l.strip() not in ("COPY . .", "COPY --chown=appuser:appuser . .")
    )
    checks.append(("No .env in COPY", not copies_env, "HIGH"))

    # Check 3 (MEDIUM): Has HEALTHCHECK
    has_healthcheck = "HEALTHCHECK" in dockerfile_content
    checks.append(("Has HEALTHCHECK", has_healthcheck, "MEDIUM"))

    # Check 4 (MEDIUM): --no-cache-dir
    has_no_cache = "--no-cache-dir" in dockerfile_content
    checks.append(("pip --no-cache-dir", has_no_cache, "MEDIUM"))

    # Check 5 (LOW): Uses slim/alpine
    has_slim = "slim" in dockerfile_content or "alpine" in dockerfile_content
    checks.append(("Uses slim/alpine base", has_slim, "LOW"))

    # Check 6 (LOW): Cleans apt cache
    cleans_apt = "rm -rf /var/lib/apt" in dockerfile_content
    checks.append(("Cleans apt cache", cleans_apt, "LOW"))

    return checks


# Test against the secure Dockerfile
print("  Scan: Secure Dockerfile (our solution)")
results = validate_security(todo1_dockerfile)
for name, ok, severity in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] [{severity}] {name}")

# Test against an insecure Dockerfile
print("\n  Scan: Insecure Dockerfile (for comparison)")
insecure = textwrap.dedent('''\
    FROM python:3.11
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.txt
    CMD python main.py
''')
results = validate_security(insecure)
for name, ok, severity in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] [{severity}] {name}")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 06 Solution complete!")
print("- TODO 1: Secure Dockerfile (non-root, healthcheck, curl, chown)")
print("- TODO 2: Security validator (6 checks: HIGH/MEDIUM/LOW severity)")
