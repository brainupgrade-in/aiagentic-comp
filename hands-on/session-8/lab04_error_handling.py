"""
Lab 04: Error Handling
========================
Goal: Build workflows that handle errors gracefully — storing errors
      in state, routing based on success/failure, and using fallbacks.

What you'll learn:
- Storing errors in state instead of raising exceptions
- Error-aware conditional routing
- Fallback nodes for graceful degradation
- Building resilient LLM-powered workflows

Requires: GROQ_API_KEY in .env
"""

import os
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

print("=" * 50)
print("  Error Handling")
print("=" * 50)

# ============================================================
# Step 1: Errors in state (not exceptions)
# ============================================================

class ProcessState(TypedDict):
    message: str
    response: str
    error: str
    audit: Annotated[list, add]

def call_llm(state: ProcessState) -> dict:
    """Call LLM with error handling — errors go into state."""
    try:
        response = llm.invoke(
            f"You are UniGPS support. Reply briefly (1 sentence) to: {state['message']}"
        )
        print(f"  [call_llm] Success: {response.content[:50]}...")
        return {
            "response": response.content.strip(),
            "error": "",
            "audit": ["LLM call successful"],
        }
    except Exception as e:
        print(f"  [call_llm] Error: {e}")
        return {
            "response": "",
            "error": str(e),
            "audit": [f"LLM error: {e}"],
        }

def format_output(state: ProcessState) -> dict:
    """Format the successful response."""
    return {
        "response": f"{state['response']}\n— UniGPS Bot",
        "audit": ["Response formatted"],
    }

graph1 = StateGraph(ProcessState)
graph1.add_node("call_llm", call_llm)
graph1.add_node("format", format_output)
graph1.add_edge(START, "call_llm")
graph1.add_edge("call_llm", "format")
graph1.add_edge("format", END)

app1 = graph1.compile()

print("\n--- Step 1: Errors in State ---")
result = app1.invoke({"message": "How many leave days do I get?", "audit": []})
print(f"  Response: {result['response'][:60]}...")
print(f"  Error: '{result['error']}'")
print(f"  Audit: {result['audit']}")

# ============================================================
# Step 2: Error-aware routing
# ============================================================
# Route to different nodes based on success or failure.

class RoutedState(TypedDict):
    message: str
    response: str
    error: str
    audit: Annotated[list, add]

def try_llm(state: RoutedState) -> dict:
    """Try the LLM call."""
    try:
        response = llm.invoke(
            f"Reply in one sentence to: {state['message']}"
        )
        return {"response": response.content.strip(), "error": "", "audit": ["LLM success"]}
    except Exception as e:
        return {"error": str(e), "audit": [f"LLM failed: {e}"]}

def handle_success(state: RoutedState) -> dict:
    """Process successful response."""
    print(f"  [success] {state['response'][:50]}...")
    return {"response": f"[OK] {state['response']}", "audit": ["Success path"]}

def handle_error(state: RoutedState) -> dict:
    """Provide a fallback response."""
    print(f"  [fallback] Using template response")
    return {
        "response": "We're experiencing issues. Your request has been logged and a team member will respond shortly.",
        "error": "",
        "audit": ["Fallback response used"],
    }

def route_on_error(state: RoutedState) -> str:
    """Route based on whether there was an error."""
    if state["error"]:
        return "error"
    return "success"

graph2 = StateGraph(RoutedState)
graph2.add_node("try_llm", try_llm)
graph2.add_node("handle_success", handle_success)
graph2.add_node("handle_error", handle_error)

graph2.add_edge(START, "try_llm")
graph2.add_conditional_edges("try_llm", route_on_error, {
    "success": "handle_success",
    "error": "handle_error",
})
graph2.add_edge("handle_success", END)
graph2.add_edge("handle_error", END)

app2 = graph2.compile()

print("\n--- Step 2: Error-Aware Routing ---")
print("Graph: START → try_llm → [success | error/fallback] → END\n")

result = app2.invoke({"message": "What's the expense policy?", "audit": []})
print(f"  Response: {result['response'][:60]}...")
print(f"  Audit: {result['audit']}")

# ============================================================
# Step 3: Multi-level fallback chain
# ============================================================

class FallbackState(TypedDict):
    message: str
    response: str
    error: str
    attempts: Annotated[list, add]

TEMPLATE_RESPONSES = {
    "hr": "Please check the HR portal or contact hr@unigps.in.",
    "tech": "Please create a Jira ticket or contact the tech team on Slack.",
    "finance": "Please email finance@unigps.in with your request details.",
    "general": "Your request has been logged. We'll get back to you shortly.",
}

def try_primary_llm(state: FallbackState) -> dict:
    """Try the primary LLM."""
    try:
        response = llm.invoke(f"Reply briefly: {state['message']}")
        return {
            "response": response.content.strip(),
            "error": "",
            "attempts": ["primary_llm: success"],
        }
    except Exception as e:
        return {"error": str(e), "attempts": [f"primary_llm: failed ({e})"]}

def try_simple_response(state: FallbackState) -> dict:
    """Fallback: keyword-based template response."""
    msg = state["message"].lower()
    for key, resp in TEMPLATE_RESPONSES.items():
        if key in msg or any(w in msg for w in ["leave", "sick"] if key == "hr") or \
           any(w in msg for w in ["server", "bug"] if key == "tech"):
            return {"response": resp, "error": "", "attempts": ["template: matched"]}
    return {"response": TEMPLATE_RESPONSES["general"], "error": "", "attempts": ["template: default"]}

def route_fallback(state: FallbackState) -> str:
    if state["error"]:
        return "fallback"
    return "done"

graph3 = StateGraph(FallbackState)
graph3.add_node("try_primary", try_primary_llm)
graph3.add_node("try_template", try_simple_response)

graph3.add_edge(START, "try_primary")
graph3.add_conditional_edges("try_primary", route_fallback, {
    "done": END,
    "fallback": "try_template",
})
graph3.add_edge("try_template", END)

app3 = graph3.compile()

print("\n--- Step 3: Fallback Chain ---")
print("Graph: START → try_primary → [done | fallback→try_template] → END\n")

result = app3.invoke({"message": "How do I apply for sick leave?", "attempts": []})
print(f"  Response: {result['response'][:60]}...")
print(f"  Attempts: {result['attempts']}")

# ============================================================
# TODO 1: Add error counting
# ============================================================
# Modify the state to track error_count (int).
# If the primary LLM fails, increment error_count.
# After 3 errors in a session, skip the LLM entirely and go
# straight to the template response (circuit breaker pattern).

# class CircuitState(TypedDict):
#     message: str
#     response: str
#     error: str
#     error_count: int
#     attempts: Annotated[list, add]
#
# def route_with_circuit_breaker(state):
#     if state["error_count"] >= 3:
#         return "template"  # Skip LLM entirely
#     return "try_llm"

# ============================================================
# TODO 2: Add a "log_error" node
# ============================================================
# When an error occurs, before using the fallback, route through
# a "log_error" node that records the error details (timestamp,
# error message, original request) in the audit trail.
# Graph: try_llm → [success | error→log_error→fallback] → END

# from datetime import datetime
# def log_error(state):
#     entry = f"[{datetime.now().isoformat()}] ERROR: {state['error']} | Request: {state['message'][:50]}"
#     return {"attempts": [f"logged: {entry}"]}

print("\n" + "=" * 50)
print("Lab 04 complete! Key takeaways:")
print("- Store errors in state, don't raise exceptions")
print("- Use conditional edges to route on error vs success")
print("- Fallback chains: primary → secondary → template")
print("- Circuit breaker: skip failing services after N errors")
print("- Always log errors in the audit trail")
