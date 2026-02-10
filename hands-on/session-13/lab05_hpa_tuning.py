"""
Lab 05: HPA Tuning & Best Practices
======================================
Configure Horizontal Pod Autoscaler for production workloads.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-05"

print("=" * 50)
print("  Lab 05: HPA Tuning & Best Practices")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: HPA tuning guidelines
# ============================================================

print("\n--- Step 1: HPA Tuning Guidelines ---\n")

guidelines = [
    {
        "rule": "minReplicas >= 2",
        "why": "Never scale to 1 in production — single pod = single point of failure",
        "bad": "minReplicas: 1",
        "good": "minReplicas: 2 (or 3 for critical services)",
    },
    {
        "rule": "CPU target: 60-80%",
        "why": "Too low = wasteful scaling; too high = no headroom for spikes",
        "bad": "targetCPUUtilizationPercentage: 95 (no room for spikes)",
        "good": "targetAverageUtilization: 70 (sweet spot for most APIs)",
    },
    {
        "rule": "Resource requests REQUIRED",
        "why": "HPA calculates percentage based on resource requests",
        "bad": "No resource requests set (HPA cannot calculate %)",
        "good": "requests: cpu=250m, memory=256Mi (HPA needs this baseline)",
    },
    {
        "rule": "Scale-down stabilization",
        "why": "Prevent flapping: don't scale down immediately after a spike",
        "bad": "No stabilization (scales down instantly, then back up = flapping)",
        "good": "scaleDown stabilizationWindowSeconds: 300 (wait 5 min before scaling down)",
    },
    {
        "rule": "Scale-up stabilization",
        "why": "Allow pods to become ready before deciding to scale more",
        "bad": "No stabilization (keeps adding pods before existing ones are ready)",
        "good": "scaleUp stabilizationWindowSeconds: 60 (wait 1 min between scale-ups)",
    },
    {
        "rule": "Multiple metrics",
        "why": "CPU alone misses memory-bound workloads (AI/ML models)",
        "bad": "Only CPU metric for an AI service that's memory-bound",
        "good": "Both CPU (70%) and Memory (80%) metrics",
    },
]

for g in guidelines:
    print(f"  Rule: {g['rule']}")
    print(f"    Why:  {g['why']}")
    print(f"    Bad:  {g['bad']}")
    print(f"    Good: {g['good']}")
    print()


# ============================================================
# Step 2: HPA flapping simulation
# ============================================================

print("\n--- Step 2: HPA Flapping — Without vs With Stabilization ---\n")

class HPASimulator:
    """Simulates HPA scaling decisions."""
    def __init__(self, min_replicas, max_replicas, target_cpu_pct,
                 stabilization_down_sec=0, stabilization_up_sec=0):
        self.min_replicas = min_replicas
        self.max_replicas = max_replicas
        self.target_cpu_pct = target_cpu_pct
        self.stabilization_down_sec = stabilization_down_sec
        self.stabilization_up_sec = stabilization_up_sec
        self.current_replicas = min_replicas
        self.last_scale_down_time = -999
        self.last_scale_up_time = -999

    def decide(self, current_cpu_pct, time_sec):
        desired = max(
            self.min_replicas,
            min(self.max_replicas,
                round(self.current_replicas * current_cpu_pct / self.target_cpu_pct))
        )

        action = "hold"
        if desired > self.current_replicas:
            if time_sec - self.last_scale_up_time >= self.stabilization_up_sec:
                action = "scale-up"
                self.current_replicas = desired
                self.last_scale_up_time = time_sec
            else:
                action = "hold (stabilizing up)"
        elif desired < self.current_replicas:
            if time_sec - self.last_scale_down_time >= self.stabilization_down_sec:
                action = "scale-down"
                self.current_replicas = desired
                self.last_scale_down_time = time_sec
            else:
                action = "hold (stabilizing down)"

        return self.current_replicas, action

# Traffic pattern: spike then drop then spike (flap scenario)
traffic = [
    (0,   30),   # low
    (30,  80),   # spike
    (60,  90),   # peak
    (90,  40),   # drop
    (120, 35),   # low
    (150, 85),   # spike again
    (180, 30),   # drop
    (210, 25),   # low
    (240, 20),   # low
    (270, 75),   # spike
    (300, 30),   # drop
]

# Without stabilization
print("  WITHOUT stabilization (flapping):")
hpa_no_stab = HPASimulator(min_replicas=2, max_replicas=10, target_cpu_pct=70,
                            stabilization_down_sec=0, stabilization_up_sec=0)
scale_changes_no_stab = 0
prev_replicas = 2
for time_sec, cpu_pct in traffic:
    replicas, action = hpa_no_stab.decide(cpu_pct, time_sec)
    if replicas != prev_replicas:
        scale_changes_no_stab += 1
    prev_replicas = replicas
    marker = " <-- SCALE" if "scale" in action else ""
    print(f"    t={time_sec:>3}s  CPU={cpu_pct:>3}%  replicas={replicas}  action={action}{marker}")

print(f"\n  Total scaling events: {scale_changes_no_stab} (flapping!)\n")

# With stabilization
print("  WITH stabilization (stable):")
hpa_stab = HPASimulator(min_replicas=2, max_replicas=10, target_cpu_pct=70,
                         stabilization_down_sec=300, stabilization_up_sec=60)
scale_changes_stab = 0
prev_replicas = 2
for time_sec, cpu_pct in traffic:
    replicas, action = hpa_stab.decide(cpu_pct, time_sec)
    if replicas != prev_replicas:
        scale_changes_stab += 1
    prev_replicas = replicas
    marker = " <-- SCALE" if action.startswith("scale") else ""
    print(f"    t={time_sec:>3}s  CPU={cpu_pct:>3}%  replicas={replicas}  action={action}{marker}")

print(f"\n  Total scaling events: {scale_changes_stab} (stable!)")
print(f"\n  Stabilization reduced flapping from {scale_changes_no_stab} to {scale_changes_stab} scaling events.")


# ============================================================
# TODO 1: Create production HPA YAML
# ============================================================

print("\n\n--- TODO 1: Create Production HPA ---\n")

print("  Create a production-ready HPA with these requirements:")
print("    - apiVersion: autoscaling/v2")
print("    - name: agent-hpa")
print("    - scaleTargetRef: Deployment/unigps-agent")
print("    - minReplicas: 2")
print("    - maxReplicas: 10")
print("    - CPU metric: targetAverageUtilization 70%")
print("    - Memory metric: targetAverageUtilization 80%")
print("    - scaleDown stabilizationWindowSeconds: 300")
print("    - scaleUp stabilizationWindowSeconds: 60\n")

# YOUR CODE HERE: Create the HPA YAML
hpa_yaml = textwrap.dedent("""\
    # TODO: Create production HPA YAML
    # Remember:
    #   - Use autoscaling/v2 API version
    #   - Set min and max replicas
    #   - Add CPU and memory metrics with target utilization
    #   - Add behavior section with stabilization windows
    #   - scaleTargetRef should point to the Deployment

""")

with open(os.path.join(WORKDIR, "hpa.yaml"), "w") as f:
    f.write(hpa_yaml)

# Validate
hpa_checks = [
    ("apiVersion: autoscaling/v2",
     "autoscaling/v2" in hpa_yaml),
    ("kind: HorizontalPodAutoscaler",
     "HorizontalPodAutoscaler" in hpa_yaml),
    ("Has scaleTargetRef",
     "scaleTargetRef:" in hpa_yaml),
    ("minReplicas: 2",
     "minReplicas: 2" in hpa_yaml or "minReplicas:2" in hpa_yaml),
    ("maxReplicas: 10",
     "maxReplicas: 10" in hpa_yaml or "maxReplicas:10" in hpa_yaml),
    ("CPU metric with averageUtilization",
     "cpu" in hpa_yaml.lower() and "averageUtilization" in hpa_yaml),
    ("Memory metric",
     "memory" in hpa_yaml.lower()),
    ("scaleDown stabilization",
     "scaleDown:" in hpa_yaml and "stabilizationWindowSeconds" in hpa_yaml),
    ("scaleUp stabilization",
     "scaleUp:" in hpa_yaml and "stabilizationWindowSeconds" in hpa_yaml),
    ("Has behavior section",
     "behavior:" in hpa_yaml),
]

passed = sum(1 for _, ok in hpa_checks if ok)
print(f"  HPA validation ({passed}/{len(hpa_checks)}):")
for name, ok in hpa_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: HPA anti-patterns quiz
# ============================================================

print("\n\n--- TODO 2: HPA Anti-Patterns Quiz ---\n")

print("  Identify what's WRONG with each HPA configuration.\n")

antipattern_quiz = [
    {
        "config": "minReplicas: 1, maxReplicas: 100, targetCPU: 50%",
        "question": "What are TWO problems with this HPA?",
        "answer": "_______________",
        # Answer: minReplicas=1 is a SPOF; maxReplicas=100 could cause cost explosion; targetCPU=50% is wasteful
    },
    {
        "config": "Deployment has NO resource requests set, HPA targets CPU 70%",
        "question": "Why will this HPA not work at all?",
        "answer": "_______________",
        # Answer: HPA cannot calculate CPU % without resource requests as baseline
    },
    {
        "config": "minReplicas: 5, maxReplicas: 5, targetCPU: 80%",
        "question": "What is the problem with this HPA?",
        "answer": "_______________",
        # Answer: min=max means HPA cannot scale at all — it's effectively disabled
    },
    {
        "config": "No scaleDown stabilization, traffic is bursty (spikes every 2 minutes)",
        "question": "What will happen during traffic spikes?",
        "answer": "_______________",
        # Answer: HPA will flap — scale up on spike, immediately scale down, repeat
    },
]

# YOUR CODE HERE: Fill in the answers for each anti-pattern
# antipattern_quiz[0]["answer"] = ???
# antipattern_quiz[1]["answer"] = ???
# antipattern_quiz[2]["answer"] = ???
# antipattern_quiz[3]["answer"] = ???

quiz_score = 0
for i, q in enumerate(antipattern_quiz, 1):
    print(f"  Q{i}: Config: {q['config']}")
    print(f"      Question: {q['question']}")
    is_filled = q["answer"] != "_______________"
    if is_filled:
        quiz_score += 1
    status = "PASS" if is_filled else "FAIL"
    print(f"  [{status}] Answer: {q['answer']}")
    print()

print(f"  Score: {quiz_score}/{len(antipattern_quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 05 Summary ---\n")
print("  Key concepts:")
print("    1. HPA needs resource requests to calculate utilization %")
print("    2. minReplicas >= 2 in production (no single point of failure)")
print("    3. CPU target 60-80% is the sweet spot for most services")
print("    4. Stabilization windows prevent flapping (scale-down: 300s, scale-up: 60s)")
print("    5. Use multiple metrics (CPU + Memory) for AI/ML workloads")
print("    6. autoscaling/v2 supports advanced behaviors and multiple metrics")
print(f"\n  TODO 1: {passed}/{len(hpa_checks)} HPA checks passed")
print(f"  TODO 2: {quiz_score}/{len(antipattern_quiz)} anti-pattern quiz answers")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<40} ({size} bytes)")
