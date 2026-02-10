"""
Lab 01 Solution: Kubernetes Concepts
======================================
"""

import os
import shutil

WORKDIR = "/tmp/k8s-lab-01"

print("=" * 50)
print("  Lab 01 Solution: Kubernetes Concepts")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: Docker-to-Kubernetes Command Mapping
# ============================================================

print("\n--- TODO 1 Solution: Command Mapping ---\n")

docker_commands = {
    "docker ps":                       "kubectl get pods",
    "docker logs CONTAINER":           "kubectl logs POD",
    "docker exec -it CONTAINER bash":  "kubectl exec -it POD -- bash",
    "docker stop CONTAINER":           "kubectl delete pod POD",
    "docker-compose up -d":            "kubectl apply -f .",
    "docker inspect CONTAINER":        "kubectl describe pod POD",
}

print("  Docker → Kubernetes command mappings:\n")
for docker, k8s in docker_commands.items():
    print(f"    {docker:<40} → {k8s}")

filled = len(docker_commands)
print(f"\n  Completed: {filled}/{filled} mappings")

print("\n  Notes:")
print("    - 'kubectl delete pod' isn't exactly 'docker stop' — if a Deployment")
print("      manages the pod, K8s will create a replacement immediately!")
print("    - 'kubectl apply -f .' applies ALL YAML files in the directory")
print("    - 'kubectl exec' needs '--' before the command (bash)")


# ============================================================
# TODO 2 Solution: Architecture Quiz
# ============================================================

print("\n\n--- TODO 2 Solution: Architecture Quiz ---\n")

quiz = [
    {
        "description": "Stores all cluster state as key-value pairs",
        "answer": "etcd",
        "correct": "etcd",
    },
    {
        "description": "Assigns new pods to appropriate worker nodes",
        "answer": "Scheduler",
        "correct": "Scheduler",
    },
    {
        "description": "Runs on every worker node, starts/stops containers",
        "answer": "kubelet",
        "correct": "kubelet",
    },
    {
        "description": "The single entry point for all cluster API calls",
        "answer": "API Server",
        "correct": "API Server",
    },
    {
        "description": "Handles network routing rules on each node",
        "answer": "kube-proxy",
        "correct": "kube-proxy",
    },
    {
        "description": "Runs control loops that reconcile desired vs actual state",
        "answer": "Controller Manager",
        "correct": "Controller Manager",
    },
]

score = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].lower().replace(" ", "") == q["correct"].lower().replace(" ", "")
    if is_correct:
        score += 1
    print(f"    [PASS] Q{i}: {q['description']}")
    print(f"           Answer: {q['answer']}")

print(f"\n  Score: {score}/{len(quiz)}")

print("\n  Component summary:")
print("    Control Plane:")
print("      API Server       — Front door, all requests go through it")
print("      etcd             — Key-value store for ALL cluster state")
print("      Scheduler        — Places pods on nodes based on resources")
print("      Controller Mgr   — Control loops: desired → actual state")
print("    Worker Nodes:")
print("      kubelet          — Agent on each node, manages pod lifecycle")
print("      kube-proxy       — Network rules, routes traffic to pods")
print("      Container Runtime — Actually runs containers (containerd)")

print("\n" + "=" * 50)
print("Lab 01 Solution complete!")
print("- TODO 1: 6/6 Docker-to-K8s command mappings")
print(f"- TODO 2: {score}/{len(quiz)} architecture quiz answers")
