"""
Lab 06 Solution: Checkpointing
================================
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
print("  Checkpointing (Solution)")
print("=" * 50)

# ============================================================
# Core workflow (same as lab)
# ============================================================

class SupportState(TypedDict):
    message: str
    category: str
    response: str
    log: Annotated[list, add]

def classify(state: SupportState) -> dict:
    prompt = (
        f"Classify this support request into exactly one category: "
        f"hr, tech, finance, or general.\n"
        f"Request: {state['message']}\n"
        f"Reply with ONLY the category name, nothing else."
    )
    response = llm.invoke(prompt)
    category = response.content.strip().lower()
    if category not in ["hr", "tech", "finance", "general"]:
        category = "general"
    print(f"  [classify] '{state['message'][:40]}' → {category}")
    return {"category": category, "log": [f"Classified as: {category}"]}

def respond(state: SupportState) -> dict:
    prompt = (
        f"You are a UniGPS support assistant. "
        f"Write a brief, helpful response for this {state['category']} request:\n"
        f"{state['message']}\nKeep it under 2 sentences."
    )
    response = llm.invoke(prompt)
    text = response.content.strip()
    print(f"  [respond] → {text[:60]}...")
    return {"response": text, "log": [f"Response generated"]}

graph = StateGraph(SupportState)
graph.add_node("classify", classify)
graph.add_node("respond", respond)
graph.add_edge(START, "classify")
graph.add_edge("classify", "respond")
graph.add_edge("respond", END)

memory = MemorySaver()
app = graph.compile(checkpointer=memory)

# ============================================================
# Run multiple threads
# ============================================================

configs = {
    "ticket-001": "I need to apply for sick leave",
    "ticket-002": "Production database is running slow",
    "ticket-003": "How do I submit my expense report?",
}

print("\n--- Running Workflows ---")
for tid, msg in configs.items():
    config = {"configurable": {"thread_id": tid}}
    result = app.invoke({"message": msg, "log": []}, config)
    print(f"\n  {tid}: {result['category']} — {result['response'][:50]}...")

# ============================================================
# TODO 1 Solution: Rerun capability
# ============================================================

print("\n--- TODO 1: Rerun on Same Thread ---")
config = {"configurable": {"thread_id": "rerun-test"}}

result1 = app.invoke({"message": "I need leave", "log": []}, config)
snap1 = app.get_state(config)
print(f"After run 1: category={snap1.values['category']}, message='{snap1.values['message']}'")

result2 = app.invoke({"message": "Server is down", "log": []}, config)
snap2 = app.get_state(config)
print(f"After run 2: category={snap2.values['category']}, message='{snap2.values['message']}'")

print("→ New run OVERWRITES the state with fresh data!")
print("  Each invoke() starts a new execution on that thread.")

# ============================================================
# TODO 2 Solution: Count checkpoints
# ============================================================

print("\n--- TODO 2: Counting Checkpoints ---")
config_count = {"configurable": {"thread_id": "ticket-001"}}
checkpoints = list(app.get_state_history(config_count))
print(f"Total checkpoints for ticket-001: {len(checkpoints)}")

print("\nCheckpoint details:")
for i, cp in enumerate(checkpoints):
    keys_with_values = [k for k, v in cp.values.items() if v]
    print(f"  Checkpoint {i}: next={cp.next}, populated_keys={keys_with_values}")

print(f"\n→ For a graph with 2 nodes (classify + respond):")
print(f"  You see {len(checkpoints)} checkpoints:")
print(f"  - After START (initial state)")
print(f"  - After classify")
print(f"  - After respond (final state)")
print(f"  Plus the graph's internal tracking checkpoints")

print("\n" + "=" * 50)
print("Lab 06 Solution complete!")
print("- TODO 1: Re-invoking same thread overwrites with new data")
print("- TODO 2: Checkpoints = N+1 for N nodes (plus internal ones)")
