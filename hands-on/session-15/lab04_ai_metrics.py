"""
Lab 04: AI-Specific Metrics
==============================
Track tokens, cost, and LLM performance
with Prometheus metrics.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-04"

print("=" * 50)
print("  Lab 04: AI-Specific Metrics")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: AI Metrics Categories
# ============================================================

print("\n--- Step 1: AI Metrics Categories ---\n")

categories = [
    ("Request Metrics",
     ["agent_requests_total (counter)", "agent_request_duration_seconds (histogram)",
      "agent_active_requests (gauge)", "agent_errors_total (counter)"]),
    ("LLM Metrics",
     ["agent_tokens_total{direction=in/out} (counter)",
      "agent_llm_duration_seconds (histogram)",
      "agent_llm_calls_total{model} (counter)",
      "agent_estimated_cost_usd{model} (counter)"]),
    ("RAG Metrics",
     ["agent_rag_duration_seconds (histogram)",
      "agent_rag_docs_retrieved (histogram)",
      "agent_rag_cache_hits_total (counter)",
      "agent_rag_cache_misses_total (counter)"]),
    ("Infrastructure Metrics",
     ["container_cpu_usage_seconds_total", "container_memory_usage_bytes",
      "kube_pod_status_ready", "kube_deployment_status_replicas"]),
]

for name, metrics in categories:
    print(f"  {name}:")
    for m in metrics:
        print(f"    - {m}")
    print()


# ============================================================
# Step 2: Token & Cost Tracking
# ============================================================

print("\n--- Step 2: Token & Cost Tracking ---\n")

print("  LLM pricing (per 1M tokens):\n")

pricing = [
    ("llama3-70b",   0.59, 0.79),
    ("llama3-8b",    0.05, 0.08),
    ("mixtral-8x7b", 0.24, 0.24),
    ("gpt-4o",       5.00, 15.00),
    ("claude-sonnet", 3.00, 15.00),
]

print(f"  {'Model':<18} {'Input ($/1M)':<15} {'Output ($/1M)'}")
print(f"  {'-'*48}")
for model, inp, out in pricing:
    print(f"  {model:<18} ${inp:<14.2f} ${out:.2f}")

print("\n  Cost tracking code:")
cost_code = textwrap.dedent("""\
    ESTIMATED_COST = Counter("agent_estimated_cost_usd", "Cost in USD", ["model"])
    PRICING = {"llama3-70b": {"input": 0.59, "output": 0.79}}

    def record_cost(model, prompt_tokens, completion_tokens):
        prices = PRICING.get(model, {"input": 0, "output": 0})
        cost = (prompt_tokens * prices["input"]
              + completion_tokens * prices["output"]) / 1_000_000
        ESTIMATED_COST.labels(model=model).inc(cost)
""")
for line in cost_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# Step 3: Cost Simulation
# ============================================================

print("\n\n--- Step 3: Cost Simulation ---\n")

requests_data = [
    ("09:00", "llama3-70b",  850, 420),
    ("09:05", "llama3-70b",  1200, 350),
    ("09:10", "llama3-8b",   500, 200),
    ("09:15", "llama3-70b",  900, 500),
    ("09:20", "gpt-4o",      600, 300),
    ("09:25", "llama3-70b",  1100, 450),
    ("09:30", "llama3-8b",   400, 180),
    ("09:35", "llama3-70b",  950, 380),
]

pricing_dict = {m: {"input": i, "output": o} for m, i, o in pricing}
total_cost = 0
total_tokens = 0

print(f"  {'Time':<8} {'Model':<18} {'Tokens':<12} {'Cost'}")
print(f"  {'-'*50}")
for time, model, tok_in, tok_out in requests_data:
    prices = pricing_dict.get(model, {"input": 0, "output": 0})
    cost = (tok_in * prices["input"] + tok_out * prices["output"]) / 1_000_000
    total_cost += cost
    total_tokens += tok_in + tok_out
    print(f"  {time:<8} {model:<18} {tok_in+tok_out:<12} ${cost:.6f}")

print(f"\n  Total tokens: {total_tokens}")
print(f"  Total cost: ${total_cost:.4f}")
print(f"  Avg cost/request: ${total_cost/len(requests_data):.6f}")


# ============================================================
# TODO 1: Design cost tracking metrics
# ============================================================

print("\n\n--- TODO 1: Cost Tracking Code ---\n")

print("  Create a complete cost-tracking module:")
print("    - Counter: agent_tokens_total (labels: model, direction)")
print("    - Counter: agent_estimated_cost_usd (labels: model)")
print("    - Histogram: agent_llm_duration_seconds (labels: model)")
print("    - Function: record_llm_call(model, tokens_in, tokens_out, duration)")
print("      that updates all three metrics")
print("    - Include PRICING dict for at least 3 models")

todo1_code = textwrap.dedent("""\
    # TODO: Complete cost tracking module
    # Define metrics and record_llm_call function

""")

with open(os.path.join(WORKDIR, "cost_tracking.py"), "w") as f:
    f.write(todo1_code)

code_checks = [
    ("Has agent_tokens_total",      "agent_tokens_total" in todo1_code),
    ("Has agent_estimated_cost_usd", "agent_estimated_cost_usd" in todo1_code),
    ("Has duration_seconds",        "duration_seconds" in todo1_code),
    ("Has Counter",                 "Counter" in todo1_code),
    ("Has Histogram",               "Histogram" in todo1_code),
    ("Has PRICING dict",            "PRICING" in todo1_code or "pricing" in todo1_code),
    ("Has record function",         "def record" in todo1_code or "def track" in todo1_code),
    ("Has model label",             "model" in todo1_code),
    ("Has direction label",         "direction" in todo1_code),
    ("Has 1_000_000 division",      "1000000" in todo1_code.replace("_", "") or "1e6" in todo1_code),
]

score1 = sum(1 for _, ok in code_checks if ok)
print(f"\n  Validating Code ({score1}/{len(code_checks)}):\n")
for name, ok in code_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: PromQL for AI metrics
# ============================================================

print("\n\n--- TODO 2: AI Metric Queries ---\n")

print("  Write PromQL queries for these AI scenarios.\n")

ai_queries = [
    {
        "scenario": "Daily cost by model",
        "query": "___",
        "check_terms": ["increase", "agent_estimated_cost_usd", "24h"],
    },
    {
        "scenario": "Token consumption per hour",
        "query": "___",
        "check_terms": ["increase", "agent_tokens_total", "1h"],
    },
    {
        "scenario": "Average cost per request",
        "query": "___",
        "check_terms": ["rate", "cost", "rate", "requests"],
    },
    {
        "scenario": "LLM p99 latency",
        "query": "___",
        "check_terms": ["histogram_quantile", "0.99", "llm"],
    },
]

# YOUR CODE HERE: Fill in the queries

score2 = 0
for i, q in enumerate(ai_queries, 1):
    if q["query"] == "___":
        status = "TODO"
    else:
        matches = all(term.lower() in q["query"].lower() for term in q["check_terms"])
        if matches:
            status = "PASS"
            score2 += 1
        else:
            status = "FAIL"
    print(f"    [{status}] {q['scenario']}")
    if q["query"] != "___":
        print(f"           {q['query']}")

print(f"\n  Score: {score2}/{len(ai_queries)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 04 Summary ---\n")
print("  Key concepts:")
print("    1. Track tokens (in/out), cost (per model), and LLM latency")
print("    2. Cost = (prompt_tokens * input_price + completion_tokens * output_price) / 1M")
print("    3. Use Counters for totals, Histograms for durations")
print("    4. PromQL: increase() for totals over time, rate() for per-second")
print(f"\n  TODO 1: {score1}/{len(code_checks)} code checks passed")
print(f"  TODO 2: {score2}/{len(ai_queries)} queries written")
print(f"\n  Files generated in {WORKDIR}/")
