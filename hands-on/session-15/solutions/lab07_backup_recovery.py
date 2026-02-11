"""
Lab 07: Backup & Disaster Recovery
=====================================
Design backup strategies for ChromaDB, PostgreSQL,
and define RTO/RPO targets for AI stack components.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-07"

print("=" * 50)
print("  Lab 07: Backup & Disaster Recovery")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: What Needs Backup?
# ============================================================

print("\n--- Step 1: What Needs Backup? ---\n")

components = [
    ("ChromaDB",      "Vector embeddings",    "PVC snapshot",     "Daily"),
    ("PostgreSQL",    "LangFuse traces",       "pg_dump",          "Daily + WAL"),
    ("Redis",         "Cache (ephemeral)",     "RDB snapshot",     "Optional"),
    ("K8s manifests", "Infrastructure config", "Git repository",   "Every commit"),
    ("Secrets",       "API keys, passwords",   "Sealed Secrets",   "Every change"),
    ("Prometheus",    "Metrics (TSDB)",        "Remote write",     "Continuous"),
]

print(f"    {'Component':<16} {'Data':<22} {'Backup Method':<18} {'Frequency'}")
print(f"    {'-'*75}")
for comp, data, method, freq in components:
    print(f"    {comp:<16} {data:<22} {method:<18} {freq}")


# ============================================================
# Step 2: RTO/RPO Definitions
# ============================================================

print("\n\n--- Step 2: RTO and RPO ---\n")

print("  RTO (Recovery Time Objective):")
print("    How long until service is restored after failure?")
print("    Example: 'Agent API must be back within 15 minutes'")
print()
print("  RPO (Recovery Point Objective):")
print("    How much data can we afford to lose?")
print("    Example: 'No more than 1 hour of trace data lost'")

print("\n  Targets by component:\n")
targets = [
    ("Agent API",    "5 min",   "N/A (stateless)",   "K8s self-heals with replicas"),
    ("ChromaDB",     "30 min",  "24 hours",          "Restore PVC from snapshot"),
    ("PostgreSQL",   "30 min",  "1 hour",            "pg_dump + WAL replay"),
    ("Redis",        "5 min",   "N/A (cache)",       "Cache rebuild on restart"),
    ("Grafana",      "15 min",  "N/A (dashboards)",  "Dashboards stored as code"),
]

print(f"    {'Component':<14} {'RTO':<10} {'RPO':<18} {'Recovery Strategy'}")
print(f"    {'-'*75}")
for comp, rto, rpo, strategy in targets:
    print(f"    {comp:<14} {rto:<10} {rpo:<18} {strategy}")


# ============================================================
# Step 3: Backup Commands
# ============================================================

print("\n\n--- Step 3: Backup Commands ---\n")

print("  ChromaDB PVC snapshot:")
print("    kubectl get pvc -n ai-stack")
print("    # Create VolumeSnapshot (requires CSI snapshot support)")

snapshot_yaml = textwrap.dedent("""\
    apiVersion: snapshot.storage.k8s.io/v1
    kind: VolumeSnapshot
    metadata:
      name: chromadb-snapshot-20250210
      namespace: ai-stack
    spec:
      source:
        persistentVolumeClaimName: chromadb-data-chromadb-0
""")

for line in snapshot_yaml.strip().split("\n"):
    print(f"    {line}")

print("\n  PostgreSQL pg_dump:")
print("    kubectl exec -n monitoring postgres-0 -- \\")
print("      pg_dump -U langfuse langfuse > langfuse-backup.sql")

print("\n  GitOps — manifests as code:")
print("    git add k8s/ && git commit -m 'Update manifests' && git push")

with open(os.path.join(WORKDIR, "snapshot-reference.yaml"), "w") as f:
    f.write(snapshot_yaml)


# ============================================================
# TODO 1: Backup plan design
# ============================================================

print("\n\n--- TODO 1: Design Backup Plan ---\n")

print("  For each component, specify: backup method, frequency, RTO, RPO.\n")

backup_plan = [
    {
        "component": "ChromaDB vector data",
        "method": "PVC snapshot",
        "frequency": "daily",
        "rto": "30 min",
        "rpo": "24 hours",
        "check_method": "snapshot",
        "check_freq": "daily",
    },
    {
        "component": "LangFuse PostgreSQL",
        "method": "pg_dump + WAL archiving",
        "frequency": "daily + continuous WAL",
        "rto": "30 min",
        "rpo": "1 hour",
        "check_method": "pg_dump",
        "check_freq": "daily",
    },
    {
        "component": "Kubernetes manifests",
        "method": "git repository (GitOps)",
        "frequency": "every commit",
        "rto": "15 min",
        "rpo": "0 (version controlled)",
        "check_method": "git",
        "check_freq": "commit",
    },
    {
        "component": "Prometheus metrics",
        "method": "remote write to long-term storage",
        "frequency": "continuous",
        "rto": "15 min",
        "rpo": "near zero",
        "check_method": "remote",
        "check_freq": "continu",
    },
]

score1 = 0
total1 = len(backup_plan) * 2  # method + frequency
for i, b in enumerate(backup_plan, 1):
    method_ok = b["method"] != "___" and b["check_method"] in b["method"].lower()
    freq_ok = b["frequency"] != "___" and b["check_freq"] in b["frequency"].lower()

    if b["method"] == "___":
        m_status = "TODO"
    elif method_ok:
        m_status = "PASS"
        score1 += 1
    else:
        m_status = "FAIL"

    if b["frequency"] == "___":
        f_status = "TODO"
    elif freq_ok:
        f_status = "PASS"
        score1 += 1
    else:
        f_status = "FAIL"

    print(f"    {i}. {b['component']}")
    print(f"       [{m_status}] Method: {b['method']}")
    print(f"       [{f_status}] Frequency: {b['frequency']}")
    print(f"       RTO: {b['rto']}, RPO: {b['rpo']}")

print(f"\n  Score: {score1}/{total1}")


# ============================================================
# TODO 2: Recovery quiz
# ============================================================

print("\n\n--- TODO 2: Backup & Recovery Quiz ---\n")

quiz = [
    {
        "question": "What does RTO stand for?",
        "answer": "recovery time objective",
        "correct": "recovery time objective",
        "check": "recovery time",
    },
    {
        "question": "What does RPO measure?",
        "answer": "acceptable data loss",
        "correct": "data loss",
        "check": "data",
    },
    {
        "question": "What K8s object type creates point-in-time PVC backups?",
        "answer": "VolumeSnapshot",
        "correct": "volumesnapshot",
        "check": "snapshot",
    },
    {
        "question": "What tool backs up PostgreSQL databases?",
        "answer": "pg_dump",
        "correct": "pg_dump",
        "check": "pg_dump",
    },
    {
        "question": "What pattern stores all K8s manifests in Git?",
        "answer": "GitOps",
        "correct": "gitops",
        "check": "gitops",
    },
]

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    check = q["check"].replace(" ", "").replace("-", "").replace("_", "")
    is_correct = check in answer

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

print(f"\n\n--- Lab 07 Summary ---\n")
print("  Key concepts:")
print("    1. Backup: ChromaDB (PVC snapshot), PostgreSQL (pg_dump), Manifests (Git)")
print("    2. RTO = recovery time, RPO = acceptable data loss")
print("    3. Stateless services (Agent API) self-heal via K8s replicas")
print("    4. GitOps: all infrastructure as code in version control")
print(f"\n  TODO 1: {score1}/{total1} backup plan checks")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
