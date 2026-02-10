"""
Lab 01: Multi-Branch Workflows
================================
Goal: Build workflows that fan out to multiple branches and converge
      back to a single node.

What you'll learn:
- Fan-out: one node routing to multiple possible next nodes
- Convergence: multiple branches leading to one shared node
- Building a complete classify → route → handle → finalize pipeline
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Multi-Branch Workflows")
print("=" * 50)

# ============================================================
# Step 1: Basic fan-out and convergence
# ============================================================
# Pattern: classify → [handler_a | handler_b | handler_c] → format → END

class TicketState(TypedDict):
    message: str
    category: str
    response: str
    audit: Annotated[list, add]

def classify(state: TicketState) -> dict:
    """Classify the ticket by keywords."""
    msg = state["message"].lower()
    if any(w in msg for w in ["leave", "sick", "wfh", "vacation"]):
        cat = "hr"
    elif any(w in msg for w in ["server", "deploy", "bug", "database"]):
        cat = "tech"
    elif any(w in msg for w in ["expense", "invoice", "salary", "reimburse"]):
        cat = "finance"
    else:
        cat = "general"
    print(f"  [classify] '{msg[:40]}' → {cat}")
    return {"category": cat, "audit": [f"Classified: {cat}"]}

def handle_hr(state: TicketState) -> dict:
    print(f"  [HR] Processing...")
    return {"response": "HR: Your leave/HR request has been logged. Check the portal.", "audit": ["Handled by HR"]}

def handle_tech(state: TicketState) -> dict:
    print(f"  [Tech] Processing...")
    return {"response": "Tech: Ticket created. Check Jira for updates.", "audit": ["Handled by Tech"]}

def handle_finance(state: TicketState) -> dict:
    print(f"  [Finance] Processing...")
    return {"response": "Finance: Your finance query is being processed.", "audit": ["Handled by Finance"]}

def handle_general(state: TicketState) -> dict:
    print(f"  [General] Processing...")
    return {"response": "Support: We've received your request.", "audit": ["Handled by General"]}

def format_response(state: TicketState) -> dict:
    """Add standard footer — ALL branches converge here."""
    formatted = f"{state['response']}\n— UniGPS Support Bot"
    print(f"  [format] Added footer")
    return {"response": formatted, "audit": ["Response formatted"]}

def route_ticket(state: TicketState) -> str:
    return f"handle_{state['category']}"

# Build the graph
graph = StateGraph(TicketState)

graph.add_node("classify", classify)
graph.add_node("handle_hr", handle_hr)
graph.add_node("handle_tech", handle_tech)
graph.add_node("handle_finance", handle_finance)
graph.add_node("handle_general", handle_general)
graph.add_node("format", format_response)

# Entry
graph.add_edge(START, "classify")

# Fan-out: classify → one of four handlers
graph.add_conditional_edges("classify", route_ticket, {
    "handle_hr": "handle_hr",
    "handle_tech": "handle_tech",
    "handle_finance": "handle_finance",
    "handle_general": "handle_general",
})

# Convergence: all handlers → format
graph.add_edge("handle_hr", "format")
graph.add_edge("handle_tech", "format")
graph.add_edge("handle_finance", "format")
graph.add_edge("handle_general", "format")
graph.add_edge("format", END)

app = graph.compile()

print("\n--- Step 1: Fan-Out & Convergence ---")
print("Graph: START → classify → [HR|Tech|Finance|General] → format → END\n")

tests = [
    "I need to apply for sick leave",
    "Production server is throwing 500 errors",
    "How do I submit my expense report?",
    "Where is the office cafeteria?",
]

for msg in tests:
    result = app.invoke({"message": msg, "audit": []})
    print(f"\n  Message:  '{msg}'")
    print(f"  Category: {result['category']}")
    print(f"  Response: {result['response']}")
    print(f"  Audit:    {result['audit']}")

# ============================================================
# Step 2: Two-level branching
# ============================================================
# After classifying, sub-classify within a category.

class DetailedState(TypedDict):
    message: str
    category: str
    sub_category: str
    priority: str
    response: str

def primary_classify(state: DetailedState) -> dict:
    msg = state["message"].lower()
    if any(w in msg for w in ["leave", "sick", "wfh"]):
        return {"category": "hr"}
    elif any(w in msg for w in ["server", "deploy", "bug"]):
        return {"category": "tech"}
    return {"category": "general"}

def hr_triage(state: DetailedState) -> dict:
    msg = state["message"].lower()
    if "sick" in msg:
        return {"sub_category": "sick_leave", "priority": "HIGH"}
    return {"sub_category": "general_leave", "priority": "LOW"}

def tech_triage(state: DetailedState) -> dict:
    msg = state["message"].lower()
    if "server" in msg or "down" in msg:
        return {"sub_category": "infrastructure", "priority": "HIGH"}
    return {"sub_category": "development", "priority": "MEDIUM"}

def general_handler(state: DetailedState) -> dict:
    return {"sub_category": "other", "priority": "LOW", "response": "Logged."}

def respond(state: DetailedState) -> dict:
    return {"response": f"[{state['priority']}] {state['category']}/{state['sub_category']}: Ticket created."}

def route_primary(state: DetailedState) -> str:
    return {"hr": "hr_triage", "tech": "tech_triage"}.get(state["category"], "general_handler")

graph2 = StateGraph(DetailedState)
graph2.add_node("classify", primary_classify)
graph2.add_node("hr_triage", hr_triage)
graph2.add_node("tech_triage", tech_triage)
graph2.add_node("general_handler", general_handler)
graph2.add_node("respond", respond)

graph2.add_edge(START, "classify")
graph2.add_conditional_edges("classify", route_primary, {
    "hr_triage": "hr_triage",
    "tech_triage": "tech_triage",
    "general_handler": "general_handler",
})
graph2.add_edge("hr_triage", "respond")
graph2.add_edge("tech_triage", "respond")
graph2.add_edge("general_handler", "respond")
graph2.add_edge("respond", END)

app2 = graph2.compile()

print("\n\n--- Step 2: Two-Level Branching ---")
print("Graph: classify → [hr_triage | tech_triage | general] → respond → END\n")

for msg in ["I'm feeling sick and need leave", "The production server is down!", "Where do I park?"]:
    result = app2.invoke({"message": msg})
    print(f"  '{msg[:40]}' → {result['response']}")

# ============================================================
# TODO 1: Add a "priority_escalate" branch
# ============================================================
# Modify the two-level branching so that HIGH priority tickets
# go to an "escalate" node before "respond", while LOW/MEDIUM
# go directly to "respond".
# Graph: classify → triage → [escalate | respond] → END
# The escalate node should prepend "[ESCALATED] " to the response.

# def route_by_priority(state):
#     if state["priority"] == "HIGH":
#         return "escalate"
#     return "respond"
#
# def escalate(state):
#     return {"response": f"[ESCALATED] {state['category']}/{state['sub_category']}"}

# ============================================================
# TODO 2: Add a fourth category with sub-routing
# ============================================================
# Add a "facilities" category (keywords: cafeteria, parking, gym, office).
# Add a "facilities_triage" node that sub-classifies into:
#   - "maintenance" (keywords: broken, repair, fix)
#   - "inquiry" (everything else)
# Both converge back to "respond".

print("\n" + "=" * 50)
print("Lab 01 complete! Key takeaways:")
print("- Fan-out: conditional edges route to multiple handlers")
print("- Convergence: multiple add_edge() calls point to one node")
print("- Two-level branching: chain conditional edges for sub-routing")
print("- All branches must eventually reach END (or converge)")
