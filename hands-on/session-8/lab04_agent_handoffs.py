"""
Lab 04: Agent Handoffs
========================
Goal: Build agents that transfer control to other agents mid-workflow,
      including escalation chains.

What you'll learn:
- Explicit handoff via state field
- Context transfer between agents
- Escalation chains (L1 → L2 → L3)

Requires: GROQ_API_KEY in .env
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
print("  Agent Handoffs")
print("=" * 50)

# ============================================================
# Step 1: Triage agent with handoff
# ============================================================
# Triage → [handle_self | handoff → specialist] → finalize

class HandoffState(TypedDict):
    request: str
    handoff_to: str
    context_notes: str
    response: str
    audit: Annotated[list, add]

def triage_agent(state: HandoffState) -> dict:
    """L1 triage: handle simple requests, handoff complex ones."""
    prompt = (
        f"You are a Level-1 support agent at UniGPS.\n"
        f"Analyze this request. Can you handle it with a simple answer?\n"
        f"Request: {state['request']}\n\n"
        f"If simple (greetings, FAQs), reply: HANDLE: <your answer>\n"
        f"If complex (needs specialist), reply: HANDOFF: hr or tech or finance\n"
        f"Also add a brief note for the specialist on a new line starting with NOTE:"
    )
    response = llm.invoke(prompt)
    text = response.content.strip()

    if "HANDOFF:" in text.upper():
        # Extract target
        for line in text.split("\n"):
            if "HANDOFF:" in line.upper():
                target = line.split(":")[-1].strip().lower()
                if target not in ["hr", "tech", "finance"]:
                    target = "general"
                break
        # Extract note
        note = ""
        for line in text.split("\n"):
            if "NOTE:" in line.upper():
                note = line.split(":", 1)[-1].strip()
        print(f"  [triage] Handing off to: {target}")
        return {
            "handoff_to": target,
            "context_notes": note,
            "audit": [f"Triage → handoff to {target}: {note[:40]}"],
        }
    else:
        # Handle directly
        answer = text.replace("HANDLE:", "").strip()
        print(f"  [triage] Handling directly")
        return {
            "handoff_to": "done",
            "response": answer,
            "audit": ["Triage handled directly"],
        }

def route_handoff(state: HandoffState) -> str:
    return state["handoff_to"]

def hr_specialist(state: HandoffState) -> dict:
    prompt = (
        f"You are a UniGPS HR specialist.\n"
        f"Context from triage: {state['context_notes']}\n"
        f"Employee request: {state['request']}\n"
        f"Provide a detailed, helpful response in 2-3 sentences."
    )
    response = llm.invoke(prompt)
    print(f"  [HR specialist] Responding...")
    return {"response": response.content.strip(), "audit": ["HR specialist responded"]}

def tech_specialist(state: HandoffState) -> dict:
    prompt = (
        f"You are a UniGPS Tech specialist.\n"
        f"Context from triage: {state['context_notes']}\n"
        f"Employee request: {state['request']}\n"
        f"Provide a detailed, helpful response in 2-3 sentences."
    )
    response = llm.invoke(prompt)
    print(f"  [Tech specialist] Responding...")
    return {"response": response.content.strip(), "audit": ["Tech specialist responded"]}

def finance_specialist(state: HandoffState) -> dict:
    prompt = (
        f"You are a UniGPS Finance specialist.\n"
        f"Context from triage: {state['context_notes']}\n"
        f"Employee request: {state['request']}\n"
        f"Provide a detailed, helpful response in 2-3 sentences."
    )
    response = llm.invoke(prompt)
    print(f"  [Finance specialist] Responding...")
    return {"response": response.content.strip(), "audit": ["Finance specialist responded"]}

def general_handler(state: HandoffState) -> dict:
    return {
        "response": "Your request has been logged. A team member will follow up.",
        "audit": ["General handler used"],
    }

def finalize(state: HandoffState) -> dict:
    return {
        "response": f"{state['response']}\n— UniGPS Support",
        "audit": ["Finalized"],
    }

graph = StateGraph(HandoffState)
graph.add_node("triage", triage_agent)
graph.add_node("hr_specialist", hr_specialist)
graph.add_node("tech_specialist", tech_specialist)
graph.add_node("finance_specialist", finance_specialist)
graph.add_node("general", general_handler)
graph.add_node("finalize", finalize)

graph.add_edge(START, "triage")
graph.add_conditional_edges("triage", route_handoff, {
    "hr": "hr_specialist",
    "tech": "tech_specialist",
    "finance": "finance_specialist",
    "general": "general",
    "done": "finalize",
})
for node in ["hr_specialist", "tech_specialist", "finance_specialist", "general"]:
    graph.add_edge(node, "finalize")
graph.add_edge("finalize", END)

app = graph.compile()

print("\nGraph: triage → [handle | handoff→specialist] → finalize → END\n")

test_requests = [
    "Hello, good morning!",
    "I need to apply for paternity leave for 2 weeks",
    "Our staging database keeps crashing every night",
    "Can you check the status of my expense reimbursement?",
]

for req in test_requests:
    result = app.invoke({"request": req, "handoff_to": "", "context_notes": "", "response": "", "audit": []})
    print(f"  Request: '{req}'")
    print(f"  Handoff: {result.get('handoff_to', 'N/A')}")
    print(f"  Response: {result['response'][:70]}...")
    print(f"  Audit: {result['audit']}")
    print()

# ============================================================
# TODO 1: Multi-level escalation (L1 → L2 → L3)
# ============================================================
# Build a 3-level escalation chain:
#   L1 (triage) → L2 (specialist) → L3 (manager)
# L2 can escalate to L3 if the issue is too complex.
#
# Hint:
#   - Add an "escalation_level" field to state
#   - L2 specialist returns escalate_to: "manager" or "done"
#   - L3 manager always handles (no further escalation)
#
# class EscalationState(TypedDict):
#     request: str
#     handoff_to: str
#     escalation_level: int      # 1, 2, or 3
#     context_notes: str
#     response: str
#     audit: Annotated[list, add]
#
# def l2_specialist(state: EscalationState) -> dict:
#     """L2 specialist: handle or escalate to L3."""
#     prompt = (
#         f"You are a Level-2 specialist at UniGPS.\n"
#         f"Request: {state['request']}\n"
#         f"Context: {state['context_notes']}\n\n"
#         f"If you can handle this, reply: RESOLVE: <your answer>\n"
#         f"If this needs a manager (policy exceptions, high cost), reply: ESCALATE: <reason>"
#     )
#     ...
#
# def l3_manager(state: EscalationState) -> dict:
#     """L3 manager: final authority."""
#     ...
#
# Test: "I need a policy exception for 30 days leave" → should escalate to L3


# ============================================================
# TODO 2: Handoff with conversation history
# ============================================================
# When handing off, include the full conversation history so the
# specialist has full context.
#
# Hint: Use Annotated[list, add] for conversation_history and
#       append each agent's interaction.
#
# class HistoryHandoffState(TypedDict):
#     request: str
#     handoff_to: str
#     conversation_history: Annotated[list, add]
#     response: str
#     audit: Annotated[list, add]
#
# def triage_with_history(state: HistoryHandoffState) -> dict:
#     ...
#     return {
#         "handoff_to": target,
#         "conversation_history": [
#             {"agent": "triage", "action": "classified", "notes": note}
#         ],
#         ...
#     }
#
# def specialist_with_history(state: HistoryHandoffState) -> dict:
#     """Specialist reads full conversation history."""
#     history = "\n".join(
#         f"  [{h['agent']}] {h['action']}: {h.get('notes', '')}"
#         for h in state["conversation_history"]
#     )
#     prompt = f"Full context:\n{history}\nRequest: {state['request']}"
#     ...


print("\n" + "=" * 50)
print("Lab 04 complete!")
print("Patterns: triage handoff, context transfer, specialist routing")
