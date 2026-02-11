"""
Lab 06: Prompt Management & A/B Testing
==========================================
Version-control prompts in LangFuse, fetch at runtime,
and compare prompt versions.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-16-06"

print("=" * 50)
print("  Lab 06: Prompt Management & A/B Testing")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Why Prompt Management?
# ============================================================

print("\n--- Step 1: Why Prompt Management? ---\n")

print("  Problems with hardcoded prompts:\n")
problems = [
    ("No version history",   "Can't roll back to a working prompt"),
    ("No A/B testing",       "Can't compare two prompt versions"),
    ("Deploy to change",     "Code deploy needed for prompt tweaks"),
    ("No audit trail",       "Who changed the prompt and when?"),
]
for problem, impact in problems:
    print(f"    {problem:<22} → {impact}")

print("\n  LangFuse prompt management solves all of these:")
benefits = [
    ("Version control",      "Every edit creates a new version"),
    ("Runtime fetching",     "Change prompts without code deploy"),
    ("Labels",               "Mark versions as 'production' or 'staging'"),
    ("A/B comparison",       "Compare metrics between versions"),
]
for benefit, detail in benefits:
    print(f"    {benefit:<22} → {detail}")


# ============================================================
# Step 2: Prompt Lifecycle
# ============================================================

print("\n\n--- Step 2: Prompt Lifecycle ---\n")

print("  1. Create prompt in LangFuse UI or API")
print("     Name: 'rag_system_prompt'")
print("     Version 1: 'You are a helpful assistant...'")
print()
print("  2. Fetch at runtime:")

fetch_code = textwrap.dedent("""\
    from langfuse import Langfuse

    langfuse = Langfuse()

    # Fetch latest production version
    prompt = langfuse.get_prompt("rag_system_prompt")

    # Or fetch specific label
    prompt = langfuse.get_prompt("rag_system_prompt", label="production")

    # Use in LangChain
    from langchain_core.prompts import ChatPromptTemplate

    template = ChatPromptTemplate.from_messages([
        ("system", prompt.prompt),
        ("human", "{question}"),
    ])
""")

for line in fetch_code.strip().split("\n"):
    print(f"    {line}")

print("\n  3. Track metrics per version:")
print("     Version 1: avg_latency=2.1s, avg_cost=$0.008, feedback=3.5/5")
print("     Version 2: avg_latency=1.8s, avg_cost=$0.006, feedback=4.2/5")
print("     → Version 2 wins on all metrics!")


# ============================================================
# Step 3: A/B Testing Pattern
# ============================================================

print("\n\n--- Step 3: A/B Testing Pattern ---\n")

ab_code = textwrap.dedent("""\
    import random

    # Fetch both versions
    prompt_v1 = langfuse.get_prompt("rag_system_prompt", version=1)
    prompt_v2 = langfuse.get_prompt("rag_system_prompt", version=2)

    # Random assignment (50/50)
    if random.random() < 0.5:
        active_prompt = prompt_v1
        version_tag = "v1"
    else:
        active_prompt = prompt_v2
        version_tag = "v2"

    # Pass version as metadata for analysis
    handler = CallbackHandler(
        user_id=user_id,
        tags=[version_tag],
        metadata={"prompt_version": version_tag},
    )
""")

print("  A/B test implementation:\n")
for line in ab_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# TODO 1: Prompt management code
# ============================================================

print("\n\n--- TODO 1: Prompt Management Code ---\n")

print("  Write code that:")
print("    - Creates Langfuse client")
print("    - Fetches a prompt by name ('rag_system_prompt')")
print("    - Uses the prompt in a ChatPromptTemplate")
print("    - Passes prompt version as metadata to CallbackHandler")
print("    - Includes version tag in handler tags\n")

# SOLUTION: Prompt management with LangFuse
todo1_code = textwrap.dedent("""\
    from langfuse import Langfuse
    from langfuse.callback import CallbackHandler
    from langchain_core.prompts import ChatPromptTemplate

    # Create LangFuse client
    langfuse = Langfuse()

    # Fetch the prompt by name from LangFuse
    prompt = langfuse.get_prompt("rag_system_prompt", label="production")

    # Build a ChatPromptTemplate using the fetched prompt
    template = ChatPromptTemplate.from_messages([
        ("system", prompt.prompt),
        ("human", "{question}"),
    ])

    # Determine version tag for tracking
    version_tag = f"v{prompt.version}"

    # Create CallbackHandler with metadata and tags for A/B tracking
    handler = CallbackHandler(
        user_id="alice",
        session_id="chat_42",
        tags=["production", version_tag],
        metadata={"prompt_version": version_tag, "prompt_name": "rag_system_prompt"},
    )
""")

with open(os.path.join(WORKDIR, "prompt_manager.py"), "w") as f:
    f.write(todo1_code)

checks1 = [
    ("Has Langfuse import",         "Langfuse" in todo1_code),
    ("Has get_prompt call",         "get_prompt" in todo1_code),
    ("Has prompt name",             "rag_system_prompt" in todo1_code),
    ("Has ChatPromptTemplate",      "ChatPromptTemplate" in todo1_code),
    ("Has prompt.prompt usage",     "prompt.prompt" in todo1_code or "prompt)" in todo1_code),
    ("Has CallbackHandler",         "CallbackHandler" in todo1_code),
    ("Has metadata with version",   "metadata" in todo1_code and "version" in todo1_code),
    ("Has tags",                    "tags" in todo1_code),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Prompt management quiz
# ============================================================

print("\n\n--- TODO 2: Prompt Management Quiz ---\n")

quiz = [
    {
        "question": "What LangFuse method fetches a prompt by name?",
        "answer": "___",
        "correct": "get_prompt",
    },
    {
        "question": "What parameter fetches a specific labeled version (e.g., 'production')?",
        "answer": "___",
        "correct": "label",
    },
    {
        "question": "What property on the prompt object returns the template text?",
        "answer": "___",
        "correct": "prompt",
    },
    {
        "question": "What handler parameter carries version info for A/B comparison?",
        "answer": "___",
        "correct": "metadata",
    },
]

# SOLUTION: Fill in quiz answers
quiz[0]["answer"] = "get_prompt"
quiz[1]["answer"] = "label"
quiz[2]["answer"] = "prompt"
quiz[3]["answer"] = "metadata"

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

print(f"\n\n--- Lab 06 Summary ---\n")
print("  Key concepts:")
print("    1. langfuse.get_prompt() fetches versioned prompts at runtime")
print("    2. Labels ('production', 'staging') control which version is active")
print("    3. A/B testing: random version assignment + tag in handler")
print("    4. Compare metrics (latency, cost, feedback) per version")
print(f"\n  TODO 1: {score1}/{len(checks1)} prompt management checks")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
