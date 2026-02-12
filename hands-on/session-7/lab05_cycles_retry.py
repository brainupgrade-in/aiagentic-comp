"""
Lab 05: Cycles & Retry Logic
==============================
Goal: Build workflows with loops — where edges go backward for retry
      and iterative refinement, with max-attempt guards.

What you'll learn:
- How to create cycles (backward edges) in LangGraph
- Retry patterns with LLM-powered quality checks
- Max-attempt guards to prevent infinite loops
- Combining conditional edges with cycles

Requires: GROQ_API_KEY in .env
"""

import os
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

print("=" * 50)
print("  Cycles & Retry Logic")
print("=" * 50)

# ============================================================
# Step 1: Understand cycles — a simple counter loop
# ============================================================
# Before using LLMs, let's understand cycles with pure logic.

class CounterState(TypedDict):
    count: int
    max_count: int
    log: Annotated[list, add]

def increment(state: CounterState) -> dict:
    new_count = state["count"] + 1
    print(f"  [increment] count: {state['count']} → {new_count}")
    return {"count": new_count, "log": [f"Incremented to {new_count}"]}

def should_continue(state: CounterState) -> str:
    """Route: keep looping or stop."""
    if state["count"] >= state["max_count"]:
        return "done"
    return "loop"

graph1 = StateGraph(CounterState)
graph1.add_node("increment", increment)
graph1.add_edge(START, "increment")
graph1.add_conditional_edges(
    "increment",
    should_continue,
    {
        "loop": "increment",   # ← CYCLE: go back to same node!
        "done": END,
    }
)

app1 = graph1.compile()

print("\n--- Step 1: Simple Counter Loop ---")
result = app1.invoke({"count": 0, "max_count": 3, "log": []})
print(f"Final count: {result['count']}")
print(f"Log: {result['log']}")
print("→ The graph looped 3 times before reaching END!")

# ============================================================
# Step 2: LLM-powered draft & review cycle
# ============================================================
# Pattern: Draft → Review → (retry or accept)
# The LLM drafts content, then a review step checks quality.

class DraftState(TypedDict):
    topic: str
    draft: str
    feedback: str
    quality_score: int
    attempts: int
    max_attempts: int
    history: Annotated[list, add]

def draft_content(state: DraftState) -> dict:
    """LLM generates or refines content based on feedback."""
    attempt = state["attempts"] + 1

    if attempt == 1:
        prompt = f"Write a brief 2-sentence description about: {state['topic']}"
    else:
        prompt = (
            f"Improve this draft based on the feedback.\n"
            f"Draft: {state['draft']}\n"
            f"Feedback: {state['feedback']}\n"
            f"Write an improved 2-sentence version."
        )

    print(f"  [draft] Attempt {attempt}...")
    response = llm.invoke(prompt)
    draft = response.content.strip()
    print(f"  [draft] → {draft[:80]}...")

    return {
        "draft": draft,
        "attempts": attempt,
        "history": [f"[Attempt {attempt}] {draft[:60]}..."],
    }

def review_content(state: DraftState) -> dict:
    """LLM reviews the draft and assigns a quality score."""
    prompt = (
        f"Rate this content on a scale of 1-10 for clarity, accuracy, and style.\n"
        f"Content: {state['draft']}\n\n"
        f"Reply with ONLY a number (1-10) on the first line, "
        f"then feedback on the second line."
    )

    response = llm.invoke(prompt)
    lines = response.content.strip().split("\n", 1)

    # Parse score (default to 5 if parsing fails)
    try:
        score = int(lines[0].strip().rstrip("."))
        score = max(1, min(10, score))
    except ValueError:
        score = 5

    feedback = lines[1].strip() if len(lines) > 1 else "No specific feedback."
    print(f"  [review] Score: {score}/10 — {feedback[:60]}")

    return {
        "quality_score": score,
        "feedback": feedback,
        "history": [f"[Review] Score: {score}/10"],
    }

def should_retry(state: DraftState) -> str:
    """Decide: accept the draft, retry, or give up."""
    if state["quality_score"] >= 7:
        print(f"  [route] ✓ Quality {state['quality_score']}/10 — accepting!")
        return "accept"
    if state["attempts"] >= state["max_attempts"]:
        print(f"  [route] ✗ Max attempts ({state['max_attempts']}) reached — stopping.")
        return "accept"  # Accept whatever we have
    print(f"  [route] ↻ Score {state['quality_score']}/10, retrying...")
    return "retry"

graph2 = StateGraph(DraftState)
graph2.add_node("draft", draft_content)
graph2.add_node("review", review_content)

graph2.add_edge(START, "draft")
graph2.add_edge("draft", "review")
graph2.add_conditional_edges(
    "review",
    should_retry,
    {
        "retry": "draft",    # ← CYCLE: loop back to draft!
        "accept": END,
    }
)

app2 = graph2.compile()

print("\n--- Step 2: LLM Draft & Review Cycle ---")
print("Graph: START → draft → review → [retry→draft | accept→END]\n")

result = app2.invoke({
    "topic": "Benefits of using LangGraph for building AI workflows",
    "draft": "",
    "feedback": "",
    "quality_score": 0,
    "attempts": 0,
    "max_attempts": 3,
    "history": ["Workflow started"],
})

print(f"\nFinal draft: {result['draft']}")
print(f"Final score: {result['quality_score']}/10")
print(f"Attempts used: {result['attempts']}/{result['max_attempts']}")
print(f"History: {result['history']}")

# ============================================================
# Step 3: Two-node cycle with guard
# ============================================================
# A common pattern: validate → fix → validate → fix → ...

class ValidationState(TypedDict):
    text: str
    issues: list
    is_valid: bool
    fix_count: int

def validate_text(state: ValidationState) -> dict:
    """Check the text for issues."""
    text = state["text"]
    issues = []
    if len(text) < 20:
        issues.append("Too short (minimum 20 characters)")
    if not text[0].isupper():
        issues.append("Must start with a capital letter")
    if not text.endswith("."):
        issues.append("Must end with a period")

    is_valid = len(issues) == 0
    print(f"  [validate] Valid: {is_valid}, Issues: {issues}")
    return {"issues": issues, "is_valid": is_valid}

def fix_text(state: ValidationState) -> dict:
    """Fix the identified issues."""
    text = state["text"]
    if "capital letter" in str(state["issues"]):
        text = text[0].upper() + text[1:]
    if "end with a period" in str(state["issues"]):
        text = text.rstrip() + "."
    if "Too short" in str(state["issues"]):
        text = text + " This is additional context for completeness."

    print(f"  [fix] '{state['text'][:30]}' → '{text[:30]}'")
    return {"text": text, "fix_count": state["fix_count"] + 1}

def check_valid(state: ValidationState) -> str:
    if state["is_valid"]:
        return "done"
    if state["fix_count"] >= 3:
        return "done"  # Give up after 3 fixes
    return "fix"

graph3 = StateGraph(ValidationState)
graph3.add_node("validate", validate_text)
graph3.add_node("fix", fix_text)

graph3.add_edge(START, "validate")
graph3.add_conditional_edges(
    "validate",
    check_valid,
    {"fix": "fix", "done": END}
)
graph3.add_edge("fix", "validate")  # After fixing, validate again

app3 = graph3.compile()

print("\n--- Step 3: Validate → Fix Cycle ---")
print("Graph: START → validate → [fix→validate | done→END]\n")

for test_text in ["hello", "Hello world this is a test.", "good morning everyone"]:
    print(f"Input: '{test_text}'")
    result = app3.invoke({"text": test_text, "issues": [], "is_valid": False, "fix_count": 0})
    print(f"Output: '{result['text']}' (fixes: {result['fix_count']}, valid: {result['is_valid']})\n")

# ============================================================
# TODO 1: Add a "max quality" threshold
# ============================================================
# Modify the draft/review cycle (Step 2) so that:
# - If score >= 9: print "Excellent!" and end
# - If score >= 7: print "Good enough" and end
# - If score < 7 and attempts < max: retry
# - If score < 7 and attempts >= max: print "Best effort" and end
# This gives you three different exit messages based on quality.

# ============================================================
# TODO 2: Build a "spell checker" cycle
# ============================================================
# Create a cycle where:
# 1. "check" node uses LLM to find spelling/grammar errors
# 2. "correct" node uses LLM to fix them
# 3. Loop until no errors found or max 2 iterations
# Test with: "thier are many benifits to using langgraph for ai"

# class SpellState(TypedDict):
#     text: str
#     has_errors: bool
#     corrections: int
#
# def check_spelling(state):
#     prompt = f"Does this text have spelling or grammar errors? Reply YES or NO, then list errors.\n{state['text']}"
#     ...
#
# def correct_spelling(state):
#     prompt = f"Fix all spelling and grammar errors in this text:\n{state['text']}"
#     ...

print("\n" + "=" * 50)
print("Lab 05 complete! Key takeaways:")
print("- Cycles = edges that go backward (loop back to earlier nodes)")
print("- Always include max-attempt guards to prevent infinite loops")
print("- Pattern: generate → review → (retry or accept)")
print("- Conditional edges decide: continue looping or exit")
print("- Cycles enable self-correcting, iterative workflows")
