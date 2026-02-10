"""
Lab 07 Solution: Docker Compose for AI Stack
================================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/docker-lab-07"

print("=" * 50)
print("  Lab 07 Solution: Docker Compose")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# Create supporting files
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
# TODO 1 Solution: Add Prometheus monitoring
# ============================================================

print("\n--- TODO 1 Solution: Prometheus Monitoring ---\n")

todo1_compose = textwrap.dedent('''\
    services:
      agent:
        build: .
        ports:
          - "8000:8000"
        environment:
          - REDIS_URL=redis://redis:6379
        depends_on:
          - redis
        restart: unless-stopped

      redis:
        image: redis:7-alpine
        ports:
          - "6379:6379"
        volumes:
          - redis-data:/data
        restart: unless-stopped

      prometheus:
        image: prom/prometheus:latest
        ports:
          - "9090:9090"
        volumes:
          - ./prometheus.yml:/etc/prometheus/prometheus.yml
          - prometheus-data:/prometheus
        restart: unless-stopped

    volumes:
      redis-data:
      prometheus-data:
''')

has_prometheus = "prometheus" in todo1_compose.lower()
has_port_9090 = "9090" in todo1_compose
has_prom_volume = "prometheus-data" in todo1_compose

print(f"  [{'PASS' if has_prometheus else 'FAIL'}] Prometheus service defined")
print(f"  [{'PASS' if has_port_9090 else 'FAIL'}] Port 9090 mapped")
print(f"  [{'PASS' if has_prom_volume else 'FAIL'}] Config/data volume mounted")

with open(os.path.join(WORKDIR, "docker-compose.monitoring.yml"), "w") as f:
    f.write(todo1_compose)

# Create prometheus config
prom_config = textwrap.dedent('''\
    global:
      scrape_interval: 15s

    scrape_configs:
      - job_name: 'unigps-agent'
        static_configs:
          - targets: ['agent:8000']
        metrics_path: /metrics
''')
with open(os.path.join(WORKDIR, "prometheus.yml"), "w") as f:
    f.write(prom_config)

print("\n  Prometheus setup:")
print("    - Service: prom/prometheus:latest on port 9090")
print("    - Config: ./prometheus.yml mounted into container")
print("    - Data: prometheus-data volume for persistent storage")
print("    - Scrapes: agent:8000/metrics every 15 seconds")


# ============================================================
# TODO 2 Solution: Compose file validator
# ============================================================

print("\n\n--- TODO 2 Solution: Compose Validator ---\n")

def validate_compose(content: str) -> list:
    """Validate docker-compose.yml for best practices."""
    checks = []
    checks.append(("Has services key", "services:" in content))
    checks.append(("Uses depends_on", "depends_on" in content))
    checks.append(("Has healthcheck", "healthcheck" in content))
    checks.append(("Uses volumes", "volumes:" in content))
    checks.append(("Has restart policy", "restart:" in content))
    checks.append(("Has environment config",
                    "environment" in content or "env_file" in content))
    return checks


# Test against the full compose file
full_compose = textwrap.dedent('''\
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
          chromadb:
            condition: service_started
        healthcheck:
          test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
          interval: 30s
          timeout: 5s
          retries: 3
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

      chromadb:
        image: chromadb/chroma:latest
        ports:
          - "8001:8000"
        volumes:
          - chroma-data:/chroma/chroma
        restart: unless-stopped

    volumes:
      redis-data:
      chroma-data:
''')

with open(os.path.join(WORKDIR, "docker-compose.yml"), "w") as f:
    f.write(full_compose)

results = validate_compose(full_compose)
passed = sum(1 for _, ok in results if ok)
print(f"  Full stack validation ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 07 Solution complete!")
print("- TODO 1: Prometheus monitoring service (port 9090, config mount)")
print("- TODO 2: Compose validator (6 checks for best practices)")
