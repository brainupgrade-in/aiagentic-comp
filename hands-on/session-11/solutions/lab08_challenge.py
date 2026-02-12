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

# SOLUTION: Complete LangFuse instrumentation module
todo1_code = textwrap.dedent("""\
    from langfuse import Langfuse
    from langfuse.callback import CallbackHandler
    from langchain_core.prompts import ChatPromptTemplate
    from langchain.chains import RetrievalQA

    # Initialize LangFuse client
    langfuse = Langfuse()

    # Fetch prompt from LangFuse prompt management
    prompt = langfuse.get_prompt("rag_system_prompt", label="production")

    # Build ChatPromptTemplate with fetched prompt
    template = ChatPromptTemplate.from_messages([
        ("system", prompt.prompt),
        ("human", "{question}"),
    ])

    # Create CallbackHandler with user tracking
    handler = CallbackHandler(
        user_id="alice",
        session_id="chat_session_42",
        tags=["production", "v2.0", "rag"],
        metadata={"prompt_version": "v2", "endpoint": "/chat"},
    )

    # Invoke chain with LangFuse callbacks
    result = chain.invoke(
        {"query": "What is RAG?"},
        config={"callbacks": [handler]},
    )

    # Get trace ID for linking feedback
    trace_id = handler.get_trace_id()

    # Submit user feedback score
    langfuse.score(
        trace_id=trace_id,
        name="user_feedback",
        value=1,
        comment="Helpful and accurate response",
    )

    # Submit automated relevance evaluation score
    langfuse.score(
        trace_id=trace_id,
        name="relevance",
        value=0.92,
        comment="High keyword overlap with question",
    )
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

# SOLUTION: LangFuse cost tracking module
todo2_code = textwrap.dedent("""\
    from langfuse import Langfuse

    # Initialize LangFuse client
    langfuse = Langfuse()

    # Pricing dictionary: model -> (input_cost_per_1M, output_cost_per_1M)
    PRICING = {
        "gpt-4-turbo":       (10.00, 30.00),
        "gpt-3.5-turbo":     (0.50, 1.50),
        "groq/llama3-70b":   (0.59, 0.79),
        "groq/llama3-8b":    (0.05, 0.08),
    }

    def calculate_cost(model, tokens_in, tokens_out):
        if model not in PRICING:
            return 0.0
        input_price, output_price = PRICING[model]
        return (tokens_in / 1_000_000) * input_price + (tokens_out / 1_000_000) * output_price

    # Create a trace and log generation with usage and cost
    trace = langfuse.trace(name="cost_tracked_request", user_id="alice")

    tokens_in, tokens_out = 500, 200
    model_name = "groq/llama3-70b"
    cost = calculate_cost(model_name, tokens_in, tokens_out)

    generation = trace.generation(
        name="llm_call",
        model=model_name,
        input=[{"role": "user", "content": "Explain RAG"}],
        output={"role": "assistant", "content": "RAG stands for..."},
        usage={"input": tokens_in, "output": tokens_out, "total_cost": cost},
    )

    # Fetch traces and aggregate cost by model
    traces = langfuse.fetch_traces()
    cost_by_model = {}
    for t in traces.data:
        if t.total_cost:
            for obs in (t.observations or []):
                model = getattr(obs, "model", "unknown")
                cost_by_model[model] = cost_by_model.get(model, 0) + (t.total_cost or 0)

    # Aggregate cost by user
    cost_by_user = {}
    for t in traces.data:
        user = t.user_id or "anonymous"
        cost_by_user[user] = cost_by_user.get(user, 0) + (t.total_cost or 0)

    # Identify expensive traces (threshold detection)
    threshold = 0.01
    expensive_traces = [t for t in traces.data if (t.total_cost or 0) > threshold]
    for t in expensive_traces:
        print(f"Expensive trace: {t.name} total_cost=${t.total_cost:.6f}")
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

# SOLUTION: Design LangFuse dashboard views
dashboard_views[0]["title"] = "Model Cost Breakdown"
dashboard_views[0]["view_type"] = "trace list"
dashboard_views[0]["filter_config"] = "group_by=model, sort_by=cost, time_range=24h"

dashboard_views[1]["title"] = "Generation Latency Distribution"
dashboard_views[1]["view_type"] = "generation list"
dashboard_views[1]["filter_config"] = "sort_by=latency, group_by=generation model, time_range=1h"

dashboard_views[2]["title"] = "Token Usage by User"
dashboard_views[2]["view_type"] = "trace list"
dashboard_views[2]["filter_config"] = "group_by=user, sort_by=token usage, time_range=24h"

dashboard_views[3]["title"] = "Feedback Score Trends"
dashboard_views[3]["view_type"] = "score list"
dashboard_views[3]["filter_config"] = "filter=user_feedback score, sort_by=time, group_by=name"

# SOLUTION: Define LangFuse scores for quality monitoring
score_definitions = textwrap.dedent("""\
    from langfuse import Langfuse

    langfuse = Langfuse()

    # Score definition: user_feedback
    # data_type: numeric (0 or 1 for thumbs down/up)
    # Used to track user satisfaction per response
    langfuse.score(
        trace_id=trace_id,
        name="user_feedback",
        value=1,
        data_type="NUMERIC",
        comment="User rated response as helpful",
    )

    # Score definition: relevance
    # data_type: numeric (0.0 to 1.0 continuous)
    # Automated eval measuring answer relevance to question
    langfuse.score(
        trace_id=trace_id,
        name="relevance",
        value=0.92,
        data_type="NUMERIC",
        comment="Cosine similarity between question and answer",
    )

    # Score definition: cost_efficiency
    # data_type: numeric (cost in USD per quality point)
    # Tracks cost relative to quality — lower is better
    langfuse.score(
        trace_id=trace_id,
        name="cost_efficiency",
        value=0.005,
        data_type="NUMERIC",
        comment="Cost per quality point: $0.005",
    )

    # Score definition: response_category
    # data_type: categorical
    # Classifies response type for analysis
    langfuse.score(
        trace_id=trace_id,
        name="response_category",
        value="factual",
        data_type="CATEGORICAL",
        comment="Response classified as factual answer",
    )
""")

# SOLUTION: LangFuse alert configuration
alert_config = textwrap.dedent("""\
    {
        "alerts": [
            {
                "name": "CostSpike",
                "description": "Alert when hourly LLM cost exceeds threshold",
                "condition": "total_cost per hour > threshold",
                "threshold": 5.00,
                "window": "1h",
                "channel": "slack",
                "webhook": "https://hooks.slack.com/services/T.../B.../xxx",
                "severity": "warning"
            },
            {
                "name": "LowFeedback",
                "description": "Alert when average user feedback drops below threshold",
                "condition": "avg(user_feedback) < threshold over window",
                "threshold": 0.5,
                "window": "30m",
                "channel": "slack",
                "webhook": "https://hooks.slack.com/services/T.../B.../xxx",
                "severity": "critical"
            },
            {
                "name": "HighLatency",
                "description": "Alert when p95 generation latency exceeds threshold",
                "condition": "p95(generation_duration) > threshold",
                "threshold": 10.0,
                "window": "5m",
                "channel": "slack",
                "webhook": "https://hooks.slack.com/services/T.../B.../xxx",
                "severity": "warning"
            }
        ]
    }
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
