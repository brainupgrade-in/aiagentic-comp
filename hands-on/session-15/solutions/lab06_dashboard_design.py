"""
Lab 06: Dashboard Design
==========================
Design Grafana dashboards using the RED and USE methods
with appropriate panel types for AI monitoring.
"""

import os
import shutil
WORKDIR = "/tmp/k8s-lab-15-06"

print("=" * 50)
print("  Lab 06: Dashboard Design")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: RED and USE Methods
# ============================================================

print("\n--- Step 1: RED and USE Methods ---\n")

print("  RED Method — for request-driven services (agent API):\n")
red = [
    ("Rate",     "How many requests per second?",   "sum(rate(requests_total[5m]))"),
    ("Errors",   "What percentage are failing?",     'sum(rate(requests{status=~"5.."}[5m])) / sum(rate(...))'),
    ("Duration", "How long do requests take?",       "histogram_quantile(0.99, rate(duration_bucket[5m]))"),
]
for signal, question, query in red:
    print(f"    {signal:<10} {question:<35} {query}")

print("\n  USE Method — for infrastructure (nodes, pods):\n")
use = [
    ("Utilization", "How busy is the resource?",    "container_cpu_usage / container_cpu_limit"),
    ("Saturation",  "How much is queued/waiting?",  "container_cpu_cfs_throttled_seconds_total"),
    ("Errors",      "Are there hardware/OS errors?", "node_filesystem_errors_total"),
]
for signal, question, query in use:
    print(f"    {signal:<14} {question:<35} {query}")


# ============================================================
# Step 2: Grafana Panel Types
# ============================================================

print("\n\n--- Step 2: Grafana Panel Types ---\n")

panels = [
    ("Stat",        "Single value with thresholds",     "Current request rate, error %"),
    ("Time Series", "Values over time (line/area)",      "Request rate trend, latency over time"),
    ("Gauge",       "Value against min/max range",       "CPU usage %, memory usage %"),
    ("Bar Chart",   "Compare categories",                "Tokens by model, cost by endpoint"),
    ("Heatmap",     "Distribution over time",            "Latency distribution (histogram)"),
    ("Table",       "Multi-column data",                 "Top endpoints by error rate"),
]

print(f"  {'Panel Type':<14} {'Best For':<35} {'AI Example'}")
print(f"  {'-'*75}")
for name, best, example in panels:
    print(f"  {name:<14} {best:<35} {example}")


# ============================================================
# Step 3: AI Dashboard Layout
# ============================================================

print("\n\n--- Step 3: AI Dashboard Layout ---\n")

print("  Row 1: Service Health (RED Method)")
print("    ┌──────────┬──────────┬──────────┬──────────┐")
print("    │ Request  │ p99      │ Error    │ Active   │")
print("    │ Rate     │ Latency  │ Rate     │ Requests │")
print("    │ 127/s    │ 340ms    │ 0.3%     │ 42       │")
print("    │ [Stat]   │ [Stat]   │ [Stat]   │ [Stat]   │")
print("    └──────────┴──────────┴──────────┴──────────┘")
print("  Row 2: AI Metrics")
print("    ┌──────────┬──────────┬──────────┬──────────┐")
print("    │ Tokens   │ Cost     │ Cache    │ Pods     │")
print("    │ /Hour    │ Today    │ Hit Rate │ Ready    │")
print("    │ 45K      │ $2.47    │ 78%      │ 3/3      │")
print("    │ [Stat]   │ [Stat]   │ [Stat]   │ [Stat]   │")
print("    └──────────┴──────────┴──────────┴──────────┘")
print("  Row 3: Trends (Time Series panels)")
print("    ┌────────────────────┬────────────────────┐")
print("    │ Request Rate       │ Latency (p50/p99)  │")
print("    │ [Time Series]      │ [Time Series]      │")
print("    └────────────────────┴────────────────────┘")
print("  Row 4: Cost Analysis (Bar Chart + Table)")
print("    ┌────────────────────┬────────────────────┐")
print("    │ Cost by Model      │ Top Endpoints      │")
print("    │ [Bar Chart]        │ [Table]            │")
print("    └────────────────────┴────────────────────┘")


# ============================================================
# TODO 1: Design dashboard panels
# ============================================================

print("\n\n--- TODO 1: Design Dashboard Panels ---\n")

print("  For each metric, choose the panel type and write the PromQL.\n")

dashboard = [
    {
        "metric": "Request rate (current value, requests/sec)",
        "panel_type": "stat",
        "promql": "sum(rate(agent_requests_total[5m]))",
        "correct_panel": "stat",
        "check_terms": ["sum", "rate", "agent_requests_total"],
    },
    {
        "metric": "Latency over time (p50 and p99 lines)",
        "panel_type": "time series",
        "promql": "histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket[5m]))",
        "correct_panel": "time series",
        "check_terms": ["histogram_quantile", "rate", "bucket"],
    },
    {
        "metric": "Error rate percentage (with red/green threshold)",
        "panel_type": "stat",
        "promql": 'sum(rate(agent_requests_total{status=~"5.."}[5m])) / sum(rate(agent_requests_total[5m])) * 100',
        "correct_panel": "stat",
        "check_terms": ["rate", "status", "100"],
    },
    {
        "metric": "Cost by model (comparison bars)",
        "panel_type": "bar chart",
        "promql": "increase(agent_estimated_cost_usd[24h]) by (model)",
        "correct_panel": "bar chart",
        "check_terms": ["increase", "cost", "model"],
    },
    {
        "metric": "CPU usage as percentage of limit",
        "panel_type": "gauge",
        "promql": "sum(container_cpu_usage_seconds_total) / sum(container_cpu_limit) * 100",
        "correct_panel": "gauge",
        "check_terms": ["cpu"],
    },
]

# Panels filled in above

score1 = 0
total1 = len(dashboard) * 2  # panel + promql
for i, d in enumerate(dashboard, 1):
    panel_ok = d["panel_type"].strip().lower() == d["correct_panel"]
    if d["promql"] == "___":
        promql_ok = False
    else:
        promql_ok = all(term.lower() in d["promql"].lower() for term in d["check_terms"])

    if d["panel_type"] == "___":
        p_status = "TODO"
    elif panel_ok:
        p_status = "PASS"
        score1 += 1
    else:
        p_status = "FAIL"

    if d["promql"] == "___":
        q_status = "TODO"
    elif promql_ok:
        q_status = "PASS"
        score1 += 1
    else:
        q_status = "FAIL"

    print(f"    {i}. {d['metric']}")
    print(f"       [{p_status}] Panel: {d['panel_type']}")
    print(f"       [{q_status}] PromQL: {d['promql']}")

print(f"\n  Score: {score1}/{total1}")


# ============================================================
# TODO 2: Dashboard design quiz
# ============================================================

print("\n\n--- TODO 2: Dashboard Quiz ---\n")

quiz = [
    {
        "question": "What method should you use for request-driven services? (RED/USE)",
        "answer": "RED",
        "correct": "red",
    },
    {
        "question": "What method should you use for infrastructure resources? (RED/USE)",
        "answer": "USE",
        "correct": "use",
    },
    {
        "question": "What panel type shows a single current value with color thresholds?",
        "answer": "stat",
        "correct": "stat",
    },
    {
        "question": "What panel type is best for showing latency distribution over time?",
        "answer": "heatmap",
        "correct": "heatmap",
    },
]

# Answers filled in above

score2 = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].strip().lower().replace(" ", "") == q["correct"].lower()
    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 06 Summary ---\n")
print("  Key concepts:")
print("    1. RED method for services: Rate, Errors, Duration")
print("    2. USE method for infrastructure: Utilization, Saturation, Errors")
print("    3. Panel types: Stat, Time Series, Gauge, Bar Chart, Heatmap, Table")
print("    4. Dashboard layout: health overview → AI metrics → trends → details")
print(f"\n  TODO 1: {score1}/{total1} dashboard panels designed")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
