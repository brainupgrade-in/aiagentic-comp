"""
Lab 07: Production Multi-Agent Patterns
==========================================
Goal: Build production-ready multi-agent systems with specialization,
      fallback chains, and observability.

What you'll learn:
- Agent specialization with different models per role
- Fallback chains (primary → fallback → template)
- Complete audit trail for every decision
- Combining all patterns into a production system

Requires: GROQ_API_KEY in .env
"""

import os
from typing import TypedDict, Annotated
from operator import add
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

# Two models: fast for routing, large for complex tasks
fast_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
smart_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

print("=" * 50)
print("  Production Multi-Agent Patterns")
print("=" * 50)

# ============================================================
# Step 1: Agent specialization — different prompts per domain
# ============================================================

class ProdState(TypedDict):
    request: str
    category: str
    worker_output: str
    error: str
    final_response: str
    audit: Annotated[list, add]

def router_agent(state: ProdState) -> dict:
    """Fast routing agent — uses simple, focused prompt."""
    prompt = (
        f"Classify into: hr, tech, finance, general. Reply one word.\n"
        f"Request: {state['request']}"
    )
    try:
        response = fast_llm.invoke(prompt)
        cat = response.content.strip().lower()
        if cat not in ["hr", "tech", "finance", "general"]:
            cat = "general"
        print(f"  [router] → {cat}")
        return {"category": cat, "error": "",
                "audit": [f"[{datetime.now().strftime('%H:%M:%S')}] Routed: {cat}"]}
    except Exception as e:
        return {"category": "general", "error": str(e),
                "audit": [f"[{datetime.now().strftime('%H:%M:%S')}] Router error: {e}"]}

def route_category(state: ProdState) -> str:
    return state["category"]

# Specialized workers with focused prompts
def hr_specialist(state: ProdState) -> dict:
    """HR agent with domain-specific system prompt."""
    prompt = (
        f"You are the HR department assistant at UniGPS (Gheware UniGPS Solutions LLP).\n"
        f"You know about: leave policies (24 days/year), WFH (2 days/week), "
        f"insurance (family coverage), PF, gratuity.\n"
        f"Employee request: {state['request']}\n"
        f"Reply helpfully in 2-3 sentences."
    )
    try:
        response = smart_llm.invoke(prompt)
        return {"worker_output": response.content.strip(), "error": "",
                "audit": [f"HR specialist responded"]}
    except Exception as e:
        return {"error": str(e), "audit": [f"HR specialist error: {e}"]}

def tech_specialist(state: ProdState) -> dict:
    """Tech agent with domain-specific system prompt."""
    prompt = (
        f"You are the IT support team at UniGPS.\n"
        f"You handle: Jira tickets, server issues, VPN, laptops, deployments.\n"
        f"Standard SLA: P1=1hr, P2=4hr, P3=next day.\n"
        f"Employee request: {state['request']}\n"
        f"Reply helpfully in 2-3 sentences."
    )
    try:
        response = smart_llm.invoke(prompt)
        return {"worker_output": response.content.strip(), "error": "",
                "audit": [f"Tech specialist responded"]}
    except Exception as e:
        return {"error": str(e), "audit": [f"Tech specialist error: {e}"]}

def finance_specialist(state: ProdState) -> dict:
    """Finance agent with domain-specific system prompt."""
    prompt = (
        f"You are the Finance team at UniGPS.\n"
        f"You handle: expense reimbursements (submit within 30 days), salary queries, "
        f"tax declarations, budget approvals.\n"
        f"Employee request: {state['request']}\n"
        f"Reply helpfully in 2-3 sentences."
    )
    try:
        response = smart_llm.invoke(prompt)
        return {"worker_output": response.content.strip(), "error": "",
                "audit": [f"Finance specialist responded"]}
    except Exception as e:
        return {"error": str(e), "audit": [f"Finance specialist error: {e}"]}

def general_handler(state: ProdState) -> dict:
    return {"worker_output": "Your request has been logged. We'll get back to you soon.",
            "error": "", "audit": ["General handler used"]}

# ============================================================
# Step 2: Fallback chain
# ============================================================

def route_after_worker(state: ProdState) -> str:
    """If worker errored, go to fallback."""
    if state["error"]:
        return "fallback"
    return "qa_check"

def fallback_agent(state: ProdState) -> dict:
    """Fallback: try simpler approach or template."""
    print(f"  [fallback] Primary agent failed, using fallback")
    templates = {
        "hr": "Please visit the HR portal or email hr@unigps.in for assistance.",
        "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
        "finance": "Please email finance@unigps.in with your query details.",
        "general": "Your request has been noted. A team member will respond shortly.",
    }
    output = templates.get(state["category"], templates["general"])
    return {"worker_output": output, "error": "",
            "audit": [f"Fallback template used ({state['category']})"]}

# ============================================================
# Step 3: QA check
# ============================================================

def qa_check(state: ProdState) -> dict:
    """Quality gate: verify response meets standards."""
    output = state["worker_output"]
    issues = []
    if len(output) < 20:
        issues.append("too short")
    if not output.strip():
        issues.append("empty")

    if issues:
        print(f"  [QA] FAIL: {issues}")
        return {"error": ", ".join(issues), "audit": [f"QA failed: {issues}"]}
    print(f"  [QA] PASS")
    return {"error": "", "audit": ["QA passed"]}

def route_after_qa(state: ProdState) -> str:
    return "fallback" if state["error"] else "finalize"

def finalize(state: ProdState) -> dict:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "final_response": f"[{state['category'].upper()}] {state['worker_output']}\n"
                         f"— UniGPS Support | {timestamp}",
        "audit": [f"Finalized at {timestamp}"],
    }

# Build the production graph
graph = StateGraph(ProdState)
graph.add_node("router", router_agent)
graph.add_node("hr", hr_specialist)
graph.add_node("tech", tech_specialist)
graph.add_node("finance", finance_specialist)
graph.add_node("general", general_handler)
graph.add_node("fallback", fallback_agent)
graph.add_node("qa_check", qa_check)
graph.add_node("finalize", finalize)

graph.add_edge(START, "router")
graph.add_conditional_edges("router", route_category, {
    "hr": "hr", "tech": "tech", "finance": "finance", "general": "general",
})
for w in ["hr", "tech", "finance", "general"]:
    graph.add_conditional_edges(w, route_after_worker, {
        "qa_check": "qa_check",
        "fallback": "fallback",
    })
graph.add_conditional_edges("qa_check", route_after_qa, {
    "finalize": "finalize",
    "fallback": "fallback",
})
graph.add_edge("fallback", "finalize")
graph.add_edge("finalize", END)

app = graph.compile()

print("\nGraph: router → [specialist] → QA → [finalize | fallback→finalize] → END\n")

test_requests = [
    "How many casual leaves do I have left?",
    "The staging server is returning 502 errors",
    "When will my expense reimbursement be processed?",
    "Can we get standing desks for our team?",
]

for req in test_requests:
    result = app.invoke({
        "request": req, "category": "", "worker_output": "",
        "error": "", "final_response": "", "audit": [],
    })
    print(f"  Request: '{req}'")
    print(f"  Category: {result['category']}")
    print(f"  Response: {result['final_response'][:70]}...")
    print(f"  Audit trail ({len(result['audit'])} entries):")
    for entry in result["audit"]:
        print(f"    {entry}")
    print()

# ============================================================
# TODO 1: Circuit breaker for the entire system
# ============================================================
# Track error counts across requests. If errors exceed a threshold,
# skip the LLM agents entirely and use templates for all requests.
#
# Hint: Add error_count to state. Check it in router.
#
# class CircuitState(TypedDict):
#     request: str
#     category: str
#     worker_output: str
#     error: str
#     error_count: int          # ← track across requests
#     circuit_open: bool        # ← True when error_count >= 3
#     final_response: str
#     audit: Annotated[list, add]
#
# def circuit_router(state: CircuitState) -> dict:
#     if state["error_count"] >= 3:
#         print(f"  [router] CIRCUIT OPEN — all requests go to template")
#         return {"circuit_open": True, "category": "general",
#                 "audit": ["Circuit breaker OPEN"]}
#     # Normal LLM routing...
#     ...
#
# def route_circuit(state: CircuitState) -> str:
#     if state["circuit_open"]:
#         return "fallback"
#     return state["category"]
#
# Test: Simulate 3 errors, then verify circuit opens


# ============================================================
# TODO 2: Response time tracking
# ============================================================
# Add timing to each agent and include it in the audit trail.
# Flag responses that take too long (> 5 seconds).
#
# import time
#
# def timed_router(state) -> dict:
#     start = time.time()
#     # ... routing logic ...
#     elapsed = time.time() - start
#     slow = " [SLOW]" if elapsed > 5 else ""
#     return {
#         ...
#         "audit": [f"Router: {elapsed:.2f}s{slow}"],
#     }
#
# def timed_specialist(state) -> dict:
#     start = time.time()
#     # ... specialist logic ...
#     elapsed = time.time() - start
#     return {
#         ...
#         "audit": [f"Specialist ({state['category']}): {elapsed:.2f}s"],
#     }
#
# After all tests, print timing summary from audit trail.


print("\n" + "=" * 50)
print("Lab 07 complete!")
print("Patterns: specialization, fallback chain, QA gate, audit trail")
