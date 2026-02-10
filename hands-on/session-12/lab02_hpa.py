"""
Lab 02: Horizontal Pod Autoscaler (HPA)
========================================
Learn how HPA automatically scales pods
based on CPU and memory utilization.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-02"

print("=" * 50)
print("  Lab 02: Horizontal Pod Autoscaler")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: How HPA Works
# ============================================================

print("\n--- Step 1: How HPA Works ---\n")

print("  HPA control loop (every 15s by default):")
print("    1. Query metrics-server for pod CPU/memory")
print("    2. Calculate: desired = ceil(current * (currentMetric / targetMetric))")
print("    3. Scale deployment to desired replicas")
print("    4. Respect minReplicas and maxReplicas bounds")

print("\n  Example:")
print("    Current: 3 replicas, CPU at 90%")
print("    Target: 70% CPU")
print("    Desired = ceil(3 * (90/70)) = ceil(3.86) = 4 replicas")
print("    → HPA scales from 3 → 4 pods")


# ============================================================
# Step 2: HPA Scaling Simulation
# ============================================================

print("\n\n--- Step 2: HPA Scaling Simulation ---\n")

class HPASim:
    """Simulate HPA scaling behavior."""

    def __init__(self, min_replicas, max_replicas, target_cpu):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_cpu = target_cpu
        self.replicas = min_replicas

    def evaluate(self, current_cpu):
        import math
        desired = math.ceil(self.replicas * (current_cpu / self.target_cpu))
        desired = max(self.min_replicas, min(self.max_replicas, desired))
        old = self.replicas
        self.replicas = desired
        return old, desired

# Simulate a traffic day
traffic_pattern = [
    ("09:00 Morning startup",   30),
    ("10:00 Normal traffic",    55),
    ("11:00 Traffic increases", 75),
    ("12:00 Lunch spike",       95),
    ("13:00 Still high",        88),
    ("14:00 Settling down",     60),
    ("15:00 Normal",            45),
    ("16:00 Batch job",         92),
    ("17:00 End of day",        35),
    ("18:00 Low traffic",       20),
]

hpa = HPASim(min_replicas=2, max_replicas=10, target_cpu=70)

print(f"  Config: minReplicas=2, maxReplicas=10, targetCPU=70%\n")
print(f"  {'Time':<25} {'CPU%':<8} {'Replicas':<12} {'Action'}")
print(f"  {'-'*65}")

for time_label, cpu in traffic_pattern:
    old, new = hpa.evaluate(cpu)
    if new > old:
        action = f"↑ Scale UP ({old} → {new})"
    elif new < old:
        action = f"↓ Scale DOWN ({old} → {new})"
    else:
        action = "— No change"
    print(f"  {time_label:<25} {cpu:<8} {new:<12} {action}")


# ============================================================
# Step 3: HPA v2 API
# ============================================================

print("\n\n--- Step 3: HPA v2 API (autoscaling/v2) ---\n")

print("  The v2 API supports multiple metrics:")
print("    - CPU utilization")
print("    - Memory utilization")
print("    - Custom metrics (Prometheus)")
print("    - External metrics (cloud provider)")
print("    - Scale-down stabilization window")

example_hpa = textwrap.dedent("""\
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
      maxReplicas: 10
      metrics:
      - type: Resource
        resource:
          name: cpu
          target:
            type: Utilization
            averageUtilization: 70
      - type: Resource
        resource:
          name: memory
          target:
            type: Utilization
            averageUtilization: 80
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
""")

print("  Example HPA v2 YAML:")
for line in example_hpa.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "example-hpa.yaml"), "w") as f:
    f.write(example_hpa)


# ============================================================
# TODO 1: Create an HPA for the Agent API
# ============================================================

print("\n\n--- TODO 1: Create Agent API HPA ---\n")

print("  Create an HPA with:")
print("    - apiVersion: autoscaling/v2")
print("    - name: agent-api-hpa")
print("    - scaleTargetRef: Deployment/agent-api")
print("    - minReplicas: 2")
print("    - maxReplicas: 8")
print("    - CPU target: 70%")
print("    - Memory target: 80%")
print("    - scaleDown stabilizationWindowSeconds: 300")

todo1_yaml = textwrap.dedent("""\
    # TODO: Create an HPA for agent-api
    # Requirements:
    #   apiVersion: autoscaling/v2
    #   kind: HorizontalPodAutoscaler
    #   name: agent-api-hpa
    #   scaleTargetRef: Deployment/agent-api
    #   minReplicas: 2, maxReplicas: 8
    #   CPU target: 70%, Memory target: 80%
    #   behavior.scaleDown.stabilizationWindowSeconds: 300

""")

with open(os.path.join(WORKDIR, "agent-hpa.yaml"), "w") as f:
    f.write(todo1_yaml)

def validate_hpa(content):
    return [
        ("Has autoscaling/v2", "autoscaling/v2" in content),
        ("Has kind: HorizontalPodAutoscaler", "HorizontalPodAutoscaler" in content),
        ("Has scaleTargetRef", "scaleTargetRef:" in content),
        ("References agent-api", "agent-api" in content),
        ("Has minReplicas: 2", "minReplicas: 2" in content),
        ("Has maxReplicas: 8", "maxReplicas: 8" in content),
        ("Has CPU metric", "cpu" in content.lower() and "70" in content),
        ("Has memory metric", "memory" in content.lower() and "80" in content),
        ("Has stabilizationWindowSeconds", "stabilizationWindowSeconds" in content),
        ("Has 300s stabilization", "300" in content),
    ]

results = validate_hpa(todo1_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"\n  Validating your HPA ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: HPA Best Practices Quiz
# ============================================================

print("\n\n--- TODO 2: HPA Best Practices Quiz ---\n")

quiz = [
    {
        "question": "Why set minReplicas >= 2?",
        "answer": "___",
        "correct": "high availability",
        "hint": "What happens if 1 pod crashes and min=1?",
    },
    {
        "question": "Why use scaleDown stabilization (300s)?",
        "answer": "___",
        "correct": "prevent flapping",
        "hint": "What if traffic bounces up and down every minute?",
    },
    {
        "question": "What K8s component must be installed for HPA to work?",
        "answer": "___",
        "correct": "metrics-server",
        "hint": "HPA needs to query pod CPU/memory from somewhere",
    },
    {
        "question": "Why set CPU target at 70% instead of 95%?",
        "answer": "___",
        "correct": "headroom for spikes",
        "hint": "What if a sudden burst arrives before HPA can scale?",
    },
]

# YOUR CODE HERE: Fill in the answers
# quiz[0]["answer"] = "high availability"
# quiz[1]["answer"] = ???
# quiz[2]["answer"] = ???
# quiz[3]["answer"] = ???

score = 0
for i, q in enumerate(quiz, 1):
    is_correct = (q["answer"].lower().replace(" ", "").replace("-", "")
                  == q["correct"].lower().replace(" ", "").replace("-", ""))
    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")
    if status == "TODO":
        print(f"           Hint: {q['hint']}")

print(f"\n  Score: {score}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 02 Summary ---\n")
print("  Key concepts:")
print("    1. HPA scales pods based on CPU/memory metrics")
print("    2. autoscaling/v2 supports multiple metric types")
print("    3. scaleDown stabilization prevents thrashing")
print("    4. metrics-server is required for HPA to work")
print(f"\n  TODO 1: {passed}/{len(results)} checks passed")
print(f"  TODO 2: {score}/{len(quiz)} answers correct")
print(f"\n  Files generated in {WORKDIR}/")
