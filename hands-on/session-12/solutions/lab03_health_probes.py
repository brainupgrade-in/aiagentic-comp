"""
Lab 02: Health Checks & Probes
================================
Implement production-grade /health endpoint
and configure Kubernetes probes.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/prod-lab-12-03"

print("=" * 50)
print("  Lab 02: Health Checks & Probes")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Health Endpoint Pattern
# ============================================================

print("\n--- Step 1: Health Endpoint Pattern ---\n")

health_code = textwrap.dedent("""\
    @app.get("/health")
    async def health():
        checks = {
            "redis": await redis_client.ping(),
            "chromadb": await chroma_client.heartbeat(),
            "model_loaded": agent.is_ready(),
        }
        healthy = all(checks.values())
        return JSONResponse(
            status_code=200 if healthy else 503,
            content={
                "status": "ok" if healthy else "degraded",
                "checks": checks,
            }
        )
""")

print("  Production health endpoint:\n")
for line in health_code.strip().split("\n"):
    print(f"    {line}")

print("\n  Healthy response (200):  {\"status\": \"ok\", \"checks\": {\"redis\": true, ...}}")
print("  Degraded response (503): {\"status\": \"degraded\", \"checks\": {\"redis\": false, ...}}")


# ============================================================
# Step 2: Kubernetes Probe Types
# ============================================================

print("\n\n--- Step 2: Kubernetes Probe Types ---\n")

probes = [
    ("readinessProbe",  "Is the pod ready to receive traffic?",
                        "Fails -> removed from Service endpoints",
                        "httpGet /health, delay=5s, period=10s"),
    ("livenessProbe",   "Is the pod alive and functioning?",
                        "Fails -> pod gets restarted",
                        "httpGet /health, delay=15s, period=30s"),
    ("startupProbe",    "Has the pod finished starting?",
                        "Fails -> readiness/liveness disabled until pass",
                        "httpGet /health, delay=0s, period=5s, failures=30"),
]

print(f"    {'Probe':<18} {'Question':<40} {'On Failure'}")
print(f"    {'-'*90}")
for name, question, failure, config in probes:
    print(f"    {name:<18} {question:<40} {failure}")
    print(f"    {'':18} Config: {config}")
    print()


# ============================================================
# Step 3: Probe Configuration Reference
# ============================================================

print("--- Step 3: Probe YAML Reference ---\n")

probe_yaml = textwrap.dedent("""\
    containers:
    - name: agent
      image: agent-api:2.0
      ports:
      - containerPort: 8000
      readinessProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 5
        periodSeconds: 10
        failureThreshold: 3
      livenessProbe:
        httpGet:
          path: /health
          port: 8000
        initialDelaySeconds: 15
        periodSeconds: 30
        failureThreshold: 3
      startupProbe:
        httpGet:
          path: /health
          port: 8000
        periodSeconds: 5
        failureThreshold: 30
""")

for line in probe_yaml.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "probe-reference.yaml"), "w") as f:
    f.write(probe_yaml)


# ============================================================
# TODO 1: Write health endpoint code
# ============================================================

print("\n\n--- TODO 1: Health Endpoint Code ---\n")

print("  Write a FastAPI /health endpoint that:")
print("    - Checks redis (redis_client.ping())")
print("    - Checks chromadb (chroma_client.heartbeat())")
print("    - Checks model (agent.is_ready())")
print("    - Returns 200 if all healthy, 503 if degraded")
print("    - Returns JSON with 'status' and 'checks' fields\n")

todo1_code = textwrap.dedent("""\
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI()

    @app.get("/health")
    async def health():
        checks = {
            "redis": await redis_client.ping(),
            "chromadb": await chroma_client.heartbeat(),
            "model_loaded": agent.is_ready(),
        }
        healthy = all(checks.values())
        return JSONResponse(
            status_code=200 if healthy else 503,
            content={
                "status": "ok" if healthy else "degraded",
                "checks": checks,
            }
        )
""")

with open(os.path.join(WORKDIR, "health.py"), "w") as f:
    f.write(todo1_code)

checks1 = [
    ("Has /health route",          "/health" in todo1_code),
    ("Has async def",              "async def" in todo1_code or "def health" in todo1_code),
    ("Checks redis",               "redis" in todo1_code),
    ("Checks chromadb",            "chromadb" in todo1_code or "chroma" in todo1_code),
    ("Checks model",               "model" in todo1_code or "agent" in todo1_code or "ready" in todo1_code),
    ("Returns 200 or 503",         "200" in todo1_code and "503" in todo1_code),
    ("Has status field",           "status" in todo1_code),
    ("Has checks field",           "checks" in todo1_code),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Deployment with probes
# ============================================================

print("\n\n--- TODO 2: Deployment with Probes ---\n")

print("  Create a Deployment YAML with:")
print("    - name: agent-api, replicas: 3, image: agent-api:2.0")
print("    - readinessProbe: /health port 8000 (delay=5, period=10)")
print("    - livenessProbe: /health port 8000 (delay=15, period=30)")
print("    - startupProbe: /health port 8000 (period=5, failures=30)\n")

todo2_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: agent-api
      namespace: ai-stack
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: agent-api
      template:
        metadata:
          labels:
            app: agent-api
        spec:
          containers:
          - name: agent-api
            image: agent-api:2.0
            ports:
            - containerPort: 8000
            readinessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 5
              periodSeconds: 10
              failureThreshold: 3
            livenessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 15
              periodSeconds: 30
              failureThreshold: 3
            startupProbe:
              httpGet:
                path: /health
                port: 8000
              periodSeconds: 5
              failureThreshold: 30
""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo2_yaml)

checks2 = [
    ("Has kind: Deployment",       "kind: Deployment" in todo2_yaml),
    ("Has replicas: 3",            "replicas: 3" in todo2_yaml),
    ("Has agent-api image",        "agent-api" in todo2_yaml),
    ("Has readinessProbe",         "readinessProbe:" in todo2_yaml),
    ("Has livenessProbe",          "livenessProbe:" in todo2_yaml),
    ("Has startupProbe",           "startupProbe:" in todo2_yaml),
    ("Has /health path",           "/health" in todo2_yaml),
    ("Has port 8000",              "8000" in todo2_yaml),
    ("Has initialDelaySeconds",    "initialDelaySeconds" in todo2_yaml),
    ("Has periodSeconds",          "periodSeconds" in todo2_yaml),
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
print("    1. /health checks all dependencies (redis, chromadb, model)")
print("    2. Returns 200 (healthy) or 503 (degraded)")
print("    3. readinessProbe: controls traffic routing")
print("    4. livenessProbe: triggers pod restart if stuck")
print("    5. startupProbe: gives slow-starting apps time")
print(f"\n  TODO 1: {score1}/{len(checks1)} health endpoint checks")
print(f"  TODO 2: {score2}/{len(checks2)} deployment checks")
print(f"\n  Files generated in {WORKDIR}/")
