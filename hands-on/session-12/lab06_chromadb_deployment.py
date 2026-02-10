"""
Lab 06: ChromaDB Full Deployment
=================================
Deploy ChromaDB with StatefulSet, dual services,
probes, and resource limits — production-ready.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-06"

print("=" * 50)
print("  Lab 06: ChromaDB Full Deployment")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: ChromaDB Architecture on K8s
# ============================================================

print("\n--- Step 1: ChromaDB Architecture on K8s ---\n")

print("  ChromaDB needs 3 Kubernetes objects:")
print()
print("    ┌─────────────────────────────────────────┐")
print("    │  StatefulSet: chromadb                   │")
print("    │    image: chromadb/chroma:latest          │")
print("    │    port: 8000                             │")
print("    │    probes: /api/v1/heartbeat              │")
print("    │    volume: data → /chroma/chroma          │")
print("    │    resources: 512Mi-2Gi / 500m-1000m      │")
print("    └─────────────────────────────────────────┘")
print("              │                    │")
print("    ┌─────────┴──────┐   ┌────────┴──────────┐")
print("    │ Headless Svc   │   │ ClusterIP Svc     │")
print("    │ chromadb-hl    │   │ chromadb-svc      │")
print("    │ clusterIP:None │   │ port: 8000        │")
print("    └────────────────┘   └───────────────────┘")
print("    (for StatefulSet)    (for other pods)")


# ============================================================
# Step 2: Production ChromaDB YAML Examples
# ============================================================

print("\n\n--- Step 2: Production ChromaDB Patterns ---\n")

print("  Key production patterns for ChromaDB:")
print("    1. readinessProbe on /api/v1/heartbeat (detect when ready)")
print("    2. livenessProbe with higher initialDelay (allow index loading)")
print("    3. Resource limits: 512Mi request, 2Gi limit (embedding ops are memory-heavy)")
print("    4. PVC via volumeClaimTemplates (data survives restarts)")


# ============================================================
# TODO 1: Create ChromaDB Headless + ClusterIP Services
# ============================================================

print("\n\n--- TODO 1: Create ChromaDB Services ---\n")

print("  Create TWO services for ChromaDB:")
print()
print("  Service 1 — Headless (for StatefulSet):")
print("    - name: chromadb-headless")
print("    - clusterIP: None")
print("    - selector: app: chromadb")
print("    - port: 8000, targetPort: 8000")
print()
print("  Service 2 — ClusterIP (for other pods to connect):")
print("    - name: chromadb-svc")
print("    - type: ClusterIP")
print("    - selector: app: chromadb")
print("    - port: 8000, targetPort: 8000")

todo1_headless = textwrap.dedent("""\
    # TODO: Headless Service for ChromaDB StatefulSet
    # Requirements:
    #   apiVersion: v1, kind: Service
    #   name: chromadb-headless
    #   clusterIP: None
    #   selector: app: chromadb
    #   port: 8000, targetPort: 8000

""")

todo1_clusterip = textwrap.dedent("""\
    # TODO: ClusterIP Service for ChromaDB
    # Requirements:
    #   apiVersion: v1, kind: Service
    #   name: chromadb-svc
    #   type: ClusterIP
    #   selector: app: chromadb
    #   port: 8000, targetPort: 8000

""")

with open(os.path.join(WORKDIR, "chromadb-headless-svc.yaml"), "w") as f:
    f.write(todo1_headless)
with open(os.path.join(WORKDIR, "chromadb-clusterip-svc.yaml"), "w") as f:
    f.write(todo1_clusterip)

def validate_svc(content, name, expected_type):
    checks = [
        ("Has apiVersion: v1", "apiVersion: v1" in content),
        ("Has kind: Service", "kind: Service" in content),
        (f"Has name: {name}", name in content),
        ("Has selector app: chromadb", "chromadb" in content),
        ("Has port 8000", "8000" in content),
    ]
    if expected_type == "headless":
        checks.append(("Has clusterIP: None", "None" in content))
    else:
        checks.append(("Has type: ClusterIP", "ClusterIP" in content))
    return checks

results_hl = validate_svc(todo1_headless, "chromadb-headless", "headless")
results_cip = validate_svc(todo1_clusterip, "chromadb-svc", "clusterip")
all_svc = results_hl + results_cip
passed = sum(1 for _, ok in all_svc if ok)
print(f"\n  Validating Headless Service ({sum(1 for _, ok in results_hl if ok)}/{len(results_hl)}):")
for name, ok in results_hl:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")
print(f"\n  Validating ClusterIP Service ({sum(1 for _, ok in results_cip if ok)}/{len(results_cip)}):")
for name, ok in results_cip:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Create Production ChromaDB StatefulSet
# ============================================================

print("\n\n--- TODO 2: Create ChromaDB StatefulSet ---\n")

print("  Create a production-ready ChromaDB StatefulSet:")
print("    - name: chromadb, serviceName: chromadb-headless")
print("    - replicas: 1")
print("    - image: chromadb/chroma:latest")
print("    - containerPort: 8000")
print("    - resources: requests 512Mi/500m, limits 2Gi/1000m")
print("    - readinessProbe: httpGet /api/v1/heartbeat port 8000")
print("      initialDelaySeconds: 10, periodSeconds: 15")
print("    - livenessProbe: httpGet /api/v1/heartbeat port 8000")
print("      initialDelaySeconds: 30, periodSeconds: 30")
print("    - volumeMount: data → /chroma/chroma")
print("    - volumeClaimTemplates: data, 10Gi, ReadWriteOnce")

todo2_yaml = textwrap.dedent("""\
    # TODO: Create a production ChromaDB StatefulSet
    # Requirements listed above — include ALL of them:
    #   StatefulSet, probes, resources, volumeClaimTemplates

""")

with open(os.path.join(WORKDIR, "chromadb-statefulset.yaml"), "w") as f:
    f.write(todo2_yaml)

def validate_chromadb_sts(content):
    return [
        ("Has kind: StatefulSet", "StatefulSet" in content),
        ("Has serviceName: chromadb-headless", "chromadb-headless" in content),
        ("Has image chromadb/chroma", "chromadb/chroma" in content),
        ("Has readinessProbe", "readinessProbe:" in content),
        ("Has livenessProbe", "livenessProbe:" in content),
        ("Has /api/v1/heartbeat", "/api/v1/heartbeat" in content),
        ("Has resources section", "resources:" in content),
        ("Has memory request 512Mi", "512Mi" in content),
        ("Has volumeClaimTemplates", "volumeClaimTemplates" in content),
        ("Has storage 10Gi", "10Gi" in content),
        ("Has mountPath /chroma/chroma", "/chroma/chroma" in content),
    ]

results2 = validate_chromadb_sts(todo2_yaml)
passed2 = sum(1 for _, ok in results2 if ok)
print(f"\n  Validating your StatefulSet ({passed2}/{len(results2)}):")
for name, ok in results2:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

total = passed + passed2
total_max = len(all_svc) + len(results2)
print(f"\n\n--- Lab 06 Summary ---\n")
print("  Key concepts:")
print("    1. ChromaDB needs Headless Service (for StatefulSet) + ClusterIP (for clients)")
print("    2. /api/v1/heartbeat for health probes")
print("    3. volumeClaimTemplates give each pod its own PVC")
print("    4. Memory limits are important for embedding operations")
print(f"\n  TODO 1: {passed}/{len(all_svc)} service checks passed")
print(f"  TODO 2: {passed2}/{len(results2)} statefulset checks passed")
print(f"\n  Files generated in {WORKDIR}/")
