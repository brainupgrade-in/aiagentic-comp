"""
Lab 07 Solution: Advanced Human-in-the-Loop
==============================================
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
print("  Advanced Human-in-the-Loop (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Edit draft before publishing
# ============================================================

class DocState(TypedDict):
    topic: str
    draft: str
    reviewed: bool
    published: bool
    log: Annotated[list, add]

def create_draft(state: DocState) -> dict:
    prompt = f"Write a brief 3-sentence internal memo about: {state['topic']}"
    response = llm.invoke(prompt)
    draft = response.content.strip()
    print(f"  [draft] Created: {draft[:50]}...")
    return {"draft": draft, "log": ["Draft created"]}

def review_draft(state: DocState) -> dict:
    print(f"  [review] Reviewing draft...")
    return {"reviewed": True, "log": ["Draft reviewed"]}

def publish(state: DocState) -> dict:
    print(f"  [publish] Publishing!")
    return {"published": True, "log": ["Published"]}

graph1 = StateGraph(DocState)
graph1.add_node("draft", create_draft)
graph1.add_node("review", review_draft)
graph1.add_node("publish", publish)
graph1.add_edge(START, "draft")
graph1.add_edge("draft", "review")
graph1.add_edge("review", "publish")
graph1.add_edge("publish", END)

memory1 = MemorySaver()
app1 = graph1.compile(checkpointer=memory1, interrupt_before=["review", "publish"])

print("\n--- TODO 1: Edit Draft Before Publishing ---\n")

config = {"configurable": {"thread_id": "edit-001"}}

# Phase 1: Create draft
app1.invoke({"topic": "Updated dress code policy for UniGPS", "log": []}, config)
snap = app1.get_state(config)
print(f"Original draft: {snap.values['draft'][:60]}...")

# Human EDITS the draft before review
edited = "Team, please note: Business casual is now the standard dress code. Formal wear is only required for client meetings. This takes effect from next Monday."
app1.update_state(config, {"draft": edited, "log": ["[HUMAN] Edited draft"]})
print(f"Edited draft: {edited[:60]}...")

# Gate 1: Resume (review uses edited draft)
app1.invoke(None, config)
snap = app1.get_state(config)
print(f"Reviewed: {snap.values['reviewed']}")

# Gate 2: Approve publication
result = app1.invoke(None, config)
print(f"Published: {result['published']}")
print(f"Final draft: {result['draft'][:60]}...")
print(f"Log: {result['log']}")
print("→ The EDITED version was reviewed and published!")

# ============================================================
# TODO 2 Solution: Rejection flow
# ============================================================

class ExpenseState(TypedDict):
    employee: str
    description: str
    amount: int
    needs_approval: bool
    approved: bool
    response: str
    log: Annotated[list, add]

def submit(state: ExpenseState) -> dict:
    print(f"  [submit] {state['employee']}: Rs {state['amount']}")
    return {"log": [f"Submitted: Rs {state['amount']}"]}

def check_threshold(state: ExpenseState) -> dict:
    needs = state["amount"] > 5000
    if not needs:
        return {"needs_approval": False, "approved": True, "log": ["Auto-approved (under Rs 5000)"]}
    return {"needs_approval": True, "approved": False, "log": ["Flagged for approval"]}

def approval_gate(state: ExpenseState) -> dict:
    return {"log": ["At approval gate"]}

def route_threshold(state: ExpenseState) -> str:
    return "needs_approval" if state["needs_approval"] else "auto_approved"

def finalize(state: ExpenseState) -> dict:
    return {
        "response": f"APPROVED: Rs {state['amount']} expense for {state['employee']}",
        "log": ["Finalized: APPROVED"],
    }

def notify_rejection(state: ExpenseState) -> dict:
    """Notify employee of rejection."""
    print(f"  [reject] Notifying {state['employee']} of rejection")
    return {
        "response": f"REJECTED: Rs {state['amount']} expense for {state['employee']}. Contact your manager.",
        "log": [f"Rejection notification sent to {state['employee']}"],
    }

def route_after_approval(state: ExpenseState) -> str:
    return "finalize" if state["approved"] else "notify_rejection"

graph2 = StateGraph(ExpenseState)
graph2.add_node("submit", submit)
graph2.add_node("check", check_threshold)
graph2.add_node("approval_gate", approval_gate)
graph2.add_node("finalize", finalize)
graph2.add_node("notify_rejection", notify_rejection)

graph2.add_edge(START, "submit")
graph2.add_edge("submit", "check")
graph2.add_conditional_edges("check", route_threshold, {
    "needs_approval": "approval_gate",
    "auto_approved": "finalize",
})
graph2.add_conditional_edges("approval_gate", route_after_approval, {
    "finalize": "finalize",
    "notify_rejection": "notify_rejection",
})
graph2.add_edge("finalize", END)
graph2.add_edge("notify_rejection", END)

memory2 = MemorySaver()
app2 = graph2.compile(checkpointer=memory2, interrupt_before=["approval_gate"])

print("\n\n--- TODO 2: Rejection Flow ---")
print("Graph: submit → check → [auto→finalize | gate→[finalize|reject]] → END\n")

# Test: Manager APPROVES
config_a = {"configurable": {"thread_id": "rej-001"}}
app2.invoke({
    "employee": "Vikram", "description": "Client dinner", "amount": 8000,
    "needs_approval": False, "approved": False, "response": "", "log": [],
}, config_a)
print("Manager APPROVES:")
app2.update_state(config_a, {"approved": True, "log": ["[MANAGER] Approved"]})
result = app2.invoke(None, config_a)
print(f"  Response: {result['response']}")
print(f"  Log: {result['log']}")

# Test: Manager REJECTS
config_b = {"configurable": {"thread_id": "rej-002"}}
app2.invoke({
    "employee": "Rahul", "description": "Personal shopping", "amount": 15000,
    "needs_approval": False, "approved": False, "response": "", "log": [],
}, config_b)
print("\nManager REJECTS:")
app2.update_state(config_b, {"approved": False, "log": ["[MANAGER] Rejected: not business expense"]})
result = app2.invoke(None, config_b)
print(f"  Response: {result['response']}")
print(f"  Log: {result['log']}")

print("\n" + "=" * 50)
print("Lab 07 Solution complete!")
print("- TODO 1: Human edits draft via update_state before review")
print("- TODO 2: Rejection routes to notify_rejection node")
