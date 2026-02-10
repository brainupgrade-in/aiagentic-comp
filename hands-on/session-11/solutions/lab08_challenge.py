"""
Lab 08 Challenge Solution: Complete AI Stack on Kubernetes
============================================================
"""

import os
import shutil
import textwrap
import base64

WORKDIR = "/tmp/k8s-lab-08"

print("=" * 60)
print("  Challenge Solution: Complete AI Stack on Kubernetes")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: ConfigMap + Secret
# ============================================================

print("\n--- TODO 1 Solution: ConfigMap + Secret ---\n")

todo1_configmap = textwrap.dedent("""\
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: agent-config
    data:
      LOG_LEVEL: "info"
      APP_VERSION: "2.0.0"
      REDIS_URL: "redis://redis-svc:6379"
      CHROMA_URL: "http://chromadb-svc:8000"
""")

groq_b64 = base64.b64encode(b"gsk_production_key_abc123").decode()

todo1_secret = textwrap.dedent(f"""\
    apiVersion: v1
    kind: Secret
    metadata:
      name: agent-secrets
    type: Opaque
    data:
      GROQ_API_KEY: {groq_b64}
""")

with open(os.path.join(WORKDIR, "configmap.yaml"), "w") as f:
    f.write(todo1_configmap)
with open(os.path.join(WORKDIR, "secret.yaml"), "w") as f:
    f.write(todo1_secret)

print("  ConfigMap: agent-config")
print("    LOG_LEVEL=info, APP_VERSION=2.0.0")
print("    REDIS_URL=redis://redis-svc:6379")
print("    CHROMA_URL=http://chromadb-svc:8000")
print(f"\n  Secret: agent-secrets")
print(f"    GROQ_API_KEY={groq_b64}")


# ============================================================
# TODO 2 Solution: Agent Deployment + Service
# ============================================================

print("\n\n--- TODO 2 Solution: Agent Deployment + Service ---\n")

todo2_deployment = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: unigps-agent
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
            image: unigps-agent:2.0
            ports:
            - containerPort: 8000
            envFrom:
            - configMapRef:
                name: agent-config
            - secretRef:
                name: agent-secrets
            env:
            - name: PYTHONUNBUFFERED
              value: "1"
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
              failureThreshold: 3
            livenessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 15
              periodSeconds: 20
              failureThreshold: 3
""")

todo2_service = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: agent-svc
    spec:
      type: LoadBalancer
      selector:
        app: agent
      ports:
      - port: 80
        targetPort: 8000
""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo2_deployment)
with open(os.path.join(WORKDIR, "agent-service.yaml"), "w") as f:
    f.write(todo2_service)

print("  Agent Deployment: 3 replicas, probes, resources, envFrom")
print("  Agent Service: LoadBalancer (port 80 → 8000)")


# ============================================================
# TODO 3 Solution: Redis Deployment + Service
# ============================================================

print("\n\n--- TODO 3 Solution: Redis Deployment + Service ---\n")

todo3_deployment = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: redis
      labels:
        app: redis
        component: cache
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: redis
      template:
        metadata:
          labels:
            app: redis
            component: cache
        spec:
          containers:
          - name: redis
            image: redis:7-alpine
            ports:
            - containerPort: 6379
            resources:
              requests:
                memory: "64Mi"
                cpu: "100m"
              limits:
                memory: "128Mi"
                cpu: "200m"
            livenessProbe:
              tcpSocket:
                port: 6379
              initialDelaySeconds: 5
              periodSeconds: 10
              failureThreshold: 3
            readinessProbe:
              exec:
                command:
                - redis-cli
                - ping
              initialDelaySeconds: 5
              periodSeconds: 10
              failureThreshold: 3
""")

todo3_service = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: redis-svc
    spec:
      type: ClusterIP
      selector:
        app: redis
      ports:
      - port: 6379
        targetPort: 6379
""")

with open(os.path.join(WORKDIR, "redis-deployment.yaml"), "w") as f:
    f.write(todo3_deployment)
with open(os.path.join(WORKDIR, "redis-service.yaml"), "w") as f:
    f.write(todo3_service)

print("  Redis Deployment: 1 replica, tcpSocket liveness, exec readiness")
print("  Redis Service: ClusterIP (redis-svc:6379)")


# ============================================================
# TODO 4 Solution: ChromaDB Deployment + Service + PVC
# ============================================================

print("\n\n--- TODO 4 Solution: ChromaDB Deployment + Service + PVC ---\n")

todo4_pvc = textwrap.dedent("""\
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: chroma-data
    spec:
      accessModes:
      - ReadWriteOnce
      resources:
        requests:
          storage: 5Gi
""")

todo4_deployment = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: chromadb
      labels:
        app: chromadb
        component: vectorstore
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: chromadb
      template:
        metadata:
          labels:
            app: chromadb
            component: vectorstore
        spec:
          containers:
          - name: chromadb
            image: chromadb/chroma:latest
            ports:
            - containerPort: 8000
            resources:
              requests:
                memory: "512Mi"
                cpu: "500m"
              limits:
                memory: "2Gi"
                cpu: "1000m"
            readinessProbe:
              httpGet:
                path: /api/v1/heartbeat
                port: 8000
              initialDelaySeconds: 10
              periodSeconds: 15
              failureThreshold: 3
            livenessProbe:
              httpGet:
                path: /api/v1/heartbeat
                port: 8000
              initialDelaySeconds: 30
              periodSeconds: 30
              failureThreshold: 3
            volumeMounts:
            - name: chroma-storage
              mountPath: /chroma/chroma
          volumes:
          - name: chroma-storage
            persistentVolumeClaim:
              claimName: chroma-data
""")

todo4_service = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: chromadb-svc
    spec:
      type: ClusterIP
      selector:
        app: chromadb
      ports:
      - port: 8000
        targetPort: 8000
""")

with open(os.path.join(WORKDIR, "chromadb-pvc.yaml"), "w") as f:
    f.write(todo4_pvc)
with open(os.path.join(WORKDIR, "chromadb-deployment.yaml"), "w") as f:
    f.write(todo4_deployment)
with open(os.path.join(WORKDIR, "chromadb-service.yaml"), "w") as f:
    f.write(todo4_service)

print("  ChromaDB PVC: 5Gi ReadWriteOnce")
print("  ChromaDB Deployment: 1 replica, /api/v1/heartbeat probes, volumeMount")
print("  ChromaDB Service: ClusterIP (chromadb-svc:8000)")


# ============================================================
# Validation
# ============================================================

print("\n\n--- Challenge Validation ---\n")

results = []

# TODO 1
results.append(("ConfigMap: apiVersion v1", "apiVersion: v1" in todo1_configmap))
results.append(("ConfigMap: kind ConfigMap", "kind: ConfigMap" in todo1_configmap))
results.append(("ConfigMap: has data section", "data:" in todo1_configmap))
results.append(("ConfigMap: has REDIS_URL", "REDIS_URL" in todo1_configmap))
results.append(("ConfigMap: has CHROMA_URL", "CHROMA_URL" in todo1_configmap))
results.append(("Secret: kind Secret", "kind: Secret" in todo1_secret))
results.append(("Secret: type Opaque", "type: Opaque" in todo1_secret))
results.append(("Secret: has GROQ_API_KEY", "GROQ_API_KEY" in todo1_secret))

# TODO 2
results.append(("Agent Deploy: kind Deployment", "kind: Deployment" in todo2_deployment))
results.append(("Agent Deploy: replicas 3", "replicas: 3" in todo2_deployment))
results.append(("Agent Deploy: image unigps-agent", "unigps-agent" in todo2_deployment))
results.append(("Agent Deploy: has resources", "resources:" in todo2_deployment))
results.append(("Agent Deploy: has readinessProbe", "readinessProbe:" in todo2_deployment))
results.append(("Agent Deploy: has livenessProbe", "livenessProbe:" in todo2_deployment))
results.append(("Agent Deploy: has envFrom", "envFrom:" in todo2_deployment))
results.append(("Agent Service: kind Service", "kind: Service" in todo2_service))
results.append(("Agent Service: LoadBalancer", "LoadBalancer" in todo2_service))
results.append(("Agent Service: port 80", "port: 80" in todo2_service))

# TODO 3
results.append(("Redis Deploy: kind Deployment", "kind: Deployment" in todo3_deployment))
results.append(("Redis Deploy: image redis", "redis:" in todo3_deployment))
results.append(("Redis Deploy: has resources", "resources:" in todo3_deployment))
results.append(("Redis Deploy: has livenessProbe", "livenessProbe:" in todo3_deployment))
results.append(("Redis Deploy: tcpSocket or exec", "tcpSocket:" in todo3_deployment or "exec:" in todo3_deployment))
results.append(("Redis Service: ClusterIP", "ClusterIP" in todo3_service))
results.append(("Redis Service: port 6379", "6379" in todo3_service))

# TODO 4
results.append(("ChromaDB Deploy: kind Deployment", "kind: Deployment" in todo4_deployment))
results.append(("ChromaDB Deploy: image chromadb", "chromadb" in todo4_deployment))
results.append(("ChromaDB Deploy: has resources", "resources:" in todo4_deployment))
results.append(("ChromaDB Deploy: has probes", "readinessProbe:" in todo4_deployment or "livenessProbe:" in todo4_deployment))
results.append(("ChromaDB Deploy: volumeMount", "volumeMount" in todo4_deployment or "volumes:" in todo4_deployment))
results.append(("ChromaDB Service: port 8000", "8000" in todo4_service))
results.append(("PVC: PersistentVolumeClaim", "PersistentVolumeClaim" in todo4_pvc))
results.append(("PVC: storage 5Gi", "5Gi" in todo4_pvc))

passed = sum(1 for _, ok in results if ok)
total = len(results)

print(f"  Results: {passed}/{total} checks passed\n")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


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
        print(f"    {rel:<35} ({size} bytes)")

print(f"\n  Deploy order on a real cluster:")
print(f"    1. kubectl apply -f configmap.yaml -f secret.yaml")
print(f"    2. kubectl apply -f chromadb-pvc.yaml")
print(f"    3. kubectl apply -f redis-deployment.yaml -f redis-service.yaml")
print(f"    4. kubectl apply -f chromadb-deployment.yaml -f chromadb-service.yaml")
print(f"    5. kubectl apply -f agent-deployment.yaml -f agent-service.yaml")
print(f"    6. kubectl get all")

print("\n" + "=" * 60)
print("Challenge Solution complete!")
print("- ConfigMap + Secret: environment config and API keys")
print("- Agent: 3 replicas, readiness/liveness probes, resources, envFrom, LB")
print("- Redis: 1 replica, tcpSocket/exec probes, ClusterIP")
print("- ChromaDB: 1 replica, httpGet probes, PVC, ClusterIP")
print(f"- {passed}/{total} validation checks passing")
