"""
Lab 08: Challenge — Production-Grade UniGPS Expense Approval System
=====================================================================
Goal: Build a complete production-grade workflow combining ALL advanced
      patterns from this session.

Scenario:
  UniGPS needs an expense approval system that:
  1. Validates the submission (parallel checks)
  2. Classifies using LLM (category + priority routing)
  3. Routes based on amount thresholds (auto/manager/VP approval)
  4. Handles errors with fallbacks
  5. Pauses for human approval on large expenses
  6. Maintains a complete audit trail (reducers)
  7. Uses checkpointing for state persistence

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

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

print("=" * 60)
print("  Challenge: Production Expense Approval System")
print("=" * 60)

# ============================================================
# YOUR TASK: Build the complete workflow
# ============================================================
#
# State definition (provided):

class ExpenseRequest(TypedDict):
    # Input
    employee_name: str
    description: str
    amount: int
    receipt_attached: bool
    # Processing
    category: str                          # travel, meals, equipment, other
    priority: str                          # normal, urgent
    validation_checks: Annotated[list, add]  # ← parallel checks
    is_valid: bool
    # Approval
    approval_level: str                    # auto, manager, vp
    approved: bool
    approver_notes: str
    # Output
    response: str
    # Tracking
    audit_trail: Annotated[list, add]      # ← reducer

# ============================================================
# STEP 1: Validation nodes (run in parallel)
# ============================================================
# Create parallel validation checks:

# def check_amount(state) -> dict:
#     """Check if amount is positive and reasonable (< Rs 500,000)."""
#     passed = 0 < state["amount"] < 500000
#     return {"validation_checks": [{"type": "amount", "passed": passed}]}

# def check_receipt(state) -> dict:
#     """Check if receipt is attached for amounts > Rs 500."""
#     if state["amount"] <= 500:
#         passed = True  # No receipt needed for small amounts
#     else:
#         passed = state["receipt_attached"]
#     return {"validation_checks": [{"type": "receipt", "passed": passed}]}

# def check_description(state) -> dict:
#     """Check if description is at least 10 characters."""
#     passed = len(state["description"]) >= 10
#     return {"validation_checks": [{"type": "description", "passed": passed}]}

# def merge_validations(state) -> dict:
#     """Merge validation results."""
#     all_passed = all(c["passed"] for c in state["validation_checks"])
#     return {"is_valid": all_passed, "audit_trail": [...]}

# ============================================================
# STEP 2: Classification node (LLM-powered)
# ============================================================

# def classify_expense(state) -> dict:
#     """Use LLM to classify expense category and priority."""
#     prompt = f"Classify this expense: {state['description']}, Rs {state['amount']}"
#     # Parse: category (travel/meals/equipment/other)
#     # Parse: priority (urgent/normal)
#     pass

# ============================================================
# STEP 3: Approval routing
# ============================================================

# def determine_approval_level(state) -> dict:
#     """Determine approval level based on amount:
#        - Rs 0-5000: auto-approve
#        - Rs 5001-50000: manager approval
#        - Rs 50000+: VP approval"""
#     pass

# def route_approval(state) -> str:
#     if not state["is_valid"]:
#         return "reject"
#     return state["approval_level"]  # "auto", "manager", "vp"

# ============================================================
# STEP 4: Handler nodes
# ============================================================

# def auto_approve(state) -> dict:
#     """Auto-approve small expenses."""
#     return {"approved": True, "response": "Auto-approved.", "audit_trail": [...]}

# def manager_review(state) -> dict:
#     """Prepare for manager review."""
#     return {"audit_trail": ["Awaiting manager approval"]}

# def vp_review(state) -> dict:
#     """Prepare for VP review."""
#     return {"audit_trail": ["Awaiting VP approval"]}

# def reject_invalid(state) -> dict:
#     """Reject invalid submissions."""
#     failed = [c for c in state["validation_checks"] if not c["passed"]]
#     return {"approved": False, "response": f"Rejected: {failed}", "audit_trail": [...]}

# def finalize(state) -> dict:
#     """Final processing and response generation."""
#     pass

# ============================================================
# STEP 5: Build the graph
# ============================================================
# Graph structure:
#   START → [check_amount | check_receipt | check_description] → merge
#         → classify → determine_level
#         → [auto | manager_review | vp_review | reject] → finalize → END
#
# Interrupt: interrupt_before=["manager_review", "vp_review"]

# graph = StateGraph(ExpenseRequest)
# ... add nodes ...
# ... add edges (parallel fan-out for validation) ...
# ... add conditional edges for routing ...
# memory = MemorySaver()
# app = graph.compile(checkpointer=memory, interrupt_before=["manager_review", "vp_review"])

# ============================================================
# STEP 6: Test the workflow
# ============================================================

test_expenses = [
    {
        "employee_name": "Priya Sharma",
        "description": "Team lunch at office cafeteria",
        "amount": 450,
        "receipt_attached": False,
        "thread_id": "exp-001",
    },
    {
        "employee_name": "Vikram Patel",
        "description": "Client dinner at Taj Hotel for project discussion",
        "amount": 8500,
        "receipt_attached": True,
        "thread_id": "exp-002",  # Should pause for manager
    },
    {
        "employee_name": "Anita Desai",
        "description": "New MacBook Pro for development team",
        "amount": 175000,
        "receipt_attached": True,
        "thread_id": "exp-003",  # Should pause for VP
    },
    {
        "employee_name": "Rahul Kumar",
        "description": "Cab",
        "amount": 2000,
        "receipt_attached": False,
        "thread_id": "exp-004",  # Should fail validation (short description, no receipt)
    },
]

# for exp in test_expenses:
#     config = {"configurable": {"thread_id": exp["thread_id"]}}
#     result = app.invoke({
#         "employee_name": exp["employee_name"],
#         "description": exp["description"],
#         "amount": exp["amount"],
#         "receipt_attached": exp["receipt_attached"],
#         "validation_checks": [],
#         "audit_trail": [],
#         "is_valid": False, "approved": False,
#         "category": "", "priority": "", "approval_level": "",
#         "approver_notes": "", "response": "",
#     }, config)
#
#     # Check if paused
#     snap = app.get_state(config)
#     if snap.next:
#         print(f"\n⚠ PAUSED for {snap.next}: {exp['employee_name']}'s Rs {exp['amount']} expense")
#         # Simulate approval
#         app.update_state(config, {
#             "approved": True,
#             "approver_notes": "Approved after review",
#             "audit_trail": [f"[{snap.next[0].upper()}] Approved"],
#         })
#         result = app.invoke(None, config)
#
#     print(f"\n{'='*45}")
#     print(f"Employee: {exp['employee_name']}")
#     print(f"Amount: Rs {exp['amount']}")
#     print(f"Valid: {result.get('is_valid')}")
#     print(f"Approved: {result.get('approved')}")
#     print(f"Response: {result.get('response', 'N/A')[:60]}")
#     print(f"Audit trail:")
#     for entry in result.get("audit_trail", []):
#         print(f"    {entry}")

print("\nChallenge: Uncomment and implement the code above!")
print("Combine everything from Labs 01-07:")
print("  - Lab 01: Multi-branch fan-out/convergence")
print("  - Lab 02: Parallel validation checks with reducers")
print("  - Lab 03: Custom reducers for audit trail")
print("  - Lab 04: Error handling with fallbacks")
print("  - Lab 05: Retry logic (optional: retry LLM classification)")
print("  - Lab 06: LLM-powered routing + priority routing")
print("  - Lab 07: Multi-gate HITL (manager + VP approval gates)")

print("\n" + "=" * 60)
print("Lab 08 (Challenge) — Good luck!")
print("Check solutions/lab08_challenge.py when you're done.")
