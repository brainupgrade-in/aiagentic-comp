"""
Lab 03 Solution: Deployments
==============================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-03"

print("=" * 50)
print("  Lab 03 Solution: Deployments")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


def validate_deployment(content: str) -> list:
    checks = []
    checks.append(("apiVersion: apps/v1", "apiVersion: apps/v1" in content))
    checks.append(("kind: Deployment", "kind: Deployment" in content))
    checks.append(("Has metadata.name", "metadata:" in content and "name:" in content))
    checks.append(("Has replicas", "replicas:" in content))
    checks.append(("Has selector.matchLabels", "matchLabels:" in content))
    checks.append(("Has template.spec.containers", "containers:" in content))
    checks.append(("Has container image", "image:" in content))
    checks.append(("Has containerPort", "containerPort:" in content))
    checks.append(("Has resource requests", "requests:" in content))
    checks.append(("Has resource limits", "limits:" in content))
    checks.append(("Has labels on template", content.count("labels:") >= 2))
    return checks


# ============================================================
# TODO 1 Solution: Redis Deployment
# ============================================================

print("\n--- TODO 1 Solution: Redis Deployment ---\n")

redis_deployment = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: redis
      labels:
        app: redis
        role: cache
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: redis
      template:
        metadata:
          labels:
            app: redis
            role: cache
        spec:
          containers:
          - name: redis
            image: redis:7-alpine
            ports:
            - containerPort: 6379
            resources:
              requests:
                memory: "64Mi"
                cpu: "100m"
              limits:
                memory: "128Mi"
                cpu: "200m"
""")

with open(os.path.join(WORKDIR, "redis-deployment.yaml"), "w") as f:
    f.write(redis_deployment)

results = validate_deployment(redis_deployment)
passed = sum(1 for _, ok in results if ok)
print(f"  Redis Deployment validation ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Redis Deployment features:")
print("    - replicas: 1 (Redis is stateful, single instance for now)")
print("    - selector matches template labels (app: redis)")
print("    - alpine image for small footprint")
print("    - Resources: 64Mi/100m request, 128Mi/200m limit")


# ============================================================
# TODO 2 Solution: Rolling Update Strategy
# ============================================================

print("\n\n--- TODO 2 Solution: Rolling Update Strategy ---\n")

agent_with_strategy = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: unigps-agent
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
            image: unigps-agent:2.0
            ports:
            - containerPort: 8000
            env:
            - name: PYTHONUNBUFFERED
              value: "1"
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "512Mi"
                cpu: "500m"
""")

with open(os.path.join(WORKDIR, "deployment-with-strategy.yaml"), "w") as f:
    f.write(agent_with_strategy)

strategy_checks = [
    ("Has strategy section", "strategy:" in agent_with_strategy),
    ("Type is RollingUpdate", "RollingUpdate" in agent_with_strategy),
    ("Has maxSurge", "maxSurge:" in agent_with_strategy),
    ("Has maxUnavailable", "maxUnavailable:" in agent_with_strategy),
]
all_checks = validate_deployment(agent_with_strategy) + strategy_checks
all_passed = sum(1 for _, ok in all_checks if ok)

print(f"  Deployment with strategy ({all_passed}/{len(all_checks)}):")
for name, ok in all_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Strategy explained:")
print("    maxSurge: 1        — Create at most 1 extra pod during update")
print("    maxUnavailable: 0  — Never have fewer than 'replicas' pods")
print("    This means: 3→4→3→4→3→4→3 (always at least 3 available)")
print("    Zero downtime guaranteed!")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 03 Solution complete!")
print("- TODO 1: Redis Deployment (1 replica, selector match)")
print(f"- TODO 2: Rolling update strategy (maxSurge=1, maxUnavailable=0)")
