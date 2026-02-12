"""
Lab 05: Retry with Backoff
============================
Goal: Build retry cycles with exponential backoff and max-attempt
      guards for resilient LLM-powered workflows.

What you'll learn:
- Retry cycles: looping back on failure
- Exponential backoff: 1s, 2s, 4s... between retries
- Max-attempt guards to prevent infinite loops
- Combining retry with quality checks

Requires: GROQ_API_KEY in .env
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
print("  Retry with Backoff")
print("=" * 50)

# ============================================================
# Step 1: Basic retry cycle
# ============================================================

class RetryState(TypedDict):
    topic: str
    response: str
    quality_ok: bool
    error: str
    attempts: int
    max_attempts: int
    history: Annotated[list, add]

def generate(state: RetryState) -> dict:
    """Generate content using LLM."""
    attempt = state["attempts"] + 1
    print(f"  [generate] Attempt {attempt}/{state['max_attempts']}...")

    try:
        prompt = (
            f"Write a brief 2-sentence professional response about: {state['topic']}\n"
            f"Be clear and specific."
        )
        if attempt > 1 and state["error"]:
            prompt += f"\nPrevious attempt had this issue: {state['error']}. Fix it."

        response = llm.invoke(prompt)
        text = response.content.strip()
        print(f"  [generate] → {text[:60]}...")
        return {
            "response": text,
            "error": "",
            "attempts": attempt,
            "history": [f"Attempt {attempt}: generated ({len(text)} chars)"],
        }
    except Exception as e:
        print(f"  [generate] Error: {e}")
        return {
            "error": str(e),
            "attempts": attempt,
            "history": [f"Attempt {attempt}: error - {e}"],
        }

def check_quality(state: RetryState) -> dict:
    """Check if the response meets quality standards."""
    response = state["response"]

    # Quality checks
    issues = []
    if len(response) < 20:
        issues.append("too short")
    if len(response) > 500:
        issues.append("too long")
    if not response[0].isupper():
        issues.append("doesn't start with capital")

    quality_ok = len(issues) == 0 and not state["error"]
    error = ", ".join(issues) if issues else state.get("error", "")

    status = "PASS" if quality_ok else f"FAIL ({error})"
    print(f"  [quality] {status}")
    return {
        "quality_ok": quality_ok,
        "error": error,
        "history": [f"Quality check: {status}"],
    }

def should_retry(state: RetryState) -> str:
    """Decide: accept, retry, or give up."""
    if state["quality_ok"]:
        return "accept"
    if state["attempts"] >= state["max_attempts"]:
        print(f"  [route] Max attempts reached. Accepting best effort.")
        return "accept"
    print(f"  [route] Retrying...")
    return "retry"

graph1 = StateGraph(RetryState)
graph1.add_node("generate", generate)
graph1.add_node("check", check_quality)

graph1.add_edge(START, "generate")
graph1.add_edge("generate", "check")
graph1.add_conditional_edges("check", should_retry, {
    "accept": END,
    "retry": "generate",  # ← CYCLE!
})

app1 = graph1.compile()

print("\n--- Step 1: Basic Retry Cycle ---")
print("Graph: START → generate → check → [retry→generate | accept→END]\n")

result = app1.invoke({
    "topic": "UniGPS employee benefits and leave policy",
    "response": "", "quality_ok": False, "error": "",
    "attempts": 0, "max_attempts": 3, "history": [],
})
print(f"\nFinal: '{result['response'][:80]}...'")
print(f"Attempts: {result['attempts']}, Quality OK: {result['quality_ok']}")
print(f"History: {result['history']}")

# ============================================================
# Step 2: Retry with exponential backoff
# ============================================================

class BackoffState(TypedDict):
    query: str
    response: str
    error: str
    attempts: int
    max_attempts: int
    total_wait: float
    log: Annotated[list, add]

def call_with_backoff(state: BackoffState) -> dict:
    """Call LLM with exponential backoff on retry."""
    attempt = state["attempts"] + 1
    total_wait = state["total_wait"]

    # Apply backoff delay (skip on first attempt)
    if attempt > 1:
        delay = min(2 ** (attempt - 1), 8)  # Cap at 8 seconds
        print(f"  [backoff] Waiting {delay}s before retry...")
        time.sleep(delay)
        total_wait += delay

    try:
        response = llm.invoke(f"Answer briefly: {state['query']}")
        text = response.content.strip()
        print(f"  [call] Attempt {attempt}: Success")
        return {
            "response": text, "error": "", "attempts": attempt,
            "total_wait": total_wait,
            "log": [f"Attempt {attempt}: success (waited {total_wait:.0f}s total)"],
        }
    except Exception as e:
        print(f"  [call] Attempt {attempt}: Failed - {e}")
        return {
            "error": str(e), "attempts": attempt,
            "total_wait": total_wait,
            "log": [f"Attempt {attempt}: failed - {e}"],
        }

def check_success(state: BackoffState) -> str:
    if not state["error"]:
        return "success"
    if state["attempts"] >= state["max_attempts"]:
        return "give_up"
    return "retry"

def fallback_response(state: BackoffState) -> dict:
    return {
        "response": "Service temporarily unavailable. Please try again later.",
        "log": [f"Fallback used after {state['attempts']} attempts"],
    }

graph2 = StateGraph(BackoffState)
graph2.add_node("call", call_with_backoff)
graph2.add_node("fallback", fallback_response)

graph2.add_edge(START, "call")
graph2.add_conditional_edges("call", check_success, {
    "success": END,
    "retry": "call",       # ← CYCLE with backoff!
    "give_up": "fallback",
})
graph2.add_edge("fallback", END)

app2 = graph2.compile()

print("\n--- Step 2: Exponential Backoff ---")
print("Graph: START → call → [success→END | retry→call | give_up→fallback→END]\n")

result = app2.invoke({
    "query": "What is UniGPS's work from home policy?",
    "response": "", "error": "", "attempts": 0,
    "max_attempts": 3, "total_wait": 0.0, "log": [],
})
print(f"Response: {result['response'][:60]}...")
print(f"Attempts: {result['attempts']}, Total wait: {result['total_wait']:.0f}s")
print(f"Log: {result['log']}")

# ============================================================
# Step 3: Quality-based retry with LLM review
# ============================================================

class ReviewState(TypedDict):
    topic: str
    draft: str
    score: int
    feedback: str
    attempts: int
    max_attempts: int

def draft(state: ReviewState) -> dict:
    attempt = state["attempts"] + 1
    if attempt == 1:
        prompt = f"Write a 2-sentence description about: {state['topic']}"
    else:
        prompt = f"Improve this: {state['draft']}\nFeedback: {state['feedback']}\nWrite a better 2-sentence version."
    response = llm.invoke(prompt)
    print(f"  [draft] Attempt {attempt}: {response.content[:50]}...")
    return {"draft": response.content.strip(), "attempts": attempt}

def review(state: ReviewState) -> dict:
    prompt = (
        f"Rate 1-10 for clarity and helpfulness. "
        f"Reply: score on line 1, feedback on line 2.\n"
        f"Text: {state['draft']}"
    )
    response = llm.invoke(prompt)
    lines = response.content.strip().split("\n", 1)
    try:
        score = int(lines[0].strip().rstrip("."))
        score = max(1, min(10, score))
    except ValueError:
        score = 5
    feedback = lines[1].strip() if len(lines) > 1 else ""
    print(f"  [review] Score: {score}/10")
    return {"score": score, "feedback": feedback}

def review_route(state: ReviewState) -> str:
    if state["score"] >= 7:
        return "accept"
    if state["attempts"] >= state["max_attempts"]:
        return "accept"
    return "retry"

graph3 = StateGraph(ReviewState)
graph3.add_node("draft", draft)
graph3.add_node("review", review)
graph3.add_edge(START, "draft")
graph3.add_edge("draft", "review")
graph3.add_conditional_edges("review", review_route, {
    "accept": END, "retry": "draft",
})
app3 = graph3.compile()

print("\n--- Step 3: LLM Draft + Review Cycle ---")
result = app3.invoke({
    "topic": "Benefits of LangGraph for production AI workflows",
    "draft": "", "score": 0, "feedback": "",
    "attempts": 0, "max_attempts": 3,
})
print(f"\nFinal: score={result['score']}/10, attempts={result['attempts']}")
print(f"Draft: {result['draft'][:100]}...")

# ============================================================
# TODO 1: Add retry budget tracking
# ============================================================
# Track total time spent retrying. If cumulative retry time
# exceeds 15 seconds, stop retrying even if max_attempts
# isn't reached (time-based circuit breaker).

# def should_retry_with_budget(state):
#     if state["quality_ok"]: return "accept"
#     if state["attempts"] >= state["max_attempts"]: return "accept"
#     if state["total_wait"] > 15: return "accept"  # Time budget exceeded
#     return "retry"

# ============================================================
# TODO 2: Add a "refinement" mode
# ============================================================
# After the first successful generation, add a "refine" step
# that asks the LLM to improve the response. The refine step
# should also have retry logic (max 2 refinement attempts).
# Graph: generate → check → [retry | refine → check_refine → END]

print("\n" + "=" * 50)
print("Lab 05 complete! Key takeaways:")
print("- Retry = cycle back to an earlier node on failure")
print("- Always cap retries with max_attempts")
print("- Exponential backoff: delay = 2^attempt (capped)")
print("- Combine retry with quality checks for self-improvement")
print("- Track attempt count and total wait time in state")
