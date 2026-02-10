"""
Lab 01: Rolling Update Strategies
===================================
Learn how Kubernetes performs zero-downtime deployments
using rolling updates with maxSurge and maxUnavailable.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-01"

print("=" * 50)
print("  Lab 01: Rolling Update Strategies")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Why Rolling Updates?
# ============================================================

print("\n--- Step 1: Why Rolling Updates? ---\n")

print("  Without rolling updates:")
print("    1. Stop all v1 pods       → DOWNTIME")
print("    2. Start all v2 pods      → users wait")
print("    3. If v2 is broken        → total outage")

print("\n  With rolling updates:")
print("    1. Start 1 new v2 pod     → v1 still serving")
print("    2. v2 passes readiness    → remove 1 v1 pod")
print("    3. Repeat until all v2    → zero downtime")
print("    4. If v2 breaks           → rollback instantly")


# ============================================================
# Step 2: Rolling Update Simulation
# ============================================================

print("\n\n--- Step 2: Rolling Update Simulation ---\n")

class RollingUpdateSim:
    """Simulate rolling update with maxSurge and maxUnavailable."""

    def __init__(self, replicas, max_surge, max_unavailable):
        self.replicas = replicas
        self.max_surge = max_surge
        self.max_unavailable = max_unavailable
        self.old_pods = replicas
        self.new_pods = 0
        self.step = 0

    def update_step(self):
        self.step += 1
        max_total = self.replicas + self.max_surge
        min_available = self.replicas - self.max_unavailable

        # Scale up new pod (if room)
        if self.old_pods + self.new_pods < max_total and self.new_pods < self.replicas:
            self.new_pods += 1

        # Scale down old pod (if enough available)
        if (self.old_pods + self.new_pods > self.replicas and
                self.new_pods >= min_available and self.old_pods > 0):
            self.old_pods -= 1

        return self.old_pods, self.new_pods

    def is_complete(self):
        return self.new_pods >= self.replicas and self.old_pods == 0

    def run(self):
        print(f"  Config: replicas={self.replicas}, "
              f"maxSurge={self.max_surge}, maxUnavailable={self.max_unavailable}")
        print(f"  {'Step':<6} {'Old(v1)':<10} {'New(v2)':<10} {'Total':<8} {'Available':<10}")
        print(f"  {'-'*44}")
        print(f"  {'Start':<6} {self.old_pods:<10} {self.new_pods:<10} "
              f"{self.old_pods + self.new_pods:<8} {self.old_pods + self.new_pods:<10}")

        while not self.is_complete():
            old, new = self.update_step()
            total = old + new
            print(f"  {self.step:<6} {old:<10} {new:<10} {total:<8} {total:<10}")

        print(f"\n  Update complete in {self.step} steps (zero downtime)")


# Example: safe configuration
print("  Example: Safe rolling update (maxSurge=1, maxUnavailable=0)\n")
sim1 = RollingUpdateSim(replicas=3, max_surge=1, max_unavailable=0)
sim1.run()


# ============================================================
# Step 3: Strategy Comparison
# ============================================================

print("\n\n--- Step 3: Strategy Comparison ---\n")

strategies = [
    ("maxSurge=1, maxUnavailable=0", "Safest: always 3+ available, uses 4 pods max"),
    ("maxSurge=0, maxUnavailable=1", "Resource-efficient: never more than 3 pods, but 1 less during update"),
    ("maxSurge=2, maxUnavailable=0", "Fastest: creates 2 new before removing old, uses 5 pods max"),
    ("maxSurge=25%, maxUnavailable=25%", "Default: percentage-based, good for large deployments"),
]

print(f"  {'Configuration':<40} {'Description'}")
print(f"  {'-'*80}")
for config, desc in strategies:
    print(f"  {config:<40} {desc}")


# ============================================================
# Step 4: Rollback Commands
# ============================================================

print("\n\n--- Step 4: Rollback Commands ---\n")

rollback_commands = {
    "View history":        "kubectl rollout history deployment/agent",
    "Check status":        "kubectl rollout status deployment/agent",
    "Undo last update":    "kubectl rollout undo deployment/agent",
    "Undo to revision 2":  "kubectl rollout undo deployment/agent --to-revision=2",
    "Pause rollout":       "kubectl rollout pause deployment/agent",
    "Resume rollout":      "kubectl rollout resume deployment/agent",
}

print(f"  {'Action':<25} {'Command'}")
print(f"  {'-'*70}")
for action, cmd in rollback_commands.items():
    print(f"  {action:<25} {cmd}")


# ============================================================
# TODO 1: Create a Deployment with Rolling Update Strategy
# ============================================================

print("\n\n--- TODO 1: Create Deployment with Rolling Update ---\n")

print("  Create an agent-api Deployment with:")
print("    - name: agent-api")
print("    - replicas: 3")
print("    - image: agent-api:2.0")
print("    - containerPort: 8000")
print("    - strategy: RollingUpdate")
print("    - maxSurge: 1")
print("    - maxUnavailable: 0")
print("    - readinessProbe: httpGet /health port 8000")
print("      initialDelaySeconds: 5, periodSeconds: 10")

todo1_yaml = textwrap.dedent("""\
    # TODO: Create an agent-api Deployment with rolling update strategy
    # Requirements:
    #   apiVersion: apps/v1
    #   kind: Deployment
    #   name: agent-api, labels: app: agent
    #   replicas: 3
    #   strategy: RollingUpdate, maxSurge: 1, maxUnavailable: 0
    #   selector matchLabels: app: agent
    #   container: agent, image: agent-api:2.0, containerPort: 8000
    #   readinessProbe: httpGet /health port 8000 (initialDelay=5, period=10)

""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo1_yaml)


def validate_deployment(content):
    checks = [
        ("Has apiVersion: apps/v1", "apiVersion: apps/v1" in content),
        ("Has kind: Deployment", "kind: Deployment" in content),
        ("Has name: agent-api", "agent-api" in content),
        ("Has replicas: 3", "replicas: 3" in content),
        ("Has strategy type RollingUpdate", "RollingUpdate" in content),
        ("Has maxSurge: 1", "maxSurge: 1" in content or "maxSurge:" in content),
        ("Has maxUnavailable: 0", "maxUnavailable: 0" in content),
        ("Has readinessProbe", "readinessProbe:" in content),
        ("Has /health path", "/health" in content),
        ("Has containerPort 8000", "8000" in content),
    ]
    return checks


results = validate_deployment(todo1_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"\n  Validating your Deployment ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Simulate Different Strategies
# ============================================================

print("\n\n--- TODO 2: Run Simulations ---\n")

print("  Run three rolling update simulations with different configs.")
print("  Fill in the maxSurge and maxUnavailable values:\n")

# Simulation A: Resource-efficient (never exceed replica count)
# Hint: maxSurge=0, maxUnavailable must be >= 1
sim_a_surge = 0        # TODO: Set this value
sim_a_unavail = 0      # TODO: Set this value (hint: 1)

# Simulation B: Fastest possible (create 2 extra, don't remove until ready)
# Hint: maxSurge=2, maxUnavailable=0
sim_b_surge = 0        # TODO: Set this value
sim_b_unavail = 0      # TODO: Set this value

# Simulation C: Balanced (1 extra, 1 can be unavailable)
# Hint: maxSurge=1, maxUnavailable=1
sim_c_surge = 0        # TODO: Set this value
sim_c_unavail = 0      # TODO: Set this value

sim_checks = [
    ("Sim A: Resource-efficient (surge=0, unavail=1)",
     sim_a_surge == 0 and sim_a_unavail == 1),
    ("Sim B: Fastest (surge=2, unavail=0)",
     sim_b_surge == 2 and sim_b_unavail == 0),
    ("Sim C: Balanced (surge=1, unavail=1)",
     sim_c_surge == 1 and sim_c_unavail == 1),
]

passed2 = sum(1 for _, ok in sim_checks if ok)
print(f"  Simulation validation ({passed2}/{len(sim_checks)}):")
for name, ok in sim_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

if passed2 == len(sim_checks):
    print("\n  Running your simulations:\n")
    for label, surge, unavail in [
        ("A: Resource-efficient", sim_a_surge, sim_a_unavail),
        ("B: Fastest", sim_b_surge, sim_b_unavail),
        ("C: Balanced", sim_c_surge, sim_c_unavail),
    ]:
        print(f"\n  --- Simulation {label} ---")
        sim = RollingUpdateSim(replicas=3, max_surge=surge, max_unavailable=unavail)
        sim.run()


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 01 Summary ---\n")
print("  Key concepts:")
print("    1. Rolling updates replace pods gradually (zero downtime)")
print("    2. maxSurge controls extra pods during update")
print("    3. maxUnavailable controls minimum available pods")
print("    4. kubectl rollout undo for instant rollback")
print(f"\n  TODO 1: {passed}/{len(results)} checks passed")
print(f"  TODO 2: {passed2}/{len(sim_checks)} checks passed")
print(f"\n  Files generated in {WORKDIR}/")
