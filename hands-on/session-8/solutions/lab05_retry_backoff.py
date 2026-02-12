"""
Lab 05 Solution: Retry with Backoff
======================================
"""

import os
import time
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.7)

print("=" * 50)
print("  Retry with Backoff (Solution)")
print("=" * 50)

# ============================================================
# Steps 1-3 same as lab — see lab file
# ============================================================

# ============================================================
# TODO 1 Solution: Time-budget retry
# ============================================================

class BudgetState(TypedDict):
    topic: str
    response: str
    quality_ok: bool
    error: str
    attempts: int
    max_attempts: int
    total_wait: float
    max_wait: float
    history: Annotated[list, add]

def generate_with_budget(state: BudgetState) -> dict:
    attempt = state["attempts"] + 1
    total_wait = state["total_wait"]

    if attempt > 1:
        delay = min(2 ** (attempt - 1), 4)
        total_wait += delay
        print(f"  [backoff] Waiting {delay}s (total: {total_wait}s)...")
        time.sleep(delay)

    prompt = f"Write a brief 2-sentence description about: {state['topic']}"
    if attempt > 1 and state["error"]:
        prompt += f"\nFix this issue: {state['error']}"

    response = llm.invoke(prompt)
    text = response.content.strip()
    print(f"  [generate] Attempt {attempt}: {text[:50]}...")
    return {
        "response": text, "error": "", "attempts": attempt,
        "total_wait": total_wait,
        "history": [f"Attempt {attempt}: generated"],
    }

def check_quality_budget(state: BudgetState) -> dict:
    issues = []
    if len(state["response"]) < 20:
        issues.append("too short")
    quality_ok = len(issues) == 0 and not state["error"]
    error = ", ".join(issues) if issues else ""
    print(f"  [quality] {'PASS' if quality_ok else f'FAIL ({error})'}")
    return {"quality_ok": quality_ok, "error": error, "history": [f"Quality: {'PASS' if quality_ok else 'FAIL'}"]}

def should_retry_with_budget(state: BudgetState) -> str:
    if state["quality_ok"]:
        return "accept"
    if state["attempts"] >= state["max_attempts"]:
        print(f"  [route] Max attempts reached")
        return "accept"
    if state["total_wait"] > state["max_wait"]:
        print(f"  [route] Time budget exceeded ({state['total_wait']:.0f}s > {state['max_wait']:.0f}s)")
        return "accept"
    return "retry"

graph1 = StateGraph(BudgetState)
graph1.add_node("generate", generate_with_budget)
graph1.add_node("check", check_quality_budget)
graph1.add_edge(START, "generate")
graph1.add_edge("generate", "check")
graph1.add_conditional_edges("check", should_retry_with_budget, {
    "accept": END, "retry": "generate",
})
app1 = graph1.compile()

print("\n--- TODO 1: Time-Budget Retry ---")
result = app1.invoke({
    "topic": "Benefits of LangGraph for AI workflows",
    "response": "", "quality_ok": False, "error": "",
    "attempts": 0, "max_attempts": 5, "total_wait": 0.0, "max_wait": 15.0,
    "history": [],
})
print(f"\nFinal: attempts={result['attempts']}, wait={result['total_wait']:.0f}s")
print(f"Response: {result['response'][:80]}...")

# ============================================================
# TODO 2 Solution: Generate + Refine with retry
# ============================================================

class RefineState(TypedDict):
    topic: str
    draft: str
    refined: str
    score: int
    phase: str
    attempts: int
    max_attempts: int

def generate_draft(state: RefineState) -> dict:
    attempt = state["attempts"] + 1
    prompt = f"Write a 2-sentence description about: {state['topic']}"
    response = llm.invoke(prompt)
    print(f"  [generate] {response.content[:50]}...")
    return {"draft": response.content.strip(), "attempts": attempt, "phase": "generated"}

def check_draft(state: RefineState) -> dict:
    prompt = f"Rate 1-10 for clarity. Reply with just the number.\nText: {state['draft']}"
    response = llm.invoke(prompt)
    try:
        score = int(response.content.strip().rstrip("."))
        score = max(1, min(10, score))
    except ValueError:
        score = 5
    print(f"  [check] Score: {score}/10")
    return {"score": score}

def route_after_check(state: RefineState) -> str:
    if state["score"] >= 7:
        return "refine"
    if state["attempts"] >= state["max_attempts"]:
        return "refine"  # Refine whatever we have
    return "retry"

def refine_draft(state: RefineState) -> dict:
    prompt = (
        f"Polish this text for professional clarity. Keep it 2 sentences:\n"
        f"{state['draft']}"
    )
    response = llm.invoke(prompt)
    print(f"  [refine] {response.content[:50]}...")
    return {"refined": response.content.strip(), "phase": "refined"}

graph2 = StateGraph(RefineState)
graph2.add_node("generate", generate_draft)
graph2.add_node("check", check_draft)
graph2.add_node("refine", refine_draft)

graph2.add_edge(START, "generate")
graph2.add_edge("generate", "check")
graph2.add_conditional_edges("check", route_after_check, {
    "retry": "generate",
    "refine": "refine",
})
graph2.add_edge("refine", END)

app2 = graph2.compile()

print("\n--- TODO 2: Generate + Refine ---")
print("Graph: generate → check → [retry→generate | refine] → END\n")

result = app2.invoke({
    "topic": "UniGPS employee onboarding process",
    "draft": "", "refined": "", "score": 0,
    "phase": "", "attempts": 0, "max_attempts": 3,
})
print(f"\nDraft: {result['draft'][:80]}...")
print(f"Refined: {result['refined'][:80]}...")
print(f"Score: {result['score']}/10, Attempts: {result['attempts']}")

print("\n" + "=" * 50)
print("Lab 05 Solution complete!")
print("- TODO 1: Time-budget stops retry when cumulative wait > 15s")
print("- TODO 2: Generate → check → [retry | refine] pipeline")
