"""
Lab 04: Persistent Storage (PVC)
=================================
Learn how PersistentVolumeClaims provide
durable storage for AI data and databases.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-04"

print("=" * 50)
print("  Lab 04: Persistent Storage (PVC)")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: The Ephemeral Data Problem
# ============================================================

print("\n--- Step 1: The Ephemeral Data Problem ---\n")

print("  Without persistent storage:")
print("    1. ChromaDB indexes 10,000 documents (2 hours of work)")
print("    2. Pod crashes or restarts")
print("    3. All 10,000 embeddings are GONE")
print("    4. Must re-index everything from scratch")
print()
print("  With persistent storage (PVC):")
print("    1. ChromaDB writes to /chroma/chroma (mounted PVC)")
print("    2. Pod crashes or restarts")
print("    3. New pod mounts the SAME PVC")
print("    4. All 10,000 embeddings are still there!")


# ============================================================
# Step 2: PV, PVC, StorageClass
# ============================================================

print("\n\n--- Step 2: Storage Concepts ---\n")

concepts = [
    ("PersistentVolume (PV)",
     "The actual disk (like a physical hard drive). Created by admins or dynamically."),
    ("PersistentVolumeClaim (PVC)",
     "A REQUEST for storage (like a purchase order). Pods reference PVCs."),
    ("StorageClass",
     "Defines HOW to create PVs (SSD vs HDD, AWS EBS vs Azure Disk)."),
    ("Dynamic Provisioning",
     "StorageClass automatically creates PV when PVC is requested."),
]

for name, desc in concepts:
    print(f"  {name}:")
    print(f"    {desc}\n")

print("  Flow: Pod → PVC → StorageClass → PV (auto-created) → Disk")


# ============================================================
# Step 3: Access Modes
# ============================================================

print("\n\n--- Step 3: PVC Access Modes ---\n")

modes = [
    ("ReadWriteOnce (RWO)", "One node can read/write",
     "Databases, ChromaDB, Redis, LangFuse PostgreSQL"),
    ("ReadOnlyMany (ROX)",  "Many nodes can read",
     "Shared config files, ML model weights (read-only)"),
    ("ReadWriteMany (RWX)", "Many nodes can read/write",
     "Shared file uploads, NFS storage (not all providers support)"),
]

print(f"  {'Mode':<25} {'Description':<30} {'AI Use Case'}")
print(f"  {'-'*85}")
for mode, desc, use_case in modes:
    print(f"  {mode:<25} {desc:<30} {use_case}")


# ============================================================
# TODO 1: Create a PVC for ChromaDB
# ============================================================

print("\n\n--- TODO 1: Create a PVC for ChromaDB ---\n")

print("  Create a PersistentVolumeClaim:")
print("    - name: chroma-data")
print("    - accessMode: ReadWriteOnce")
print("    - storage request: 10Gi")
print("    - storageClassName: standard")

todo1_yaml = textwrap.dedent("""\
    # TODO: Create a PVC for ChromaDB vector storage
    # Requirements:
    #   apiVersion: v1
    #   kind: PersistentVolumeClaim
    #   name: chroma-data
    #   accessModes: [ReadWriteOnce]
    #   resources.requests.storage: 10Gi
    #   storageClassName: standard

""")

with open(os.path.join(WORKDIR, "chroma-pvc.yaml"), "w") as f:
    f.write(todo1_yaml)

def validate_pvc(content):
    return [
        ("Has apiVersion: v1", "apiVersion: v1" in content),
        ("Has kind: PersistentVolumeClaim", "PersistentVolumeClaim" in content),
        ("Has name: chroma-data", "chroma-data" in content),
        ("Has ReadWriteOnce", "ReadWriteOnce" in content),
        ("Has storage: 10Gi", "10Gi" in content),
        ("Has storageClassName", "storageClassName:" in content),
    ]

results = validate_pvc(todo1_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"\n  Validating your PVC ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Mount PVC in a Deployment
# ============================================================

print("\n\n--- TODO 2: Mount PVC in ChromaDB Deployment ---\n")

print("  Create a ChromaDB Deployment that mounts the PVC:")
print("    - name: chromadb")
print("    - image: chromadb/chroma:latest")
print("    - containerPort: 8000")
print("    - volumeMount: name=chroma-storage, mountPath=/chroma/chroma")
print("    - volume: name=chroma-storage, persistentVolumeClaim: claimName=chroma-data")

todo2_yaml = textwrap.dedent("""\
    # TODO: Create a ChromaDB Deployment with PVC mount
    # Requirements:
    #   apiVersion: apps/v1
    #   kind: Deployment
    #   name: chromadb, labels: app: chromadb
    #   replicas: 1
    #   container: chromadb, image: chromadb/chroma:latest
    #   containerPort: 8000
    #   volumeMounts:
    #     - name: chroma-storage, mountPath: /chroma/chroma
    #   volumes:
    #     - name: chroma-storage
    #       persistentVolumeClaim:
    #         claimName: chroma-data

""")

with open(os.path.join(WORKDIR, "chromadb-deployment.yaml"), "w") as f:
    f.write(todo2_yaml)

def validate_deployment_pvc(content):
    return [
        ("Has kind: Deployment", "kind: Deployment" in content),
        ("Has name: chromadb", "chromadb" in content),
        ("Has image chromadb/chroma", "chromadb/chroma" in content),
        ("Has containerPort 8000", "8000" in content),
        ("Has volumeMounts section", "volumeMount" in content),
        ("Has mountPath /chroma/chroma", "/chroma/chroma" in content),
        ("Has volumes section", "volumes:" in content),
        ("Has persistentVolumeClaim", "persistentVolumeClaim:" in content),
        ("Has claimName: chroma-data", "chroma-data" in content),
    ]

results2 = validate_deployment_pvc(todo2_yaml)
passed2 = sum(1 for _, ok in results2 if ok)
print(f"\n  Validating your Deployment ({passed2}/{len(results2)}):")
for name, ok in results2:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 04 Summary ---\n")
print("  Key concepts:")
print("    1. PVCs provide persistent storage that survives pod restarts")
print("    2. Access modes: RWO (single node), ROX (read-many), RWX (write-many)")
print("    3. StorageClass enables dynamic provisioning")
print("    4. Mount PVCs via spec.volumes + spec.containers.volumeMounts")
print(f"\n  TODO 1: {passed}/{len(results)} checks passed")
print(f"  TODO 2: {passed2}/{len(results2)} checks passed")
print(f"\n  Files generated in {WORKDIR}/")
