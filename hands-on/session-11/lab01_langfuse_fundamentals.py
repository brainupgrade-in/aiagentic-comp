"""
Lab 01: LangFuse Fundamentals
===============================
Understand LangFuse architecture, trace hierarchy,
and how it complements traditional observability.
"""

import os
import shutil

WORKDIR = "/tmp/k8s-lab-11-01"

print("=" * 50)
print("  Lab 01: LangFuse Fundamentals")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Why LangFuse?
# ============================================================

print("\n--- Step 1: Why LangFuse? ---\n")

print("  What traditional observability (OTel + metrics) CAN'T do for AI:\n")
gaps = [
    ("Exact prompt text",       "Can't see what was sent to the LLM"),
    ("Full LLM response",       "Can't see what the model returned"),
    ("Prompt version compare",  "Can't A/B test prompt templates"),
    ("Cost per user",           "Can't track spend by user/conversation"),
    ("User feedback",           "Can't collect thumbs-up/down ratings"),
    ("Prompt management",       "Can't version-control prompts at runtime"),
]
for what, why in gaps:
    print(f"    {what:<25} {why}")

print("\n  What LangFuse adds:\n")
adds = [
    ("Full LLM I/O",          "Captures exact prompts + completions"),
    ("Prompt management",      "Version control, fetch at runtime"),
    ("Cost tracking",          "Per-model, per-user, per-conversation"),
    ("User feedback",          "Binary or numeric scores linked to traces"),
    ("Evaluation scoring",     "Automated quality checks on responses"),
    ("Self-hosted option",     "Run on your own infra with PostgreSQL"),
]
for what, how in adds:
    print(f"    {what:<25} {how}")


# ============================================================
# Step 2: Trace Hierarchy
# ============================================================

print("\n\n--- Step 2: Trace Hierarchy ---\n")

print("  LangFuse organizes data in three levels:\n")
print("    Trace  ─── top-level, one per user request")
print("    ├── Span  ─── logical grouping (rag_retrieval, tool_execution)")
print("    │   ├── Generation  ─── actual LLM API call")
print("    │   └── Generation  ─── another LLM call")
print("    └── Span  ─── another step")
print("        └── Generation  ─── LLM call")

print("\n  What each level captures:\n")
levels = [
    ("Trace",      "user_id, session_id, tags, metadata",
                   "One per /chat request"),
    ("Span",       "name, start_time, end_time, metadata",
                   "rag_retrieval, tool_execution, response_gen"),
    ("Generation", "model, input, output, tokens_in, tokens_out, cost",
                   "Actual LLM API call with full prompt/response"),
]
print(f"    {'Level':<12} {'Captures':<50} {'Example'}")
print(f"    {'-'*90}")
for level, captures, example in levels:
    print(f"    {level:<12} {captures:<50} {example}")


# ============================================================
# Step 3: LangFuse vs Traditional Tools
# ============================================================

print("\n\n--- Step 3: Complementary Tools ---\n")

print("  Full observability stack:\n")
print("    Layer              Tool              What It Monitors")
print("    " + "-" * 65)
stack = [
    ("Infrastructure",  "OTel Metrics",   "CPU, memory, container health, HTTP rate/errors"),
    ("Distributed Trace", "OTel Traces",  "Request flow across services, spans"),
    ("AI/LLM",          "LangFuse",       "Prompt text, LLM I/O, cost, feedback"),
    ("Log Aggregation",  "OTel Logs/ELK", "Structured logs, error details"),
    ("Alerting",         "LangFuse/OTel", "Score-based and threshold-based notifications"),
]
for layer, tool, monitors in stack:
    print(f"    {layer:<18} {tool:<18} {monitors}")


# ============================================================
# TODO 1: Match tools to capabilities
# ============================================================

print("\n\n--- TODO 1: Match Tools to Capabilities ---\n")

print("  For each capability, specify which tool handles it.")
print("  Options: otel_metrics, opentelemetry, langfuse\n")

capabilities = [
    {
        "capability": "Track request rate and error percentage",
        "answer": "___",
        "correct": "otel_metrics",
    },
    {
        "capability": "See the exact prompt sent to GPT-4",
        "answer": "___",
        "correct": "langfuse",
    },
    {
        "capability": "Trace a request across agent → chromadb → LLM",
        "answer": "___",
        "correct": "opentelemetry",
    },
    {
        "capability": "Compare two prompt template versions side-by-side",
        "answer": "___",
        "correct": "langfuse",
    },
    {
        "capability": "Alert when container memory exceeds 80%",
        "answer": "___",
        "correct": "otel_metrics",
    },
    {
        "capability": "Collect user thumbs-up/down on AI responses",
        "answer": "___",
        "correct": "langfuse",
    },
    {
        "capability": "Measure HTTP latency with histogram buckets",
        "answer": "___",
        "correct": "otel_metrics",
    },
    {
        "capability": "Track cost per user per conversation",
        "answer": "___",
        "correct": "langfuse",
    },
]

# YOUR CODE HERE: Fill in the answers
# capabilities[0]["answer"] = "otel_metrics"
# capabilities[1]["answer"] = "langfuse"
# ...

score1 = 0
for i, c in enumerate(capabilities, 1):
    is_correct = c["answer"].strip().lower() == c["correct"]
    if c["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score1 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] {i}. {c['capability']}")

print(f"\n  Score: {score1}/{len(capabilities)}")


# ============================================================
# TODO 2: Design trace hierarchy
# ============================================================

print("\n\n--- TODO 2: Trace Hierarchy Design ---\n")

print("  Design the trace hierarchy for an AI chat request.")
print("  User sends: POST /chat {message: 'What is RAG?'}")
print("  The agent: retrieves docs, calls LLM, returns answer.\n")
print("  Fill in the level (trace/span/generation) and name for each:\n")

hierarchy = [
    {
        "description": "Top-level: the entire /chat request",
        "level": "___",
        "name": "___",
        "correct_level": "trace",
        "check_name": "chat",
    },
    {
        "description": "Step: retrieve documents from ChromaDB",
        "level": "___",
        "name": "___",
        "correct_level": "span",
        "check_name": "retriev",
    },
    {
        "description": "Step: generate answer using LLM",
        "level": "___",
        "name": "___",
        "correct_level": "span",
        "check_name": "generat",
    },
    {
        "description": "Actual LLM API call within the generation step",
        "level": "___",
        "name": "___",
        "correct_level": "generation",
        "check_name": "llm",
    },
]

# YOUR CODE HERE: Fill in levels and names
# hierarchy[0]["level"] = "trace"
# hierarchy[0]["name"] = "chat_request"
# ...

score2 = 0
total2 = len(hierarchy) * 2
for i, h in enumerate(hierarchy, 1):
    level_ok = h["level"].strip().lower() == h["correct_level"]
    name_ok = h["name"] != "___" and h["check_name"] in h["name"].lower()

    if h["level"] == "___":
        l_status = "TODO"
    elif level_ok:
        l_status = "PASS"
        score2 += 1
    else:
        l_status = "FAIL"

    if h["name"] == "___":
        n_status = "TODO"
    elif name_ok:
        n_status = "PASS"
        score2 += 1
    else:
        n_status = "FAIL"

    print(f"    {i}. {h['description']}")
    print(f"       [{l_status}] Level: {h['level']}")
    print(f"       [{n_status}] Name:  {h['name']}")

print(f"\n  Score: {score2}/{total2}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 01 Summary ---\n")
print("  Key concepts:")
print("    1. LangFuse fills the AI observability gap (prompt text, cost, feedback)")
print("    2. Trace hierarchy: Trace → Span → Generation")
print("    3. Complementary stack: OTel + LangFuse = full coverage")
print("    4. Self-hosted with PostgreSQL backend")
print(f"\n  TODO 1: {score1}/{len(capabilities)} tool matching")
print(f"  TODO 2: {score2}/{total2} hierarchy design")
print(f"\n  Files generated in {WORKDIR}/")
