"""
Lab 04: Distributed Traces
============================
Understand trace/span hierarchy, parent-child relationships,
and how to trace AI agent workflows.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-04"

print("=" * 50)
print("  Lab 04: Distributed Traces")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Trace and Span Concepts
# ============================================================

print("\n--- Step 1: Trace and Span Concepts ---\n")

print("  Trace = end-to-end journey of a single request")
print("  Span  = one operation within that journey")
print("  Spans have parent-child relationships:\n")

print("  Trace: abc-123")
print("    Span: API Gateway (480ms)")
print("    └── Span: Agent Workflow (420ms)")
print("        ├── Span: RAG Retrieval (45ms)")
print("        │   └── Span: ChromaDB Query (38ms)")
print("        ├── Span: LLM Call #1 (280ms)")
print("        └── Span: LLM Call #2 (85ms)")
print()
print("  Each span has:")
print("    - trace_id: shared across ALL spans in one request")
print("    - span_id: unique to THIS span")
print("    - parent_span_id: which span started this one")
print("    - name: what operation this represents")
print("    - duration: how long it took")
print("    - attributes: key-value metadata")


# ============================================================
# Step 2: Trace Visualization
# ============================================================

print("\n\n--- Step 2: Trace Visualization ---\n")

print("  Timeline view (Jaeger/Tempo style):\n")

spans = [
    ("API Gateway",     0,   480, 0),
    ("Agent Workflow",  10,  420, 1),
    ("RAG Retrieval",   20,   45, 2),
    ("ChromaDB Query",  25,   38, 3),
    ("LLM Call #1",     70,  280, 2),
    ("LLM Call #2",    355,   85, 2),
]

print(f"  {'Span':<20} {'Start':<8} {'Duration':<12} {'Timeline (each = = 20ms)'}")
print(f"  {'-'*85}")
for name, start, duration, depth in spans:
    indent = "  " * depth
    bar_start = start // 20
    bar_len = max(1, duration // 20)
    timeline = "." * bar_start + "#" * bar_len
    print(f"  {indent}{name:<{20-len(indent)}} {start:>4}ms   {duration:>4}ms      {timeline}")


# ============================================================
# Step 3: AI Agent Trace Patterns
# ============================================================

print("\n\n--- Step 3: AI Agent Trace Patterns ---\n")

print("  AI agents create complex traces with multiple patterns:\n")

patterns = [
    ("Sequential",  "RAG → LLM → Response",
     "Simple Q&A: retrieve context then generate answer"),
    ("Parallel",    "Tool1 + Tool2 → LLM",
     "Agent calls multiple tools simultaneously"),
    ("Iterative",   "LLM → Tool → LLM → Tool → LLM",
     "Agent reasoning loop (ReAct pattern)"),
    ("Nested",      "Agent → Sub-agent → Tools",
     "Multi-agent systems with delegation"),
]

for name, flow, example in patterns:
    print(f"    {name:<12} {flow:<30} {example}")


# ============================================================
# Step 4: Span Attributes for AI
# ============================================================

print("\n\n--- Step 4: AI Span Attributes ---\n")

print("  Standard attributes to add to AI spans:\n")

attributes = [
    ("llm.model",           "string",  '"groq/llama3-70b"',    "LLM spans"),
    ("llm.tokens_in",       "int",     "850",                   "LLM spans"),
    ("llm.tokens_out",      "int",     "420",                   "LLM spans"),
    ("llm.cost_usd",        "float",   "0.0038",                "LLM spans"),
    ("rag.docs_retrieved",  "int",     "5",                     "RAG spans"),
    ("rag.collection",      "string",  '"knowledge_base"',      "RAG spans"),
    ("agent.tools_used",    "int",     "3",                     "Workflow spans"),
    ("agent.steps",         "int",     "4",                     "Workflow spans"),
]

print(f"  {'Attribute':<24} {'Type':<8} {'Example':<20} {'Added to'}")
print(f"  {'-'*70}")
for attr, typ, example, added_to in attributes:
    print(f"  {attr:<24} {typ:<8} {example:<20} {added_to}")


# ============================================================
# TODO 1: Design a trace hierarchy
# ============================================================

print("\n\n--- TODO 1: Design a Trace Hierarchy ---\n")

print("  Given this AI workflow, design the trace spans:\n")
print("    1. User sends chat message to /chat endpoint")
print("    2. Agent API receives request")
print("    3. Agent retrieves context from ChromaDB (45ms)")
print("    4. Agent calls LLM with context (1200ms)")
print("    5. LLM decides to call web_search tool (350ms)")
print("    6. Agent calls LLM again with search results (800ms)")
print("    7. Response returned to user")
print()
print("  Fill in the span hierarchy below.")
print("  Format: (span_name, parent_span, duration_ms)\n")

trace_design = [
    ("___", None,  "___"),   # Root span (the whole request)
    ("___", "___", "___"),   # RAG retrieval
    ("___", "___", "___"),   # First LLM call
    ("___", "___", "___"),   # Tool: web_search
    ("___", "___", "___"),   # Second LLM call
]

# YOUR CODE HERE: Fill in the span hierarchy
# trace_design[0] = ("chat_request", None, "2400")
# trace_design[1] = ("rag_retrieval", "chat_request", "45")
# trace_design[2] = ("llm_call_1", "chat_request", "1200")
# trace_design[3] = ("web_search", "chat_request", "350")
# trace_design[4] = ("llm_call_2", "chat_request", "800")

score1 = 0
total1 = len(trace_design)
for i, (name, parent, duration) in enumerate(trace_design):
    has_name = name != "___" and len(name.strip()) > 2
    has_dur = duration != "___" and str(duration).strip().isdigit()
    if has_name and has_dur:
        score1 += 1
        status = "PASS"
    elif name == "___":
        status = "TODO"
    else:
        status = "FAIL"

    parent_str = f"parent={parent}" if parent else "ROOT"
    dur_str = f"{duration}ms" if duration != "___" else "___ms"
    print(f"    [{status}] Span {i+1}: {name} ({parent_str}, {dur_str})")

print(f"\n  Score: {score1}/{total1}")


# ============================================================
# TODO 2: Trace analysis quiz
# ============================================================

print("\n\n--- TODO 2: Trace Concepts Quiz ---\n")

quiz = [
    {
        "question": "What ID is shared across ALL spans in one request?",
        "answer": "___",
        "correct": "trace_id",
    },
    {
        "question": "What links a child span to its parent?",
        "answer": "___",
        "correct": "parent_span_id",
    },
    {
        "question": "If LLM call takes 1200ms and total request is 1500ms, what % is LLM?",
        "answer": "___",
        "correct": "80",
    },
    {
        "question": "Which AI trace pattern describes: LLM → Tool → LLM → Tool → LLM?",
        "answer": "___",
        "correct": "iterative",
    },
    {
        "question": "What tool visualizes distributed traces? (Jaeger/Tempo/Zipkin)",
        "answer": "___",
        "correct_options": ["jaeger", "tempo", "zipkin"],
    },
]

# YOUR CODE HERE: Fill in the answers
# quiz[0]["answer"] = "trace_id"
# ...

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace("_", "")
    if "correct_options" in q:
        is_correct = answer in [opt.lower() for opt in q["correct_options"]]
    else:
        is_correct = answer == q["correct"].lower().replace("_", "")

    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")

print(f"\n  Score: {score2}/{len(quiz)}")

# Save reference
ref = textwrap.dedent("""\
    # Distributed Traces Reference

    ## Key Concepts
    - Trace: End-to-end request journey (shared trace_id)
    - Span: Single operation (unique span_id, references parent_span_id)
    - Attributes: Key-value metadata on spans

    ## AI Span Attributes
    - llm.model, llm.tokens_in, llm.tokens_out, llm.cost_usd
    - rag.docs_retrieved, rag.collection
    - agent.tools_used, agent.steps

    ## AI Trace Patterns
    - Sequential: RAG → LLM → Response
    - Parallel: Tool1 + Tool2 → LLM
    - Iterative: LLM → Tool → LLM → Tool (ReAct)
    - Nested: Agent → Sub-agent → Tools
""")

with open(os.path.join(WORKDIR, "traces-reference.md"), "w") as f:
    f.write(ref)


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 04 Summary ---\n")
print("  Key concepts:")
print("    1. Traces track end-to-end request flow across services")
print("    2. Spans are individual operations with parent-child relationships")
print("    3. trace_id is shared, span_id is unique, parent_span_id links hierarchy")
print("    4. AI agents create complex traces: sequential, parallel, iterative, nested")
print(f"\n  TODO 1: {score1}/{total1} spans designed")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
