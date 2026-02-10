"""
Lab 03 Solution: Conditional Routing
======================================
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Conditional Routing (Solution)")
print("=" * 50)

# ============================================================
# Original request router with TODO solutions
# ============================================================

class RequestState(TypedDict):
    message: str
    category: str
    priority: str   # ← TODO 1: added field
    response: str

# ============================================================
# TODO 1 Solution: Urgent priority detection
# ============================================================

def classify(state: RequestState) -> dict:
    """Classify the request and detect urgency."""
    msg = state["message"].lower()

    # Detect priority first
    if any(w in msg for w in ["urgent", "critical", "emergency", "asap"]):
        priority = "URGENT"
    else:
        priority = "normal"

    # Classify category
    if any(w in msg for w in ["leave", "sick", "wfh", "vacation", "maternity"]):
        category = "hr"
    elif any(w in msg for w in ["deploy", "bug", "server", "code", "database", "api"]):
        category = "tech"
    elif any(w in msg for w in ["expense", "reimburse", "invoice", "salary", "bill"]):
        category = "finance"
    else:
        category = "general"

    return {"category": category, "priority": priority}

def handle_hr(state: RequestState) -> dict:
    return {"response": f"HR Team: We'll handle your request about '{state['category']}'. Check the HR portal for policies."}

def handle_tech(state: RequestState) -> dict:
    return {"response": f"Tech Support: Ticket created for your technical issue. Check Jira for updates."}

def handle_finance(state: RequestState) -> dict:
    return {"response": f"Finance Team: Your expense/finance query has been logged. Submit receipts to finance@unigps.in."}

def handle_general(state: RequestState) -> dict:
    return {"response": f"General Support: We've received your request and will route it to the appropriate team."}

def handle_urgent(state: RequestState) -> dict:
    """Special handler for urgent requests."""
    return {"response": f"[URGENT] Escalated! '{state['message'][:50]}' — Priority support team notified immediately."}

# ============================================================
# Routing function with urgency check
# ============================================================

def route_request(state: RequestState) -> str:
    # TODO 1: Check urgency first
    if state["priority"] == "URGENT":
        return "handle_urgent"

    category = state["category"]
    if category == "hr":
        return "handle_hr"
    elif category == "tech":
        return "handle_tech"
    elif category == "finance":
        return "handle_finance"
    return "handle_general"

# ============================================================
# TODO 2 Solution: format_response convergence node
# ============================================================

def format_response(state: RequestState) -> dict:
    """Add standard footer to all responses."""
    return {"response": f"{state['response']}\n— UniGPS Support Bot"}

# ============================================================
# Build the graph
# ============================================================

graph = StateGraph(RequestState)

graph.add_node("classify", classify)
graph.add_node("handle_hr", handle_hr)
graph.add_node("handle_tech", handle_tech)
graph.add_node("handle_finance", handle_finance)
graph.add_node("handle_general", handle_general)
graph.add_node("handle_urgent", handle_urgent)        # ← TODO 1
graph.add_node("format_response", format_response)    # ← TODO 2

graph.add_edge(START, "classify")

graph.add_conditional_edges(
    "classify",
    route_request,
    {
        "handle_hr": "handle_hr",
        "handle_tech": "handle_tech",
        "handle_finance": "handle_finance",
        "handle_general": "handle_general",
        "handle_urgent": "handle_urgent",              # ← TODO 1
    }
)

# TODO 2: All handlers converge to format_response instead of END
graph.add_edge("handle_hr", "format_response")
graph.add_edge("handle_tech", "format_response")
graph.add_edge("handle_finance", "format_response")
graph.add_edge("handle_general", "format_response")
graph.add_edge("handle_urgent", "format_response")
graph.add_edge("format_response", END)

app = graph.compile()
print("Graph: START → classify → [HR|Tech|Finance|General|Urgent] → format_response → END\n")

# ============================================================
# Test with different requests
# ============================================================

test_requests = [
    "I need to apply for sick leave next week",
    "The production server is showing 500 errors",
    "How do I submit my travel expense report?",
    "Where is the Bangalore office cafeteria?",
    "URGENT: Critical database failure, all services down!",   # ← Tests urgent handler
    "Can I work from home on Wednesdays?",
    "CRITICAL: Need immediate help with deployment",           # ← Tests urgent handler
]

print("--- Routing Requests ---")
for msg in test_requests:
    result = app.invoke({"message": msg})
    print(f"\n  Message:  '{msg}'")
    print(f"  Category: {result['category']}")
    print(f"  Priority: {result['priority']}")
    print(f"  Response: {result['response']}")

print("\n" + "=" * 50)
print("Lab 03 Solution complete!")
print("- TODO 1: Urgent requests route to handle_urgent")
print("- TODO 2: All handlers converge to format_response → END")
