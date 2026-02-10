"""
Lab 02: Multi-Step Workflow
============================
Goal: Build a workflow with multiple processing steps to see how
      state flows through a chain of nodes.

What you'll learn:
- How state accumulates as it passes through nodes
- How each node can read fields set by previous nodes
- Building a realistic multi-step data processing pipeline
- Inspecting state at each stage
"""

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Multi-Step Workflow")
print("=" * 50)

# ============================================================
# Step 1: Define the state for a support ticket pipeline
# ============================================================

class TicketState(TypedDict):
    raw_input: str
    cleaned_input: str
    category: str
    priority: str
    response: str

# ============================================================
# Step 2: Create processing nodes
# ============================================================
# Each node handles one step of the pipeline.
# They read from state and return updates.

def clean_input(state: TicketState) -> dict:
    """Remove extra whitespace and lowercase the input."""
    cleaned = " ".join(state["raw_input"].split()).lower().strip()
    print(f"  [clean_input] '{state['raw_input']}' → '{cleaned}'")
    return {"cleaned_input": cleaned}

def classify(state: TicketState) -> dict:
    """Classify the ticket into a category."""
    text = state["cleaned_input"]
    if any(w in text for w in ["leave", "sick", "wfh", "vacation"]):
        category = "hr"
    elif any(w in text for w in ["deploy", "bug", "server", "database", "code"]):
        category = "tech"
    elif any(w in text for w in ["expense", "reimburse", "invoice", "bill"]):
        category = "finance"
    else:
        category = "general"
    print(f"  [classify] '{text}' → category: {category}")
    return {"category": category}

def assign_priority(state: TicketState) -> dict:
    """Assign priority based on keywords."""
    text = state["cleaned_input"]
    if any(w in text for w in ["urgent", "down", "critical", "blocked"]):
        priority = "HIGH"
    elif any(w in text for w in ["help", "issue", "problem", "error"]):
        priority = "MEDIUM"
    else:
        priority = "LOW"
    print(f"  [assign_priority] → {priority}")
    return {"priority": priority}

def generate_response(state: TicketState) -> dict:
    """Generate a response based on category and priority."""
    responses = {
        "hr": "Your HR request has been forwarded to the HR team.",
        "tech": "A tech support ticket has been created.",
        "finance": "Your finance query has been sent to the accounts team.",
        "general": "Your request has been logged. We'll get back to you shortly.",
    }
    base = responses.get(state["category"], responses["general"])
    response = f"[{state['priority']}] {base} (Category: {state['category']})"
    print(f"  [generate_response] → {response}")
    return {"response": response}

# ============================================================
# Step 3: Build the pipeline graph
# ============================================================

graph = StateGraph(TicketState)
graph.add_node("clean", clean_input)
graph.add_node("classify", classify)
graph.add_node("prioritize", assign_priority)
graph.add_node("respond", generate_response)

graph.add_edge(START, "clean")
graph.add_edge("clean", "classify")
graph.add_edge("classify", "prioritize")
graph.add_edge("prioritize", "respond")
graph.add_edge("respond", END)

app = graph.compile()
print("Graph: START → clean → classify → prioritize → respond → END\n")

# ============================================================
# Step 4: Run with test tickets
# ============================================================

test_tickets = [
    "I need to apply for   sick LEAVE   next week",
    "URGENT: production server is DOWN!",
    "How do I submit my   expense   report?",
    "Where is the office cafeteria?",
]

print("--- Processing Tickets ---")
for ticket in test_tickets:
    print(f"\nTicket: '{ticket}'")
    result = app.invoke({"raw_input": ticket})
    print(f"  Final state:")
    print(f"    category: {result['category']}")
    print(f"    priority: {result['priority']}")
    print(f"    response: {result['response']}")

# ============================================================
# Step 5: Inspect the full state
# ============================================================

print("\n--- Full State Inspection ---")
result = app.invoke({"raw_input": "Urgent help needed with database deployment"})
print("Complete state after all nodes:")
for key, value in result.items():
    print(f"  {key}: {value}")

# ============================================================
# TODO 1: Add a validation node
# ============================================================
# Add a node called "validate" that runs BEFORE "classify".
# It should check if the cleaned_input is at least 5 characters.
# If too short, set the response to "Input too short" and
# category to "invalid".
# Graph: START → clean → validate → classify → prioritize → respond → END

# def validate(state):
#     if len(state["cleaned_input"]) < 5:
#         return {"category": "invalid", "response": "Input too short. Please provide more details."}
#     return {}
#
# Test with: app.invoke({"raw_input": "Hi"})

# ============================================================
# TODO 2: Add a logging node at the end
# ============================================================
# Add a "log" node that runs after "respond" (before END).
# It should create a log entry string combining all fields:
# "[TIMESTAMP] [PRIORITY] [CATEGORY] response"
# Add a new state field "log_entry" (str) to store it.

# from datetime import datetime
# def log_ticket(state):
#     entry = f"[{datetime.now().isoformat()}] [{state['priority']}] [{state['category']}] {state['response']}"
#     print(f"  [log] {entry}")
#     return {"log_entry": entry}

print("\n" + "=" * 50)
print("Lab 02 complete! Key takeaways:")
print("- State accumulates as it passes through nodes")
print("- Each node can read fields set by earlier nodes")
print("- Nodes only update the fields they return")
print("- Multi-step pipelines = clean → classify → prioritize → respond")
print("- Print statements inside nodes help debug the flow")
