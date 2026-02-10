"""
Lab 08: Challenge — UniGPS Support Request Workflow
=====================================================
Goal: Build a complete LangGraph workflow that combines everything
      from this session: state, conditional routing, reducers,
      cycles, checkpointing, and human-in-the-loop.

Scenario:
  UniGPS receives support requests from employees. Build a workflow that:
  1. Receives and classifies the request (HR, Tech, Finance)
  2. Routes to the appropriate handler
  3. Generates a response using LLM
  4. For Finance requests > Rs 5000: pause for manager approval (HITL)
  5. Maintains a full audit trail (reducer)
  6. If response quality is low, retry (cycle)
  7. Uses checkpointing to track state

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

print("=" * 60)
print("  Challenge: UniGPS Support Request Workflow")
print("=" * 60)

# ============================================================
# YOUR TASK: Build the complete workflow
# ============================================================
#
# State definition (provided):

class SupportRequest(TypedDict):
    # Input
    employee_name: str
    message: str
    # Processing
    category: str           # hr, tech, finance
    priority: str           # LOW, MEDIUM, HIGH
    amount: int             # For finance requests (Rs)
    # Output
    response: str
    approved: bool
    # Tracking
    audit_trail: Annotated[list, add]  # ← reducer!

# ============================================================
# STEP 1: Create the nodes
# ============================================================
# Implement these nodes:

# def receive_request(state) -> dict:
#     """Log receipt of the request. Add to audit trail."""
#     # Return: audit_trail entry
#     pass

# def classify_request(state) -> dict:
#     """Use LLM to classify into hr/tech/finance.
#        Also detect priority (HIGH if "urgent"/"critical" in message).
#        For finance: extract amount if mentioned."""
#     # Return: category, priority, amount, audit_trail entry
#     pass

# def handle_hr(state) -> dict:
#     """Use LLM to generate HR-specific response."""
#     # Return: response, audit_trail entry
#     pass

# def handle_tech(state) -> dict:
#     """Use LLM to generate Tech-specific response."""
#     # Return: response, audit_trail entry
#     pass

# def handle_finance(state) -> dict:
#     """Use LLM to generate Finance-specific response.
#        If amount > 5000, set approved=False (needs manager)."""
#     # Return: response, approved, audit_trail entry
#     pass

# def finalize(state) -> dict:
#     """Create final audit entry with status."""
#     # Return: audit_trail entry with final status
#     pass

# ============================================================
# STEP 2: Create the routing function
# ============================================================

# def route_to_handler(state) -> str:
#     """Route based on category."""
#     # Return: "handle_hr", "handle_tech", or "handle_finance"
#     pass

# ============================================================
# STEP 3: Build the graph
# ============================================================
# Graph structure:
#   START → receive → classify → [route] → handle_* → finalize → END
#
# For finance with amount > 5000:
#   Use interrupt_before=["finalize"] so manager can approve/reject

# graph = StateGraph(SupportRequest)
# ... add nodes ...
# ... add edges (including conditional edges for routing) ...
# memory = MemorySaver()
# app = graph.compile(checkpointer=memory, interrupt_before=["finalize"])

# ============================================================
# STEP 4: Test the workflow
# ============================================================
# Test with these requests:

test_requests = [
    {
        "employee_name": "Priya Sharma",
        "message": "I need to apply for maternity leave starting next month",
        "thread_id": "req-001",
    },
    {
        "employee_name": "Vikram Patel",
        "message": "URGENT: Production database is down, all services affected",
        "thread_id": "req-002",
    },
    {
        "employee_name": "Anita Desai",
        "message": "Please reimburse my travel expense of Rs 8500 for the client visit",
        "thread_id": "req-003",  # This should trigger HITL!
    },
    {
        "employee_name": "Rahul Kumar",
        "message": "Submit my lunch expense of Rs 450",
        "thread_id": "req-004",  # Low amount, auto-approve
    },
]

# for req in test_requests:
#     config = {"configurable": {"thread_id": req["thread_id"]}}
#     result = app.invoke({
#         "employee_name": req["employee_name"],
#         "message": req["message"],
#         "audit_trail": [],
#     }, config)
#
#     # Check if workflow paused (finance > 5000)
#     snapshot = app.get_state(config)
#     if snapshot.next:
#         print(f"\n⚠ PAUSED: {req['employee_name']}'s request needs manager approval!")
#         print(f"  Amount: Rs {snapshot.values.get('amount', 0)}")
#         print(f"  Response: {snapshot.values['response'][:60]}...")
#
#         # Manager approves
#         app.update_state(config, {"approved": True, "audit_trail": ["[MANAGER] Approved"]})
#         result = app.invoke(None, config)
#
#     print(f"\n{'='*40}")
#     print(f"Employee: {req['employee_name']}")
#     print(f"Category: {result['category']}")
#     print(f"Priority: {result['priority']}")
#     print(f"Response: {result['response'][:80]}...")
#     print(f"Approved: {result.get('approved', 'N/A')}")
#     print(f"Audit trail:")
#     for entry in result['audit_trail']:
#         print(f"    {entry}")

# ============================================================
# BONUS: Add state inspection
# ============================================================
# After all requests are processed, list all threads and their
# final states using get_state() for each config.

# print("\n--- All Tickets Summary ---")
# for req in test_requests:
#     config = {"configurable": {"thread_id": req["thread_id"]}}
#     snap = app.get_state(config)
#     print(f"  {req['thread_id']}: {snap.values['category']} / "
#           f"{snap.values['priority']} / "
#           f"Approved: {snap.values.get('approved', 'N/A')}")

print("\nChallenge: Uncomment and implement the code above!")
print("Use what you learned in Labs 01-07 to build this workflow.")
print("\nHints:")
print("- Lab 01-02: StateGraph basics and multi-step workflows")
print("- Lab 03: Conditional routing with add_conditional_edges()")
print("- Lab 04: Annotated[list, add] for audit_trail")
print("- Lab 05: Cycles for retry logic (optional)")
print("- Lab 06: MemorySaver and thread_id for checkpointing")
print("- Lab 07: interrupt_before for human-in-the-loop")

print("\n" + "=" * 60)
print("Lab 08 (Challenge) — Good luck!")
print("Check solutions/lab08_challenge.py when you're done.")
