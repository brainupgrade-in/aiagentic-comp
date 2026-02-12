"""
Lab 07: Production Checklist Essentials
=========================================
Understand the production readiness checklist
for deploying AI applications with Python tooling.
"""

import os
import shutil

WORKDIR = "/tmp/prod-lab-12-07"

print("=" * 50)
print("  Lab 07: Production Checklist Essentials")
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
        "Python async HealthChecker for each service endpoint",
        "Signal handlers (SIGTERM) for graceful shutdown",
        "Startup sequencing with retry/wait loops for dependencies",
        "FastAPI /health endpoint with dependency checks",
    ]),
    ("Resource Management", [
        "psutil for memory/CPU monitoring per process",
        "uvicorn --workers for scaling worker processes",
        "Local file storage for persistent data",
        "In-process ChromaDB for vector DB (no server needed)",
    ]),
    ("Secrets Management", [
        ".env files (never committed to git)",
        ".gitignore for .env, .env.example for templates",
        "python-dotenv load_dotenv() for env injection",
        "Vault services for production (HashiCorp Vault, AWS Secrets Manager)",
    ]),
    ("Observability", [
        "Structured JSON logs with trace_id",
        "LangFuse for AI-specific traces and cost tracking",
        "FastAPI /health endpoint for monitoring",
        "Python logging module with JSONFormatter",
    ]),
    ("Alerting", [
        "Critical: down, error rate, OOM",
        "Warning: latency, cost, storage",
        "LangFuse alerts for cost/latency thresholds",
        "External monitoring (UptimeRobot, Healthchecks.io)",
    ]),
    ("Backup & Recovery", [
        "ChromaDB persist_directory backups",
        "Application state snapshots",
        "Config files in version control",
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

print("  Correct order for deploying AI stack with Python tooling:\n")
order = [
    ("1. Environment",     "Create .env from .env.example, set API keys"),
    ("2. Config files",    ".env, app.py, requirements.txt"),
    ("3. Dependencies",    "pip install -r requirements.txt"),
    ("4. Startup checks",  "Validate env vars, wait for external services (retry loops)"),
    ("5. Application",     "uvicorn app:app --host 0.0.0.0 --port 8000"),
    ("6. Verify",          "curl localhost:8000/health"),
]
for step, detail in order:
    print(f"    {step:<22} {detail}")


# ============================================================
# Step 3: Resource Recommendations
# ============================================================

print("\n\n--- Step 3: Resource Recommendations (8 GB Codespace) ---\n")

resources = [
    ("Agent API (uvicorn)",  "256 MB",   "1 GB",     "2 workers (--workers 2)"),
    ("ChromaDB (in-proc)",   "512 MB",   "2 GB",     "1 (in-process, no server)"),
    ("LangFuse (if used)",   "512 MB",   "1 GB",     "1 (external service)"),
    ("Python total",         "~1.5 GB",  "~4 GB",    "Monitor with psutil"),
]

print(f"    {'Component':<22} {'Typical':<16} {'Peak':<16} {'Notes'}")
print(f"    {'-'*74}")
for comp, req, lim, rep in resources:
    print(f"    {comp:<22} {req:<16} {lim:<16} {rep}")


# ============================================================
# TODO 1: Match scenarios to checklist items
# ============================================================

print("\n\n--- TODO 1: Production Scenarios ---\n")

print("  For each scenario, identify the checklist category.")
print("  Options: health, resources, secrets, observability, alerting, backup\n")

scenarios = [
    {
        "scenario": "API keys are stored in a file committed to git",
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
        "scenario": "Traffic spike causes process to run out of memory",
        "answer": "resources",
        "correct": "resources",
    },
    {
        "scenario": "ChromaDB data lost after process restart",
        "answer": "backup",
        "correct": "backup",
    },
    {
        "scenario": "Error rate hits 10% but nobody notices for hours",
        "answer": "alerting",
        "correct": "alerting",
    },
    {
        "scenario": "App starts before database is ready, crashes on connect",
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
        "question": "What Python signal enables graceful shutdown on termination?",
        "answer": "SIGTERM",
        "correct": "sigterm",
        "check": "sigterm",
    },
    {
        "question": "What Python class can periodically check if endpoints are healthy?",
        "answer": "HealthChecker",
        "correct": "healthchecker",
        "check": "healthcheck",
    },
    {
        "question": "Should API keys go in git or in a .env file?",
        "answer": ".env file",
        "correct": ".env",
        "check": "env",
    },
    {
        "question": "What Python library monitors process memory and CPU usage?",
        "answer": "psutil",
        "correct": "psutil",
        "check": "psutil",
    },
    {
        "question": "What tool provides AI-specific trace observability (traces, cost, latency)?",
        "answer": "LangFuse",
        "correct": "langfuse",
        "check": "langfuse",
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

print(f"\n\n--- Lab 07 Summary ---\n")
print("  Key concepts:")
print("    1. Six categories: health, resources, secrets, observability, alerting, backup")
print("    2. Deploy in order: config -> deps -> startup checks -> app -> verify")
print("    3. Use psutil to monitor resource usage and prevent OOM")
print("    4. Use .env files (not hardcoded) for API keys with load_dotenv()")
print(f"\n  TODO 1: {score1}/{len(scenarios)} scenarios matched")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
