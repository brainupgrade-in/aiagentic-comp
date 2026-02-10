"""
Lab 06: Resource Management
=============================
Configure resource requests and limits for AI workloads on Kubernetes.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-06"

print("=" * 50)
print("  Lab 06: Resource Management")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Requests vs Limits
# ============================================================

print("\n--- Step 1: Requests vs Limits ---\n")

print("  requests = minimum guaranteed resources")
print("    - Scheduler uses this to PLACE pods on nodes")
print("    - Set to what your app NORMALLY uses")
print()
print("  limits = maximum allowed resources")
print("    - Memory exceeded → OOMKilled (pod restarted)")
print("    - CPU exceeded → throttled (not killed, just slower)")
print()

class Node:
    """Simulates a K8s worker node."""
    def __init__(self, name, memory_mi, cpu_m):
        self.name = name
        self.total_memory_mi = memory_mi
        self.total_cpu_m = cpu_m
        self.allocated_memory_mi = 0
        self.allocated_cpu_m = 0
        self.pods = []

    @property
    def available_memory_mi(self):
        return self.total_memory_mi - self.allocated_memory_mi

    @property
    def available_cpu_m(self):
        return self.total_cpu_m - self.allocated_cpu_m

    def can_schedule(self, memory_request_mi, cpu_request_m):
        return (self.available_memory_mi >= memory_request_mi
                and self.available_cpu_m >= cpu_request_m)

    def schedule(self, pod_name, memory_request_mi, cpu_request_m):
        if not self.can_schedule(memory_request_mi, cpu_request_m):
            return False
        self.allocated_memory_mi += memory_request_mi
        self.allocated_cpu_m += cpu_request_m
        self.pods.append(pod_name)
        return True


class Scheduler:
    """Simulates the K8s scheduler."""
    def __init__(self, nodes):
        self.nodes = nodes
        self.pending = []

    def schedule_pod(self, pod_name, memory_request_mi, cpu_request_m):
        for node in self.nodes:
            if node.schedule(pod_name, memory_request_mi, cpu_request_m):
                return f"Scheduled {pod_name} on {node.name} " \
                       f"(remaining: {node.available_memory_mi}Mi memory, {node.available_cpu_m}m CPU)"
        self.pending.append(pod_name)
        return f"PENDING: {pod_name} — no node has enough resources!"


# Create a 2-node cluster
nodes = [
    Node("node-1", memory_mi=2048, cpu_m=2000),
    Node("node-2", memory_mi=2048, cpu_m=2000),
]
scheduler = Scheduler(nodes)

# Schedule AI workloads
workloads = [
    ("agent-1", 512, 500),
    ("agent-2", 512, 500),
    ("agent-3", 512, 500),
    ("chromadb", 1024, 500),
    ("redis", 128, 100),
    ("agent-4", 512, 500),
    ("embedding-model", 2048, 1000),  # Won't fit!
]

print("  Cluster: 2 nodes × 2048Mi memory × 2000m CPU\n")
print("  Scheduling AI workloads:\n")
for name, mem, cpu in workloads:
    result = scheduler.schedule_pod(name, mem, cpu)
    print(f"    {result}")

if scheduler.pending:
    print(f"\n  Pending pods: {scheduler.pending}")
    print("  → These pods wait until a node has enough resources!")


# ============================================================
# Step 2: Resource guidelines for AI components
# ============================================================

print("\n\n--- Step 2: AI Resource Guidelines ---\n")

guidelines = [
    ("FastAPI + LangChain Agent", "256-512 Mi", "1 Gi", "250m", "1000m"),
    ("ChromaDB (vector store)",   "512 Mi-1 Gi", "2 Gi", "500m", "1000m"),
    ("Redis (cache/session)",     "64-128 Mi", "256 Mi", "100m", "200m"),
    ("Embedding model (local)",   "1-4 Gi", "4-8 Gi", "1000m", "4000m"),
    ("LLM API proxy (Groq/OpenAI)", "128-256 Mi", "512 Mi", "250m", "500m"),
]

print(f"  {'Component':<30} {'Mem Request':>12} {'Mem Limit':>10} {'CPU Req':>8} {'CPU Lim':>8}")
print(f"  {'─'*30} {'─'*12} {'─'*10} {'─'*8} {'─'*8}")
for name, mem_req, mem_lim, cpu_req, cpu_lim in guidelines:
    print(f"  {name:<30} {mem_req:>12} {mem_lim:>10} {cpu_req:>8} {cpu_lim:>8}")

print()
print("  Strategy: Start small, monitor with 'kubectl top pods', then adjust.")
print("  Under-requesting wastes node resources (fragmentation).")
print("  Under-limiting risks OOMKills (pod restarts).")


# ============================================================
# Step 3: OOMKill simulation
# ============================================================

print("\n\n--- Step 3: OOMKill vs CPU Throttling ---\n")

class PodRuntime:
    """Simulates pod resource usage."""
    def __init__(self, name, memory_limit_mi, cpu_limit_m):
        self.name = name
        self.memory_limit_mi = memory_limit_mi
        self.cpu_limit_m = cpu_limit_m

    def use_memory(self, current_mi, label=""):
        if current_mi > self.memory_limit_mi:
            return f"  OOMKilled! {self.name} used {current_mi}Mi > limit {self.memory_limit_mi}Mi ({label})"
        pct = current_mi / self.memory_limit_mi * 100
        return f"  OK: {self.name} using {current_mi}Mi / {self.memory_limit_mi}Mi ({pct:.0f}%) ({label})"

    def use_cpu(self, current_m, label=""):
        if current_m > self.cpu_limit_m:
            throttled = current_m - self.cpu_limit_m
            return f"  Throttled: {self.name} wants {current_m}m, capped at {self.cpu_limit_m}m (-{throttled}m) ({label})"
        pct = current_m / self.cpu_limit_m * 100
        return f"  OK: {self.name} using {current_m}m / {self.cpu_limit_m}m ({pct:.0f}%) ({label})"

agent = PodRuntime("agent", memory_limit_mi=512, cpu_limit_m=1000)

print("  Memory scenarios (limit: 512Mi):")
print(agent.use_memory(256, "normal load"))
print(agent.use_memory(480, "large LLM response processing"))
print(agent.use_memory(600, "loading embeddings into memory"))
print()
print("  CPU scenarios (limit: 1000m):")
print(agent.use_cpu(300, "normal API request"))
print(agent.use_cpu(900, "embedding computation"))
print(agent.use_cpu(1500, "batch processing spike"))
print()
print("  Memory exceeded = OOMKilled (pod RESTARTS)")
print("  CPU exceeded = throttled (pod SLOWS DOWN but stays alive)")


# ============================================================
# Step 4: Resource YAML patterns
# ============================================================

print("\n\n--- Step 4: Resource YAML Patterns ---\n")

resource_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: unigps-agent
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
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "1000m"
""")

with open(os.path.join(WORKDIR, "deployment-resources.yaml"), "w") as f:
    f.write(resource_yaml)

print("  CPU units:")
print("    1000m = 1 CPU core")
print("    500m  = 0.5 CPU core")
print("    250m  = 0.25 CPU core (quarter core)")
print()
print("  Memory units:")
print("    Mi = Mebibytes (1 Mi = 1,048,576 bytes)")
print("    Gi = Gibibytes (1 Gi = 1,073,741,824 bytes)")
print("    256Mi ≈ 268 MB,  1Gi ≈ 1.07 GB")
print()
print("  Generated: deployment-resources.yaml")


# ============================================================
# TODO 1: Set resources for a complete AI stack
# ============================================================

print("\n\n--- TODO 1: Resource Configuration for AI Stack ---\n")

print("  Configure resources for ALL components of the AI stack.")
print("  Use the guidelines from Step 2.\n")

# YOUR CODE HERE: Create deployments with appropriate resources
agent_resources = textwrap.dedent("""\
    # TODO: Create agent Deployment with resources
    # Hint:
    #   requests: memory=256Mi, cpu=250m
    #   limits:   memory=1Gi, cpu=1000m

""")

redis_resources = textwrap.dedent("""\
    # TODO: Create redis Deployment with resources
    # Hint:
    #   requests: memory=64Mi, cpu=100m
    #   limits:   memory=128Mi, cpu=200m

""")

chromadb_resources = textwrap.dedent("""\
    # TODO: Create chromadb Deployment with resources
    # Hint:
    #   requests: memory=512Mi, cpu=500m
    #   limits:   memory=2Gi, cpu=1000m

""")

for name, content in [("agent", agent_resources), ("redis", redis_resources), ("chromadb", chromadb_resources)]:
    filepath = os.path.join(WORKDIR, f"{name}-deployment.yaml")
    with open(filepath, "w") as f:
        f.write(content)

    has_requests = "requests:" in content
    has_limits = "limits:" in content
    has_memory = "memory:" in content
    has_cpu = "cpu:" in content
    checks = [has_requests, has_limits, has_memory, has_cpu]
    passed = sum(checks)
    print(f"  {name}: {passed}/4 resource checks passed")


# ============================================================
# TODO 2: Calculate total cluster resources needed
# ============================================================

print("\n\n--- TODO 2: Cluster Capacity Calculator ---\n")

print("  Given the AI stack below, calculate total resource needs.\n")

stack = [
    {"name": "agent", "replicas": 3, "mem_request_mi": 256, "cpu_request_m": 250},
    {"name": "redis", "replicas": 1, "mem_request_mi": 64, "cpu_request_m": 100},
    {"name": "chromadb", "replicas": 1, "mem_request_mi": 512, "cpu_request_m": 500},
]

# YOUR CODE HERE: Calculate totals
# total_memory_mi = sum of (replicas * mem_request_mi) for all components
# total_cpu_m = sum of (replicas * cpu_request_m) for all components

total_memory_mi = 0  # TODO: Calculate
total_cpu_m = 0      # TODO: Calculate

# Hint: the answer should be:
# Memory: 3*256 + 1*64 + 1*512 = 1344 Mi
# CPU:    3*250 + 1*100 + 1*500 = 1350m

print("  Stack:")
for comp in stack:
    print(f"    {comp['name']:>10}: {comp['replicas']} replicas × "
          f"{comp['mem_request_mi']}Mi mem, {comp['cpu_request_m']}m CPU")
print()
print(f"  Your calculated totals:")
print(f"    Total memory requests: {total_memory_mi} Mi")
print(f"    Total CPU requests:    {total_cpu_m}m")
print()

expected_mem = 3*256 + 1*64 + 1*512
expected_cpu = 3*250 + 1*100 + 1*500
mem_correct = total_memory_mi == expected_mem
cpu_correct = total_cpu_m == expected_cpu

print(f"    [{'PASS' if mem_correct else 'TODO'}] Memory total (expected: {expected_mem} Mi)")
print(f"    [{'PASS' if cpu_correct else 'TODO'}] CPU total (expected: {expected_cpu}m)")

if mem_correct and cpu_correct:
    print(f"\n    A node with 2 Gi memory + 2000m CPU can fit this stack.")
    print(f"    For HA, use 2+ nodes with at least 1 Gi memory each.")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 06 Summary ---\n")
print("  Key concepts:")
print("    1. requests = guaranteed minimum (scheduler uses this)")
print("    2. limits = maximum allowed (OOMKill or throttle)")
print("    3. Memory exceeded → OOMKilled (pod restarts)")
print("    4. CPU exceeded → throttled (pod slows down)")
print("    5. CPU: 1000m = 1 core; Memory: 1Gi ≈ 1.07 GB")
print("    6. Start small, monitor, adjust — don't guess")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<35} ({size} bytes)")
