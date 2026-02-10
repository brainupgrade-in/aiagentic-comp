"""
Lab 02 Solution: Pod Manifests
================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-02"

print("=" * 50)
print("  Lab 02 Solution: Pod Manifests")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: Redis Pod Manifest
# ============================================================

print("\n--- TODO 1 Solution: Redis Pod ---\n")

redis_pod_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: Pod
    metadata:
      name: redis
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

with open(os.path.join(WORKDIR, "redis-pod.yaml"), "w") as f:
    f.write(redis_pod_yaml)

def validate_pod_yaml(content: str) -> list:
    checks = []
    checks.append(("Has apiVersion", "apiVersion:" in content))
    checks.append(("Has kind: Pod", "kind: Pod" in content))
    checks.append(("Has metadata.name", "name:" in content and "metadata:" in content))
    checks.append(("Has spec.containers", "containers:" in content and "spec:" in content))
    checks.append(("Has container image", "image:" in content))
    checks.append(("Has containerPort", "containerPort:" in content))
    checks.append(("Has labels", "labels:" in content))
    checks.append(("Has resource requests", "requests:" in content))
    checks.append(("Has resource limits", "limits:" in content))
    return checks

results = validate_pod_yaml(redis_pod_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"  Redis Pod validation ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Redis Pod features:")
print("    - image: redis:7-alpine (small, production-ready)")
print("    - containerPort: 6379 (Redis default)")
print("    - labels: app=redis, role=cache (for Service selection)")
print("    - resources: small footprint (64Mi request, 128Mi limit)")


# ============================================================
# TODO 2 Solution: Fix Broken Pod
# ============================================================

print("\n\n--- TODO 2 Solution: Fixed Pod ---\n")

print("  The 5 problems and fixes:\n")
print("    1. apiversion → apiVersion (camelCase)")
print("    2. kind: pod → kind: Pod (capitalized)")
print("    3. metadata needs 'name:' field + 'labels:' section")
print("    4. container → containers (plural)")
print("    5. port/containerport → ports/containerPort (camelCase)\n")

fixed_pod = textwrap.dedent("""\
    apiVersion: v1
    kind: Pod
    metadata:
      name: chromadb
      labels:
        app: chromadb
    spec:
      containers:
      - name: chromadb
        image: chromadb/chroma
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "512Mi"
""")

with open(os.path.join(WORKDIR, "fixed-pod.yaml"), "w") as f:
    f.write(fixed_pod)

fix_checks = [
    ("apiVersion (camelCase)", "apiVersion:" in fixed_pod),
    ("kind: Pod (capitalized)", "kind: Pod" in fixed_pod),
    ("metadata.name present", "name:" in fixed_pod and "metadata:" in fixed_pod),
    ("containers (plural)", "containers:" in fixed_pod),
    ("containerPort (camelCase)", "containerPort:" in fixed_pod),
]

fix_passed = sum(1 for _, ok in fix_checks if ok)
print(f"  Fix validation ({fix_passed}/{len(fix_checks)}):")
for name, ok in fix_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 02 Solution complete!")
print(f"- TODO 1: Redis Pod manifest ({passed}/{len(results)} checks)")
print(f"- TODO 2: Fixed broken Pod ({fix_passed}/{len(fix_checks)} fixes)")
