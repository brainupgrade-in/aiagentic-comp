"""
Lab 01 Solution: Rolling Update Strategies
============================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-01"

print("=" * 50)
print("  Lab 01 Solution: Rolling Update Strategies")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: Deployment with Rolling Update Strategy
# ============================================================

print("\n--- TODO 1 Solution: Agent Deployment with Rolling Update ---\n")

todo1_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: agent-api
      labels:
        app: agent
    spec:
      replicas: 3
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 1
          maxUnavailable: 0
      selector:
        matchLabels:
          app: agent
      template:
        metadata:
          labels:
            app: agent
        spec:
          containers:
          - name: agent
            image: agent-api:2.0
            ports:
            - containerPort: 8000
            readinessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 5
              periodSeconds: 10
""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo1_yaml)

checks = [
    ("Has apiVersion: apps/v1", "apiVersion: apps/v1" in todo1_yaml),
    ("Has kind: Deployment", "kind: Deployment" in todo1_yaml),
    ("Has name: agent-api", "agent-api" in todo1_yaml),
    ("Has replicas: 3", "replicas: 3" in todo1_yaml),
    ("Has strategy type RollingUpdate", "RollingUpdate" in todo1_yaml),
    ("Has maxSurge: 1", "maxSurge: 1" in todo1_yaml),
    ("Has maxUnavailable: 0", "maxUnavailable: 0" in todo1_yaml),
    ("Has readinessProbe", "readinessProbe:" in todo1_yaml),
    ("Has /health path", "/health" in todo1_yaml),
    ("Has containerPort 8000", "8000" in todo1_yaml),
]

passed = sum(1 for _, ok in checks if ok)
print(f"  Deployment validation ({passed}/{len(checks)}):")
for name, ok in checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Strategy explained:")
print("    maxSurge: 1        — Create at most 1 extra pod during update")
print("    maxUnavailable: 0  — Never have fewer than 'replicas' pods")
print("    This means: 3->4->3->4->3->4->3 (always at least 3 available)")


# ============================================================
# TODO 2 Solution: Simulation Values
# ============================================================

print("\n\n--- TODO 2 Solution: Simulation Values ---\n")

# Simulation A: Resource-efficient (never exceed replica count)
sim_a_surge = 0
sim_a_unavail = 1

# Simulation B: Fastest possible (create 2 extra)
sim_b_surge = 2
sim_b_unavail = 0

# Simulation C: Balanced (1 extra, 1 can be unavailable)
sim_c_surge = 1
sim_c_unavail = 1

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

print("\n  Strategy comparison:")
print("    A (surge=0, unavail=1): Never more than 3 pods, 1 less during update")
print("    B (surge=2, unavail=0): Creates 2 new before removing old, uses 5 max")
print("    C (surge=1, unavail=1): 1 extra + 1 less = fastest balanced approach")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 01 Solution complete!")
print(f"- TODO 1: {passed}/{len(checks)} deployment checks passed")
print(f"- TODO 2: {passed2}/{len(sim_checks)} simulation values correct")
