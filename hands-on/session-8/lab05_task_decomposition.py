"""
Lab 05: Task Decomposition
============================
Goal: Build a supervisor that decomposes complex requests into
      sub-tasks and dispatches them to workers.

What you'll learn:
- LLM-powered task decomposition
- Parallel sub-task execution via fan-out
- Collecting results from multiple workers

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
print("  Task Decomposition")
print("=" * 50)

# ============================================================
# Step 1: Supervisor decomposes into sub-tasks
# ============================================================

class DecompState(TypedDict):
    request: str
    subtasks: list
    current_subtask: str
    results: Annotated[list, add]
    final_response: str
    audit: Annotated[list, add]

def decompose(state: DecompState) -> dict:
    """LLM breaks the request into sub-tasks."""
    prompt = (
        f"You are a task planner at UniGPS.\n"
        f"Break this request into 2-3 simple sub-tasks.\n"
        f"Request: {state['request']}\n\n"
        f"Reply with one sub-task per line, numbered:\n"
        f"1. ...\n2. ...\n3. ..."
    )
    response = llm.invoke(prompt)
    lines = response.content.strip().split("\n")
    subtasks = []
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit():
            # Remove number prefix
            task = line.lstrip("0123456789.").strip()
            if task:
                subtasks.append(task)
    if not subtasks:
        subtasks = [state["request"]]
    print(f"  [decompose] {len(subtasks)} sub-tasks identified:")
    for i, t in enumerate(subtasks, 1):
        print(f"    {i}. {t[:60]}")
    return {
        "subtasks": subtasks,
        "current_subtask": subtasks[0] if subtasks else "",
        "audit": [f"Decomposed into {len(subtasks)} sub-tasks"],
    }

def execute_subtask(state: DecompState) -> dict:
    """Execute the current sub-task."""
    task = state["current_subtask"]
    prompt = (
        f"You are a UniGPS support agent.\n"
        f"Complete this sub-task in 1-2 sentences:\n{task}"
    )
    response = llm.invoke(prompt)
    result = response.content.strip()
    print(f"  [execute] '{task[:40]}' → done")
    return {
        "results": [{"task": task, "result": result}],
        "audit": [f"Completed: {task[:40]}"],
    }

def advance_subtask(state: DecompState) -> dict:
    """Move to the next sub-task."""
    completed = len(state["results"])
    remaining = state["subtasks"][completed:]
    if remaining:
        return {"current_subtask": remaining[0]}
    return {"current_subtask": ""}

def route_subtasks(state: DecompState) -> str:
    """Check if there are more sub-tasks."""
    completed = len(state["results"])
    if completed < len(state["subtasks"]):
        return "execute"
    return "aggregate"

def aggregate(state: DecompState) -> dict:
    """Combine all sub-task results."""
    combined = "\n".join(
        f"• {r['task']}: {r['result'][:80]}"
        for r in state["results"]
    )
    print(f"  [aggregate] Combined {len(state['results'])} results")
    return {
        "final_response": f"Here's what we've done:\n{combined}\n— UniGPS Support",
        "audit": [f"Aggregated {len(state['results'])} results"],
    }

graph = StateGraph(DecompState)
graph.add_node("decompose", decompose)
graph.add_node("execute", execute_subtask)
graph.add_node("advance", advance_subtask)
graph.add_node("aggregate", aggregate)

graph.add_edge(START, "decompose")
graph.add_edge("decompose", "execute")
graph.add_edge("execute", "advance")
graph.add_conditional_edges("advance", route_subtasks, {
    "execute": "execute",
    "aggregate": "aggregate",
})
graph.add_edge("aggregate", END)

app = graph.compile()

print("\nGraph: decompose → [execute → advance → loop] → aggregate → END\n")

test_requests = [
    "Onboard new employee Priya Sharma: create HR record, set up laptop, and assign desk",
    "Prepare for client visit: book conference room and arrange lunch",
]

for req in test_requests:
    print(f"--- Request: {req[:60]}... ---")
    result = app.invoke({
        "request": req,
        "subtasks": [],
        "current_subtask": "",
        "results": [],
        "final_response": "",
        "audit": [],
    })
    print(f"\nResponse:\n{result['final_response'][:200]}")
    print(f"Audit: {result['audit']}")
    print()

# ============================================================
# TODO 1: Parallel sub-task execution
# ============================================================
# Instead of executing sub-tasks one at a time, execute them
# in parallel using fan-out edges.
#
# Hint: Create separate worker nodes for different domains
#       and fan-out from decompose to all workers simultaneously.
#
# class ParallelDecompState(TypedDict):
#     request: str
#     hr_task: str
#     tech_task: str
#     facilities_task: str
#     results: Annotated[list, add]  # ← reducer merges parallel results
#     final_response: str
#     audit: Annotated[list, add]
#
# def decompose_parallel(state: ParallelDecompState) -> dict:
#     """Decompose and assign tasks to specific workers."""
#     prompt = (
#         f"Break this into HR, Tech, and Facilities tasks.\n"
#         f"Request: {state['request']}\n"
#         f"Reply:\nHR: ...\nTECH: ...\nFACILITIES: ..."
#     )
#     ...
#
# def hr_worker(state: ParallelDecompState) -> dict:
#     if not state["hr_task"]: return {"results": []}
#     ...
#
# # Fan-out: decompose → [hr_worker, tech_worker, facilities_worker]
# # Converge: all workers → aggregate
# graph.add_edge("decompose", "hr_worker")
# graph.add_edge("decompose", "tech_worker")
# graph.add_edge("decompose", "facilities_worker")
# graph.add_edge("hr_worker", "aggregate")
# graph.add_edge("tech_worker", "aggregate")
# graph.add_edge("facilities_worker", "aggregate")


# ============================================================
# TODO 2: Decomposition with dependency ordering
# ============================================================
# Some sub-tasks depend on others. Build a system where the
# decomposer identifies dependencies and executes in order.
#
# Example: "Set up employee account then grant VPN access"
#   Task 1: Create account (no dependency)
#   Task 2: Grant VPN access (depends on Task 1)
#
# Hint: Add a "dependencies" field to each subtask.
#
# subtasks = [
#     {"task": "Create employee account", "depends_on": None},
#     {"task": "Grant VPN access", "depends_on": "Create employee account"},
# ]
#
# def route_with_deps(state) -> str:
#     """Only execute tasks whose dependencies are complete."""
#     completed_tasks = [r["task"] for r in state["results"]]
#     for st in state["subtasks"]:
#         if st["task"] not in completed_tasks:
#             dep = st["depends_on"]
#             if dep is None or dep in completed_tasks:
#                 return "execute"  # ready to execute
#     return "aggregate"  # all done


print("\n" + "=" * 50)
print("Lab 05 complete!")
print("Patterns: LLM decomposition, sequential execution, aggregation")
