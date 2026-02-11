"""
Lab 03: Resource Management & Autoscaling
============================================
Configure CPU/memory requests and limits,
and set up HorizontalPodAutoscaler.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-03"

print("=" * 50)
print("  Lab 03: Resource Management & Autoscaling")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Requests vs Limits
# ============================================================

print("\n--- Step 1: Requests vs Limits ---\n")

print("  resources:")
print("    requests:          # Scheduling guarantee")
print("      memory: 256Mi   # Node must have this free to schedule")
print("      cpu: 250m       # 0.25 CPU cores guaranteed")
print("    limits:            # Hard ceiling")
print("      memory: 1Gi     # OOMKilled if exceeded")
print("      cpu: 1000m      # Throttled if exceeded")

print("\n  Key rules:")
rules = [
    ("Set both requests AND limits", "Prevents resource starvation"),
    ("requests <= limits",           "Limits must be >= requests"),
    ("requests = typical usage",     "Based on actual profiling"),
    ("limits = max acceptable",      "Buffer above requests (2-4x)"),
]
for rule, why in rules:
    print(f"    {rule:<35} -> {why}")


# ============================================================
# Step 2: HorizontalPodAutoscaler
# ============================================================

print("\n\n--- Step 2: HorizontalPodAutoscaler (HPA) ---\n")

hpa_yaml = textwrap.dedent("""\
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: agent-hpa
      namespace: ai-stack
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: agent-api
      minReplicas: 2
      maxReplicas: 10
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
""")

print("  HPA auto-scales pods based on CPU:\n")
for line in hpa_yaml.strip().split("\n"):
    print(f"    {line}")

print("\n  How it works:")
print("    CPU < 70%  -> scale down (min 2 pods)")
print("    CPU > 70%  -> scale up (max 10 pods)")
print("    Stabilization: ~60s before scaling, prevents flapping")

with open(os.path.join(WORKDIR, "hpa-reference.yaml"), "w") as f:
    f.write(hpa_yaml)


# ============================================================
# Step 3: PodDisruptionBudget
# ============================================================

print("\n\n--- Step 3: PodDisruptionBudget (PDB) ---\n")

pdb_yaml = textwrap.dedent("""\
    apiVersion: policy/v1
    kind: PodDisruptionBudget
    metadata:
      name: agent-pdb
      namespace: ai-stack
    spec:
      minAvailable: 2
      selector:
        matchLabels:
          app: agent-api
""")

print("  PDB ensures minimum pods during disruptions:\n")
for line in pdb_yaml.strip().split("\n"):
    print(f"    {line}")

print("\n  Scenarios:")
print("    Node drain for maintenance -> PDB keeps 2+ agent pods running")
print("    Cluster upgrade -> voluntary evictions respect PDB")

with open(os.path.join(WORKDIR, "pdb-reference.yaml"), "w") as f:
    f.write(pdb_yaml)


# ============================================================
# TODO 1: Create HPA + PDB manifests
# ============================================================

print("\n\n--- TODO 1: HPA + PDB Configuration ---\n")

print("  Create YAML with:")
print("    HPA:")
print("      - Target: agent-api Deployment")
print("      - Min replicas: 2, Max replicas: 10")
print("      - CPU target: 70% utilization")
print("    PDB:")
print("      - minAvailable: 2")
print("      - Selector: app=agent-api\n")

todo1_yaml = textwrap.dedent("""\
    apiVersion: autoscaling/v2
    kind: HorizontalPodAutoscaler
    metadata:
      name: agent-hpa
      namespace: ai-stack
    spec:
      scaleTargetRef:
        apiVersion: apps/v1
        kind: Deployment
        name: agent-api
      minReplicas: 2
      maxReplicas: 10
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
    ---
    apiVersion: policy/v1
    kind: PodDisruptionBudget
    metadata:
      name: agent-pdb
      namespace: ai-stack
    spec:
      minAvailable: 2
      selector:
        matchLabels:
          app: agent-api
""")

with open(os.path.join(WORKDIR, "autoscaling.yaml"), "w") as f:
    f.write(todo1_yaml)

checks1 = [
    ("Has HPA kind",               "HorizontalPodAutoscaler" in todo1_yaml),
    ("Has autoscaling API",        "autoscaling" in todo1_yaml),
    ("Has scaleTargetRef",         "scaleTargetRef" in todo1_yaml),
    ("Has agent-api target",       "agent-api" in todo1_yaml),
    ("Has minReplicas: 2",         "minReplicas: 2" in todo1_yaml or "minReplicas:2" in todo1_yaml),
    ("Has maxReplicas: 10",        "maxReplicas: 10" in todo1_yaml or "maxReplicas:10" in todo1_yaml),
    ("Has CPU metric",             "cpu" in todo1_yaml.lower()),
    ("Has 70% target",             "70" in todo1_yaml),
    ("Has PDB kind",               "PodDisruptionBudget" in todo1_yaml),
    ("Has minAvailable: 2",        "minAvailable: 2" in todo1_yaml or "minAvailable:2" in todo1_yaml),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Resource management quiz
# ============================================================

print("\n\n--- TODO 2: Resource Management Quiz ---\n")

quiz = [
    {
        "question": "What happens when a container exceeds its memory limit?",
        "answer": "OOMKilled",
        "correct": "oomkilled",
        "check": "oom",
    },
    {
        "question": "What happens when a container exceeds its CPU limit?",
        "answer": "throttled",
        "correct": "throttled",
        "check": "throttl",
    },
    {
        "question": "What CPU target % is recommended for HPA? (number)",
        "answer": "70",
        "correct": "70",
        "check": "70",
    },
    {
        "question": "What resource field is used for scheduling decisions?",
        "answer": "requests",
        "correct": "requests",
        "check": "request",
    },
    {
        "question": "What K8s object prevents all pods from being evicted at once?",
        "answer": "PDB",
        "correct": "pdb",
        "check": "pdb",
    },
]

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    is_correct = q["check"] in answer

    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 03 Summary ---\n")
print("  Key concepts:")
print("    1. Requests = scheduling guarantee, Limits = hard ceiling")
print("    2. Memory exceeds limit -> OOMKilled, CPU exceeds -> throttled")
print("    3. HPA: auto-scale on CPU (target 70%, min 2, max 10)")
print("    4. PDB: ensure minAvailable during disruptions")
print(f"\n  TODO 1: {score1}/{len(checks1)} autoscaling checks")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
