"""
Lab 02: Supervisor with LLM Routing
======================================
Goal: Build a supervisor that uses an LLM to classify and route
      requests, instead of keyword matching.

What you'll learn:
- LLM-powered supervisor agent
- Dynamic worker selection based on LLM classification
- Handling LLM classification errors gracefully

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
print("  Supervisor with LLM Routing")
print("=" * 50)

# ============================================================
# Step 1: LLM supervisor classifies requests
# ============================================================

class AgentState(TypedDict):
    request: str
    assigned_to: str
    worker_output: str
    final_response: str
    audit: Annotated[list, add]

def llm_supervisor(state: AgentState) -> dict:
    """Use LLM to classify and route the request."""
    prompt = (
        f"You are a support desk supervisor at UniGPS.\n"
        f"Classify this request into exactly one category: hr, tech, finance, general\n"
        f"Request: {state['request']}\n"
        f"Reply with just the category name, nothing else."
    )
    try:
        response = llm.invoke(prompt)
        category = response.content.strip().lower()
        # Validate LLM output
        valid = ["hr", "tech", "finance", "general"]
        if category not in valid:
            print(f"  [supervisor] LLM returned '{category}', defaulting to general")
            category = "general"
        print(f"  [supervisor] LLM classified → {category}")
        return {"assigned_to": category, "audit": [f"LLM classified: {category}"]}
    except Exception as e:
        print(f"  [supervisor] LLM error: {e}, defaulting to general")
        return {"assigned_to": "general", "audit": [f"LLM failed, fallback: general"]}

def route_worker(state: AgentState) -> str:
    return state["assigned_to"]

def hr_agent(state: AgentState) -> dict:
    """HR specialist agent with LLM."""
    response = llm.invoke(
        f"You are UniGPS HR agent. Reply helpfully in 2 sentences.\n"
        f"Employee request: {state['request']}"
    )
    return {"worker_output": response.content.strip(), "audit": ["HR agent responded"]}

def tech_agent(state: AgentState) -> dict:
    """Tech support specialist agent with LLM."""
    response = llm.invoke(
        f"You are UniGPS Tech Support. Reply helpfully in 2 sentences.\n"
        f"Employee request: {state['request']}"
    )
    return {"worker_output": response.content.strip(), "audit": ["Tech agent responded"]}

def finance_agent(state: AgentState) -> dict:
    """Finance specialist agent with LLM."""
    response = llm.invoke(
        f"You are UniGPS Finance team. Reply helpfully in 2 sentences.\n"
        f"Employee request: {state['request']}"
    )
    return {"worker_output": response.content.strip(), "audit": ["Finance agent responded"]}

def general_agent(state: AgentState) -> dict:
    return {
        "worker_output": "Your request has been logged. Our team will get back to you.",
        "audit": ["General agent responded"],
    }

def format_response(state: AgentState) -> dict:
    return {
        "final_response": f"[{state['assigned_to'].upper()}] {state['worker_output']}\n— UniGPS Support",
        "audit": ["Response formatted"],
    }

# Build graph
graph = StateGraph(AgentState)
graph.add_node("supervisor", llm_supervisor)
graph.add_node("hr_agent", hr_agent)
graph.add_node("tech_agent", tech_agent)
graph.add_node("finance_agent", finance_agent)
graph.add_node("general_agent", general_agent)
graph.add_node("format", format_response)

graph.add_edge(START, "supervisor")
graph.add_conditional_edges("supervisor", route_worker, {
    "hr": "hr_agent",
    "tech": "tech_agent",
    "finance": "finance_agent",
    "general": "general_agent",
})
for agent in ["hr_agent", "tech_agent", "finance_agent", "general_agent"]:
    graph.add_edge(agent, "format")
graph.add_edge("format", END)

app = graph.compile()

print("\nGraph: LLM_supervisor → [hr|tech|finance|general] → format → END\n")

test_requests = [
    "I want to take 3 days off next week for a family function",
    "My laptop screen is flickering since this morning",
    "When will the Diwali bonus be credited?",
    "Can we get better coffee in the pantry?",
]

for req in test_requests:
    result = app.invoke({"request": req, "audit": []})
    print(f"  Request: '{req}'")
    print(f"  Assigned: {result['assigned_to']}")
    print(f"  Response: {result['final_response'][:70]}...")
    print()

# ============================================================
# TODO 1: Add confidence-based routing
# ============================================================
# Modify the supervisor to also return a confidence score (1-10).
# If confidence < 5, route to a "clarify" agent that asks the user
# for more details instead of routing to a worker.
#
# Hint: Change the LLM prompt to return both CATEGORY and CONFIDENCE.
#
# class ConfidentState(TypedDict):
#     request: str
#     assigned_to: str
#     confidence: int
#     worker_output: str
#     final_response: str
#     audit: Annotated[list, add]
#
# def confident_supervisor(state: ConfidentState) -> dict:
#     prompt = (
#         f"Classify this request into: hr, tech, finance, general\n"
#         f"Also rate your confidence 1-10.\n"
#         f"Request: {state['request']}\n"
#         f"Reply:\nCATEGORY: ...\nCONFIDENCE: ..."
#     )
#     ...
#
# def clarify_agent(state: ConfidentState) -> dict:
#     return {"worker_output": f"I'm not sure I understand. Could you provide more details about: '{state['request']}'?"}
#
# def route_with_confidence(state: ConfidentState) -> str:
#     if state["confidence"] < 5:
#         return "clarify"
#     return state["assigned_to"]
#
# Test: "asdfgh" (should clarify), "I need leave" (should route to HR)


# ============================================================
# TODO 2: Supervisor with memory (iterative)
# ============================================================
# Build a supervisor that remembers conversation history.
# Each invocation adds to the conversation, so the supervisor
# can handle follow-up requests.
#
# Hint: Use MemorySaver checkpointer + thread_id.
#
# from langgraph.checkpoint.memory import MemorySaver
#
# class ConvoState(TypedDict):
#     request: str
#     history: Annotated[list, add]
#     assigned_to: str
#     worker_output: str
#     final_response: str
#     audit: Annotated[list, add]
#
# def memory_supervisor(state: ConvoState) -> dict:
#     """Supervisor that uses conversation history for context."""
#     history_str = "\n".join(state["history"][-5:])  # last 5 messages
#     prompt = (
#         f"You are UniGPS support supervisor.\n"
#         f"Conversation history:\n{history_str}\n\n"
#         f"New request: {state['request']}\n"
#         f"Classify into: hr, tech, finance, general"
#     )
#     ...
#
# memory = MemorySaver()
# app = graph.compile(checkpointer=memory)
# config = {"configurable": {"thread_id": "convo-001"}}
#
# # Turn 1: "I need leave next week"
# # Turn 2: "Actually, make it 5 days" ← supervisor should remember context


print("\n" + "=" * 50)
print("Lab 02 complete!")
print("Patterns: LLM supervisor, error handling, dynamic routing")
