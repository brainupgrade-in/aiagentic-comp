"""
Lab 03: Conditional Routing
=============================
Goal: Build workflows that branch — routing to different nodes
      based on state values.

What you'll learn:
- How to use add_conditional_edges() for branching
- How routing functions inspect state and choose the next node
- How multiple branches can converge back to a single node
- Building a request router for different departments
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Conditional Routing")
print("=" * 50)

# ============================================================
# Step 1: Define state for a request router
# ============================================================

class RequestState(TypedDict):
    message: str
    category: str
    response: str

# ============================================================
# Step 2: Create the nodes
# ============================================================

def classify(state: RequestState) -> dict:
    """Classify the request into HR, Tech, or Finance."""
    msg = state["message"].lower()
    if any(w in msg for w in ["leave", "sick", "wfh", "vacation", "maternity"]):
        return {"category": "hr"}
    elif any(w in msg for w in ["deploy", "bug", "server", "code", "database", "api"]):
        return {"category": "tech"}
    elif any(w in msg for w in ["expense", "reimburse", "invoice", "salary", "bill"]):
        return {"category": "finance"}
    return {"category": "general"}

def handle_hr(state: RequestState) -> dict:
    print(f"  [HR Handler] Processing: {state['message'][:50]}")
    return {"response": f"HR Team: We'll handle your request about '{state['category']}'. Check the HR portal for policies."}

def handle_tech(state: RequestState) -> dict:
    print(f"  [Tech Handler] Processing: {state['message'][:50]}")
    return {"response": f"Tech Support: Ticket created for your technical issue. Check Jira for updates."}

def handle_finance(state: RequestState) -> dict:
    print(f"  [Finance Handler] Processing: {state['message'][:50]}")
    return {"response": f"Finance Team: Your expense/finance query has been logged. Submit receipts to finance@unigps.in."}

def handle_general(state: RequestState) -> dict:
    print(f"  [General Handler] Processing: {state['message'][:50]}")
    return {"response": f"General Support: We've received your request and will route it to the appropriate team."}

# ============================================================
# Step 3: The routing function
# ============================================================
# This function reads the state and returns the name of the next node.

def route_request(state: RequestState) -> str:
    """Route to the appropriate handler based on category."""
    category = state["category"]
    if category == "hr":
        return "handle_hr"
    elif category == "tech":
        return "handle_tech"
    elif category == "finance":
        return "handle_finance"
    return "handle_general"

# ============================================================
# Step 4: Build the graph with conditional edges
# ============================================================

graph = StateGraph(RequestState)

# Add all nodes
graph.add_node("classify", classify)
graph.add_node("handle_hr", handle_hr)
graph.add_node("handle_tech", handle_tech)
graph.add_node("handle_finance", handle_finance)
graph.add_node("handle_general", handle_general)

# Entry edge
graph.add_edge(START, "classify")

# Conditional edge — classify routes to the appropriate handler
graph.add_conditional_edges(
    "classify",          # source node
    route_request,       # routing function
    {                    # mapping: return value → node name
        "handle_hr": "handle_hr",
        "handle_tech": "handle_tech",
        "handle_finance": "handle_finance",
        "handle_general": "handle_general",
    }
)

# All handlers converge to END
graph.add_edge("handle_hr", END)
graph.add_edge("handle_tech", END)
graph.add_edge("handle_finance", END)
graph.add_edge("handle_general", END)

app = graph.compile()

print("Graph: START → classify → [HR|Tech|Finance|General] → END\n")

# ============================================================
# Step 5: Test with different requests
# ============================================================

test_requests = [
    "I need to apply for sick leave next week",
    "The production server is showing 500 errors",
    "How do I submit my travel expense report?",
    "Where is the Bangalore office cafeteria?",
    "Can I work from home on Wednesdays?",
    "I need help deploying the new API to staging",
]

print("--- Routing Requests ---")
for msg in test_requests:
    result = app.invoke({"message": msg})
    print(f"\n  Message:  '{msg}'")
    print(f"  Category: {result['category']}")
    print(f"  Response: {result['response']}")

# ============================================================
# Step 6: Visualize the routing
# ============================================================

print("\n--- Routing Summary ---")
categories = {}
for msg in test_requests:
    result = app.invoke({"message": msg})
    cat = result["category"]
    categories[cat] = categories.get(cat, 0) + 1

for cat, count in sorted(categories.items()):
    print(f"  {cat:>10}: {'█' * count * 3} ({count})")

# ============================================================
# TODO 1: Add an "urgent" priority route
# ============================================================
# Modify the workflow so that requests containing "urgent" or
# "critical" go to a special "handle_urgent" node that prepends
# "[URGENT]" to the response, regardless of category.
# Hint: Add a second conditional check after classify, or add
# a priority classification step before routing.

# def handle_urgent(state):
#     return {"response": f"[URGENT] Escalated! {state['message'][:50]}... — Priority support team notified."}

# ============================================================
# TODO 2: Add a "format_response" convergence node
# ============================================================
# Instead of having all handlers go directly to END, add a
# "format_response" node that all handlers route to. This node
# should add a standard footer: "\n— UniGPS Support Bot"
# Graph: START → classify → [handlers] → format_response → END

# def format_response(state):
#     return {"response": f"{state['response']}\n— UniGPS Support Bot"}

print("\n" + "=" * 50)
print("Lab 03 complete! Key takeaways:")
print("- add_conditional_edges() enables branching workflows")
print("- The routing function reads state and returns a node name")
print("- Multiple branches can converge back to a single node")
print("- Pattern: classify → route → specialized handlers → END")
print("- Routing is deterministic — same state always picks same path")
