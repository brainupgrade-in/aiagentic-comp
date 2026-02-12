"""
Lab 05 Solution: Task Decomposition
======================================
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
print("  Task Decomposition (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Parallel sub-task execution
# ============================================================

class ParallelDecompState(TypedDict):
    request: str
    hr_task: str
    tech_task: str
    facilities_task: str
    results: Annotated[list, add]
    final_response: str
    audit: Annotated[list, add]

def decompose_parallel(state: ParallelDecompState) -> dict:
    """Decompose and assign tasks to specific domain workers."""
    prompt = (
        f"Break this into HR, Tech, and Facilities tasks.\n"
        f"If a domain isn't needed, write 'none' for that domain.\n"
        f"Request: {state['request']}\n"
        f"Reply:\nHR: ...\nTECH: ...\nFACILITIES: ..."
    )
    response = llm.invoke(prompt)
    text = response.content.strip()

    hr_task = ""
    tech_task = ""
    facilities_task = ""
    for line in text.split("\n"):
        line_lower = line.lower()
        if line_lower.startswith("hr:"):
            task = line.split(":", 1)[-1].strip()
            if task.lower() != "none":
                hr_task = task
        elif line_lower.startswith("tech:"):
            task = line.split(":", 1)[-1].strip()
            if task.lower() != "none":
                tech_task = task
        elif line_lower.startswith("facilities:"):
            task = line.split(":", 1)[-1].strip()
            if task.lower() != "none":
                facilities_task = task

    assigned = []
    if hr_task: assigned.append("HR")
    if tech_task: assigned.append("Tech")
    if facilities_task: assigned.append("Facilities")
    print(f"  [decompose] Assigned to: {assigned}")

    return {
        "hr_task": hr_task,
        "tech_task": tech_task,
        "facilities_task": facilities_task,
        "audit": [f"Decomposed → {assigned}"],
    }

def hr_worker(state: ParallelDecompState) -> dict:
    if not state["hr_task"]:
        return {"results": [], "audit": []}
    response = llm.invoke(
        f"You are UniGPS HR. Complete this task in 1-2 sentences:\n{state['hr_task']}"
    )
    result = response.content.strip()
    print(f"  [HR worker] Done: {result[:50]}...")
    return {"results": [{"domain": "HR", "task": state["hr_task"], "result": result}],
            "audit": [f"HR completed: {state['hr_task'][:40]}"]}

def tech_worker(state: ParallelDecompState) -> dict:
    if not state["tech_task"]:
        return {"results": [], "audit": []}
    response = llm.invoke(
        f"You are UniGPS IT. Complete this task in 1-2 sentences:\n{state['tech_task']}"
    )
    result = response.content.strip()
    print(f"  [Tech worker] Done: {result[:50]}...")
    return {"results": [{"domain": "Tech", "task": state["tech_task"], "result": result}],
            "audit": [f"Tech completed: {state['tech_task'][:40]}"]}

def facilities_worker(state: ParallelDecompState) -> dict:
    if not state["facilities_task"]:
        return {"results": [], "audit": []}
    response = llm.invoke(
        f"You are UniGPS Facilities. Complete this task in 1-2 sentences:\n{state['facilities_task']}"
    )
    result = response.content.strip()
    print(f"  [Facilities worker] Done: {result[:50]}...")
    return {"results": [{"domain": "Facilities", "task": state["facilities_task"], "result": result}],
            "audit": [f"Facilities completed: {state['facilities_task'][:40]}"]}

def aggregate(state: ParallelDecompState) -> dict:
    active_results = [r for r in state["results"] if r]
    combined = "\n".join(f"• [{r['domain']}] {r['result'][:80]}" for r in active_results)
    print(f"  [aggregate] Combined {len(active_results)} results")
    return {
        "final_response": f"Completed tasks:\n{combined}\n— UniGPS Support",
        "audit": [f"Aggregated {len(active_results)} results"],
    }

graph = StateGraph(ParallelDecompState)
graph.add_node("decompose", decompose_parallel)
graph.add_node("hr_worker", hr_worker)
graph.add_node("tech_worker", tech_worker)
graph.add_node("facilities_worker", facilities_worker)
graph.add_node("aggregate", aggregate)

graph.add_edge(START, "decompose")
# Fan-out: all 3 workers run in parallel
graph.add_edge("decompose", "hr_worker")
graph.add_edge("decompose", "tech_worker")
graph.add_edge("decompose", "facilities_worker")
# Converge
graph.add_edge("hr_worker", "aggregate")
graph.add_edge("tech_worker", "aggregate")
graph.add_edge("facilities_worker", "aggregate")
graph.add_edge("aggregate", END)

app = graph.compile()

print("\n--- TODO 1: Parallel Execution ---")
print("Graph: decompose → [HR + Tech + Facilities] → aggregate → END\n")

result = app.invoke({
    "request": "Onboard Priya Sharma: create HR record, set up laptop, assign desk",
    "hr_task": "", "tech_task": "", "facilities_task": "",
    "results": [], "final_response": "", "audit": [],
})
print(f"\nResponse:\n{result['final_response'][:200]}")
print(f"Audit: {result['audit']}")

# ============================================================
# TODO 2 Solution: Decomposition with dependency ordering
# ============================================================

print("\n\n--- TODO 2: Dependency Ordering ---\n")

class DepDecompState(TypedDict):
    request: str
    subtasks: list           # [{"task": ..., "depends_on": ...}]
    current_subtask: str
    results: Annotated[list, add]
    final_response: str
    audit: Annotated[list, add]

def decompose_with_deps(state: DepDecompState) -> dict:
    """Decompose into tasks with explicit dependencies."""
    prompt = (
        f"Break this into ordered sub-tasks.\n"
        f"Request: {state['request']}\n\n"
        f"For each task, specify if it depends on a previous task.\n"
        f"Reply:\n1. <task> [depends: none]\n2. <task> [depends: 1]\n3. <task> [depends: 2]"
    )
    response = llm.invoke(prompt)
    lines = response.content.strip().split("\n")

    subtasks = []
    for i, line in enumerate(lines):
        line = line.strip()
        if not line or not line[0].isdigit():
            continue
        # Parse dependency
        depends_on = None
        if "[depends:" in line.lower():
            dep_part = line.lower().split("[depends:")[1].split("]")[0].strip()
            if dep_part != "none":
                try:
                    dep_idx = int(dep_part) - 1
                    if 0 <= dep_idx < len(subtasks):
                        depends_on = subtasks[dep_idx]["task"]
                except ValueError:
                    pass
        # Clean task name
        task = line.lstrip("0123456789.").strip()
        task = task.split("[depends")[0].strip()
        if task:
            subtasks.append({"task": task, "depends_on": depends_on})

    if not subtasks:
        subtasks = [{"task": state["request"], "depends_on": None}]

    print(f"  [decompose] {len(subtasks)} tasks with dependencies:")
    for st in subtasks:
        dep = f" (depends on: {st['depends_on'][:30]})" if st['depends_on'] else " (independent)"
        print(f"    - {st['task'][:50]}{dep}")

    return {"subtasks": subtasks, "audit": [f"Decomposed: {len(subtasks)} tasks"]}

def find_and_execute_next(state: DepDecompState) -> dict:
    """Find the next task whose dependencies are met and execute it."""
    completed_tasks = [r["task"] for r in state["results"]]

    for st in state["subtasks"]:
        if st["task"] in completed_tasks:
            continue
        dep = st["depends_on"]
        if dep is None or dep in completed_tasks:
            # This task is ready
            task = st["task"]
            response = llm.invoke(f"Complete this task in 1 sentence:\n{task}")
            result = response.content.strip()
            print(f"  [execute] '{task[:40]}' → done")
            return {
                "current_subtask": task,
                "results": [{"task": task, "result": result}],
                "audit": [f"Completed: {task[:40]}"],
            }
    return {"current_subtask": "", "audit": ["No executable tasks found"]}

def route_deps(state: DepDecompState) -> str:
    completed = [r["task"] for r in state["results"]]
    for st in state["subtasks"]:
        if st["task"] not in completed:
            dep = st["depends_on"]
            if dep is None or dep in completed:
                return "execute"
    return "aggregate"

def dep_aggregate(state: DepDecompState) -> dict:
    combined = "\n".join(f"• {r['task'][:40]}: {r['result'][:60]}" for r in state["results"])
    return {"final_response": f"All tasks completed:\n{combined}\n— UniGPS",
            "audit": [f"Aggregated {len(state['results'])} results"]}

g2 = StateGraph(DepDecompState)
g2.add_node("decompose", decompose_with_deps)
g2.add_node("execute", find_and_execute_next)
g2.add_node("aggregate", dep_aggregate)

g2.add_edge(START, "decompose")
g2.add_edge("decompose", "execute")
g2.add_conditional_edges("execute", route_deps, {
    "execute": "execute",
    "aggregate": "aggregate",
})
g2.add_edge("aggregate", END)

app2 = g2.compile()

result = app2.invoke({
    "request": "Create employee account, then grant VPN access, then send welcome email",
    "subtasks": [], "current_subtask": "",
    "results": [], "final_response": "", "audit": [],
})
print(f"\nResponse:\n{result['final_response'][:250]}")
print(f"Execution order: {[r['task'][:30] for r in result['results']]}")

print("\n" + "=" * 50)
print("Lab 05 Solution complete!")
print("- TODO 1: Parallel fan-out to HR + Tech + Facilities workers")
print("- TODO 2: Dependency-aware execution order")
