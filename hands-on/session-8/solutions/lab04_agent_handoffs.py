"""
Lab 04 Solution: Agent Handoffs
=================================
"""

import os
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

print("=" * 50)
print("  Agent Handoffs (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Multi-level escalation (L1 → L2 → L3)
# ============================================================

class EscalationState(TypedDict):
    request: str
    handoff_to: str
    escalation_level: int
    context_notes: str
    response: str
    audit: Annotated[list, add]

def l1_triage(state: EscalationState) -> dict:
    """L1: simple requests only."""
    prompt = (
        f"You are Level-1 support at UniGPS. Handle simple requests only.\n"
        f"Request: {state['request']}\n\n"
        f"If simple (greetings, basic FAQ), reply: HANDLE: <answer>\n"
        f"If needs specialist, reply: HANDOFF: hr or tech or finance\n"
        f"Add NOTE: <context for next level>"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()

    if "HANDOFF:" in text.upper():
        target = "general"
        note = ""
        for line in text.split("\n"):
            if "HANDOFF:" in line.upper():
                t = line.split(":")[-1].strip().lower()
                if t in ["hr", "tech", "finance"]:
                    target = t
            if "NOTE:" in line.upper():
                note = line.split(":", 1)[-1].strip()
        print(f"  [L1] Handoff → L2 ({target})")
        return {"handoff_to": target, "context_notes": note,
                "escalation_level": 2,
                "audit": [f"L1 → handoff to L2 {target}: {note[:40]}"]}
    else:
        answer = text.replace("HANDLE:", "").strip()
        print(f"  [L1] Handled directly")
        return {"handoff_to": "done", "response": answer,
                "escalation_level": 1, "audit": ["L1 handled directly"]}

def route_l1(state: EscalationState) -> str:
    return state["handoff_to"]

def l2_specialist(state: EscalationState) -> dict:
    """L2: handle most requests, escalate policy exceptions to L3."""
    prompt = (
        f"You are Level-2 {state['handoff_to']} specialist at UniGPS.\n"
        f"Context from L1: {state['context_notes']}\n"
        f"Request: {state['request']}\n\n"
        f"If you can resolve this, reply: RESOLVE: <your detailed answer>\n"
        f"If this needs manager approval (policy exceptions, high cost, special cases),\n"
        f"reply: ESCALATE: <reason>"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()

    if "ESCALATE:" in text.upper():
        reason = ""
        for line in text.split("\n"):
            if "ESCALATE:" in line.upper():
                reason = line.split(":", 1)[-1].strip()
        print(f"  [L2] Escalating to L3: {reason[:40]}")
        return {"handoff_to": "manager", "escalation_level": 3,
                "context_notes": f"L2 escalation: {reason}",
                "audit": [f"L2 → escalate to L3: {reason[:40]}"]}
    else:
        answer = text.replace("RESOLVE:", "").strip()
        print(f"  [L2] Resolved")
        return {"handoff_to": "done", "response": answer,
                "audit": ["L2 specialist resolved"]}

def route_l2(state: EscalationState) -> str:
    return state["handoff_to"]

def l3_manager(state: EscalationState) -> dict:
    """L3: final authority, handles policy exceptions."""
    prompt = (
        f"You are a manager at UniGPS with authority over policy exceptions.\n"
        f"Escalation context: {state['context_notes']}\n"
        f"Employee request: {state['request']}\n"
        f"Provide a definitive answer in 2-3 sentences. You have authority to approve exceptions."
    )
    response = llm.invoke(prompt)
    print(f"  [L3 Manager] Final decision")
    return {"response": response.content.strip(),
            "audit": ["L3 manager resolved"]}

def finalize(state: EscalationState) -> dict:
    level = state["escalation_level"]
    return {
        "response": f"[L{level}] {state['response']}\n— UniGPS Support",
        "audit": [f"Finalized at L{level}"],
    }

graph = StateGraph(EscalationState)
graph.add_node("l1_triage", l1_triage)
graph.add_node("l2_specialist", l2_specialist)
graph.add_node("l3_manager", l3_manager)
graph.add_node("finalize", finalize)

graph.add_edge(START, "l1_triage")
graph.add_conditional_edges("l1_triage", route_l1, {
    "hr": "l2_specialist",
    "tech": "l2_specialist",
    "finance": "l2_specialist",
    "general": "l2_specialist",
    "done": "finalize",
})
graph.add_conditional_edges("l2_specialist", route_l2, {
    "manager": "l3_manager",
    "done": "finalize",
})
graph.add_edge("l3_manager", "finalize")
graph.add_edge("finalize", END)

app = graph.compile()

print("\n--- TODO 1: L1 → L2 → L3 Escalation ---")
print("Graph: L1 → [done | L2] → [done | L3] → finalize → END\n")

tests = [
    "Hello, good morning!",
    "I need sick leave for tomorrow",
    "I need a policy exception for 30 days leave for my wedding",
    "Our production database got corrupted and we need a rollback",
]

for req in tests:
    result = app.invoke({
        "request": req, "handoff_to": "", "escalation_level": 1,
        "context_notes": "", "response": "", "audit": [],
    })
    print(f"  Request: '{req}'")
    print(f"  Level: L{result['escalation_level']}")
    print(f"  Response: {result['response'][:70]}...")
    print(f"  Audit: {result['audit']}")
    print()

# ============================================================
# TODO 2 Solution: Handoff with conversation history
# ============================================================

print("\n--- TODO 2: Handoff with History ---\n")

class HistoryHandoffState(TypedDict):
    request: str
    handoff_to: str
    conversation_history: Annotated[list, add]
    response: str
    audit: Annotated[list, add]

def triage_with_history(state: HistoryHandoffState) -> dict:
    prompt = (
        f"You are L1 support at UniGPS.\n"
        f"Request: {state['request']}\n"
        f"If simple, reply: HANDLE: <answer>\n"
        f"If complex, reply: HANDOFF: hr or tech or finance"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()

    history_entry = {"agent": "triage", "action": "received", "notes": state["request"][:50]}

    if "HANDOFF:" in text.upper():
        target = "general"
        for line in text.split("\n"):
            if "HANDOFF:" in line.upper():
                t = line.split(":")[-1].strip().lower()
                if t in ["hr", "tech", "finance"]:
                    target = t
        history_entry["action"] = f"handoff to {target}"
        return {"handoff_to": target,
                "conversation_history": [history_entry],
                "audit": [f"Triage → {target}"]}
    else:
        answer = text.replace("HANDLE:", "").strip()
        history_entry["action"] = "resolved"
        return {"handoff_to": "done", "response": answer,
                "conversation_history": [history_entry],
                "audit": ["Triage resolved"]}

def specialist_with_history(state: HistoryHandoffState) -> dict:
    history = "\n".join(
        f"  [{h['agent']}] {h['action']}: {h.get('notes', '')}"
        for h in state["conversation_history"]
    )
    prompt = (
        f"You are a UniGPS {state['handoff_to']} specialist.\n"
        f"Full context from previous agents:\n{history}\n\n"
        f"Original request: {state['request']}\n"
        f"Provide a helpful response in 2-3 sentences."
    )
    response = llm.invoke(prompt)
    return {
        "response": response.content.strip(),
        "conversation_history": [
            {"agent": f"{state['handoff_to']}_specialist",
             "action": "resolved",
             "notes": response.content.strip()[:50]}
        ],
        "audit": [f"Specialist resolved with full history"],
    }

def hist_route(state: HistoryHandoffState) -> str:
    return state["handoff_to"]

def hist_finalize(state: HistoryHandoffState) -> dict:
    return {"response": f"{state['response']}\n— UniGPS",
            "audit": ["Finalized"]}

g2 = StateGraph(HistoryHandoffState)
g2.add_node("triage", triage_with_history)
g2.add_node("specialist", specialist_with_history)
g2.add_node("finalize", hist_finalize)

g2.add_edge(START, "triage")
g2.add_conditional_edges("triage", hist_route, {
    "hr": "specialist", "tech": "specialist",
    "finance": "specialist", "general": "specialist",
    "done": "finalize",
})
g2.add_edge("specialist", "finalize")
g2.add_edge("finalize", END)

app2 = g2.compile()

result = app2.invoke({
    "request": "I need to change my tax declaration for this quarter",
    "handoff_to": "", "conversation_history": [],
    "response": "", "audit": [],
})
print(f"  Response: {result['response'][:70]}...")
print(f"  History ({len(result['conversation_history'])} entries):")
for h in result["conversation_history"]:
    print(f"    [{h['agent']}] {h['action']}: {h.get('notes', '')[:50]}")
print(f"  Audit: {result['audit']}")

print("\n" + "=" * 50)
print("Lab 04 Solution complete!")
print("- TODO 1: 3-level escalation (L1→L2→L3) with LLM-driven decisions")
print("- TODO 2: Full conversation history travels with handoffs")
