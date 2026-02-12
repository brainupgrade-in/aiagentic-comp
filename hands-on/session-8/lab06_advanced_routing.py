"""
Lab 06: Advanced Routing
==========================
Goal: Build sophisticated routing patterns including nested conditionals,
      LLM-powered routing, and priority-based routing.

What you'll learn:
- Nested conditional edges (multi-level decision trees)
- LLM-powered routing (let the LLM choose the path)
- Priority routing (check urgency before category)
- Combining multiple routing strategies

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
print("  Advanced Routing")
print("=" * 50)

# ============================================================
# Step 1: LLM-powered routing
# ============================================================
# Let the LLM decide which handler to route to.

class LLMRouteState(TypedDict):
    message: str
    category: str
    response: str
    audit: Annotated[list, add]

def llm_classify(state: LLMRouteState) -> dict:
    """Use LLM to classify the request."""
    prompt = (
        f"Classify this employee request into exactly one category.\n"
        f"Categories: hr, tech, finance, facilities\n"
        f"Request: {state['message']}\n"
        f"Reply with ONLY the category name."
    )
    response = llm.invoke(prompt)
    category = response.content.strip().lower()
    if category not in ["hr", "tech", "finance", "facilities"]:
        category = "general"
    print(f"  [LLM classify] '{state['message'][:40]}' → {category}")
    return {"category": category, "audit": [f"LLM classified: {category}"]}

def handle_hr(state: LLMRouteState) -> dict:
    resp = llm.invoke(f"As HR support, reply briefly to: {state['message']}")
    return {"response": resp.content.strip(), "audit": ["HR handler"]}

def handle_tech(state: LLMRouteState) -> dict:
    resp = llm.invoke(f"As tech support, reply briefly to: {state['message']}")
    return {"response": resp.content.strip(), "audit": ["Tech handler"]}

def handle_finance(state: LLMRouteState) -> dict:
    resp = llm.invoke(f"As finance support, reply briefly to: {state['message']}")
    return {"response": resp.content.strip(), "audit": ["Finance handler"]}

def handle_facilities(state: LLMRouteState) -> dict:
    resp = llm.invoke(f"As facilities support, reply briefly to: {state['message']}")
    return {"response": resp.content.strip(), "audit": ["Facilities handler"]}

def handle_general(state: LLMRouteState) -> dict:
    return {"response": "Your request has been logged. We'll route it to the right team.", "audit": ["General handler"]}

def route_by_category(state: LLMRouteState) -> str:
    mapping = {"hr": "hr", "tech": "tech", "finance": "finance", "facilities": "facilities"}
    return mapping.get(state["category"], "general")

graph1 = StateGraph(LLMRouteState)
graph1.add_node("classify", llm_classify)
graph1.add_node("hr", handle_hr)
graph1.add_node("tech", handle_tech)
graph1.add_node("finance", handle_finance)
graph1.add_node("facilities", handle_facilities)
graph1.add_node("general", handle_general)

graph1.add_edge(START, "classify")
graph1.add_conditional_edges("classify", route_by_category, {
    "hr": "hr", "tech": "tech", "finance": "finance",
    "facilities": "facilities", "general": "general",
})
for node in ["hr", "tech", "finance", "facilities", "general"]:
    graph1.add_edge(node, END)

app1 = graph1.compile()

print("\n--- Step 1: LLM-Powered Routing ---")
tests = [
    "I need to apply for maternity leave",
    "The AC in conference room B is not working",
    "Can you help me deploy the new API?",
    "How do I submit my travel reimbursement?",
]
for msg in tests:
    result = app1.invoke({"message": msg, "audit": []})
    print(f"\n  Message:  '{msg}'")
    print(f"  Category: {result['category']}")
    print(f"  Response: {result['response'][:60]}...")

# ============================================================
# Step 2: Priority routing (urgency before category)
# ============================================================

class PriorityState(TypedDict):
    message: str
    category: str
    priority: str
    response: str
    audit: Annotated[list, add]

def classify_and_prioritize(state: PriorityState) -> dict:
    """Classify category AND detect priority."""
    prompt = (
        f"Analyze this request:\n{state['message']}\n\n"
        f"Reply in exactly this format:\n"
        f"CATEGORY: hr or tech or finance\n"
        f"PRIORITY: urgent or normal"
    )
    response = llm.invoke(prompt)
    text = response.content.strip().lower()

    category = "general"
    priority = "normal"
    for line in text.split("\n"):
        if "category:" in line:
            cat = line.split(":")[-1].strip()
            if cat in ["hr", "tech", "finance"]:
                category = cat
        elif "priority:" in line:
            pri = line.split(":")[-1].strip()
            if pri in ["urgent", "normal"]:
                priority = pri

    print(f"  [classify] {category}/{priority}")
    return {"category": category, "priority": priority, "audit": [f"Classified: {category}/{priority}"]}

def handle_urgent(state: PriorityState) -> dict:
    """Urgent requests skip normal flow."""
    resp = llm.invoke(
        f"This is URGENT. Provide an immediate response to: {state['message']}\n"
        f"Category: {state['category']}. Be direct and action-oriented."
    )
    return {
        "response": f"[URGENT] {resp.content.strip()}",
        "audit": ["Urgent escalation handler"],
    }

def handle_normal_hr(state: PriorityState) -> dict:
    return {"response": "HR: Your request has been logged.", "audit": ["Normal HR handler"]}

def handle_normal_tech(state: PriorityState) -> dict:
    return {"response": "Tech: A support ticket has been created.", "audit": ["Normal Tech handler"]}

def handle_normal_finance(state: PriorityState) -> dict:
    return {"response": "Finance: Your query is being processed.", "audit": ["Normal Finance handler"]}

def priority_route(state: PriorityState) -> str:
    """Check priority FIRST, then category."""
    if state["priority"] == "urgent":
        return "urgent"
    return f"normal_{state['category']}"

graph2 = StateGraph(PriorityState)
graph2.add_node("classify", classify_and_prioritize)
graph2.add_node("urgent", handle_urgent)
graph2.add_node("normal_hr", handle_normal_hr)
graph2.add_node("normal_tech", handle_normal_tech)
graph2.add_node("normal_finance", handle_normal_finance)

graph2.add_edge(START, "classify")
graph2.add_conditional_edges("classify", priority_route, {
    "urgent": "urgent",
    "normal_hr": "normal_hr",
    "normal_tech": "normal_tech",
    "normal_finance": "normal_finance",
    "normal_general": "normal_hr",  # Fallback
})
for node in ["urgent", "normal_hr", "normal_tech", "normal_finance"]:
    graph2.add_edge(node, END)

app2 = graph2.compile()

print("\n\n--- Step 2: Priority Routing ---")
print("Graph: classify → [urgent | normal_hr | normal_tech | normal_finance] → END\n")

for msg in [
    "URGENT: Production database is corrupted!",
    "I'd like to apply for annual leave next month",
    "How do I submit my expense report?",
]:
    result = app2.invoke({"message": msg, "audit": []})
    print(f"  '{msg[:45]}' → [{result['priority']}] {result['response'][:50]}...")

# ============================================================
# TODO 1: Add nested routing within tech
# ============================================================
# After routing to "normal_tech", add a second level of routing:
#   - "infrastructure" (server, database, network)
#   - "development" (code, bug, deploy, api)
#   - "general_tech" (everything else)
# Each sub-handler generates a specialized response.

# def tech_sub_route(state):
#     msg = state["message"].lower()
#     if any(w in msg for w in ["server", "database", "network"]):
#         return "infra"
#     elif any(w in msg for w in ["code", "bug", "deploy", "api"]):
#         return "dev"
#     return "general_tech"

# ============================================================
# TODO 2: LLM confidence routing
# ============================================================
# Modify the LLM classifier to also return a confidence score (1-10).
# If confidence < 5, route to a "clarify" node that asks the user
# for more details (instead of guessing the wrong category).

# Prompt: "CATEGORY: hr\nCONFIDENCE: 8"
# def route_with_confidence(state):
#     if state["confidence"] < 5:
#         return "clarify"
#     return state["category"]

print("\n\n" + "=" * 50)
print("Lab 06 complete! Key takeaways:")
print("- LLM routing: let the LLM classify and choose the path")
print("- Priority routing: check urgency BEFORE category")
print("- Nested routing: chain conditional edges for sub-categories")
print("- Always include fallback routes for unexpected classifications")
