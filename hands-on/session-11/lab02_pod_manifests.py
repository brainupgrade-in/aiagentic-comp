"""
Lab 02: Pod Manifests
======================
Create and validate Kubernetes Pod YAML manifests.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-02"

print("=" * 50)
print("  Lab 02: Pod Manifests")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Anatomy of a Pod YAML
# ============================================================

print("\n--- Step 1: Pod YAML Structure ---\n")

print("  Every Kubernetes YAML has 4 top-level fields:\n")
print("    apiVersion  — Which API group (v1, apps/v1, etc.)")
print("    kind        — Resource type (Pod, Deployment, Service...)")
print("    metadata    — Name, labels, annotations")
print("    spec        — The desired state (containers, ports, etc.)\n")

pod_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: Pod
    metadata:
      name: unigps-agent
      labels:
        app: agent
        version: "2.0"
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

with open(os.path.join(WORKDIR, "pod.yaml"), "w") as f:
    f.write(pod_yaml)

print("  Generated: pod.yaml")
for line in pod_yaml.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# Step 2: Understanding Labels
# ============================================================

print("\n\n--- Step 2: Labels — How K8s Finds Resources ---\n")

print("  Labels are key-value pairs attached to resources.")
print("  They're how Services find Pods, and how Deployments manage Pods.\n")

class K8sResource:
    """Simulates K8s label matching."""
    def __init__(self, kind, name, labels):
        self.kind = kind
        self.name = name
        self.labels = labels

    def matches(self, selector):
        """Check if this resource matches a label selector."""
        return all(
            self.labels.get(k) == v
            for k, v in selector.items()
        )

# Create some pods with labels
pods = [
    K8sResource("Pod", "agent-abc12", {"app": "agent", "version": "2.0", "env": "prod"}),
    K8sResource("Pod", "agent-def34", {"app": "agent", "version": "2.0", "env": "prod"}),
    K8sResource("Pod", "agent-ghi56", {"app": "agent", "version": "1.0", "env": "staging"}),
    K8sResource("Pod", "redis-jkl78", {"app": "redis", "role": "cache", "env": "prod"}),
    K8sResource("Pod", "chroma-mno90", {"app": "chromadb", "role": "vectorstore", "env": "prod"}),
]

# Simulate selector matching
selectors = [
    ({"app": "agent"}, "Service: agent-svc (selector: app=agent)"),
    ({"app": "agent", "version": "2.0"}, "Canary: only v2.0 pods"),
    ({"env": "prod"}, "All production pods"),
    ({"app": "redis"}, "Redis pods only"),
]

for selector, description in selectors:
    matches = [p.name for p in pods if p.matches(selector)]
    print(f"  {description}")
    print(f"    Selector: {selector}")
    print(f"    Matches:  {matches}")
    print()


# ============================================================
# Step 3: Pod with multiple containers (sidecar pattern)
# ============================================================

print("\n--- Step 3: Multi-Container Pod (Sidecar Pattern) ---\n")

sidecar_pod = textwrap.dedent("""\
    apiVersion: v1
    kind: Pod
    metadata:
      name: agent-with-logging
      labels:
        app: agent
    spec:
      containers:
      # Main application container
      - name: agent
        image: unigps-agent:2.0
        ports:
        - containerPort: 8000
        volumeMounts:
        - name: logs
          mountPath: /app/logs

      # Sidecar: log collector
      - name: log-collector
        image: fluent/fluent-bit:latest
        volumeMounts:
        - name: logs
          mountPath: /var/log/app

      # Shared volume between containers
      volumes:
      - name: logs
        emptyDir: {}
""")

with open(os.path.join(WORKDIR, "pod-sidecar.yaml"), "w") as f:
    f.write(sidecar_pod)

print("  Sidecar pattern: two containers share a volume in one Pod.")
print("  - agent: writes logs to /app/logs")
print("  - log-collector: reads logs from /var/log/app (same volume)")
print("  - Both containers share the same network (localhost)")
print()
print("  Generated: pod-sidecar.yaml")


# ============================================================
# Step 4: Pod YAML validator
# ============================================================

print("\n\n--- Step 4: Pod YAML Validator ---\n")

def validate_pod_yaml(content: str) -> list:
    """Validate a Pod YAML manifest for correctness."""
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

# Validate our pod.yaml
results = validate_pod_yaml(pod_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"  Validating pod.yaml ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 1: Create a Pod manifest for Redis
# ============================================================

print("\n\n--- TODO 1: Create a Redis Pod Manifest ---\n")

print("  Create a Pod YAML for Redis with these requirements:")
print("    - name: redis")
print("    - image: redis:7-alpine")
print("    - containerPort: 6379")
print("    - labels: app=redis, role=cache")
print("    - Resource requests: memory=64Mi, cpu=100m")
print("    - Resource limits: memory=128Mi, cpu=200m\n")

# YOUR CODE HERE: Write the Redis Pod YAML
redis_pod_yaml = textwrap.dedent("""\
    # TODO: Create a Pod YAML for Redis
    # Requirements:
    #   apiVersion: v1
    #   kind: Pod
    #   name: redis
    #   image: redis:7-alpine
    #   containerPort: 6379
    #   labels: app=redis, role=cache
    #   resources: requests (64Mi/100m), limits (128Mi/200m)

""")

with open(os.path.join(WORKDIR, "redis-pod.yaml"), "w") as f:
    f.write(redis_pod_yaml)

# Validate
results = validate_pod_yaml(redis_pod_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"  Validating your Redis pod ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

if passed < 5:
    print("\n  Hint: Start with the pod.yaml template and change:")
    print("    - metadata.name → redis")
    print("    - labels → app: redis, role: cache")
    print("    - image → redis:7-alpine")
    print("    - containerPort → 6379")


# ============================================================
# TODO 2: Fix a broken Pod manifest
# ============================================================

print("\n\n--- TODO 2: Fix the Broken Pod Manifest ---\n")

print("  This Pod YAML has 5 problems. Find and fix them.\n")

broken_pod = textwrap.dedent("""\
    apiversion: v1
    kind: pod
    metadata:
      app: chromadb
    spec:
      container:
      - name: chromadb
        image: chromadb/chroma
        port:
        - containerport: 8000
        resources:
          requests:
            memory: "512Mi"
""")

with open(os.path.join(WORKDIR, "broken-pod.yaml"), "w") as f:
    f.write(broken_pod)

print("  The 5 problems:")
print("    1. apiversion should be __________ (hint: camelCase)")
print("    2. kind: pod should be __________ (hint: capitalized)")
print("    3. metadata needs a 'name' field and 'labels' section")
print("    4. 'container' should be __________ (hint: plural)")
print("    5. 'port' and 'containerport' should be __________ (hint: camelCase)\n")

# YOUR CODE HERE: Write the fixed version
fixed_pod = textwrap.dedent("""\
    # TODO: Fix all 5 problems in the broken Pod manifest above
    # Write the corrected YAML here

""")

with open(os.path.join(WORKDIR, "fixed-pod.yaml"), "w") as f:
    f.write(fixed_pod)

# Validate the fix
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


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 02 Summary ---\n")
print("  Key concepts:")
print("    1. Pod YAML: apiVersion, kind, metadata, spec")
print("    2. Labels: key-value pairs for selection and organization")
print("    3. Sidecar pattern: multiple containers sharing volumes")
print("    4. Resource requests/limits: tell K8s what your pod needs")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<30} ({size} bytes)")
