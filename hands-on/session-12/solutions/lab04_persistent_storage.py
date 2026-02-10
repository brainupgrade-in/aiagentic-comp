"""
Lab 04 Solution: Persistent Storage (PVC)
===========================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-04"

print("=" * 50)
print("  Lab 04 Solution: Persistent Storage (PVC)")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: PVC for ChromaDB
# ============================================================

print("\n--- TODO 1 Solution: ChromaDB PVC ---\n")

todo1_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: chroma-data
    spec:
      accessModes:
      - ReadWriteOnce
      storageClassName: standard
      resources:
        requests:
          storage: 10Gi
""")

with open(os.path.join(WORKDIR, "chroma-pvc.yaml"), "w") as f:
    f.write(todo1_yaml)

pvc_checks = [
    ("Has apiVersion: v1", "apiVersion: v1" in todo1_yaml),
    ("Has kind: PersistentVolumeClaim", "PersistentVolumeClaim" in todo1_yaml),
    ("Has name: chroma-data", "chroma-data" in todo1_yaml),
    ("Has ReadWriteOnce", "ReadWriteOnce" in todo1_yaml),
    ("Has storage: 10Gi", "10Gi" in todo1_yaml),
    ("Has storageClassName", "storageClassName:" in todo1_yaml),
]

passed = sum(1 for _, ok in pvc_checks if ok)
print(f"  PVC validation ({passed}/{len(pvc_checks)}):")
for name, ok in pvc_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  PVC features:")
print("    - ReadWriteOnce: one node can mount read/write (standard for DBs)")
print("    - 10Gi: sufficient for ChromaDB vector embeddings")
print("    - storageClassName: standard triggers dynamic provisioning")


# ============================================================
# TODO 2 Solution: ChromaDB Deployment with PVC Mount
# ============================================================

print("\n\n--- TODO 2 Solution: ChromaDB Deployment with PVC ---\n")

todo2_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: chromadb
      labels:
        app: chromadb
    spec:
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
            volumeMounts:
            - name: chroma-storage
              mountPath: /chroma/chroma
          volumes:
          - name: chroma-storage
            persistentVolumeClaim:
              claimName: chroma-data
""")

with open(os.path.join(WORKDIR, "chromadb-deployment.yaml"), "w") as f:
    f.write(todo2_yaml)

deploy_checks = [
    ("Has kind: Deployment", "kind: Deployment" in todo2_yaml),
    ("Has name: chromadb", "chromadb" in todo2_yaml),
    ("Has image chromadb/chroma", "chromadb/chroma" in todo2_yaml),
    ("Has containerPort 8000", "8000" in todo2_yaml),
    ("Has volumeMounts section", "volumeMount" in todo2_yaml),
    ("Has mountPath /chroma/chroma", "/chroma/chroma" in todo2_yaml),
    ("Has volumes section", "volumes:" in todo2_yaml),
    ("Has persistentVolumeClaim", "persistentVolumeClaim:" in todo2_yaml),
    ("Has claimName: chroma-data", "chroma-data" in todo2_yaml),
]

passed2 = sum(1 for _, ok in deploy_checks if ok)
print(f"  Deployment validation ({passed2}/{len(deploy_checks)}):")
for name, ok in deploy_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Volume mount explained:")
print("    volumeMounts.name: chroma-storage  (reference name)")
print("    volumeMounts.mountPath: /chroma/chroma  (where ChromaDB writes data)")
print("    volumes.persistentVolumeClaim.claimName: chroma-data  (links to PVC)")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 04 Solution complete!")
print(f"- TODO 1: {passed}/{len(pvc_checks)} PVC checks passed")
print(f"- TODO 2: {passed2}/{len(deploy_checks)} deployment checks passed")
