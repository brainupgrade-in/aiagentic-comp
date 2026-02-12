"""
Lab 03: Instrumenting LangChain with LangFuse
================================================
Use CallbackHandler to trace LangChain chains and agents.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-11-03"

print("=" * 50)
print("  Lab 03: Instrumenting LangChain with LangFuse")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: CallbackHandler Pattern
# ============================================================

print("\n--- Step 1: CallbackHandler Pattern ---\n")

print("  One-line integration with LangChain:\n")

code_example = textwrap.dedent("""\
    from langfuse.callback import CallbackHandler

    handler = CallbackHandler(
        public_key="pk-lf-...",
        secret_key="sk-lf-...",
        host="http://localhost:3000",
        user_id="alice",
        session_id="chat_42",
        tags=["production", "v2.0"],
    )

    # Pass handler to any LangChain invoke
    result = chain.invoke(
        {"question": "What is RAG?"},
        config={"callbacks": [handler]},
    )
""")

for line in code_example.strip().split("\n"):
    print(f"    {line}")

print("\n  What gets captured automatically:")
captured = [
    ("LLM calls",      "Model, input, output, tokens, cost, latency"),
    ("Tool calls",      "Tool name, input, output, duration"),
    ("Chain execution", "Each chain step with input/output"),
    ("Retriever calls", "Query, retrieved documents, scores"),
]
for what, detail in captured:
    print(f"    {what:<18} {detail}")


# ============================================================
# Step 2: RAG Pipeline Tracing
# ============================================================

print("\n\n--- Step 2: RAG Pipeline Tracing ---\n")

rag_example = textwrap.dedent("""\
    from langchain.chains import RetrievalQA
    from langchain_community.vectorstores import Chroma

    # Set up retriever
    vectorstore = Chroma(persist_directory="./chroma_db")
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    # Create chain
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        chain_type="stuff",
    )

    # Invoke with LangFuse callback
    result = chain.invoke(
        {"query": "How does RAG work?"},
        config={"callbacks": [handler]},
    )
""")

print("  RAG pipeline with LangFuse tracing:\n")
for line in rag_example.strip().split("\n"):
    print(f"    {line}")

print("\n  Trace structure for RAG:")
print("    Trace: chat_request")
print("    ├── Span: retriever")
print("    │   └── (query: 'How does RAG work?', docs: 5)")
print("    └── Span: llm_chain")
print("        └── Generation: groq/llama3-70b")
print("            ├── input_tokens: 1,200")
print("            ├── output_tokens: 350")
print("            └── cost: $0.0062")


# ============================================================
# Step 3: Handler Configuration
# ============================================================

print("\n\n--- Step 3: Handler Configuration ---\n")

print("  Key parameters for CallbackHandler:\n")
params = [
    ("user_id",     "Identifies the user",        "Required for cost-per-user tracking"),
    ("session_id",  "Groups related requests",     "Conversation thread ID"),
    ("tags",        "Categorize traces",           '["production", "v2.0", "experiment"]'),
    ("metadata",    "Custom key-value pairs",      '{"endpoint": "/chat", "model": "llama3"}'),
    ("trace_name",  "Override default trace name",  '"rag_query" or "agent_run"'),
]
print(f"    {'Param':<14} {'Purpose':<30} {'Example'}")
print(f"    {'-'*80}")
for param, purpose, example in params:
    print(f"    {param:<14} {purpose:<30} {example}")


# ============================================================
# TODO 1: Instrument a LangChain app
# ============================================================

print("\n\n--- TODO 1: LangChain Instrumentation Code ---\n")

print("  Write code that:")
print("    - Imports CallbackHandler from langfuse.callback")
print("    - Creates handler with user_id, session_id, tags")
print("    - Creates a RetrievalQA chain with retriever")
print("    - Invokes chain with callbacks=[handler]")
print("    - Gets trace_id from handler\n")

todo1_code = textwrap.dedent("""\
    # TODO: Instrument a LangChain RAG pipeline with LangFuse
    # Include: import, handler creation, chain invocation

""")

with open(os.path.join(WORKDIR, "instrumented_rag.py"), "w") as f:
    f.write(todo1_code)

checks1 = [
    ("Has CallbackHandler import",  "CallbackHandler" in todo1_code),
    ("Has langfuse import",         "langfuse" in todo1_code),
    ("Has handler creation",        "CallbackHandler(" in todo1_code),
    ("Has user_id",                 "user_id" in todo1_code),
    ("Has session_id",              "session_id" in todo1_code),
    ("Has tags",                    "tags" in todo1_code),
    ("Has chain invoke",            "invoke" in todo1_code),
    ("Has callbacks config",        "callbacks" in todo1_code),
    ("Has handler reference",       "handler" in todo1_code),
    ("Has trace_id retrieval",      "trace_id" in todo1_code or "get_trace" in todo1_code),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Integration quiz
# ============================================================

print("\n\n--- TODO 2: Integration Quiz ---\n")

quiz = [
    {
        "question": "What LangFuse class integrates with LangChain?",
        "answer": "___",
        "correct": "callbackhandler",
    },
    {
        "question": "What config key passes the handler to chain.invoke()?",
        "answer": "___",
        "correct": "callbacks",
    },
    {
        "question": "What handler parameter groups requests into conversations?",
        "answer": "___",
        "correct": "session_id",
    },
    {
        "question": "What trace level captures the actual LLM API call?",
        "answer": "___",
        "correct": "generation",
    },
]

# YOUR CODE HERE: Fill in quiz answers

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace("_", "").replace(" ", "")
    correct = q["correct"].lower().replace("_", "").replace(" ", "")
    is_correct = answer == correct

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

print(f"\n\n--- Lab 03 Summary ---\n")
print("  Key concepts:")
print("    1. CallbackHandler = one-line LangChain integration")
print("    2. Pass handler via config={'callbacks': [handler]}")
print("    3. Automatically captures LLM calls, tools, chains, retrievers")
print("    4. Set user_id + session_id for per-user tracking")
print(f"\n  TODO 1: {score1}/{len(checks1)} instrumentation checks")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
