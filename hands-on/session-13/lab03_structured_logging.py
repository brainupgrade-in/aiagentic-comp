"""
Lab 03: Structured Logging
===========================
Learn structured JSON logging with trace_id correlation
for debugging AI agent applications.
"""

import os
import shutil
import textwrap
import json

WORKDIR = "/tmp/k8s-lab-13-03"

print("=" * 50)
print("  Lab 03: Structured Logging")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Structured vs Unstructured Logging
# ============================================================

print("\n--- Step 1: Structured vs Unstructured ---\n")

print("  Unstructured (BAD for searching/filtering):")
print('    2024-01-15 09:23:45 INFO Processing chat request from user-42, model=llama3')
print()
print("  Structured JSON (GOOD for searching/filtering):")
sample_log = {
    "timestamp": "2024-01-15T09:23:45Z",
    "level": "INFO",
    "message": "Processing chat request",
    "service": "agent-api",
    "trace_id": "abc123def456",
    "user_id": "user-42",
    "model": "llama3",
    "endpoint": "/chat",
}
print(f"    {json.dumps(sample_log, indent=2).replace(chr(10), chr(10) + '    ')}")

print("\n  Why structured?")
print("    1. Searchable: filter by user_id, model, trace_id")
print("    2. Parseable: tools like Loki, ELK can index fields")
print("    3. Correlatable: trace_id links logs to traces")


# ============================================================
# Step 2: AI-Specific Log Fields
# ============================================================

print("\n\n--- Step 2: AI-Specific Log Fields ---\n")

fields = [
    ("trace_id",          "Correlation ID linking logs to traces"),
    ("user_id",           "Who made the request"),
    ("model",             "Which LLM model was used"),
    ("tokens_in",         "Prompt tokens consumed"),
    ("tokens_out",        "Completion tokens generated"),
    ("tool_calls",        "List of tools the agent invoked"),
    ("retrieval_count",   "Number of documents retrieved from RAG"),
    ("cost_usd",          "Estimated cost of this request"),
    ("duration_ms",       "Total request processing time"),
    ("agent_steps",       "Number of reasoning steps taken"),
]

print(f"  {'Field':<20} {'Purpose'}")
print(f"  {'-'*60}")
for field, purpose in fields:
    print(f"  {field:<20} {purpose}")


# ============================================================
# Step 3: Log Correlation with Trace IDs
# ============================================================

print("\n\n--- Step 3: Log Correlation Demo ---\n")

print("  When a request flows through multiple services,")
print("  trace_id links all logs together:\n")

trace_id = "7f3a2b1c4d5e6f00"
logs = [
    {"service": "ingress",   "message": "Received POST /chat",       "duration_ms": None},
    {"service": "agent-api", "message": "Starting agent workflow",    "duration_ms": None},
    {"service": "agent-api", "message": "RAG retrieval: 5 docs",     "duration_ms": 45},
    {"service": "agent-api", "message": "LLM call: llama3-70b",      "duration_ms": 1250},
    {"service": "agent-api", "message": "Tool call: web_search",     "duration_ms": 320},
    {"service": "agent-api", "message": "LLM call: final response",  "duration_ms": 890},
    {"service": "agent-api", "message": "Request complete",          "duration_ms": 2505},
]

for log in logs:
    dur = f"  ({log['duration_ms']}ms)" if log['duration_ms'] else ""
    print(f"    [{log['service']:<10}] trace={trace_id[:8]}... {log['message']}{dur}")

print(f"\n  All 7 log entries share trace_id={trace_id}")
print("  Searching by trace_id shows the full request story.")


# ============================================================
# Step 4: Log Levels for AI Applications
# ============================================================

print("\n\n--- Step 4: Log Levels ---\n")

levels = [
    ("DEBUG",   "Detailed internal state (prompt text, full response)",
     "Development only — too verbose for production"),
    ("INFO",    "Normal operations (request received, workflow complete)",
     "Production default — track normal flow"),
    ("WARNING", "Recoverable issues (retry, fallback, cache miss)",
     "Things that might become errors"),
    ("ERROR",   "Failures (LLM timeout, ChromaDB down, auth failure)",
     "Requires investigation"),
]

print(f"  {'Level':<10} {'What to Log':<55} {'Note'}")
print(f"  {'-'*100}")
for level, what, note in levels:
    print(f"  {level:<10} {what:<55} {note}")


# ============================================================
# TODO 1: Create structured log entries
# ============================================================

print("\n\n--- TODO 1: Create Structured Log Entries ---\n")

print("  Create JSON log entries for each scenario.")
print("  Each log must include: timestamp, level, message, service, trace_id")
print("  Plus scenario-specific fields.\n")

# Example log entry for reference:
example = {
    "timestamp": "2024-01-15T09:23:45Z",
    "level": "INFO",
    "message": "Chat request received",
    "service": "agent-api",
    "trace_id": "abc123",
    "user_id": "user-42",
    "endpoint": "/chat",
}

todo1_logs = {
    "llm_call_complete": "___",  # Log an LLM call completing (include model, tokens_in, tokens_out, duration_ms)
    "rag_retrieval":     "___",  # Log a RAG retrieval (include collection, query, docs_found, duration_ms)
    "agent_error":       "___",  # Log an error (include error type, error message, level=ERROR)
}

# YOUR CODE HERE: Create structured log entries as JSON strings
# Example:
# todo1_logs["llm_call_complete"] = json.dumps({
#     "timestamp": "2024-01-15T09:23:46Z",
#     "level": "INFO",
#     "message": "LLM call complete",
#     "service": "agent-api",
#     "trace_id": "abc123",
#     "model": "llama3-70b",
#     "tokens_in": 850,
#     "tokens_out": 420,
#     "duration_ms": 1250,
# })

score1 = 0
total1 = len(todo1_logs)
checks = []
for name, content in todo1_logs.items():
    if content == "___":
        checks.append((f"Log: {name}", False, "TODO"))
        continue
    try:
        parsed = json.loads(content)
        has_basics = all(k in parsed for k in ["level", "message", "service"])
        has_trace = "trace_id" in parsed
        if has_basics and has_trace:
            score1 += 1
            checks.append((f"Log: {name}", True, "PASS"))
        else:
            missing = [k for k in ["level", "message", "service", "trace_id"] if k not in parsed]
            checks.append((f"Log: {name} (missing: {', '.join(missing)})", False, "FAIL"))
    except (json.JSONDecodeError, TypeError):
        checks.append((f"Log: {name} (invalid JSON)", False, "FAIL"))

for name, ok, status in checks:
    print(f"    [{status}] {name}")

print(f"\n  Score: {score1}/{total1}")


# ============================================================
# TODO 2: Log analysis quiz
# ============================================================

print("\n\n--- TODO 2: Logging Best Practices Quiz ---\n")

quiz = [
    {
        "question": "What format should production logs use? (text/json)",
        "answer": "___",
        "correct": "json",
    },
    {
        "question": "What field links logs to distributed traces?",
        "answer": "___",
        "correct": "trace_id",
    },
    {
        "question": "Should you log full LLM prompts in production? (yes/no)",
        "answer": "___",
        "correct": "no",
        "hint": "Full prompts are verbose; use DEBUG level only",
    },
    {
        "question": "What log level for a retry after a transient failure?",
        "answer": "___",
        "correct": "warning",
    },
]

# YOUR CODE HERE: Fill in the answers
# quiz[0]["answer"] = "json"
# ...

score2 = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].strip().lower() == q["correct"].lower()
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

# Save reference
ref_content = textwrap.dedent("""\
    # Structured Logging Reference

    ## Required Fields (every log entry)
    - timestamp: ISO 8601 format
    - level: DEBUG, INFO, WARNING, ERROR
    - message: Human-readable description
    - service: Service name (agent-api, chromadb)
    - trace_id: Distributed trace correlation ID

    ## AI-Specific Fields
    - model: LLM model name
    - tokens_in / tokens_out: Token counts
    - tool_calls: Agent tool invocations
    - retrieval_count: RAG documents found
    - cost_usd: Estimated cost
    - duration_ms: Processing time

    ## Best Practices
    - Use JSON format in production
    - Never log secrets or PII
    - Use DEBUG for full prompts (not in production)
    - Include trace_id for correlation
    - Log at request boundaries (start, complete, error)
""")

with open(os.path.join(WORKDIR, "logging-reference.md"), "w") as f:
    f.write(ref_content)


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 03 Summary ---\n")
print("  Key concepts:")
print("    1. Structured JSON logs are searchable and parseable")
print("    2. trace_id correlates logs across services")
print("    3. AI-specific fields: model, tokens, tool_calls, cost")
print("    4. Use INFO for normal flow, WARNING for retries, ERROR for failures")
print(f"\n  TODO 1: {score1}/{total1} log entries created")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
