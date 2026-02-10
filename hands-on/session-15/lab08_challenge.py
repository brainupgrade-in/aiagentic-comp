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
    # TODO: Complete metrics module for AI agent
    # Include all metrics, /metrics endpoint, and cost tracking

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
    # TODO: Alert rules for AI monitoring
    # groups with 5 alerts, each having expr, for, labels, annotations

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
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "Current request rate (requests/sec)",
        "correct_type": "stat",
        "check_terms": ["rate", "agent_requests_total"],
    },
    {
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "p99 latency (current value with threshold)",
        "correct_type": "stat",
        "check_terms": ["histogram_quantile", "0.99"],
    },
    {
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "Error rate percentage",
        "correct_type": "stat",
        "check_terms": ["rate", "status", "100"],
    },
    {
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "Request rate trend over time",
        "correct_type": "time series",
        "check_terms": ["rate", "agent_requests_total"],
    },
    {
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "Daily cost by model (comparison)",
        "correct_type": "bar chart",
        "check_terms": ["increase", "cost", "24h"],
    },
    {
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "Token usage per hour",
        "correct_type": "stat",
        "check_terms": ["increase", "tokens", "1h"],
    },
]

# YOUR CODE HERE: Design dashboard panels
# panels[0]["title"] = "Request Rate"
# panels[0]["panel_type"] = "stat"
# panels[0]["promql"] = "sum(rate(agent_requests_total[5m]))"
# ...


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
