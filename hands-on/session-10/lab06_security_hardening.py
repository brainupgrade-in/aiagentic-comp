"""
Lab 06: Security Hardening
=============================
Non-root users, health checks, and environment variable management.

No Docker installation required — generates and validates Dockerfiles.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-06"

print("=" * 50)
print("  Lab 06: Security Hardening")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Why Non-Root Users?
# ============================================================

print("\n--- Step 1: Why Non-Root Users? ---\n")

print("  By default, Docker containers run as root (UID 0).")
print("  This means if your app is compromised, the attacker has root access!")
print()

scenarios = [
    {
        "name": "Root container (default)",
        "user": "root (UID 0)",
        "risk": "HIGH",
        "attacker_can": [
            "Install backdoors (apt-get install ...)",
            "Read /etc/shadow (password hashes)",
            "Modify system files",
            "Potentially escape to host",
        ],
    },
    {
        "name": "Non-root container (hardened)",
        "user": "appuser (UID 1000)",
        "risk": "LOW",
        "attacker_can": [
            "Only read/write files owned by appuser",
            "Cannot install system packages",
            "Cannot access sensitive system files",
            "Much harder to escalate privileges",
        ],
    },
]

for s in scenarios:
    print(f"  {s['name']}:")
    print(f"    User: {s['user']}")
    print(f"    Risk: {s['risk']}")
    print(f"    If compromised, attacker can:")
    for item in s["attacker_can"]:
        print(f"      - {item}")
    print()


# ============================================================
# Step 2: Adding a Non-Root User
# ============================================================

print("\n--- Step 2: Non-Root User Dockerfile ---\n")

nonroot_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim

    WORKDIR /app

    # Install dependencies as root (needs write access to /usr/local)
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    # Create a non-root user
    RUN useradd --create-home --shell /bin/bash appuser

    # Copy application code and set ownership
    COPY --chown=appuser:appuser . .

    # Switch to non-root user (all subsequent commands run as appuser)
    USER appuser

    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

with open(os.path.join(WORKDIR, "Dockerfile.nonroot"), "w") as f:
    f.write(nonroot_dockerfile)

print("  Key instructions:")
print()
print("    RUN useradd --create-home --shell /bin/bash appuser")
print("        ↑ Create user BEFORE copying app files")
print()
print("    COPY --chown=appuser:appuser . .")
print("        ↑ Set file ownership during copy (no extra RUN layer)")
print()
print("    USER appuser")
print("        ↑ Switch user AFTER installing deps (pip needs root)")
print()
print("  Order matters:")
print("    1. Install deps (as root) → needs /usr/local write access")
print("    2. Create user")
print("    3. Copy code with --chown")
print("    4. Switch to non-root user")
print("    5. CMD runs as appuser")


# ============================================================
# Step 3: Health Checks
# ============================================================

print("\n\n--- Step 3: Docker Health Checks ---\n")

healthcheck_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim

    WORKDIR /app

    # Install curl for health checks
    RUN apt-get update && apt-get install -y --no-install-recommends curl \\
        && rm -rf /var/lib/apt/lists/*

    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt

    RUN useradd --create-home appuser
    COPY --chown=appuser:appuser . .
    USER appuser

    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000

    # Health check: Docker will call this every 30s
    HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
        CMD curl -f http://localhost:8000/health || exit 1

    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

with open(os.path.join(WORKDIR, "Dockerfile.healthcheck"), "w") as f:
    f.write(healthcheck_dockerfile)

print("  HEALTHCHECK instruction:")
print()
print("    HEALTHCHECK --interval=30s --timeout=5s --retries=3 \\")
print("        CMD curl -f http://localhost:8000/health || exit 1")
print()
print("  Parameters:")

params = [
    ("--interval=30s",      "How often to run the check (every 30 seconds)"),
    ("--timeout=5s",        "Max time to wait for a response"),
    ("--start-period=10s",  "Grace period for app startup (no checks)"),
    ("--retries=3",         "How many failures before 'unhealthy'"),
]
for param, desc in params:
    print(f"    {param:<22} {desc}")

print()
print("  Container states: starting → healthy → unhealthy")
print("  Docker and Kubernetes use this to restart unhealthy containers.")


# ============================================================
# Step 4: FastAPI Health Endpoint
# ============================================================

print("\n\n--- Step 4: FastAPI Health Endpoint ---\n")

health_app = textwrap.dedent('''\
    """UniGPS AI Agent — with health endpoint for Docker HEALTHCHECK"""
    import os
    from datetime import datetime
    from fastapi import FastAPI

    app = FastAPI(title="UniGPS Agent", version="2.0.0")

    _start_time = datetime.now()

    @app.get("/health")
    async def health():
        """Health check endpoint for Docker HEALTHCHECK."""
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

print("  The /health endpoint returns:")
print('    {"status": "healthy", "agent": "ready", "uptime_seconds": 42.5}')
print()
print("  Docker HEALTHCHECK calls this endpoint periodically.")
print("  If it returns non-200 or times out → container marked unhealthy.")


# ============================================================
# Step 5: Environment Variable Management
# ============================================================

print("\n\n--- Step 5: Environment Variable Management ---\n")

print("  Three ways to set environment variables in Docker:\n")

methods = [
    ("ENV in Dockerfile",
     "ENV PYTHONUNBUFFERED=1",
     "Baked into image. Good for non-secret config.",
     "Use for: PYTHONUNBUFFERED, APP_VERSION, WORKERS"),
    ("docker run -e",
     "docker run -e GROQ_API_KEY=xxx myapp",
     "Set at runtime. Good for secrets.",
     "Use for: API keys, database URLs, secrets"),
    (".env file + --env-file",
     "docker run --env-file .env myapp",
     "Load from file at runtime. Good for many vars.",
     "Use for: Multiple environment-specific settings"),
]

for name, example, desc, use_for in methods:
    print(f"  {name}:")
    print(f"    Example: {example}")
    print(f"    {desc}")
    print(f"    {use_for}")
    print()

print("  NEVER put secrets in ENV instructions!")
print("  They are visible in 'docker inspect' and 'docker history'.")


# ============================================================
# TODO 1: Complete the secure Dockerfile
# ============================================================

print("\n\n--- TODO 1: Complete the Secure Dockerfile ---\n")

# TODO: Fill in the missing security features in this Dockerfile.
# It needs: non-root user, health check, proper ENV management.

todo1_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim AS builder
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

    FROM python:3.11-slim
    WORKDIR /app

    # TODO 1a: Install curl for health checks (and clean up apt cache)

    COPY --from=builder /install /usr/local

    # TODO 1b: Create a non-root user called "appuser"

    COPY . .

    # TODO 1c: Set ownership of /app to appuser (hint: use --chown above or chown here)

    # TODO 1d: Switch to the non-root user

    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000

    # TODO 1e: Add a HEALTHCHECK that checks /health every 30s

    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

# Uncomment with your solution:
# todo1_dockerfile = textwrap.dedent('''\
#     FROM python:3.11-slim AS builder
#     WORKDIR /app
#     COPY requirements.txt .
#     RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
#
#     FROM python:3.11-slim
#     WORKDIR /app
#
#     RUN apt-get update && apt-get install -y --no-install-recommends curl \\
#         && rm -rf /var/lib/apt/lists/*
#
#     COPY --from=builder /install /usr/local
#
#     RUN useradd --create-home appuser
#
#     COPY --chown=appuser:appuser . .
#
#     USER appuser
#
#     ENV PYTHONUNBUFFERED=1
#     EXPOSE 8000
#
#     HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \\
#         CMD curl -f http://localhost:8000/health || exit 1
#
#     CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
# ''')

# Validate
checks = {
    "curl installed": "curl" in todo1_dockerfile and "apt-get" in todo1_dockerfile,
    "Non-root user created": "useradd" in todo1_dockerfile,
    "File ownership set": "--chown" in todo1_dockerfile or "chown" in todo1_dockerfile,
    "USER instruction": "\nUSER " in todo1_dockerfile or todo1_dockerfile.startswith("USER "),
    "HEALTHCHECK added": "HEALTHCHECK" in todo1_dockerfile,
}

passed = sum(1 for v in checks.values() if v)
print(f"  Security checks ({passed}/{len(checks)}):")
for name, ok in checks.items():
    print(f"    [{'PASS' if ok else 'TODO'}] {name}")


# ============================================================
# TODO 2: Write a security checklist validator
# ============================================================

print("\n\n--- TODO 2: Dockerfile Security Validator ---\n")

# TODO: Write a function that checks a Dockerfile for security issues.
# Return a list of (check_name, passed, severity) tuples.

def validate_security(dockerfile_content: str) -> list:
    """Validate Dockerfile for security best practices."""
    checks = []

    # TODO: Implement these checks:

    # Check 1 (HIGH): Has USER instruction (non-root)
    # Check 2 (HIGH): No .env COPY (secrets in image)
    # Check 3 (MEDIUM): Has HEALTHCHECK
    # Check 4 (MEDIUM): Uses --no-cache-dir with pip
    # Check 5 (LOW): Uses slim or alpine base
    # Check 6 (LOW): Cleans apt cache (rm -rf /var/lib/apt/lists/*)

    # Uncomment:
    # has_user = "USER " in dockerfile_content and "USER root" not in dockerfile_content
    # checks.append(("Non-root USER", has_user, "HIGH"))
    #
    # has_env_copy = ".env" in dockerfile_content and "COPY" in dockerfile_content
    # # Check if .env is in a COPY line specifically
    # copies_env = any(".env" in l for l in dockerfile_content.split("\n")
    #                   if l.strip().startswith("COPY"))
    # checks.append(("No .env in COPY", not copies_env, "HIGH"))
    #
    # has_healthcheck = "HEALTHCHECK" in dockerfile_content
    # checks.append(("Has HEALTHCHECK", has_healthcheck, "MEDIUM"))
    #
    # has_no_cache = "--no-cache-dir" in dockerfile_content
    # checks.append(("pip --no-cache-dir", has_no_cache, "MEDIUM"))
    #
    # has_slim = "slim" in dockerfile_content or "alpine" in dockerfile_content
    # checks.append(("Uses slim/alpine base", has_slim, "LOW"))
    #
    # cleans_apt = "rm -rf /var/lib/apt" in dockerfile_content
    # checks.append(("Cleans apt cache", cleans_apt, "LOW"))

    return checks

# Test the validator
test_dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim
    WORKDIR /app
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    COPY . .
    CMD ["uvicorn", "main:app"]
''')

results = validate_security(test_dockerfile)
if results:
    print("  Security scan of test Dockerfile:")
    for check_name, passed_check, severity in results:
        icon = "PASS" if passed_check else "FAIL"
        print(f"    [{icon}] [{severity}] {check_name}")
else:
    print("  TODO: Implement the validate_security function")
    print("  It should check for:")
    print("    - Non-root USER (HIGH)")
    print("    - No .env in COPY (HIGH)")
    print("    - HEALTHCHECK present (MEDIUM)")
    print("    - pip --no-cache-dir (MEDIUM)")
    print("    - slim/alpine base image (LOW)")
    print("    - apt cache cleanup (LOW)")


# ============================================================
# Summary
# ============================================================

print("\n\n--- Lab 06 Summary ---\n")
print("  Security hardening checklist:")
print("    1. Run as non-root user (useradd + USER)")
print("    2. Add HEALTHCHECK for container monitoring")
print("    3. Never bake secrets into images (use -e or --env-file)")
print("    4. Use --no-cache-dir with pip")
print("    5. Clean apt cache (rm -rf /var/lib/apt/lists/*)")
print("    6. Use slim base images (smaller attack surface)")
print(f"\n  Files in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    print(f"    {f}")
