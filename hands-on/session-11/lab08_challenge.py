"""
Lab 08 Challenge: Complete AI Stack on Kubernetes
===================================================
Deploy the full UniGPS AI Agent stack with all Kubernetes concepts.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap
import base64

WORKDIR = "/tmp/k8s-lab-08"

print("=" * 60)
print("  Challenge: Complete AI Stack on Kubernetes")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Context: What you're building
# ============================================================

print("\n--- Challenge Overview ---\n")

print("  Deploy the UniGPS AI Agent stack on Kubernetes:")
print()
print("    ┌──────────────┐    ┌───────────────┐    ┌───────────────┐")
print("    │  AI Agent     │───▶│  Redis Cache   │    │  ChromaDB     │")
print("    │  (FastAPI)    │    │  (Session)     │    │  (Vectors)    │")
print("    │  ×3 replicas  │    │  ×1 replica    │    │  ×1 replica   │")
print("    └──────┬───────┘    └───────────────┘    └───────────────┘")
print("           │")
print("    ┌──────┴───────┐")
print("    │  LoadBalancer │")
print("    │  Service      │")
print("    └──────────────┘")
print()
print("  You need to create ALL Kubernetes manifests:\n")

deliverables = [
    ("TODO 1", "ConfigMap + Secret", "Environment configuration and API keys"),
    ("TODO 2", "Agent Deployment + Service", "3 replicas, probes, resources, LoadBalancer"),
    ("TODO 3", "Redis Deployment + Service", "1 replica, probes, ClusterIP"),
    ("TODO 4", "ChromaDB Deployment + Service", "1 replica, probes, persistent volume claim"),
]

for todo, what, detail in deliverables:
    print(f"    {todo}: {what}")
    print(f"           {detail}")
print()


# ============================================================
# TODO 1: ConfigMap + Secret
# ============================================================

print("\n--- TODO 1: ConfigMap + Secret ---\n")

print("  Create:")
print("    1. ConfigMap 'agent-config' with:")
print("       LOG_LEVEL=info, APP_VERSION=2.0.0,")
print("       REDIS_URL=redis://redis-svc:6379,")
print("       CHROMA_URL=http://chromadb-svc:8000")
print()
print("    2. Secret 'agent-secrets' with (base64-encoded):")
print("       GROQ_API_KEY=gsk_production_key_abc123\n")

# Encode hint
groq_key = "gsk_production_key_abc123"
groq_b64 = base64.b64encode(groq_key.encode()).decode()
print(f"  Hint: base64 of '{groq_key}' = {groq_b64}\n")

# YOUR CODE HERE
todo1_configmap = textwrap.dedent("""\
    # TODO: Create ConfigMap named 'agent-config'
    # apiVersion: v1, kind: ConfigMap
    # data: LOG_LEVEL, APP_VERSION, REDIS_URL, CHROMA_URL

""")

todo1_secret = textwrap.dedent("""\
    # TODO: Create Secret named 'agent-secrets'
    # apiVersion: v1, kind: Secret, type: Opaque
    # data: GROQ_API_KEY (base64-encoded)

""")

with open(os.path.join(WORKDIR, "configmap.yaml"), "w") as f:
    f.write(todo1_configmap)
with open(os.path.join(WORKDIR, "secret.yaml"), "w") as f:
    f.write(todo1_secret)


# ============================================================
# TODO 2: Agent Deployment + Service
# ============================================================

print("\n--- TODO 2: Agent Deployment + LoadBalancer Service ---\n")

print("  Agent Deployment requirements:")
print("    - name: unigps-agent")
print("    - replicas: 3")
print("    - image: unigps-agent:2.0")
print("    - containerPort: 8000")
print("    - labels: app=agent, component=api")
print("    - envFrom: agent-config (configMapRef) + agent-secrets (secretRef)")
print("    - resources: requests (256Mi/250m), limits (1Gi/1000m)")
print("    - readinessProbe: httpGet /health:8000, initialDelay=5, period=10")
print("    - livenessProbe: httpGet /health:8000, initialDelay=15, period=20")
print()
print("  Agent Service requirements:")
print("    - name: agent-svc")
print("    - type: LoadBalancer")
print("    - selector: app=agent")
print("    - port: 80 → targetPort: 8000\n")

# YOUR CODE HERE
todo2_deployment = textwrap.dedent("""\
    # TODO: Create Agent Deployment
    # apiVersion: apps/v1, kind: Deployment
    # replicas: 3, image: unigps-agent:2.0
    # Include: envFrom, resources, readinessProbe, livenessProbe

""")

todo2_service = textwrap.dedent("""\
    # TODO: Create Agent LoadBalancer Service
    # apiVersion: v1, kind: Service
    # type: LoadBalancer, port: 80 → targetPort: 8000

""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo2_deployment)
with open(os.path.join(WORKDIR, "agent-service.yaml"), "w") as f:
    f.write(todo2_service)


# ============================================================
# TODO 3: Redis Deployment + Service
# ============================================================

print("\n--- TODO 3: Redis Deployment + ClusterIP Service ---\n")

print("  Redis Deployment requirements:")
print("    - name: redis")
print("    - replicas: 1")
print("    - image: redis:7-alpine")
print("    - containerPort: 6379")
print("    - labels: app=redis, component=cache")
print("    - resources: requests (64Mi/100m), limits (128Mi/200m)")
print("    - livenessProbe: tcpSocket port 6379, initialDelay=5, period=10")
print("    - readinessProbe: exec 'redis-cli ping', initialDelay=5, period=10")
print()
print("  Redis Service requirements:")
print("    - name: redis-svc")
print("    - type: ClusterIP")
print("    - selector: app=redis")
print("    - port: 6379 → targetPort: 6379\n")

# YOUR CODE HERE
todo3_deployment = textwrap.dedent("""\
    # TODO: Create Redis Deployment
    # replicas: 1, image: redis:7-alpine
    # Include: resources, livenessProbe (tcpSocket), readinessProbe (exec)

""")

todo3_service = textwrap.dedent("""\
    # TODO: Create Redis ClusterIP Service
    # port: 6379 → targetPort: 6379

""")

with open(os.path.join(WORKDIR, "redis-deployment.yaml"), "w") as f:
    f.write(todo3_deployment)
with open(os.path.join(WORKDIR, "redis-service.yaml"), "w") as f:
    f.write(todo3_service)


# ============================================================
# TODO 4: ChromaDB Deployment + Service
# ============================================================

print("\n--- TODO 4: ChromaDB Deployment + ClusterIP Service ---\n")

print("  ChromaDB Deployment requirements:")
print("    - name: chromadb")
print("    - replicas: 1")
print("    - image: chromadb/chroma:latest")
print("    - containerPort: 8000")
print("    - labels: app=chromadb, component=vectorstore")
print("    - resources: requests (512Mi/500m), limits (2Gi/1000m)")
print("    - readinessProbe: httpGet /api/v1/heartbeat:8000, initialDelay=10, period=15")
print("    - livenessProbe: httpGet /api/v1/heartbeat:8000, initialDelay=30, period=30")
print("    - volumeMount: /chroma/chroma → PVC 'chroma-data'")
print()
print("  ChromaDB Service requirements:")
print("    - name: chromadb-svc")
print("    - type: ClusterIP")
print("    - selector: app=chromadb")
print("    - port: 8000 → targetPort: 8000\n")
print("  PersistentVolumeClaim:")
print("    - name: chroma-data")
print("    - storage: 5Gi")
print("    - accessModes: ReadWriteOnce\n")

# YOUR CODE HERE
todo4_deployment = textwrap.dedent("""\
    # TODO: Create ChromaDB Deployment with PVC
    # replicas: 1, image: chromadb/chroma:latest
    # Include: resources, probes, volumeMount to PVC

""")

todo4_service = textwrap.dedent("""\
    # TODO: Create ChromaDB ClusterIP Service
    # port: 8000 → targetPort: 8000

""")

todo4_pvc = textwrap.dedent("""\
    # TODO: Create PersistentVolumeClaim for ChromaDB
    # name: chroma-data, storage: 5Gi, accessModes: ReadWriteOnce

""")

with open(os.path.join(WORKDIR, "chromadb-deployment.yaml"), "w") as f:
    f.write(todo4_deployment)
with open(os.path.join(WORKDIR, "chromadb-service.yaml"), "w") as f:
    f.write(todo4_service)
with open(os.path.join(WORKDIR, "chromadb-pvc.yaml"), "w") as f:
    f.write(todo4_pvc)


# ============================================================
# Validation
# ============================================================

print("\n\n--- Challenge Validation ---\n")

def validate_challenge():
    results = []

    # TODO 1: ConfigMap + Secret
    results.append(("ConfigMap: apiVersion v1", "apiVersion: v1" in todo1_configmap))
    results.append(("ConfigMap: kind ConfigMap", "kind: ConfigMap" in todo1_configmap))
    results.append(("ConfigMap: has data section", "data:" in todo1_configmap))
    results.append(("ConfigMap: has REDIS_URL", "REDIS_URL" in todo1_configmap))
    results.append(("ConfigMap: has CHROMA_URL", "CHROMA_URL" in todo1_configmap))
    results.append(("Secret: kind Secret", "kind: Secret" in todo1_secret))
    results.append(("Secret: type Opaque", "type: Opaque" in todo1_secret or "Opaque" in todo1_secret))
    results.append(("Secret: has GROQ_API_KEY", "GROQ_API_KEY" in todo1_secret))

    # TODO 2: Agent Deployment + Service
    results.append(("Agent Deploy: kind Deployment", "kind: Deployment" in todo2_deployment))
    results.append(("Agent Deploy: replicas 3", "replicas: 3" in todo2_deployment or "replicas:3" in todo2_deployment))
    results.append(("Agent Deploy: image unigps-agent", "unigps-agent" in todo2_deployment))
    results.append(("Agent Deploy: has resources", "resources:" in todo2_deployment))
    results.append(("Agent Deploy: has readinessProbe", "readinessProbe:" in todo2_deployment))
    results.append(("Agent Deploy: has livenessProbe", "livenessProbe:" in todo2_deployment))
    results.append(("Agent Deploy: has envFrom", "envFrom:" in todo2_deployment))
    results.append(("Agent Service: kind Service", "kind: Service" in todo2_service))
    results.append(("Agent Service: LoadBalancer", "LoadBalancer" in todo2_service))
    results.append(("Agent Service: port 80", "port: 80" in todo2_service or "port:80" in todo2_service))

    # TODO 3: Redis Deployment + Service
    results.append(("Redis Deploy: kind Deployment", "kind: Deployment" in todo3_deployment))
    results.append(("Redis Deploy: image redis", "redis:" in todo3_deployment))
    results.append(("Redis Deploy: has resources", "resources:" in todo3_deployment))
    results.append(("Redis Deploy: has livenessProbe", "livenessProbe:" in todo3_deployment))
    results.append(("Redis Deploy: tcpSocket or exec", "tcpSocket:" in todo3_deployment or "exec:" in todo3_deployment))
    results.append(("Redis Service: ClusterIP", "ClusterIP" in todo3_service or "kind: Service" in todo3_service))
    results.append(("Redis Service: port 6379", "6379" in todo3_service))

    # TODO 4: ChromaDB Deployment + Service + PVC
    results.append(("ChromaDB Deploy: kind Deployment", "kind: Deployment" in todo4_deployment))
    results.append(("ChromaDB Deploy: image chromadb", "chromadb" in todo4_deployment))
    results.append(("ChromaDB Deploy: has resources", "resources:" in todo4_deployment))
    results.append(("ChromaDB Deploy: has probes", "readinessProbe:" in todo4_deployment or "livenessProbe:" in todo4_deployment))
    results.append(("ChromaDB Deploy: volumeMount", "volumeMount" in todo4_deployment or "volumes:" in todo4_deployment))
    results.append(("ChromaDB Service: port 8000", "8000" in todo4_service))
    results.append(("PVC: PersistentVolumeClaim", "PersistentVolumeClaim" in todo4_pvc))
    results.append(("PVC: storage 5Gi", "5Gi" in todo4_pvc))

    return results

results = validate_challenge()
passed = sum(1 for _, ok in results if ok)
total = len(results)

print(f"  Results: {passed}/{total} checks passed\n")
for name, ok in results:
    status = "PASS" if ok else "FAIL"
    print(f"    [{status}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Challenge Summary ---\n")
print(f"  Score: {passed}/{total} ({passed/total*100:.0f}%)")
print(f"\n  Files to create in {WORKDIR}/:")
expected = [
    "configmap.yaml", "secret.yaml",
    "agent-deployment.yaml", "agent-service.yaml",
    "redis-deployment.yaml", "redis-service.yaml",
    "chromadb-deployment.yaml", "chromadb-service.yaml", "chromadb-pvc.yaml",
]
for f in expected:
    exists = os.path.exists(os.path.join(WORKDIR, f))
    size = os.path.getsize(os.path.join(WORKDIR, f)) if exists else 0
    print(f"    {'✓' if exists else '✗'} {f:<35} ({size} bytes)")

print(f"\n  To deploy on a real cluster:")
print(f"    cd {WORKDIR}")
print(f"    kubectl apply -f configmap.yaml -f secret.yaml")
print(f"    kubectl apply -f redis-deployment.yaml -f redis-service.yaml")
print(f"    kubectl apply -f chromadb-pvc.yaml -f chromadb-deployment.yaml -f chromadb-service.yaml")
print(f"    kubectl apply -f agent-deployment.yaml -f agent-service.yaml")
print(f"    kubectl get all")

print("\n" + "=" * 60)
print("Challenge complete!")
print("- TODO 1: ConfigMap + Secret for environment configuration")
print("- TODO 2: Agent Deployment (3 replicas, probes, resources) + LoadBalancer")
print("- TODO 3: Redis Deployment + ClusterIP Service")
print("- TODO 4: ChromaDB Deployment + ClusterIP Service + PVC")
print(f"- {passed}/{total} validation checks passing")
