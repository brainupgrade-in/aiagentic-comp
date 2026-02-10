"""
Lab 03: Peer-to-Peer Collaboration
=====================================
Goal: Build a multi-agent system where agents collaborate directly
      via shared state, taking turns to build on each other's work.

What you'll learn:
- Shared state message board pattern
- Turn-based agent execution
- Iterative refinement with cycles
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Peer-to-Peer Collaboration")
print("=" * 50)

# ============================================================
# Step 1: Two agents taking turns (researcher + writer)
# ============================================================

class CollabState(TypedDict):
    topic: str
    messages: Annotated[list, add]  # shared message board
    current_turn: str
    turns_left: int
    final_output: str

def researcher(state: CollabState) -> dict:
    """Researcher adds facts to the shared message board."""
    turn = (state.get("turns_left", 4) - state["turns_left"]) // 2 + 1
    # Simulate research findings
    findings = {
        1: f"[Research] Key facts about {state['topic']}: Founded in 2015, 500+ employees, HQ in Pune.",
        2: f"[Research] Additional data: Revenue grew 40% YoY, expanded to 3 cities, won Best Workplace award.",
    }
    msg = findings.get(turn, f"[Research] Further analysis on {state['topic']} completed.")
    print(f"  [researcher] Turn {turn}: {msg[:60]}...")
    return {
        "messages": [msg],
        "current_turn": "writer",
        "turns_left": state["turns_left"] - 1,
    }

def writer(state: CollabState) -> dict:
    """Writer reads research and produces content."""
    # Read all previous research messages
    research = [m for m in state["messages"] if m.startswith("[Research]")]
    turn = len([m for m in state["messages"] if m.startswith("[Writer]")]) + 1

    if turn == 1:
        content = f"[Writer] Draft: {state['topic']} is a leading company. " + research[-1].replace("[Research] ", "")
    else:
        content = f"[Writer] Revised: Enhanced with new data — " + research[-1].replace("[Research] ", "")
    print(f"  [writer] Turn {turn}: {content[:60]}...")
    return {
        "messages": [content],
        "current_turn": "researcher",
        "turns_left": state["turns_left"] - 1,
    }

def route_turn(state: CollabState) -> str:
    if state["turns_left"] <= 0:
        return "finish"
    return state["current_turn"]

def finish(state: CollabState) -> dict:
    """Combine the final output."""
    writer_msgs = [m for m in state["messages"] if m.startswith("[Writer]")]
    final = writer_msgs[-1] if writer_msgs else "No output produced."
    return {"final_output": final}

graph = StateGraph(CollabState)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
graph.add_node("finish", finish)

graph.add_conditional_edges(START, route_turn, {
    "researcher": "researcher",
    "writer": "writer",
    "finish": "finish",
})
graph.add_conditional_edges("researcher", route_turn, {
    "writer": "writer",
    "finish": "finish",
    "researcher": "researcher",
})
graph.add_conditional_edges("writer", route_turn, {
    "researcher": "researcher",
    "finish": "finish",
    "writer": "writer",
})
graph.add_edge("finish", END)

app = graph.compile()

print("\nGraph: [researcher ↔ writer] (turn-based) → finish → END\n")

result = app.invoke({
    "topic": "UniGPS Solutions",
    "messages": [],
    "current_turn": "researcher",
    "turns_left": 4,
    "final_output": "",
})

print(f"\nAll messages ({len(result['messages'])}):")
for msg in result["messages"]:
    print(f"  {msg[:70]}...")
print(f"\nFinal output: {result['final_output'][:80]}...")

# ============================================================
# Step 2: Three agents — researcher, writer, reviewer
# ============================================================

print("\n\n--- Step 2: Three-Agent Collaboration ---\n")

class ReviewCollabState(TypedDict):
    topic: str
    messages: Annotated[list, add]
    current_turn: str
    rounds_left: int
    final_output: str
    score: int

def research_agent(state: ReviewCollabState) -> dict:
    """Gather facts."""
    msg = f"[Researcher] Facts about {state['topic']}: leading fleet management company, 200+ clients across India."
    print(f"  [researcher] {msg[:60]}...")
    return {"messages": [msg], "current_turn": "writer"}

def write_agent(state: ReviewCollabState) -> dict:
    """Draft content from research."""
    research = [m for m in state["messages"] if m.startswith("[Researcher]")]
    msg = f"[Writer] Draft: {state['topic']} serves 200+ clients with innovative fleet management solutions."
    if state["rounds_left"] < 2:
        msg = f"[Writer] Revised: {state['topic']} is India's leading fleet management platform serving 200+ enterprises."
    print(f"  [writer] {msg[:60]}...")
    return {"messages": [msg], "current_turn": "reviewer"}

def review_agent(state: ReviewCollabState) -> dict:
    """Review and score the latest draft."""
    writer_msgs = [m for m in state["messages"] if m.startswith("[Writer]")]
    latest = writer_msgs[-1] if writer_msgs else ""
    # Simple scoring: longer is better
    score = min(10, len(latest) // 10)
    feedback = f"[Reviewer] Score: {score}/10. "
    if score < 7:
        feedback += "Needs more detail and data points."
    else:
        feedback += "Good quality, ready to publish."
    print(f"  [reviewer] Score: {score}/10")
    return {
        "messages": [feedback],
        "current_turn": "researcher",
        "rounds_left": state["rounds_left"] - 1,
        "score": score,
    }

def route_review(state: ReviewCollabState) -> str:
    if state["rounds_left"] <= 0 or state.get("score", 0) >= 7:
        return "compile"
    return state["current_turn"]

def compile_output(state: ReviewCollabState) -> dict:
    writer_msgs = [m for m in state["messages"] if m.startswith("[Writer]")]
    return {"final_output": writer_msgs[-1] if writer_msgs else "No output."}

g2 = StateGraph(ReviewCollabState)
g2.add_node("researcher", research_agent)
g2.add_node("writer", write_agent)
g2.add_node("reviewer", review_agent)
g2.add_node("compile", compile_output)

g2.add_edge(START, "researcher")
g2.add_edge("researcher", "writer")
g2.add_edge("writer", "reviewer")
g2.add_conditional_edges("reviewer", route_review, {
    "researcher": "researcher",
    "compile": "compile",
})
g2.add_edge("compile", END)

app2 = g2.compile()

result2 = app2.invoke({
    "topic": "UniGPS Fleet Management",
    "messages": [],
    "current_turn": "researcher",
    "rounds_left": 3,
    "final_output": "",
    "score": 0,
})

print(f"\nFinal: {result2['final_output'][:80]}...")
print(f"Score: {result2['score']}/10")
print(f"Messages exchanged: {len(result2['messages'])}")

# ============================================================
# TODO 1: Add an editor agent
# ============================================================
# Add a 4th agent "editor" that runs AFTER the reviewer but BEFORE
# the next research round. The editor polishes the writer's draft.
#
# Flow: researcher → writer → reviewer → editor → [researcher | compile]
#
# def editor_agent(state: ReviewCollabState) -> dict:
#     """Edit the latest draft for grammar and clarity."""
#     writer_msgs = [m for m in state["messages"] if m.startswith("[Writer]")]
#     latest = writer_msgs[-1] if writer_msgs else ""
#     # Simple edit: capitalize and add period
#     edited = f"[Editor] Polished: {latest.replace('[Writer] ', '').strip()}"
#     print(f"  [editor] {edited[:60]}...")
#     return {"messages": [edited], "current_turn": "researcher"}
#
# Add the node and update edges so reviewer → editor → route


# ============================================================
# TODO 2: Add message limit
# ============================================================
# Prevent infinite collaboration by adding a max_messages limit.
# If the total messages exceed the limit, force a compile regardless
# of score or rounds_left.
#
# Hint: Add max_messages to state and check in route_review.
#
# class LimitedCollabState(TypedDict):
#     topic: str
#     messages: Annotated[list, add]
#     current_turn: str
#     rounds_left: int
#     max_messages: int              # ← new
#     final_output: str
#     score: int
#
# def route_with_limit(state: LimitedCollabState) -> str:
#     if len(state["messages"]) >= state["max_messages"]:
#         print(f"  [route] Message limit ({state['max_messages']}) reached!")
#         return "compile"
#     if state["rounds_left"] <= 0 or state.get("score", 0) >= 7:
#         return "compile"
#     return state["current_turn"]
#
# Test with max_messages=6 and rounds_left=10
# Expected: stops at message limit, not round limit


print("\n" + "=" * 50)
print("Lab 03 complete!")
print("Patterns: shared state, turn-based agents, iterative refinement")
