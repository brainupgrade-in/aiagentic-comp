"""
Lab 06 Solution: Advanced Routing
====================================
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
print("  Advanced Routing (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Nested routing within tech
# ============================================================

class NestedState(TypedDict):
    message: str
    category: str
    sub_category: str
    priority: str
    response: str
    audit: Annotated[list, add]

def llm_classify(state: NestedState) -> dict:
    prompt = (
        f"Classify this request into: hr, tech, finance, facilities\n"
        f"Also detect priority: urgent or normal\n"
        f"Request: {state['message']}\n"
        f"Reply:\nCATEGORY: ...\nPRIORITY: ..."
    )
    response = llm.invoke(prompt)
    text = response.content.lower()
    category = "general"
    priority = "normal"
    for line in text.split("\n"):
        if "category:" in line:
            cat = line.split(":")[-1].strip()
            if cat in ["hr", "tech", "finance", "facilities"]:
                category = cat
        elif "priority:" in line:
            pri = line.split(":")[-1].strip()
            if pri in ["urgent", "normal"]:
                priority = pri
    print(f"  [classify] {category}/{priority}")
    return {"category": category, "priority": priority, "audit": [f"Classified: {category}/{priority}"]}

def route_primary(state: NestedState) -> str:
    if state["priority"] == "urgent":
        return "urgent"
    return state["category"]

def handle_urgent(state: NestedState) -> dict:
    resp = llm.invoke(f"URGENT response for: {state['message']}")
    return {"response": f"[URGENT] {resp.content.strip()}", "audit": ["Urgent handler"]}

def handle_hr(state: NestedState) -> dict:
    resp = llm.invoke(f"HR response for: {state['message']}")
    return {"response": resp.content.strip(), "sub_category": "hr", "audit": ["HR handler"]}

def handle_finance(state: NestedState) -> dict:
    resp = llm.invoke(f"Finance response for: {state['message']}")
    return {"response": resp.content.strip(), "sub_category": "finance", "audit": ["Finance handler"]}

# Nested tech routing
def tech_sub_route(state: NestedState) -> str:
    msg = state["message"].lower()
    if any(w in msg for w in ["server", "database", "network", "down"]):
        return "infra"
    elif any(w in msg for w in ["code", "bug", "deploy", "api"]):
        return "dev"
    return "general_tech"

def handle_infra(state: NestedState) -> dict:
    resp = llm.invoke(f"Infrastructure support for: {state['message']}")
    return {"response": resp.content.strip(), "sub_category": "infrastructure", "audit": ["Infra handler"]}

def handle_dev(state: NestedState) -> dict:
    resp = llm.invoke(f"Development support for: {state['message']}")
    return {"response": resp.content.strip(), "sub_category": "development", "audit": ["Dev handler"]}

def handle_general_tech(state: NestedState) -> dict:
    return {"response": "Tech: General ticket created.", "sub_category": "general_tech", "audit": ["General tech"]}

def handle_general(state: NestedState) -> dict:
    return {"response": "Your request has been logged.", "sub_category": "general", "audit": ["General handler"]}

graph = StateGraph(NestedState)
graph.add_node("classify", llm_classify)
graph.add_node("urgent", handle_urgent)
graph.add_node("hr", handle_hr)
graph.add_node("finance", handle_finance)
graph.add_node("infra", handle_infra)
graph.add_node("dev", handle_dev)
graph.add_node("general_tech", handle_general_tech)
graph.add_node("general", handle_general)

graph.add_edge(START, "classify")
graph.add_conditional_edges("classify", route_primary, {
    "urgent": "urgent", "hr": "hr", "finance": "finance",
    "tech": "infra",  # Placeholder — nested routing below
    "facilities": "general", "general": "general",
})

# Override: tech goes to nested sub-routing
# We use a trick: route tech to a "tech_router" function
# Actually for nested, we route classify→tech to sub-route directly
# Let's rebuild with proper nesting:

graph2 = StateGraph(NestedState)
graph2.add_node("classify", llm_classify)
graph2.add_node("urgent", handle_urgent)
graph2.add_node("hr", handle_hr)
graph2.add_node("finance", handle_finance)
graph2.add_node("infra", handle_infra)
graph2.add_node("dev", handle_dev)
graph2.add_node("general_tech", handle_general_tech)
graph2.add_node("general", handle_general)

# Level 1 routing
def route_level1(state: NestedState) -> str:
    if state["priority"] == "urgent":
        return "urgent"
    if state["category"] == "tech":
        return "tech_sub"  # Go to nested routing
    return state["category"]

graph2.add_edge(START, "classify")
graph2.add_conditional_edges("classify", route_level1, {
    "urgent": "urgent",
    "hr": "hr",
    "finance": "finance",
    "tech_sub": "infra",  # We'll use a pass-through
    "general": "general",
    "facilities": "general",
})

# For proper nested routing, add a tech_triage node
def tech_triage(state: NestedState) -> dict:
    return {"audit": ["Tech triage"]}

graph3 = StateGraph(NestedState)
graph3.add_node("classify", llm_classify)
graph3.add_node("urgent", handle_urgent)
graph3.add_node("hr", handle_hr)
graph3.add_node("finance", handle_finance)
graph3.add_node("tech_triage", tech_triage)
graph3.add_node("infra", handle_infra)
graph3.add_node("dev", handle_dev)
graph3.add_node("general_tech", handle_general_tech)
graph3.add_node("general", handle_general)

graph3.add_edge(START, "classify")

def route_l1(state: NestedState) -> str:
    if state["priority"] == "urgent":
        return "urgent"
    mapping = {"hr": "hr", "tech": "tech_triage", "finance": "finance"}
    return mapping.get(state["category"], "general")

graph3.add_conditional_edges("classify", route_l1, {
    "urgent": "urgent", "hr": "hr", "tech_triage": "tech_triage",
    "finance": "finance", "general": "general",
})

# Level 2: nested tech routing
graph3.add_conditional_edges("tech_triage", tech_sub_route, {
    "infra": "infra", "dev": "dev", "general_tech": "general_tech",
})

for node in ["urgent", "hr", "finance", "infra", "dev", "general_tech", "general"]:
    graph3.add_edge(node, END)

app = graph3.compile()

print("\n--- TODO 1: Nested Tech Routing ---")
print("classify → [urgent | hr | finance | tech_triage→[infra|dev|general_tech] | general] → END\n")

tests = [
    "URGENT: Everything is on fire!",
    "I need to apply for leave",
    "The production database is running slow",
    "Help me deploy the new API to staging",
    "How do I submit my expense report?",
    "General tech question about our stack",
]

for msg in tests:
    result = app.invoke({"message": msg, "audit": []})
    print(f"  '{msg[:45]}' → [{result.get('sub_category', 'N/A')}] {result['response'][:40]}...")

# ============================================================
# TODO 2 Solution: LLM confidence routing
# ============================================================

print("\n--- TODO 2: Confidence Routing ---")

class ConfState(TypedDict):
    message: str
    category: str
    confidence: int
    response: str

def classify_with_confidence(state: ConfState) -> dict:
    prompt = (
        f"Classify: {state['message']}\n"
        f"Reply:\nCATEGORY: hr or tech or finance\nCONFIDENCE: 1-10"
    )
    response = llm.invoke(prompt)
    text = response.content.lower()
    category = "general"
    confidence = 5
    for line in text.split("\n"):
        if "category:" in line:
            cat = line.split(":")[-1].strip()
            if cat in ["hr", "tech", "finance"]:
                category = cat
        elif "confidence:" in line:
            try:
                confidence = int(line.split(":")[-1].strip().rstrip("."))
            except ValueError:
                confidence = 5
    print(f"  [classify] {category} (confidence: {confidence}/10)")
    return {"category": category, "confidence": confidence}

def clarify(state: ConfState) -> dict:
    return {"response": f"I'm not sure I understand. Could you provide more details about: '{state['message']}'?"}

def handle(state: ConfState) -> dict:
    return {"response": f"[{state['category'].upper()}] Your request has been routed."}

def route_with_confidence(state: ConfState) -> str:
    if state["confidence"] < 5:
        return "clarify"
    return "handle"

g = StateGraph(ConfState)
g.add_node("classify", classify_with_confidence)
g.add_node("clarify", clarify)
g.add_node("handle", handle)
g.add_edge(START, "classify")
g.add_conditional_edges("classify", route_with_confidence, {"clarify": "clarify", "handle": "handle"})
g.add_edge("clarify", END)
g.add_edge("handle", END)
app2 = g.compile()

for msg in ["I need sick leave", "asdfghjkl", "Something about the thing"]:
    result = app2.invoke({"message": msg})
    print(f"  '{msg}' → {result['response'][:60]}...")

print("\n" + "=" * 50)
print("Lab 06 Solution complete!")
print("- TODO 1: Nested tech routing (infra/dev/general_tech)")
print("- TODO 2: Low-confidence → clarify instead of wrong route")
