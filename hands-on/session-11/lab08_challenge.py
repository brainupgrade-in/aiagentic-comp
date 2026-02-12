"""
Lab 08 Challenge: Complete LangFuse Observability Pipeline
============================================================
Build end-to-end LangFuse integration with LangChain,
dashboard configuration, score definitions, and alert rules.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-11-08"

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
print("    3. Cost tracking with LangFuse native API")
print("    4. LangFuse dashboard config + score-based alerts")
print()
print("    Architecture:")
print("      LangChain Agent --callback--> LangFuse Server --> PostgreSQL")
print("                                        |")
print("                                   Traces / Scores / Cost")
print("                                        |")
print("                                   LangFuse Dashboard")
print("                                        |")
print("                                   Score Alerts --> Webhook/Slack")


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
# TODO 2: Cost Tracking Module
# ============================================================

print("\n\n--- TODO 2: LangFuse Cost Tracking Module ---\n")

print("  Write code that tracks costs using LangFuse native API:")
print("    - PRICING dict with at least 3 models")
print("    - calculate_cost(model, tokens_in, tokens_out) function")
print("    - Log generation with usage and cost to LangFuse")
print("    - fetch_traces() to retrieve cost data")
print("    - Aggregate cost by model and by user")
print("    - Identify expensive traces (threshold detection)")

todo2_code = textwrap.dedent("""\
    # TODO: LangFuse cost tracking module

""")

with open(os.path.join(WORKDIR, "cost_tracking.py"), "w") as f:
    f.write(todo2_code)


# ============================================================
# TODO 3: Dashboard + Alert Design
# ============================================================

print("\n\n--- TODO 3: Dashboard & Alert Design ---\n")

print("  Design LangFuse dashboard views and alert configurations.\n")

dashboard_views = [
    {
        "title": "___",
        "view_type": "___",
        "filter_config": "___",
        "purpose": "Cost breakdown by model over time",
        "correct_type": "trace list",
        "check_terms": ["model", "cost", "time"],
    },
    {
        "title": "___",
        "view_type": "___",
        "filter_config": "___",
        "purpose": "Generation latency distribution",
        "correct_type": "generation list",
        "check_terms": ["latency", "generation", "model"],
    },
    {
        "title": "___",
        "view_type": "___",
        "filter_config": "___",
        "purpose": "Token usage by user",
        "correct_type": "trace list",
        "check_terms": ["user", "token", "usage"],
    },
    {
        "title": "___",
        "view_type": "___",
        "filter_config": "___",
        "purpose": "User feedback score trends",
        "correct_type": "score list",
        "check_terms": ["feedback", "score", "time"],
    },
]

# YOUR CODE HERE: Design LangFuse dashboard views
# dashboard_views[0]["title"] = "Model Cost Breakdown"
# dashboard_views[0]["view_type"] = "trace list"
# dashboard_views[0]["filter_config"] = "group_by=model, sort_by=cost, time_range=24h"
# ...

score_definitions = textwrap.dedent("""\
    # TODO: Define LangFuse scores for quality monitoring
    # Include: user_feedback, relevance, cost_efficiency

""")

alert_config = textwrap.dedent("""\
    # TODO: LangFuse alert configuration (JSON format)
    # Include: CostSpike, LowFeedback, HighLatency alerts

""")

with open(os.path.join(WORKDIR, "score_definitions.py"), "w") as f:
    f.write(score_definitions)

with open(os.path.join(WORKDIR, "langfuse_alerts.json"), "w") as f:
    f.write(alert_config)


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

# TODO 2: Cost tracking
results.append(("Cost: Langfuse import",          "Langfuse" in todo2_code or "langfuse" in todo2_code))
results.append(("Cost: PRICING dict",             "PRICING" in todo2_code))
results.append(("Cost: calculate_cost function",  "def calculate" in todo2_code or "def calc" in todo2_code))
results.append(("Cost: trace creation",           ".trace(" in todo2_code or "trace(" in todo2_code))
results.append(("Cost: generation logging",       ".generation(" in todo2_code or "generation(" in todo2_code))
results.append(("Cost: usage tracking",           "usage" in todo2_code))
results.append(("Cost: fetch_traces",             "fetch_traces" in todo2_code))
results.append(("Cost: total_cost",               "total_cost" in todo2_code))
results.append(("Cost: model aggregation",        "model" in todo2_code.lower()))

# TODO 3: Dashboard views
for dv in dashboard_views:
    type_ok = dv["view_type"].strip().lower() == dv["correct_type"]
    if dv["filter_config"] == "___":
        config_ok = False
    else:
        config_ok = all(t.lower() in dv["filter_config"].lower() for t in dv["check_terms"])
    results.append((f"View '{dv['purpose'][:30]}': type",    type_ok))
    results.append((f"View '{dv['purpose'][:30]}': config",  config_ok))

# TODO 3: Score definitions
results.append(("Scores: user_feedback defined",   "user_feedback" in score_definitions))
results.append(("Scores: relevance defined",       "relevance" in score_definitions))
results.append(("Scores: cost_efficiency defined", "cost_efficiency" in score_definitions or "cost" in score_definitions))
results.append(("Scores: data_type specified",     "data_type" in score_definitions or "numeric" in score_definitions or "categorical" in score_definitions))

# TODO 3: Alert config
results.append(("Alert: CostSpike rule",           "cost" in alert_config.lower()))
results.append(("Alert: LowFeedback rule",         "feedback" in alert_config.lower()))
results.append(("Alert: HighLatency rule",         "latency" in alert_config.lower()))
results.append(("Alert: threshold value",          "threshold" in alert_config.lower()))
results.append(("Alert: webhook or channel",       "webhook" in alert_config.lower() or "channel" in alert_config.lower()))

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
print(f"    1. langfuse_instrumentation.py -- CallbackHandler + scores + prompts")
print(f"    2. cost_tracking.py -- LangFuse-native cost/token tracking")
print(f"    3. Dashboard -- 4 views with filters and grouping")
print(f"    4. langfuse_alerts.json -- Cost, latency, feedback alerts")

print("\n" + "=" * 60)
print("Challenge complete!")
print(f"- Instrumentation: CallbackHandler + feedback + prompt management")
print(f"- Cost tracking: PRICING dict, generation logging, fetch_traces analysis")
print(f"- Dashboard: 4 LangFuse views (cost, latency, tokens, feedback)")
print(f"- Alerts: Cost spike, low feedback, high latency via LangFuse")
print(f"- {passed}/{total} validation checks passing")
