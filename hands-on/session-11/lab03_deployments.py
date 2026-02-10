"""
Lab 03: Deployments
====================
Create Kubernetes Deployments that manage pod replicas, rolling updates,
and self-healing.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-03"

print("=" * 50)
print("  Lab 03: Deployments")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Why Deployments, not bare Pods?
# ============================================================

print("\n--- Step 1: Why Deployments? ---\n")

class BarePod:
    """Bare Pod: no self-healing."""
    def __init__(self, name):
        self.name = name
        self.status = "Running"

    def crash(self):
        self.status = "Failed"
        return f"Pod {self.name} crashed. Status: {self.status}. NO automatic restart."

class ManagedPod:
    """Pod managed by a Deployment: self-healing."""
    def __init__(self, name, deployment):
        self.name = name
        self.deployment = deployment
        self.status = "Running"

    def crash(self):
        self.status = "Failed"
        new_pod = self.deployment.reconcile()
        return (f"Pod {self.name} crashed. Deployment detected mismatch: "
                f"desired={self.deployment.replicas}, "
                f"actual={len([p for p in self.deployment.pods if p.status == 'Running'])}. "
                f"Created replacement: {new_pod}")

class Deployment:
    """Simulates a K8s Deployment controller."""
    def __init__(self, name, replicas=3):
        self.name = name
        self.replicas = replicas
        self.pods = []
        self._counter = 0
        for _ in range(replicas):
            self._counter += 1
            pod = ManagedPod(f"{name}-{self._counter:05x}", self)
            self.pods.append(pod)

    def reconcile(self):
        """Control loop: ensure desired == actual."""
        running = [p for p in self.pods if p.status == "Running"]
        while len(running) < self.replicas:
            self._counter += 1
            new_pod = ManagedPod(f"{self.name}-{self._counter:05x}", self)
            self.pods.append(new_pod)
            running.append(new_pod)
            return new_pod.name
        return None

# Demo: bare pod crash
bare = BarePod("agent-solo")
print(f"  Bare Pod:   {bare.crash()}")
print()

# Demo: managed pod crash
deploy = Deployment("agent", replicas=3)
print(f"  Deployment: {len(deploy.pods)} pods running")
print(f"  Pods: {[p.name for p in deploy.pods]}")
crash_result = deploy.pods[0].crash()
print(f"  {crash_result}")
print(f"  Pods after self-heal: {[p.name for p in deploy.pods if p.status == 'Running']}")


# ============================================================
# Step 2: Deployment YAML
# ============================================================

print("\n\n--- Step 2: Deployment YAML ---\n")

deployment_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: unigps-agent
      labels:
        app: agent
    spec:
      replicas: 3
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

with open(os.path.join(WORKDIR, "deployment.yaml"), "w") as f:
    f.write(deployment_yaml)

print("  Key Deployment fields:")
print()
print("    spec.replicas        — How many identical pods to run")
print("    spec.selector        — How the Deployment finds its pods (label match)")
print("    spec.template        — Pod template (what each pod looks like)")
print("    template.metadata.labels — MUST match spec.selector.matchLabels")
print()
print("  Generated: deployment.yaml")


# ============================================================
# Step 3: Label selector matching
# ============================================================

print("\n\n--- Step 3: Selector Must Match Template Labels ---\n")

print("  The Deployment's selector.matchLabels MUST match template.metadata.labels.")
print("  This is how the Deployment knows which pods belong to it.\n")

def check_selector_match(yaml_content):
    """Check if selector matches template labels (simplified)."""
    lines = yaml_content.split("\n")

    selector_labels = {}
    template_labels = {}
    in_match_labels = False
    in_template_labels = False
    template_count = 0

    for line in lines:
        stripped = line.strip()
        if "matchLabels:" in stripped:
            in_match_labels = True
            in_template_labels = False
            continue
        if "template:" in stripped:
            template_count += 1
            continue
        if template_count == 1 and "labels:" in stripped and "metadata:" not in stripped:
            in_template_labels = True
            in_match_labels = False
            continue

        if in_match_labels and ":" in stripped and not stripped.startswith("#"):
            if stripped.startswith("-") or stripped.startswith("spec") or stripped.startswith("template"):
                in_match_labels = False
                continue
            key, val = stripped.split(":", 1)
            selector_labels[key.strip()] = val.strip().strip('"')

        if in_template_labels and ":" in stripped and not stripped.startswith("#"):
            if stripped.startswith("-") or stripped.startswith("spec") or stripped.startswith("containers"):
                in_template_labels = False
                continue
            key, val = stripped.split(":", 1)
            template_labels[key.strip()] = val.strip().strip('"')

    return selector_labels, template_labels, selector_labels == template_labels

sel, tmpl, match = check_selector_match(deployment_yaml)
print(f"  selector.matchLabels:    {sel}")
print(f"  template.metadata.labels: {tmpl}")
print(f"  Match: {'YES — Deployment will find its pods' if match else 'NO — Deployment cannot manage pods!'}")


# ============================================================
# Step 4: Rolling Updates simulation
# ============================================================

print("\n\n--- Step 4: Rolling Update Simulation ---\n")

class RollingUpdateSim:
    """Simulates a K8s rolling update."""
    def __init__(self, replicas, old_version, new_version):
        self.replicas = replicas
        self.old_version = old_version
        self.new_version = new_version

    def simulate(self):
        steps = []
        old_count = self.replicas
        new_count = 0

        steps.append(f"  Start: {old_count}x v{self.old_version}, {new_count}x v{self.new_version}")

        for i in range(self.replicas):
            # K8s creates a new pod, then terminates an old one
            new_count += 1
            steps.append(f"  Step {i*2+1}: Create v{self.new_version} pod "
                         f"→ {old_count}x old + {new_count}x new = {old_count + new_count} total")
            old_count -= 1
            steps.append(f"  Step {i*2+2}: Terminate v{self.old_version} pod "
                         f"→ {old_count}x old + {new_count}x new = {old_count + new_count} total")

        steps.append(f"  Done: {new_count}x v{self.new_version} (zero downtime)")
        return steps

sim = RollingUpdateSim(3, "1.0", "2.0")
for step in sim.simulate():
    print(step)

print()
print("  Key: At every step, at least 'replicas' pods are available.")
print("  Users experience zero downtime during the update.")


# ============================================================
# Step 5: Deployment YAML Validator
# ============================================================

print("\n\n--- Step 5: Deployment Validator ---\n")

def validate_deployment(content: str) -> list:
    """Validate a Deployment YAML for correctness and best practices."""
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

results = validate_deployment(deployment_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"  Validating deployment.yaml ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 1: Create a Redis Deployment
# ============================================================

print("\n\n--- TODO 1: Create a Redis Deployment ---\n")

print("  Create a Deployment YAML for Redis with these requirements:")
print("    - name: redis")
print("    - replicas: 1 (Redis is stateful, 1 replica for now)")
print("    - image: redis:7-alpine")
print("    - containerPort: 6379")
print("    - labels: app=redis, role=cache")
print("    - Resources: requests (64Mi/100m), limits (128Mi/200m)\n")

# YOUR CODE HERE: Write the Redis Deployment YAML
redis_deployment = textwrap.dedent("""\
    # TODO: Create a Redis Deployment YAML
    # Remember:
    #   - apiVersion: apps/v1
    #   - kind: Deployment
    #   - selector.matchLabels MUST match template.metadata.labels
    #   - replicas: 1

""")

with open(os.path.join(WORKDIR, "redis-deployment.yaml"), "w") as f:
    f.write(redis_deployment)

results = validate_deployment(redis_deployment)
passed = sum(1 for _, ok in results if ok)
print(f"  Validating your Redis Deployment ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Add rolling update strategy
# ============================================================

print("\n\n--- TODO 2: Add Rolling Update Strategy ---\n")

print("  Add a strategy section to control how rolling updates work.")
print("  Requirements:")
print("    - strategy type: RollingUpdate")
print("    - maxSurge: 1 (at most 1 extra pod during update)")
print("    - maxUnavailable: 0 (never have fewer than replicas pods)\n")

# YOUR CODE HERE: Add strategy to the agent deployment
agent_with_strategy = textwrap.dedent("""\
    # TODO: Copy the deployment.yaml from Step 2 and add:
    #
    #   strategy:
    #     type: RollingUpdate
    #     rollingUpdate:
    #       maxSurge: 1
    #       maxUnavailable: 0
    #
    # This goes under spec: (same level as replicas:)

""")

with open(os.path.join(WORKDIR, "deployment-with-strategy.yaml"), "w") as f:
    f.write(agent_with_strategy)

strategy_checks = [
    ("Has strategy section", "strategy:" in agent_with_strategy),
    ("Type is RollingUpdate", "RollingUpdate" in agent_with_strategy),
    ("Has maxSurge", "maxSurge:" in agent_with_strategy),
    ("Has maxUnavailable", "maxUnavailable:" in agent_with_strategy),
]

strategy_passed = sum(1 for _, ok in strategy_checks if ok)
all_checks = validate_deployment(agent_with_strategy) + strategy_checks
all_passed = sum(1 for _, ok in all_checks if ok)

print(f"  Validating deployment with strategy ({all_passed}/{len(all_checks)}):")
for name, ok in all_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 03 Summary ---\n")
print("  Key concepts:")
print("    1. Deployments manage pods — bare pods don't self-heal")
print("    2. selector.matchLabels MUST match template.metadata.labels")
print("    3. Rolling updates: gradual replacement, zero downtime")
print("    4. Strategy: maxSurge (extra pods) and maxUnavailable (min available)")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<40} ({size} bytes)")
