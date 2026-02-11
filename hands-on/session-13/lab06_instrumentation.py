"""
Lab 06: Instrumentation
========================
Learn auto vs manual instrumentation, and how to create
custom spans for AI-specific logic.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-06"

print("=" * 50)
print("  Lab 06: Instrumentation")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Auto vs Manual Instrumentation
# ============================================================

print("\n--- Step 1: Auto vs Manual Instrumentation ---\n")

comparison = [
    ("Feature",        "Auto-instrumentation",               "Manual instrumentation"),
    ("Code changes",   "Zero — inject at startup",            "Add spans in your code"),
    ("Coverage",       "HTTP, DB, cache frameworks",          "Business logic, AI workflows"),
    ("Granularity",    "Framework-level (request, query)",    "Operation-level (LLM call, RAG)"),
    ("Setup",          "pip install + instrument command",    "tracer.start_as_current_span()"),
    ("Best for",       "Getting started quickly",             "AI-specific observability"),
]

print(f"  {'Feature':<18} {'Auto':<38} {'Manual'}")
print(f"  {'-'*90}")
for row in comparison[1:]:
    print(f"  {row[0]:<18} {row[1]:<38} {row[2]}")

print("\n  Best practice: Use BOTH together!")
print("    Auto = framework (FastAPI, Redis, requests)")
print("    Manual = business logic (agent steps, LLM calls, RAG)")


# ============================================================
# Step 2: Auto-Instrumentation Examples
# ============================================================

print("\n\n--- Step 2: Auto-Instrumentation ---\n")

print("  Option A — Code-based (add to your app):\n")
code_a = textwrap.dedent("""\
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.instrumentation.redis import RedisInstrumentor

    app = FastAPI()
    FastAPIInstrumentor.instrument_app(app)
    RequestsInstrumentor().instrument()
    RedisInstrumentor().instrument()
""")
for line in code_a.strip().split("\n"):
    print(f"    {line}")

print("\n  Option B — Zero-code (command-line):\n")
print("    opentelemetry-instrument \\")
print("      --service_name agent-api \\")
print("      --exporter_otlp_endpoint http://otel-collector:4317 \\")
print("      python -m uvicorn main:app --host 0.0.0.0 --port 8000")


# ============================================================
# Step 3: Manual Spans for AI Logic
# ============================================================

print("\n\n--- Step 3: Manual Spans for AI ---\n")

print("  Creating custom spans for AI operations:\n")

manual_code = textwrap.dedent("""\
    from opentelemetry import trace
    tracer = trace.get_tracer("agent.core")

    async def process_query(query: str):
        with tracer.start_as_current_span("agent_workflow") as span:
            span.set_attribute("agent.query", query)

            # RAG retrieval span
            with tracer.start_as_current_span("rag_retrieval") as rag_span:
                docs = await chromadb.query(query, n_results=5)
                rag_span.set_attribute("rag.docs_retrieved", len(docs))
                rag_span.set_attribute("rag.collection", "knowledge_base")

            # LLM call span
            with tracer.start_as_current_span("llm_call") as llm_span:
                response = await llm.invoke(query, context=docs)
                llm_span.set_attribute("llm.model", "groq/llama3-70b")
                llm_span.set_attribute("llm.tokens_in", response.usage.prompt_tokens)
                llm_span.set_attribute("llm.tokens_out", response.usage.completion_tokens)

            return response.content
""")
for line in manual_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# Step 4: What Gets Auto-Instrumented
# ============================================================

print("\n\n--- Step 4: Auto-Instrumented Libraries ---\n")

libs = [
    ("fastapi",     "HTTP requests/responses",   "Method, path, status code, duration"),
    ("requests",    "Outbound HTTP calls",        "URL, method, status, duration"),
    ("httpx",       "Async HTTP calls",           "URL, method, status, duration"),
    ("redis",       "Redis commands",             "Command, key, duration"),
    ("sqlalchemy",  "Database queries",           "Query, db type, duration"),
    ("logging",     "Log entries",                "Injects trace_id, span_id"),
]

print(f"  {'Library':<14} {'What It Traces':<28} {'Attributes Added'}")
print(f"  {'-'*75}")
for lib, what, attrs in libs:
    print(f"  {lib:<14} {what:<28} {attrs}")


# ============================================================
# TODO 1: Write instrumentation code
# ============================================================

print("\n\n--- TODO 1: Write Instrumentation Code ---\n")

print("  Create a Python file that sets up OTel for an AI agent:")
print("    1. Import and configure TracerProvider with Resource")
print("    2. Add BatchSpanProcessor with OTLPSpanExporter")
print("    3. Auto-instrument FastAPI")
print("    4. Create a tracer named 'agent.core'")
print("    5. Write a function with manual spans for RAG + LLM\n")

todo1_code = textwrap.dedent("""\
    # TODO: Complete OTel setup for AI agent
    # 1. TracerProvider with Resource (service.name = agent-api)
    # 2. BatchSpanProcessor + OTLPSpanExporter
    # 3. Auto-instrument FastAPI
    # 4. Create tracer
    # 5. Function with manual spans

""")

with open(os.path.join(WORKDIR, "otel_setup.py"), "w") as f:
    f.write(todo1_code)

code_checks = [
    ("Has TracerProvider",          "TracerProvider" in todo1_code),
    ("Has Resource",                "Resource" in todo1_code),
    ("Has service.name",            "service.name" in todo1_code),
    ("Has BatchSpanProcessor",      "BatchSpanProcessor" in todo1_code),
    ("Has OTLPSpanExporter",        "OTLPSpanExporter" in todo1_code),
    ("Has FastAPIInstrumentor",     "FastAPIInstrumentor" in todo1_code),
    ("Has get_tracer",              "get_tracer" in todo1_code),
    ("Has start_as_current_span",   "start_as_current_span" in todo1_code),
    ("Has set_attribute",           "set_attribute" in todo1_code),
    ("Has rag span",                "rag" in todo1_code.lower() and "span" in todo1_code.lower()),
]

score1 = sum(1 for _, ok in code_checks if ok)
print(f"  Validating Code ({score1}/{len(code_checks)}):\n")
for name, ok in code_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Instrumentation quiz
# ============================================================

print("\n\n--- TODO 2: Instrumentation Quiz ---\n")

quiz = [
    {
        "question": "Should you use auto, manual, or both instrumentation?",
        "answer": "___",
        "correct": "both",
    },
    {
        "question": "What Python method creates a new span?",
        "answer": "___",
        "correct": "start_as_current_span",
    },
    {
        "question": "What does BatchSpanProcessor do vs SimpleSpanProcessor?",
        "answer": "___",
        "correct": "batches",
        "hint": "Batches spans for efficient export (fewer network calls)",
    },
    {
        "question": "What OTel env var sets the service name without code changes?",
        "answer": "___",
        "correct": "OTEL_SERVICE_NAME",
    },
]

# YOUR CODE HERE: Fill in the answers

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace("_", "").replace(" ", "")
    correct = q["correct"].lower().replace("_", "").replace(" ", "")
    is_correct = correct in answer or answer == correct

    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")
    if status == "TODO" and "hint" in q:
        print(f"           Hint: {q['hint']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 06 Summary ---\n")
print("  Key concepts:")
print("    1. Auto-instrumentation: zero-code coverage for frameworks")
print("    2. Manual instrumentation: custom spans for AI business logic")
print("    3. Best practice: use BOTH together")
print("    4. set_attribute() adds AI-specific metadata to spans")
print(f"\n  TODO 1: {score1}/{len(code_checks)} code checks passed")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
