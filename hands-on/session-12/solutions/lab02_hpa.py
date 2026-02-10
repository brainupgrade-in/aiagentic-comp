"""
Lab 02 Solution: Horizontal Pod Autoscaler
============================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-02"

print("=" * 50)
print("  Lab 02 Solution: Horizontal Pod Autoscaler")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: HPA YAML
# ============================================================

print("\n--- TODO 1 Solution: Agent API HPA ---\n")

todo1_yaml = textwrap.dedent("""\
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
      maxReplicas: 8
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

with open(os.path.join(WORKDIR, "agent-hpa.yaml"), "w") as f:
    f.write(todo1_yaml)

checks = [
    ("Has autoscaling/v2", "autoscaling/v2" in todo1_yaml),
    ("Has kind: HorizontalPodAutoscaler", "HorizontalPodAutoscaler" in todo1_yaml),
    ("Has scaleTargetRef", "scaleTargetRef:" in todo1_yaml),
    ("References agent-api", "agent-api" in todo1_yaml),
    ("Has minReplicas: 2", "minReplicas: 2" in todo1_yaml),
    ("Has maxReplicas: 8", "maxReplicas: 8" in todo1_yaml),
    ("Has CPU metric", "cpu" in todo1_yaml.lower() and "70" in todo1_yaml),
    ("Has memory metric", "memory" in todo1_yaml.lower() and "80" in todo1_yaml),
    ("Has stabilizationWindowSeconds", "stabilizationWindowSeconds" in todo1_yaml),
    ("Has 300s stabilization", "300" in todo1_yaml),
]

passed = sum(1 for _, ok in checks if ok)
print(f"  HPA validation ({passed}/{len(checks)}):")
for name, ok in checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  HPA features:")
print("    - autoscaling/v2: supports multiple metrics (CPU + memory)")
print("    - minReplicas: 2 for high availability")
print("    - maxReplicas: 8 as cost ceiling")
print("    - 300s stabilization prevents scale-down thrashing")


# ============================================================
# TODO 2 Solution: Best Practices Quiz
# ============================================================

print("\n\n--- TODO 2 Solution: HPA Best Practices Quiz ---\n")

quiz = [
    {
        "question": "Why set minReplicas >= 2?",
        "answer": "high availability",
        "correct": "high availability",
    },
    {
        "question": "Why use scaleDown stabilization (300s)?",
        "answer": "prevent flapping",
        "correct": "prevent flapping",
    },
    {
        "question": "What K8s component must be installed for HPA to work?",
        "answer": "metrics-server",
        "correct": "metrics-server",
    },
    {
        "question": "Why set CPU target at 70% instead of 95%?",
        "answer": "headroom for spikes",
        "correct": "headroom for spikes",
    },
]

score = 0
for i, q in enumerate(quiz, 1):
    is_correct = (q["answer"].lower().replace(" ", "").replace("-", "")
                  == q["correct"].lower().replace(" ", "").replace("-", ""))
    if is_correct:
        score += 1
    print(f"    [PASS] Q{i}: {q['question']}")
    print(f"           Answer: {q['answer']}")

print(f"\n  Score: {score}/{len(quiz)}")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 02 Solution complete!")
print(f"- TODO 1: {passed}/{len(checks)} HPA checks passed")
print(f"- TODO 2: {score}/{len(quiz)} quiz answers correct")
