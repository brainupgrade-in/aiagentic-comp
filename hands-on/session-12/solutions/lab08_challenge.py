"""
Lab 08 Challenge Solution: Production AI Stack
=================================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-08"

print("=" * 60)
print("  Challenge Solution: Production AI Stack Deployment")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: ChromaDB StatefulSet + Services
# ============================================================

print("\n--- TODO 1 Solution: ChromaDB (StatefulSet + Services) ---\n")

todo1_headless = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: chromadb-headless
    spec:
      clusterIP: None
      selector:
        app: chromadb
      ports:
      - port: 8000
        targetPort: 8000
""")

todo1_svc = textwrap.dedent("""\
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

todo1_sts = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: StatefulSet
    metadata:
      name: chromadb
      labels:
        app: chromadb
    spec:
      serviceName: chromadb-headless
      replicas: 1
      selector:
        matchLabels:
          app: chromadb
      template:
        metadata:
          labels:
            app: chromadb
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
            livenessProbe:
              httpGet:
                path: /api/v1/heartbeat
                port: 8000
              initialDelaySeconds: 30
              periodSeconds: 30
            volumeMounts:
            - name: data
              mountPath: /chroma/chroma
      volumeClaimTemplates:
      - metadata:
          name: data
        spec:
          accessModes:
          - ReadWriteOnce
          resources:
            requests:
              storage: 10Gi
""")

with open(os.path.join(WORKDIR, "chromadb-headless-svc.yaml"), "w") as f:
    f.write(todo1_headless)
with open(os.path.join(WORKDIR, "chromadb-svc.yaml"), "w") as f:
    f.write(todo1_svc)
with open(os.path.join(WORKDIR, "chromadb-statefulset.yaml"), "w") as f:
    f.write(todo1_sts)

print("  Headless Service: chromadb-headless (clusterIP: None)")
print("  ClusterIP Service: chromadb-svc (port 8000)")
print("  StatefulSet: chromadb (probes, resources, volumeClaimTemplates)")


# ============================================================
# TODO 2 Solution: Agent Deployment + Service + HPA
# ============================================================

print("\n\n--- TODO 2 Solution: Agent API (Deployment + Service + HPA) ---\n")

todo2_deploy = textwrap.dedent("""\
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

todo2_svc = textwrap.dedent("""\
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

todo2_hpa = textwrap.dedent("""\
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: agent-api-hpa
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: agent-api
      minReplicas: 2
      maxReplicas: 8
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo2_deploy)
with open(os.path.join(WORKDIR, "agent-service.yaml"), "w") as f:
    f.write(todo2_svc)
with open(os.path.join(WORKDIR, "agent-hpa.yaml"), "w") as f:
    f.write(todo2_hpa)

print("  Deployment: agent-api (3 replicas, rolling update, envFrom, probes)")
print("  Service: agent-svc (LoadBalancer, port 80 -> 8000)")
print("  HPA: agent-api-hpa (min=2, max=8, CPU=70%, stabilization=300)")


# ============================================================
# TODO 3 Solution: Ingress with TLS
# ============================================================

print("\n\n--- TODO 3 Solution: Ingress with TLS ---\n")

todo3_ingress = textwrap.dedent("""\
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: ai-stack-ingress
      annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /
    spec:
      ingressClassName: nginx
      tls:
      - hosts:
        - ai.example.com
        secretName: ai-tls-secret
      rules:
      - host: ai.example.com
        http:
          paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: agent-svc
                port:
                  number: 80
          - path: /docs
            pathType: Prefix
            backend:
              service:
                name: chromadb-svc
                port:
                  number: 8000
""")

with open(os.path.join(WORKDIR, "ingress.yaml"), "w") as f:
    f.write(todo3_ingress)

print("  Ingress: ai-stack-ingress (nginx, TLS)")
print("    /api  -> agent-svc:80")
print("    /docs -> chromadb-svc:8000")
print("    TLS: ai-tls-secret for ai.example.com")


# ============================================================
# Validation (30 checks matching student lab)
# ============================================================

print("\n\n--- Challenge Validation ---\n")

results = []

# TODO 1: ChromaDB
results.append(("Headless: kind Service", "kind: Service" in todo1_headless))
results.append(("Headless: clusterIP None", "None" in todo1_headless))
results.append(("Headless: port 8000", "8000" in todo1_headless))
results.append(("ClusterIP: kind Service", "kind: Service" in todo1_svc))
results.append(("ClusterIP: chromadb-svc", "chromadb-svc" in todo1_svc))
results.append(("StatefulSet: kind", "StatefulSet" in todo1_sts))
results.append(("StatefulSet: serviceName", "chromadb-headless" in todo1_sts))
results.append(("StatefulSet: probes", "readinessProbe:" in todo1_sts or "livenessProbe:" in todo1_sts))
results.append(("StatefulSet: resources", "resources:" in todo1_sts))
results.append(("StatefulSet: volumeClaimTemplates", "volumeClaimTemplates" in todo1_sts))
results.append(("StatefulSet: heartbeat", "/api/v1/heartbeat" in todo1_sts))

# TODO 2: Agent
results.append(("Agent Deploy: kind Deployment", "kind: Deployment" in todo2_deploy))
results.append(("Agent Deploy: replicas 3", "replicas: 3" in todo2_deploy))
results.append(("Agent Deploy: RollingUpdate", "RollingUpdate" in todo2_deploy))
results.append(("Agent Deploy: envFrom", "envFrom:" in todo2_deploy))
results.append(("Agent Deploy: readinessProbe", "readinessProbe:" in todo2_deploy))
results.append(("Agent Deploy: resources", "resources:" in todo2_deploy))
results.append(("Agent Service: LoadBalancer", "LoadBalancer" in todo2_svc))
results.append(("Agent Service: port 80", "port: 80" in todo2_svc))
results.append(("HPA: autoscaling/v2", "autoscaling/v2" in todo2_hpa))
results.append(("HPA: minReplicas 2", "minReplicas: 2" in todo2_hpa))
results.append(("HPA: maxReplicas 8", "maxReplicas: 8" in todo2_hpa))
results.append(("HPA: stabilization 300", "300" in todo2_hpa))

# TODO 3: Ingress
results.append(("Ingress: kind", "kind: Ingress" in todo3_ingress))
results.append(("Ingress: nginx class", "nginx" in todo3_ingress))
results.append(("Ingress: TLS secret", "ai-tls-secret" in todo3_ingress))
results.append(("Ingress: path /api", "/api" in todo3_ingress))
results.append(("Ingress: path /docs", "/docs" in todo3_ingress))
results.append(("Ingress: agent-svc", "agent-svc" in todo3_ingress))
results.append(("Ingress: chromadb-svc", "chromadb-svc" in todo3_ingress))

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
        print(f"    {rel:<40} ({size} bytes)")

print(f"\n  Deploy order on a real cluster:")
print(f"    1. kubectl apply -f chromadb-headless-svc.yaml -f chromadb-svc.yaml")
print(f"    2. kubectl apply -f chromadb-statefulset.yaml")
print(f"    3. kubectl apply -f agent-deployment.yaml -f agent-service.yaml")
print(f"    4. kubectl apply -f agent-hpa.yaml")
print(f"    5. kubectl apply -f ingress.yaml")
print(f"    6. kubectl get all && kubectl get ingress")

print("\n" + "=" * 60)
print("Challenge Solution complete!")
print("- ChromaDB: StatefulSet + headless + ClusterIP + PVC")
print("- Agent: Deployment + LB Service + HPA")
print("- Ingress: TLS + path-based routing")
print(f"- {passed}/{total} validation checks passing")
