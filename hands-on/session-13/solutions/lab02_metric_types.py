"""
Lab 02: Metric Types
=====================
Learn the four metric types: Counter, Gauge, Histogram, Summary
and when to use each for AI applications.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-02"

print("=" * 50)
print("  Lab 02: Metric Types")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: The Four Metric Types
# ============================================================

print("\n--- Step 1: The Four Metric Types ---\n")

types = [
    ("Counter",   "Only goes UP (monotonically increasing)",
     "total requests, total tokens, total errors",
     "rate(counter[5m]) gives per-second rate"),
    ("Gauge",     "Goes UP and DOWN",
     "active connections, memory usage, queue depth",
     "Direct value — no rate() needed"),
    ("Histogram",  "Distribution of values in BUCKETS",
     "request latency, response size, token count per request",
     "histogram_quantile(0.99, ...) for percentiles"),
    ("Summary",   "Pre-calculated quantiles (client-side)",
     "Similar to histogram but less flexible",
     "Cannot aggregate across instances"),
]

print(f"  {'Type':<12} {'Behavior':<38} {'Examples':<48} {'PromQL Note'}")
print(f"  {'-'*130}")
for name, behavior, examples, promql in types:
    print(f"  {name:<12} {behavior:<38} {examples:<48} {promql}")


# ============================================================
# Step 2: Counter Simulation
# ============================================================

print("\n\n--- Step 2: Counter Simulation ---\n")

print("  Counters only go UP. They reset to 0 on restart.\n")

class CounterSim:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def inc(self, amount=1):
        self.value += amount
        return self.value

requests = CounterSim("agent_requests_total")
tokens = CounterSim("agent_tokens_total")

events = [
    ("09:00", "chat request",  1, 850),
    ("09:01", "chat request",  1, 1200),
    ("09:02", "health check",  1, 0),
    ("09:03", "chat request",  1, 920),
    ("09:05", "chat request",  1, 1500),
]

print(f"  {'Time':<8} {'Event':<18} {'requests_total':<18} {'tokens_total'}")
print(f"  {'-'*55}")
for time, event, req_inc, tok_inc in events:
    requests.inc(req_inc)
    tokens.inc(tok_inc)
    print(f"  {time:<8} {event:<18} {requests.value:<18} {tokens.value}")

print(f"\n  Note: rate(agent_requests_total[5m]) = {len(events)/(5*60):.4f} req/sec")
print(f"  Note: increase(agent_tokens_total[5m]) = {tokens.value} tokens")


# ============================================================
# Step 3: Gauge vs Counter
# ============================================================

print("\n\n--- Step 3: Gauge vs Counter ---\n")

print("  Gauges go UP and DOWN — they represent current state.\n")

class GaugeSim:
    def __init__(self, name):
        self.name = name
        self.value = 0

    def set(self, val):
        self.value = val
        return self.value

    def inc(self):
        self.value += 1
        return self.value

    def dec(self):
        self.value -= 1
        return self.value

active = GaugeSim("agent_active_requests")
gauge_events = [
    ("09:00", "request starts",  "inc"),
    ("09:00", "request starts",  "inc"),
    ("09:01", "request finishes", "dec"),
    ("09:01", "request starts",  "inc"),
    ("09:02", "request starts",  "inc"),
    ("09:02", "request finishes", "dec"),
    ("09:03", "request finishes", "dec"),
    ("09:03", "request finishes", "dec"),
]

print(f"  {'Time':<8} {'Event':<22} {'active_requests'}")
print(f"  {'-'*40}")
for time, event, action in gauge_events:
    if action == "inc":
        active.inc()
    else:
        active.dec()
    print(f"  {time:<8} {event:<22} {active.value}")


# ============================================================
# Step 4: Histogram — Latency Distribution
# ============================================================

print("\n\n--- Step 4: Histogram (Latency Buckets) ---\n")

print("  Histograms count how many values fall into each bucket.\n")

buckets = [0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, float('inf')]
bucket_counts = {b: 0 for b in buckets}

latencies = [0.05, 0.12, 0.23, 0.45, 0.8, 1.2, 0.3, 0.15, 3.5, 0.9,
             0.08, 0.55, 2.1, 0.35, 0.18, 7.2, 0.42, 0.95, 0.28, 0.6]

for lat in latencies:
    for b in buckets:
        if lat <= b:
            bucket_counts[b] += 1

print(f"  Sample latencies: {len(latencies)} requests")
print(f"  Min: {min(latencies):.2f}s  Max: {max(latencies):.2f}s  Avg: {sum(latencies)/len(latencies):.2f}s\n")

print(f"  {'Bucket (le)':<15} {'Count':<10} {'Visualization'}")
print(f"  {'-'*55}")
for b in buckets:
    label = f"le={b}" if b != float('inf') else "le=+Inf"
    bar = "#" * bucket_counts[b]
    print(f"  {label:<15} {bucket_counts[b]:<10} {bar}")

print(f"\n  p50 ~ 0.45s, p90 ~ 2.1s, p99 ~ 7.2s")
print(f"  PromQL: histogram_quantile(0.99, rate(duration_bucket[5m]))")


# ============================================================
# TODO 1: Classify metrics by type
# ============================================================

print("\n\n--- TODO 1: Classify Metrics by Type ---\n")

print("  For each metric, write 'counter', 'gauge', or 'histogram'.\n")

metrics_quiz = [
    {
        "metric": "agent_requests_total",
        "description": "Total number of requests received",
        "answer": "___",
        "correct": "counter",
    },
    {
        "metric": "agent_active_connections",
        "description": "Current number of active connections",
        "answer": "___",
        "correct": "gauge",
    },
    {
        "metric": "agent_request_duration_seconds",
        "description": "Request latency distribution in buckets",
        "answer": "___",
        "correct": "histogram",
    },
    {
        "metric": "agent_tokens_total",
        "description": "Total tokens consumed (only increases)",
        "answer": "___",
        "correct": "counter",
    },
    {
        "metric": "agent_memory_usage_bytes",
        "description": "Current memory usage of the agent process",
        "answer": "___",
        "correct": "gauge",
    },
    {
        "metric": "agent_llm_call_duration_seconds",
        "description": "Distribution of LLM call durations",
        "answer": "___",
        "correct": "histogram",
    },
    {
        "metric": "agent_errors_total",
        "description": "Total number of errors (only goes up)",
        "answer": "___",
        "correct": "counter",
    },
    {
        "metric": "agent_queue_depth",
        "description": "Current number of items waiting in queue",
        "answer": "___",
        "correct": "gauge",
    },
]

# YOUR CODE HERE: Fill in the answers
metrics_quiz[0]["answer"] = "counter"
metrics_quiz[1]["answer"] = "gauge"
metrics_quiz[2]["answer"] = "histogram"
metrics_quiz[3]["answer"] = "counter"
metrics_quiz[4]["answer"] = "gauge"
metrics_quiz[5]["answer"] = "histogram"
metrics_quiz[6]["answer"] = "counter"
metrics_quiz[7]["answer"] = "gauge"

score1 = 0
for i, q in enumerate(metrics_quiz, 1):
    is_correct = q["answer"].strip().lower() == q["correct"]
    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score1 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] {q['metric']}: {q['description']}")

print(f"\n  Score: {score1}/{len(metrics_quiz)}")


# ============================================================
# TODO 2: Design AI Metrics
# ============================================================

print("\n\n--- TODO 2: Design AI Metrics ---\n")

print("  Define metrics for an AI agent application.")
print("  For each, provide: name, type, and labels.\n")

ai_metrics = [
    {
        "purpose": "Track total LLM API calls",
        "name": "___",
        "type": "___",
        "labels": "___",
        "correct_name": "llm_calls_total",
        "correct_type": "counter",
        "correct_labels": "model, endpoint",
    },
    {
        "purpose": "Track LLM response latency distribution",
        "name": "___",
        "type": "___",
        "labels": "___",
        "correct_name": "llm_response_duration_seconds",
        "correct_type": "histogram",
        "correct_labels": "model",
    },
    {
        "purpose": "Track currently active agent workflows",
        "name": "___",
        "type": "___",
        "labels": "___",
        "correct_name": "agent_active_workflows",
        "correct_type": "gauge",
        "correct_labels": "workflow_type",
    },
    {
        "purpose": "Track estimated cost in USD",
        "name": "___",
        "type": "___",
        "labels": "___",
        "correct_name": "agent_estimated_cost_usd",
        "correct_type": "counter",
        "correct_labels": "model",
    },
]

# YOUR CODE HERE: Fill in the metric definitions
ai_metrics[0]["name"] = "llm_calls_total"
ai_metrics[0]["type"] = "counter"
ai_metrics[0]["labels"] = "model, endpoint"
ai_metrics[1]["name"] = "llm_response_duration_seconds"
ai_metrics[1]["type"] = "histogram"
ai_metrics[1]["labels"] = "model"
ai_metrics[2]["name"] = "agent_active_workflows"
ai_metrics[2]["type"] = "gauge"
ai_metrics[2]["labels"] = "workflow_type"
ai_metrics[3]["name"] = "agent_estimated_cost_usd"
ai_metrics[3]["type"] = "counter"
ai_metrics[3]["labels"] = "model"

score2 = 0
total2 = len(ai_metrics) * 2  # name + type (labels are flexible)
for i, m in enumerate(ai_metrics, 1):
    type_ok = m["type"].strip().lower() == m["correct_type"]
    name_ok = m["name"] != "___" and len(m["name"].strip()) > 3

    if m["type"] == "___":
        t_status = "TODO"
    elif type_ok:
        t_status = "PASS"
        score2 += 1
    else:
        t_status = "FAIL"

    if m["name"] == "___":
        n_status = "TODO"
    elif name_ok:
        n_status = "PASS"
        score2 += 1
    else:
        n_status = "FAIL"

    print(f"    {i}. {m['purpose']}")
    print(f"       [{n_status}] Name: {m['name']}")
    print(f"       [{t_status}] Type: {m['type']}")
    print(f"       Labels: {m['labels']}")

print(f"\n  Score: {score2}/{total2}")

# Save reference
ref = textwrap.dedent("""\
    # Metric Types Reference

    | Type      | Behavior           | Use For                    | PromQL             |
    |-----------|--------------------|----------------------------|--------------------|
    | Counter   | Only goes up       | Totals (requests, tokens)  | rate(), increase() |
    | Gauge     | Goes up and down   | Current state (connections)| Direct value       |
    | Histogram | Buckets + sum/count| Distributions (latency)    | histogram_quantile |
    | Summary   | Pre-calc quantiles | Distributions (client-side)| Cannot aggregate   |
""")

with open(os.path.join(WORKDIR, "metric-types-reference.md"), "w") as f:
    f.write(ref)


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 02 Summary ---\n")
print("  Key concepts:")
print("    1. Counter: monotonically increasing (requests, tokens, errors)")
print("    2. Gauge: goes up and down (active connections, memory, queue depth)")
print("    3. Histogram: distribution in buckets (latency percentiles)")
print("    4. Use rate() on counters, direct value for gauges, histogram_quantile for histograms")
print(f"\n  TODO 1: {score1}/{len(metrics_quiz)} metrics classified")
print(f"  TODO 2: {score2}/{total2} AI metrics designed")
print(f"\n  Files generated in {WORKDIR}/")
