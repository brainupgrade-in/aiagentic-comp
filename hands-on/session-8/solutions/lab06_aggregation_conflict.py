"""
Lab 06 Solution: Result Aggregation & Conflict Resolution
============================================================
"""

import os
from typing import TypedDict, Annotated
from operator import add
from collections import Counter
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

print("=" * 50)
print("  Result Aggregation & Conflict Resolution (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Arbitrator agent
# ============================================================

class ArbitratedVoteState(TypedDict):
    request: str
    votes: Annotated[list, add]
    winner: str
    confidence: str
    has_conflict: bool
    final_category: str
    audit: Annotated[list, add]

def classifier_a(state: ArbitratedVoteState) -> dict:
    response = llm.invoke(
        f"Classify as: hr, tech, finance, general. Reply one word.\n"
        f"Request: {state['request']}"
    )
    vote = response.content.strip().lower()
    if vote not in ["hr", "tech", "finance", "general"]:
        vote = "general"
    print(f"  [classifier_a] {vote}")
    return {"votes": [vote], "audit": [f"A: {vote}"]}

def classifier_b(state: ArbitratedVoteState) -> dict:
    response = llm.invoke(
        f"You are a support desk router. Classify: hr, tech, finance, general.\n"
        f"Employee says: {state['request']}\nReply one word."
    )
    vote = response.content.strip().lower()
    if vote not in ["hr", "tech", "finance", "general"]:
        vote = "general"
    print(f"  [classifier_b] {vote}")
    return {"votes": [vote], "audit": [f"B: {vote}"]}

def classifier_c(state: ArbitratedVoteState) -> dict:
    response = llm.invoke(
        f"Categorize: {state['request']}\nOptions: hr, tech, finance, general\nOne word."
    )
    vote = response.content.strip().lower()
    if vote not in ["hr", "tech", "finance", "general"]:
        vote = "general"
    print(f"  [classifier_c] {vote}")
    return {"votes": [vote], "audit": [f"C: {vote}"]}

def tally_and_detect(state: ArbitratedVoteState) -> dict:
    counts = Counter(state["votes"])
    winner, top_count = counts.most_common(1)[0]
    has_conflict = top_count < len(state["votes"])
    conf = "unanimous" if not has_conflict else f"split ({dict(counts)})"
    print(f"  [tally] {dict(counts)} → {winner} ({conf}), conflict={has_conflict}")
    return {
        "winner": winner,
        "confidence": conf,
        "has_conflict": has_conflict,
        "final_category": winner,
        "audit": [f"Tally: {winner} ({conf}), conflict={has_conflict}"],
    }

def arbitrator(state: ArbitratedVoteState) -> dict:
    """Dedicated agent resolves the conflict."""
    prompt = (
        f"Three classifiers disagreed on this request.\n"
        f"Request: {state['request']}\n"
        f"Votes: {state['votes']}\n\n"
        f"Analyze carefully and pick the correct category: hr, tech, finance, general\n"
        f"Reply:\nCATEGORY: ...\nREASON: ..."
    )
    response = llm.invoke(prompt)
    text = response.content.lower()
    category = state["winner"]  # default to majority
    reason = ""
    for line in text.split("\n"):
        if "category:" in line:
            cat = line.split(":")[-1].strip()
            if cat in ["hr", "tech", "finance", "general"]:
                category = cat
        elif "reason:" in line:
            reason = line.split(":", 1)[-1].strip()
    print(f"  [arbitrator] Decision: {category} ({reason[:40]})")
    return {
        "final_category": category,
        "audit": [f"Arbitrator: {category} ({reason[:40]})"],
    }

def route_conflict(state: ArbitratedVoteState) -> str:
    return "arbitrator" if state["has_conflict"] else "done"

def done_node(state: ArbitratedVoteState) -> dict:
    return {"audit": ["Final category set"]}

graph = StateGraph(ArbitratedVoteState)
graph.add_node("classifier_a", classifier_a)
graph.add_node("classifier_b", classifier_b)
graph.add_node("classifier_c", classifier_c)
graph.add_node("tally", tally_and_detect)
graph.add_node("arbitrator", arbitrator)
graph.add_node("done", done_node)

graph.add_edge(START, "classifier_a")
graph.add_edge(START, "classifier_b")
graph.add_edge(START, "classifier_c")
graph.add_edge("classifier_a", "tally")
graph.add_edge("classifier_b", "tally")
graph.add_edge("classifier_c", "tally")
graph.add_conditional_edges("tally", route_conflict, {
    "arbitrator": "arbitrator",
    "done": "done",
})
graph.add_edge("arbitrator", END)
graph.add_edge("done", END)

app = graph.compile()

print("\n--- TODO 1: Arbitrator Agent ---")
print("Graph: [A+B+C] → tally → [arbitrator | done] → END\n")

tests = [
    "My laptop is not booting",
    "I want to apply for leave",
    "Something about the office thing and computers",
]

for msg in tests:
    result = app.invoke({
        "request": msg, "votes": [], "winner": "",
        "confidence": "", "has_conflict": False,
        "final_category": "", "audit": [],
    })
    print(f"  '{msg}'")
    print(f"  → Votes: {result['votes']}, Final: {result['final_category']}, Conflict: {result['has_conflict']}")
    print()

# ============================================================
# TODO 2 Solution: Weighted voting
# ============================================================

print("\n--- TODO 2: Weighted Voting ---\n")

class WeightedVoteState(TypedDict):
    request: str
    votes: Annotated[list, add]   # [{"classifier": "a", "vote": "hr"}, ...]
    winner: str
    scores: str
    audit: Annotated[list, add]

def w_classifier_a(state: WeightedVoteState) -> dict:
    """HR expert classifier."""
    response = llm.invoke(
        f"You are an HR expert. Classify: hr, tech, finance, general.\n{state['request']}\nOne word."
    )
    vote = response.content.strip().lower()
    if vote not in ["hr", "tech", "finance", "general"]:
        vote = "general"
    return {"votes": [{"classifier": "a", "vote": vote}], "audit": [f"A(HR expert): {vote}"]}

def w_classifier_b(state: WeightedVoteState) -> dict:
    """Tech expert classifier."""
    response = llm.invoke(
        f"You are a tech support expert. Classify: hr, tech, finance, general.\n{state['request']}\nOne word."
    )
    vote = response.content.strip().lower()
    if vote not in ["hr", "tech", "finance", "general"]:
        vote = "general"
    return {"votes": [{"classifier": "b", "vote": vote}], "audit": [f"B(Tech expert): {vote}"]}

def w_classifier_c(state: WeightedVoteState) -> dict:
    """General classifier."""
    response = llm.invoke(
        f"Classify: hr, tech, finance, general.\n{state['request']}\nOne word."
    )
    vote = response.content.strip().lower()
    if vote not in ["hr", "tech", "finance", "general"]:
        vote = "general"
    return {"votes": [{"classifier": "c", "vote": vote}], "audit": [f"C(General): {vote}"]}

def weighted_tally(state: WeightedVoteState) -> dict:
    """Tally with domain expertise weights."""
    weights = {
        "a": {"hr": 2, "tech": 1, "finance": 1, "general": 1},  # HR expert
        "b": {"hr": 1, "tech": 2, "finance": 1, "general": 1},  # Tech expert
        "c": {"hr": 1, "tech": 1, "finance": 1, "general": 1},  # General
    }
    scores = {"hr": 0, "tech": 0, "finance": 0, "general": 0}
    for v in state["votes"]:
        w = weights[v["classifier"]][v["vote"]]
        scores[v["vote"]] += w
    winner = max(scores, key=scores.get)
    print(f"  [weighted_tally] Scores: {scores} → {winner}")
    return {
        "winner": winner,
        "scores": str(scores),
        "audit": [f"Weighted: {scores} → {winner}"],
    }

g2 = StateGraph(WeightedVoteState)
g2.add_node("classifier_a", w_classifier_a)
g2.add_node("classifier_b", w_classifier_b)
g2.add_node("classifier_c", w_classifier_c)
g2.add_node("tally", weighted_tally)

g2.add_edge(START, "classifier_a")
g2.add_edge(START, "classifier_b")
g2.add_edge(START, "classifier_c")
g2.add_edge("classifier_a", "tally")
g2.add_edge("classifier_b", "tally")
g2.add_edge("classifier_c", "tally")
g2.add_edge("tally", END)

app2 = g2.compile()

for msg in ["I need help with my leave balance", "My VPN keeps disconnecting"]:
    result = app2.invoke({"request": msg, "votes": [], "winner": "", "scores": "", "audit": []})
    votes = [(v["classifier"], v["vote"]) for v in result["votes"]]
    print(f"  '{msg}'")
    print(f"  Votes: {votes}")
    print(f"  Scores: {result['scores']}")
    print(f"  Winner: {result['winner']}")
    print()

print("\n" + "=" * 50)
print("Lab 06 Solution complete!")
print("- TODO 1: Arbitrator agent resolves split votes with LLM reasoning")
print("- TODO 2: Weighted voting gives domain experts 2x weight for their domain")
