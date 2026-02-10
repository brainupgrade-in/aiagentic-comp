"""
Lab 04: Services
=================
Create Kubernetes Services for stable networking and load balancing.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap
import random

WORKDIR = "/tmp/k8s-lab-04"

print("=" * 50)
print("  Lab 04: Services")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Why Services? The ephemeral IP problem
# ============================================================

print("\n--- Step 1: The Ephemeral IP Problem ---\n")

class Pod:
    """Simulates a K8s pod with a random IP."""
    def __init__(self, name, labels):
        self.name = name
        self.labels = labels
        self.ip = f"10.244.{random.randint(1,5)}.{random.randint(1,254)}"
        self.status = "Running"

    def restart(self):
        old_ip = self.ip
        self.ip = f"10.244.{random.randint(1,5)}.{random.randint(1,254)}"
        return old_ip

# Demo: pods get new IPs on restart
random.seed(42)
agent_pod = Pod("agent-abc12", {"app": "agent"})
print(f"  Pod {agent_pod.name} started with IP: {agent_pod.ip}")

for i in range(3):
    old_ip = agent_pod.restart()
    print(f"  Pod restarted: {old_ip} → {agent_pod.ip}")

print()
print("  Problem: If Redis connects to the agent at 10.244.x.y,")
print("           that IP changes every time the pod restarts!")
print("  Solution: A SERVICE gives a stable DNS name + load balancing.")


# ============================================================
# Step 2: How Services Work (simulation)
# ============================================================

print("\n\n--- Step 2: Service Load Balancing Simulation ---\n")

class Service:
    """Simulates a K8s ClusterIP Service."""
    def __init__(self, name, selector, port, target_port):
        self.name = name
        self.selector = selector
        self.port = port
        self.target_port = target_port
        self.cluster_ip = f"10.96.0.{random.randint(10,250)}"
        self.dns_name = f"{name}.default.svc.cluster.local"

    def find_endpoints(self, all_pods):
        """Find pods matching this service's selector."""
        return [
            p for p in all_pods
            if all(p.labels.get(k) == v for k, v in self.selector.items())
            and p.status == "Running"
        ]

    def route_request(self, all_pods):
        """Route a request to one of the matching pods (round-robin)."""
        endpoints = self.find_endpoints(all_pods)
        if not endpoints:
            return "No endpoints available!"
        chosen = random.choice(endpoints)
        return f"{chosen.name} ({chosen.ip}:{self.target_port})"

# Create pods
pods = [
    Pod("agent-abc12", {"app": "agent", "version": "2.0"}),
    Pod("agent-def34", {"app": "agent", "version": "2.0"}),
    Pod("agent-ghi56", {"app": "agent", "version": "2.0"}),
    Pod("redis-jkl78", {"app": "redis"}),
]

# Create service
agent_svc = Service("agent-svc", {"app": "agent"}, 8000, 8000)

print(f"  Service: {agent_svc.name}")
print(f"  ClusterIP: {agent_svc.cluster_ip}")
print(f"  DNS: {agent_svc.dns_name}")
print(f"  Selector: {agent_svc.selector}")
print(f"  Endpoints: {[p.name for p in agent_svc.find_endpoints(pods)]}")
print()

print("  Simulating 6 requests to agent-svc:8000:")
for i in range(6):
    target = agent_svc.route_request(pods)
    print(f"    Request {i+1} → {target}")

print()
print("  The Service provides:")
print("    - Stable DNS name (agent-svc) that never changes")
print("    - Load balancing across all matching pods")
print("    - Automatic endpoint updates when pods come/go")


# ============================================================
# Step 3: Service Types
# ============================================================

print("\n\n--- Step 3: Service Types ---\n")

service_types = [
    {
        "type": "ClusterIP",
        "scope": "Internal only (default)",
        "use_case": "Agent ↔ Redis, Agent ↔ ChromaDB",
        "access": "Only from within the cluster",
    },
    {
        "type": "NodePort",
        "scope": "External via node IP:port (30000-32767)",
        "use_case": "Quick testing, development access",
        "access": "http://<node-ip>:<node-port>",
    },
    {
        "type": "LoadBalancer",
        "scope": "External via cloud load balancer",
        "use_case": "Production API on AWS/GCP/Azure",
        "access": "http://<external-ip>:<port>",
    },
]

for svc_type in service_types:
    print(f"  {svc_type['type']}")
    print(f"    Scope:   {svc_type['scope']}")
    print(f"    Use:     {svc_type['use_case']}")
    print(f"    Access:  {svc_type['access']}")
    print()


# ============================================================
# Step 4: Service YAML examples
# ============================================================

print("\n--- Step 4: Service YAML Examples ---\n")

clusterip_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: agent-svc
    spec:
      type: ClusterIP
      selector:
        app: agent
      ports:
      - port: 8000
        targetPort: 8000
""")

nodeport_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: agent-nodeport
    spec:
      type: NodePort
      selector:
        app: agent
      ports:
      - port: 8000
        targetPort: 8000
        nodePort: 30080
""")

with open(os.path.join(WORKDIR, "service-clusterip.yaml"), "w") as f:
    f.write(clusterip_yaml)
with open(os.path.join(WORKDIR, "service-nodeport.yaml"), "w") as f:
    f.write(nodeport_yaml)

print("  ClusterIP Service (internal):")
for line in clusterip_yaml.strip().split("\n"):
    print(f"    {line}")

print()
print("  NodePort Service (external dev access):")
for line in nodeport_yaml.strip().split("\n"):
    print(f"    {line}")

print()
print("  Generated: service-clusterip.yaml, service-nodeport.yaml")


# ============================================================
# Step 5: Service Validator
# ============================================================

print("\n\n--- Step 5: Service Validator ---\n")

def validate_service(content: str) -> list:
    """Validate a Service YAML manifest."""
    checks = []

    checks.append(("Has apiVersion: v1", "apiVersion: v1" in content))
    checks.append(("Has kind: Service", "kind: Service" in content))
    checks.append(("Has metadata.name", "metadata:" in content and "name:" in content))
    checks.append(("Has spec.selector", "selector:" in content))
    checks.append(("Has spec.ports", "ports:" in content))
    checks.append(("Has port defined", "port:" in content))
    checks.append(("Has targetPort defined", "targetPort:" in content))

    return checks

results = validate_service(clusterip_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"  Validating ClusterIP Service ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 1: Create a Redis ClusterIP Service
# ============================================================

print("\n\n--- TODO 1: Create a Redis Service ---\n")

print("  Create a ClusterIP Service for Redis:")
print("    - name: redis-svc")
print("    - type: ClusterIP")
print("    - selector: app=redis")
print("    - port: 6379 → targetPort: 6379")
print("  After creation, the agent connects to: redis-svc:6379\n")

# YOUR CODE HERE: Write the Redis Service YAML
redis_svc_yaml = textwrap.dedent("""\
    # TODO: Create a ClusterIP Service for Redis
    # This allows the agent to connect via: redis-svc:6379
    # instead of hardcoding a pod IP

""")

with open(os.path.join(WORKDIR, "redis-service.yaml"), "w") as f:
    f.write(redis_svc_yaml)

results = validate_service(redis_svc_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"  Validating your Redis Service ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Create a LoadBalancer Service for production
# ============================================================

print("\n\n--- TODO 2: Create a LoadBalancer Service ---\n")

print("  Create a LoadBalancer Service to expose the agent externally:")
print("    - name: agent-lb")
print("    - type: LoadBalancer")
print("    - selector: app=agent")
print("    - port: 80 → targetPort: 8000")
print("  On AWS/GCP/Azure, this creates an actual cloud load balancer.\n")

# YOUR CODE HERE: Write the LoadBalancer Service YAML
lb_svc_yaml = textwrap.dedent("""\
    # TODO: Create a LoadBalancer Service
    # This exposes the agent to the internet via a cloud load balancer
    # Note: port 80 (external) maps to targetPort 8000 (container)

""")

with open(os.path.join(WORKDIR, "agent-loadbalancer.yaml"), "w") as f:
    f.write(lb_svc_yaml)

lb_checks = validate_service(lb_svc_yaml)
lb_extra = [("Type is LoadBalancer", "LoadBalancer" in lb_svc_yaml)]
all_checks = lb_checks + lb_extra
all_passed = sum(1 for _, ok in all_checks if ok)

print(f"  Validating your LoadBalancer Service ({all_passed}/{len(all_checks)}):")
for name, ok in all_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 04 Summary ---\n")
print("  Key concepts:")
print("    1. Pods get new IPs on restart — don't hardcode IPs")
print("    2. Services provide stable DNS + load balancing")
print("    3. ClusterIP: internal only (default, use for inter-service)")
print("    4. NodePort: external via node port (dev/testing)")
print("    5. LoadBalancer: external via cloud LB (production)")
print("    6. selector matches pod labels to route traffic")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<35} ({size} bytes)")
