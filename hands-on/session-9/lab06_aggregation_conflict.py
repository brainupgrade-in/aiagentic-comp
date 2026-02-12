"""
Lab 06: Result Aggregation & Conflict Resolution
===================================================
Goal: Build systems that merge outputs from multiple agents and
      handle disagreements between agents.

What you'll learn:
- LLM synthesis aggregation
- Voting / majority consensus
- Arbitrator agent for conflict resolution

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
print("  Result Aggregation & Conflict Resolution")
print("=" * 50)

# ============================================================
# Step 1: LLM Synthesis — merge 3 agent outputs
# ============================================================

class AggState(TypedDict):
    request: str
    agent_outputs: Annotated[list, add]
    synthesized: str
    audit: Annotated[list, add]

def technical_view(state: AggState) -> dict:
    """Technical agent perspective."""
    response = llm.invoke(
        f"You are a technical analyst at UniGPS.\n"
        f"Analyze from a TECHNICAL perspective in 2 sentences:\n{state['request']}"
    )
    output = response.content.strip()
    print(f"  [technical] {output[:60]}...")
    return {"agent_outputs": [{"agent": "technical", "output": output}],
            "audit": ["Technical analysis done"]}

def business_view(state: AggState) -> dict:
    """Business agent perspective."""
    response = llm.invoke(
        f"You are a business analyst at UniGPS.\n"
        f"Analyze from a BUSINESS perspective in 2 sentences:\n{state['request']}"
    )
    output = response.content.strip()
    print(f"  [business] {output[:60]}...")
    return {"agent_outputs": [{"agent": "business", "output": output}],
            "audit": ["Business analysis done"]}

def user_experience_view(state: AggState) -> dict:
    """UX agent perspective."""
    response = llm.invoke(
        f"You are a UX specialist at UniGPS.\n"
        f"Analyze from a USER EXPERIENCE perspective in 2 sentences:\n{state['request']}"
    )
    output = response.content.strip()
    print(f"  [UX] {output[:60]}...")
    return {"agent_outputs": [{"agent": "ux", "output": output}],
            "audit": ["UX analysis done"]}

def synthesize(state: AggState) -> dict:
    """LLM merges all agent outputs into one coherent response."""
    all_outputs = "\n".join(
        f"[{o['agent'].upper()}]: {o['output']}" for o in state["agent_outputs"]
    )
    prompt = (
        f"Synthesize these 3 expert perspectives into one unified response.\n"
        f"Keep it to 3-4 sentences.\n\n{all_outputs}"
    )
    response = llm.invoke(prompt)
    print(f"  [synthesize] Combined {len(state['agent_outputs'])} outputs")
    return {
        "synthesized": response.content.strip(),
        "audit": ["Synthesized all outputs"],
    }

# Build with parallel fan-out
graph = StateGraph(AggState)
graph.add_node("technical", technical_view)
graph.add_node("business", business_view)
graph.add_node("ux", user_experience_view)
graph.add_node("synthesize", synthesize)

# Fan-out: all 3 agents run "in parallel" (collected by reducer)
graph.add_edge(START, "technical")
graph.add_edge(START, "business")
graph.add_edge(START, "ux")
# Converge to synthesis
graph.add_edge("technical", "synthesize")
graph.add_edge("business", "synthesize")
graph.add_edge("ux", "synthesize")
graph.add_edge("synthesize", END)

app = graph.compile()

print("\nGraph: [technical + business + UX] → synthesize → END\n")

result = app.invoke({
    "request": "Should UniGPS build a mobile app for fleet managers?",
    "agent_outputs": [],
    "synthesized": "",
    "audit": [],
})

print(f"\nIndividual outputs:")
for o in result["agent_outputs"]:
    print(f"  [{o['agent'].upper()}]: {o['output'][:70]}...")
print(f"\nSynthesized: {result['synthesized'][:150]}...")

# ============================================================
# Step 2: Voting — 3 classifiers, majority wins
# ============================================================

print("\n\n--- Step 2: Voting / Majority Consensus ---\n")

class VoteState(TypedDict):
    request: str
    votes: Annotated[list, add]
    winner: str
    confidence: str
    audit: Annotated[list, add]

def classifier_a(state: VoteState) -> dict:
    response = llm.invoke(
        f"Classify as: hr, tech, finance, general. Reply with just one word.\n"
        f"Request: {state['request']}"
    )
    vote = response.content.strip().lower()
    if vote not in ["hr", "tech", "finance", "general"]:
        vote = "general"
    print(f"  [classifier_a] Votes: {vote}")
    return {"votes": [vote], "audit": [f"Classifier A: {vote}"]}

def classifier_b(state: VoteState) -> dict:
    response = llm.invoke(
        f"You are a support desk router. Classify: hr, tech, finance, general.\n"
        f"Employee says: {state['request']}\nReply one word."
    )
    vote = response.content.strip().lower()
    if vote not in ["hr", "tech", "finance", "general"]:
        vote = "general"
    print(f"  [classifier_b] Votes: {vote}")
    return {"votes": [vote], "audit": [f"Classifier B: {vote}"]}

def classifier_c(state: VoteState) -> dict:
    response = llm.invoke(
        f"Categorize this employee request: {state['request']}\n"
        f"Options: hr, tech, finance, general\nOne word answer."
    )
    vote = response.content.strip().lower()
    if vote not in ["hr", "tech", "finance", "general"]:
        vote = "general"
    print(f"  [classifier_c] Votes: {vote}")
    return {"votes": [vote], "audit": [f"Classifier C: {vote}"]}

def tally_votes(state: VoteState) -> dict:
    """Count votes and pick the winner."""
    from collections import Counter
    counts = Counter(state["votes"])
    winner, count = counts.most_common(1)[0]
    total = len(state["votes"])
    conf = "unanimous" if count == total else f"majority ({count}/{total})"
    print(f"  [tally] Votes: {dict(counts)} → winner: {winner} ({conf})")
    return {
        "winner": winner,
        "confidence": conf,
        "audit": [f"Vote result: {winner} ({conf})"],
    }

g2 = StateGraph(VoteState)
g2.add_node("classifier_a", classifier_a)
g2.add_node("classifier_b", classifier_b)
g2.add_node("classifier_c", classifier_c)
g2.add_node("tally", tally_votes)

# Parallel voting
g2.add_edge(START, "classifier_a")
g2.add_edge(START, "classifier_b")
g2.add_edge(START, "classifier_c")
g2.add_edge("classifier_a", "tally")
g2.add_edge("classifier_b", "tally")
g2.add_edge("classifier_c", "tally")
g2.add_edge("tally", END)

app2 = g2.compile()

test_msgs = [
    "My laptop is not booting up",
    "I want to apply for casual leave",
    "asdfghjkl random gibberish",
]

for msg in test_msgs:
    result = app2.invoke({"request": msg, "votes": [], "winner": "", "confidence": "", "audit": []})
    print(f"  '{msg}' → {result['winner']} ({result['confidence']})\n")

# ============================================================
# TODO 1: Arbitrator agent for conflict resolution
# ============================================================
# When the 3 classifiers DON'T agree unanimously, send the
# conflicting votes to an arbitrator agent that makes the final call.
#
# Hint: Add a conflict detection node after tally.
#
# class ArbitratedVoteState(TypedDict):
#     request: str
#     votes: Annotated[list, add]
#     winner: str
#     confidence: str
#     has_conflict: bool
#     final_category: str
#     audit: Annotated[list, add]
#
# def detect_conflict(state: ArbitratedVoteState) -> dict:
#     from collections import Counter
#     counts = Counter(state["votes"])
#     _, top_count = counts.most_common(1)[0]
#     has_conflict = top_count < len(state["votes"])
#     return {"has_conflict": has_conflict}
#
# def arbitrator(state: ArbitratedVoteState) -> dict:
#     prompt = (
#         f"Three classifiers disagreed on this request.\n"
#         f"Request: {state['request']}\n"
#         f"Votes: {state['votes']}\n"
#         f"Analyze carefully and pick the correct category: hr, tech, finance, general"
#     )
#     response = llm.invoke(prompt)
#     ...
#
# def route_conflict(state: ArbitratedVoteState) -> str:
#     return "arbitrator" if state["has_conflict"] else "done"
#
# Test with an ambiguous request that might cause disagreement


# ============================================================
# TODO 2: Weighted voting
# ============================================================
# Assign different weights to each classifier based on their
# domain expertise. A domain-expert classifier's vote counts more.
#
# Hint:
#   - Classifier A (HR expert): weight 2 for HR votes, 1 otherwise
#   - Classifier B (Tech expert): weight 2 for tech votes, 1 otherwise
#   - Classifier C (General): weight 1 always
#
# def weighted_tally(state) -> dict:
#     weights = {
#         "a": {"hr": 2, "tech": 1, "finance": 1, "general": 1},
#         "b": {"hr": 1, "tech": 2, "finance": 1, "general": 1},
#         "c": {"hr": 1, "tech": 1, "finance": 1, "general": 1},
#     }
#     # Calculate weighted scores per category
#     scores = {"hr": 0, "tech": 0, "finance": 0, "general": 0}
#     for i, (name, vote) in enumerate(zip(["a", "b", "c"], state["votes"])):
#         scores[vote] += weights[name][vote]
#     winner = max(scores, key=scores.get)
#     ...


print("\n" + "=" * 50)
print("Lab 06 complete!")
print("Patterns: LLM synthesis, parallel fan-out, voting, aggregation")
