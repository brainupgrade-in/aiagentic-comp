"""
Lab 01 Solution: Multi-Branch Workflows
==========================================
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Multi-Branch Workflows (Solution)")
print("=" * 50)

# ============================================================
# Two-level branching with TODO solutions
# ============================================================

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
    elif any(w in msg for w in ["cafeteria", "parking", "gym", "office", "broken", "repair"]):
        return {"category": "facilities"}
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

# ============================================================
# TODO 2 Solution: Facilities category with sub-routing
# ============================================================

def facilities_triage(state: DetailedState) -> dict:
    msg = state["message"].lower()
    if any(w in msg for w in ["broken", "repair", "fix", "not working"]):
        return {"sub_category": "maintenance", "priority": "MEDIUM"}
    return {"sub_category": "inquiry", "priority": "LOW"}

def general_handler(state: DetailedState) -> dict:
    return {"sub_category": "other", "priority": "LOW"}

# ============================================================
# TODO 1 Solution: Priority escalation
# ============================================================

def escalate(state: DetailedState) -> dict:
    """Escalate high-priority tickets."""
    return {"response": f"[ESCALATED] {state['category']}/{state['sub_category']} — Priority team notified!"}

def respond(state: DetailedState) -> dict:
    return {"response": f"[{state['priority']}] {state['category']}/{state['sub_category']}: Ticket created."}

def route_primary(state: DetailedState) -> str:
    mapping = {"hr": "hr_triage", "tech": "tech_triage", "facilities": "facilities_triage"}
    return mapping.get(state["category"], "general_handler")

def route_by_priority(state: DetailedState) -> str:
    """Route high priority to escalate, others to respond."""
    if state["priority"] == "HIGH":
        return "escalate"
    return "respond"

# Build graph with both TODOs
graph = StateGraph(DetailedState)
graph.add_node("classify", primary_classify)
graph.add_node("hr_triage", hr_triage)
graph.add_node("tech_triage", tech_triage)
graph.add_node("facilities_triage", facilities_triage)
graph.add_node("general_handler", general_handler)
graph.add_node("escalate", escalate)
graph.add_node("respond", respond)

graph.add_edge(START, "classify")
graph.add_conditional_edges("classify", route_primary, {
    "hr_triage": "hr_triage",
    "tech_triage": "tech_triage",
    "facilities_triage": "facilities_triage",
    "general_handler": "general_handler",
})

# All triage nodes → priority routing
for node in ["hr_triage", "tech_triage", "facilities_triage", "general_handler"]:
    graph.add_conditional_edges(node, route_by_priority, {
        "escalate": "escalate",
        "respond": "respond",
    })

graph.add_edge("escalate", END)
graph.add_edge("respond", END)

app = graph.compile()

print("\nGraph: classify → [triage] → [escalate | respond] → END\n")

tests = [
    "I'm feeling sick and need leave",
    "The production server is down!",
    "Where is the office cafeteria?",
    "The AC in room B3 is broken and needs repair",
    "I want to apply for annual leave",
    "Help me deploy the new API",
]

for msg in tests:
    result = app.invoke({"message": msg})
    print(f"  '{msg[:45]}' → {result['response']}")

print("\n" + "=" * 50)
print("Lab 01 Solution complete!")
print("- TODO 1: HIGH priority → escalate node")
print("- TODO 2: Facilities category with maintenance/inquiry sub-routing")
