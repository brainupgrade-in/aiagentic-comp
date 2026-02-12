"""
Lab 07: Cost & Token Analysis
================================
Track token usage, calculate costs per model/user,
and design cost monitoring dashboards.
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
    ("Over time",      "Is cost trending up or down?",      "Daily: $15 → $12 after optimization"),
]
print(f"    {'View':<16} {'Question':<40} {'Example'}")
print(f"    {'-'*95}")
for view, question, example in views:
    print(f"    {view:<16} {question:<40} {example}")


# ============================================================
# Step 3: Exporting to Prometheus
# ============================================================

print("\n\n--- Step 3: Exporting Costs to Prometheus ---\n")

print("  Bridge LangFuse traces to Prometheus for alerting:\n")

bridge_code = textwrap.dedent("""\
    from prometheus_client import Counter, Histogram

    # Prometheus metrics for LangFuse data
    llm_cost = Counter(
        "langfuse_llm_cost_usd_total",
        "Total LLM cost in USD",
        ["model", "user_id"],
    )
    llm_tokens = Counter(
        "langfuse_tokens_total",
        "Total tokens consumed",
        ["model", "direction"],  # direction: input/output
    )
    llm_latency = Histogram(
        "langfuse_generation_duration_seconds",
        "LLM generation latency",
        ["model"],
    )

    # After each LLM call, update Prometheus
    def record_generation(model, tokens_in, tokens_out, cost, latency):
        llm_cost.labels(model=model, user_id=user_id).inc(cost)
        llm_tokens.labels(model=model, direction="input").inc(tokens_in)
        llm_tokens.labels(model=model, direction="output").inc(tokens_out)
        llm_latency.labels(model=model).observe(latency)
""")

for line in bridge_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# TODO 1: Cost tracking code
# ============================================================

print("\n\n--- TODO 1: Cost Tracking Code ---\n")

print("  Write code that:")
print("    - Defines a PRICING dict (model → input_per_1m, output_per_1m)")
print("    - Has a calculate_cost(model, tokens_in, tokens_out) function")
print("    - Creates Prometheus Counter for cost tracking")
print("    - Creates Prometheus Counter for token tracking")
print("    - Exports metrics via /metrics endpoint\n")

todo1_code = textwrap.dedent("""\
    # TODO: Cost tracking with PRICING dict and Prometheus export

""")

with open(os.path.join(WORKDIR, "cost_tracker.py"), "w") as f:
    f.write(todo1_code)

checks1 = [
    ("Has PRICING dict",           "PRICING" in todo1_code),
    ("Has model pricing entry",    "gpt-4" in todo1_code.lower() or "llama" in todo1_code.lower()),
    ("Has calculate_cost function", "def calculate" in todo1_code or "def calc" in todo1_code),
    ("Has 1_000_000 or 1000000",   "1_000_000" in todo1_code or "1000000" in todo1_code),
    ("Has Counter import",         "Counter" in todo1_code),
    ("Has cost counter",           "cost" in todo1_code.lower() and "Counter(" in todo1_code),
    ("Has token counter",          "token" in todo1_code.lower() and "Counter(" in todo1_code),
    ("Has model label",            "model" in todo1_code),
    ("Has generate_latest",        "generate_latest" in todo1_code or "/metrics" in todo1_code),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Cost dashboard queries
# ============================================================

print("\n\n--- TODO 2: Cost Dashboard PromQL ---\n")

print("  Write PromQL queries for cost monitoring panels:\n")

queries = [
    {
        "purpose": "Total cost per hour by model",
        "promql": "___",
        "check_terms": ["increase", "cost", "1h"],
    },
    {
        "purpose": "Token consumption rate (tokens/sec) by model",
        "promql": "___",
        "check_terms": ["rate", "token"],
    },
    {
        "purpose": "Average cost per request",
        "promql": "___",
        "check_terms": ["cost", "request"],
    },
    {
        "purpose": "Alert: cost exceeds $5/hour",
        "promql": "___",
        "check_terms": ["increase", "cost", "5"],
    },
]

# YOUR CODE HERE: Fill in PromQL queries

score2 = 0
for i, q in enumerate(queries, 1):
    if q["promql"] == "___":
        status = "TODO"
    elif all(t.lower() in q["promql"].lower() for t in q["check_terms"]):
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] {i}. {q['purpose']}")
    print(f"           PromQL: {q['promql']}")

print(f"\n  Score: {score2}/{len(queries)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 07 Summary ---\n")
print("  Key concepts:")
print("    1. LangFuse auto-calculates cost from model + tokens")
print("    2. Cost views: by model, user, conversation, prompt version, time")
print("    3. Bridge to Prometheus: Counter for cost/tokens, Histogram for latency")
print("    4. Alert on cost spikes with PromQL (increase > threshold)")
print(f"\n  TODO 1: {score1}/{len(checks1)} cost tracking checks")
print(f"  TODO 2: {score2}/{len(queries)} dashboard queries")
print(f"\n  Files generated in {WORKDIR}/")
