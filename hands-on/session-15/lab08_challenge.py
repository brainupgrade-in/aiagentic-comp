"""
Lab 08 Challenge: Complete Production Deployment
===================================================
Build a production-ready AI stack deployment with
probes, resources, secrets, HPA, PDB, and alerts.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-08"

print("=" * 60)
print("  Challenge: Complete Production Deployment")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Challenge Overview
# ============================================================

print("\n  Build a complete production-ready AI stack:\n")
print("    1. Agent Deployment with probes, resources, secrets, annotations")
print("    2. ChromaDB StatefulSet with persistent storage")
print("    3. HPA + PDB for high availability")
print("    4. Alert rules for production monitoring")
print()
print("    Architecture:")
print("      Ingress ──> Service ──> Agent API (x3)")
print("                                │")
print("                     ┌──────────┼──────────┐")
print("                     ▼          ▼          ▼")
print("                   Redis    ChromaDB    LLM API")
print("                             (PVC)")
print()
print("      Monitoring: Prometheus + Grafana + Alertmanager + LangFuse")


# ============================================================
# TODO 1: Agent Deployment
# ============================================================

print("\n\n--- TODO 1: Production Agent Deployment ---\n")

print("  Create a complete Deployment with:")
print("    - name: agent-api, namespace: ai-stack, replicas: 3")
print("    - image: agent-api:2.0, containerPort: 8000")
print("    - Prometheus annotations: scrape=true, port=8000, path=/metrics")
print("    - readinessProbe: /health port 8000 (delay=5, period=10)")
print("    - livenessProbe: /health port 8000 (delay=15, period=30)")
print("    - resources: requests 256Mi/250m, limits 1Gi/1000m")
print("    - Secret injection: GROQ_API_KEY from secret 'api-keys'")

todo1_yaml = textwrap.dedent("""\
    # TODO: Production Agent Deployment
    # Probes, resources, secrets, Prometheus annotations

""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo1_yaml)


# ============================================================
# TODO 2: ChromaDB StatefulSet
# ============================================================

print("\n\n--- TODO 2: ChromaDB StatefulSet ---\n")

print("  Create a StatefulSet with:")
print("    - name: chromadb, namespace: ai-stack")
print("    - serviceName: chromadb-headless")
print("    - image: chromadb/chroma:latest, containerPort: 8000")
print("    - PVC: 10Gi ReadWriteOnce, mounted at /data")
print("    - resources: requests 512Mi/500m, limits 2Gi/1000m")

todo2_yaml = textwrap.dedent("""\
    # TODO: ChromaDB StatefulSet with PVC

""")

with open(os.path.join(WORKDIR, "chromadb-statefulset.yaml"), "w") as f:
    f.write(todo2_yaml)


# ============================================================
# TODO 3: HPA + PDB + Ingress
# ============================================================

print("\n\n--- TODO 3: HPA, PDB, and Ingress ---\n")

print("  Create:")
print("    HPA: target agent-api, min 2, max 10, CPU 70%")
print("    PDB: minAvailable 2 for agent-api")
print("    Ingress: host agent.example.com → agent-api:8000")

todo3_yaml = textwrap.dedent("""\
    # TODO: HPA, PDB, and Ingress for production

""")

with open(os.path.join(WORKDIR, "ha-config.yaml"), "w") as f:
    f.write(todo3_yaml)


# ============================================================
# Validation
# ============================================================

print("\n\n--- Challenge Validation ---\n")

results = []

# TODO 1: Agent Deployment
results.append(("Deploy: kind Deployment",      "kind: Deployment" in todo1_yaml))
results.append(("Deploy: namespace ai-stack",    "ai-stack" in todo1_yaml))
results.append(("Deploy: replicas 3",            "replicas: 3" in todo1_yaml))
results.append(("Deploy: agent-api image",       "agent-api" in todo1_yaml))
results.append(("Deploy: containerPort 8000",    "8000" in todo1_yaml))
results.append(("Deploy: prometheus.io/scrape",  "prometheus.io/scrape" in todo1_yaml))
results.append(("Deploy: readinessProbe",        "readinessProbe:" in todo1_yaml))
results.append(("Deploy: livenessProbe",         "livenessProbe:" in todo1_yaml))
results.append(("Deploy: /health path",          "/health" in todo1_yaml))
results.append(("Deploy: resources section",     "resources:" in todo1_yaml))
results.append(("Deploy: memory requests",       "256Mi" in todo1_yaml))
results.append(("Deploy: CPU requests",          "250m" in todo1_yaml))
results.append(("Deploy: memory limits",         "1Gi" in todo1_yaml))
results.append(("Deploy: secretKeyRef",          "secretKeyRef" in todo1_yaml or "secretRef" in todo1_yaml))
results.append(("Deploy: GROQ_API_KEY",          "GROQ_API_KEY" in todo1_yaml))

# TODO 2: ChromaDB StatefulSet
results.append(("ChromaDB: kind StatefulSet",    "kind: StatefulSet" in todo2_yaml))
results.append(("ChromaDB: serviceName",         "serviceName:" in todo2_yaml))
results.append(("ChromaDB: chromadb image",      "chromadb" in todo2_yaml.lower()))
results.append(("ChromaDB: volumeClaimTemplates", "volumeClaimTemplates" in todo2_yaml))
results.append(("ChromaDB: 10Gi storage",        "10Gi" in todo2_yaml))
results.append(("ChromaDB: ReadWriteOnce",       "ReadWriteOnce" in todo2_yaml))
results.append(("ChromaDB: mountPath /data",     "/data" in todo2_yaml))
results.append(("ChromaDB: resources section",   "resources:" in todo2_yaml))

# TODO 3: HPA + PDB + Ingress
results.append(("HPA: kind",                     "HorizontalPodAutoscaler" in todo3_yaml))
results.append(("HPA: minReplicas 2",            "minReplicas: 2" in todo3_yaml or "minReplicas:2" in todo3_yaml))
results.append(("HPA: maxReplicas 10",           "maxReplicas: 10" in todo3_yaml or "maxReplicas:10" in todo3_yaml))
results.append(("HPA: CPU 70%",                  "70" in todo3_yaml))
results.append(("PDB: kind",                     "PodDisruptionBudget" in todo3_yaml))
results.append(("PDB: minAvailable 2",           "minAvailable: 2" in todo3_yaml or "minAvailable:2" in todo3_yaml))
results.append(("Ingress: kind",                 "kind: Ingress" in todo3_yaml))
results.append(("Ingress: host",                 "agent.example.com" in todo3_yaml or "host:" in todo3_yaml))

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
        print(f"    {rel:<45} ({size} bytes)")

print(f"\n  Production-ready AI stack:")
print(f"    1. agent-deployment.yaml — Probes, resources, secrets, annotations")
print(f"    2. chromadb-statefulset.yaml — StatefulSet with PVC")
print(f"    3. ha-config.yaml — HPA, PDB, Ingress")

print("\n" + "=" * 60)
print("Challenge complete!")
print(f"- Deployment: probes + resources + secrets + Prometheus annotations")
print(f"- StatefulSet: ChromaDB with persistent volume (10Gi)")
print(f"- HA: HPA (2-10 pods, 70% CPU), PDB (min 2), Ingress")
print(f"- {passed}/{total} validation checks passing")
