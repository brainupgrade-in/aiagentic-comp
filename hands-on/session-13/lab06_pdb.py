"""
Lab 06: Pod Disruption Budgets
================================
Protect application availability during voluntary disruptions.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-06"

print("=" * 50)
print("  Lab 06: Pod Disruption Budgets")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Why Pod Disruption Budgets?
# ============================================================

print("\n--- Step 1: Why PDB? Voluntary Disruptions ---\n")

print("  Kubernetes has TWO types of disruptions:\n")

disruptions = [
    {
        "type": "Voluntary (PDB helps)",
        "examples": [
            "kubectl drain node (for maintenance)",
            "Cluster upgrade (node-by-node rolling upgrade)",
            "Cluster autoscaler removing underutilized nodes",
            "kubectl delete pod (manual deletion)",
        ],
        "description": "Planned events that K8s can control the pace of",
    },
    {
        "type": "Involuntary (PDB does NOT help)",
        "examples": [
            "Node hardware failure (node dies)",
            "OOMKilled (kernel kills container)",
            "VM instance preemption (spot/preemptible instance reclaimed)",
            "Kernel panic on the node",
        ],
        "description": "Unplanned events outside K8s control",
    },
]

for d in disruptions:
    print(f"  {d['type']}")
    print(f"    {d['description']}")
    for ex in d["examples"]:
        print(f"      - {ex}")
    print()

print("  PDB tells K8s: 'During voluntary disruptions, ALWAYS keep at")
print("  least N pods running (or disrupt at most M pods at a time).'\n")

print("  Without PDB, a 'kubectl drain' could kill ALL your pods at once!")


# ============================================================
# Step 2: Without vs with PDB simulation
# ============================================================

print("\n\n--- Step 2: Node Drain — Without vs With PDB ---\n")

class PDBSimulator:
    """Simulates node drain with and without PDB."""
    def __init__(self, replicas, pods_on_node, pdb_min_available=None):
        self.replicas = replicas
        self.pods_on_node = pods_on_node  # how many pods are on the node being drained
        self.pdb_min_available = pdb_min_available

    def drain(self):
        steps = []
        running = self.replicas
        to_evict = self.pods_on_node

        if self.pdb_min_available is None:
            # No PDB: drain evicts all pods on the node at once
            steps.append(f"  Before drain: {running} pods running")
            running -= to_evict
            steps.append(f"  kubectl drain node-2: evicts {to_evict} pods at once")
            steps.append(f"  During drain: {running} pods running  <-- POTENTIAL OUTAGE!")
            steps.append(f"  New pods scheduled on other nodes: takes 10-30 seconds")
            steps.append(f"  Users experience: 503 errors for 10-30 seconds")
            return steps

        # With PDB: drain respects minAvailable
        steps.append(f"  PDB: minAvailable={self.pdb_min_available}")
        steps.append(f"  Before drain: {running} pods running")

        evicted = 0
        for i in range(to_evict):
            can_evict = (running - 1) >= self.pdb_min_available
            if can_evict:
                running -= 1
                evicted += 1
                steps.append(f"  Step {i+1}: Evict 1 pod ({running} running >= {self.pdb_min_available} min) -> OK")
                # K8s creates replacement before evicting next
                running += 1
                steps.append(f"  Step {i+1}: Replacement pod ready ({running} running) -> evict next")
            else:
                steps.append(f"  Step {i+1}: BLOCKED — evicting would leave {running-1} < {self.pdb_min_available} min")
                steps.append(f"  Step {i+1}: Drain waits for replacement pod to be ready...")
                running += 1  # simulate replacement becoming ready
                running -= 1  # then evict
                evicted += 1
                steps.append(f"  Step {i+1}: Replacement ready -> evict -> {running} running >= {self.pdb_min_available}")

        steps.append(f"  After drain: {running} pods running, {evicted} pods evicted")
        steps.append(f"  Users experience: ZERO downtime!")
        return steps


# Without PDB
print("  Scenario: 3 replicas of agent, 2 on node-2. Admin drains node-2.\n")

print("  WITHOUT PDB:")
no_pdb = PDBSimulator(replicas=3, pods_on_node=2, pdb_min_available=None)
for step in no_pdb.drain():
    print(f"  {step}")

print()

print("  WITH PDB (minAvailable: 2):")
with_pdb = PDBSimulator(replicas=3, pods_on_node=2, pdb_min_available=2)
for step in with_pdb.drain():
    print(f"  {step}")

print()
print("  PDB ensures K8s evicts pods ONE AT A TIME, waiting for")
print("  replacements to be ready before evicting the next pod.")


# ============================================================
# Step 3: PDB YAML reference
# ============================================================

print("\n\n--- Step 3: PDB YAML Reference ---\n")

pdb_example_min = textwrap.dedent("""\
    apiVersion: policy/v1
    kind: PodDisruptionBudget
    metadata:
      name: agent-pdb
    spec:
      minAvailable: 2
      selector:
        matchLabels:
          app: agent
""")

pdb_example_max = textwrap.dedent("""\
    apiVersion: policy/v1
    kind: PodDisruptionBudget
    metadata:
      name: agent-pdb
    spec:
      maxUnavailable: 1
      selector:
        matchLabels:
          app: agent
""")

print("  Option A: minAvailable (minimum pods that must stay running)")
for line in pdb_example_min.strip().split("\n"):
    print(f"    {line}")

print()
print("  Option B: maxUnavailable (maximum pods that can be down at once)")
for line in pdb_example_max.strip().split("\n"):
    print(f"    {line}")

print()
print("  minAvailable vs maxUnavailable:")
print("    - minAvailable: 2 with 3 replicas -> at most 1 can be disrupted")
print("    - maxUnavailable: 1 with 3 replicas -> same effect!")
print("    - maxUnavailable scales better: works with HPA (any replica count)")
print("    - minAvailable: '50%' also works (percentage of replicas)")

with open(os.path.join(WORKDIR, "pdb-reference-min.yaml"), "w") as f:
    f.write(pdb_example_min)

with open(os.path.join(WORKDIR, "pdb-reference-max.yaml"), "w") as f:
    f.write(pdb_example_max)

print("\n  Generated: pdb-reference-min.yaml, pdb-reference-max.yaml")


# ============================================================
# TODO 1: Create PDB YAML
# ============================================================

print("\n\n--- TODO 1: Create a Pod Disruption Budget ---\n")

print("  Create a PDB for the AI Agent Deployment with these requirements:")
print("    - apiVersion: policy/v1")
print("    - kind: PodDisruptionBudget")
print("    - name: agent-pdb")
print("    - minAvailable: 2")
print("    - selector: matchLabels: app: agent")
print()
print("  The Deployment has 3 replicas with label 'app: agent'.\n")

# YOUR CODE HERE: Create the PDB YAML
pdb_yaml = textwrap.dedent("""\
    # TODO: Create PDB for the AI Agent
    # Remember:
    #   - Use policy/v1 API version
    #   - Set the minimum number of pods that must stay available
    #   - selector must match the Deployment's pod labels

""")

with open(os.path.join(WORKDIR, "agent-pdb.yaml"), "w") as f:
    f.write(pdb_yaml)

# Validate
pdb_checks = [
    ("apiVersion: policy/v1",
     "policy/v1" in pdb_yaml),
    ("kind: PodDisruptionBudget",
     "PodDisruptionBudget" in pdb_yaml),
    ("Has metadata name",
     "name:" in pdb_yaml),
    ("Has minAvailable: 2",
     "minAvailable: 2" in pdb_yaml or "minAvailable:2" in pdb_yaml),
    ("Has selector with matchLabels",
     "matchLabels:" in pdb_yaml),
    ("Selector includes app: agent",
     "app: agent" in pdb_yaml or "app:agent" in pdb_yaml),
]

passed = sum(1 for _, ok in pdb_checks if ok)
print(f"  PDB validation ({passed}/{len(pdb_checks)}):")
for name, ok in pdb_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: PDB quiz
# ============================================================

print("\n\n--- TODO 2: PDB Knowledge Quiz ---\n")

pdb_quiz = [
    {
        "question": "You have 5 replicas and PDB minAvailable=3. How many pods can be disrupted at once?",
        "answer": "___",
        "correct": "2",
    },
    {
        "question": "You have 4 replicas and PDB maxUnavailable=1. How many pods MUST stay running during drain?",
        "answer": "___",
        "correct": "3",
    },
    {
        "question": "A node crashes (hardware failure). Does PDB protect your pods? (yes/no)",
        "answer": "___",
        "correct": "no",
    },
    {
        "question": "You have 2 replicas and PDB minAvailable=2. What happens when you drain the node with 1 pod?",
        "answer": "___",
        "correct": "drain blocks until replacement is ready",
    },
    {
        "question": "Which is better for HPA-scaled Deployments: minAvailable or maxUnavailable?",
        "answer": "___",
        "correct": "maxUnavailable",
    },
    {
        "question": "Can you use BOTH minAvailable AND maxUnavailable in the same PDB? (yes/no)",
        "answer": "___",
        "correct": "no",
    },
]

# YOUR CODE HERE: Fill in the answers
# pdb_quiz[0]["answer"] = "2"
# pdb_quiz[1]["answer"] = ???
# pdb_quiz[2]["answer"] = ???
# pdb_quiz[3]["answer"] = ???
# pdb_quiz[4]["answer"] = ???
# pdb_quiz[5]["answer"] = ???

quiz_score = 0
for i, q in enumerate(pdb_quiz, 1):
    is_correct = q["answer"].strip().lower() == q["correct"].strip().lower()
    if is_correct:
        quiz_score += 1
    status = "PASS" if is_correct else "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")
    if is_correct:
        print(f"           Your answer: {q['answer']}")
    else:
        print(f"           Your answer: {q['answer']}  (fill in the answer)")

print(f"\n  Score: {quiz_score}/{len(pdb_quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 06 Summary ---\n")
print("  Key concepts:")
print("    1. PDB protects against VOLUNTARY disruptions (drain, upgrades)")
print("    2. PDB does NOT protect against involuntary disruptions (node crash, OOM)")
print("    3. minAvailable = minimum pods that must stay running")
print("    4. maxUnavailable = maximum pods that can be down (better for HPA)")
print("    5. Without PDB, 'kubectl drain' can kill all pods at once = outage")
print("    6. Always set PDB for production Deployments with 2+ replicas")
print(f"\n  TODO 1: {passed}/{len(pdb_checks)} PDB YAML checks passed")
print(f"  TODO 2: {quiz_score}/{len(pdb_quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<40} ({size} bytes)")
