"""
Lab 08: Challenge - Production-Ready AI API
=============================================
Goal: Build a complete production-ready FastAPI application combining
      ALL patterns from this session: FastAPI endpoints, Pydantic models,
      health checks, structured logging, secrets management, and
      production checklist validation.

Scenario:
  UniGPS is deploying an AI support agent to production.
  You need to create:
  1. A FastAPI app with Pydantic request/response models
  2. A production-grade /health endpoint with dependency checks
  3. Structured JSON logging configuration
  4. A .env file and Python deployment config (load_dotenv + uvicorn)
  5. A production readiness checklist score

No API key needed - pure Python + FastAPI.
"""

import os
import shutil
import json
import textwrap
from datetime import datetime

WORKDIR = "/tmp/prod-lab-12-08"

print("=" * 60)
print("  Challenge: Production-Ready AI API")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Architecture Overview
# ============================================================

print("\n--- Architecture ---\n")

print("  Production AI API Stack (Python):")
print("  ==================================")
print("    Client -> uvicorn -> FastAPI (+ /health)")
print("                           |")
print("                     +-----+-----+")
print("                     |           |")
print("                  LangGraph   ChromaDB")
print("                   Agent    (in-process)")
print("                     |")
print("                  Groq API")
print("                  (.env + load_dotenv)")
print()
print("  Production layers:")
print("    1. API: FastAPI + Pydantic validation")
print("    2. Health: /health with dependency checks + HealthChecker")
print("    3. Logging: Structured JSON with trace_id")
print("    4. Secrets: .env file + load_dotenv() + uvicorn launch")
print("    5. Checklist: Readiness score")


# ============================================================
# TODO 1: FastAPI App with Pydantic Models (write to file)
# ============================================================

print("\n\n--- TODO 1: FastAPI App with Pydantic Models ---\n")

print("  Create a FastAPI app with:")
print("    - SupportRequest model: employee_name (str, min 2 chars),")
print("      request (str, min 5 chars), priority (str, default='normal',")
print("      pattern: low|normal|high|urgent)")
print("    - SupportResponse model: category (str), response (str),")
print("      priority (str), timestamp (str)")
print("    - POST /api/support endpoint using the models")
print("    - Simple keyword classifier for: hr, tech, finance, general\n")

todo1_code = textwrap.dedent("""\
    # TODO: Production FastAPI app
    # 1. Import FastAPI, BaseModel, Field
    # 2. Create SupportRequest with Field constraints
    # 3. Create SupportResponse model
    # 4. Add classify_request() function
    # 5. Add POST /api/support endpoint

""")

with open(os.path.join(WORKDIR, "app.py"), "w") as f:
    f.write(todo1_code)

checks1 = [
    ("Has FastAPI import",       "FastAPI" in todo1_code or "fastapi" in todo1_code),
    ("Has BaseModel",            "BaseModel" in todo1_code),
    ("Has Field import",         "Field" in todo1_code),
    ("Has SupportRequest",       "SupportRequest" in todo1_code),
    ("Has SupportResponse",      "SupportResponse" in todo1_code),
    ("Has employee_name",        "employee_name" in todo1_code),
    ("Has min_length",           "min_length" in todo1_code),
    ("Has priority pattern",     "pattern" in todo1_code or "priority" in todo1_code),
    ("Has /api/support",         "/api/support" in todo1_code),
    ("Has classify function",    "classify" in todo1_code),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Health Endpoint (write to file)
# ============================================================

print("\n\n--- TODO 2: Production Health Endpoint ---\n")

print("  Create a /health endpoint that:")
print("    - Checks redis (redis_client.ping())")
print("    - Checks chromadb (chroma_client.heartbeat())")
print("    - Checks model (agent.is_ready())")
print("    - Returns 200 with {\"status\": \"ok\"} if all healthy")
print("    - Returns 503 with {\"status\": \"degraded\"} if any check fails")
print("    - Include a 'checks' dict showing each dependency status\n")

todo2_code = textwrap.dedent("""\
    # TODO: Health endpoint
    # 1. @app.get("/health")
    # 2. Check all dependencies
    # 3. Return 200 or 503 based on checks

""")

with open(os.path.join(WORKDIR, "health.py"), "w") as f:
    f.write(todo2_code)

checks2 = [
    ("Has /health route",       "/health" in todo2_code),
    ("Has async def",           "async def" in todo2_code or "def health" in todo2_code),
    ("Checks redis",            "redis" in todo2_code),
    ("Checks chromadb",         "chromadb" in todo2_code or "chroma" in todo2_code),
    ("Checks model",            "model" in todo2_code or "agent" in todo2_code or "ready" in todo2_code),
    ("Returns 200 or 503",      "200" in todo2_code and "503" in todo2_code),
    ("Has status field",        "status" in todo2_code),
    ("Has checks dict",         "checks" in todo2_code),
]

score2 = sum(1 for _, ok in checks2 if ok)
print(f"  Validating ({score2}/{len(checks2)}):\n")
for name, ok in checks2:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 3: Structured JSON Logging Config (write to file)
# ============================================================

print("\n\n--- TODO 3: Structured JSON Logging ---\n")

print("  Create a Python logging config that outputs JSON with:")
print("    - timestamp, level, message, logger fields")
print("    - Extra fields: trace_id, user_id, model, tokens_in,")
print("      tokens_out, cost_usd, duration_s")
print("    - A JSONFormatter class and logger setup")
print("    - Example log entry as a JSON string\n")

todo3_code = textwrap.dedent("""\
    # TODO: Structured JSON logging
    # 1. Create JSONFormatter class
    # 2. Setup handler and logger
    # 3. Write an example log entry

""")

with open(os.path.join(WORKDIR, "logging_config.py"), "w") as f:
    f.write(todo3_code)

# Also check for a sample JSON log entry
todo3_log = "___"

checks3 = [
    ("Has JSONFormatter class",  "JSONFormatter" in todo3_code or "Formatter" in todo3_code),
    ("Has logging import",       "logging" in todo3_code or "import json" in todo3_code),
    ("Has trace_id field",       "trace_id" in todo3_code),
    ("Has handler setup",        "handler" in todo3_code or "Handler" in todo3_code),
    ("Has logger setup",         "logger" in todo3_code or "getLogger" in todo3_code),
]

# Validate the sample log entry
log_valid = False
if todo3_log != "___":
    try:
        parsed = json.loads(todo3_log)
        log_valid = all(
            any(f in k.lower() for k in parsed.keys())
            for f in ["level", "message"]
        )
    except (json.JSONDecodeError, TypeError):
        log_valid = False

checks3.append(("Sample log is valid JSON", log_valid))

score3 = sum(1 for _, ok in checks3 if ok)
print(f"  Validating ({score3}/{len(checks3)}):\n")
for name, ok in checks3:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 4: .env File and Python Deployment Config
# ============================================================

print("\n\n--- TODO 4: .env File and Python Deployment Config ---\n")

print("  Create:")
print("    - A .env file with: GROQ_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY")
print("    - Python code using load_dotenv() to load .env")
print("    - A .gitignore entry for .env")
print("    - A uvicorn launch command for the application\n")

todo4_config = textwrap.dedent("""\
    # TODO: .env file + Python deployment config (load_dotenv + uvicorn)

""")

with open(os.path.join(WORKDIR, "deploy_config.py"), "w") as f:
    f.write(todo4_config)

checks4 = [
    ("Has .env content",        ".env" in todo4_config or "GROQ" in todo4_config),
    ("Has GROQ_API_KEY",        "GROQ_API_KEY" in todo4_config),
    ("Has LANGFUSE_SECRET_KEY", "LANGFUSE_SECRET_KEY" in todo4_config),
    ("Has LANGFUSE_PUBLIC_KEY", "LANGFUSE_PUBLIC_KEY" in todo4_config),
    ("Has load_dotenv",         "load_dotenv" in todo4_config),
    ("Has uvicorn",             "uvicorn" in todo4_config),
    ("Has signal handler",      "signal" in todo4_config or "SIGTERM" in todo4_config),
    ("Has health check",        "health" in todo4_config.lower()),
]

score4 = sum(1 for _, ok in checks4 if ok)
print(f"  Validating ({score4}/{len(checks4)}):\n")
for name, ok in checks4:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 5: Production Checklist Scoring
# ============================================================

print("\n\n--- TODO 5: Production Checklist ---\n")

print("  Score your production readiness (answer each):\n")

checklist = [
    {
        "item": "Health endpoint checks all dependencies (redis, chromadb, model)",
        "answer": "___",
        "correct": "yes",
    },
    {
        "item": "Structured JSON logging with trace_id correlation",
        "answer": "___",
        "correct": "yes",
    },
    {
        "item": "API keys stored in .env file (not hardcoded or in git)",
        "answer": "___",
        "correct": "yes",
    },
    {
        "item": "Pydantic models validate all request inputs",
        "answer": "___",
        "correct": "yes",
    },
    {
        "item": "Signal handler (SIGTERM) configured for graceful shutdown",
        "answer": "___",
        "correct": "yes",
    },
    {
        "item": "psutil monitoring for memory/CPU to prevent OOM",
        "answer": "___",
        "correct": "yes",
    },
]

# YOUR CODE HERE: Answer "yes" or "no" for each item
# checklist[0]["answer"] = "yes"

score5 = 0
for i, c in enumerate(checklist, 1):
    if c["answer"] == "___":
        status = "TODO"
    elif c["answer"].strip().lower() == c["correct"]:
        status = "PASS"
        score5 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] {i}. {c['item']}")

print(f"\n  Checklist score: {score5}/{len(checklist)}")


# ============================================================
# Summary
# ============================================================

total_checks = len(checks1) + len(checks2) + len(checks3) + len(checks4) + len(checklist)
total_score = score1 + score2 + score3 + score4 + score5

print(f"\n\n{'=' * 60}")
print(f"  Challenge Summary")
print(f"{'=' * 60}")
print(f"\n  TODO 1 - FastAPI + Pydantic:       {score1}/{len(checks1)}")
print(f"  TODO 2 - Health Endpoint:           {score2}/{len(checks2)}")
print(f"  TODO 3 - Structured Logging:        {score3}/{len(checks3)}")
print(f"  TODO 4 - .env + Python Deploy:      {score4}/{len(checks4)}")
print(f"  TODO 5 - Production Checklist:      {score5}/{len(checklist)}")
print(f"\n  TOTAL: {total_score}/{total_checks}")
print(f"\n  Files generated in {WORKDIR}/")
print(f"    - app.py              (FastAPI application)")
print(f"    - health.py           (Health endpoint)")
print(f"    - logging_config.py   (JSON logging setup)")
print(f"    - deploy_config.py    (Python deployment config)")

if total_score == total_checks:
    print(f"\n  PRODUCTION READY! All checks passed.")
elif total_score >= total_checks * 0.7:
    print(f"\n  ALMOST THERE! Fix remaining items for production readiness.")
else:
    print(f"\n  NEEDS WORK. Review the session labs and fill in TODO sections.")

print(f"\nCheck solutions/lab08_challenge.py when done!")
