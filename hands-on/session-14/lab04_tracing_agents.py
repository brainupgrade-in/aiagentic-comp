"""
Lab 04: Tracing Agent Reasoning
=================================
Trace multi-step agent execution, tool calls,
and identify performance bottlenecks.
"""

import os
import shutil

WORKDIR = "/tmp/k8s-lab-14-04"

print("=" * 50)
print("  Lab 04: Tracing Agent Reasoning")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Agent Trace Structure
# ============================================================

print("\n--- Step 1: Agent Trace Structure ---\n")

print("  A typical agent trace shows the reasoning loop:\n")
print("    Trace: agent_run (user_id=alice, session_id=chat_42)")
print("    │")
print("    ├── Span: agent_step_1")
print("    │   ├── Generation: llama3-70b  (decide action)")
print("    │   │   tokens: 800 in, 50 out  |  latency: 1.2s")
print("    │   └── Span: tool_call (search_docs)")
print("    │       latency: 0.3s  |  results: 5 docs")
print("    │")
print("    ├── Span: agent_step_2")
print("    │   ├── Generation: llama3-70b  (analyze results)")
print("    │   │   tokens: 1500 in, 200 out  |  latency: 2.1s")
print("    │   └── Span: tool_call (calculate)")
print("    │       latency: 0.05s")
print("    │")
print("    └── Span: agent_step_3 (final answer)")
print("        └── Generation: llama3-70b")
print("            tokens: 2000 in, 400 out  |  latency: 3.0s")
print()
print("    Total: 3 LLM calls, 2 tool calls, 6.65s, $0.018")


# ============================================================
# Step 2: Common Agent Issues
# ============================================================

print("\n\n--- Step 2: Common Agent Issues (visible in traces) ---\n")

issues = [
    ("Infinite loop",      "Agent keeps calling tools without converging",
                           "Trace shows 10+ steps with repeating pattern"),
    ("Wrong tool",         "Agent selects incorrect tool for task",
                           "Tool span shows irrelevant tool + wasted tokens"),
    ("High latency",       "One LLM call dominates total time",
                           "Generation span with 3x average duration"),
    ("Token explosion",    "Context grows each step (all history included)",
                           "input_tokens: 800 → 1500 → 3000 → 5000"),
    ("Hallucination",      "Model ignores retrieved docs",
                           "Generation output contradicts retriever results"),
]

print(f"    {'Issue':<18} {'Symptom':<45} {'What Trace Shows'}")
print(f"    {'-'*105}")
for issue, symptom, trace_shows in issues:
    print(f"    {issue:<18} {symptom:<45} {trace_shows}")


# ============================================================
# Step 3: Latency Breakdown
# ============================================================

print("\n\n--- Step 3: Latency Breakdown ---\n")

print("  Typical AI agent latency distribution:\n")
breakdown = [
    ("LLM calls",      70, "████████████████████████████████████"),
    ("Vector search",   15, "███████▌"),
    ("Tool execution",   8, "████"),
    ("Network/other",    7, "███▌"),
]
for component, pct, bar in breakdown:
    print(f"    {component:<16} {pct:>3}%  {bar}")

print("\n  Key insight: LLM calls dominate — optimize prompts & model choice first")


# ============================================================
# TODO 1: Analyze agent trace
# ============================================================

print("\n\n--- TODO 1: Analyze Agent Trace ---\n")

print("  Given the agent trace below, answer the questions.\n")

trace_data = [
    {"step": 1, "action": "LLM decide",    "tool": None,           "tokens_in": 600,  "tokens_out": 40,  "latency_ms": 900,  "cost": 0.0026},
    {"step": 2, "action": "tool_call",      "tool": "search_docs",  "tokens_in": 0,    "tokens_out": 0,   "latency_ms": 250,  "cost": 0.0},
    {"step": 3, "action": "LLM analyze",    "tool": None,           "tokens_in": 1400, "tokens_out": 150, "latency_ms": 1800, "cost": 0.0062},
    {"step": 4, "action": "tool_call",      "tool": "calculator",   "tokens_in": 0,    "tokens_out": 0,   "latency_ms": 30,   "cost": 0.0},
    {"step": 5, "action": "LLM final",      "tool": None,           "tokens_in": 2200, "tokens_out": 350, "latency_ms": 2800, "cost": 0.0102},
]

print(f"    {'Step':<6} {'Action':<16} {'Tool':<14} {'Tokens In':<12} {'Out':<8} {'Latency':<10} {'Cost'}")
print(f"    {'-'*80}")
for t in trace_data:
    tool = t["tool"] or "-"
    print(f"    {t['step']:<6} {t['action']:<16} {tool:<14} {t['tokens_in']:<12} {t['tokens_out']:<8} {t['latency_ms']:<10} ${t['cost']:.4f}")

total_latency = sum(t["latency_ms"] for t in trace_data)
total_cost = sum(t["cost"] for t in trace_data)
total_tokens = sum(t["tokens_in"] + t["tokens_out"] for t in trace_data)
print(f"\n    Total: {total_latency}ms latency, ${total_cost:.4f} cost, {total_tokens} tokens")

analysis = [
    {
        "question": "How many LLM calls (generations) are there?",
        "answer": "___",
        "correct": "3",
    },
    {
        "question": "Which step has the highest latency? (number)",
        "answer": "___",
        "correct": "5",
    },
    {
        "question": "What percentage of total latency is LLM calls? (round to nearest 5%)",
        "answer": "___",
        "correct": "95",
    },
    {
        "question": "Is there a token explosion pattern? (yes/no)",
        "answer": "___",
        "correct": "yes",
    },
    {
        "question": "What is the total cost in dollars? (e.g., 0.019)",
        "answer": "___",
        "correct": "0.019",
    },
]

# YOUR CODE HERE: Fill in the analysis answers

score1 = 0
for i, a in enumerate(analysis, 1):
    is_correct = a["answer"].strip().lower().replace("$", "") == a["correct"]
    if a["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score1 += 1
    else:
        status = "FAIL"
    print(f"\n    [{status}] Q{i}: {a['question']}")
    print(f"            Your answer: {a['answer']}")

print(f"\n  Score: {score1}/{len(analysis)}")


# ============================================================
# TODO 2: Debug scenarios quiz
# ============================================================

print("\n\n--- TODO 2: Agent Debugging Quiz ---\n")

quiz = [
    {
        "question": "An agent makes 15 tool calls before answering. What issue is this?",
        "answer": "___",
        "correct": "infinite loop",
        "check": "loop",
    },
    {
        "question": "input_tokens grows from 500→1500→4000→8000. What's the pattern?",
        "answer": "___",
        "correct": "token explosion",
        "check": "token",
    },
    {
        "question": "Agent calls 'search_weather' when asked about stock prices. What issue?",
        "answer": "___",
        "correct": "wrong tool",
        "check": "wrong",
    },
    {
        "question": "What LangFuse level captures the exact LLM prompt and response?",
        "answer": "___",
        "correct": "generation",
        "check": "generation",
    },
]

# YOUR CODE HERE: Fill in quiz answers

score2 = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"] != "___" and q["check"] in q["answer"].strip().lower()
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

print(f"\n\n--- Lab 04 Summary ---\n")
print("  Key concepts:")
print("    1. Agent traces show reasoning loop: decide → tool → analyze → repeat")
print("    2. Common issues: infinite loops, wrong tools, token explosion")
print("    3. LLM calls dominate latency (~70%+ of total time)")
print("    4. Trace analysis reveals optimization opportunities")
print(f"\n  TODO 1: {score1}/{len(analysis)} trace analysis")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
