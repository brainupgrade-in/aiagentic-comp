"""
Lab 07 Solution: Human-in-the-Loop
=====================================
"""

import os
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

print("=" * 50)
print("  Human-in-the-Loop (Solution)")
print("=" * 50)

# ============================================================
# Steps 1-5 same as lab — see lab file for details
# ============================================================

# (Email workflow and Review workflow run exactly as in lab)

# ============================================================
# TODO 1 Solution: Expense Approval Workflow
# ============================================================

class ExpenseState(TypedDict):
    employee: str
    description: str
    amount: int
    flagged: bool
    approved: bool
    reason: str
    log: Annotated[list, add]

def submit_expense(state: ExpenseState) -> dict:
    """Capture expense submission."""
    print(f"  [submit] {state['employee']}: Rs {state['amount']} — {state['description']}")
    return {"log": [f"Submitted: Rs {state['amount']} by {state['employee']}"]}

def validate_expense(state: ExpenseState) -> dict:
    """Check if expense needs manager review."""
    flagged = state["amount"] > 5000
    status = "FLAGGED for review" if flagged else "Auto-eligible"
    print(f"  [validate] Rs {state['amount']} → {status}")
    return {
        "flagged": flagged,
        "log": [f"Validated: {status}"],
    }

def approve_expense(state: ExpenseState) -> dict:
    """Mark as approved (runs after human review if flagged)."""
    # If not flagged, auto-approve
    if not state["flagged"]:
        print(f"  [approve] Auto-approved (Rs {state['amount']} <= 5000)")
        return {
            "approved": True,
            "reason": "Auto-approved: under Rs 5000 threshold",
            "log": ["Auto-approved"],
        }
    # If flagged, the human should have set approved via update_state
    status = "APPROVED by manager" if state.get("approved") else "REJECTED by manager"
    print(f"  [approve] {status}")
    return {
        "log": [f"Manager decision: {status}"],
    }

graph1 = StateGraph(ExpenseState)
graph1.add_node("submit", submit_expense)
graph1.add_node("validate", validate_expense)
graph1.add_node("approve", approve_expense)
graph1.add_edge(START, "submit")
graph1.add_edge("submit", "validate")
graph1.add_edge("validate", "approve")
graph1.add_edge("approve", END)

memory1 = MemorySaver()
app1 = graph1.compile(checkpointer=memory1, interrupt_before=["approve"])

print("\n--- TODO 1: Expense Approval Workflow ---")
print("Graph: START → submit → validate → [PAUSE] → approve → END\n")

# Test 1: Small expense (auto-approve)
print("Test 1: Small expense")
config_a = {"configurable": {"thread_id": "expense-001"}}
app1.invoke({
    "employee": "Priya", "description": "Team lunch", "amount": 450,
    "flagged": False, "approved": False, "reason": "", "log": [],
}, config_a)

snap = app1.get_state(config_a)
print(f"  Paused. Flagged: {snap.values['flagged']}")
# Human approves (it's small, just let it through)
result = app1.invoke(None, config_a)
print(f"  Result: approved={result['approved']}, reason={result['reason']}")
print(f"  Log: {result['log']}")

# Test 2: Large expense (needs manager review)
print("\nTest 2: Large expense")
config_b = {"configurable": {"thread_id": "expense-002"}}
app1.invoke({
    "employee": "Vikram", "description": "Client dinner at Taj", "amount": 8500,
    "flagged": False, "approved": False, "reason": "", "log": [],
}, config_b)

snap = app1.get_state(config_b)
print(f"  Paused. Flagged: {snap.values['flagged']}, Amount: Rs {snap.values['amount']}")

# Manager approves
print("  [Manager reviews and APPROVES]")
app1.update_state(config_b, {
    "approved": True,
    "reason": "Approved: valid client entertainment expense",
    "log": ["[MANAGER] Reviewed and approved"],
})
result = app1.invoke(None, config_b)
print(f"  Result: approved={result['approved']}, reason={result['reason']}")
print(f"  Log: {result['log']}")

# Test 3: Large expense — manager REJECTS
print("\nTest 3: Large expense (rejected)")
config_c = {"configurable": {"thread_id": "expense-003"}}
app1.invoke({
    "employee": "Rahul", "description": "Personal shopping", "amount": 12000,
    "flagged": False, "approved": False, "reason": "", "log": [],
}, config_c)

snap = app1.get_state(config_c)
print(f"  Paused. Flagged: {snap.values['flagged']}, Amount: Rs {snap.values['amount']}")

# Manager rejects
print("  [Manager reviews and REJECTS]")
app1.update_state(config_c, {
    "approved": False,
    "reason": "Rejected: personal expense not covered by policy",
    "log": ["[MANAGER] Reviewed and rejected"],
})
result = app1.invoke(None, config_c)
print(f"  Result: approved={result['approved']}, reason={result['reason']}")
print(f"  Log: {result['log']}")

# ============================================================
# TODO 2 Solution: Multi-gate workflow (two pauses)
# ============================================================

class MultiGateState(TypedDict):
    request: str
    draft: str
    reviewed: bool
    sent: bool
    log: Annotated[list, add]

def create_draft(state: MultiGateState) -> dict:
    prompt = f"Draft a brief 2-sentence professional email for: {state['request']}"
    response = llm.invoke(prompt)
    draft = response.content.strip()
    print(f"  [draft] Created: {draft[:50]}...")
    return {"draft": draft, "log": ["Draft created"]}

def review_draft(state: MultiGateState) -> dict:
    print(f"  [review] Reviewing draft...")
    return {"reviewed": True, "log": ["Draft reviewed and approved"]}

def send_message(state: MultiGateState) -> dict:
    print(f"  [send] Sending: {state['draft'][:40]}...")
    return {"sent": True, "log": ["Message sent!"]}

graph2 = StateGraph(MultiGateState)
graph2.add_node("draft", create_draft)
graph2.add_node("review", review_draft)
graph2.add_node("send", send_message)
graph2.add_edge(START, "draft")
graph2.add_edge("draft", "review")
graph2.add_edge("review", "send")
graph2.add_edge("send", END)

memory2 = MemorySaver()
# TWO interrupt points!
app2 = graph2.compile(checkpointer=memory2, interrupt_before=["review", "send"])

print("\n--- TODO 2: Multi-Gate Workflow ---")
print("Graph: START → draft → [PAUSE 1] → review → [PAUSE 2] → send → END\n")

config_d = {"configurable": {"thread_id": "multi-001"}}

# Phase 1: Draft is created, pauses before review
app2.invoke({"request": "Announce team outing on Friday", "reviewed": False, "sent": False, "log": []}, config_d)
snap = app2.get_state(config_d)
print(f"PAUSE 1: Before review. Next: {snap.next}")
print(f"  Draft: {snap.values['draft'][:60]}...")

# Human approves review
print("\n  [Human approves for review]")
result = app2.invoke(None, config_d)

# Now paused again before send
snap = app2.get_state(config_d)
print(f"\nPAUSE 2: Before send. Next: {snap.next}")
print(f"  Reviewed: {snap.values['reviewed']}")

# Human approves sending
print("\n  [Human approves sending]")
result = app2.invoke(None, config_d)
print(f"\nFinal: sent={result['sent']}")
print(f"Log: {result['log']}")
print("→ Two human approvals were required before the message was sent!")

print("\n" + "=" * 50)
print("Lab 07 Solution complete!")
print("- TODO 1: Expense approval with flagging > Rs 5000")
print("- TODO 2: Multi-gate with TWO interrupt_before points")
