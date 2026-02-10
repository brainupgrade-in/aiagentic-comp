"""
Lab 01: Kubernetes Concepts
============================
Understand Kubernetes architecture through code analogies and comparisons.

No Kubernetes cluster required — this lab teaches concepts via Python.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-01"

print("=" * 50)
print("  Lab 01: Kubernetes Concepts")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Docker Compose vs Kubernetes — Code Analogy
# ============================================================

print("\n--- Step 1: Docker Compose vs Kubernetes ---\n")

class DockerComposePlatform:
    """Docker Compose: single machine, basic restart."""
    def __init__(self):
        self.name = "Docker Compose"
        self.hosts = 1
        self.self_healing = "restart policy only"
        self.scaling = "manual (--scale N)"
        self.updates = "stop-then-start (downtime)"
        self.service_discovery = "container names on shared network"
        self.config_management = ".env files"

class KubernetesPlatform:
    """Kubernetes: cluster of machines, full orchestration."""
    def __init__(self):
        self.name = "Kubernetes"
        self.hosts = "1 to 5000+ nodes"
        self.self_healing = "auto-restart, reschedule to healthy node"
        self.scaling = "auto-scaling (HPA) on CPU/memory/custom metrics"
        self.updates = "rolling updates (zero downtime)"
        self.service_discovery = "DNS + load balancing (Services)"
        self.config_management = "ConfigMaps + Secrets (versioned, injected)"

compose = DockerComposePlatform()
k8s = KubernetesPlatform()

for attr in ["hosts", "self_healing", "scaling", "updates", "service_discovery", "config_management"]:
    print(f"  {attr:>22}: Compose = {getattr(compose, attr)}")
    print(f"  {' ':>22}  K8s    = {getattr(k8s, attr)}")
    print()


# ============================================================
# Step 2: Control Plane Components
# ============================================================

print("\n--- Step 2: K8s Architecture — Control Plane ---\n")

class ControlPlaneComponent:
    def __init__(self, name, role, analogy):
        self.name = name
        self.role = role
        self.analogy = analogy

control_plane = [
    ControlPlaneComponent(
        "API Server (kube-apiserver)",
        "Front door — all requests go through it",
        "Hotel reception desk: every request/check-in goes here first"
    ),
    ControlPlaneComponent(
        "etcd",
        "Key-value store — holds ALL cluster state",
        "Hotel ledger: records every room booking, guest, and event"
    ),
    ControlPlaneComponent(
        "Scheduler (kube-scheduler)",
        "Assigns new pods to worker nodes",
        "Room assignment: finds best available room for each guest"
    ),
    ControlPlaneComponent(
        "Controller Manager",
        "Runs control loops: desired state → actual state",
        "Hotel manager: constantly checks if rooms match bookings"
    ),
]

for comp in control_plane:
    print(f"  {comp.name}")
    print(f"    Role:    {comp.role}")
    print(f"    Analogy: {comp.analogy}")
    print()


# ============================================================
# Step 3: Worker Node Components
# ============================================================

print("\n--- Step 3: K8s Architecture — Worker Nodes ---\n")

worker_components = [
    ControlPlaneComponent(
        "kubelet",
        "Agent on each node — starts/stops pods as told by API Server",
        "Floor manager: makes sure each room is set up per instructions"
    ),
    ControlPlaneComponent(
        "kube-proxy",
        "Network rules — routes traffic to correct pods",
        "Switchboard operator: directs calls to the right rooms"
    ),
    ControlPlaneComponent(
        "Container Runtime (containerd)",
        "Actually runs containers (replaced Docker in K8s 1.24+)",
        "Utility workers: physically set up the room furniture"
    ),
]

for comp in worker_components:
    print(f"  {comp.name}")
    print(f"    Role:    {comp.role}")
    print(f"    Analogy: {comp.analogy}")
    print()

print("  Key insight: You tell the Control Plane WHAT you want.")
print("               Worker Nodes figure out HOW to make it happen.")


# ============================================================
# Step 4: Declarative vs Imperative
# ============================================================

print("\n\n--- Step 4: Declarative vs Imperative ---\n")

imperative_steps = [
    "docker run -d --name agent -p 8000:8000 unigps-agent:2.0",
    "docker run -d --name redis redis:7-alpine",
    "docker network create ai-net",
    "docker network connect ai-net agent",
    "docker network connect ai-net redis",
    "# If agent crashes at 3 AM... manually restart",
    "# If you need 3 copies... run the commands 3 times",
]

declarative_yaml = textwrap.dedent("""\
    # deployment.yaml — Kubernetes declarative model
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: unigps-agent
    spec:
      replicas: 3            # I want 3 copies
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
    # kubectl apply -f deployment.yaml
    # K8s handles: scheduling, restarts, networking, scaling
""")

print("  IMPERATIVE (Docker): You tell it EACH STEP")
for i, step in enumerate(imperative_steps, 1):
    print(f"    {i}. {step}")

print()
print("  DECLARATIVE (Kubernetes): You describe the END STATE")
print()
for line in declarative_yaml.split("\n"):
    print(f"    {line}")

print()
print("  Imperative = recipe (step by step)")
print("  Declarative = order from menu (describe what you want)")


# ============================================================
# Step 5: kubectl commands reference
# ============================================================

print("\n\n--- Step 5: kubectl Command Reference ---\n")

kubectl_cmds = [
    ("kubectl apply -f FILE",     "Create or update resources from YAML"),
    ("kubectl get pods",          "List all pods in current namespace"),
    ("kubectl get deployments",   "List all deployments"),
    ("kubectl get services",      "List all services"),
    ("kubectl describe pod NAME", "Show detailed pod info + events"),
    ("kubectl logs NAME",         "View container stdout/stderr"),
    ("kubectl logs -f NAME",      "Stream logs (like tail -f)"),
    ("kubectl exec -it NAME -- bash", "Open shell inside pod"),
    ("kubectl delete -f FILE",    "Delete resources defined in YAML"),
    ("kubectl scale deployment NAME --replicas=N", "Scale to N pods"),
    ("kubectl top pods",          "Show CPU/memory usage per pod"),
    ("kubectl get all",           "List pods + services + deployments"),
]

for cmd, desc in kubectl_cmds:
    print(f"  {cmd:<48} — {desc}")


# ============================================================
# TODO 1: Map Docker commands to kubectl equivalents
# ============================================================

print("\n\n--- TODO 1: Docker-to-Kubernetes Command Mapping ---\n")

print("  Map each Docker command to its kubectl equivalent.\n")

docker_commands = {
    "docker ps":             "_______________",  # kubectl get pods
    "docker logs CONTAINER": "_______________",  # kubectl logs POD
    "docker exec -it CONTAINER bash": "_______________",  # kubectl exec -it POD -- bash
    "docker stop CONTAINER": "_______________",  # kubectl delete pod POD
    "docker-compose up -d":  "_______________",  # kubectl apply -f .
    "docker inspect CONTAINER": "_______________",  # kubectl describe pod POD
}

# YOUR CODE HERE: Replace the blank values with kubectl commands
# Hint: Look at the reference table above

# Example (already done for you):
docker_commands["docker ps"] = "kubectl get pods"

# TODO: Fill in the rest (5 mappings)
# docker_commands["docker logs CONTAINER"] = ???
# docker_commands["docker exec -it CONTAINER bash"] = ???
# docker_commands["docker stop CONTAINER"] = ???
# docker_commands["docker-compose up -d"] = ???
# docker_commands["docker inspect CONTAINER"] = ???


# Validate
print("  Your mappings:")
filled = 0
for docker, k8s in docker_commands.items():
    is_filled = k8s != "_______________"
    if is_filled:
        filled += 1
    status = "DONE" if is_filled else "TODO"
    print(f"    [{status}] {docker:<40} → {k8s}")

print(f"\n  Completed: {filled}/{len(docker_commands)} mappings")


# ============================================================
# TODO 2: Identify K8s architecture components
# ============================================================

print("\n\n--- TODO 2: Architecture Quiz ---\n")

print("  For each description, name the Kubernetes component.\n")

quiz = [
    {
        "description": "Stores all cluster state as key-value pairs",
        "answer": "___",  # etcd
        "correct": "etcd",
    },
    {
        "description": "Assigns new pods to appropriate worker nodes",
        "answer": "___",  # Scheduler
        "correct": "Scheduler",
    },
    {
        "description": "Runs on every worker node, starts/stops containers",
        "answer": "___",  # kubelet
        "correct": "kubelet",
    },
    {
        "description": "The single entry point for all cluster API calls",
        "answer": "___",  # API Server
        "correct": "API Server",
    },
    {
        "description": "Handles network routing rules on each node",
        "answer": "___",  # kube-proxy
        "correct": "kube-proxy",
    },
    {
        "description": "Runs control loops that reconcile desired vs actual state",
        "answer": "___",  # Controller Manager
        "correct": "Controller Manager",
    },
]

# YOUR CODE HERE: Fill in the answer field for each quiz question
# quiz[0]["answer"] = "etcd"
# quiz[1]["answer"] = ???
# ... etc

score = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].lower().replace(" ", "") == q["correct"].lower().replace(" ", "")
    if is_correct:
        score += 1
    status = "PASS" if is_correct else "TODO"
    print(f"    [{status}] Q{i}: {q['description']}")
    if is_correct:
        print(f"           Your answer: {q['answer']}")
    else:
        print(f"           Your answer: {q['answer']}  (fill in the component name)")

print(f"\n  Score: {score}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 01 Summary ---\n")
print("  Key concepts covered:")
print("    1. Docker Compose = single machine; K8s = cluster orchestration")
print("    2. Control Plane (API Server, etcd, Scheduler, Controller Manager)")
print("    3. Worker Nodes (kubelet, kube-proxy, Container Runtime)")
print("    4. Declarative model: describe desired state, K8s makes it happen")
print("    5. kubectl: the CLI to interact with Kubernetes")
print(f"\n  TODO 1: {filled}/{len(docker_commands)} command mappings completed")
print(f"  TODO 2: {score}/{len(quiz)} architecture quiz answers correct")
