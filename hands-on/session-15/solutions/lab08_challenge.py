"""
Lab 08 Challenge: Complete Monitoring Stack
=============================================
Build a complete Prometheus monitoring setup:
metrics code, scrape config, alerts, and dashboard design.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-08"

print("=" * 60)
print("  Challenge: Complete Monitoring Stack")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Challenge Overview
# ============================================================

print("\n  Build a complete monitoring setup for an AI agent:\n")
print("    1. Python metrics code (prometheus_client)")
print("    2. Prometheus scrape + alert rules")
print("    3. Dashboard panel design with PromQL")
print()
print("    Architecture:")
print("      agent-api:8000/metrics ──scrape──> Prometheus ──> Grafana")
print("                                            │")
print("                                       Alert Rules")
print("                                            │")
print("                                       Alertmanager")
print("                                            │")
print("                                    Slack / PagerDuty")


# ============================================================
# TODO 1: Metrics Code
# ============================================================

print("\n\n--- TODO 1: Python Metrics Code ---\n")

print("  Create a complete metrics module with:")
print("    - Counter: agent_requests_total (labels: endpoint, status)")
print("    - Counter: agent_tokens_total (labels: model, direction)")
print("    - Counter: agent_estimated_cost_usd (labels: model)")
print("    - Histogram: agent_request_duration_seconds (labels: endpoint)")
print("    - Histogram: agent_llm_duration_seconds (labels: model)")
print("    - Gauge: agent_active_requests")
print("    - /metrics endpoint")
print("    - PRICING dict for cost calculation")
print("    - record_llm_call() function")

todo1_code = textwrap.dedent("""\
    from prometheus_client import Counter, Histogram, Gauge, generate_latest
    from fastapi import FastAPI, Response

    app = FastAPI()

    # Counter: total requests by endpoint and status
    REQUEST_COUNT = Counter(
        "agent_requests_total",
        "Total agent requests",
        ["endpoint", "status"]
    )

    # Counter: total tokens by model and direction
    TOKEN_COUNT = Counter(
        "agent_tokens_total",
        "Total tokens consumed",
        ["model", "direction"]
    )

    # Counter: estimated cost in USD by model
    ESTIMATED_COST = Counter(
        "agent_estimated_cost_usd",
        "Estimated cost in USD",
        ["model"]
    )

    # Histogram: request duration_seconds by endpoint
    REQUEST_LATENCY = Histogram(
        "agent_request_duration_seconds",
        "Request duration in seconds",
        ["endpoint"],
        buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    )

    # Histogram: LLM call duration_seconds by model
    LLM_LATENCY = Histogram(
        "agent_llm_duration_seconds",
        "LLM call duration in seconds",
        ["model"],
        buckets=[0.5, 1.0, 2.5, 5.0, 10.0, 30.0]
    )

    # Gauge: currently active requests
    ACTIVE_REQUESTS = Gauge(
        "agent_active_requests",
        "Currently processing requests"
    )

    PRICING = {
        "llama3-70b": {"input": 0.59, "output": 0.79},
        "llama3-8b": {"input": 0.05, "output": 0.08},
        "gpt-4o": {"input": 5.00, "output": 15.00},
    }

    def record_llm_call(model, tokens_in, tokens_out, duration):
        TOKEN_COUNT.labels(model=model, direction="in").inc(tokens_in)
        TOKEN_COUNT.labels(model=model, direction="out").inc(tokens_out)
        prices = PRICING.get(model, {"input": 0, "output": 0})
        cost = (tokens_in * prices["input"] + tokens_out * prices["output"]) / 1_000_000
        ESTIMATED_COST.labels(model=model).inc(cost)
        LLM_LATENCY.labels(model=model).observe(duration)

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type="text/plain")
""")

with open(os.path.join(WORKDIR, "metrics.py"), "w") as f:
    f.write(todo1_code)


# ============================================================
# TODO 2: Alert Rules
# ============================================================

print("\n\n--- TODO 2: Prometheus Alert Rules ---\n")

print("  Create alert rules with:")
print("    1. HighErrorRate: error rate > 5% for 5m (critical)")
print("    2. HighLatency: p99 > 5s for 10m (warning)")
print("    3. AgentDown: up{job='agent-api'} == 0 for 1m (critical)")
print("    4. HighCostRate: cost > $5/hour for 30m (warning)")
print("    5. ChromaDBDown: up{job='chromadb'} == 0 for 1m (critical)")

todo2_yaml = textwrap.dedent("""\
    groups:
    - name: agent-alerts
      rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(agent_requests_total{status=~"5.."}[5m]))
          / sum(rate(agent_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 5% for 5 minutes"
          description: "Current error rate: {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket[5m])) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency above 5 seconds for 10 minutes"
          description: "Current p99 latency: {{ $value }}s"

      - alert: AgentDown
        expr: up{job="agent-api"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Agent API target is down"
          description: "agent-api has been unreachable for more than 1 minute"

      - alert: HighCostRate
        expr: rate(agent_estimated_cost_usd[1h]) * 3600 > 5
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Cost rate exceeds $5/hour for 30 minutes"
          description: "Current cost rate: ${{ $value }}/hour"

      - alert: ChromaDBDown
        expr: up{job="chromadb"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "ChromaDB vector store is down"
          description: "ChromaDB has been unreachable for more than 1 minute"
""")

with open(os.path.join(WORKDIR, "alerting-rules.yaml"), "w") as f:
    f.write(todo2_yaml)


# ============================================================
# TODO 3: Dashboard Design
# ============================================================

print("\n\n--- TODO 3: Dashboard Panel Design ---\n")

print("  Design an AI monitoring dashboard.")
print("  For each panel, specify: title, panel_type, PromQL query.\n")

panels = [
    {
        "title": "Request Rate",
        "panel_type": "stat",
        "promql": "sum(rate(agent_requests_total[5m]))",
        "purpose": "Current request rate (requests/sec)",
        "correct_type": "stat",
        "check_terms": ["rate", "agent_requests_total"],
    },
    {
        "title": "p99 Latency",
        "panel_type": "stat",
        "promql": "histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket[5m]))",
        "purpose": "p99 latency (current value with threshold)",
        "correct_type": "stat",
        "check_terms": ["histogram_quantile", "0.99"],
    },
    {
        "title": "Error Rate",
        "panel_type": "stat",
        "promql": 'sum(rate(agent_requests_total{status=~"5.."}[5m])) / sum(rate(agent_requests_total[5m])) * 100',
        "purpose": "Error rate percentage",
        "correct_type": "stat",
        "check_terms": ["rate", "status", "100"],
    },
    {
        "title": "Request Rate Trend",
        "panel_type": "time series",
        "promql": "sum(rate(agent_requests_total[5m])) by (endpoint)",
        "purpose": "Request rate trend over time",
        "correct_type": "time series",
        "check_terms": ["rate", "agent_requests_total"],
    },
    {
        "title": "Daily Cost by Model",
        "panel_type": "bar chart",
        "promql": "increase(agent_estimated_cost_usd[24h]) by (model)",
        "purpose": "Daily cost by model (comparison)",
        "correct_type": "bar chart",
        "check_terms": ["increase", "cost", "24h"],
    },
    {
        "title": "Token Usage per Hour",
        "panel_type": "stat",
        "promql": "increase(agent_tokens_total[1h])",
        "purpose": "Token usage per hour",
        "correct_type": "stat",
        "check_terms": ["increase", "tokens", "1h"],
    },
]

# Panels filled in above


# ============================================================
# Validation
# ============================================================

print("\n\n--- Challenge Validation ---\n")

results = []

# TODO 1: Metrics code
results.append(("Code: Counter import",            "Counter" in todo1_code))
results.append(("Code: Histogram import",           "Histogram" in todo1_code))
results.append(("Code: Gauge import",               "Gauge" in todo1_code))
results.append(("Code: generate_latest",            "generate_latest" in todo1_code))
results.append(("Code: agent_requests_total",       "agent_requests_total" in todo1_code))
results.append(("Code: agent_tokens_total",         "agent_tokens_total" in todo1_code))
results.append(("Code: agent_estimated_cost_usd",   "agent_estimated_cost_usd" in todo1_code))
results.append(("Code: duration_seconds",           "duration_seconds" in todo1_code))
results.append(("Code: agent_active_requests",      "agent_active_requests" in todo1_code))
results.append(("Code: PRICING dict",               "PRICING" in todo1_code or "pricing" in todo1_code))
results.append(("Code: record function",            "def record" in todo1_code or "def track" in todo1_code))
results.append(("Code: /metrics endpoint",          "/metrics" in todo1_code))

# TODO 2: Alert rules
results.append(("Alert: groups section",            "groups:" in todo2_yaml))
results.append(("Alert: HighErrorRate",             "HighErrorRate" in todo2_yaml))
results.append(("Alert: HighLatency",               "HighLatency" in todo2_yaml))
results.append(("Alert: AgentDown",                 "AgentDown" in todo2_yaml))
results.append(("Alert: HighCostRate",              "HighCostRate" in todo2_yaml))
results.append(("Alert: ChromaDBDown",              "ChromaDBDown" in todo2_yaml))
results.append(("Alert: severity critical",         "critical" in todo2_yaml))
results.append(("Alert: severity warning",          "warning" in todo2_yaml))
results.append(("Alert: has for duration",          "for:" in todo2_yaml))
results.append(("Alert: has annotations",           "annotations:" in todo2_yaml))

# TODO 3: Dashboard panels
for p in panels:
    type_ok = p["panel_type"].strip().lower() == p["correct_type"]
    if p["promql"] == "___":
        promql_ok = False
    else:
        promql_ok = all(t.lower() in p["promql"].lower() for t in p["check_terms"])
    results.append((f"Panel '{p['purpose'][:30]}': type", type_ok))
    results.append((f"Panel '{p['purpose'][:30]}': query", promql_ok))

passed = sum(1 for _, ok in results if ok)
total = len(results)

print(f"  Results: {passed}/{total} checks passed\n")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Challenge Complete ---\n")
print(f"  Score: {passed}/{total} ({passed/total*100:.0f}%)")
print(f"\n  Files created in {WORKDIR}/:")
for root, dirs, files in os.walk(WORKDIR):
    for f in sorted(files):
        rel = os.path.relpath(os.path.join(root, f), WORKDIR)
        size = os.path.getsize(os.path.join(root, f))
        print(f"    {rel:<45} ({size} bytes)")

print(f"\n  Complete monitoring stack:")
print(f"    1. metrics.py — Counter, Histogram, Gauge, cost tracking")
print(f"    2. alerting-rules.yaml — 5 alert rules (errors, latency, cost, down)")
print(f"    3. Dashboard design — 6 panels (RED + AI metrics)")

print("\n" + "=" * 60)
print("Challenge complete!")
print(f"- Metrics: 6 metric definitions + cost tracking")
print(f"- Alerts: 5 rules (HighErrorRate, HighLatency, Down, Cost)")
print(f"- Dashboard: 6 panels with panel types + PromQL")
print(f"- {passed}/{total} validation checks passing")
