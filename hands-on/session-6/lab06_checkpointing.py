"""
Lab 06: Checkpointing
======================
Goal: Learn how to save and resume workflow state using checkpointers,
      inspect state at any point, and manage multiple workflow threads.

What you'll learn:
- Compiling with MemorySaver for state persistence
- Using thread_id to manage separate workflow instances
- Inspecting state with get_state()
- How checkpoints let you resume or replay workflows

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

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

print("=" * 50)
print("  Checkpointing")
print("=" * 50)

# ============================================================
# Step 1: Compile with a checkpointer
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
    # Ensure valid category
    if category not in ["hr", "tech", "finance", "general"]:
        category = "general"
    print(f"  [classify] '{state['message'][:40]}' → {category}")
    return {"category": category, "log": [f"Classified as: {category}"]}

def respond(state: SupportState) -> dict:
    prompt = (
        f"You are a UniGPS support assistant. "
        f"Write a brief, helpful response for this {state['category']} request:\n"
        f"{state['message']}\n"
        f"Keep it under 2 sentences."
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

# ← KEY: Compile with MemorySaver checkpointer
memory = MemorySaver()
app = graph.compile(checkpointer=memory)

print("\n--- Step 1: Checkpointed Workflow ---")
print("Graph: START → classify → respond → END")
print("Compiled with MemorySaver — state saved after each node!\n")

# ============================================================
# Step 2: Run with a thread_id
# ============================================================
# thread_id identifies a unique workflow instance.
# The checkpointer saves state for each thread separately.

config_1 = {"configurable": {"thread_id": "ticket-001"}}
result = app.invoke({"message": "I need to apply for sick leave", "log": []}, config_1)

print("--- Step 2: Run with thread_id ---")
print(f"Thread: ticket-001")
print(f"Category: {result['category']}")
print(f"Response: {result['response']}")
print(f"Log: {result['log']}")

# ============================================================
# Step 3: Inspect state with get_state()
# ============================================================
# After running, we can inspect what was saved.

print("\n--- Step 3: Inspect Saved State ---")
snapshot = app.get_state(config_1)

print(f"Saved state values:")
for key, value in snapshot.values.items():
    display = str(value)[:60] + "..." if len(str(value)) > 60 else str(value)
    print(f"  {key}: {display}")

print(f"\nNext node to run: {snapshot.next}")
print("→ Empty tuple means workflow completed!")

# ============================================================
# Step 4: Multiple threads — separate conversations
# ============================================================

print("\n--- Step 4: Multiple Threads ---")

config_2 = {"configurable": {"thread_id": "ticket-002"}}
config_3 = {"configurable": {"thread_id": "ticket-003"}}

result2 = app.invoke({"message": "Production database is running slow", "log": []}, config_2)
result3 = app.invoke({"message": "How do I submit my expense report?", "log": []}, config_3)

# Each thread has its own saved state
for tid, cfg in [("ticket-001", config_1), ("ticket-002", config_2), ("ticket-003", config_3)]:
    snap = app.get_state(cfg)
    print(f"\n  Thread {tid}:")
    print(f"    Message:  {snap.values['message'][:50]}")
    print(f"    Category: {snap.values['category']}")
    print(f"    Log:      {snap.values['log']}")

print("\n→ Each thread maintains its own independent state!")

# ============================================================
# Step 5: State history — walk through checkpoints
# ============================================================

print("\n--- Step 5: State History ---")
print("Walking through checkpoints for ticket-001:\n")

for i, state in enumerate(app.get_state_history(config_1)):
    print(f"  Checkpoint {i}:")
    print(f"    Next: {state.next}")
    keys = list(state.values.keys())
    print(f"    Keys in state: {keys}")
    if "category" in state.values:
        print(f"    Category: {state.values['category']}")

print("\n→ Checkpointers record state after EVERY node execution!")

# ============================================================
# TODO 1: Add a "rerun" capability
# ============================================================
# Using checkpointing, implement the following:
# 1. Run a workflow with thread_id "rerun-test"
# 2. Inspect the state with get_state()
# 3. Run a NEW message on the SAME thread_id
# 4. Inspect the state again — what changed?
# Does the new run overwrite the old state or create new checkpoints?

# config = {"configurable": {"thread_id": "rerun-test"}}
# result1 = app.invoke({"message": "I need leave", "log": []}, config)
# snap1 = app.get_state(config)
# print(f"After run 1: {snap1.values['category']}")
#
# result2 = app.invoke({"message": "Server is down", "log": []}, config)
# snap2 = app.get_state(config)
# print(f"After run 2: {snap2.values['category']}")

# ============================================================
# TODO 2: Count checkpoints
# ============================================================
# Use get_state_history() to count how many checkpoints exist
# for a given thread. Then answer: if a graph has N nodes,
# how many checkpoints are created per invoke()?

# config = {"configurable": {"thread_id": "ticket-001"}}
# checkpoints = list(app.get_state_history(config))
# print(f"Total checkpoints: {len(checkpoints)}")
# # For a graph with 2 nodes (classify + respond),
# # how many checkpoints do you see? Why?

print("\n" + "=" * 50)
print("Lab 06 complete! Key takeaways:")
print("- MemorySaver() saves state after every node execution")
print("- thread_id separates different workflow instances")
print("- get_state(config) returns the latest snapshot")
print("- get_state_history(config) returns ALL checkpoints")
print("- Checkpointing is the foundation for human-in-the-loop")
