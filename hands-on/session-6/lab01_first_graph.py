"""
Lab 01: Your First LangGraph Workflow
=======================================
Goal: Build a simple graph with state, nodes, and edges to understand
      the core building blocks of LangGraph.

What you'll learn:
- How to define state with TypedDict
- How to create nodes (Python functions that update state)
- How to connect nodes with edges (START → node → END)
- How to compile and invoke a graph
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Your First LangGraph Workflow")
print("=" * 50)

# ============================================================
# Step 1: Define the state
# ============================================================
# State is a TypedDict — a dictionary with typed fields.
# Every node in the graph reads from and writes to this state.

class GreetingState(TypedDict):
    name: str
    greeting: str

print("\n--- Step 1: State Defined ---")
print("GreetingState has two fields: 'name' (str) and 'greeting' (str)")

# ============================================================
# Step 2: Create a node
# ============================================================
# A node is a Python function that:
#   - Takes the full state as input
#   - Returns a dict with the fields to update

def greet(state: GreetingState) -> dict:
    """Generate a greeting for the given name."""
    name = state["name"]
    return {"greeting": f"Hello, {name}! Welcome to UniGPS."}

print("\n--- Step 2: Node Created ---")
print("Function 'greet' takes state and returns a greeting update")

# ============================================================
# Step 3: Build the graph
# ============================================================
# 1. Create a StateGraph with the state type
# 2. Add nodes
# 3. Connect them with edges

graph = StateGraph(GreetingState)
graph.add_node("greet", greet)
graph.add_edge(START, "greet")  # START → greet
graph.add_edge("greet", END)    # greet → END

print("\n--- Step 3: Graph Built ---")
print("Graph: START → greet → END")

# ============================================================
# Step 4: Compile and run
# ============================================================
# compile() creates a runnable application from the graph.
# invoke() runs the graph with initial state values.

app = graph.compile()

result = app.invoke({"name": "Priya"})

print("\n--- Step 4: Graph Executed ---")
print(f"Input:  name = 'Priya'")
print(f"Output: {result}")
print(f"Greeting: {result['greeting']}")

# ============================================================
# Step 5: Try with different inputs
# ============================================================

print("\n--- Step 5: Different Inputs ---")
for name in ["Rahul", "Anita", "Vikram"]:
    result = app.invoke({"name": name})
    print(f"  {name} → {result['greeting']}")

# ============================================================
# Step 6: Two-node graph
# ============================================================
# Let's add a second node that modifies the greeting.

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
graph2.add_edge("greet", "add_dept")   # greet → add_dept
graph2.add_edge("add_dept", END)

app2 = graph2.compile()

print("\n--- Step 6: Two-Node Graph ---")
print("Graph: START → greet → add_dept → END")
result = app2.invoke({"name": "Priya", "department": "Engineering"})
print(f"Result: {result['greeting']}")

result = app2.invoke({"name": "Rahul", "department": "Sales"})
print(f"Result: {result['greeting']}")

# ============================================================
# TODO 1: Add a third node
# ============================================================
# Add a node called "add_office" that appends the office location
# to the greeting. Use a new state field "office" (str).
# The graph should be: START → greet → add_dept → add_office → END
# Test with: {"name": "Anita", "department": "QA", "office": "Pune"}

# class ExtendedState(TypedDict):
#     name: str
#     department: str
#     office: str
#     greeting: str
#
# def create_greeting_v2(state): return {"greeting": f"Welcome, {state['name']}!"}
# def add_department_v2(state): return {"greeting": f"{state['greeting']} Dept: {state['department']}."}
# def add_office(state): return {"greeting": f"{state['greeting']} Office: {state['office']}."}
#
# graph3 = StateGraph(ExtendedState)
# ... add nodes and edges ...
# app3 = graph3.compile()
# result = app3.invoke({"name": "Anita", "department": "QA", "office": "Pune"})
# print(f"Extended: {result['greeting']}")

# ============================================================
# TODO 2: Experiment with node order
# ============================================================
# What happens if you swap the edge order so add_dept runs
# BEFORE greet? Does the greeting still make sense?
# Try: START → add_dept → greet → END
# What does the output look like?

print("\n" + "=" * 50)
print("Lab 01 complete! Key takeaways:")
print("- State = TypedDict defining the data schema")
print("- Nodes = Python functions that read state and return updates")
print("- Edges = connections: START → nodes → END")
print("- compile() builds the graph, invoke() runs it")
print("- Nodes only update the fields they return")
