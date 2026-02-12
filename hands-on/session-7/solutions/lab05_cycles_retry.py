"""
Lab 05 Solution: Cycles & Retry Logic
=======================================
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
print("  Cycles & Retry Logic (Solution)")
print("=" * 50)

# ============================================================
# Step 1: Counter loop (same as lab)
# ============================================================

class CounterState(TypedDict):
    count: int
    max_count: int
    log: Annotated[list, add]

def increment(state: CounterState) -> dict:
    new_count = state["count"] + 1
    print(f"  [increment] count: {state['count']} → {new_count}")
    return {"count": new_count, "log": [f"Incremented to {new_count}"]}

def should_continue(state: CounterState) -> str:
    if state["count"] >= state["max_count"]:
        return "done"
    return "loop"

graph1 = StateGraph(CounterState)
graph1.add_node("increment", increment)
graph1.add_edge(START, "increment")
graph1.add_conditional_edges(
    "increment", should_continue,
    {"loop": "increment", "done": END}
)
app1 = graph1.compile()

print("\n--- Step 1: Counter Loop ---")
result = app1.invoke({"count": 0, "max_count": 3, "log": []})
print(f"Final: {result['count']}, Log: {result['log']}")

# ============================================================
# Step 2: LLM Draft & Review (same as lab)
# ============================================================

class DraftState(TypedDict):
    topic: str
    draft: str
    feedback: str
    quality_score: int
    attempts: int
    max_attempts: int
    history: Annotated[list, add]

def draft_content(state: DraftState) -> dict:
    attempt = state["attempts"] + 1
    if attempt == 1:
        prompt = f"Write a brief 2-sentence description about: {state['topic']}"
    else:
        prompt = (
            f"Improve this draft based on the feedback.\n"
            f"Draft: {state['draft']}\nFeedback: {state['feedback']}\n"
            f"Write an improved 2-sentence version."
        )
    print(f"  [draft] Attempt {attempt}...")
    response = llm.invoke(prompt)
    draft = response.content.strip()
    print(f"  [draft] → {draft[:80]}...")
    return {"draft": draft, "attempts": attempt, "history": [f"[Attempt {attempt}] {draft[:60]}..."]}

def review_content(state: DraftState) -> dict:
    prompt = (
        f"Rate this content on a scale of 1-10 for clarity, accuracy, and style.\n"
        f"Content: {state['draft']}\n\n"
        f"Reply with ONLY a number (1-10) on the first line, then feedback on the second line."
    )
    response = llm.invoke(prompt)
    lines = response.content.strip().split("\n", 1)
    try:
        score = int(lines[0].strip().rstrip("."))
        score = max(1, min(10, score))
    except ValueError:
        score = 5
    feedback = lines[1].strip() if len(lines) > 1 else "No specific feedback."
    print(f"  [review] Score: {score}/10 — {feedback[:60]}")
    return {"quality_score": score, "feedback": feedback, "history": [f"[Review] Score: {score}/10"]}

# ============================================================
# TODO 1 Solution: Multi-level quality threshold
# ============================================================

def should_retry_enhanced(state: DraftState) -> str:
    """Enhanced retry with multiple quality levels."""
    score = state["quality_score"]
    attempts = state["attempts"]

    if score >= 9:
        print(f"  [route] ★ Excellent! Score {score}/10")
        return "accept"
    if score >= 7:
        print(f"  [route] ✓ Good enough. Score {score}/10")
        return "accept"
    if attempts >= state["max_attempts"]:
        print(f"  [route] ✗ Best effort after {attempts} attempts. Score {score}/10")
        return "accept"
    print(f"  [route] ↻ Score {score}/10, retrying (attempt {attempts}/{state['max_attempts']})...")
    return "retry"

graph2 = StateGraph(DraftState)
graph2.add_node("draft", draft_content)
graph2.add_node("review", review_content)
graph2.add_edge(START, "draft")
graph2.add_edge("draft", "review")
graph2.add_conditional_edges("review", should_retry_enhanced, {"retry": "draft", "accept": END})

app2 = graph2.compile()

print("\n--- TODO 1: Multi-Level Quality ---")
result = app2.invoke({
    "topic": "Benefits of using LangGraph for building AI workflows",
    "draft": "", "feedback": "", "quality_score": 0,
    "attempts": 0, "max_attempts": 3, "history": ["Workflow started"],
})
print(f"\nFinal: score={result['quality_score']}/10, attempts={result['attempts']}")

# ============================================================
# TODO 2 Solution: Spell checker cycle
# ============================================================

class SpellState(TypedDict):
    text: str
    has_errors: bool
    corrections: int

def check_spelling(state: SpellState) -> dict:
    """Use LLM to check for errors."""
    prompt = (
        f"Does this text have any spelling or grammar errors? "
        f"Reply with YES or NO on the first line.\n"
        f"Text: {state['text']}"
    )
    response = llm.invoke(prompt)
    answer = response.content.strip().split("\n")[0].upper()
    has_errors = "YES" in answer
    print(f"  [check] Has errors: {has_errors}")
    return {"has_errors": has_errors}

def correct_spelling(state: SpellState) -> dict:
    """Use LLM to fix errors."""
    prompt = (
        f"Fix all spelling and grammar errors in this text. "
        f"Return ONLY the corrected text, nothing else:\n"
        f"{state['text']}"
    )
    response = llm.invoke(prompt)
    corrected = response.content.strip()
    print(f"  [correct] '{state['text'][:40]}' → '{corrected[:40]}'")
    return {"text": corrected, "corrections": state["corrections"] + 1}

def check_result(state: SpellState) -> str:
    if not state["has_errors"]:
        return "clean"
    if state["corrections"] >= 2:
        return "clean"  # Max 2 correction rounds
    return "fix"

graph3 = StateGraph(SpellState)
graph3.add_node("check", check_spelling)
graph3.add_node("correct", correct_spelling)
graph3.add_edge(START, "check")
graph3.add_conditional_edges("check", check_result, {"fix": "correct", "clean": END})
graph3.add_edge("correct", "check")  # After fixing, check again

app3 = graph3.compile()

print("\n--- TODO 2: Spell Checker Cycle ---")
for text in [
    "thier are many benifits to using langgraph for ai",
    "The quick brown fox jumps over the lazy dog.",
]:
    print(f"\nInput: '{text}'")
    result = app3.invoke({"text": text, "has_errors": False, "corrections": 0})
    print(f"Output: '{result['text']}'")
    print(f"Corrections: {result['corrections']}")

print("\n" + "=" * 50)
print("Lab 05 Solution complete!")
print("- TODO 1: Three-level quality (Excellent/Good/Best effort)")
print("- TODO 2: Spell checker with check → correct → check cycle")
