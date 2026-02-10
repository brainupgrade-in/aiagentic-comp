"""
Lab 07 Solution: Full Stack Deployment
========================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-07"

print("=" * 50)
print("  Lab 07 Solution: Full Stack Deployment")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: Agent Deployment with envFrom
# ============================================================

print("\n--- TODO 1 Solution: Agent Deployment with envFrom ---\n")

todo1_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: agent-api
      labels:
        app: agent
        component: api
    spec:
      replicas: 3
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 1
          maxUnavailable: 0
      selector:
        matchLabels:
          app: agent
      template:
        metadata:
          labels:
            app: agent
            component: api
        spec:
          containers:
          - name: agent
            image: agent-api:2.0
            ports:
            - containerPort: 8000
            envFrom:
            - configMapRef:
                name: agent-config
            - secretRef:
                name: agent-secrets
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "1000m"
            readinessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 5
              periodSeconds: 10
            livenessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 15
              periodSeconds: 20
""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo1_yaml)

checks = [
    ("Has kind: Deployment", "kind: Deployment" in todo1_yaml),
    ("Has replicas: 3", "replicas: 3" in todo1_yaml),
    ("Has RollingUpdate strategy", "RollingUpdate" in todo1_yaml),
    ("Has maxUnavailable: 0", "maxUnavailable: 0" in todo1_yaml),
    ("Has image agent-api", "agent-api" in todo1_yaml),
    ("Has envFrom section", "envFrom:" in todo1_yaml),
    ("Has configMapRef", "configMapRef:" in todo1_yaml),
    ("Has secretRef", "secretRef:" in todo1_yaml),
    ("Has resources", "resources:" in todo1_yaml),
    ("Has readinessProbe", "readinessProbe:" in todo1_yaml),
    ("Has livenessProbe", "livenessProbe:" in todo1_yaml),
    ("Has /health path", "/health" in todo1_yaml),
]

passed = sum(1 for _, ok in checks if ok)
print(f"  Agent Deployment validation ({passed}/{len(checks)}):")
for name, ok in checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Deployment features:")
print("    - envFrom: configMapRef + secretRef (all env vars from config)")
print("    - RollingUpdate: maxSurge=1, maxUnavailable=0 (zero downtime)")
print("    - Resources: 256Mi/250m req, 1Gi/1000m lim")
print("    - Readiness: /health delay=5 period=10")
print("    - Liveness: /health delay=15 period=20")


# ============================================================
# TODO 2 Solution: Deploy Order
# ============================================================

print("\n\n--- TODO 2 Solution: Deployment Order ---\n")

deploy_steps = [
    "configmap.yaml + secret.yaml",
    "redis-deployment.yaml + redis-service.yaml",
    "chromadb-statefulset.yaml + chromadb-headless-svc.yaml + chromadb-svc.yaml",
    "agent-deployment.yaml + agent-service.yaml",
    "agent-hpa.yaml + agent-pdb.yaml",
    "ingress.yaml",
]

expected = [
    "configmap.yaml + secret.yaml",
    "redis-deployment.yaml + redis-service.yaml",
    "chromadb-statefulset.yaml + chromadb-headless-svc.yaml + chromadb-svc.yaml",
    "agent-deployment.yaml + agent-service.yaml",
    "agent-hpa.yaml + agent-pdb.yaml",
    "ingress.yaml",
]

step_labels = [
    "Config & Secrets",
    "Redis (cache)",
    "ChromaDB (vector store)",
    "Agent API (application)",
    "HPA + PDB (scaling)",
    "Ingress (external access)",
]

key_terms = {
    0: ["configmap", "secret"],
    1: ["redis"],
    2: ["chromadb", "statefulset"],
    3: ["agent", "deployment"],
    4: ["hpa", "pdb"],
    5: ["ingress"],
}

passed2 = 0
for i, (step, exp, label) in enumerate(zip(deploy_steps, expected, step_labels)):
    matches = all(term in step.lower() for term in key_terms[i])
    if matches:
        passed2 += 1
    status = "PASS" if matches else "FAIL"
    print(f"    [{status}] Step {i+1}: {label}")
    print(f"           Files: {step}")

print(f"\n  Deploy order: {passed2}/{len(deploy_steps)} steps correct")

print("\n  Why this order:")
print("    1. Config first: pods need ConfigMap/Secret before starting")
print("    2. Data layer: Redis + ChromaDB must be running for agent")
print("    3. App layer: Agent connects to Redis + ChromaDB on startup")
print("    4. Scaling: HPA + PDB protect running agent pods")
print("    5. Ingress: needs services to route traffic to")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 07 Solution complete!")
print(f"- TODO 1: {passed}/{len(checks)} deployment checks passed")
print(f"- TODO 2: {passed2}/{len(deploy_steps)} deploy order correct")
