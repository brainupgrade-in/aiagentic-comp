"""
Lab 08 Challenge: Debugging + High Availability
==================================================
Apply everything from Session 13 — diagnose failures and build HA configurations.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-08"

print("=" * 60)
print("  Challenge: Debugging + High Availability")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Context: What you're doing
# ============================================================

print("\n--- Challenge Overview ---\n")

print("  You are the on-call engineer for the AI Agent platform.")
print("  Three tasks:\n")

deliverables = [
    ("TODO 1", "Diagnose 4 broken pods", "Read pod descriptions, identify root cause and fix"),
    ("TODO 2", "Build HA configuration", "Deployment (3 replicas, probes, resources) + HPA + PDB"),
    ("TODO 3", "Debug command cheat sheet", "Fill in 8 commands for common debug scenarios"),
]

for todo, what, detail in deliverables:
    print(f"    {todo}: {what}")
    print(f"           {detail}")
print()


# ============================================================
# TODO 1: Diagnose 4 broken pods
# ============================================================

print("\n--- TODO 1: Diagnose Broken Pods ---\n")

print("  For each pod, read the description/events/logs and diagnose the problem.\n")

broken_pods = [
    {
        "name": "agent-7f8b9c-x2k4l",
        "status": "CrashLoopBackOff",
        "restarts": 8,
        "events": [
            "Normal   Scheduled  Successfully assigned to node-1",
            "Normal   Pulled     Container image 'ai-agent:2.0' pulled",
            "Normal   Created    Created container agent",
            "Normal   Started    Started container agent",
            "Warning  BackOff    Back-off restarting failed container",
        ],
        "logs": [
            "INFO:     Starting AI Agent v2.0",
            "INFO:     Connecting to Redis at redis-svc:6379...",
            "ERROR:    ConnectionRefusedError: [Errno 111] Connection refused",
            "INFO:     Retrying in 5 seconds...",
            "ERROR:    ConnectionRefusedError: [Errno 111] Connection refused",
            "CRITICAL: Cannot connect to Redis after 3 retries. Exiting.",
        ],
        "diagnosis": "_______________",
        # Answer: Redis service not running/not ready — agent depends on Redis but it's not available
        "fix": "_______________",
        # Answer: Deploy Redis first, or add init container to wait for Redis, or add retry logic
    },
    {
        "name": "chromadb-5a9c1-m3n7p",
        "status": "Pending",
        "restarts": 0,
        "events": [
            "Warning  FailedScheduling  0/3 nodes are available:",
            "         3 Insufficient memory. (requested: 8Gi)",
        ],
        "logs": ["<no logs — pod never started>"],
        "diagnosis": "_______________",
        # Answer: Memory request (8Gi) exceeds available memory on all 3 nodes
        "fix": "_______________",
        # Answer: Reduce memory request to fit cluster capacity, or add larger nodes
    },
    {
        "name": "embedding-svc-2b4d6-k8j2",
        "status": "OOMKilled",
        "restarts": 5,
        "events": [
            "Normal   Scheduled  Successfully assigned to node-2",
            "Normal   Pulled     Container image 'embedding:1.0' pulled",
            "Normal   Created    Created container embedding",
            "Normal   Started    Started container embedding",
            "Normal   Killing    Stopping container (OOMKilled)",
        ],
        "logs": [
            "INFO: Loading sentence-transformers model (384 dimensions)...",
            "INFO: Model size: 420MB",
            "INFO: Allocating GPU tensors...",
            "Killed",
        ],
        "last_state": "Terminated: OOMKilled (exit code 137)",
        "resources": "limits: memory=256Mi",
        "diagnosis": "_______________",
        # Answer: Memory limit (256Mi) too low for model that needs ~420MB+ for loading
        "fix": "_______________",
        # Answer: Increase memory limit to at least 1Gi (420MB model + runtime overhead)
    },
    {
        "name": "api-gateway-9c3e1-p4q8",
        "status": "ImagePullBackOff",
        "restarts": 0,
        "events": [
            "Normal   Scheduled     Successfully assigned to node-3",
            "Normal   Pulling       Pulling image 'registry.internal/api-gateway:v3.1'",
            "Warning  Failed        Failed to pull image: unauthorized",
            "Warning  Failed        Error: ErrImagePull",
            "Normal   BackOff       Back-off pulling image",
        ],
        "logs": ["<no logs — container never started>"],
        "diagnosis": "_______________",
        # Answer: Unauthorized to pull from private registry — missing imagePullSecrets
        "fix": "_______________",
        # Answer: Create docker-registry Secret and add imagePullSecrets to pod spec
    },
]

# YOUR CODE HERE: For each broken pod, fill in diagnosis and fix
# broken_pods[0]["diagnosis"] = "Redis not running — agent can't connect"
# broken_pods[0]["fix"] = "Deploy Redis first or add init container"
# broken_pods[1]["diagnosis"] = ???
# broken_pods[1]["fix"] = ???
# broken_pods[2]["diagnosis"] = ???
# broken_pods[2]["fix"] = ???
# broken_pods[3]["diagnosis"] = ???
# broken_pods[3]["fix"] = ???

diag_score = 0
for pod in broken_pods:
    print(f"  Pod: {pod['name']}")
    print(f"  Status: {pod['status']} (restarts: {pod['restarts']})")
    print(f"  Events:")
    for event in pod["events"]:
        print(f"    {event}")
    print(f"  Logs:")
    for log_line in pod["logs"]:
        print(f"    | {log_line}")
    if "resources" in pod:
        print(f"  Resources: {pod['resources']}")
    if "last_state" in pod:
        print(f"  Last state: {pod['last_state']}")

    diag_filled = pod["diagnosis"] != "_______________"
    fix_filled = pod["fix"] != "_______________"
    if diag_filled:
        diag_score += 1
    if fix_filled:
        diag_score += 1

    print(f"  [{'PASS' if diag_filled else 'FAIL'}] Diagnosis: {pod['diagnosis']}")
    print(f"  [{'PASS' if fix_filled else 'FAIL'}] Fix: {pod['fix']}")
    print()

print(f"  Diagnosis score: {diag_score}/{len(broken_pods) * 2} (diagnosis + fix)")


# ============================================================
# TODO 2: Create complete HA configuration
# ============================================================

print("\n\n--- TODO 2: Build High-Availability Configuration ---\n")

print("  Create a complete production-ready HA stack for the AI Agent:")
print()
print("  1. Deployment:")
print("     - name: ai-agent")
print("     - replicas: 3")
print("     - image: ai-agent:2.0")
print("     - containerPort: 8000")
print("     - labels: app: agent")
print("     - Rolling update: maxSurge=1, maxUnavailable=0")
print("     - Readiness probe: httpGet /health:8000, initialDelay=5, period=10")
print("     - Liveness probe: httpGet /health:8000, initialDelay=15, period=20, failureThreshold=3")
print("     - Resources: requests (256Mi/250m), limits (1Gi/1000m)")
print()
print("  2. HPA:")
print("     - apiVersion: autoscaling/v2")
print("     - name: agent-hpa, targets Deployment/ai-agent")
print("     - minReplicas: 2, maxReplicas: 8")
print("     - CPU metric: averageUtilization 70%")
print("     - scaleDown stabilization: 300s")
print()
print("  3. PDB:")
print("     - apiVersion: policy/v1")
print("     - name: agent-pdb")
print("     - minAvailable: 2")
print("     - selector: app: agent\n")

# YOUR CODE HERE: Create all three YAML manifests

todo2_deployment = textwrap.dedent("""\
    # TODO: Create HA Deployment
    # - 3 replicas, rolling update strategy
    # - readiness and liveness probes
    # - resource requests and limits
    # apiVersion: apps/v1
    # kind: Deployment

""")

todo2_hpa = textwrap.dedent("""\
    # TODO: Create HPA
    # - autoscaling/v2
    # - minReplicas: 2, maxReplicas: 8
    # - CPU averageUtilization: 70
    # - scaleDown stabilization: 300s

""")

todo2_pdb = textwrap.dedent("""\
    # TODO: Create PDB
    # - policy/v1
    # - minAvailable: 2
    # - selector: app: agent

""")

with open(os.path.join(WORKDIR, "ha-deployment.yaml"), "w") as f:
    f.write(todo2_deployment)
with open(os.path.join(WORKDIR, "ha-hpa.yaml"), "w") as f:
    f.write(todo2_hpa)
with open(os.path.join(WORKDIR, "ha-pdb.yaml"), "w") as f:
    f.write(todo2_pdb)

# Validate
ha_checks = [
    # Deployment checks
    ("Deployment: apiVersion apps/v1", "apiVersion: apps/v1" in todo2_deployment),
    ("Deployment: kind Deployment", "kind: Deployment" in todo2_deployment),
    ("Deployment: replicas 3", "replicas: 3" in todo2_deployment),
    ("Deployment: has RollingUpdate strategy", "RollingUpdate" in todo2_deployment),
    ("Deployment: maxSurge defined", "maxSurge:" in todo2_deployment),
    ("Deployment: maxUnavailable defined", "maxUnavailable:" in todo2_deployment),
    ("Deployment: has readinessProbe", "readinessProbe:" in todo2_deployment),
    ("Deployment: has livenessProbe", "livenessProbe:" in todo2_deployment),
    ("Deployment: has resource requests", "requests:" in todo2_deployment),
    ("Deployment: has resource limits", "limits:" in todo2_deployment),
    ("Deployment: image ai-agent:2.0", "ai-agent:2.0" in todo2_deployment),
    # HPA checks
    ("HPA: apiVersion autoscaling/v2", "autoscaling/v2" in todo2_hpa),
    ("HPA: kind HorizontalPodAutoscaler", "HorizontalPodAutoscaler" in todo2_hpa),
    ("HPA: minReplicas 2", "minReplicas: 2" in todo2_hpa or "minReplicas:2" in todo2_hpa),
    ("HPA: maxReplicas 8", "maxReplicas: 8" in todo2_hpa or "maxReplicas:8" in todo2_hpa),
    ("HPA: CPU metric", "cpu" in todo2_hpa.lower() and "70" in todo2_hpa),
    ("HPA: scaleDown stabilization", "scaleDown:" in todo2_hpa and "stabilizationWindowSeconds" in todo2_hpa),
    # PDB checks
    ("PDB: apiVersion policy/v1", "policy/v1" in todo2_pdb),
    ("PDB: kind PodDisruptionBudget", "PodDisruptionBudget" in todo2_pdb),
    ("PDB: minAvailable 2", "minAvailable: 2" in todo2_pdb or "minAvailable:2" in todo2_pdb),
    ("PDB: selector app: agent", "app: agent" in todo2_pdb or "app:agent" in todo2_pdb),
]

ha_passed = sum(1 for _, ok in ha_checks if ok)
print(f"  HA Configuration validation ({ha_passed}/{len(ha_checks)}):\n")
for name, ok in ha_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 3: Debug command cheat sheet
# ============================================================

print("\n\n--- TODO 3: Debug Command Cheat Sheet ---\n")

print("  Fill in the kubectl command for each scenario.\n")

cheat_sheet = [
    {
        "scenario": "List all pods with their node names and IPs",
        "command": "_______________",
        "correct": "kubectl get pods -o wide",
    },
    {
        "scenario": "View logs from a crashed container (previous instance)",
        "command": "_______________",
        "correct": "kubectl logs POD --previous",
    },
    {
        "scenario": "Check why a pod is stuck in Pending (see events)",
        "command": "_______________",
        "correct": "kubectl describe pod POD",
    },
    {
        "scenario": "See real-time CPU and memory usage of all pods",
        "command": "_______________",
        "correct": "kubectl top pods",
    },
    {
        "scenario": "Open a shell inside a running container",
        "command": "_______________",
        "correct": "kubectl exec -it POD -- bash",
    },
    {
        "scenario": "View all recent cluster events sorted by time",
        "command": "_______________",
        "correct": "kubectl get events --sort-by=.lastTimestamp",
    },
    {
        "scenario": "Check if a Service has endpoints (pods matched by selector)",
        "command": "_______________",
        "correct": "kubectl get endpoints SERVICE",
    },
    {
        "scenario": "Check node conditions (disk pressure, memory pressure, etc.)",
        "command": "_______________",
        "correct": "kubectl describe node NODE",
    },
]

# YOUR CODE HERE: Fill in the commands
# cheat_sheet[0]["command"] = "kubectl get pods -o wide"
# cheat_sheet[1]["command"] = ???
# ... etc

cheat_score = 0
for i, item in enumerate(cheat_sheet, 1):
    is_correct = item["command"].strip().lower() == item["correct"].strip().lower()
    if is_correct:
        cheat_score += 1
    status = "PASS" if is_correct else "FAIL"
    print(f"    [{status}] {i}. {item['scenario']}")
    if is_correct:
        print(f"           {item['command']}")
    else:
        print(f"           Your answer: {item['command']}  (fill in the command)")

print(f"\n  Cheat sheet score: {cheat_score}/{len(cheat_sheet)}")

# Save cheat sheet
cheat_content = "# Kubernetes Debug Cheat Sheet\n\n"
for i, item in enumerate(cheat_sheet, 1):
    cmd = item["command"] if item["command"] != "_______________" else "(TODO)"
    cheat_content += f"{i}. {item['scenario']}\n   {cmd}\n\n"

with open(os.path.join(WORKDIR, "debug-cheat-sheet.txt"), "w") as f:
    f.write(cheat_content)


# ============================================================
# Validation
# ============================================================

print("\n\n--- Challenge Validation ---\n")

total_possible = (len(broken_pods) * 2) + len(ha_checks) + len(cheat_sheet)
total_score = diag_score + ha_passed + cheat_score

print(f"  Results: {total_score}/{total_possible} checks passed\n")
print(f"    TODO 1 — Diagnose broken pods:      {diag_score}/{len(broken_pods) * 2}")
print(f"    TODO 2 — HA configuration:           {ha_passed}/{len(ha_checks)}")
print(f"    TODO 3 — Debug cheat sheet:          {cheat_score}/{len(cheat_sheet)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Challenge Summary ---\n")
print(f"  Score: {total_score}/{total_possible} ({total_score/total_possible*100:.0f}%)")
print(f"\n  Files generated in {WORKDIR}/:")
expected = [
    "ha-deployment.yaml", "ha-hpa.yaml", "ha-pdb.yaml",
    "debug-cheat-sheet.txt",
]
for f in expected:
    exists = os.path.exists(os.path.join(WORKDIR, f))
    size = os.path.getsize(os.path.join(WORKDIR, f)) if exists else 0
    marker = "+" if exists else "-"
    print(f"    [{marker}] {f:<35} ({size} bytes)")

print(f"\n  To deploy on a real cluster:")
print(f"    cd {WORKDIR}")
print(f"    kubectl apply -f ha-deployment.yaml")
print(f"    kubectl apply -f ha-hpa.yaml")
print(f"    kubectl apply -f ha-pdb.yaml")
print(f"    kubectl get all")
print(f"    kubectl get pdb")
print(f"    kubectl get hpa")

print("\n" + "=" * 60)
print("Challenge complete!")
print("- TODO 1: Diagnose broken pods (CrashLoop, Pending, OOMKill, ImagePull)")
print("- TODO 2: Build complete HA config (Deployment + HPA + PDB)")
print("- TODO 3: Debug command cheat sheet")
print(f"- {total_score}/{total_possible} validation checks passing")
