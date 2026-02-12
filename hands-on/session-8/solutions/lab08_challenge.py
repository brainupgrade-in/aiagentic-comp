"""
Lab 08 Solution: Challenge — Production Expense Approval System
=================================================================
Complete implementation combining: parallel validation, LLM routing,
multi-gate HITL, error handling, reducers, and checkpointing.
"""

import os
import re
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

print("=" * 60)
print("  Challenge Solution: Production Expense Approval System")
print("=" * 60)

# ============================================================
# State
# ============================================================

class ExpenseRequest(TypedDict):
    employee_name: str
    description: str
    amount: int
    receipt_attached: bool
    category: str
    priority: str
    validation_checks: Annotated[list, add]
    is_valid: bool
    approval_level: str
    approved: bool
    approver_notes: str
    response: str
    audit_trail: Annotated[list, add]

# ============================================================
# STEP 1: Parallel validation nodes
# ============================================================

def check_amount(state: ExpenseRequest) -> dict:
    passed = 0 < state["amount"] < 500000
    detail = "valid" if passed else f"invalid amount: Rs {state['amount']}"
    return {"validation_checks": [{"type": "amount", "passed": passed, "detail": detail}]}

def check_receipt(state: ExpenseRequest) -> dict:
    if state["amount"] <= 500:
        passed = True
        detail = "not required (under Rs 500)"
    else:
        passed = state["receipt_attached"]
        detail = "attached" if passed else "MISSING (required for > Rs 500)"
    return {"validation_checks": [{"type": "receipt", "passed": passed, "detail": detail}]}

def check_description(state: ExpenseRequest) -> dict:
    passed = len(state["description"]) >= 10
    detail = f"{len(state['description'])} chars" + ("" if passed else " (min 10)")
    return {"validation_checks": [{"type": "description", "passed": passed, "detail": detail}]}

def merge_validations(state: ExpenseRequest) -> dict:
    all_passed = all(c["passed"] for c in state["validation_checks"])
    failed = [c for c in state["validation_checks"] if not c["passed"]]
    summary = "All checks passed" if all_passed else f"Failed: {[c['type'] for c in failed]}"
    print(f"  [validate] {summary}")
    return {
        "is_valid": all_passed,
        "audit_trail": [f"[VALIDATION] {summary}"],
    }

# ============================================================
# STEP 2: LLM classification
# ============================================================

def classify_expense(state: ExpenseRequest) -> dict:
    prompt = (
        f"Classify this expense:\n"
        f"Description: {state['description']}\nAmount: Rs {state['amount']}\n\n"
        f"Reply:\nCATEGORY: travel or meals or equipment or other\n"
        f"PRIORITY: urgent or normal"
    )
    try:
        response = llm.invoke(prompt)
        text = response.content.lower()
        category = "other"
        priority = "normal"
        for line in text.split("\n"):
            if "category:" in line:
                cat = line.split(":")[-1].strip()
                if cat in ["travel", "meals", "equipment", "other"]:
                    category = cat
            elif "priority:" in line:
                pri = line.split(":")[-1].strip()
                if pri in ["urgent", "normal"]:
                    priority = pri
        print(f"  [classify] {category}/{priority}")
        return {
            "category": category,
            "priority": priority,
            "audit_trail": [f"[CLASSIFIED] {category}/{priority}"],
        }
    except Exception as e:
        print(f"  [classify] Error: {e}, using defaults")
        return {
            "category": "other", "priority": "normal",
            "audit_trail": [f"[CLASSIFIED] Fallback: other/normal (error: {e})"],
        }

# ============================================================
# STEP 3: Approval routing
# ============================================================

def determine_approval_level(state: ExpenseRequest) -> dict:
    amount = state["amount"]
    if amount <= 5000:
        level = "auto"
    elif amount <= 50000:
        level = "manager"
    else:
        level = "vp"
    print(f"  [approval_level] Rs {amount} → {level}")
    return {"approval_level": level, "audit_trail": [f"[APPROVAL LEVEL] {level} (Rs {amount})"]}

def route_approval(state: ExpenseRequest) -> str:
    if not state["is_valid"]:
        return "reject"
    return state["approval_level"]

# ============================================================
# STEP 4: Handler nodes
# ============================================================

def auto_approve(state: ExpenseRequest) -> dict:
    print(f"  [auto] Approved Rs {state['amount']}")
    return {
        "approved": True,
        "response": f"Auto-approved: Rs {state['amount']} {state['category']} expense.",
        "audit_trail": ["[AUTO] Approved (under Rs 5000)"],
    }

def manager_review(state: ExpenseRequest) -> dict:
    """Prepare for manager review — will pause here."""
    print(f"  [manager_review] Awaiting manager approval for Rs {state['amount']}")
    return {"audit_trail": [f"[MANAGER REVIEW] Awaiting approval for Rs {state['amount']}"]}

def vp_review(state: ExpenseRequest) -> dict:
    """Prepare for VP review — will pause here."""
    print(f"  [vp_review] Awaiting VP approval for Rs {state['amount']}")
    return {"audit_trail": [f"[VP REVIEW] Awaiting VP approval for Rs {state['amount']}"]}

def reject_invalid(state: ExpenseRequest) -> dict:
    failed = [f"{c['type']}: {c['detail']}" for c in state["validation_checks"] if not c["passed"]]
    msg = f"Rejected: validation failed — {'; '.join(failed)}"
    print(f"  [reject] {msg}")
    return {
        "approved": False,
        "response": msg,
        "audit_trail": [f"[REJECTED] {msg}"],
    }

def finalize(state: ExpenseRequest) -> dict:
    status = "APPROVED" if state["approved"] else "REJECTED"
    resp = state["response"] or f"{status}: Rs {state['amount']} expense for {state['employee_name']}"
    print(f"  [finalize] {status}")
    return {
        "response": resp,
        "audit_trail": [f"[FINALIZED] {status} — {state['employee_name']}'s Rs {state['amount']} expense"],
    }

# ============================================================
# STEP 5: Build the graph
# ============================================================

graph = StateGraph(ExpenseRequest)

# Validation nodes (parallel)
graph.add_node("check_amount", check_amount)
graph.add_node("check_receipt", check_receipt)
graph.add_node("check_description", check_description)
graph.add_node("merge_validations", merge_validations)

# Processing nodes
graph.add_node("classify", classify_expense)
graph.add_node("determine_level", determine_approval_level)

# Approval nodes
graph.add_node("auto_approve", auto_approve)
graph.add_node("manager_review", manager_review)
graph.add_node("vp_review", vp_review)
graph.add_node("reject", reject_invalid)
graph.add_node("finalize", finalize)

# Parallel validation
graph.add_edge(START, "check_amount")
graph.add_edge(START, "check_receipt")
graph.add_edge(START, "check_description")
graph.add_edge("check_amount", "merge_validations")
graph.add_edge("check_receipt", "merge_validations")
graph.add_edge("check_description", "merge_validations")

# Classification and level determination
graph.add_edge("merge_validations", "classify")
graph.add_edge("classify", "determine_level")

# Approval routing
graph.add_conditional_edges("determine_level", route_approval, {
    "auto": "auto_approve",
    "manager": "manager_review",
    "vp": "vp_review",
    "reject": "reject",
})

# All paths → finalize
graph.add_edge("auto_approve", "finalize")
graph.add_edge("manager_review", "finalize")
graph.add_edge("vp_review", "finalize")
graph.add_edge("reject", "finalize")
graph.add_edge("finalize", END)

memory = MemorySaver()
app = graph.compile(
    checkpointer=memory,
    interrupt_before=["manager_review", "vp_review"],  # HITL gates
)

print("\nGraph: [parallel validation] → classify → determine_level")
print("  → [auto | PAUSE:manager | PAUSE:vp | reject] → finalize → END\n")

# ============================================================
# STEP 6: Test
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
        "thread_id": "exp-002",
    },
    {
        "employee_name": "Anita Desai",
        "description": "New MacBook Pro for development team lead",
        "amount": 175000,
        "receipt_attached": True,
        "thread_id": "exp-003",
    },
    {
        "employee_name": "Rahul Kumar",
        "description": "Cab",
        "amount": 2000,
        "receipt_attached": False,
        "thread_id": "exp-004",
    },
]

print("--- Processing Expenses ---")
for exp in test_expenses:
    config = {"configurable": {"thread_id": exp["thread_id"]}}

    print(f"\n{'='*50}")
    print(f"Employee: {exp['employee_name']} | Rs {exp['amount']} | {exp['description']}")

    result = app.invoke({
        "employee_name": exp["employee_name"],
        "description": exp["description"],
        "amount": exp["amount"],
        "receipt_attached": exp["receipt_attached"],
        "validation_checks": [],
        "audit_trail": [],
        "is_valid": False, "approved": False,
        "category": "", "priority": "", "approval_level": "",
        "approver_notes": "", "response": "",
    }, config)

    # Check if paused (needs human approval)
    snap = app.get_state(config)
    if snap.next:
        level = snap.next[0] if snap.next else "unknown"
        print(f"\n  PAUSED: Needs {level} for Rs {exp['amount']}")

        # Simulate approval
        app.update_state(config, {
            "approved": True,
            "approver_notes": f"Approved by {level}",
            "audit_trail": [f"[{level.upper()}] Approved by reviewer"],
        })
        result = app.invoke(None, config)

    print(f"\n  Category: {result.get('category', 'N/A')}")
    print(f"  Valid: {result.get('is_valid', 'N/A')}")
    print(f"  Approval: {result.get('approval_level', 'N/A')}")
    print(f"  Approved: {result.get('approved', 'N/A')}")
    print(f"  Response: {result.get('response', 'N/A')[:60]}")
    print(f"  Audit trail:")
    for entry in result.get("audit_trail", []):
        print(f"    {entry}")

# Summary
print(f"\n{'='*60}")
print("--- Summary ---")
print(f"{'Thread':<10} {'Employee':<18} {'Amount':>8} {'Level':<10} {'Approved'}")
print("-" * 60)
for exp in test_expenses:
    config = {"configurable": {"thread_id": exp["thread_id"]}}
    snap = app.get_state(config)
    v = snap.values
    print(
        f"{exp['thread_id']:<10} "
        f"{exp['employee_name']:<18} "
        f"Rs {exp['amount']:>5} "
        f"{v.get('approval_level', 'N/A'):<10} "
        f"{v.get('approved', 'N/A')}"
    )

print(f"\n{'='*60}")
print("Challenge Solution complete!")
print("Patterns used:")
print("  - Parallel validation (3 checks with Annotated[list, add])")
print("  - LLM classification (category + priority)")
print("  - Multi-level approval routing (auto/manager/VP)")
print("  - interrupt_before for HITL (manager + VP gates)")
print("  - Error handling with fallback in classify")
print("  - Audit trail reducer throughout")
print("  - MemorySaver checkpointing with thread_id")
