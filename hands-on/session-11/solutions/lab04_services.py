"""
Lab 04 Solution: Services
===========================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-04"

print("=" * 50)
print("  Lab 04 Solution: Services")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


def validate_service(content: str) -> list:
    checks = []
    checks.append(("Has apiVersion: v1", "apiVersion: v1" in content))
    checks.append(("Has kind: Service", "kind: Service" in content))
    checks.append(("Has metadata.name", "metadata:" in content and "name:" in content))
    checks.append(("Has spec.selector", "selector:" in content))
    checks.append(("Has spec.ports", "ports:" in content))
    checks.append(("Has port defined", "port:" in content))
    checks.append(("Has targetPort defined", "targetPort:" in content))
    return checks


# ============================================================
# TODO 1 Solution: Redis ClusterIP Service
# ============================================================

print("\n--- TODO 1 Solution: Redis Service ---\n")

redis_svc_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: redis-svc
    spec:
      type: ClusterIP
      selector:
        app: redis
      ports:
      - port: 6379
        targetPort: 6379
""")

with open(os.path.join(WORKDIR, "redis-service.yaml"), "w") as f:
    f.write(redis_svc_yaml)

results = validate_service(redis_svc_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"  Redis Service validation ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  How other pods connect:")
print("    REDIS_URL=redis://redis-svc:6379")
print("    The DNS name 'redis-svc' resolves to the Service ClusterIP.")
print("    Traffic is load-balanced across all pods with label app=redis.")


# ============================================================
# TODO 2 Solution: LoadBalancer Service
# ============================================================

print("\n\n--- TODO 2 Solution: LoadBalancer Service ---\n")

lb_svc_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: agent-lb
    spec:
      type: LoadBalancer
      selector:
        app: agent
      ports:
      - port: 80
        targetPort: 8000
""")

with open(os.path.join(WORKDIR, "agent-loadbalancer.yaml"), "w") as f:
    f.write(lb_svc_yaml)

lb_checks = validate_service(lb_svc_yaml) + [("Type is LoadBalancer", "LoadBalancer" in lb_svc_yaml)]
lb_passed = sum(1 for _, ok in lb_checks if ok)
print(f"  LoadBalancer Service validation ({lb_passed}/{len(lb_checks)}):")
for name, ok in lb_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  LoadBalancer features:")
print("    - port: 80 (what users access)")
print("    - targetPort: 8000 (what the container listens on)")
print("    - On AWS: creates an ELB/ALB automatically")
print("    - On GCP: creates a Google Cloud Load Balancer")
print("    - On minikube: use 'minikube service agent-lb' to get URL")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 04 Solution complete!")
print("- TODO 1: Redis ClusterIP Service (redis-svc:6379)")
print("- TODO 2: Agent LoadBalancer Service (port 80 → 8000)")
