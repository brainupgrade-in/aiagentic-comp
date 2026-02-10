"""
Lab 07: Human-in-the-Loop
===========================
Goal: Build workflows that pause for human approval, allow state
      editing, and resume execution.

What you'll learn:
- interrupt_before: pause before a node runs
- interrupt_after: pause after a node runs
- get_state() to inspect the paused state
- update_state() to modify state before resuming
- invoke(None, config) to resume a paused workflow

Requires: GROQ_API_KEY in .env
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
print("  Human-in-the-Loop")
print("=" * 50)

# ============================================================
# Step 1: Basic interrupt_before
# ============================================================
# Scenario: Draft an email, then PAUSE for human review before sending.

class EmailState(TypedDict):
    request: str
    draft: str
    sent: bool
    log: Annotated[list, add]

def draft_email(state: EmailState) -> dict:
    """LLM drafts an email based on the request."""
    prompt = (
        f"Draft a brief professional email (2-3 sentences) for this request:\n"
        f"{state['request']}\n"
        f"Include a subject line. Format as:\nSubject: ...\nBody: ..."
    )
    response = llm.invoke(prompt)
    draft = response.content.strip()
    print(f"  [draft_email] Draft created ({len(draft)} chars)")
    return {"draft": draft, "log": ["Email drafted"]}

def send_email(state: EmailState) -> dict:
    """Simulate sending the email."""
    print(f"  [send_email] SENDING: {state['draft'][:50]}...")
    return {"sent": True, "log": ["Email sent!"]}

graph1 = StateGraph(EmailState)
graph1.add_node("draft", draft_email)
graph1.add_node("send", send_email)
graph1.add_edge(START, "draft")
graph1.add_edge("draft", "send")
graph1.add_edge("send", END)

# ← KEY: interrupt_before="send" — pause BEFORE sending!
memory1 = MemorySaver()
app1 = graph1.compile(checkpointer=memory1, interrupt_before=["send"])

print("\n--- Step 1: interrupt_before ---")
print("Graph: START → draft → [PAUSE] → send → END\n")

config1 = {"configurable": {"thread_id": "email-001"}}

# Run — this will PAUSE before the "send" node
result = app1.invoke(
    {"request": "Tell the team about Friday's team lunch at 1 PM", "log": []},
    config1
)

# Check the paused state
snapshot = app1.get_state(config1)
print(f"Workflow paused!")
print(f"Next node: {snapshot.next}")
print(f"Draft preview:\n{snapshot.values['draft']}\n")
print(f"Sent: {snapshot.values.get('sent', False)}")
print("→ The email was drafted but NOT sent yet!")

# ============================================================
# Step 2: Resume the paused workflow
# ============================================================
# Human has reviewed the draft and approves it.

print("\n--- Step 2: Resume (Human Approves) ---")

# Resume by passing None — "continue from where you paused"
result = app1.invoke(None, config1)

print(f"After resume:")
print(f"Sent: {result['sent']}")
print(f"Log: {result['log']}")
print("→ The email was sent after human approval!")

# ============================================================
# Step 3: Modify state before resuming
# ============================================================
# What if the human wants to EDIT the draft before sending?

print("\n--- Step 3: Edit State Before Resume ---")

config2 = {"configurable": {"thread_id": "email-002"}}

# Run until pause
app1.invoke(
    {"request": "Notify the team about server maintenance on Saturday", "log": []},
    config2
)

# Inspect the draft
snapshot = app1.get_state(config2)
print(f"Original draft:\n{snapshot.values['draft']}\n")

# Human edits the draft
edited_draft = "Subject: Server Maintenance - Saturday 10 PM\nBody: Hi team, planned maintenance this Saturday at 10 PM IST. Expected downtime: 2 hours. Please save your work before 9:45 PM."

# Update the state with the human's edit
app1.update_state(config2, {"draft": edited_draft, "log": ["[HUMAN] Draft edited"]})

print(f"Human edited the draft!")
print(f"Updated draft:\n{edited_draft}\n")

# Now resume — the send node will use the edited draft
result = app1.invoke(None, config2)
print(f"Sent with edited draft: {result['sent']}")
print(f"Log: {result['log']}")
print("→ Human modified the draft, then the workflow resumed with the changes!")

# ============================================================
# Step 4: interrupt_after — pause AFTER a node runs
# ============================================================

class ReviewState(TypedDict):
    request: str
    analysis: str
    decision: str
    log: Annotated[list, add]

def analyze_request(state: ReviewState) -> dict:
    """LLM analyzes the request."""
    prompt = (
        f"Analyze this support request and provide a brief assessment "
        f"(2 sentences) including urgency and recommended action:\n"
        f"{state['request']}"
    )
    response = llm.invoke(prompt)
    analysis = response.content.strip()
    print(f"  [analyze] {analysis[:60]}...")
    return {"analysis": analysis, "log": ["Request analyzed"]}

def make_decision(state: ReviewState) -> dict:
    """Make a final decision based on the analysis."""
    prompt = (
        f"Based on this analysis, what should we do? "
        f"Reply with exactly: APPROVE, ESCALATE, or REJECT.\n"
        f"Analysis: {state['analysis']}"
    )
    response = llm.invoke(prompt)
    decision = response.content.strip().upper()
    if decision not in ["APPROVE", "ESCALATE", "REJECT"]:
        decision = "ESCALATE"
    print(f"  [decision] → {decision}")
    return {"decision": decision, "log": [f"Decision: {decision}"]}

graph2 = StateGraph(ReviewState)
graph2.add_node("analyze", analyze_request)
graph2.add_node("decide", make_decision)
graph2.add_edge(START, "analyze")
graph2.add_edge("analyze", "decide")
graph2.add_edge("decide", END)

# ← interrupt_after="analyze" — pause AFTER analysis is done
memory2 = MemorySaver()
app2 = graph2.compile(checkpointer=memory2, interrupt_after=["analyze"])

print("\n--- Step 4: interrupt_after ---")
print("Graph: START → analyze → [PAUSE] → decide → END\n")

config3 = {"configurable": {"thread_id": "review-001"}}

# Run — pauses AFTER analyze completes
app2.invoke({"request": "Employee requests transfer to Bangalore office", "log": []}, config3)

# Inspect the analysis before the decision is made
snapshot = app2.get_state(config3)
print(f"Paused after analysis!")
print(f"Analysis: {snapshot.values['analysis']}")
print(f"Next node: {snapshot.next}")
print(f"Decision: {snapshot.values.get('decision', 'Not yet made')}")

# Human reviews the analysis and lets it proceed
print("\n[Human reviews analysis and approves...]")
result = app2.invoke(None, config3)
print(f"Final decision: {result['decision']}")
print(f"Log: {result['log']}")

# ============================================================
# Step 5: Summary — interrupt_before vs interrupt_after
# ============================================================

print("\n--- Step 5: Comparison ---")
print("""
  interrupt_before=["send"]     interrupt_after=["analyze"]
  ─────────────────────────     ──────────────────────────
  Pauses BEFORE node runs       Pauses AFTER node completes
  Use: approve actions           Use: review outputs
  Example: send email,           Example: review analysis,
           make payment                   check classification
           delete data                    verify LLM output
""")

# ============================================================
# TODO 1: Build an approval workflow
# ============================================================
# Create a workflow for expense approval:
# 1. "submit" node: captures expense details (amount, description)
# 2. "validate" node: checks if amount > 5000 (flag for review)
# 3. "approve" node: marks as approved
# Use interrupt_before=["approve"] so a human reviews first.
# If amount > 5000, the human can update_state to reject.

# class ExpenseState(TypedDict):
#     description: str
#     amount: int
#     flagged: bool
#     approved: bool
#     log: Annotated[list, add]

# ============================================================
# TODO 2: Multi-gate workflow
# ============================================================
# Create a workflow with TWO interrupt points:
# 1. START → draft → [PAUSE] → review → [PAUSE] → send → END
# Use: interrupt_before=["review", "send"]
# This requires TWO human approvals before sending.

print("\n" + "=" * 50)
print("Lab 07 complete! Key takeaways:")
print("- interrupt_before: pause BEFORE a node (approve actions)")
print("- interrupt_after: pause AFTER a node (review outputs)")
print("- get_state(): inspect the paused workflow state")
print("- update_state(): modify state before resuming")
print("- invoke(None, config): resume from the pause point")
print("- Requires a checkpointer (MemorySaver) to work")
