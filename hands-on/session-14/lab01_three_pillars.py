"""
Lab 01: Three Pillars of Observability
========================================
Understand Metrics, Logs, and Traces — the three pillars
that give you visibility into your AI applications.
"""

import os
import shutil
WORKDIR = "/tmp/k8s-lab-14-01"

print("=" * 50)
print("  Lab 01: Three Pillars of Observability")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: The Three Pillars
# ============================================================

print("\n--- Step 1: The Three Pillars ---\n")

pillars = [
    ("Metrics",
     "Quantitative measurements over time",
     "Is the system healthy right now?",
     "request rate, error rate, latency, CPU, memory"),
    ("Logs",
     "Discrete timestamped events",
     "What went wrong?",
     "errors, warnings, request details, stack traces"),
    ("Traces",
     "End-to-end request flow across services",
     "Why is this request slow?",
     "service call chain, per-operation timing, bottlenecks"),
]

print(f"  {'Pillar':<10} {'Definition':<40} {'Answers':<30} {'Examples'}")
print(f"  {'-'*110}")
for name, definition, answers, examples in pillars:
    print(f"  {name:<10} {definition:<40} {answers:<30} {examples}")

print("\n  Together these give you FULL visibility into your AI stack.")


# ============================================================
# Step 2: Why AI Apps Need Special Observability
# ============================================================

print("\n\n--- Step 2: Why AI Apps Are Different ---\n")

challenges = [
    ("Non-deterministic",  "Same input can produce different outputs",
     "Track prompt versions, temperature, model responses"),
    ("Multi-step reasoning", "Agent: plan → tool → reflect → retry",
     "Trace each step as a span with timing"),
    ("Cost per request",   "Every LLM call costs money (tokens = $$)",
     "Counter for tokens consumed, cost tracking"),
    ("Variable latency",   "200ms cache hit vs 30s LLM call",
     "Histogram for latency distribution, p50/p99"),
]

print(f"  {'Challenge':<22} {'Why It Matters':<45} {'Observability Solution'}")
print(f"  {'-'*95}")
for challenge, why, solution in challenges:
    print(f"  {challenge:<22} {why:<45} {solution}")


# ============================================================
# Step 3: When to Use Which Pillar
# ============================================================

print("\n\n--- Step 3: When to Use Which Pillar ---\n")

scenarios = [
    ("Dashboard: Is system healthy?",            "Metrics",  "Counters, gauges on Grafana dashboard"),
    ("Alert: Error rate spiked!",                 "Metrics",  "Prometheus alert on rate() > threshold"),
    ("Debug: Why did request X fail?",            "Logs",     "Search logs for request ID / trace ID"),
    ("Debug: Why is this request slow?",          "Traces",   "View span breakdown, find bottleneck"),
    ("Audit: What did the agent do?",             "Logs",     "Structured log with tool_calls, actions"),
    ("Capacity: Are we running out of tokens?",   "Metrics",  "Token counter, cost gauge over time"),
    ("Root cause: Which service is the problem?", "Traces",   "Distributed trace across agent→LLM→DB"),
]

for scenario, pillar, how in scenarios:
    print(f"    {scenario:<48} → {pillar:<8} ({how})")


# ============================================================
# TODO 1: Match scenarios to pillars
# ============================================================

print("\n\n--- TODO 1: Match Scenarios to Pillars ---\n")

print("  For each scenario, write 'metrics', 'logs', or 'traces'.\n")

quiz = [
    {
        "scenario": "You need a Grafana dashboard showing request rate over time",
        "answer": "___",
        "correct": "metrics",
    },
    {
        "scenario": "A user reports a specific request returned wrong results",
        "answer": "___",
        "correct": "logs",
    },
    {
        "scenario": "Agent responses are slower than usual — which service is the bottleneck?",
        "answer": "___",
        "correct": "traces",
    },
    {
        "scenario": "You want to alert when error rate exceeds 5%",
        "answer": "___",
        "correct": "metrics",
    },
    {
        "scenario": "You need to see what tools the agent called for request abc-123",
        "answer": "___",
        "correct": "logs",
    },
    {
        "scenario": "ChromaDB retrieval takes 2s but LLM call takes 15s — find which one",
        "answer": "___",
        "correct": "traces",
    },
]

# YOUR CODE HERE: Fill in the answers
# quiz[0]["answer"] = "metrics"
# quiz[1]["answer"] = ???
# ...

score1 = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].strip().lower() == q["correct"]
    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score1 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['scenario']}")
    if status == "TODO":
        print(f"           (Answer: 'metrics', 'logs', or 'traces')")

print(f"\n  Score: {score1}/{len(quiz)}")


# ============================================================
# TODO 2: AI Observability Design
# ============================================================

print("\n\n--- TODO 2: AI Observability Design ---\n")

print("  For each AI component, identify what to observe and which pillar.\n")

design = [
    {
        "component": "LLM API call",
        "what_to_observe": "___",
        "pillar": "___",
        "correct_what": "latency, tokens, cost, model name",
        "correct_pillar": "metrics",
    },
    {
        "component": "Agent decision (tool selection)",
        "what_to_observe": "___",
        "pillar": "___",
        "correct_what": "which tool was called, reasoning, result",
        "correct_pillar": "logs",
    },
    {
        "component": "RAG retrieval from ChromaDB",
        "what_to_observe": "___",
        "pillar": "___",
        "correct_what": "query time, docs retrieved, relevance scores",
        "correct_pillar": "traces",
    },
    {
        "component": "End-to-end request flow",
        "what_to_observe": "___",
        "pillar": "___",
        "correct_what": "full request path, per-service timing",
        "correct_pillar": "traces",
    },
    {
        "component": "Error tracking across services",
        "what_to_observe": "___",
        "pillar": "___",
        "correct_what": "error count, error rate, status codes",
        "correct_pillar": "metrics",
    },
    {
        "component": "Agent multi-step reasoning",
        "what_to_observe": "___",
        "pillar": "___",
        "correct_what": "step count, tool calls, plan changes",
        "correct_pillar": "logs",
    },
]

score2 = 0
total2 = len(design) * 2  # 2 fields per item
for i, d in enumerate(design, 1):
    pillar_ok = d["pillar"].strip().lower() == d["correct_pillar"]
    what_ok = d["what_to_observe"] != "___" and len(d["what_to_observe"].strip()) > 3

    if d["pillar"] == "___":
        p_status = "TODO"
    elif pillar_ok:
        p_status = "PASS"
        score2 += 1
    else:
        p_status = "FAIL"

    if d["what_to_observe"] == "___":
        w_status = "TODO"
    elif what_ok:
        w_status = "PASS"
        score2 += 1
    else:
        w_status = "FAIL"

    print(f"    {i}. {d['component']}")
    print(f"       [{w_status}] What to observe: {d['what_to_observe']}")
    print(f"       [{p_status}] Primary pillar: {d['pillar']}")

print(f"\n  Score: {score2}/{total2}")

# Save reference
ref = "# Three Pillars of Observability — Quick Reference\n\n"
ref += "| Pillar  | Question It Answers       | AI Use Case                        |\n"
ref += "|---------|---------------------------|------------------------------------|\\n"
ref += "| Metrics | Is system healthy?        | Request rate, token cost, latency  |\n"
ref += "| Logs    | What went wrong?          | Agent decisions, errors, tool calls|\n"
ref += "| Traces  | Why is this request slow? | Service call chain, span timing   |\n"

with open(os.path.join(WORKDIR, "three-pillars-reference.md"), "w") as f:
    f.write(ref)


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 01 Summary ---\n")
print("  Key concepts:")
print("    1. Metrics = quantitative measurements (counters, gauges, histograms)")
print("    2. Logs = discrete events with structured fields (JSON, trace_id)")
print("    3. Traces = end-to-end request path (spans with timing)")
print("    4. AI apps need all three: cost tracking, step tracing, error debugging")
print(f"\n  TODO 1: {score1}/{len(quiz)} scenarios matched")
print(f"  TODO 2: {score2}/{total2} design items completed")
print(f"\n  Files generated in {WORKDIR}/")
