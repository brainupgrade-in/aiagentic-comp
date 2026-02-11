"""
Lab 01: Production Checklist Essentials
=========================================
Understand the production readiness checklist
for deploying AI applications on Kubernetes.
"""

import os
import shutil

WORKDIR = "/tmp/k8s-lab-15-01"

print("=" * 50)
print("  Lab 01: Production Checklist Essentials")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Production Readiness Categories
# ============================================================

print("\n--- Step 1: Production Readiness Categories ---\n")

categories = [
    ("Health & Reliability", [
        "Readiness + liveness probes",
        "Self-healing (Deployment + 2+ replicas)",
        "PodDisruptionBudget",
        "Rolling update strategy",
    ]),
    ("Resource Management", [
        "CPU/memory requests and limits",
        "HPA (CPU target 60-80%)",
        "StatefulSets for persistent data",
        "PVC for vector DB storage",
    ]),
    ("Secrets Management", [
        "K8s Secrets (NOT ConfigMap for keys)",
        "RBAC for secret access",
        "Never hardcode API keys",
        "External Secrets Operator (advanced)",
    ]),
    ("Observability", [
        "Structured JSON logs with trace_id",
        "Prometheus /metrics endpoint",
        "Grafana dashboards (RED method)",
        "LangFuse for AI-specific traces",
    ]),
    ("Alerting", [
        "Critical: down, error rate, OOM",
        "Warning: latency, cost, storage",
        "Alertmanager routing per severity",
        "PagerDuty (critical), Slack (warning)",
    ]),
    ("Backup & Recovery", [
        "ChromaDB PVC snapshots",
        "PostgreSQL pg_dump for LangFuse",
        "GitOps: all manifests in version control",
        "RTO/RPO targets defined",
    ]),
]

for cat, items in categories:
    print(f"  {cat}:")
    for item in items:
        print(f"    - {item}")
    print()


# ============================================================
# Step 2: Deployment Order
# ============================================================

print("--- Step 2: Deployment Order ---\n")

print("  Correct order for deploying AI stack:\n")
order = [
    ("1. Namespaces",      "kubectl create namespace ai-stack && monitoring"),
    ("2. Config + Secrets", "ConfigMap, Secret (API keys, settings)"),
    ("3. Data layer",       "Redis, ChromaDB (StatefulSet), PostgreSQL"),
    ("4. Observability",    "Prometheus (Helm), OTel Collector, LangFuse"),
    ("5. Application",      "Deployment, Service, HPA, PDB"),
    ("6. Ingress",          "Ingress controller + rules"),
    ("7. Verify",           "kubectl get all -n ai-stack"),
]
for step, detail in order:
    print(f"    {step:<22} {detail}")


# ============================================================
# Step 3: Resource Recommendations
# ============================================================

print("\n\n--- Step 3: Resource Recommendations ---\n")

resources = [
    ("Agent API",     "256Mi/250m",  "1Gi/1000m",    "3 (HPA: 2-10)"),
    ("ChromaDB",      "512Mi/500m",  "2Gi/1000m",    "1 (StatefulSet)"),
    ("Redis",         "64Mi/100m",   "128Mi/200m",   "1"),
    ("OTel Collector", "128Mi/100m", "512Mi/500m",   "1"),
    ("LangFuse",      "256Mi/250m",  "1Gi/1000m",    "1"),
    ("PostgreSQL",    "256Mi/250m",  "1Gi/500m",     "1 (StatefulSet)"),
]

print(f"    {'Component':<18} {'Requests':<16} {'Limits':<16} {'Replicas'}")
print(f"    {'-'*70}")
for comp, req, lim, rep in resources:
    print(f"    {comp:<18} {req:<16} {lim:<16} {rep}")


# ============================================================
# TODO 1: Match scenarios to checklist items
# ============================================================

print("\n\n--- TODO 1: Production Scenarios ---\n")

print("  For each scenario, identify the checklist category.")
print("  Options: health, resources, secrets, observability, alerting, backup\n")

scenarios = [
    {
        "scenario": "API keys are stored in a ConfigMap visible to all pods",
        "answer": "secrets",
        "correct": "secrets",
    },
    {
        "scenario": "App crashes and stays down until manual restart",
        "answer": "health",
        "correct": "health",
    },
    {
        "scenario": "Can't tell which LLM call caused the slow response",
        "answer": "observability",
        "correct": "observability",
    },
    {
        "scenario": "Traffic spike causes pods to run out of memory",
        "answer": "resources",
        "correct": "resources",
    },
    {
        "scenario": "ChromaDB data lost after pod restart",
        "answer": "backup",
        "correct": "backup",
    },
    {
        "scenario": "Error rate hits 10% but nobody notices for hours",
        "answer": "alerting",
        "correct": "alerting",
    },
    {
        "scenario": "Deploying 3 pods but cluster maintenance takes all down",
        "answer": "health",
        "correct": "health",
    },
    {
        "scenario": "LLM costs double overnight with no explanation",
        "answer": "alerting",
        "correct": "alerting",
    },
]

score1 = 0
for i, s in enumerate(scenarios, 1):
    is_correct = s["answer"].strip().lower() == s["correct"]
    if s["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score1 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] {i}. {s['scenario']}")

print(f"\n  Score: {score1}/{len(scenarios)}")


# ============================================================
# TODO 2: Production readiness quiz
# ============================================================

print("\n\n--- TODO 2: Production Readiness Quiz ---\n")

quiz = [
    {
        "question": "What K8s object ensures minimum pods during maintenance?",
        "answer": "PDB (PodDisruptionBudget)",
        "correct": "poddisruptionbudget",
        "check": "pdb",
    },
    {
        "question": "What probe checks if a pod is ready to receive traffic?",
        "answer": "readiness probe",
        "correct": "readinessprobe",
        "check": "readiness",
    },
    {
        "question": "Should API keys go in ConfigMap or Secret?",
        "answer": "secret",
        "correct": "secret",
        "check": "secret",
    },
    {
        "question": "What K8s object auto-scales pods based on CPU?",
        "answer": "HPA",
        "correct": "hpa",
        "check": "hpa",
    },
    {
        "question": "What K8s object type should ChromaDB use for persistent storage?",
        "answer": "StatefulSet",
        "correct": "statefulset",
        "check": "stateful",
    },
]

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    is_correct = q["check"] in answer

    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 01 Summary ---\n")
print("  Key concepts:")
print("    1. Six categories: health, resources, secrets, observability, alerting, backup")
print("    2. Deploy in order: config -> data -> observability -> app -> ingress")
print("    3. Set resource requests AND limits for every container")
print("    4. Use Secrets (not ConfigMap) for API keys")
print(f"\n  TODO 1: {score1}/{len(scenarios)} scenarios matched")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
