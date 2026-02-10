"""
Lab 02 Solution: Parallel Execution
======================================
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Parallel Execution (Solution)")
print("=" * 50)

# ============================================================
# Full parallel pipeline with TODO solutions
# ============================================================

WEIGHTS = {"spam": 3, "length": 1, "language": 2, "profanity": 2}

class CheckState(TypedDict):
    text: str
    checks: Annotated[list, add]
    score: int
    approved: bool

def check_spam(state: CheckState) -> dict:
    spam_words = ["buy now", "free money", "click here", "limited offer"]
    is_spam = any(w in state["text"].lower() for w in spam_words)
    return {"checks": [{"type": "spam", "passed": not is_spam}]}

def check_length(state: CheckState) -> dict:
    passed = len(state["text"]) >= 10
    return {"checks": [{"type": "length", "passed": passed}]}

def check_language(state: CheckState) -> dict:
    english_words = {"the", "is", "a", "to", "and", "of", "for", "i", "my", "how", "do", "need"}
    words = set(state["text"].lower().split())
    passed = len(words & english_words) >= 1
    return {"checks": [{"type": "language", "passed": passed}]}

# ============================================================
# TODO 1 Solution: Profanity check
# ============================================================

def check_profanity(state: CheckState) -> dict:
    bad_words = ["stupid", "idiot", "hate"]
    has_profanity = any(w in state["text"].lower() for w in bad_words)
    return {"checks": [{"type": "profanity", "passed": not has_profanity}]}

# ============================================================
# TODO 2 Solution: Weighted scoring
# ============================================================

def merge_results(state: CheckState) -> dict:
    """Weighted scoring instead of all-or-nothing."""
    score = sum(WEIGHTS.get(c["type"], 1) for c in state["checks"] if c["passed"])
    max_score = sum(WEIGHTS.values())
    approved = score >= 4  # Threshold
    summary = ", ".join(f"{c['type']}={'PASS' if c['passed'] else 'FAIL'}" for c in state["checks"])
    print(f"  [merge] {summary}")
    print(f"  [merge] Score: {score}/{max_score} → {'APPROVED' if approved else 'REJECTED'}")
    return {"score": score, "approved": approved}

# Build graph
graph = StateGraph(CheckState)
graph.add_node("check_spam", check_spam)
graph.add_node("check_length", check_length)
graph.add_node("check_language", check_language)
graph.add_node("check_profanity", check_profanity)  # ← TODO 1
graph.add_node("merge", merge_results)

# Parallel fan-out
graph.add_edge(START, "check_spam")
graph.add_edge(START, "check_length")
graph.add_edge(START, "check_language")
graph.add_edge(START, "check_profanity")  # ← TODO 1

# Convergence
graph.add_edge("check_spam", "merge")
graph.add_edge("check_length", "merge")
graph.add_edge("check_language", "merge")
graph.add_edge("check_profanity", "merge")  # ← TODO 1
graph.add_edge("merge", END)

app = graph.compile()

print("\nGraph: START → [spam|length|language|profanity] → merge → END\n")

tests = [
    "I need to apply for sick leave next week please",
    "Hi",
    "Buy now! Free money! Click here!",
    "I hate this stupid system, it is an idiot",
    "How do I submit my travel expense report?",
]

for text in tests:
    print(f"Text: '{text[:50]}'")
    result = app.invoke({"text": text, "checks": [], "score": 0})
    print(f"  Score: {result['score']}/{sum(WEIGHTS.values())}, Approved: {result['approved']}")
    for c in result["checks"]:
        w = WEIGHTS.get(c["type"], 1)
        print(f"    {c['type']} (weight {w}): {'PASS' if c['passed'] else 'FAIL'}")
    print()

print("=" * 50)
print("Lab 02 Solution complete!")
print("- TODO 1: Added profanity check as 4th parallel node")
print("- TODO 2: Weighted scoring (spam=3, language=2, profanity=2, length=1)")
