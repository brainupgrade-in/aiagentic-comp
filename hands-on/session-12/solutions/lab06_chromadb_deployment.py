"""
Lab 06 Solution: ChromaDB Full Deployment
===========================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-06"

print("=" * 50)
print("  Lab 06 Solution: ChromaDB Full Deployment")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: Headless + ClusterIP Services
# ============================================================

print("\n--- TODO 1 Solution: ChromaDB Services ---\n")

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

todo1_clusterip = textwrap.dedent("""\
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

passed_hl = sum(1 for _, ok in results_hl if ok)
print(f"  Headless Service ({passed_hl}/{len(results_hl)}):")
for name, ok in results_hl:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

passed_cip = sum(1 for _, ok in results_cip if ok)
print(f"\n  ClusterIP Service ({passed_cip}/{len(results_cip)}):")
for name, ok in results_cip:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

passed = passed_hl + passed_cip
all_svc = results_hl + results_cip


# ============================================================
# TODO 2 Solution: Production ChromaDB StatefulSet
# ============================================================

print("\n\n--- TODO 2 Solution: ChromaDB StatefulSet ---\n")

todo2_yaml = textwrap.dedent("""\
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

with open(os.path.join(WORKDIR, "chromadb-statefulset.yaml"), "w") as f:
    f.write(todo2_yaml)

sts_checks = [
    ("Has kind: StatefulSet", "StatefulSet" in todo2_yaml),
    ("Has serviceName: chromadb-headless", "chromadb-headless" in todo2_yaml),
    ("Has image chromadb/chroma", "chromadb/chroma" in todo2_yaml),
    ("Has readinessProbe", "readinessProbe:" in todo2_yaml),
    ("Has livenessProbe", "livenessProbe:" in todo2_yaml),
    ("Has /api/v1/heartbeat", "/api/v1/heartbeat" in todo2_yaml),
    ("Has resources section", "resources:" in todo2_yaml),
    ("Has memory request 512Mi", "512Mi" in todo2_yaml),
    ("Has volumeClaimTemplates", "volumeClaimTemplates" in todo2_yaml),
    ("Has storage 10Gi", "10Gi" in todo2_yaml),
    ("Has mountPath /chroma/chroma", "/chroma/chroma" in todo2_yaml),
]

passed2 = sum(1 for _, ok in sts_checks if ok)
print(f"  StatefulSet validation ({passed2}/{len(sts_checks)}):")
for name, ok in sts_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Production features:")
print("    - Readiness probe: /api/v1/heartbeat (delay=10, period=15)")
print("    - Liveness probe: /api/v1/heartbeat (delay=30, period=30)")
print("    - Resources: 512Mi/500m requests, 2Gi/1000m limits")
print("    - volumeClaimTemplates: 10Gi per pod (data survives restarts)")

total = passed + passed2
total_max = len(all_svc) + len(sts_checks)
print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 06 Solution complete!")
print(f"- TODO 1: {passed}/{len(all_svc)} service checks passed")
print(f"- TODO 2: {passed2}/{len(sts_checks)} StatefulSet checks passed")
