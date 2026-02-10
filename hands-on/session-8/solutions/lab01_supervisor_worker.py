"""
Lab 01 Solution: Supervisor/Worker Basics
============================================
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Supervisor/Worker Basics (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Facilities worker
# ============================================================

class TeamState(TypedDict):
    request: str
    assigned_to: str
    worker_output: str
    final_response: str
    audit: Annotated[list, add]

def supervisor(state: TeamState) -> dict:
    msg = state["request"].lower()
    if any(w in msg for w in ["leave", "sick", "wfh", "policy", "hr"]):
        assigned = "hr"
    elif any(w in msg for w in ["server", "bug", "deploy", "network", "laptop"]):
        assigned = "tech"
    elif any(w in msg for w in ["expense", "salary", "invoice", "budget"]):
        assigned = "finance"
    elif any(w in msg for w in ["office", "desk", "parking", "cafeteria", "building", "access card"]):
        assigned = "facilities"
    else:
        assigned = "general"
    print(f"  [supervisor] '{msg[:40]}' → {assigned}")
    return {"assigned_to": assigned, "audit": [f"Supervisor → {assigned}"]}

def route_to_worker(state: TeamState) -> str:
    return state["assigned_to"]

def hr_worker(state: TeamState) -> dict:
    return {"worker_output": f"HR Agent: Your request about '{state['request'][:30]}' has been logged.",
            "audit": ["HR worker"]}

def tech_worker(state: TeamState) -> dict:
    return {"worker_output": f"Tech Agent: Jira ticket created for '{state['request'][:30]}'.",
            "audit": ["Tech worker"]}

def finance_worker(state: TeamState) -> dict:
    return {"worker_output": f"Finance Agent: Query about '{state['request'][:30]}' is being reviewed.",
            "audit": ["Finance worker"]}

def facilities_worker(state: TeamState) -> dict:
    print(f"  [Facilities worker] Processing: {state['request'][:40]}")
    return {
        "worker_output": f"Facilities Agent: Your request about '{state['request'][:30]}' "
                         "has been forwarded to the admin team. Expected response within 1 business day.",
        "audit": ["Facilities worker processed request"],
    }

def general_worker(state: TeamState) -> dict:
    return {"worker_output": "General Agent: Your request has been received.",
            "audit": ["General worker"]}

def finalize(state: TeamState) -> dict:
    return {"final_response": f"{state['worker_output']}\n— UniGPS Support",
            "audit": ["Finalized"]}

graph = StateGraph(TeamState)
graph.add_node("supervisor", supervisor)
graph.add_node("hr_worker", hr_worker)
graph.add_node("tech_worker", tech_worker)
graph.add_node("finance_worker", finance_worker)
graph.add_node("facilities_worker", facilities_worker)
graph.add_node("general_worker", general_worker)
graph.add_node("finalize", finalize)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges("supervisor", route_to_worker, {
    "hr": "hr_worker",
    "tech": "tech_worker",
    "finance": "finance_worker",
    "facilities": "facilities_worker",
    "general": "general_worker",
})
for w in ["hr_worker", "tech_worker", "finance_worker", "facilities_worker", "general_worker"]:
    graph.add_edge(w, "finalize")
graph.add_edge("finalize", END)

app = graph.compile()

print("\n--- TODO 1: Facilities Worker ---\n")

tests = [
    "Where is the parking area?",
    "I need an access card for building B",
    "I need to apply for sick leave",
    "The production server is down",
]

for req in tests:
    result = app.invoke({"request": req, "audit": []})
    print(f"  '{req}' → [{result['assigned_to']}] {result['final_response'][:60]}...")

# ============================================================
# TODO 2 Solution: Supervisor iteration (multi-worker)
# ============================================================

print("\n\n--- TODO 2: Multi-Worker Supervisor ---\n")

class MultiWorkerState(TypedDict):
    request: str
    pending_workers: list
    completed_workers: Annotated[list, add]
    final_response: str
    audit: Annotated[list, add]

def multi_supervisor(state: MultiWorkerState) -> dict:
    """Identify all relevant domains."""
    msg = state["request"].lower()
    workers = []
    if any(w in msg for w in ["leave", "sick", "hr"]):
        workers.append("hr")
    if any(w in msg for w in ["laptop", "server", "bug", "deploy"]):
        workers.append("tech")
    if any(w in msg for w in ["expense", "salary"]):
        workers.append("finance")
    if any(w in msg for w in ["desk", "parking", "cafeteria"]):
        workers.append("facilities")
    if not workers:
        workers.append("general")
    print(f"  [multi_supervisor] Workers: {workers}")
    return {"pending_workers": workers, "audit": [f"Workers queued: {workers}"]}

def dispatch_next(state: MultiWorkerState) -> dict:
    """Execute the first pending worker."""
    pending = state["pending_workers"]
    if not pending:
        return {"audit": ["No pending workers"]}

    current = pending[0]
    remaining = pending[1:]

    # Simulate worker execution
    responses = {
        "hr": "HR Agent: Leave request processed.",
        "tech": "Tech Agent: IT ticket created.",
        "finance": "Finance Agent: Expense reviewed.",
        "facilities": "Facilities Agent: Admin notified.",
        "general": "General Agent: Request logged.",
    }
    output = responses.get(current, "Agent: Done.")
    print(f"  [dispatch] Executing {current} worker")
    return {
        "pending_workers": remaining,
        "completed_workers": [{"worker": current, "output": output}],
        "audit": [f"Dispatched {current}: {output[:40]}"],
    }

def route_dispatch(state: MultiWorkerState) -> str:
    if state["pending_workers"]:
        return "dispatch"
    return "aggregate"

def multi_aggregate(state: MultiWorkerState) -> dict:
    combined = "\n".join(f"• {w['worker']}: {w['output']}" for w in state["completed_workers"])
    return {"final_response": f"Multi-agent response:\n{combined}\n— UniGPS",
            "audit": [f"Aggregated {len(state['completed_workers'])} results"]}

g2 = StateGraph(MultiWorkerState)
g2.add_node("supervisor", multi_supervisor)
g2.add_node("dispatch", dispatch_next)
g2.add_node("aggregate", multi_aggregate)

g2.add_edge(START, "supervisor")
g2.add_edge("supervisor", "dispatch")
g2.add_conditional_edges("dispatch", route_dispatch, {
    "dispatch": "dispatch",
    "aggregate": "aggregate",
})
g2.add_edge("aggregate", END)

app2 = g2.compile()

# Test with multi-domain request
result = app2.invoke({
    "request": "I need sick leave and also my laptop is broken",
    "pending_workers": [],
    "completed_workers": [],
    "final_response": "",
    "audit": [],
})
print(f"\nResponse:\n{result['final_response']}")
print(f"Audit: {result['audit']}")

# Another multi-domain request
result = app2.invoke({
    "request": "Submit my expense report and also I need a parking spot",
    "pending_workers": [],
    "completed_workers": [],
    "final_response": "",
    "audit": [],
})
print(f"\nResponse:\n{result['final_response']}")
print(f"Workers used: {[w['worker'] for w in result['completed_workers']]}")

print("\n" + "=" * 50)
print("Lab 01 Solution complete!")
print("- TODO 1: Facilities worker handles office/desk/parking/cafeteria")
print("- TODO 2: Multi-worker supervisor dispatches to HR + Tech for combined requests")
