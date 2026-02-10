"""
Lab 07: Docker Compose for AI Stack
======================================
Define multi-service AI applications with Docker Compose.

No Docker installation required — generates and validates docker-compose.yml.
"""

import os
import shutil
import textwrap
import json

WORKDIR = "/tmp/docker-lab-07"

print("=" * 50)
print("  Lab 07: Docker Compose for AI Stack")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Why Docker Compose?
# ============================================================

print("\n--- Step 1: Why Docker Compose? ---\n")

print("  Real AI applications need multiple services:\n")

services = [
    ("AI Agent (FastAPI)", "8000", "The LangGraph agent API"),
    ("Redis", "6379", "Response caching and session store"),
    ("ChromaDB", "8001", "Vector database for RAG"),
    ("Prometheus", "9090", "Metrics collection"),
]

print(f"  {'Service':<25} {'Port':<8} {'Purpose'}")
print("  " + "-" * 60)
for name, port, purpose in services:
    print(f"  {name:<25} {port:<8} {purpose}")

print()
print("  Without Compose: 4 separate 'docker run' commands")
print("  With Compose: 1 file, 1 command → docker compose up")

# ============================================================
# Step 2: Basic docker-compose.yml
# ============================================================

print("\n\n--- Step 2: Basic docker-compose.yml ---\n")

basic_compose = textwrap.dedent('''\
    # docker-compose.yml — UniGPS AI Agent Stack
    services:

      # The AI Agent API
      agent:
        build: .
        ports:
          - "8000:8000"
        environment:
          - PYTHONUNBUFFERED=1
          - REDIS_URL=redis://redis:6379
        depends_on:
          - redis
        restart: unless-stopped

      # Redis for caching
      redis:
        image: redis:7-alpine
        ports:
          - "6379:6379"
        volumes:
          - redis-data:/data
        restart: unless-stopped

    volumes:
      redis-data:
''')

with open(os.path.join(WORKDIR, "docker-compose.yml"), "w") as f:
    f.write(basic_compose)

print("  Key concepts:")
print()
print("  services:          ← Define each container")
print("    agent:           ← Service name (also the hostname on network)")
print("      build: .       ← Build from Dockerfile in current directory")
print("      ports:         ← Map host:container ports")
print("      environment:   ← Set env vars (like docker run -e)")
print("      depends_on:    ← Start redis before agent")
print("      restart:       ← Auto-restart policy")
print()
print("  volumes:           ← Persistent storage (survives container restarts)")
print("    redis-data:      ← Named volume for Redis data")

# ============================================================
# Step 3: Networking in Compose
# ============================================================

print("\n\n--- Step 3: Networking in Compose ---\n")

print("  Docker Compose creates a network automatically.")
print("  Services can reach each other by service name:\n")
print("    agent → redis:6379     (not localhost:6379!)")
print("    agent → chromadb:8000  (by service name)")
print()
print("  In your Python code:")
print()

network_example = textwrap.dedent('''\
    # WRONG: This looks for Redis on the agent's own container
    # redis_url = "redis://localhost:6379"

    # RIGHT: Use the service name from docker-compose.yml
    redis_url = "redis://redis:6379"

    # Or better: use an environment variable
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
''')

for line in network_example.strip().split("\n"):
    print(f"    {line}")

# ============================================================
# Step 4: Full AI Stack Compose
# ============================================================

print("\n\n--- Step 4: Full AI Stack ---\n")

full_compose = textwrap.dedent('''\
    # docker-compose.yml — UniGPS Full AI Stack
    services:

      # AI Agent API
      agent:
        build:
          context: .
          dockerfile: Dockerfile
        ports:
          - "8000:8000"
        environment:
          - PYTHONUNBUFFERED=1
          - REDIS_URL=redis://redis:6379
          - CHROMA_HOST=chromadb
          - CHROMA_PORT=8001
        env_file:
          - .env
        depends_on:
          redis:
            condition: service_healthy
          chromadb:
            condition: service_started
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
          interval: 30s
          timeout: 5s
          retries: 3
          start_period: 10s
        restart: unless-stopped

      # Redis for response caching
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

      # ChromaDB for vector storage
      chromadb:
        image: chromadb/chroma:latest
        ports:
          - "8001:8000"
        volumes:
          - chroma-data:/chroma/chroma
        environment:
          - ANONYMIZED_TELEMETRY=false
        restart: unless-stopped

    volumes:
      redis-data:
        driver: local
      chroma-data:
        driver: local
''')

with open(os.path.join(WORKDIR, "docker-compose.full.yml"), "w") as f:
    f.write(full_compose)

print("  Full stack with 3 services:")
print()
print("    agent (FastAPI + LangGraph)")
print("      ├── depends_on: redis (healthy), chromadb (started)")
print("      ├── env_file: .env (API keys)")
print("      └── healthcheck: curl /health")
print()
print("    redis (caching)")
print("      ├── volume: redis-data (persistent)")
print("      └── healthcheck: redis-cli ping")
print()
print("    chromadb (vector DB)")
print("      └── volume: chroma-data (persistent)")
print()
print("  Commands:")
print("    docker compose up -d          # Start all services")
print("    docker compose ps             # Check status")
print("    docker compose logs agent     # View agent logs")
print("    docker compose down           # Stop all services")

# Also create the Dockerfile and app files
dockerfile = textwrap.dedent('''\
    FROM python:3.11-slim
    WORKDIR /app
    RUN apt-get update && apt-get install -y --no-install-recommends curl \\
        && rm -rf /var/lib/apt/lists/*
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    RUN useradd --create-home appuser
    COPY --chown=appuser:appuser . .
    USER appuser
    ENV PYTHONUNBUFFERED=1
    EXPOSE 8000
    HEALTHCHECK --interval=30s --timeout=5s --retries=3 \\
        CMD curl -f http://localhost:8000/health || exit 1
    CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

app_code = textwrap.dedent('''\
    """UniGPS AI Agent — Docker Compose Demo"""
    import os
    from datetime import datetime
    from fastapi import FastAPI

    app = FastAPI(title="UniGPS Agent", version="2.0.0")

    _start_time = datetime.now()

    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "redis_url": os.getenv("REDIS_URL", "not set"),
            "uptime": round((datetime.now() - _start_time).total_seconds(), 1),
        }

    @app.get("/")
    async def root():
        return {"message": "UniGPS AI Agent is running"}
''')

requirements = textwrap.dedent('''\
    fastapi==0.104.1
    uvicorn[standard]==0.24.0
    pydantic==2.5.0
    redis==5.0.1
''')

with open(os.path.join(WORKDIR, "Dockerfile"), "w") as f:
    f.write(dockerfile)
with open(os.path.join(WORKDIR, "main.py"), "w") as f:
    f.write(app_code)
with open(os.path.join(WORKDIR, "requirements.txt"), "w") as f:
    f.write(requirements)
with open(os.path.join(WORKDIR, ".env"), "w") as f:
    f.write("GROQ_API_KEY=your-key-here\n")


# ============================================================
# TODO 1: Add a monitoring service
# ============================================================

print("\n\n--- TODO 1: Add Prometheus Monitoring ---\n")

# TODO: Extend the docker-compose.yml to include a Prometheus service.
# Requirements:
# - Image: prom/prometheus:latest
# - Port: 9090:9090
# - Mount a config file: ./prometheus.yml:/etc/prometheus/prometheus.yml
# - Add to the volumes section
# - The agent should depend on it (optional)

todo1_compose = ""

# Uncomment:
# todo1_compose = textwrap.dedent('''\
#     services:
#       agent:
#         build: .
#         ports:
#           - "8000:8000"
#         environment:
#           - REDIS_URL=redis://redis:6379
#         depends_on:
#           - redis
#         restart: unless-stopped
#
#       redis:
#         image: redis:7-alpine
#         ports:
#           - "6379:6379"
#         volumes:
#           - redis-data:/data
#         restart: unless-stopped
#
#       prometheus:
#         image: prom/prometheus:latest
#         ports:
#           - "9090:9090"
#         volumes:
#           - ./prometheus.yml:/etc/prometheus/prometheus.yml
#           - prometheus-data:/prometheus
#         restart: unless-stopped
#
#     volumes:
#       redis-data:
#       prometheus-data:
# ''')

if todo1_compose:
    has_prometheus = "prometheus" in todo1_compose.lower()
    has_port_9090 = "9090" in todo1_compose
    has_prom_volume = "prometheus-data" in todo1_compose or "prometheus.yml" in todo1_compose

    print(f"  [{'PASS' if has_prometheus else 'FAIL'}] Prometheus service defined")
    print(f"  [{'PASS' if has_port_9090 else 'FAIL'}] Port 9090 mapped")
    print(f"  [{'PASS' if has_prom_volume else 'FAIL'}] Config/data volume mounted")

    if has_prometheus:
        with open(os.path.join(WORKDIR, "docker-compose.monitoring.yml"), "w") as f:
            f.write(todo1_compose)
        print(f"\n  Saved docker-compose.monitoring.yml to {WORKDIR}/")
else:
    print("  TODO: Add a Prometheus service to the compose file")
    print("  Hints:")
    print("    - Image: prom/prometheus:latest")
    print("    - Ports: 9090:9090")
    print("    - Volume: ./prometheus.yml:/etc/prometheus/prometheus.yml")


# ============================================================
# TODO 2: Validate a docker-compose.yml
# ============================================================

print("\n\n--- TODO 2: Compose File Validator ---\n")

# TODO: Write a function that validates a docker-compose.yml for
# common issues in AI application deployments.

def validate_compose(content: str) -> list:
    """Validate docker-compose.yml for best practices."""
    checks = []

    # TODO: Implement these checks:
    # 1. Has 'services:' key
    # 2. Uses 'depends_on' for service ordering
    # 3. Has health checks defined
    # 4. Uses named volumes (not bind mounts for data)
    # 5. Has restart policy
    # 6. Uses env_file or environment for config

    # Uncomment:
    # checks.append(("Has services key", "services:" in content))
    # checks.append(("Uses depends_on", "depends_on" in content))
    # checks.append(("Has healthcheck", "healthcheck" in content))
    # checks.append(("Uses volumes", "volumes:" in content))
    # checks.append(("Has restart policy", "restart:" in content))
    # checks.append(("Has environment config", "environment" in content or "env_file" in content))

    return checks

results = validate_compose(full_compose)
if results:
    passed = sum(1 for _, ok in results if ok)
    print(f"  Compose validation ({passed}/{len(results)}):")
    for name, ok in results:
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}")
else:
    print("  TODO: Implement the validate_compose function")
    print("  Check for: services, depends_on, healthcheck,")
    print("  volumes, restart policy, environment config")


# ============================================================
# Summary
# ============================================================

print("\n\n--- Lab 07 Summary ---\n")
print("  Docker Compose for AI:")
print("    1. Define multi-service stacks in one YAML file")
print("    2. Services communicate by name (agent → redis:6379)")
print("    3. Use depends_on + healthcheck for startup ordering")
print("    4. Named volumes for persistent data (Redis, ChromaDB)")
print("    5. env_file for secrets (not in docker-compose.yml)")
print("    6. One command to start everything: docker compose up -d")
print(f"\n  Files in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    print(f"    {f}")
