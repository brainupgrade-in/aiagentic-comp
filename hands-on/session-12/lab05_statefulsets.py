"""
Lab 05: StatefulSets
=====================
Learn how StatefulSets differ from Deployments
for stateful workloads like databases and vector stores.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-05"

print("=" * 50)
print("  Lab 05: StatefulSets")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Deployment vs StatefulSet
# ============================================================

print("\n--- Step 1: Deployment vs StatefulSet ---\n")

comparison = [
    ("Feature",           "Deployment",            "StatefulSet"),
    ("Pod names",         "random (agent-abc123)",  "ordinal (chromadb-0, chromadb-1)"),
    ("Startup order",     "All at once",            "Sequential (0, then 1, then 2)"),
    ("Shutdown order",    "Any order",              "Reverse (2, then 1, then 0)"),
    ("Storage",           "Shared PVC (or none)",   "Unique PVC per pod"),
    ("Network identity",  "No stable hostname",     "Stable DNS: pod-0.svc-name"),
    ("Use case",          "Stateless APIs",         "Databases, caches, vector stores"),
]

print(f"  {'Feature':<22} {'Deployment':<26} {'StatefulSet'}")
print(f"  {'-'*74}")
for row in comparison[1:]:
    print(f"  {row[0]:<22} {row[1]:<26} {row[2]}")

print("\n  When to use StatefulSet:")
print("    ✓ Data must survive pod restarts (ChromaDB, PostgreSQL)")
print("    ✓ Pods need stable network names (database replication)")
print("    ✓ Each pod needs its own PVC (unique storage per instance)")
print("\n  When to use Deployment:")
print("    ✓ Stateless services (agent API, web frontend)")
print("    ✓ All pods are interchangeable")
print("    ✓ Shared config via ConfigMap/Secret")


# ============================================================
# Step 2: Headless Services
# ============================================================

print("\n\n--- Step 2: Headless Services ---\n")

print("  StatefulSets require a 'headless' service (clusterIP: None)")
print("  This creates DNS records for individual pods:\n")
print("    Regular Service (clusterIP: auto):")
print("      chromadb-svc → load-balanced to any pod")
print()
print("    Headless Service (clusterIP: None):")
print("      chromadb-0.chromadb-headless → always goes to pod 0")
print("      chromadb-1.chromadb-headless → always goes to pod 1")
print("      chromadb-2.chromadb-headless → always goes to pod 2")

headless_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: chromadb-headless
    spec:
      clusterIP: None          # Makes it headless
      selector:
        app: chromadb
      ports:
      - port: 8000
        targetPort: 8000
""")

print("\n  Headless Service YAML:")
for line in headless_yaml.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "chromadb-headless-svc.yaml"), "w") as f:
    f.write(headless_yaml)


# ============================================================
# Step 3: volumeClaimTemplates
# ============================================================

print("\n\n--- Step 3: volumeClaimTemplates ---\n")

print("  In Deployments:")
print("    - You create 1 PVC manually")
print("    - All pods share the same PVC")
print()
print("  In StatefulSets:")
print("    - volumeClaimTemplates create 1 PVC per pod automatically")
print("    - chromadb-0 → data-chromadb-0 (its own PVC)")
print("    - chromadb-1 → data-chromadb-1 (its own PVC)")
print("    - Deleting a pod does NOT delete its PVC")


# ============================================================
# TODO 1: Create a ChromaDB StatefulSet
# ============================================================

print("\n\n--- TODO 1: Create ChromaDB StatefulSet ---\n")

print("  Create a StatefulSet for ChromaDB:")
print("    - name: chromadb")
print("    - serviceName: chromadb-headless")
print("    - replicas: 1")
print("    - image: chromadb/chroma:latest")
print("    - containerPort: 8000")
print("    - volumeMount: name=data, mountPath=/chroma/chroma")
print("    - volumeClaimTemplates:")
print("        name: data, storage: 10Gi, accessMode: ReadWriteOnce")

todo1_yaml = textwrap.dedent("""\
    # TODO: Create a ChromaDB StatefulSet
    # Requirements:
    #   apiVersion: apps/v1
    #   kind: StatefulSet
    #   name: chromadb
    #   serviceName: chromadb-headless
    #   replicas: 1
    #   selector matchLabels: app: chromadb
    #   container: chromadb, image: chromadb/chroma:latest
    #   containerPort: 8000
    #   volumeMounts: name=data, mountPath=/chroma/chroma
    #   volumeClaimTemplates:
    #     name: data, accessModes: [ReadWriteOnce], storage: 10Gi

""")

with open(os.path.join(WORKDIR, "chromadb-statefulset.yaml"), "w") as f:
    f.write(todo1_yaml)

def validate_statefulset(content):
    return [
        ("Has apiVersion: apps/v1", "apiVersion: apps/v1" in content),
        ("Has kind: StatefulSet", "StatefulSet" in content),
        ("Has name: chromadb", "chromadb" in content),
        ("Has serviceName: chromadb-headless", "chromadb-headless" in content),
        ("Has replicas: 1", "replicas: 1" in content),
        ("Has image chromadb/chroma", "chromadb/chroma" in content),
        ("Has volumeMounts", "volumeMount" in content),
        ("Has mountPath /chroma/chroma", "/chroma/chroma" in content),
        ("Has volumeClaimTemplates", "volumeClaimTemplates" in content),
        ("Has storage 10Gi", "10Gi" in content),
        ("Has ReadWriteOnce", "ReadWriteOnce" in content),
    ]

results = validate_statefulset(todo1_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"\n  Validating your StatefulSet ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: StatefulSet vs Deployment Quiz
# ============================================================

print("\n\n--- TODO 2: StatefulSet Concepts Quiz ---\n")

quiz = [
    {
        "question": "What kind of Service does a StatefulSet require?",
        "answer": "___",
        "correct": "headless",
    },
    {
        "question": "If a StatefulSet has replicas=3, what is the name of the third pod?",
        "answer": "___",
        "correct": "chromadb-2",
        "hint": "Pod names are 0-indexed: name-0, name-1, name-2",
    },
    {
        "question": "Does deleting a StatefulSet pod delete its PVC?",
        "answer": "___",
        "correct": "no",
    },
    {
        "question": "Which should ChromaDB use: Deployment or StatefulSet?",
        "answer": "___",
        "correct": "statefulset",
        "hint": "ChromaDB needs persistent unique storage for embeddings",
    },
]

score = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].lower().strip().replace(" ", "") == q["correct"].lower().strip().replace(" ", "")
    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")
    if status == "TODO" and "hint" in q:
        print(f"           Hint: {q['hint']}")

print(f"\n  Score: {score}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 05 Summary ---\n")
print("  Key concepts:")
print("    1. StatefulSets give pods stable names and unique PVCs")
print("    2. Headless Service (clusterIP: None) provides per-pod DNS")
print("    3. volumeClaimTemplates create 1 PVC per pod automatically")
print("    4. Use StatefulSet for databases and vector stores")
print(f"\n  TODO 1: {passed}/{len(results)} checks passed")
print(f"  TODO 2: {score}/{len(quiz)} answers correct")
print(f"\n  Files generated in {WORKDIR}/")
