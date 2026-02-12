"""
Lab 08 Solution: Challenge — UniGPS Support Request Workflow
==============================================================
Complete implementation combining: state, conditional routing,
reducers, checkpointing, and human-in-the-loop.
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

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

print("=" * 60)
print("  Challenge Solution: UniGPS Support Request Workflow")
print("=" * 60)

# ============================================================
# State definition
# ============================================================

class SupportRequest(TypedDict):
    employee_name: str
    message: str
    category: str
    priority: str
    amount: int
    response: str
    approved: bool
    audit_trail: Annotated[list, add]

# ============================================================
# STEP 1: Nodes
# ============================================================

def receive_request(state: SupportRequest) -> dict:
    """Log receipt of the request."""
    print(f"  [receive] From: {state['employee_name']}")
    return {
        "audit_trail": [f"[RECEIVED] From: {state['employee_name']} — {state['message'][:50]}"]
    }

def classify_request(state: SupportRequest) -> dict:
    """Use LLM to classify and extract metadata."""
    prompt = (
        f"Analyze this employee support request and reply in exactly this format:\n"
        f"CATEGORY: hr or tech or finance\n"
        f"PRIORITY: HIGH or MEDIUM or LOW\n"
        f"AMOUNT: number (if a money amount is mentioned, else 0)\n\n"
        f"Request: {state['message']}\n\n"
        f"Rules:\n"
        f"- HR: leave, sick, vacation, wfh, maternity, transfer\n"
        f"- Tech: server, deploy, bug, database, code, api, error\n"
        f"- Finance: expense, reimburse, invoice, salary, bill\n"
        f"- HIGH priority if: urgent, critical, down, emergency\n"
        f"- Extract Rs/INR amount if mentioned"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()

    # Parse response
    category = "general"
    priority = "LOW"
    amount = 0

    for line in text.split("\n"):
        line_lower = line.lower()
        if "category:" in line_lower:
            cat = line_lower.split("category:")[-1].strip()
            if cat in ["hr", "tech", "finance"]:
                category = cat
        elif "priority:" in line_lower:
            pri = line.split(":")[-1].strip().upper()
            if pri in ["HIGH", "MEDIUM", "LOW"]:
                priority = pri
        elif "amount:" in line_lower:
            nums = re.findall(r'\d+', line)
            if nums:
                amount = int(nums[0])

    print(f"  [classify] category={category}, priority={priority}, amount=Rs {amount}")
    return {
        "category": category,
        "priority": priority,
        "amount": amount,
        "audit_trail": [f"[CLASSIFIED] {category}/{priority}, amount=Rs {amount}"],
    }

def handle_hr(state: SupportRequest) -> dict:
    """Generate HR-specific response."""
    prompt = (
        f"You are UniGPS HR support. Write a brief, helpful response (2 sentences) for:\n"
        f"{state['message']}\nEmployee: {state['employee_name']}"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()
    print(f"  [handle_hr] → {text[:60]}...")
    return {
        "response": f"[{state['priority']}] {text}",
        "approved": True,
        "audit_trail": [f"[HR HANDLER] Response generated"],
    }

def handle_tech(state: SupportRequest) -> dict:
    """Generate Tech-specific response."""
    prompt = (
        f"You are UniGPS Tech Support. Write a brief, helpful response (2 sentences) for:\n"
        f"{state['message']}\nEmployee: {state['employee_name']}"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()
    print(f"  [handle_tech] → {text[:60]}...")
    return {
        "response": f"[{state['priority']}] {text}",
        "approved": True,
        "audit_trail": [f"[TECH HANDLER] Response generated"],
    }

def handle_finance(state: SupportRequest) -> dict:
    """Generate Finance-specific response. Flag high amounts."""
    prompt = (
        f"You are UniGPS Finance Support. Write a brief, helpful response (2 sentences) for:\n"
        f"{state['message']}\nEmployee: {state['employee_name']}\nAmount: Rs {state['amount']}"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()

    # Auto-approve if under Rs 5000, flag otherwise
    needs_approval = state["amount"] > 5000
    approved = not needs_approval

    status = "PENDING MANAGER APPROVAL" if needs_approval else "Auto-approved"
    print(f"  [handle_finance] Rs {state['amount']} → {status}")
    print(f"  [handle_finance] → {text[:60]}...")

    return {
        "response": f"[{state['priority']}] {text}",
        "approved": approved,
        "audit_trail": [f"[FINANCE HANDLER] {status}, response generated"],
    }

def finalize(state: SupportRequest) -> dict:
    """Create final audit entry."""
    status = "APPROVED" if state["approved"] else "PENDING MANAGER REVIEW"
    print(f"  [finalize] Status: {status}")
    return {
        "audit_trail": [f"[FINALIZED] Status: {status} — Response delivered to {state['employee_name']}"]
    }

# ============================================================
# STEP 2: Routing function
# ============================================================

def route_to_handler(state: SupportRequest) -> str:
    """Route based on category."""
    category = state["category"]
    if category == "hr":
        return "handle_hr"
    elif category == "tech":
        return "handle_tech"
    elif category == "finance":
        return "handle_finance"
    return "handle_hr"  # Default to HR for general

# ============================================================
# STEP 3: Build the graph
# ============================================================

graph = StateGraph(SupportRequest)

graph.add_node("receive", receive_request)
graph.add_node("classify", classify_request)
graph.add_node("handle_hr", handle_hr)
graph.add_node("handle_tech", handle_tech)
graph.add_node("handle_finance", handle_finance)
graph.add_node("finalize", finalize)

graph.add_edge(START, "receive")
graph.add_edge("receive", "classify")

graph.add_conditional_edges(
    "classify",
    route_to_handler,
    {
        "handle_hr": "handle_hr",
        "handle_tech": "handle_tech",
        "handle_finance": "handle_finance",
    }
)

graph.add_edge("handle_hr", "finalize")
graph.add_edge("handle_tech", "finalize")
graph.add_edge("handle_finance", "finalize")
graph.add_edge("finalize", END)

memory = MemorySaver()
app = graph.compile(checkpointer=memory, interrupt_before=["finalize"])

print("\nGraph: START → receive → classify → [HR|Tech|Finance] → [PAUSE] → finalize → END")
print("Finance requests > Rs 5000 require manager approval at the pause point.\n")

# ============================================================
# STEP 4: Test the workflow
# ============================================================

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
        "thread_id": "req-003",
    },
    {
        "employee_name": "Rahul Kumar",
        "message": "Submit my lunch expense of Rs 450",
        "thread_id": "req-004",
    },
]

print("--- Processing Requests ---")
for req in test_requests:
    config = {"configurable": {"thread_id": req["thread_id"]}}

    print(f"\n{'='*50}")
    print(f"Request from: {req['employee_name']}")
    print(f"Message: {req['message']}")

    result = app.invoke({
        "employee_name": req["employee_name"],
        "message": req["message"],
        "category": "",
        "priority": "",
        "amount": 0,
        "response": "",
        "approved": False,
        "audit_trail": [],
    }, config)

    # Check if workflow paused (needs manager approval)
    snapshot = app.get_state(config)
    if snapshot.next:
        amount = snapshot.values.get("amount", 0)
        approved = snapshot.values.get("approved", False)

        if not approved and amount > 5000:
            print(f"\n  ⚠ PAUSED: Needs manager approval! (Rs {amount})")
            print(f"  Response preview: {snapshot.values['response'][:60]}...")

            # Simulate manager approval
            print(f"  [Manager] Reviewing Rs {amount} expense...")
            print(f"  [Manager] APPROVED")
            app.update_state(config, {
                "approved": True,
                "audit_trail": [f"[MANAGER] Approved Rs {amount} expense for {req['employee_name']}"],
            })

        # Resume the workflow
        result = app.invoke(None, config)
    else:
        result = snapshot.values

    print(f"\n  Category: {result['category']}")
    print(f"  Priority: {result['priority']}")
    print(f"  Amount: Rs {result['amount']}")
    print(f"  Approved: {result['approved']}")
    print(f"  Response: {result['response'][:80]}...")
    print(f"  Audit trail:")
    for entry in result["audit_trail"]:
        print(f"    {entry}")

# ============================================================
# BONUS: All Tickets Summary
# ============================================================

print(f"\n{'='*60}")
print("--- All Tickets Summary ---")
print(f"{'Thread':<12} {'Category':<10} {'Priority':<8} {'Amount':>8} {'Approved'}")
print("-" * 55)

for req in test_requests:
    config = {"configurable": {"thread_id": req["thread_id"]}}
    snap = app.get_state(config)
    v = snap.values
    print(
        f"{req['thread_id']:<12} "
        f"{v.get('category', 'N/A'):<10} "
        f"{v.get('priority', 'N/A'):<8} "
        f"Rs {v.get('amount', 0):>5} "
        f"{v.get('approved', 'N/A')}"
    )

print(f"\n{'='*60}")
print("Challenge Solution complete!")
print("Concepts used:")
print("  - StateGraph with TypedDict")
print("  - Annotated[list, add] for audit_trail (reducer)")
print("  - Conditional routing (HR/Tech/Finance)")
print("  - MemorySaver checkpointing with thread_id")
print("  - interrupt_before for HITL (finance > Rs 5000)")
print("  - update_state() for manager approval")
print("  - invoke(None, config) to resume paused workflow")
