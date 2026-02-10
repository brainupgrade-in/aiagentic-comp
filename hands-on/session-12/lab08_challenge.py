"""
Lab 08 Challenge: Production AI Stack
=======================================
Deploy the complete AI stack with all advanced features:
StatefulSet, Ingress, HPA, PDB, and proper deploy order.
"""

import os
import shutil
import textwrap
WORKDIR = "/tmp/k8s-lab-12-08"

print("=" * 60)
print("  Challenge: Production AI Stack Deployment")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Challenge Overview
# ============================================================

print("\n  Deploy a production-ready AI stack with:")
print("    1. ChromaDB StatefulSet + dual Services + PVC")
print("    2. Agent API Deployment + LoadBalancer Service")
print("    3. HPA for agent (auto-scaling)")
print("    4. Ingress with path-based routing and TLS")
print()
print("  Architecture:")
print("    Ingress (TLS)")
print("      /api  → agent-svc:80 → Agent Deployment (x3, HPA 2-8)")
print("      /docs → chromadb-svc:8000 → ChromaDB StatefulSet (x1, PVC)")


# ============================================================
# TODO 1: ChromaDB StatefulSet + Services
# ============================================================

print("\n\n--- TODO 1: ChromaDB (StatefulSet + Headless + ClusterIP) ---\n")

print("  Create 3 manifests for ChromaDB:")
print("  1. Headless Service: chromadb-headless, clusterIP: None")
print("  2. ClusterIP Service: chromadb-svc, port 8000")
print("  3. StatefulSet: chromadb, serviceName=chromadb-headless")
print("     image: chromadb/chroma:latest, port 8000")
print("     readinessProbe: /api/v1/heartbeat (delay=10, period=15)")
print("     livenessProbe: /api/v1/heartbeat (delay=30, period=30)")
print("     resources: 512Mi/500m requests, 2Gi/1000m limits")
print("     volumeClaimTemplates: data, 10Gi, ReadWriteOnce")

todo1_headless = textwrap.dedent("""\
    # TODO: Headless Service for ChromaDB

""")

todo1_svc = textwrap.dedent("""\
    # TODO: ClusterIP Service for ChromaDB

""")

todo1_sts = textwrap.dedent("""\
    # TODO: ChromaDB StatefulSet with probes, resources, volumeClaimTemplates

""")

with open(os.path.join(WORKDIR, "chromadb-headless-svc.yaml"), "w") as f:
    f.write(todo1_headless)
with open(os.path.join(WORKDIR, "chromadb-svc.yaml"), "w") as f:
    f.write(todo1_svc)
with open(os.path.join(WORKDIR, "chromadb-statefulset.yaml"), "w") as f:
    f.write(todo1_sts)


# ============================================================
# TODO 2: Agent Deployment + Service + HPA
# ============================================================

print("\n\n--- TODO 2: Agent API (Deployment + Service + HPA) ---\n")

print("  Create 3 manifests for the Agent API:")
print("  1. Deployment: agent-api, 3 replicas, RollingUpdate (surge=1, unavail=0)")
print("     image: agent-api:2.0, port 8000")
print("     envFrom: configMapRef agent-config, secretRef agent-secrets")
print("     resources: 256Mi/250m requests, 1Gi/1000m limits")
print("     readinessProbe: /health (delay=5, period=10)")
print("  2. Service: agent-svc, type LoadBalancer, port 80 → 8000")
print("  3. HPA: agent-api-hpa, min=2, max=8, CPU target 70%")
print("     scaleDown stabilizationWindowSeconds: 300")

todo2_deploy = textwrap.dedent("""\
    # TODO: Agent API Deployment with rolling update, envFrom, probes, resources

""")

todo2_svc = textwrap.dedent("""\
    # TODO: Agent Service (LoadBalancer, port 80 → 8000)

""")

todo2_hpa = textwrap.dedent("""\
    # TODO: Agent HPA (autoscaling/v2, min=2, max=8, CPU=70%, stabilization=300)

""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo2_deploy)
with open(os.path.join(WORKDIR, "agent-service.yaml"), "w") as f:
    f.write(todo2_svc)
with open(os.path.join(WORKDIR, "agent-hpa.yaml"), "w") as f:
    f.write(todo2_hpa)


# ============================================================
# TODO 3: Ingress with TLS
# ============================================================

print("\n\n--- TODO 3: Ingress with TLS ---\n")

print("  Create an Ingress:")
print("    - name: ai-stack-ingress")
print("    - ingressClassName: nginx")
print("    - TLS: secretName ai-tls-secret, host ai.example.com")
print("    - Rules for ai.example.com:")
print("      /api  → agent-svc:80 (Prefix)")
print("      /docs → chromadb-svc:8000 (Prefix)")

todo3_ingress = textwrap.dedent("""\
    # TODO: Ingress with TLS and path-based routing

""")

with open(os.path.join(WORKDIR, "ingress.yaml"), "w") as f:
    f.write(todo3_ingress)


# ============================================================
# Validation
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
print("Challenge complete!")
print(f"- ChromaDB: StatefulSet + headless + ClusterIP + PVC")
print(f"- Agent: Deployment + LB Service + HPA")
print(f"- Ingress: TLS + path-based routing")
print(f"- {passed}/{total} validation checks passing")
