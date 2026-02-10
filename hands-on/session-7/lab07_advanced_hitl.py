"""
Lab 07: Advanced Human-in-the-Loop
=====================================
Goal: Build workflows with multi-gate approvals, user input collection
      mid-workflow, and timeout-based escalation.

What you'll learn:
- Multiple interrupt points in one workflow (multi-gate)
- Collecting user input via pause → update_state → resume
- Conditional interrupts (only pause for certain conditions)
- Timeout detection for paused workflows

Requires: GROQ_API_KEY in .env
"""

import os
from typing import TypedDict, Annotated
from operator import add
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

print("=" * 50)
print("  Advanced Human-in-the-Loop")
print("=" * 50)

# ============================================================
# Step 1: Multi-gate approval (two pause points)
# ============================================================

class DocState(TypedDict):
    topic: str
    draft: str
    reviewed: bool
    published: bool
    log: Annotated[list, add]

def create_draft(state: DocState) -> dict:
    """LLM creates a draft document."""
    prompt = f"Write a brief 3-sentence internal memo about: {state['topic']}"
    response = llm.invoke(prompt)
    draft = response.content.strip()
    print(f"  [draft] Created: {draft[:50]}...")
    return {"draft": draft, "log": ["Draft created"]}

def review_draft(state: DocState) -> dict:
    """Mark as reviewed (runs after first human approval)."""
    print(f"  [review] Draft reviewed and approved")
    return {"reviewed": True, "log": ["Draft reviewed"]}

def publish(state: DocState) -> dict:
    """Publish the document (runs after second human approval)."""
    print(f"  [publish] Document published!")
    return {"published": True, "log": ["Document published"]}

graph1 = StateGraph(DocState)
graph1.add_node("draft", create_draft)
graph1.add_node("review", review_draft)
graph1.add_node("publish", publish)

graph1.add_edge(START, "draft")
graph1.add_edge("draft", "review")
graph1.add_edge("review", "publish")
graph1.add_edge("publish", END)

memory1 = MemorySaver()
# TWO interrupt points!
app1 = graph1.compile(checkpointer=memory1, interrupt_before=["review", "publish"])

print("\n--- Step 1: Multi-Gate Approval ---")
print("Graph: draft → [GATE 1] → review → [GATE 2] → publish → END\n")

config1 = {"configurable": {"thread_id": "doc-001"}}

# Phase 1: Create draft, pause before review
app1.invoke({"topic": "New flexible work-from-home policy at UniGPS", "log": []}, config1)
snap = app1.get_state(config1)
print(f"GATE 1: Paused before '{snap.next}'")
print(f"  Draft: {snap.values['draft'][:60]}...")

# Gate 1: Human approves review
print("\n  [Human] Approves draft for review")
app1.invoke(None, config1)

# Now paused at Gate 2
snap = app1.get_state(config1)
print(f"\nGATE 2: Paused before '{snap.next}'")
print(f"  Reviewed: {snap.values['reviewed']}")

# Gate 2: Human approves publication
print("\n  [Human] Approves for publication")
result = app1.invoke(None, config1)
print(f"\nFinal: published={result['published']}")
print(f"Log: {result['log']}")

# ============================================================
# Step 2: User input collection mid-workflow
# ============================================================

class InputState(TypedDict):
    request_type: str
    question: str
    user_answer: str
    result: str
    log: Annotated[list, add]

def analyze_request(state: InputState) -> dict:
    """Analyze the request and determine what info we need."""
    req = state["request_type"]
    if req == "leave":
        question = "How many days of leave do you need?"
    elif req == "expense":
        question = "What is the expense amount in Rs?"
    else:
        question = "Please provide more details about your request."

    print(f"  [analyze] Need user input: '{question}'")
    return {"question": question, "log": [f"Question generated: {question}"]}

def process_answer(state: InputState) -> dict:
    """Process the user's answer."""
    prompt = (
        f"Process this support request:\n"
        f"Type: {state['request_type']}\n"
        f"Question asked: {state['question']}\n"
        f"User's answer: {state['user_answer']}\n"
        f"Provide a brief confirmation response."
    )
    response = llm.invoke(prompt)
    print(f"  [process] {response.content[:50]}...")
    return {"result": response.content.strip(), "log": ["Answer processed"]}

graph2 = StateGraph(InputState)
graph2.add_node("analyze", analyze_request)
graph2.add_node("process", process_answer)

graph2.add_edge(START, "analyze")
graph2.add_edge("analyze", "process")
graph2.add_edge("process", END)

memory2 = MemorySaver()
app2 = graph2.compile(checkpointer=memory2, interrupt_before=["process"])

print("\n\n--- Step 2: User Input Collection ---")
print("Graph: analyze → [PAUSE: user answers] → process → END\n")

config2 = {"configurable": {"thread_id": "input-001"}}

# Phase 1: Run until pause — system generates a question
app2.invoke({"request_type": "leave", "user_answer": "", "log": []}, config2)

# Read the question
snap = app2.get_state(config2)
print(f"System asks: '{snap.values['question']}'")

# Simulate user answering
user_response = "I need 5 days off starting next Monday"
print(f"User answers: '{user_response}'")
app2.update_state(config2, {
    "user_answer": user_response,
    "log": [f"User replied: {user_response}"],
})

# Resume
result = app2.invoke(None, config2)
print(f"Result: {result['result'][:80]}...")
print(f"Log: {result['log']}")

# ============================================================
# Step 3: Conditional interrupt (only pause when needed)
# ============================================================

class ExpenseState(TypedDict):
    employee: str
    description: str
    amount: int
    needs_approval: bool
    approved: bool
    log: Annotated[list, add]

def submit_expense(state: ExpenseState) -> dict:
    print(f"  [submit] {state['employee']}: Rs {state['amount']}")
    return {"log": [f"Submitted: Rs {state['amount']}"]}

def check_threshold(state: ExpenseState) -> dict:
    """Flag expenses over Rs 5000 for approval."""
    needs = state["amount"] > 5000
    print(f"  [check] Rs {state['amount']} → {'NEEDS APPROVAL' if needs else 'auto-approve'}")
    if not needs:
        return {"needs_approval": False, "approved": True, "log": ["Auto-approved"]}
    return {"needs_approval": True, "approved": False, "log": ["Flagged for approval"]}

def approval_gate(state: ExpenseState) -> dict:
    """This node runs after human approval (if needed)."""
    status = "approved" if state["approved"] else "pending"
    print(f"  [approval] Status: {status}")
    return {"log": [f"Approval status: {status}"]}

def finalize_expense(state: ExpenseState) -> dict:
    status = "APPROVED" if state["approved"] else "REJECTED"
    print(f"  [finalize] {status}")
    return {"log": [f"Finalized: {status}"]}

def route_by_threshold(state: ExpenseState) -> str:
    if state["needs_approval"]:
        return "needs_approval"
    return "auto_approved"

graph3 = StateGraph(ExpenseState)
graph3.add_node("submit", submit_expense)
graph3.add_node("check", check_threshold)
graph3.add_node("approval_gate", approval_gate)
graph3.add_node("finalize", finalize_expense)

graph3.add_edge(START, "submit")
graph3.add_edge("submit", "check")
graph3.add_conditional_edges("check", route_by_threshold, {
    "needs_approval": "approval_gate",
    "auto_approved": "finalize",
})
graph3.add_edge("approval_gate", "finalize")
graph3.add_edge("finalize", END)

memory3 = MemorySaver()
# Only pause before approval_gate (high-value expenses)
app3 = graph3.compile(checkpointer=memory3, interrupt_before=["approval_gate"])

print("\n\n--- Step 3: Conditional Interrupt ---")
print("Graph: submit → check → [auto→finalize | approval_gate→finalize] → END")
print("Only expenses > Rs 5000 pause for human approval.\n")

# Test: Small expense (no pause)
config_small = {"configurable": {"thread_id": "exp-small"}}
result = app3.invoke({
    "employee": "Priya", "description": "Team lunch", "amount": 800,
    "needs_approval": False, "approved": False, "log": [],
}, config_small)
snap = app3.get_state(config_small)
print(f"Small (Rs 800): approved={result['approved']}, paused={bool(snap.next)}")

# Test: Large expense (pauses!)
config_large = {"configurable": {"thread_id": "exp-large"}}
app3.invoke({
    "employee": "Vikram", "description": "Client dinner", "amount": 12000,
    "needs_approval": False, "approved": False, "log": [],
}, config_large)
snap = app3.get_state(config_large)
print(f"Large (Rs 12000): paused={bool(snap.next)}, next={snap.next}")

# Manager approves
app3.update_state(config_large, {"approved": True, "log": ["[MANAGER] Approved"]})
result = app3.invoke(None, config_large)
print(f"After approval: approved={result['approved']}")
print(f"Log: {result['log']}")

# ============================================================
# TODO 1: Edit draft before publishing
# ============================================================
# In Step 1, modify the multi-gate workflow so that at GATE 1,
# the human can EDIT the draft using update_state() before
# the review proceeds. Verify the edited version flows through.

# snap = app1.get_state(config)
# print(f"Original draft: {snap.values['draft']}")
# app1.update_state(config, {"draft": "My edited version..."})
# app1.invoke(None, config)  # Resume with edited draft

# ============================================================
# TODO 2: Implement rejection flow
# ============================================================
# In Step 3, if the manager REJECTS the expense (sets approved=False),
# add a "notify_rejection" node that sends a rejection message.
# Route: approval_gate → [approved→finalize | rejected→notify] → END

# def notify_rejection(state):
#     return {"log": [f"REJECTED: {state['employee']}'s expense of Rs {state['amount']}"]}
#
# def route_after_approval(state):
#     return "finalize" if state["approved"] else "notify_rejection"

print("\n\n" + "=" * 50)
print("Lab 07 complete! Key takeaways:")
print("- Multi-gate: interrupt_before=['a', 'b'] for multiple pauses")
print("- User input: pause → read question → update_state → resume")
print("- Conditional interrupt: only pause when state meets criteria")
print("- update_state() lets humans modify ANY state field")
print("- invoke(None, config) resumes from the exact pause point")
