"""
Lab 02 Solution: Multi-Step Workflow
======================================
"""

from typing import TypedDict
from datetime import datetime
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Multi-Step Workflow (Solution)")
print("=" * 50)

# ============================================================
# Original pipeline with TODO solutions
# ============================================================

class TicketState(TypedDict):
    raw_input: str
    cleaned_input: str
    category: str
    priority: str
    response: str
    log_entry: str  # ← TODO 2: added field

def clean_input(state: TicketState) -> dict:
    cleaned = " ".join(state["raw_input"].split()).lower().strip()
    print(f"  [clean_input] '{state['raw_input']}' → '{cleaned}'")
    return {"cleaned_input": cleaned}

# ============================================================
# TODO 1 Solution: Validation node
# ============================================================

def validate(state: TicketState) -> dict:
    """Check if cleaned_input is at least 5 characters."""
    if len(state["cleaned_input"]) < 5:
        print(f"  [validate] TOO SHORT: '{state['cleaned_input']}'")
        return {
            "category": "invalid",
            "response": "Input too short. Please provide more details.",
        }
    print(f"  [validate] OK (length: {len(state['cleaned_input'])})")
    return {}

def classify(state: TicketState) -> dict:
    text = state["cleaned_input"]
    if state.get("category") == "invalid":
        print(f"  [classify] Skipping — already marked invalid")
        return {}
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
    if state.get("category") == "invalid":
        return {}  # Already has response from validate
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
# TODO 2 Solution: Logging node
# ============================================================

def log_ticket(state: TicketState) -> dict:
    """Create a log entry combining all fields."""
    entry = (
        f"[{datetime.now().isoformat()}] "
        f"[{state.get('priority', 'N/A')}] "
        f"[{state.get('category', 'N/A')}] "
        f"{state.get('response', 'No response')}"
    )
    print(f"  [log] {entry}")
    return {"log_entry": entry}

# ============================================================
# Build the complete pipeline
# ============================================================

graph = StateGraph(TicketState)
graph.add_node("clean", clean_input)
graph.add_node("validate", validate)     # ← TODO 1
graph.add_node("classify", classify)
graph.add_node("prioritize", assign_priority)
graph.add_node("respond", generate_response)
graph.add_node("log", log_ticket)        # ← TODO 2

graph.add_edge(START, "clean")
graph.add_edge("clean", "validate")      # ← TODO 1
graph.add_edge("validate", "classify")
graph.add_edge("classify", "prioritize")
graph.add_edge("prioritize", "respond")
graph.add_edge("respond", "log")         # ← TODO 2
graph.add_edge("log", END)

app = graph.compile()
print("Graph: START → clean → validate → classify → prioritize → respond → log → END\n")

# ============================================================
# Test with various inputs
# ============================================================

test_tickets = [
    "I need to apply for   sick LEAVE   next week",
    "URGENT: production server is DOWN!",
    "How do I submit my   expense   report?",
    "Hi",                                # ← Too short! Tests validate
    "Where is the office cafeteria?",
]

print("--- Processing Tickets ---")
for ticket in test_tickets:
    print(f"\nTicket: '{ticket}'")
    result = app.invoke({"raw_input": ticket})
    print(f"  Final state:")
    print(f"    category:  {result['category']}")
    print(f"    priority:  {result.get('priority', 'N/A')}")
    print(f"    response:  {result['response']}")
    print(f"    log_entry: {result.get('log_entry', 'N/A')[:60]}...")

print("\n" + "=" * 50)
print("Lab 02 Solution complete!")
print("- TODO 1: validate node rejects inputs < 5 characters")
print("- TODO 2: log node creates timestamped entries")
