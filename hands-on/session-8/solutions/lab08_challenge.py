"""
Lab 08 Solution: Challenge — Complete UniGPS Multi-Agent Support System
=========================================================================
Complete implementation combining: LLM supervisor, specialized workers,
escalation, fallback chains, QA gate, audit trail, and checkpointing.
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
print("  Challenge Solution: UniGPS Multi-Agent Support System")
print("=" * 60)

# ============================================================
# State
# ============================================================

class SupportRequest(TypedDict):
    employee_name: str
    request: str
    category: str
    confidence: int
    worker_output: str
    needs_escalation: bool
    escalation_reason: str
    error: str
    fallback_used: bool
    final_response: str
    audit: Annotated[list, add]

# ============================================================
# 1. LLM Supervisor
# ============================================================

def supervisor(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    prompt = (
        f"You are the UniGPS support desk supervisor.\n"
        f"Classify this employee request into: hr, tech, finance, facilities, general\n"
        f"Also rate your confidence 1-10.\n"
        f"Employee: {state['employee_name']}\n"
        f"Request: {state['request']}\n"
        f"Reply:\nCATEGORY: ...\nCONFIDENCE: ..."
    )
    try:
        response = llm.invoke(prompt)
        text = response.content.lower()
        category = "general"
        confidence = 5
        for line in text.split("\n"):
            if "category:" in line:
                cat = line.split(":")[-1].strip()
                if cat in ["hr", "tech", "finance", "facilities", "general"]:
                    category = cat
            elif "confidence:" in line:
                try:
                    confidence = int(line.split(":")[-1].strip().rstrip("."))
                    confidence = max(1, min(10, confidence))
                except ValueError:
                    confidence = 5
        print(f"  [supervisor] {category} (conf: {confidence}/10)")
        return {
            "category": category,
            "confidence": confidence,
            "error": "",
            "audit": [f"[{ts}] Supervisor: {category} (conf: {confidence})"],
        }
    except Exception as e:
        print(f"  [supervisor] Error: {e}")
        return {
            "category": "general",
            "confidence": 1,
            "error": "",
            "audit": [f"[{ts}] Supervisor error, fallback to general"],
        }

def route_supervisor(state: SupportRequest) -> str:
    if state["confidence"] < 5:
        return "clarify"
    return state["category"]

# ============================================================
# 2. Specialized Workers
# ============================================================

def clarify_agent(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    print(f"  [clarify] Low confidence, asking for details")
    return {
        "worker_output": f"Hi {state['employee_name']}, I'm not sure I understand your request: "
                         f"'{state['request']}'. Could you provide more details?",
        "needs_escalation": False,
        "error": "",
        "audit": [f"[{ts}] Clarification requested (conf: {state['confidence']})"],
    }

def hr_worker(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    prompt = (
        f"You are UniGPS HR (Gheware UniGPS Solutions LLP).\n"
        f"Policies: 24 casual leaves/year, 2 WFH days/week, family health insurance.\n"
        f"Employee: {state['employee_name']}\n"
        f"Request: {state['request']}\n"
        f"Reply helpfully in 2-3 sentences.\n"
        f"If this needs a policy exception (>10 days leave, special cases), "
        f"add on a new line: ESCALATE: <reason>"
    )
    try:
        response = llm.invoke(prompt)
        text = response.content.strip()
        escalate = False
        reason = ""
        if "ESCALATE:" in text.upper():
            escalate = True
            for line in text.split("\n"):
                if "ESCALATE:" in line.upper():
                    reason = line.split(":", 1)[-1].strip()
            text = text.split("ESCALATE:")[0].strip()
        print(f"  [HR worker] Responded (escalate={escalate})")
        return {
            "worker_output": text,
            "needs_escalation": escalate,
            "escalation_reason": reason,
            "error": "",
            "audit": [f"[{ts}] HR worker: {'escalating' if escalate else 'resolved'}"],
        }
    except Exception as e:
        return {"error": str(e), "audit": [f"[{ts}] HR worker error: {e}"]}

def tech_worker(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    prompt = (
        f"You are UniGPS IT Support.\n"
        f"SLA: P1=1hr, P2=4hr, P3=next day. Tools: Jira, VPN, AWS.\n"
        f"Employee: {state['employee_name']}\n"
        f"Request: {state['request']}\n"
        f"Reply helpfully in 2-3 sentences.\n"
        f"If this is P1 severity (production down, data loss), add: ESCALATE: <reason>"
    )
    try:
        response = llm.invoke(prompt)
        text = response.content.strip()
        escalate = False
        reason = ""
        if "ESCALATE:" in text.upper():
            escalate = True
            for line in text.split("\n"):
                if "ESCALATE:" in line.upper():
                    reason = line.split(":", 1)[-1].strip()
            text = text.split("ESCALATE:")[0].strip()
        print(f"  [Tech worker] Responded (escalate={escalate})")
        return {
            "worker_output": text,
            "needs_escalation": escalate,
            "escalation_reason": reason,
            "error": "",
            "audit": [f"[{ts}] Tech worker: {'escalating' if escalate else 'resolved'}"],
        }
    except Exception as e:
        return {"error": str(e), "audit": [f"[{ts}] Tech worker error: {e}"]}

def finance_worker(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    prompt = (
        f"You are UniGPS Finance team.\n"
        f"Policies: expense claims within 30 days, salary on 1st of month, tax deadline March 31.\n"
        f"Employee: {state['employee_name']}\n"
        f"Request: {state['request']}\n"
        f"Reply helpfully in 2-3 sentences."
    )
    try:
        response = llm.invoke(prompt)
        print(f"  [Finance worker] Responded")
        return {
            "worker_output": response.content.strip(),
            "needs_escalation": False,
            "error": "",
            "audit": [f"[{ts}] Finance worker resolved"],
        }
    except Exception as e:
        return {"error": str(e), "audit": [f"[{ts}] Finance worker error: {e}"]}

def facilities_worker(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    prompt = (
        f"You are UniGPS Facilities/Admin team.\n"
        f"You handle: desks, parking, cafeteria, access cards, building maintenance.\n"
        f"Employee: {state['employee_name']}\n"
        f"Request: {state['request']}\n"
        f"Reply helpfully in 2-3 sentences."
    )
    try:
        response = llm.invoke(prompt)
        print(f"  [Facilities worker] Responded")
        return {
            "worker_output": response.content.strip(),
            "needs_escalation": False,
            "error": "",
            "audit": [f"[{ts}] Facilities worker resolved"],
        }
    except Exception as e:
        return {"error": str(e), "audit": [f"[{ts}] Facilities worker error: {e}"]}

def general_worker(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    return {
        "worker_output": f"Hi {state['employee_name']}, your request has been logged. "
                         f"A team member will get back to you shortly.",
        "needs_escalation": False,
        "error": "",
        "audit": [f"[{ts}] General worker"],
    }

# ============================================================
# 3. Escalation
# ============================================================

def escalation_check(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    if state["error"]:
        return {"audit": [f"[{ts}] Worker errored, sending to fallback"]}
    return {"audit": [f"[{ts}] Escalation check: {state['needs_escalation']}"]}

def route_escalation(state: SupportRequest) -> str:
    if state["error"]:
        return "fallback"
    if state["needs_escalation"]:
        return "manager"
    return "qa_check"

def manager_agent(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    prompt = (
        f"You are a manager at UniGPS with authority over policy exceptions.\n"
        f"Escalation reason: {state['escalation_reason']}\n"
        f"Employee: {state['employee_name']}\n"
        f"Original request: {state['request']}\n"
        f"Worker's initial response: {state['worker_output'][:100]}\n\n"
        f"Provide a definitive answer with your authority. 2-3 sentences."
    )
    try:
        response = llm.invoke(prompt)
        print(f"  [Manager] Decision made")
        return {
            "worker_output": f"[Manager Review] {response.content.strip()}",
            "error": "",
            "audit": [f"[{ts}] Manager resolved escalation"],
        }
    except Exception as e:
        return {"error": str(e), "audit": [f"[{ts}] Manager error: {e}"]}

# ============================================================
# 4. QA Gate & Fallback
# ============================================================

def qa_check(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    output = state["worker_output"]
    issues = []
    if len(output) < 20:
        issues.append("too short")
    if not output.strip():
        issues.append("empty")

    if issues:
        print(f"  [QA] FAIL: {issues}")
        return {"error": ", ".join(issues),
                "audit": [f"[{ts}] QA FAIL: {issues}"]}
    print(f"  [QA] PASS")
    return {"error": "", "audit": [f"[{ts}] QA PASS"]}

def route_qa(state: SupportRequest) -> str:
    return "fallback" if state["error"] else "finalize"

def fallback(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    templates = {
        "hr": "Please visit the HR portal or email hr@unigps.in.",
        "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
        "finance": "Please email finance@unigps.in with your query.",
        "facilities": "Please email admin@unigps.in for facilities requests.",
        "general": "Your request has been noted. We'll respond shortly.",
    }
    output = templates.get(state["category"], templates["general"])
    print(f"  [fallback] Using template for {state['category']}")
    return {
        "worker_output": output,
        "fallback_used": True,
        "error": "",
        "audit": [f"[{ts}] Fallback template: {state['category']}"],
    }

# ============================================================
# 5. Finalize
# ============================================================

def finalize(state: SupportRequest) -> dict:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fallback_note = " (via fallback)" if state.get("fallback_used") else ""
    return {
        "final_response": (
            f"[{state['category'].upper()}] {state['worker_output']}\n"
            f"— UniGPS Support{fallback_note} | {ts}"
        ),
        "audit": [f"[{ts}] Finalized for {state['employee_name']}"],
    }

# ============================================================
# 6. Build Graph
# ============================================================

graph = StateGraph(SupportRequest)

graph.add_node("supervisor", supervisor)
graph.add_node("clarify", clarify_agent)
graph.add_node("hr_worker", hr_worker)
graph.add_node("tech_worker", tech_worker)
graph.add_node("finance_worker", finance_worker)
graph.add_node("facilities_worker", facilities_worker)
graph.add_node("general_worker", general_worker)
graph.add_node("escalation_check", escalation_check)
graph.add_node("manager", manager_agent)
graph.add_node("qa_check", qa_check)
graph.add_node("fallback", fallback)
graph.add_node("finalize", finalize)

graph.add_edge(START, "supervisor")

graph.add_conditional_edges("supervisor", route_supervisor, {
    "clarify": "clarify",
    "hr": "hr_worker",
    "tech": "tech_worker",
    "finance": "finance_worker",
    "facilities": "facilities_worker",
    "general": "general_worker",
})

# All workers → escalation check
graph.add_edge("clarify", "finalize")
for w in ["hr_worker", "tech_worker", "finance_worker", "facilities_worker", "general_worker"]:
    graph.add_edge(w, "escalation_check")

graph.add_conditional_edges("escalation_check", route_escalation, {
    "manager": "manager",
    "qa_check": "qa_check",
    "fallback": "fallback",
})

graph.add_edge("manager", "qa_check")

graph.add_conditional_edges("qa_check", route_qa, {
    "finalize": "finalize",
    "fallback": "fallback",
})

graph.add_edge("fallback", "finalize")
graph.add_edge("finalize", END)

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

print("\nGraph: supervisor → [clarify|hr|tech|finance|facilities|general]")
print("  → escalation_check → [manager|qa_check] → [finalize|fallback] → END\n")

# ============================================================
# 7. Test
# ============================================================

test_requests = [
    {
        "employee_name": "Priya Sharma",
        "request": "I want to apply for 5 days casual leave from next Monday",
        "thread_id": "support-001",
    },
    {
        "employee_name": "Vikram Patel",
        "request": "The production database is running very slow and queries are timing out",
        "thread_id": "support-002",
    },
    {
        "employee_name": "Anita Desai",
        "request": "When will my travel expense reimbursement from last month be credited?",
        "thread_id": "support-003",
    },
    {
        "employee_name": "Rahul Kumar",
        "request": "I need a standing desk and a parking spot in the new building",
        "thread_id": "support-004",
    },
    {
        "employee_name": "Meera Joshi",
        "request": "asdfghjkl",
        "thread_id": "support-005",
    },
    {
        "employee_name": "Amit Singh",
        "request": "I need a policy exception for 30 days leave for my wedding",
        "thread_id": "support-006",
    },
]

print("--- Processing Support Requests ---\n")
for req in test_requests:
    config = {"configurable": {"thread_id": req["thread_id"]}}
    print(f"{'='*50}")
    print(f"Employee: {req['employee_name']}")
    print(f"Request: {req['request']}")

    result = app.invoke({
        "employee_name": req["employee_name"],
        "request": req["request"],
        "category": "", "confidence": 0,
        "worker_output": "", "needs_escalation": False,
        "escalation_reason": "", "error": "",
        "fallback_used": False, "final_response": "",
        "audit": [],
    }, config)

    print(f"\n  Category: {result.get('category', 'N/A')}")
    print(f"  Confidence: {result.get('confidence', 'N/A')}/10")
    print(f"  Escalated: {result.get('needs_escalation', False)}")
    print(f"  Fallback: {result.get('fallback_used', False)}")
    print(f"  Response: {result.get('final_response', 'N/A')[:80]}...")
    print(f"  Audit trail:")
    for entry in result.get("audit", []):
        print(f"    {entry}")
    print()

# Summary
print(f"\n{'='*60}")
print("--- Summary ---")
print(f"{'Thread':<14} {'Employee':<18} {'Category':<12} {'Conf':>4} {'Escalated'}")
print("-" * 60)
for req in test_requests:
    config = {"configurable": {"thread_id": req["thread_id"]}}
    snap = app.get_state(config)
    v = snap.values
    print(
        f"{req['thread_id']:<14} "
        f"{req['employee_name']:<18} "
        f"{v.get('category', 'N/A'):<12} "
        f"{v.get('confidence', 'N/A'):>4} "
        f"{v.get('needs_escalation', False)}"
    )

print(f"\n{'='*60}")
print("Challenge Solution complete!")
print("Patterns used:")
print("  - LLM supervisor with confidence routing (< 5 → clarify)")
print("  - 5 specialized domain workers (HR, Tech, Finance, Facilities, General)")
print("  - Escalation path to manager agent for policy exceptions")
print("  - Fallback chain (LLM → template on error/QA fail)")
print("  - QA gate validates response quality before delivery")
print("  - Audit trail with timestamps via Annotated[list, add]")
print("  - MemorySaver checkpointing with thread_id per employee")
