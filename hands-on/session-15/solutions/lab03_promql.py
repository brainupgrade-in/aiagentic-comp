"""
Lab 03: PromQL Queries
=======================
Master essential PromQL functions: rate, sum,
histogram_quantile, and alert expressions.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-03"

print("=" * 50)
print("  Lab 03: PromQL Queries")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Essential PromQL Functions
# ============================================================

print("\n--- Step 1: Essential PromQL Functions ---\n")

functions = [
    ("rate(counter[5m])",
     "Per-second rate of a counter over 5 minutes",
     "rate(agent_requests_total[5m])"),
    ("increase(counter[1h])",
     "Total increase of a counter over 1 hour",
     "increase(agent_tokens_total[1h])"),
    ("sum(metric)",
     "Aggregate across all label combinations",
     "sum(rate(agent_requests_total[5m]))"),
    ("avg(metric)",
     "Average across instances",
     "avg(agent_active_requests)"),
    ("histogram_quantile(q, hist)",
     "Percentile from histogram buckets",
     "histogram_quantile(0.99, rate(bucket[5m]))"),
    ("absent(metric)",
     "Returns 1 if metric is missing (target down)",
     "absent(up{job='agent-api'})"),
]

for func, desc, example in functions:
    print(f"  {func}")
    print(f"    {desc}")
    print(f"    Example: {example}\n")


# ============================================================
# Step 2: PromQL Simulation
# ============================================================

print("\n--- Step 2: PromQL Simulation ---\n")

print("  Simulating rate() on a counter:\n")

# Simulate counter values over 5 minutes
counter_values = [
    ("09:00", 1000),
    ("09:01", 1012),
    ("09:02", 1025),
    ("09:03", 1041),
    ("09:04", 1058),
    ("09:05", 1080),
]

print(f"  {'Time':<8} {'Counter':<12} {'Increase':<12} {'rate() (req/s)'}")
print(f"  {'-'*48}")
prev = counter_values[0][1]
for time, value in counter_values:
    increase = value - prev
    rate = increase / 60 if increase > 0 else 0
    print(f"  {time:<8} {value:<12} +{increase:<11} {rate:.3f}")
    prev = value

total_increase = counter_values[-1][1] - counter_values[0][1]
avg_rate = total_increase / (5 * 60)
print(f"\n  rate(counter[5m]) = {total_increase} / 300s = {avg_rate:.3f} req/s")
print(f"  increase(counter[5m]) = {total_increase}")


# ============================================================
# Step 3: Common Query Patterns
# ============================================================

print("\n\n--- Step 3: Common Query Patterns ---\n")

patterns = [
    ("Request rate",
     "sum(rate(agent_requests_total[5m]))"),
    ("Error rate %",
     'sum(rate(agent_requests_total{status=~"5.."}[5m])) / sum(rate(agent_requests_total[5m])) * 100'),
    ("p99 latency",
     "histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket[5m]))"),
    ("p50 latency",
     "histogram_quantile(0.50, rate(agent_request_duration_seconds_bucket[5m]))"),
    ("Tokens per hour",
     "increase(agent_tokens_total[1h])"),
    ("Cost per request",
     "sum(rate(agent_estimated_cost_usd[1h])) / sum(rate(agent_requests_total[1h]))"),
    ("Target down",
     'absent(up{job="agent-api"})'),
]

for name, query in patterns:
    print(f"  {name}:")
    print(f"    {query}\n")


# ============================================================
# TODO 1: Write PromQL queries
# ============================================================

print("\n--- TODO 1: Write PromQL Queries ---\n")

print("  Write the PromQL query for each scenario.\n")

queries = [
    {
        "scenario": "Total request rate across all endpoints (req/s)",
        "query": "sum(rate(agent_requests_total[5m]))",
        "correct": "sum(rate(agent_requests_total[5m]))",
        "check_terms": ["sum", "rate", "agent_requests_total", "5m"],
    },
    {
        "scenario": "Error rate as a percentage (5xx status codes)",
        "query": 'sum(rate(agent_requests_total{status=~"5.."}[5m])) / sum(rate(agent_requests_total[5m])) * 100',
        "correct": 'sum(rate(agent_requests_total{status=~"5.."}[5m])) / sum(rate(agent_requests_total[5m])) * 100',
        "check_terms": ["rate", "status", "5", "100"],
    },
    {
        "scenario": "p99 request latency from histogram",
        "query": "histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket[5m]))",
        "correct": "histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket[5m]))",
        "check_terms": ["histogram_quantile", "0.99", "bucket"],
    },
    {
        "scenario": "Total tokens consumed in the last hour",
        "query": "increase(agent_tokens_total[1h])",
        "correct": "increase(agent_tokens_total[1h])",
        "check_terms": ["increase", "agent_tokens_total", "1h"],
    },
    {
        "scenario": "Detect if the agent-api target is down",
        "query": 'absent(up{job="agent-api"})',
        "correct": 'absent(up{job="agent-api"})',
        "check_terms": ["absent", "up", "agent-api"],
    },
]

# Queries filled in above

score1 = 0
for i, q in enumerate(queries, 1):
    if q["query"] == "___":
        status = "TODO"
    else:
        matches = all(term.lower() in q["query"].lower() for term in q["check_terms"])
        if matches:
            status = "PASS"
            score1 += 1
        else:
            status = "FAIL"
    print(f"    [{status}] {q['scenario']}")
    if q["query"] != "___":
        print(f"           {q['query']}")

print(f"\n  Score: {score1}/{len(queries)}")


# ============================================================
# TODO 2: PromQL concepts quiz
# ============================================================

print("\n\n--- TODO 2: PromQL Quiz ---\n")

quiz = [
    {
        "question": "What function calculates per-second rate of a counter?",
        "answer": "rate",
        "correct": "rate",
    },
    {
        "question": "What function gives you the 99th percentile from a histogram?",
        "answer": "histogram_quantile",
        "correct": "histogram_quantile",
    },
    {
        "question": "Why can't you use rate() directly on a gauge?",
        "answer": "rate() is for counters; gauges already show current value",
        "correct": "gauges",
        "hint": "rate() is for counters; gauges already show current value",
    },
    {
        "question": "What does [5m] mean in rate(counter[5m])?",
        "answer": "range vector selector - look back 5 minutes",
        "correct": "range",
        "hint": "It's a range vector selector — look back 5 minutes",
    },
]

# Answers filled in above

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace("_", "").replace(" ", "")
    correct = q["correct"].lower().replace("_", "").replace(" ", "")
    is_correct = correct in answer

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
ref = textwrap.dedent("""\
    # PromQL Quick Reference

    ## Functions
    | Function | Purpose | Example |
    |----------|---------|---------|
    | rate()   | Per-second rate of counter | rate(requests_total[5m]) |
    | increase() | Total increase over time | increase(tokens_total[1h]) |
    | sum()    | Aggregate across labels | sum(rate(requests[5m])) |
    | histogram_quantile() | Percentile | histogram_quantile(0.99, rate(bucket[5m])) |
    | absent() | Detect missing metric | absent(up{job="api"}) |

    ## Common Patterns
    - Request rate: sum(rate(requests_total[5m]))
    - Error rate %: sum(rate(requests{status=~"5.."}[5m])) / sum(rate(requests[5m])) * 100
    - p99 latency: histogram_quantile(0.99, rate(duration_bucket[5m]))
""")

with open(os.path.join(WORKDIR, "promql-reference.md"), "w") as f:
    f.write(ref)


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 03 Summary ---\n")
print("  Key concepts:")
print("    1. rate() on counters, histogram_quantile() on histograms")
print("    2. sum() aggregates, absent() detects down targets")
print("    3. Error rate = errors / total * 100")
print("    4. [5m] is a range vector — look back 5 minutes")
print(f"\n  TODO 1: {score1}/{len(queries)} queries written")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
