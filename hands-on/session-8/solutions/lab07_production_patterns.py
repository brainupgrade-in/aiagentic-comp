"""
Lab 07 Solution: Production Multi-Agent Patterns
===================================================
"""

import os
import time
from typing import TypedDict, Annotated
from operator import add
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

fast_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
smart_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

print("=" * 50)
print("  Production Multi-Agent Patterns (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Circuit breaker
# ============================================================

class CircuitState(TypedDict):
    request: str
    category: str
    worker_output: str
    error: str
    error_count: int
    circuit_open: bool
    final_response: str
    audit: Annotated[list, add]

TEMPLATES = {
    "hr": "Please visit the HR portal or email hr@unigps.in.",
    "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
    "finance": "Please email finance@unigps.in with details.",
    "general": "Your request has been noted. A team member will respond shortly.",
}

def circuit_router(state: CircuitState) -> dict:
    if state["error_count"] >= 3:
        print(f"  [router] CIRCUIT OPEN — {state['error_count']} errors, using templates")
        return {"circuit_open": True, "category": "general",
                "audit": [f"[{datetime.now().strftime('%H:%M:%S')}] Circuit breaker OPEN"]}

    prompt = f"Classify: hr, tech, finance, general. One word.\n{state['request']}"
    try:
        response = fast_llm.invoke(prompt)
        cat = response.content.strip().lower()
        if cat not in ["hr", "tech", "finance", "general"]:
            cat = "general"
        print(f"  [router] → {cat}")
        return {"category": cat, "circuit_open": False, "error": "",
                "audit": [f"[{datetime.now().strftime('%H:%M:%S')}] Routed: {cat}"]}
    except Exception as e:
        return {"category": "general", "error": str(e),
                "error_count": state["error_count"] + 1, "circuit_open": False,
                "audit": [f"[{datetime.now().strftime('%H:%M:%S')}] Router error: {e}"]}

def route_circuit(state: CircuitState) -> str:
    if state["circuit_open"]:
        return "fallback"
    return state["category"]

def specialist(state: CircuitState) -> dict:
    prompt = (
        f"You are UniGPS {state['category']} support.\n"
        f"Request: {state['request']}\n"
        f"Reply helpfully in 2 sentences."
    )
    try:
        response = smart_llm.invoke(prompt)
        return {"worker_output": response.content.strip(), "error": "",
                "audit": [f"Specialist ({state['category']}) responded"]}
    except Exception as e:
        return {"error": str(e), "error_count": state["error_count"] + 1,
                "audit": [f"Specialist error: {e}"]}

def route_after_specialist(state: CircuitState) -> str:
    return "fallback" if state["error"] else "finalize"

def fallback(state: CircuitState) -> dict:
    output = TEMPLATES.get(state["category"], TEMPLATES["general"])
    print(f"  [fallback] Template: {state['category']}")
    return {"worker_output": output, "error": "",
            "audit": [f"Fallback template ({state['category']})"]}

def finalize(state: CircuitState) -> dict:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS | {ts}",
            "audit": [f"Finalized at {ts}"]}

graph = StateGraph(CircuitState)
graph.add_node("router", circuit_router)
graph.add_node("hr", specialist)
graph.add_node("tech", specialist)
graph.add_node("finance", specialist)
graph.add_node("general", specialist)
graph.add_node("fallback", fallback)
graph.add_node("finalize", finalize)

graph.add_edge(START, "router")
graph.add_conditional_edges("router", route_circuit, {
    "hr": "hr", "tech": "tech", "finance": "finance",
    "general": "general", "fallback": "fallback",
})
for w in ["hr", "tech", "finance", "general"]:
    graph.add_conditional_edges(w, route_after_specialist, {
        "finalize": "finalize", "fallback": "fallback",
    })
graph.add_edge("fallback", "finalize")
graph.add_edge("finalize", END)

app = graph.compile()

print("\n--- TODO 1: Circuit Breaker ---\n")

# Normal operation (circuit closed)
for req in ["How many leave days?", "Server is slow"]:
    result = app.invoke({
        "request": req, "category": "", "worker_output": "",
        "error": "", "error_count": 0, "circuit_open": False,
        "final_response": "", "audit": [],
    })
    print(f"  '{req}' → {result['final_response'][:60]}...\n")

# Simulate circuit open (3+ errors)
print("  With error_count=3 (circuit OPEN):")
result = app.invoke({
    "request": "Any question at all",
    "category": "", "worker_output": "", "error": "",
    "error_count": 3, "circuit_open": False,
    "final_response": "", "audit": [],
})
print(f"  → {result['final_response'][:60]}...")
print(f"  Circuit open: {result['circuit_open']}")
print(f"  Audit: {result['audit']}")
print(f"  → LLM was skipped entirely!")

# ============================================================
# TODO 2 Solution: Response time tracking
# ============================================================

print("\n\n--- TODO 2: Response Time Tracking ---\n")

class TimedState(TypedDict):
    request: str
    category: str
    worker_output: str
    error: str
    final_response: str
    timings: Annotated[list, add]
    audit: Annotated[list, add]

def timed_router(state: TimedState) -> dict:
    start = time.time()
    prompt = f"Classify: hr, tech, finance, general. One word.\n{state['request']}"
    try:
        response = fast_llm.invoke(prompt)
        cat = response.content.strip().lower()
        if cat not in ["hr", "tech", "finance", "general"]:
            cat = "general"
    except Exception:
        cat = "general"
    elapsed = time.time() - start
    slow = " [SLOW]" if elapsed > 5 else ""
    print(f"  [router] {cat} ({elapsed:.2f}s{slow})")
    return {"category": cat, "error": "",
            "timings": [{"agent": "router", "seconds": round(elapsed, 2)}],
            "audit": [f"Router: {elapsed:.2f}s{slow}"]}

def timed_specialist(state: TimedState) -> dict:
    start = time.time()
    prompt = (
        f"You are UniGPS {state['category']} support.\n"
        f"Request: {state['request']}\nReply in 2 sentences."
    )
    try:
        response = smart_llm.invoke(prompt)
        output = response.content.strip()
        error = ""
    except Exception as e:
        output = TEMPLATES.get(state["category"], TEMPLATES["general"])
        error = str(e)
    elapsed = time.time() - start
    slow = " [SLOW]" if elapsed > 5 else ""
    print(f"  [specialist] {state['category']} ({elapsed:.2f}s{slow})")
    return {"worker_output": output, "error": error,
            "timings": [{"agent": f"specialist_{state['category']}", "seconds": round(elapsed, 2)}],
            "audit": [f"Specialist ({state['category']}): {elapsed:.2f}s{slow}"]}

def timed_finalize(state: TimedState) -> dict:
    total = sum(t["seconds"] for t in state["timings"])
    slow = " [SLOW TOTAL]" if total > 10 else ""
    return {
        "final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS",
        "timings": [{"agent": "total", "seconds": round(total, 2)}],
        "audit": [f"Total: {total:.2f}s{slow}"],
    }

g2 = StateGraph(TimedState)
g2.add_node("router", timed_router)
g2.add_node("specialist", timed_specialist)
g2.add_node("finalize", timed_finalize)

g2.add_edge(START, "router")
g2.add_edge("router", "specialist")
g2.add_edge("specialist", "finalize")
g2.add_edge("finalize", END)

app2 = g2.compile()

for req in ["I need sick leave", "Deploy the new API", "When is my salary?"]:
    result = app2.invoke({
        "request": req, "category": "", "worker_output": "",
        "error": "", "final_response": "",
        "timings": [], "audit": [],
    })
    print(f"  '{req}' → {result['category']}")
    for t in result["timings"]:
        print(f"    {t['agent']}: {t['seconds']}s")
    print()

# Print timing summary
print("  Timing Summary:")
print(f"  {'Agent':<25} {'Time':>8}")
print("  " + "-" * 35)
for t in result["timings"]:
    flag = " !" if t["seconds"] > 5 else ""
    print(f"  {t['agent']:<25} {t['seconds']:>6.2f}s{flag}")

print("\n" + "=" * 50)
print("Lab 07 Solution complete!")
print("- TODO 1: Circuit breaker skips LLM after 3 errors, uses templates")
print("- TODO 2: Per-agent timing with [SLOW] flags for > 5s responses")
