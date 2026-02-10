"""
Lab 04: State Reducers
========================
Goal: Learn how Annotated fields with reducers accumulate state
      across nodes instead of overwriting it.

What you'll learn:
- The difference between overwrite (default) and append (reducer)
- How Annotated[list, add] appends to lists
- Building a message/log accumulator across nodes
- Why reducers matter for conversation history
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  State Reducers")
print("=" * 50)

# ============================================================
# Step 1: Default behavior — overwrite
# ============================================================

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

print("\n--- Step 1: Overwrite Behavior ---")
print(f"Input:  'initial'")
print(f"After node_a: 'set by node_a'")
print(f"After node_b: '{result['value']}'")
print("→ Last node's value wins (overwrite)")

# ============================================================
# Step 2: Reducer behavior — append
# ============================================================

class AppendState(TypedDict):
    log: Annotated[list, add]  # ← reducer: append, don't overwrite!

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

print("\n--- Step 2: Append (Reducer) Behavior ---")
print(f"Log: {result['log']}")
print("→ Each node APPENDS to the list instead of overwriting!")

# ============================================================
# Step 3: Realistic example — audit trail
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

def auto_approve(state: AuditState) -> dict:
    # Auto-approve non-finance requests
    approved = state["category"] != "finance"
    return {
        "approved": approved,
        "audit_trail": [f"[APPROVAL] {'Auto-approved' if approved else 'Requires manual review'}"],
    }

def finalize(state: AuditState) -> dict:
    status = "APPROVED" if state["approved"] else "PENDING REVIEW"
    return {"audit_trail": [f"[FINALIZED] Status: {status}"]}

graph3 = StateGraph(AuditState)
graph3.add_node("receive", receive_request)
graph3.add_node("classify", classify_request)
graph3.add_node("approve", auto_approve)
graph3.add_node("finalize", finalize)
graph3.add_edge(START, "receive")
graph3.add_edge("receive", "classify")
graph3.add_edge("classify", "approve")
graph3.add_edge("approve", "finalize")
graph3.add_edge("finalize", END)

app3 = graph3.compile()

print("\n--- Step 3: Audit Trail ---")
for request in ["Apply for annual leave", "Submit expense report for Rs 5000"]:
    print(f"\nRequest: '{request}'")
    result = app3.invoke({"request": request})
    print(f"  Category: {result['category']}")
    print(f"  Approved: {result['approved']}")
    print(f"  Audit trail:")
    for entry in result["audit_trail"]:
        print(f"    {entry}")

# ============================================================
# Step 4: Mixing overwrite and append fields
# ============================================================

print("\n--- Step 4: Mixed Fields ---")
print("'category' and 'approved' OVERWRITE (last write wins)")
print("'audit_trail' APPENDS (accumulates across all nodes)")
print("This lets you track the full history while keeping current values!")

# ============================================================
# TODO 1: Add a counter reducer
# ============================================================
# Create a state with a field: steps_completed: Annotated[list, add]
# Each node should append its name. At the end, print the total
# number of steps by checking len(state["steps_completed"]).

# class CounterState(TypedDict):
#     data: str
#     steps_completed: Annotated[list, add]
#
# def step_a(state): return {"steps_completed": ["step_a"]}
# def step_b(state): return {"steps_completed": ["step_b"]}
# def step_c(state): return {"steps_completed": ["step_c"]}
#
# Build graph, invoke, then:
# print(f"Steps completed: {len(result['steps_completed'])}")
# print(f"Order: {result['steps_completed']}")

# ============================================================
# TODO 2: Conditional audit trail
# ============================================================
# Modify the audit trail example to add conditional routing:
# Finance requests go to "manual_review" node, others go to
# "auto_approve". Both converge to "finalize".
# Each path should add its own audit trail entry.

print("\n" + "=" * 50)
print("Lab 04 complete! Key takeaways:")
print("- Default: fields are OVERWRITTEN by each node")
print("- Annotated[list, add]: values are APPENDED (reducer)")
print("- Reducers are perfect for logs, audit trails, message history")
print("- Mix both: overwrite for 'current' values, append for history")
print("- The operator.add function concatenates lists")
