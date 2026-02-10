"""
Lab 01 Solution: Your First LangGraph Workflow
================================================
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Your First LangGraph Workflow (Solution)")
print("=" * 50)

# Step 1-5: Same as lab (omitted for brevity — see lab file)

class GreetingState(TypedDict):
    name: str
    greeting: str

def greet(state: GreetingState) -> dict:
    name = state["name"]
    return {"greeting": f"Hello, {name}! Welcome to UniGPS."}

graph = StateGraph(GreetingState)
graph.add_node("greet", greet)
graph.add_edge(START, "greet")
graph.add_edge("greet", END)

app = graph.compile()

print("\n--- Single Node ---")
for name in ["Priya", "Rahul", "Anita", "Vikram"]:
    result = app.invoke({"name": name})
    print(f"  {name} → {result['greeting']}")

# Step 6: Two-node graph

class FormalState(TypedDict):
    name: str
    department: str
    greeting: str

def create_greeting(state: FormalState) -> dict:
    return {"greeting": f"Welcome, {state['name']}!"}

def add_department(state: FormalState) -> dict:
    return {"greeting": f"{state['greeting']} You are in the {state['department']} department."}

graph2 = StateGraph(FormalState)
graph2.add_node("greet", create_greeting)
graph2.add_node("add_dept", add_department)
graph2.add_edge(START, "greet")
graph2.add_edge("greet", "add_dept")
graph2.add_edge("add_dept", END)

app2 = graph2.compile()

print("\n--- Two-Node Graph ---")
result = app2.invoke({"name": "Priya", "department": "Engineering"})
print(f"Result: {result['greeting']}")

# ============================================================
# TODO 1 Solution: Add a third node
# ============================================================

class ExtendedState(TypedDict):
    name: str
    department: str
    office: str
    greeting: str

def create_greeting_v2(state: ExtendedState) -> dict:
    return {"greeting": f"Welcome, {state['name']}!"}

def add_department_v2(state: ExtendedState) -> dict:
    return {"greeting": f"{state['greeting']} Dept: {state['department']}."}

def add_office(state: ExtendedState) -> dict:
    return {"greeting": f"{state['greeting']} Office: {state['office']}."}

graph3 = StateGraph(ExtendedState)
graph3.add_node("greet", create_greeting_v2)
graph3.add_node("add_dept", add_department_v2)
graph3.add_node("add_office", add_office)

graph3.add_edge(START, "greet")
graph3.add_edge("greet", "add_dept")
graph3.add_edge("add_dept", "add_office")
graph3.add_edge("add_office", END)

app3 = graph3.compile()

print("\n--- TODO 1: Three-Node Graph ---")
print("Graph: START → greet → add_dept → add_office → END")
result = app3.invoke({"name": "Anita", "department": "QA", "office": "Pune"})
print(f"Result: {result['greeting']}")

result = app3.invoke({"name": "Vikram", "department": "DevOps", "office": "Hyderabad"})
print(f"Result: {result['greeting']}")

# ============================================================
# TODO 2 Solution: Experiment with node order
# ============================================================

print("\n--- TODO 2: Swapped Node Order ---")
print("Graph: START → add_dept → greet → END")

graph4 = StateGraph(FormalState)
graph4.add_node("greet", create_greeting)
graph4.add_node("add_dept", add_department)

# Swapped order!
graph4.add_edge(START, "add_dept")
graph4.add_edge("add_dept", "greet")
graph4.add_edge("greet", END)

app4 = graph4.compile()
result = app4.invoke({"name": "Priya", "department": "Engineering"})
print(f"Result: {result['greeting']}")
print("→ When add_dept runs first, state['greeting'] doesn't exist yet,")
print("  so it fails or produces unexpected results.")
print("  Node ORDER matters — earlier nodes set state for later nodes!")

print("\n" + "=" * 50)
print("Lab 01 Solution complete!")
