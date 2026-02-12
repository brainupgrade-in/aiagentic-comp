"""
Lab 08 Solution: Challenge - Production-Ready AI API
======================================================
Complete implementation combining: FastAPI + Pydantic, health endpoint,
structured logging, .env + Python deployment config, and production checklist.

No API key needed - pure Python + FastAPI.
"""

import os
import shutil
import json
import textwrap
from datetime import datetime

WORKDIR = "/tmp/prod-lab-12-08"

print("=" * 60)
print("  Challenge Solution: Production-Ready AI API")
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
# TODO 1 Solution: FastAPI App with Pydantic Models
# ============================================================

print("\n\n--- TODO 1: FastAPI App with Pydantic Models ---\n")

todo1_code = textwrap.dedent("""\
    from fastapi import FastAPI, HTTPException
    from pydantic import BaseModel, Field
    from datetime import datetime

    app = FastAPI(title="UniGPS Support API", version="2.0.0")

    # --- Pydantic Models with Field constraints ---

    class SupportRequest(BaseModel):
        employee_name: str = Field(..., min_length=2, max_length=50)
        request: str = Field(..., min_length=5, max_length=500)
        priority: str = Field(default="normal", pattern="^(low|normal|high|urgent)$")

    class SupportResponse(BaseModel):
        category: str
        response: str
        priority: str
        timestamp: str

    # --- Keyword classifier ---

    TEMPLATES = {
        "hr": "Your HR request has been logged. Check the HR portal.",
        "tech": "A Jira ticket has been created. IT will respond within 4 hours.",
        "finance": "Your finance query is being reviewed. Expect a reply in 2 days.",
        "general": "Your request has been received. A team member will respond shortly.",
    }

    def classify_request(text: str) -> str:
        msg = text.lower()
        if any(w in msg for w in ["leave", "sick", "wfh", "policy", "hr"]):
            return "hr"
        elif any(w in msg for w in ["server", "bug", "deploy", "laptop", "vpn"]):
            return "tech"
        elif any(w in msg for w in ["expense", "salary", "invoice", "budget"]):
            return "finance"
        return "general"

    # --- Endpoint ---

    @app.post("/api/support", response_model=SupportResponse)
    async def handle_support(req: SupportRequest):
        category = classify_request(req.request)
        return SupportResponse(
            category=category,
            response=f"Hi {req.employee_name}, {TEMPLATES[category]}",
            priority=req.priority,
            timestamp=datetime.now().isoformat(),
        )
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
# TODO 2 Solution: Health Endpoint
# ============================================================

print("\n\n--- TODO 2: Production Health Endpoint ---\n")

todo2_code = textwrap.dedent("""\
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI()

    @app.get("/health")
    async def health():
        checks = {
            "redis": await redis_client.ping(),
            "chromadb": await chroma_client.heartbeat(),
            "model_loaded": agent.is_ready(),
        }
        healthy = all(checks.values())
        return JSONResponse(
            status_code=200 if healthy else 503,
            content={
                "status": "ok" if healthy else "degraded",
                "checks": checks,
            }
        )
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
# TODO 3 Solution: Structured JSON Logging Config
# ============================================================

print("\n\n--- TODO 3: Structured JSON Logging ---\n")

todo3_code = textwrap.dedent("""\
    import logging
    import json

    class JSONFormatter(logging.Formatter):
        def format(self, record):
            log_data = {
                "timestamp": self.formatTime(record),
                "level": record.levelname,
                "message": record.getMessage(),
                "logger": record.name,
            }
            for key in ["trace_id", "user_id", "model", "tokens_in",
                        "tokens_out", "cost_usd", "duration_s"]:
                if hasattr(record, key):
                    log_data[key] = getattr(record, key)
            return json.dumps(log_data)

    # Setup
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    logger = logging.getLogger("agent")
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Usage
    logger.info("llm_call_completed", extra={
        "trace_id": "abc123",
        "model": "llama3-70b",
        "tokens_in": 800,
        "tokens_out": 200,
        "cost_usd": 0.004,
        "duration_s": 1.8,
    })
""")

with open(os.path.join(WORKDIR, "logging_config.py"), "w") as f:
    f.write(todo3_code)

# Sample log entry
todo3_log = '{"level": "INFO", "message": "llm_call_completed", "model": "llama3-70b", "tokens_in": 800, "tokens_out": 200, "cost_usd": 0.004, "duration_s": 1.8, "trace_id": "abc123"}'

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
# TODO 4 Solution: .env File and Python Deployment Config
# ============================================================

print("\n\n--- TODO 4: .env File and Python Deployment Config ---\n")

todo4_config = textwrap.dedent("""\
    # --- .env file (NEVER commit to git) ---
    # GROQ_API_KEY=gsk_abc123...
    # LANGFUSE_SECRET_KEY=sk-lf-...
    # LANGFUSE_PUBLIC_KEY=pk-lf-...
    # LANGFUSE_HOST=http://localhost:8080
    # APP_ENV=production
    # LOG_LEVEL=INFO

    # --- .gitignore entry ---
    # .env
    # .env.local

    # --- Python deployment config ---
    import os
    import signal
    from dotenv import load_dotenv

    # Load environment variables from .env
    load_dotenv()

    # Validate required keys
    required_keys = ["GROQ_API_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_PUBLIC_KEY"]
    missing = [k for k in required_keys if not os.getenv(k)]
    if missing:
        raise RuntimeError(f"Missing required env vars: {missing}")

    # Signal handler for graceful shutdown
    def handle_sigterm(signum, frame):
        print("SIGTERM received, shutting down gracefully...")
        # Flush logs, close connections, etc.
        raise SystemExit(0)

    signal.signal(signal.SIGTERM, handle_sigterm)

    # --- Health check startup verification ---
    # import httpx
    # async def verify_health():
    #     async with httpx.AsyncClient() as client:
    #         resp = await client.get("http://localhost:8000/health")
    #         assert resp.status_code == 200

    # --- Launch command ---
    # uvicorn app:app --host 0.0.0.0 --port 8000 --workers 2
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
# TODO 5 Solution: Production Checklist Scoring
# ============================================================

print("\n\n--- TODO 5: Production Checklist ---\n")

checklist = [
    {
        "item": "Health endpoint checks all dependencies (redis, chromadb, model)",
        "answer": "yes",
        "correct": "yes",
    },
    {
        "item": "Structured JSON logging with trace_id correlation",
        "answer": "yes",
        "correct": "yes",
    },
    {
        "item": "API keys stored in .env file (not hardcoded or in git)",
        "answer": "yes",
        "correct": "yes",
    },
    {
        "item": "Pydantic models validate all request inputs",
        "answer": "yes",
        "correct": "yes",
    },
    {
        "item": "Signal handler (SIGTERM) configured for graceful shutdown",
        "answer": "yes",
        "correct": "yes",
    },
    {
        "item": "psutil monitoring for memory/CPU to prevent OOM",
        "answer": "yes",
        "correct": "yes",
    },
]

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
print(f"  Challenge Solution Summary")
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

print(f"\n{'=' * 60}")
print("Challenge Solution complete!")
print("Patterns used:")
print("  - FastAPI with Pydantic Field validation (min_length, pattern)")
print("  - Production /health endpoint (200 ok / 503 degraded)")
print("  - Structured JSON logging with JSONFormatter + trace_id")
print("  - .env file + load_dotenv() for secrets management")
print("  - Signal handlers (SIGTERM) for graceful shutdown")
print("  - psutil for resource monitoring (6 production categories)")
