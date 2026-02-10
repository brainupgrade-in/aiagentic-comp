"""
Lab 05 Solution: StatefulSets
===============================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-05"

print("=" * 50)
print("  Lab 05 Solution: StatefulSets")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: ChromaDB StatefulSet
# ============================================================

print("\n--- TODO 1 Solution: ChromaDB StatefulSet ---\n")

todo1_yaml = textwrap.dedent("""\
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
    f.write(todo1_yaml)

checks = [
    ("Has apiVersion: apps/v1", "apiVersion: apps/v1" in todo1_yaml),
    ("Has kind: StatefulSet", "StatefulSet" in todo1_yaml),
    ("Has name: chromadb", "chromadb" in todo1_yaml),
    ("Has serviceName: chromadb-headless", "chromadb-headless" in todo1_yaml),
    ("Has replicas: 1", "replicas: 1" in todo1_yaml),
    ("Has image chromadb/chroma", "chromadb/chroma" in todo1_yaml),
    ("Has volumeMounts", "volumeMount" in todo1_yaml),
    ("Has mountPath /chroma/chroma", "/chroma/chroma" in todo1_yaml),
    ("Has volumeClaimTemplates", "volumeClaimTemplates" in todo1_yaml),
    ("Has storage 10Gi", "10Gi" in todo1_yaml),
    ("Has ReadWriteOnce", "ReadWriteOnce" in todo1_yaml),
]

passed = sum(1 for _, ok in checks if ok)
print(f"  StatefulSet validation ({passed}/{len(checks)}):")
for name, ok in checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Key differences from Deployment:")
print("    - serviceName links to headless service for stable DNS")
print("    - volumeClaimTemplates creates 1 PVC per pod automatically")
print("    - Pod names are ordinal: chromadb-0, chromadb-1, etc.")


# ============================================================
# TODO 2 Solution: StatefulSet Concepts Quiz
# ============================================================

print("\n\n--- TODO 2 Solution: StatefulSet Concepts Quiz ---\n")

quiz = [
    {
        "question": "What kind of Service does a StatefulSet require?",
        "answer": "headless",
        "correct": "headless",
    },
    {
        "question": "If a StatefulSet has replicas=3, what is the name of the third pod?",
        "answer": "chromadb-2",
        "correct": "chromadb-2",
    },
    {
        "question": "Does deleting a StatefulSet pod delete its PVC?",
        "answer": "no",
        "correct": "no",
    },
    {
        "question": "Which should ChromaDB use: Deployment or StatefulSet?",
        "answer": "statefulset",
        "correct": "statefulset",
    },
]

score = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].lower().strip().replace(" ", "") == q["correct"].lower().strip().replace(" ", "")
    if is_correct:
        score += 1
    print(f"    [PASS] Q{i}: {q['question']}")
    print(f"           Answer: {q['answer']}")

print(f"\n  Score: {score}/{len(quiz)}")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 05 Solution complete!")
print(f"- TODO 1: {passed}/{len(checks)} StatefulSet checks passed")
print(f"- TODO 2: {score}/{len(quiz)} quiz answers correct")
