"""
Lab 02: LangFuse Setup & Deployment
======================================
Deploy LangFuse self-hosted with Docker Compose
and configure environment variables.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-11-02"

print("=" * 50)
print("  Lab 02: LangFuse Setup & Deployment")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Self-Hosted Architecture
# ============================================================

print("\n--- Step 1: Self-Hosted Architecture ---\n")

print("  LangFuse self-hosted components:\n")
print("    LangChain App")
print("        │")
print("        ▼")
print("    LangFuse SDK / CallbackHandler")
print("        │")
print("        ▼")
print("    LangFuse Server (API + Web UI)")
print("        │")
print("        ▼")
print("    PostgreSQL (trace storage)")
print()
print("  Access: http://localhost:3000 (LangFuse UI)")


# ============================================================
# Step 2: Docker Compose Reference
# ============================================================

print("\n\n--- Step 2: Docker Compose Reference ---\n")

compose_ref = textwrap.dedent("""\
    version: "3.8"
    services:
      langfuse:
        image: langfuse/langfuse:latest
        ports:
          - "3000:3000"
        environment:
          DATABASE_URL: postgresql://langfuse:langfuse@db:5432/langfuse
          NEXTAUTH_SECRET: mysecret
          NEXTAUTH_URL: http://localhost:3000
          SALT: mysalt
        depends_on:
          - db

      db:
        image: postgres:16-alpine
        environment:
          POSTGRES_USER: langfuse
          POSTGRES_PASSWORD: langfuse
          POSTGRES_DB: langfuse
        volumes:
          - langfuse-data:/var/lib/postgresql/data

    volumes:
      langfuse-data:
""")

print("  Reference docker-compose.yml:\n")
for line in compose_ref.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "docker-compose-reference.yaml"), "w") as f:
    f.write(compose_ref)


# ============================================================
# Step 3: Environment Variables
# ============================================================

print("\n\n--- Step 3: Environment Variables ---\n")

print("  Client-side (your Python app):\n")
env_vars = [
    ("LANGFUSE_PUBLIC_KEY",  "pk-lf-...",              "API public key"),
    ("LANGFUSE_SECRET_KEY",  "sk-lf-...",              "API secret key"),
    ("LANGFUSE_HOST",        "http://localhost:3000",   "LangFuse server URL"),
]
for name, example, desc in env_vars:
    print(f"    {name:<25} {example:<30} # {desc}")

print("\n  Server-side (docker-compose):\n")
server_vars = [
    ("DATABASE_URL",     "postgresql://user:pass@db:5432/langfuse"),
    ("NEXTAUTH_SECRET",  "random-secret-for-auth"),
    ("NEXTAUTH_URL",     "http://localhost:3000"),
    ("SALT",             "random-salt-for-hashing"),
]
for name, example in server_vars:
    print(f"    {name:<20} {example}")


# ============================================================
# TODO 1: Create Docker Compose for LangFuse
# ============================================================

print("\n\n--- TODO 1: Docker Compose Configuration ---\n")

print("  Create a docker-compose.yml with:")
print("    - langfuse service: image langfuse/langfuse:latest, port 3000")
print("    - db service: postgres:16-alpine with volume")
print("    - DATABASE_URL connecting langfuse to db")
print("    - NEXTAUTH_SECRET, NEXTAUTH_URL, SALT")
print("    - Named volume for PostgreSQL data")

todo1_yaml = textwrap.dedent("""\
    # TODO: Docker Compose for self-hosted LangFuse
    # Include langfuse + postgres services

""")

with open(os.path.join(WORKDIR, "docker-compose.yaml"), "w") as f:
    f.write(todo1_yaml)

checks1 = [
    ("Has services section",       "services:" in todo1_yaml),
    ("Has langfuse service",       "langfuse:" in todo1_yaml),
    ("Has langfuse image",         "langfuse/langfuse" in todo1_yaml),
    ("Has port 3000",              "3000" in todo1_yaml),
    ("Has db service",             "db:" in todo1_yaml or "postgres:" in todo1_yaml),
    ("Has postgres image",         "postgres:" in todo1_yaml),
    ("Has DATABASE_URL",           "DATABASE_URL" in todo1_yaml),
    ("Has NEXTAUTH_SECRET",        "NEXTAUTH_SECRET" in todo1_yaml),
    ("Has NEXTAUTH_URL",           "NEXTAUTH_URL" in todo1_yaml),
    ("Has SALT",                   "SALT" in todo1_yaml),
    ("Has volumes section",        "volumes:" in todo1_yaml),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"\n  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Client environment setup
# ============================================================

print("\n\n--- TODO 2: Client Environment Setup ---\n")

print("  Create the Python code to initialize LangFuse client.")
print("  Include: environment variables, Langfuse() client, health check.\n")

todo2_code = textwrap.dedent("""\
    # TODO: LangFuse client initialization
    # Set up env vars and create client

""")

with open(os.path.join(WORKDIR, "langfuse_client.py"), "w") as f:
    f.write(todo2_code)

checks2 = [
    ("Has os import",              "import os" in todo2_code or "from os" in todo2_code),
    ("Has LANGFUSE_PUBLIC_KEY",    "LANGFUSE_PUBLIC_KEY" in todo2_code),
    ("Has LANGFUSE_SECRET_KEY",    "LANGFUSE_SECRET_KEY" in todo2_code),
    ("Has LANGFUSE_HOST",          "LANGFUSE_HOST" in todo2_code),
    ("Has Langfuse import",        "Langfuse" in todo2_code or "langfuse" in todo2_code),
    ("Has client creation",        "Langfuse(" in todo2_code),
]

score2 = sum(1 for _, ok in checks2 if ok)
print(f"  Validating ({score2}/{len(checks2)}):\n")
for name, ok in checks2:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 02 Summary ---\n")
print("  Key concepts:")
print("    1. Self-hosted LangFuse: Docker Compose with PostgreSQL backend")
print("    2. Server env vars: DATABASE_URL, NEXTAUTH_SECRET, SALT")
print("    3. Client env vars: LANGFUSE_PUBLIC_KEY, SECRET_KEY, HOST")
print("    4. Access LangFuse UI at http://localhost:3000")
print(f"\n  TODO 1: {score1}/{len(checks1)} compose checks passed")
print(f"  TODO 2: {score2}/{len(checks2)} client setup checks passed")
print(f"\n  Files generated in {WORKDIR}/")
