"""
Lab 02 Solution: Supervisor with LLM Routing
===============================================
"""

import os
from typing import TypedDict, Annotated
from operator import add
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

print("=" * 50)
print("  Supervisor with LLM Routing (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Confidence-based routing
# ============================================================

class ConfidentState(TypedDict):
    request: str
    assigned_to: str
    confidence: int
    worker_output: str
    final_response: str
    audit: Annotated[list, add]

def confident_supervisor(state: ConfidentState) -> dict:
    prompt = (
        f"You are a UniGPS support desk supervisor.\n"
        f"Classify this request into: hr, tech, finance, general\n"
        f"Also rate your confidence 1-10.\n"
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
                if cat in ["hr", "tech", "finance", "general"]:
                    category = cat
            elif "confidence:" in line:
                try:
                    confidence = int(line.split(":")[-1].strip().rstrip("."))
                    confidence = max(1, min(10, confidence))
                except ValueError:
                    confidence = 5
        print(f"  [supervisor] {category} (confidence: {confidence}/10)")
        return {"assigned_to": category, "confidence": confidence,
                "audit": [f"Classified: {category} (conf: {confidence})"]}
    except Exception as e:
        print(f"  [supervisor] Error: {e}")
        return {"assigned_to": "general", "confidence": 1,
                "audit": [f"LLM error, fallback to general"]}

def route_with_confidence(state: ConfidentState) -> str:
    if state["confidence"] < 5:
        return "clarify"
    return state["assigned_to"]

def clarify_agent(state: ConfidentState) -> dict:
    return {
        "worker_output": f"I'm not sure I understand your request: '{state['request']}'. "
                         f"Could you provide more details?",
        "audit": ["Clarification requested (low confidence)"],
    }

def hr_agent(state: ConfidentState) -> dict:
    response = llm.invoke(
        f"You are UniGPS HR. Reply helpfully in 2 sentences.\n"
        f"Request: {state['request']}"
    )
    return {"worker_output": response.content.strip(), "audit": ["HR agent"]}

def tech_agent(state: ConfidentState) -> dict:
    response = llm.invoke(
        f"You are UniGPS Tech Support. Reply helpfully in 2 sentences.\n"
        f"Request: {state['request']}"
    )
    return {"worker_output": response.content.strip(), "audit": ["Tech agent"]}

def finance_agent(state: ConfidentState) -> dict:
    response = llm.invoke(
        f"You are UniGPS Finance. Reply helpfully in 2 sentences.\n"
        f"Request: {state['request']}"
    )
    return {"worker_output": response.content.strip(), "audit": ["Finance agent"]}

def general_agent(state: ConfidentState) -> dict:
    return {"worker_output": "Your request has been logged.", "audit": ["General agent"]}

def format_response(state: ConfidentState) -> dict:
    return {
        "final_response": f"[{state['assigned_to'].upper()}] {state['worker_output']}\n— UniGPS",
        "audit": ["Formatted"],
    }

graph = StateGraph(ConfidentState)
graph.add_node("supervisor", confident_supervisor)
graph.add_node("clarify", clarify_agent)
graph.add_node("hr_agent", hr_agent)
graph.add_node("tech_agent", tech_agent)
graph.add_node("finance_agent", finance_agent)
graph.add_node("general_agent", general_agent)
graph.add_node("format", format_response)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges("supervisor", route_with_confidence, {
    "clarify": "clarify",
    "hr": "hr_agent",
    "tech": "tech_agent",
    "finance": "finance_agent",
    "general": "general_agent",
})
for node in ["clarify", "hr_agent", "tech_agent", "finance_agent", "general_agent"]:
    graph.add_edge(node, "format")
graph.add_edge("format", END)

app = graph.compile()

print("\n--- TODO 1: Confidence-Based Routing ---\n")

tests = [
    "I need to apply for maternity leave",
    "asdfghjkl gibberish",
    "Something about the thing",
    "My laptop crashed and I lost all my work",
]

for req in tests:
    result = app.invoke({"request": req, "confidence": 0, "audit": []})
    print(f"  '{req}'")
    print(f"  → [{result['assigned_to']}] conf={result['confidence']} | {result['final_response'][:60]}...")
    print()

# ============================================================
# TODO 2 Solution: Supervisor with memory
# ============================================================

print("\n--- TODO 2: Supervisor with Memory ---\n")

class ConvoState(TypedDict):
    request: str
    history: Annotated[list, add]
    assigned_to: str
    confidence: int
    worker_output: str
    final_response: str
    audit: Annotated[list, add]

def memory_supervisor(state: ConvoState) -> dict:
    history_str = "\n".join(state["history"][-5:]) if state["history"] else "No history"
    prompt = (
        f"You are UniGPS support supervisor.\n"
        f"Conversation history:\n{history_str}\n\n"
        f"New request: {state['request']}\n"
        f"Classify: hr, tech, finance, general\n"
        f"Reply:\nCATEGORY: ...\nCONFIDENCE: ..."
    )
    response = llm.invoke(prompt)
    text = response.content.lower()
    category = "general"
    confidence = 5
    for line in text.split("\n"):
        if "category:" in line:
            cat = line.split(":")[-1].strip()
            if cat in ["hr", "tech", "finance", "general"]:
                category = cat
        elif "confidence:" in line:
            try:
                confidence = int(line.split(":")[-1].strip().rstrip("."))
            except ValueError:
                confidence = 5
    print(f"  [supervisor] {category} (conf: {confidence})")
    return {"assigned_to": category, "confidence": confidence,
            "history": [f"[User] {state['request']}"],
            "audit": [f"Classified: {category}"]}

def memory_worker(state: ConvoState) -> dict:
    history_str = "\n".join(state["history"][-5:])
    prompt = (
        f"You are a UniGPS {state['assigned_to']} agent.\n"
        f"Conversation:\n{history_str}\n"
        f"Reply helpfully in 2 sentences."
    )
    response = llm.invoke(prompt)
    output = response.content.strip()
    return {"worker_output": output,
            "history": [f"[{state['assigned_to'].upper()} Agent] {output[:80]}"],
            "audit": [f"{state['assigned_to']} agent responded"]}

def memory_format(state: ConvoState) -> dict:
    return {"final_response": f"[{state['assigned_to'].upper()}] {state['worker_output']}\n— UniGPS",
            "audit": ["Formatted"]}

g2 = StateGraph(ConvoState)
g2.add_node("supervisor", memory_supervisor)
g2.add_node("worker", memory_worker)
g2.add_node("format", memory_format)

g2.add_edge(START, "supervisor")
g2.add_edge("supervisor", "worker")
g2.add_edge("worker", "format")
g2.add_edge("format", END)

memory = MemorySaver()
app2 = g2.compile(checkpointer=memory)

config = {"configurable": {"thread_id": "convo-001"}}

# Turn 1
result = app2.invoke({"request": "I need leave next week", "history": [], "audit": []}, config)
print(f"  Turn 1: '{result['final_response'][:60]}...'")

# Turn 2: follow-up (supervisor sees history)
result = app2.invoke({"request": "Actually, make it 5 days instead of 3", "history": [], "audit": []}, config)
print(f"  Turn 2: '{result['final_response'][:60]}...'")

# Check history
snap = app2.get_state(config)
print(f"\n  Conversation history ({len(snap.values.get('history', []))} messages):")
for h in snap.values.get("history", []):
    print(f"    {h[:70]}...")

print("\n" + "=" * 50)
print("Lab 02 Solution complete!")
print("- TODO 1: Low-confidence → clarify instead of wrong routing")
print("- TODO 2: MemorySaver preserves conversation context across turns")
