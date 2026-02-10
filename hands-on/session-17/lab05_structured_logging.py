"""
Lab 05: Structured Logging in Production
===========================================
Convert print statements to structured JSON logs
with trace_id correlation for AI applications.
"""

import os
import shutil
import textwrap
import json

WORKDIR = "/tmp/k8s-lab-17-05"

print("=" * 50)
print("  Lab 05: Structured Logging in Production")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Why Structured Logging?
# ============================================================

print("\n--- Step 1: Why Structured Logging? ---\n")

print("  WRONG (unstructured):")
print('    print(f"Processed request for user {user_id} in {duration}s")')
print("    → Processed request for user alice in 2.3s")
print()
print("  RIGHT (structured JSON):")
print('    logger.info("request_processed", extra={')
print('        "user_id": "alice",')
print('        "duration_s": 2.3,')
print('        "trace_id": "abc123",')
print("    })")
print('    → {"level":"INFO","msg":"request_processed","user_id":"alice","duration_s":2.3,"trace_id":"abc123"}')

print("\n  Benefits of structured logging:")
benefits = [
    ("Machine parseable",  "Log aggregators (Loki, ELK) can index fields"),
    ("Searchable",         "Query: user_id='alice' AND duration_s > 5"),
    ("Correlated",         "trace_id links logs to traces and spans"),
    ("AI-specific",        "Add model, tokens, cost as log fields"),
]
for benefit, detail in benefits:
    print(f"    {benefit:<22} → {detail}")


# ============================================================
# Step 2: AI-Specific Log Fields
# ============================================================

print("\n\n--- Step 2: AI-Specific Log Fields ---\n")

print("  Add these fields to AI application logs:\n")
fields = [
    ("trace_id",    "Correlation with distributed traces"),
    ("user_id",     "Who made the request"),
    ("model",       "Which LLM model was used"),
    ("tokens_in",   "Input token count"),
    ("tokens_out",  "Output token count"),
    ("cost_usd",    "Estimated cost of this call"),
    ("duration_s",  "Request latency"),
    ("endpoint",    "API endpoint (/chat, /search)"),
    ("status",      "HTTP status code"),
]
print(f"    {'Field':<14} {'Purpose'}")
print(f"    {'-'*50}")
for field, purpose in fields:
    print(f"    {field:<14} {purpose}")


# ============================================================
# Step 3: Python Logging Setup
# ============================================================

print("\n\n--- Step 3: Python JSON Logging ---\n")

logging_code = textwrap.dedent("""\
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
            # Add extra fields (user_id, trace_id, etc.)
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

for line in logging_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# TODO 1: Write structured log entries
# ============================================================

print("\n\n--- TODO 1: Structured Log Entries ---\n")

print("  Create 3 structured log entries as JSON strings.\n")

logs = [
    {
        "description": "Successful LLM call (INFO): model=llama3-70b, tokens=800+200, cost=0.004",
        "json_str": "___",
        "check_fields": ["level", "model", "tokens"],
    },
    {
        "description": "Slow request warning (WARN): duration_s=8.5, endpoint=/chat, user_id=alice",
        "json_str": "___",
        "check_fields": ["level", "duration", "user_id"],
    },
    {
        "description": "Error (ERROR): status=500, error='ChromaDB timeout', trace_id=xyz789",
        "json_str": "___",
        "check_fields": ["level", "error", "trace_id"],
    },
]

# YOUR CODE HERE: Write JSON log strings
# logs[0]["json_str"] = '{"level": "INFO", "message": "llm_call", "model": "llama3-70b", ...}'

score1 = 0
total1 = len(logs)
for i, log in enumerate(logs, 1):
    if log["json_str"] == "___":
        status = "TODO"
        valid = False
    else:
        try:
            parsed = json.loads(log["json_str"])
            has_fields = all(
                any(f in k.lower() for k in parsed.keys())
                for f in log["check_fields"]
            )
            if has_fields:
                status = "PASS"
                score1 += 1
                valid = True
            else:
                status = "FAIL"
                valid = False
        except json.JSONDecodeError:
            status = "FAIL"
            valid = False

    print(f"    [{status}] {i}. {log['description']}")
    if not valid and log["json_str"] != "___":
        print(f"           Missing fields: {log['check_fields']}")

print(f"\n  Score: {score1}/{total1}")


# ============================================================
# TODO 2: Logging quiz
# ============================================================

print("\n\n--- TODO 2: Logging Quiz ---\n")

quiz = [
    {
        "question": "What format should production logs use? (text/json)",
        "answer": "___",
        "correct": "json",
    },
    {
        "question": "What field correlates logs with distributed traces?",
        "answer": "___",
        "correct": "trace_id",
    },
    {
        "question": "What Python module is used instead of print() for logging?",
        "answer": "___",
        "correct": "logging",
    },
    {
        "question": "What log aggregation tools can index structured JSON fields?",
        "answer": "___",
        "correct": "loki",
        "check_fn": lambda a: "loki" in a.lower() or "elk" in a.lower() or "elastic" in a.lower(),
    },
]

# YOUR CODE HERE: Fill in quiz answers

score2 = 0
for i, q in enumerate(quiz, 1):
    if q["answer"] == "___":
        status = "TODO"
    elif "check_fn" in q:
        if q["check_fn"](q["answer"]):
            status = "PASS"
            score2 += 1
        else:
            status = "FAIL"
    else:
        answer = q["answer"].strip().lower().replace("_", "").replace(" ", "")
        correct = q["correct"].lower().replace("_", "").replace(" ", "")
        if answer == correct:
            status = "PASS"
            score2 += 1
        else:
            status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 05 Summary ---\n")
print("  Key concepts:")
print("    1. Use structured JSON logging, not print()")
print("    2. Include trace_id for correlation with distributed traces")
print("    3. Add AI fields: model, tokens, cost, duration")
print("    4. JSON logs are machine-parseable and searchable")
print(f"\n  TODO 1: {score1}/{total1} structured log entries")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
