"""
Lab 04 Solution: Error Handling
=================================
"""

import os
from typing import TypedDict, Annotated
from operator import add
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

print("=" * 50)
print("  Error Handling (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Circuit breaker pattern
# ============================================================

class CircuitState(TypedDict):
    message: str
    response: str
    error: str
    error_count: int
    audit: Annotated[list, add]

TEMPLATE_RESPONSES = {
    "hr": "Please check the HR portal or contact hr@unigps.in.",
    "tech": "Please create a Jira ticket or contact the tech team.",
    "finance": "Please email finance@unigps.in with details.",
    "general": "Your request has been logged.",
}

def route_with_circuit_breaker(state: CircuitState) -> str:
    """Skip LLM if too many errors (circuit breaker)."""
    if state["error_count"] >= 3:
        print(f"  [circuit breaker] OPEN — skipping LLM ({state['error_count']} errors)")
        return "template"
    return "try_llm"

def try_llm(state: CircuitState) -> dict:
    try:
        response = llm.invoke(f"Reply briefly to: {state['message']}")
        return {
            "response": response.content.strip(),
            "error": "",
            "audit": ["LLM success"],
        }
    except Exception as e:
        return {
            "error": str(e),
            "error_count": state["error_count"] + 1,
            "audit": [f"LLM failed: {e}"],
        }

def use_template(state: CircuitState) -> dict:
    msg = state["message"].lower()
    for key in ["hr", "leave", "sick"]:
        if key in msg:
            return {"response": TEMPLATE_RESPONSES["hr"], "error": "", "audit": ["Template: HR"]}
    for key in ["server", "bug", "deploy"]:
        if key in msg:
            return {"response": TEMPLATE_RESPONSES["tech"], "error": "", "audit": ["Template: tech"]}
    return {"response": TEMPLATE_RESPONSES["general"], "error": "", "audit": ["Template: general"]}

def route_after_llm(state: CircuitState) -> str:
    if state["error"]:
        return "template"
    return "done"

graph1 = StateGraph(CircuitState)
graph1.add_node("try_llm", try_llm)
graph1.add_node("template", use_template)

graph1.add_conditional_edges(START, route_with_circuit_breaker, {
    "try_llm": "try_llm",
    "template": "template",
})
graph1.add_conditional_edges("try_llm", route_after_llm, {
    "template": "template",
    "done": END,
})
graph1.add_edge("template", END)

app1 = graph1.compile()

print("\n--- TODO 1: Circuit Breaker ---")
for msg in ["How many leave days?", "Server is down", "Submit my expense"]:
    result = app1.invoke({"message": msg, "error": "", "error_count": 0, "audit": []})
    print(f"  '{msg}' → {result['response'][:50]}... [{result['audit']}]")

# Test circuit breaker (simulate high error count)
print("\n  With error_count=3 (circuit breaker OPEN):")
result = app1.invoke({"message": "Any question", "error": "", "error_count": 3, "audit": []})
print(f"  → {result['response'][:50]}... [{result['audit']}]")
print("  → LLM was skipped entirely!")

# ============================================================
# TODO 2 Solution: Error logging node
# ============================================================

class LoggedState(TypedDict):
    message: str
    response: str
    error: str
    audit: Annotated[list, add]

def try_llm_v2(state: LoggedState) -> dict:
    try:
        response = llm.invoke(f"Reply briefly: {state['message']}")
        return {"response": response.content.strip(), "error": "", "audit": ["LLM success"]}
    except Exception as e:
        return {"error": str(e), "audit": [f"LLM failed"]}

def log_error(state: LoggedState) -> dict:
    """Log error details with timestamp."""
    entry = f"[{datetime.now().isoformat()}] ERROR: {state['error']} | Request: {state['message'][:50]}"
    print(f"  [log_error] {entry[:80]}...")
    return {"audit": [f"Logged: {entry[:60]}"]}

def fallback_response(state: LoggedState) -> dict:
    return {"response": "Service issue. We've logged the error.", "error": "", "audit": ["Fallback used"]}

def success_format(state: LoggedState) -> dict:
    return {"response": f"{state['response']}\n— UniGPS", "audit": ["Formatted"]}

def route_v2(state: LoggedState) -> str:
    return "error" if state["error"] else "success"

graph2 = StateGraph(LoggedState)
graph2.add_node("try_llm", try_llm_v2)
graph2.add_node("log_error", log_error)
graph2.add_node("fallback", fallback_response)
graph2.add_node("success", success_format)

graph2.add_edge(START, "try_llm")
graph2.add_conditional_edges("try_llm", route_v2, {
    "error": "log_error",
    "success": "success",
})
graph2.add_edge("log_error", "fallback")
graph2.add_edge("fallback", END)
graph2.add_edge("success", END)

app2 = graph2.compile()

print("\n--- TODO 2: Error Logging Node ---")
print("Graph: try_llm → [error→log_error→fallback | success→format] → END\n")

result = app2.invoke({"message": "What's the WFH policy?", "audit": []})
print(f"  Response: {result['response'][:60]}...")
print(f"  Audit: {result['audit']}")

print("\n" + "=" * 50)
print("Lab 04 Solution complete!")
print("- TODO 1: Circuit breaker skips LLM after 3 errors")
print("- TODO 2: log_error node records timestamp + details before fallback")
