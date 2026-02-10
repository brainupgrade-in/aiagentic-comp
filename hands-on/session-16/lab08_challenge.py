"""
Lab 08 Challenge: Complete LangFuse Observability Pipeline
============================================================
Build end-to-end LangFuse integration with LangChain,
Prometheus bridge, dashboard design, and alert rules.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-16-08"

print("=" * 60)
print("  Challenge: Complete LangFuse Observability Pipeline")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Challenge Overview
# ============================================================

print("\n  Build a complete LangFuse observability pipeline:\n")
print("    1. LangChain instrumentation with CallbackHandler")
print("    2. Feedback collection and evaluation")
print("    3. Cost tracking with Prometheus bridge")
print("    4. Dashboard design + alert rules")
print()
print("    Architecture:")
print("      LangChain Agent ──callback──> LangFuse Server ──> PostgreSQL")
print("                                        │")
print("                                   Cost/Token data")
print("                                        │")
print("                                   Prometheus ──> Grafana")
print("                                        │")
print("                                   Alertmanager ──> Slack")


# ============================================================
# TODO 1: Complete Instrumentation Code
# ============================================================

print("\n\n--- TODO 1: Complete Instrumentation Code ---\n")

print("  Write a complete LangFuse instrumentation module with:")
print("    - CallbackHandler from langfuse.callback")
print("    - Langfuse client for scores and prompts")
print("    - Handler with user_id, session_id, tags")
print("    - get_prompt() for runtime prompt fetching")
print("    - score() for user feedback (user_feedback)")
print("    - score() for automated eval (relevance)")
print("    - get_trace_id() for linking feedback")

todo1_code = textwrap.dedent("""\
    # TODO: Complete LangFuse instrumentation module

""")

with open(os.path.join(WORKDIR, "langfuse_instrumentation.py"), "w") as f:
    f.write(todo1_code)


# ============================================================
# TODO 2: Prometheus Bridge
# ============================================================

print("\n\n--- TODO 2: Prometheus Cost Bridge ---\n")

print("  Write code that bridges LangFuse data to Prometheus:")
print("    - Counter: langfuse_llm_cost_usd_total (labels: model, user_id)")
print("    - Counter: langfuse_tokens_total (labels: model, direction)")
print("    - Histogram: langfuse_generation_duration_seconds (labels: model)")
print("    - Counter: langfuse_feedback_total (labels: score_name, value)")
print("    - PRICING dict with at least 3 models")
print("    - record_generation() function")
print("    - generate_latest for /metrics endpoint")

todo2_code = textwrap.dedent("""\
    # TODO: Prometheus bridge for LangFuse metrics

""")

with open(os.path.join(WORKDIR, "prometheus_bridge.py"), "w") as f:
    f.write(todo2_code)


# ============================================================
# TODO 3: Dashboard + Alert Design
# ============================================================

print("\n\n--- TODO 3: Dashboard & Alert Design ---\n")

print("  Design dashboard panels and alert rules.\n")

panels = [
    {
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "Cost per hour by model",
        "correct_type": "bar chart",
        "check_terms": ["increase", "cost", "1h"],
    },
    {
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "LLM latency trend (p99)",
        "correct_type": "time series",
        "check_terms": ["histogram_quantile", "0.99"],
    },
    {
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "Token consumption rate",
        "correct_type": "stat",
        "check_terms": ["rate", "token"],
    },
    {
        "title": "___",
        "panel_type": "___",
        "promql": "___",
        "purpose": "Average user feedback score",
        "correct_type": "stat",
        "check_terms": ["feedback"],
    },
]

# YOUR CODE HERE: Design dashboard panels
# panels[0]["title"] = "Cost per Hour"
# panels[0]["panel_type"] = "bar chart"
# panels[0]["promql"] = "sum by (model) (increase(langfuse_llm_cost_usd_total[1h]))"
# ...

alerts_yaml = textwrap.dedent("""\
    # TODO: Alert rules for LangFuse monitoring
    # Include: CostSpike, HighLLMLatency, LowFeedbackScore

""")

with open(os.path.join(WORKDIR, "langfuse-alerts.yaml"), "w") as f:
    f.write(alerts_yaml)


# ============================================================
# Validation
# ============================================================

print("\n\n--- Challenge Validation ---\n")

results = []

# TODO 1: Instrumentation code
results.append(("Code: CallbackHandler import",  "CallbackHandler" in todo1_code))
results.append(("Code: langfuse import",          "langfuse" in todo1_code))
results.append(("Code: handler creation",         "CallbackHandler(" in todo1_code))
results.append(("Code: user_id",                  "user_id" in todo1_code))
results.append(("Code: session_id",               "session_id" in todo1_code))
results.append(("Code: tags",                     "tags" in todo1_code))
results.append(("Code: get_prompt",               "get_prompt" in todo1_code))
results.append(("Code: score() call",             ".score(" in todo1_code))
results.append(("Code: user_feedback score",      "user_feedback" in todo1_code))
results.append(("Code: relevance score",          "relevance" in todo1_code))
results.append(("Code: get_trace_id",             "get_trace_id" in todo1_code or "trace_id" in todo1_code))

# TODO 2: Prometheus bridge
results.append(("Bridge: Counter import",         "Counter" in todo2_code))
results.append(("Bridge: Histogram import",       "Histogram" in todo2_code))
results.append(("Bridge: cost counter",           "cost" in todo2_code.lower()))
results.append(("Bridge: token counter",          "token" in todo2_code.lower()))
results.append(("Bridge: duration histogram",     "duration" in todo2_code.lower()))
results.append(("Bridge: feedback counter",       "feedback" in todo2_code.lower()))
results.append(("Bridge: PRICING dict",           "PRICING" in todo2_code))
results.append(("Bridge: record function",        "def record" in todo2_code))
results.append(("Bridge: generate_latest",        "generate_latest" in todo2_code or "/metrics" in todo2_code))

# TODO 3: Dashboard panels
for p in panels:
    type_ok = p["panel_type"].strip().lower() == p["correct_type"]
    if p["promql"] == "___":
        promql_ok = False
    else:
        promql_ok = all(t.lower() in p["promql"].lower() for t in p["check_terms"])
    results.append((f"Panel '{p['purpose'][:30]}': type",  type_ok))
    results.append((f"Panel '{p['purpose'][:30]}': query", promql_ok))

# TODO 3: Alert rules
results.append(("Alert: groups section",          "groups:" in alerts_yaml))
results.append(("Alert: CostSpike",               "CostSpike" in alerts_yaml or "cost" in alerts_yaml.lower()))
results.append(("Alert: HighLLMLatency",           "Latency" in alerts_yaml or "latency" in alerts_yaml))
results.append(("Alert: LowFeedbackScore",         "Feedback" in alerts_yaml or "feedback" in alerts_yaml))
results.append(("Alert: severity labels",          "severity" in alerts_yaml))
results.append(("Alert: for duration",             "for:" in alerts_yaml))

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

print(f"\n  Complete LangFuse pipeline:")
print(f"    1. langfuse_instrumentation.py — CallbackHandler + scores + prompts")
print(f"    2. prometheus_bridge.py — Cost/token/latency Prometheus metrics")
print(f"    3. Dashboard — 4 panels with PromQL")
print(f"    4. langfuse-alerts.yaml — Cost, latency, feedback alerts")

print("\n" + "=" * 60)
print("Challenge complete!")
print(f"- Instrumentation: CallbackHandler + feedback + prompt management")
print(f"- Prometheus bridge: Cost, tokens, latency, feedback counters")
print(f"- Dashboard: 4 panels (cost, latency, tokens, feedback)")
print(f"- Alerts: Cost spike, high latency, low feedback")
print(f"- {passed}/{total} validation checks passing")
