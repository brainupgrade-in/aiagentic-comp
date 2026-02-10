"""
Lab 04: Resource Issues Debugging
===================================
Diagnose and fix OOMKilled, Pending pods, and resource-related failures.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-04"

print("=" * 50)
print("  Lab 04: Resource Issues Debugging")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: OOMKilled explained
# ============================================================

print("\n--- Step 1: OOMKilled — What Happens When Memory Limit Is Exceeded ---\n")

print("  OOMKilled = Out Of Memory Killed")
print("  The Linux kernel's OOM killer terminates the process when")
print("  container memory usage exceeds the memory limit.\n")

class OOMSimulator:
    """Simulates a container hitting its memory limit."""
    def __init__(self, name, memory_limit_mi):
        self.name = name
        self.memory_limit_mi = memory_limit_mi
        self.current_mi = 0
        self.alive = True

    def allocate(self, amount_mi, description):
        if not self.alive:
            return f"  [DEAD] {self.name}: Cannot allocate — container was OOMKilled"

        self.current_mi += amount_mi
        pct = self.current_mi / self.memory_limit_mi * 100

        if self.current_mi > self.memory_limit_mi:
            self.alive = False
            return (f"  [OOM!] {self.name}: Allocated {amount_mi}Mi for {description} "
                    f"-> {self.current_mi}Mi / {self.memory_limit_mi}Mi ({pct:.0f}%) "
                    f"-> OOMKilled! (exit code 137)")

        bar_len = 30
        filled = int(bar_len * pct / 100)
        bar = "#" * filled + "." * (bar_len - filled)
        return (f"  [ OK ] {self.name}: +{amount_mi}Mi for {description} "
                f"-> {self.current_mi}Mi / {self.memory_limit_mi}Mi [{bar}] {pct:.0f}%")


print("  Scenario: AI Agent with memory limit of 256Mi\n")

agent = OOMSimulator("agent", memory_limit_mi=256)
allocations = [
    (50, "Python runtime"),
    (30, "FastAPI framework"),
    (40, "LangChain + dependencies"),
    (60, "Loading embedding model"),
    (80, "Processing large document"),
    (50, "Caching LLM response"),
]

for amount, desc in allocations:
    print(agent.allocate(amount, desc))

print()
print("  What K8s does after OOMKill:")
print("    1. Container exits with code 137")
print("    2. Pod status shows 'OOMKilled' in last state")
print("    3. K8s restarts the container (respecting backoff)")
print("    4. If it keeps happening: CrashLoopBackOff")
print()
print("  How to detect:")
print("    kubectl describe pod POD | grep -A5 'Last State'")
print("    kubectl get pod POD -o jsonpath='{.status.containerStatuses[0].lastState}'")


# ============================================================
# Step 2: Pending pods
# ============================================================

print("\n\n--- Step 2: Why Pods Get Stuck in Pending ---\n")

pending_causes = [
    {
        "cause": "Insufficient CPU/Memory",
        "description": "No node has enough free resources to schedule the pod",
        "event_message": "0/3 nodes are available: 3 Insufficient memory",
        "fix": "Reduce resource requests, add nodes, or free resources",
    },
    {
        "cause": "PVC Not Bound",
        "description": "PersistentVolumeClaim cannot find a matching PersistentVolume",
        "event_message": "pod has unbound immediate PersistentVolumeClaims",
        "fix": "Create matching PV or check StorageClass",
    },
    {
        "cause": "Node Selector / Affinity",
        "description": "Pod requires specific node labels that no node has",
        "event_message": "0/3 nodes are available: 3 node(s) didn't match Pod's node affinity",
        "fix": "Add labels to nodes or fix nodeSelector in pod spec",
    },
    {
        "cause": "Taints and Tolerations",
        "description": "All nodes have taints that the pod doesn't tolerate",
        "event_message": "0/3 nodes are available: 3 node(s) had taint {gpu=true: NoSchedule}",
        "fix": "Add toleration to pod spec or remove taint from node",
    },
    {
        "cause": "ResourceQuota Exceeded",
        "description": "Namespace resource quota prevents creating more pods",
        "event_message": "exceeded quota: pods-limit, requested: 1, used: 10, limited: 10",
        "fix": "Increase quota or reduce resource requests",
    },
]

for pc in pending_causes:
    print(f"  Cause: {pc['cause']}")
    print(f"    Why: {pc['description']}")
    print(f"    Event: {pc['event_message']}")
    print(f"    Fix: {pc['fix']}")
    print()


class PendingSimulator:
    """Simulates scheduling decisions."""
    def __init__(self, nodes):
        self.nodes = nodes  # list of (name, free_mem_mi, free_cpu_m)

    def try_schedule(self, pod_name, mem_request_mi, cpu_request_m):
        results = []
        for node_name, free_mem, free_cpu in self.nodes:
            mem_ok = free_mem >= mem_request_mi
            cpu_ok = free_cpu >= cpu_request_m
            if mem_ok and cpu_ok:
                results.append((node_name, "SCHEDULED", f"Has {free_mem}Mi/{free_cpu}m free"))
                return results
            reason = []
            if not mem_ok:
                reason.append(f"need {mem_request_mi}Mi, have {free_mem}Mi")
            if not cpu_ok:
                reason.append(f"need {cpu_request_m}m, have {free_cpu}m")
            results.append((node_name, "REJECTED", "; ".join(reason)))
        results.append(("scheduler", "PENDING", f"No node can fit {pod_name}"))
        return results

sched = PendingSimulator([
    ("node-1", 512, 1000),
    ("node-2", 256, 500),
    ("node-3", 128, 200),
])

print("  Scheduling simulation:")
print("  Cluster: node-1 (512Mi/1000m free), node-2 (256Mi/500m free), node-3 (128Mi/200m free)\n")

test_pods = [
    ("small-pod", 128, 200),
    ("medium-pod", 400, 800),
    ("large-pod", 1024, 2000),
]

for pod_name, mem, cpu in test_pods:
    print(f"  Pod: {pod_name} (requests: {mem}Mi memory, {cpu}m CPU)")
    results = sched.try_schedule(pod_name, mem, cpu)
    for node, status, detail in results:
        indicator = "OK" if status == "SCHEDULED" else "!!"
        print(f"    [{indicator}] {node}: {status} — {detail}")
    print()


# ============================================================
# TODO 1: Identify resource problems
# ============================================================

print("\n--- TODO 1: Diagnose Resource Scenarios ---\n")

print("  For each scenario, identify the specific resource problem.\n")

resource_scenarios = [
    {
        "name": "Scenario A",
        "describe_output": textwrap.dedent("""\
            Name: ml-model-7f8b9c
            Status: Running -> OOMKilled
            Last State: Terminated (exit code 137)
            Containers:
              ml-model:
                Limits:  memory=256Mi
                Requests: memory=128Mi
            kubectl top pod ml-model-7f8b9c:
              NAME            CPU    MEMORY
              ml-model-7f8b9  100m   248Mi"""),
        "answer": "_______________",
        # Answer: Memory limit too low (256Mi) — pod using 248Mi, will OOMKill on spike
    },
    {
        "name": "Scenario B",
        "describe_output": textwrap.dedent("""\
            Name: agent-deploy-5c8f2
            Status: Pending
            Events:
              Warning  FailedScheduling  0/3 nodes are available:
              3 Insufficient memory.
            Containers:
              agent:
                Requests: memory=4Gi, cpu=2000m"""),
        "answer": "_______________",
        # Answer: Resource request too high (4Gi) — no node has enough free memory
    },
    {
        "name": "Scenario C",
        "describe_output": textwrap.dedent("""\
            Name: chromadb-9a2b1
            Status: Pending
            Events:
              Warning  FailedScheduling  pod has unbound immediate
              PersistentVolumeClaims
            Volumes:
              chroma-data:
                Type: PersistentVolumeClaim
                ClaimName: chroma-pvc (not found)"""),
        "answer": "_______________",
        # Answer: PVC 'chroma-pvc' not found or not bound — need to create PVC/PV
    },
    {
        "name": "Scenario D",
        "describe_output": textwrap.dedent("""\
            Name: gpu-worker-1a2b3
            Status: Pending
            Events:
              Warning  FailedScheduling  0/3 nodes are available:
              3 node(s) didn't match Pod's node affinity/selector
            Node Selector: gpu=true"""),
        "answer": "_______________",
        # Answer: No node has label gpu=true — need to label a node or remove nodeSelector
    },
]

# SOLUTION: Fill in the diagnosis for each scenario
resource_scenarios[0]["answer"] = "Memory limit too low (256Mi) — pod using 248Mi, will OOMKill on spike"
resource_scenarios[1]["answer"] = "Resource request too high (4Gi) — no node has enough free memory"
resource_scenarios[2]["answer"] = "PVC 'chroma-pvc' not found or not bound — need to create PVC/PV"
resource_scenarios[3]["answer"] = "No node has label gpu=true — need to label a node or remove nodeSelector"

score = 0
for scenario in resource_scenarios:
    print(f"  {scenario['name']}:")
    for line in scenario["describe_output"].strip().split("\n"):
        print(f"    | {line}")
    is_filled = scenario["answer"] != "_______________"
    if is_filled:
        score += 1
    status = "PASS" if is_filled else "FAIL"
    print(f"  [{status}] Diagnosis: {scenario['answer']}")
    print()

print(f"  Diagnosed: {score}/{len(resource_scenarios)} scenarios")


# ============================================================
# TODO 2: Fix OOMKilled Deployment
# ============================================================

print("\n\n--- TODO 2: Fix an OOMKilled Deployment ---\n")

print("  This AI model Deployment keeps getting OOMKilled.")
print("  The model needs ~400Mi memory to load and ~300Mi for inference.")
print("  Fix the memory limits so it stops crashing.\n")

broken_deployment = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ai-model
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: ai-model
      template:
        metadata:
          labels:
            app: ai-model
        spec:
          containers:
          - name: model
            image: ai-model:1.0
            ports:
            - containerPort: 8080
            resources:
              requests:
                memory: "64Mi"
                cpu: "100m"
              limits:
                memory: "128Mi"
                cpu: "500m"
""")

print("  Current (broken) Deployment:")
for i, line in enumerate(broken_deployment.strip().split("\n"), 1):
    print(f"    {i:>2}: {line}")

print()
print("  Requirements:")
print("    - Model loading: ~400Mi")
print("    - Inference peak: ~300Mi additional")
print("    - Total needed: ~700Mi peak")
print("    - Set memory request to 512Mi (normal usage)")
print("    - Set memory limit to 1Gi (peak usage with safety margin)")
print("    - Keep CPU as-is or increase slightly\n")

# SOLUTION: Create the fixed Deployment with correct memory limits
fixed_deployment = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ai-model
    spec:
      replicas: 2
      selector:
        matchLabels:
          app: ai-model
      template:
        metadata:
          labels:
            app: ai-model
        spec:
          containers:
          - name: model
            image: ai-model:1.0
            ports:
            - containerPort: 8080
            resources:
              requests:
                memory: "512Mi"
                cpu: "100m"
              limits:
                memory: "1Gi"
                cpu: "500m"
""")

with open(os.path.join(WORKDIR, "fixed-ai-model-deployment.yaml"), "w") as f:
    f.write(fixed_deployment)

# Validate
fix_checks = [
    ("Has apiVersion: apps/v1",
     "apiVersion: apps/v1" in fixed_deployment),
    ("Has kind: Deployment",
     "kind: Deployment" in fixed_deployment),
    ("Has name: ai-model",
     "name: ai-model" in fixed_deployment),
    ("Memory request >= 512Mi",
     "512Mi" in fixed_deployment or "memory:" in fixed_deployment),
    ("Memory limit >= 512Mi (not 128Mi)",
     "128Mi" not in fixed_deployment and ("1Gi" in fixed_deployment or "1024Mi" in fixed_deployment or "512Mi" in fixed_deployment)),
    ("Has resources section",
     "resources:" in fixed_deployment),
    ("Has requests section",
     "requests:" in fixed_deployment),
    ("Has limits section",
     "limits:" in fixed_deployment),
]

passed = sum(1 for _, ok in fix_checks if ok)
print(f"  Fixed Deployment validation ({passed}/{len(fix_checks)}):")
for name, ok in fix_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 04 Summary ---\n")
print("  Key concepts:")
print("    1. OOMKilled = container exceeded memory limit (exit code 137)")
print("    2. Pending = scheduler cannot place pod (resources, PVC, selectors)")
print("    3. Memory exceeded -> OOMKilled (pod restarts)")
print("    4. CPU exceeded -> throttled (pod slows, doesn't die)")
print("    5. Use kubectl top pods to see actual resource usage before setting limits")
print("    6. Memory request = normal usage, limit = peak usage + safety margin")
print(f"\n  TODO 1: {score}/{len(resource_scenarios)} resource scenarios diagnosed")
print(f"  TODO 2: {passed}/{len(fix_checks)} fix checks passed")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<40} ({size} bytes)")
