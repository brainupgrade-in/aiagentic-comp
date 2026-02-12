"""
Lab 04 Solution: State Reducers
=================================
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  State Reducers (Solution)")
print("=" * 50)

# ============================================================
# Steps 1-4: Same as lab (see lab file for overwrite/append demos)
# ============================================================

# --- Step 1: Overwrite ---
class OverwriteState(TypedDict):
    value: str

def node_a(state: OverwriteState) -> dict:
    return {"value": "set by node_a"}

def node_b(state: OverwriteState) -> dict:
    return {"value": "set by node_b"}

graph1 = StateGraph(OverwriteState)
graph1.add_node("a", node_a)
graph1.add_node("b", node_b)
graph1.add_edge(START, "a")
graph1.add_edge("a", "b")
graph1.add_edge("b", END)

app1 = graph1.compile()
result = app1.invoke({"value": "initial"})
print(f"\n--- Overwrite: '{result['value']}' (last write wins) ---")

# --- Step 2: Append ---
class AppendState(TypedDict):
    log: Annotated[list, add]

def step_one(state: AppendState) -> dict:
    return {"log": ["Step 1 completed"]}

def step_two(state: AppendState) -> dict:
    return {"log": ["Step 2 completed"]}

def step_three(state: AppendState) -> dict:
    return {"log": ["Step 3 completed"]}

graph2 = StateGraph(AppendState)
graph2.add_node("one", step_one)
graph2.add_node("two", step_two)
graph2.add_node("three", step_three)
graph2.add_edge(START, "one")
graph2.add_edge("one", "two")
graph2.add_edge("two", "three")
graph2.add_edge("three", END)

app2 = graph2.compile()
result = app2.invoke({"log": ["Workflow started"]})
print(f"\n--- Append: {result['log']} ---")

# ============================================================
# TODO 1 Solution: Counter reducer
# ============================================================

class CounterState(TypedDict):
    data: str
    steps_completed: Annotated[list, add]

def step_a(state: CounterState) -> dict:
    return {"steps_completed": ["step_a"]}

def step_b(state: CounterState) -> dict:
    return {"steps_completed": ["step_b"]}

def step_c(state: CounterState) -> dict:
    return {"steps_completed": ["step_c"]}

graph_counter = StateGraph(CounterState)
graph_counter.add_node("a", step_a)
graph_counter.add_node("b", step_b)
graph_counter.add_node("c", step_c)
graph_counter.add_edge(START, "a")
graph_counter.add_edge("a", "b")
graph_counter.add_edge("b", "c")
graph_counter.add_edge("c", END)

app_counter = graph_counter.compile()
result = app_counter.invoke({"data": "test", "steps_completed": []})

print("\n--- TODO 1: Counter Reducer ---")
print(f"Steps completed: {len(result['steps_completed'])}")
print(f"Order: {result['steps_completed']}")

# ============================================================
# TODO 2 Solution: Conditional audit trail
# ============================================================

class AuditState(TypedDict):
    request: str
    category: str
    approved: bool
    audit_trail: Annotated[list, add]

def receive_request(state: AuditState) -> dict:
    return {"audit_trail": [f"[RECEIVED] Request: {state['request']}"]}

def classify_request(state: AuditState) -> dict:
    req = state["request"].lower()
    if "expense" in req:
        cat = "finance"
    elif "leave" in req:
        cat = "hr"
    else:
        cat = "general"
    return {
        "category": cat,
        "audit_trail": [f"[CLASSIFIED] Category: {cat}"],
    }

def route_approval(state: AuditState) -> str:
    """Route: finance goes to manual_review, others to auto_approve."""
    if state["category"] == "finance":
        return "manual_review"
    return "auto_approve"

def auto_approve(state: AuditState) -> dict:
    return {
        "approved": True,
        "audit_trail": [f"[AUTO-APPROVED] Non-finance request auto-approved"],
    }

def manual_review(state: AuditState) -> dict:
    return {
        "approved": False,
        "audit_trail": [f"[MANUAL REVIEW] Finance request requires manager approval"],
    }

def finalize(state: AuditState) -> dict:
    status = "APPROVED" if state["approved"] else "PENDING REVIEW"
    return {"audit_trail": [f"[FINALIZED] Status: {status}"]}

graph_audit = StateGraph(AuditState)
graph_audit.add_node("receive", receive_request)
graph_audit.add_node("classify", classify_request)
graph_audit.add_node("auto_approve", auto_approve)
graph_audit.add_node("manual_review", manual_review)
graph_audit.add_node("finalize", finalize)

graph_audit.add_edge(START, "receive")
graph_audit.add_edge("receive", "classify")

# Conditional routing!
graph_audit.add_conditional_edges(
    "classify",
    route_approval,
    {
        "auto_approve": "auto_approve",
        "manual_review": "manual_review",
    }
)

# Both paths converge to finalize
graph_audit.add_edge("auto_approve", "finalize")
graph_audit.add_edge("manual_review", "finalize")
graph_audit.add_edge("finalize", END)

app_audit = graph_audit.compile()

print("\n--- TODO 2: Conditional Audit Trail ---")
print("Graph: receive → classify → [auto_approve | manual_review] → finalize → END\n")

for request in ["Apply for annual leave", "Submit expense report for Rs 5000"]:
    print(f"Request: '{request}'")
    result = app_audit.invoke({"request": request})
    print(f"  Category: {result['category']}")
    print(f"  Approved: {result['approved']}")
    print(f"  Audit trail:")
    for entry in result["audit_trail"]:
        print(f"    {entry}")
    print()

print("=" * 50)
print("Lab 04 Solution complete!")
print("- TODO 1: Counter reducer tracks step names and counts")
print("- TODO 2: Finance → manual_review, others → auto_approve")
