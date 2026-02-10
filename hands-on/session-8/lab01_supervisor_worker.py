"""
Lab 01: Supervisor/Worker Basics
===================================
Goal: Build a supervisor/worker architecture where a central supervisor
      routes requests to specialized worker agents.

What you'll learn:
- Supervisor agent that classifies and routes requests
- Specialized worker nodes per domain
- Result flow back through the supervisor
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Supervisor/Worker Basics")
print("=" * 50)

# ============================================================
# Step 1: Simple supervisor with 3 workers
# ============================================================
# Pattern: supervisor → [hr_worker | tech_worker | finance_worker] → finalize

class TeamState(TypedDict):
    request: str
    assigned_to: str
    worker_output: str
    final_response: str
    audit: Annotated[list, add]

def supervisor(state: TeamState) -> dict:
    """Supervisor analyzes request and assigns to the right worker."""
    msg = state["request"].lower()
    if any(w in msg for w in ["leave", "sick", "wfh", "policy", "hr"]):
        assigned = "hr"
    elif any(w in msg for w in ["server", "bug", "deploy", "network", "laptop"]):
        assigned = "tech"
    elif any(w in msg for w in ["expense", "salary", "invoice", "budget"]):
        assigned = "finance"
    else:
        assigned = "general"
    print(f"  [supervisor] '{msg[:40]}' → assigned to: {assigned}")
    return {"assigned_to": assigned, "audit": [f"Supervisor assigned to {assigned}"]}

def route_to_worker(state: TeamState) -> str:
    """Routing function: returns the worker name."""
    return state["assigned_to"]

def hr_worker(state: TeamState) -> dict:
    print(f"  [HR worker] Processing: {state['request'][:40]}")
    return {
        "worker_output": f"HR Agent: Your request about '{state['request'][:30]}' has been logged. "
                         f"Check the HR portal for status.",
        "audit": ["HR worker processed request"],
    }

def tech_worker(state: TeamState) -> dict:
    print(f"  [Tech worker] Processing: {state['request'][:40]}")
    return {
        "worker_output": f"Tech Agent: We've created a Jira ticket for '{state['request'][:30]}'. "
                         f"A technician will respond within 4 hours.",
        "audit": ["Tech worker processed request"],
    }

def finance_worker(state: TeamState) -> dict:
    print(f"  [Finance worker] Processing: {state['request'][:40]}")
    return {
        "worker_output": f"Finance Agent: Your query about '{state['request'][:30]}' is being reviewed. "
                         f"Expected response within 2 business days.",
        "audit": ["Finance worker processed request"],
    }

def general_worker(state: TeamState) -> dict:
    print(f"  [General worker] Processing: {state['request'][:40]}")
    return {
        "worker_output": "General Agent: Your request has been received. We'll route it to the right team.",
        "audit": ["General worker processed request"],
    }

def finalize(state: TeamState) -> dict:
    print(f"  [finalize] Preparing response")
    return {
        "final_response": f"{state['worker_output']}\n— UniGPS Support",
        "audit": ["Response finalized"],
    }

# Build the graph
graph = StateGraph(TeamState)
graph.add_node("supervisor", supervisor)
graph.add_node("hr_worker", hr_worker)
graph.add_node("tech_worker", tech_worker)
graph.add_node("finance_worker", finance_worker)
graph.add_node("general_worker", general_worker)
graph.add_node("finalize", finalize)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges("supervisor", route_to_worker, {
    "hr": "hr_worker",
    "tech": "tech_worker",
    "finance": "finance_worker",
    "general": "general_worker",
})
graph.add_edge("hr_worker", "finalize")
graph.add_edge("tech_worker", "finalize")
graph.add_edge("finance_worker", "finalize")
graph.add_edge("general_worker", "finalize")
graph.add_edge("finalize", END)

app = graph.compile()

print("\nGraph: supervisor → [hr|tech|finance|general] → finalize → END\n")

# Test
test_requests = [
    "I need to apply for sick leave",
    "The production server is down",
    "How do I submit my expense report?",
    "Where is the cafeteria?",
]

for req in test_requests:
    result = app.invoke({"request": req, "audit": []})
    print(f"  Request: '{req}'")
    print(f"  → {result['final_response'][:60]}...")
    print(f"  Audit: {result['audit']}")
    print()

# ============================================================
# Step 2: Supervisor with re-routing
# ============================================================
# Supervisor checks worker output and can re-route if unsatisfied

print("\n--- Step 2: Supervisor with Quality Check ---\n")

class QATeamState(TypedDict):
    request: str
    assigned_to: str
    worker_output: str
    quality_ok: bool
    attempts: int
    max_attempts: int
    final_response: str
    audit: Annotated[list, add]

def qa_supervisor(state: QATeamState) -> dict:
    msg = state["request"].lower()
    if "leave" in msg or "hr" in msg:
        assigned = "hr"
    elif "server" in msg or "bug" in msg:
        assigned = "tech"
    else:
        assigned = "general"
    return {"assigned_to": assigned, "attempts": state["attempts"] + 1,
            "audit": [f"Attempt {state['attempts'] + 1}: assigned to {assigned}"]}

def qa_worker(state: QATeamState) -> dict:
    """Worker that sometimes produces short output."""
    assigned = state["assigned_to"]
    attempt = state["attempts"]
    # Simulate: first attempt might be too short
    if attempt == 1 and assigned == "general":
        output = "OK"
    else:
        output = f"{assigned.upper()} Agent: Your request has been thoroughly processed with detailed steps."
    return {"worker_output": output, "audit": [f"Worker produced: {output[:30]}"]}

def quality_check(state: QATeamState) -> dict:
    """Supervisor checks if worker output meets quality bar."""
    ok = len(state["worker_output"]) >= 20
    print(f"  [quality] Output length={len(state['worker_output'])}, OK={ok}")
    return {"quality_ok": ok, "audit": [f"Quality: {'PASS' if ok else 'FAIL'}"]}

def route_quality(state: QATeamState) -> str:
    if state["quality_ok"]:
        return "accept"
    if state["attempts"] >= state["max_attempts"]:
        return "accept"  # accept whatever we have
    return "retry"

def qa_finalize(state: QATeamState) -> dict:
    return {"final_response": f"{state['worker_output']}\n— UniGPS",
            "audit": ["Finalized"]}

g2 = StateGraph(QATeamState)
g2.add_node("supervisor", qa_supervisor)
g2.add_node("worker", qa_worker)
g2.add_node("quality_check", quality_check)
g2.add_node("finalize", qa_finalize)

g2.add_edge(START, "supervisor")
g2.add_edge("supervisor", "worker")
g2.add_edge("worker", "quality_check")
g2.add_conditional_edges("quality_check", route_quality, {
    "accept": "finalize",
    "retry": "supervisor",
})
g2.add_edge("finalize", END)
app2 = g2.compile()

# Test with a request that triggers retry
result = app2.invoke({
    "request": "What's the WiFi password?",
    "attempts": 0, "max_attempts": 3, "quality_ok": False,
    "assigned_to": "", "worker_output": "", "final_response": "", "audit": [],
})
print(f"  Attempts: {result['attempts']}")
print(f"  Response: {result['final_response'][:60]}...")
print(f"  Audit: {result['audit']}")

# ============================================================
# TODO 1: Add a "facilities" worker
# ============================================================
# Add a facilities_worker that handles requests about:
#   office, desk, parking, cafeteria, building, access card
# Update the supervisor to route to this new worker.
#
# Hint:
#   1. Add keyword detection in supervisor for "facilities"
#   2. Create a facilities_worker function
#   3. Add the node and edges to the graph
#
# def facilities_worker(state: TeamState) -> dict:
#     print(f"  [Facilities worker] Processing: {state['request'][:40]}")
#     return {
#         "worker_output": f"Facilities Agent: Your request about '{state['request'][:30]}' "
#                          "has been forwarded to the admin team.",
#         "audit": ["Facilities worker processed request"],
#     }
#
# Test with: "Where is the parking area?" and "I need an access card"


# ============================================================
# TODO 2: Add supervisor iteration (multi-worker)
# ============================================================
# Build a supervisor that can call MULTIPLE workers for one request.
# E.g., "I need leave and also a new laptop" → HR worker + Tech worker.
#
# Hint: Use a list in state for pending_workers and process them
#       in a loop via the supervisor re-routing back.
#
# class MultiWorkerState(TypedDict):
#     request: str
#     pending_workers: list          # workers still to call
#     completed_workers: Annotated[list, add]  # results collected
#     final_response: str
#     audit: Annotated[list, add]
#
# def multi_supervisor(state: MultiWorkerState) -> dict:
#     """Identify all domains and queue workers."""
#     msg = state["request"].lower()
#     workers = []
#     if any(w in msg for w in ["leave", "sick", "hr"]):
#         workers.append("hr")
#     if any(w in msg for w in ["laptop", "server", "bug"]):
#         workers.append("tech")
#     if any(w in msg for w in ["expense", "salary"]):
#         workers.append("finance")
#     if not workers:
#         workers.append("general")
#     print(f"  [multi_supervisor] Identified workers: {workers}")
#     return {"pending_workers": workers, "audit": [f"Workers queued: {workers}"]}
#
# def dispatch_next(state: MultiWorkerState) -> dict:
#     """Pop next worker from pending and execute."""
#     ...
#
# def route_dispatch(state: MultiWorkerState) -> str:
#     """Continue if pending_workers remain, else finalize."""
#     ...
#
# Test: "I need sick leave and also my laptop is broken"
# Expected: Both HR and Tech workers called


print("\n" + "=" * 50)
print("Lab 01 complete!")
print("Patterns: supervisor routing, quality check, re-routing")
