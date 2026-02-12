"""
Lab 02: Parallel Execution
============================
Goal: Execute multiple nodes simultaneously and merge their results
      using state reducers.

What you'll learn:
- How to fan out from one node to multiple parallel nodes
- Why reducers are essential for parallel writes
- Merge patterns: collecting results from parallel nodes
- Building a multi-check validation pipeline
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Parallel Execution")
print("=" * 50)

# ============================================================
# Step 1: The problem — parallel writes without a reducer
# ============================================================

class BadState(TypedDict):
    text: str
    result: str  # ← No reducer! Only one value survives.

def check_a(state: BadState) -> dict:
    return {"result": "check_a: passed"}

def check_b(state: BadState) -> dict:
    return {"result": "check_b: passed"}

# Both write to "result" → only one value survives (last write wins)
print("\n--- Step 1: The Problem (No Reducer) ---")
print("When parallel nodes write to the same field without a reducer,")
print("only the last write survives. This is a common bug!")

# ============================================================
# Step 2: The solution — parallel writes WITH a reducer
# ============================================================

class CheckState(TypedDict):
    text: str
    checks: Annotated[list, add]  # ← Reducer: all results accumulate!
    approved: bool

def check_spam(state: CheckState) -> dict:
    """Check if text contains spam keywords."""
    spam_words = ["buy now", "free money", "click here", "limited offer"]
    is_spam = any(w in state["text"].lower() for w in spam_words)
    result = {"type": "spam", "passed": not is_spam, "detail": "spam detected" if is_spam else "clean"}
    print(f"  [check_spam] {'FAIL' if is_spam else 'PASS'}")
    return {"checks": [result]}

def check_length(state: CheckState) -> dict:
    """Check if text meets minimum length."""
    passed = len(state["text"]) >= 10
    result = {"type": "length", "passed": passed, "detail": f"{len(state['text'])} chars"}
    print(f"  [check_length] {'PASS' if passed else 'FAIL'} ({len(state['text'])} chars)")
    return {"checks": [result]}

def check_language(state: CheckState) -> dict:
    """Check if text is in English (simple heuristic)."""
    english_words = {"the", "is", "a", "an", "to", "and", "of", "for", "in", "on", "i", "my", "how", "do", "can", "need"}
    words = set(state["text"].lower().split())
    overlap = len(words & english_words)
    passed = overlap >= 1
    result = {"type": "language", "passed": passed, "detail": f"English confidence: {overlap} common words"}
    print(f"  [check_language] {'PASS' if passed else 'FAIL'}")
    return {"checks": [result]}

def merge_results(state: CheckState) -> dict:
    """Merge all check results and make final decision."""
    all_passed = all(c["passed"] for c in state["checks"])
    summary = ", ".join(f"{c['type']}={'PASS' if c['passed'] else 'FAIL'}" for c in state["checks"])
    print(f"  [merge] {summary} → {'APPROVED' if all_passed else 'REJECTED'}")
    return {"approved": all_passed}

# Build parallel graph
graph = StateGraph(CheckState)
graph.add_node("check_spam", check_spam)
graph.add_node("check_length", check_length)
graph.add_node("check_language", check_language)
graph.add_node("merge", merge_results)

# Fan-out from START to all three checks (parallel!)
graph.add_edge(START, "check_spam")
graph.add_edge(START, "check_length")
graph.add_edge(START, "check_language")

# All checks converge to merge
graph.add_edge("check_spam", "merge")
graph.add_edge("check_length", "merge")
graph.add_edge("check_language", "merge")
graph.add_edge("merge", END)

app = graph.compile()

print("\n--- Step 2: Parallel Checks with Reducer ---")
print("Graph: START → [spam | length | language] → merge → END\n")

test_texts = [
    "I need to apply for sick leave next week please",
    "Hi",
    "Buy now! Free money! Click here for limited offer!",
    "How do I submit my travel expense report for the client visit?",
]

for text in test_texts:
    print(f"Text: '{text[:50]}...'")
    result = app.invoke({"text": text, "checks": []})
    print(f"  Checks: {len(result['checks'])} completed")
    print(f"  Approved: {result['approved']}")
    for c in result["checks"]:
        print(f"    {c['type']}: {'PASS' if c['passed'] else 'FAIL'} ({c['detail']})")
    print()

# ============================================================
# Step 3: Parallel with conditional post-processing
# ============================================================
# After merge, route based on the result.

class ReviewState(TypedDict):
    text: str
    checks: Annotated[list, add]
    approved: bool
    response: str

def check_spam_v2(state: ReviewState) -> dict:
    is_spam = any(w in state["text"].lower() for w in ["buy now", "free", "click here"])
    return {"checks": [{"type": "spam", "passed": not is_spam}]}

def check_length_v2(state: ReviewState) -> dict:
    return {"checks": [{"type": "length", "passed": len(state["text"]) >= 10}]}

def merge_v2(state: ReviewState) -> dict:
    all_passed = all(c["passed"] for c in state["checks"])
    return {"approved": all_passed}

def handle_approved(state: ReviewState) -> dict:
    return {"response": f"Message accepted: '{state['text'][:30]}...'"}

def handle_rejected(state: ReviewState) -> dict:
    failed = [c["type"] for c in state["checks"] if not c["passed"]]
    return {"response": f"Message rejected. Failed checks: {', '.join(failed)}"}

def route_after_merge(state: ReviewState) -> str:
    return "approved" if state["approved"] else "rejected"

graph2 = StateGraph(ReviewState)
graph2.add_node("check_spam", check_spam_v2)
graph2.add_node("check_length", check_length_v2)
graph2.add_node("merge", merge_v2)
graph2.add_node("handle_approved", handle_approved)
graph2.add_node("handle_rejected", handle_rejected)

graph2.add_edge(START, "check_spam")
graph2.add_edge(START, "check_length")
graph2.add_edge("check_spam", "merge")
graph2.add_edge("check_length", "merge")
graph2.add_conditional_edges("merge", route_after_merge, {
    "approved": "handle_approved",
    "rejected": "handle_rejected",
})
graph2.add_edge("handle_approved", END)
graph2.add_edge("handle_rejected", END)

app2 = graph2.compile()

print("--- Step 3: Parallel + Conditional ---")
print("Graph: START → [spam | length] → merge → [approved | rejected] → END\n")

for text in ["Valid support request about leave", "Hi", "Buy now free stuff click here"]:
    result = app2.invoke({"text": text, "checks": []})
    print(f"  '{text[:35]}' → {result['response']}")

# ============================================================
# TODO 1: Add a fourth parallel check
# ============================================================
# Add a "check_profanity" node that checks for bad words.
# It should run in parallel with the other checks.
# bad_words = ["stupid", "idiot", "hate"]
# Add it to the fan-out from START and convergence to merge.

# def check_profanity(state):
#     bad_words = ["stupid", "idiot", "hate"]
#     has_profanity = any(w in state["text"].lower() for w in bad_words)
#     return {"checks": [{"type": "profanity", "passed": not has_profanity}]}

# ============================================================
# TODO 2: Weighted scoring
# ============================================================
# Instead of all-or-nothing (all checks must pass), implement
# weighted scoring:
#   spam check: weight 3
#   length check: weight 1
#   language check: weight 2
# If total score >= 4, approve. Otherwise reject.
# Modify merge_results to calculate the weighted score.

# WEIGHTS = {"spam": 3, "length": 1, "language": 2}
# score = sum(WEIGHTS.get(c["type"], 1) for c in checks if c["passed"])

print("\n" + "=" * 50)
print("Lab 02 complete! Key takeaways:")
print("- Multiple edges from one node = parallel execution")
print("- ALWAYS use Annotated[list, add] for parallel writes")
print("- Without a reducer, last write wins (data loss!)")
print("- Pattern: fan-out → parallel checks → merge → route")
