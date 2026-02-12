"""
Lab 07: Cost & Token Analysis
================================
Track token usage, calculate costs per model/user,
and design cost monitoring using LangFuse native features.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-11-07"

print("=" * 50)
print("  Lab 07: Cost & Token Analysis")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Cost Tracking in LangFuse
# ============================================================

print("\n--- Step 1: Cost Tracking in LangFuse ---\n")

print("  LangFuse automatically calculates cost from:")
print("    - Model name (from generation)")
print("    - Input tokens + Output tokens")
print("    - Built-in pricing table\n")

pricing = [
    ("gpt-4-turbo",             "$10.00",  "$30.00"),
    ("gpt-3.5-turbo",           "$0.50",   "$1.50"),
    ("groq/llama3-70b",         "$0.59",   "$0.79"),
    ("groq/llama3-8b",          "$0.05",   "$0.08"),
    ("text-embedding-3-small",  "$0.02",   "N/A"),
]

print(f"    {'Model':<30} {'Input/1M tokens':<18} {'Output/1M tokens'}")
print(f"    {'-'*65}")
for model, inp, out in pricing:
    print(f"    {model:<30} {inp:<18} {out}")


# ============================================================
# Step 2: Cost Breakdown Views
# ============================================================

print("\n\n--- Step 2: Cost Breakdown Views ---\n")

print("  LangFuse provides cost analysis by:\n")
views = [
    ("By model",       "Which models cost the most?",      "gpt-4: $12.50, llama3-70b: $3.20"),
    ("By user",        "Which users consume most tokens?",  "alice: $5.10, bob: $2.30"),
    ("By trace/conv",  "Which conversations are expensive?", "session_42: $0.85 (10 turns)"),
    ("By prompt ver",  "Does new prompt cost less?",        "v1: $0.008/req, v2: $0.006/req"),
    ("Over time",      "Is cost trending up or down?",      "Daily: $15 -> $12 after optimization"),
]
print(f"    {'View':<16} {'Question':<40} {'Example'}")
print(f"    {'-'*95}")
for view, question, example in views:
    print(f"    {view:<16} {question:<40} {example}")


# ============================================================
# Step 3: LangFuse Cost Tracking API
# ============================================================

print("\n\n--- Step 3: LangFuse Cost Tracking API ---\n")

print("  LangFuse tracks cost natively through its Python SDK:\n")

api_code = textwrap.dedent("""\
    from langfuse import Langfuse
    from langfuse.callback import CallbackHandler

    langfuse = Langfuse()

    # Option 1: Automatic cost tracking via CallbackHandler
    # LangFuse auto-captures model, tokens, and cost from LangChain
    handler = CallbackHandler(user_id="alice", session_id="sess_42")
    result = chain.invoke(query, config={"callbacks": [handler]})

    # Option 2: Manual generation logging with explicit cost
    trace = langfuse.trace(name="chat_request", user_id="alice")
    generation = trace.generation(
        name="llm_call",
        model="groq/llama3-70b",
        input=[{"role": "user", "content": "What is RAG?"}],
        output={"role": "assistant", "content": "RAG is..."},
        usage={"input": 150, "output": 250},
        # LangFuse auto-calculates cost, or set explicitly:
        # usage={"input": 150, "output": 250, "total_cost": 0.00028}
    )

    # Option 3: Query cost data via API
    traces = langfuse.fetch_traces(user_id="alice")
    for t in traces.data:
        print(f"  Trace: {t.name}  Cost: ${t.total_cost:.6f}")
""")

for line in api_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# TODO 1: Cost Tracking Code
# ============================================================

print("\n\n--- TODO 1: Cost Tracking Code ---\n")

print("  Write code that:")
print("    - Defines a PRICING dict (model -> input_per_1m, output_per_1m)")
print("    - Has a calculate_cost(model, tokens_in, tokens_out) function")
print("    - Creates a LangFuse trace with user_id")
print("    - Logs a generation with model, usage, and cost")
print("    - Fetches traces and prints total_cost per trace\n")

todo1_code = textwrap.dedent("""\
    # TODO: Cost tracking with PRICING dict and LangFuse generation logging

""")

with open(os.path.join(WORKDIR, "cost_tracker.py"), "w") as f:
    f.write(todo1_code)

checks1 = [
    ("Has PRICING dict",            "PRICING" in todo1_code),
    ("Has model pricing entry",     "gpt-4" in todo1_code.lower() or "llama" in todo1_code.lower()),
    ("Has calculate_cost function", "def calculate" in todo1_code or "def calc" in todo1_code),
    ("Has 1_000_000 or 1000000",    "1_000_000" in todo1_code or "1000000" in todo1_code),
    ("Has Langfuse import",         "Langfuse" in todo1_code or "langfuse" in todo1_code),
    ("Has trace creation",          ".trace(" in todo1_code or "trace(" in todo1_code),
    ("Has generation logging",      ".generation(" in todo1_code or "generation(" in todo1_code),
    ("Has usage dict",              "usage" in todo1_code),
    ("Has total_cost or fetch",     "total_cost" in todo1_code or "fetch_traces" in todo1_code),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Cost Analysis Queries
# ============================================================

print("\n\n--- TODO 2: Cost Analysis Queries ---\n")

print("  Write LangFuse SDK code snippets for cost monitoring:\n")

queries = [
    {
        "purpose": "Total cost per model over the last 24 hours",
        "code": "___",
        "check_terms": ["fetch_traces", "model", "total_cost"],
    },
    {
        "purpose": "Token consumption breakdown (input vs output) by model",
        "code": "___",
        "check_terms": ["usage", "input", "output"],
    },
    {
        "purpose": "Average cost per user session",
        "code": "___",
        "check_terms": ["session", "cost", "len"],
    },
    {
        "purpose": "Identify traces exceeding a cost threshold ($0.01)",
        "code": "___",
        "check_terms": ["total_cost", "0.01", "trace"],
    },
]

# YOUR CODE HERE: Fill in LangFuse SDK code snippets

score2 = 0
for i, q in enumerate(queries, 1):
    if q["code"] == "___":
        status = "TODO"
    elif all(t.lower() in q["code"].lower() for t in q["check_terms"]):
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] {i}. {q['purpose']}")
    print(f"           Code: {q['code'][:80]}...")

print(f"\n  Score: {score2}/{len(queries)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 07 Summary ---\n")
print("  Key concepts:")
print("    1. LangFuse auto-calculates cost from model + tokens")
print("    2. Cost views: by model, user, conversation, prompt version, time")
print("    3. LangFuse API: trace/generation logging with usage, fetch_traces for analysis")
print("    4. Cost analysis: aggregate by model, user, session; alert on thresholds")
print(f"\n  TODO 1: {score1}/{len(checks1)} cost tracking checks")
print(f"  TODO 2: {score2}/{len(queries)} cost analysis queries")
print(f"\n  Files generated in {WORKDIR}/")
