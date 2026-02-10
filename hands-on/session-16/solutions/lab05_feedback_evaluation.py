"""
Lab 05: User Feedback & Evaluation
=====================================
Collect user feedback, implement automated scoring,
and link quality metrics to traces.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-16-05"

print("=" * 50)
print("  Lab 05: User Feedback & Evaluation")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Feedback Types
# ============================================================

print("\n--- Step 1: Feedback Types ---\n")

print("  LangFuse supports multiple feedback mechanisms:\n")
types = [
    ("User feedback",    "Manual: thumbs up/down or 1-5 stars",
                         "End user rates the response"),
    ("Automated eval",   "Code-based scoring on response quality",
                         "Check factual accuracy, format compliance"),
    ("Human review",     "Expert annotator rates trace quality",
                         "QA team reviews sampled traces"),
]
print(f"    {'Type':<18} {'Method':<45} {'Use Case'}")
print(f"    {'-'*95}")
for t, method, use in types:
    print(f"    {t:<18} {method:<45} {use}")


# ============================================================
# Step 2: Collecting Feedback
# ============================================================

print("\n\n--- Step 2: Collecting Feedback ---\n")

feedback_code = textwrap.dedent("""\
    from langfuse import Langfuse

    langfuse = Langfuse()

    # After chain.invoke() with handler:
    trace_id = handler.get_trace_id()

    # Binary feedback (thumbs up = 1, down = 0)
    langfuse.score(
        trace_id=trace_id,
        name="user_feedback",
        value=1,
        comment="Accurate and helpful",
    )

    # Numeric scale (0-5)
    langfuse.score(
        trace_id=trace_id,
        name="quality_rating",
        value=4,
        comment="Good but slightly verbose",
    )
""")

print("  Feedback collection code:\n")
for line in feedback_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# Step 3: Automated Evaluation
# ============================================================

print("\n\n--- Step 3: Automated Evaluation ---\n")

print("  Common automated scoring patterns:\n")
patterns = [
    ("Relevance",       "Does the answer address the question?",
                        "Compare question keywords with response"),
    ("Completeness",    "Does it cover all asked points?",
                        "Check all sub-questions answered"),
    ("Hallucination",   "Does it contradict retrieved docs?",
                        "Compare response claims with source docs"),
    ("Format",          "Does it follow requested format?",
                        "Check JSON validity, markdown structure"),
    ("Token efficiency", "Was the response concise?",
                        "output_tokens vs expected range"),
]
print(f"    {'Score Name':<18} {'What It Checks':<40} {'How'}")
print(f"    {'-'*95}")
for name, what, how in patterns:
    print(f"    {name:<18} {what:<40} {how}")

eval_code = textwrap.dedent("""\
    def evaluate_response(trace_id, question, response, docs):
        scores = {}

        # Relevance: do keywords from question appear in response?
        q_words = set(question.lower().split())
        r_words = set(response.lower().split())
        overlap = len(q_words & r_words) / max(len(q_words), 1)
        scores["relevance"] = min(1.0, overlap * 2)

        # Conciseness: penalize very long responses
        word_count = len(response.split())
        scores["conciseness"] = 1.0 if word_count < 200 else 0.5

        # Submit scores
        for name, value in scores.items():
            langfuse.score(
                trace_id=trace_id,
                name=name,
                value=value,
            )
""")

print("\n  Example automated evaluation:\n")
for line in eval_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# TODO 1: Write feedback collection code
# ============================================================

print("\n\n--- TODO 1: Feedback Collection Code ---\n")

print("  Write code that:")
print("    - Imports Langfuse from langfuse")
print("    - Creates Langfuse() client")
print("    - Gets trace_id from handler (get_trace_id)")
print("    - Submits user_feedback score (binary: 0 or 1)")
print("    - Submits quality_rating score (0-5 scale)")
print("    - Includes comment in at least one score\n")

# SOLUTION: Feedback collection code
todo1_code = textwrap.dedent("""\
    from langfuse import Langfuse

    # Create LangFuse client
    langfuse = Langfuse()

    # Get the trace ID from the callback handler
    trace_id = handler.get_trace_id()

    # Submit binary user feedback (thumbs up = 1, thumbs down = 0)
    langfuse.score(
        trace_id=trace_id,
        name="user_feedback",
        value=1,
        comment="The response was accurate and helpful",
    )

    # Submit quality rating on a 0-5 scale
    langfuse.score(
        trace_id=trace_id,
        name="quality_rating",
        value=4,
        comment="Good response, slightly verbose",
    )
""")

with open(os.path.join(WORKDIR, "feedback.py"), "w") as f:
    f.write(todo1_code)

checks1 = [
    ("Has Langfuse import",        "Langfuse" in todo1_code),
    ("Has langfuse client",        "Langfuse()" in todo1_code or "langfuse(" in todo1_code.lower()),
    ("Has get_trace_id",           "get_trace_id" in todo1_code or "trace_id" in todo1_code),
    ("Has score() call",           ".score(" in todo1_code),
    ("Has user_feedback name",     "user_feedback" in todo1_code),
    ("Has quality_rating name",    "quality_rating" in todo1_code),
    ("Has value parameter",        "value=" in todo1_code or "value =" in todo1_code),
    ("Has comment parameter",      "comment" in todo1_code),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Feedback quiz
# ============================================================

print("\n\n--- TODO 2: Feedback & Evaluation Quiz ---\n")

quiz = [
    {
        "question": "What LangFuse method records a score on a trace?",
        "answer": "___",
        "correct": "score",
    },
    {
        "question": "What handler method returns the trace ID?",
        "answer": "___",
        "correct": "get_trace_id",
        "check_fn": lambda a: "gettraceid" in a.replace("_", "").replace(" ", "").lower(),
    },
    {
        "question": "For thumbs-up/down feedback, what values do you use?",
        "answer": "___",
        "correct": "0 and 1",
        "check_fn": lambda a: "0" in a and "1" in a,
    },
    {
        "question": "What type of eval checks if the response contradicts source docs?",
        "answer": "___",
        "correct": "hallucination",
        "check_fn": lambda a: "hallucin" in a.lower(),
    },
]

# SOLUTION: Fill in quiz answers
quiz[0]["answer"] = "score"
quiz[1]["answer"] = "get_trace_id"
quiz[2]["answer"] = "0 and 1"
quiz[3]["answer"] = "hallucination detection"

score2 = 0
for i, q in enumerate(quiz, 1):
    if q["answer"] == "___":
        status = "TODO"
    elif "check_fn" in q:
        if q["check_fn"](q["answer"]):
            status = "PASS"
            score2 += 1
        else:
            status = "FAIL"
    else:
        is_correct = q["correct"].lower() in q["answer"].strip().lower()
        if is_correct:
            status = "PASS"
            score2 += 1
        else:
            status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 05 Summary ---\n")
print("  Key concepts:")
print("    1. langfuse.score() links feedback to traces via trace_id")
print("    2. User feedback: binary (0/1) or numeric (0-5)")
print("    3. Automated eval: relevance, completeness, hallucination checks")
print("    4. Quality metrics feed into continuous improvement")
print(f"\n  TODO 1: {score1}/{len(checks1)} feedback code checks")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
