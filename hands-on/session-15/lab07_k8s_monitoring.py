"""
Lab 07: Kubernetes Monitoring Stack
=====================================
Deploy Prometheus + Grafana on K8s using
kube-prometheus-stack and pod annotations.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-07"

print("=" * 50)
print("  Lab 07: Kubernetes Monitoring Stack")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: kube-prometheus-stack
# ============================================================

print("\n--- Step 1: kube-prometheus-stack ---\n")

print("  The kube-prometheus-stack Helm chart installs everything:\n")

components = [
    ("Prometheus",        "Metrics scraping and storage"),
    ("Grafana",           "Dashboards and visualization"),
    ("Alertmanager",      "Alert routing and notification"),
    ("node-exporter",     "Host metrics (CPU, disk, network) — DaemonSet"),
    ("kube-state-metrics", "K8s object state (pods, deployments)"),
    ("Prometheus Operator", "Manages Prometheus config via CRDs"),
]

for name, purpose in components:
    print(f"    {name:<22} {purpose}")

print("\n  Install commands:")
print("    helm repo add prometheus-community \\")
print("      https://prometheus-community.github.io/helm-charts")
print("    helm install monitoring prometheus-community/kube-prometheus-stack \\")
print("      --namespace monitoring --create-namespace \\")
print('      --set grafana.adminPassword="your-password"')


# ============================================================
# Step 2: Pod Annotations for Auto-Discovery
# ============================================================

print("\n\n--- Step 2: Pod Annotations ---\n")

print("  Add annotations to your Deployment for Prometheus auto-discovery:\n")

annotations_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: agent-api
    spec:
      template:
        metadata:
          annotations:
            prometheus.io/scrape: "true"      # Enable scraping
            prometheus.io/port: "8000"        # Metrics port
            prometheus.io/path: "/metrics"    # Metrics path
        spec:
          containers:
          - name: agent
            image: agent-api:2.0
            ports:
            - containerPort: 8000
""")

for line in annotations_yaml.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "annotated-deployment-example.yaml"), "w") as f:
    f.write(annotations_yaml)


# ============================================================
# Step 3: Monitoring Architecture
# ============================================================

print("\n\n--- Step 3: Architecture ---\n")

print("  Namespace layout:\n")
print("    default/                    monitoring/")
print("    ├── agent-api (x3)          ├── prometheus")
print("    │   annotations:            ├── grafana")
print("    │     scrape: true          ├── alertmanager")
print("    │     port: 8000            ├── node-exporter (DaemonSet)")
print("    ├── chromadb                ├── kube-state-metrics")
print("    └── redis                   └── otel-collector")
print()
print("  Access:")
print("    kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80")
print("    kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090")


# ============================================================
# TODO 1: Create annotated Deployment
# ============================================================

print("\n\n--- TODO 1: Annotated Agent Deployment ---\n")

print("  Create an agent-api Deployment with Prometheus annotations:")
print("    - name: agent-api, replicas: 3, image: agent-api:2.0")
print("    - containerPort: 8000")
print("    - annotations: prometheus.io/scrape=true, port=8000, path=/metrics")
print("    - readinessProbe: /health port 8000 (delay=5, period=10)")
print("    - resources: requests 256Mi/250m, limits 1Gi/1000m")

todo1_yaml = textwrap.dedent("""\
    # TODO: Agent Deployment with Prometheus annotations

""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo1_yaml)

deploy_checks = [
    ("Has kind: Deployment",        "kind: Deployment" in todo1_yaml),
    ("Has replicas: 3",             "replicas: 3" in todo1_yaml),
    ("Has agent-api image",         "agent-api" in todo1_yaml),
    ("Has containerPort 8000",      "8000" in todo1_yaml),
    ("Has prometheus.io/scrape",    "prometheus.io/scrape" in todo1_yaml),
    ("Has prometheus.io/port",      "prometheus.io/port" in todo1_yaml),
    ("Has prometheus.io/path",      "prometheus.io/path" in todo1_yaml),
    ("Has readinessProbe",          "readinessProbe:" in todo1_yaml),
    ("Has resources",               "resources:" in todo1_yaml),
]

score1 = sum(1 for _, ok in deploy_checks if ok)
print(f"\n  Validating Deployment ({score1}/{len(deploy_checks)}):\n")
for name, ok in deploy_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Monitoring stack quiz
# ============================================================

print("\n\n--- TODO 2: Monitoring Stack Quiz ---\n")

quiz = [
    {
        "question": "What Helm chart installs the full Prometheus + Grafana stack?",
        "answer": "___",
        "correct": "kube-prometheus-stack",
    },
    {
        "question": "What K8s namespace should monitoring tools be deployed in?",
        "answer": "___",
        "correct": "monitoring",
    },
    {
        "question": "What annotation enables Prometheus scraping on a pod?",
        "answer": "___",
        "correct": "prometheus.io/scrape",
    },
    {
        "question": "What K8s object type is node-exporter deployed as?",
        "answer": "___",
        "correct": "daemonset",
    },
    {
        "question": "What command accesses Grafana locally?",
        "answer": "___",
        "correct": "port-forward",
        "hint": "kubectl port-forward -n monitoring svc/grafana 3000:80",
    },
]

# YOUR CODE HERE: Fill in the answers

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace("-", "").replace("_", "").replace(" ", "")
    correct = q["correct"].lower().replace("-", "").replace("_", "").replace(" ", "")
    is_correct = correct in answer or answer == correct

    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")
    if status == "TODO" and "hint" in q:
        print(f"           Hint: {q['hint']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 07 Summary ---\n")
print("  Key concepts:")
print("    1. kube-prometheus-stack = Prometheus + Grafana + Alertmanager + exporters")
print("    2. Pod annotations enable auto-discovery (prometheus.io/scrape)")
print("    3. Separate monitoring namespace from application namespace")
print("    4. kubectl port-forward for local access to dashboards")
print(f"\n  TODO 1: {score1}/{len(deploy_checks)} deployment checks passed")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
