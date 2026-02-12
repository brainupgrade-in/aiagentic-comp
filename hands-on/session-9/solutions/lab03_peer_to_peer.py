"""
Lab 03 Solution: Peer-to-Peer Collaboration
==============================================
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Peer-to-Peer Collaboration (Solution)")
print("=" * 50)

# ============================================================
# TODO 1 Solution: Add an editor agent
# ============================================================

class ReviewCollabState(TypedDict):
    topic: str
    messages: Annotated[list, add]
    current_turn: str
    rounds_left: int
    final_output: str
    score: int

def research_agent(state: ReviewCollabState) -> dict:
    msg = f"[Researcher] Facts about {state['topic']}: leading fleet company, 200+ clients, HQ in Pune, 500 employees."
    print(f"  [researcher] {msg[:60]}...")
    return {"messages": [msg], "current_turn": "writer"}

def write_agent(state: ReviewCollabState) -> dict:
    research = [m for m in state["messages"] if m.startswith("[Researcher]")]
    edited = [m for m in state["messages"] if m.startswith("[Editor]")]
    base = edited[-1] if edited else research[-1] if research else ""
    content = base.split("] ", 1)[-1] if "] " in base else base

    if state["rounds_left"] > 1:
        msg = f"[Writer] Draft: {state['topic']} — {content[:80]}"
    else:
        msg = f"[Writer] Final: {state['topic']} is a premier fleet management platform. {content[:60]}"
    print(f"  [writer] {msg[:60]}...")
    return {"messages": [msg], "current_turn": "reviewer"}

def review_agent(state: ReviewCollabState) -> dict:
    writer_msgs = [m for m in state["messages"] if m.startswith("[Writer]")]
    latest = writer_msgs[-1] if writer_msgs else ""
    score = min(10, len(latest) // 10)
    feedback = f"[Reviewer] Score: {score}/10. "
    if score < 7:
        feedback += "Add more specifics and data points."
    else:
        feedback += "Good quality — publish ready."
    print(f"  [reviewer] Score: {score}/10")
    return {"messages": [feedback], "current_turn": "editor",
            "rounds_left": state["rounds_left"] - 1, "score": score}

def editor_agent(state: ReviewCollabState) -> dict:
    """Editor polishes the latest writer draft."""
    writer_msgs = [m for m in state["messages"] if m.startswith("[Writer]")]
    latest = writer_msgs[-1] if writer_msgs else ""
    content = latest.replace("[Writer] ", "").strip()
    # Simple edit: clean up and enhance
    edited = f"[Editor] Polished: {content}. Trusted by enterprises across India."
    print(f"  [editor] {edited[:60]}...")
    return {"messages": [edited], "current_turn": "researcher"}

def route_after_review(state: ReviewCollabState) -> str:
    if state["rounds_left"] <= 0 or state.get("score", 0) >= 7:
        return "compile"
    return "editor"

def compile_output(state: ReviewCollabState) -> dict:
    # Prefer editor output, fall back to writer
    edited = [m for m in state["messages"] if m.startswith("[Editor]")]
    writer = [m for m in state["messages"] if m.startswith("[Writer]")]
    final = edited[-1] if edited else writer[-1] if writer else "No output."
    return {"final_output": final}

graph = StateGraph(ReviewCollabState)
graph.add_node("researcher", research_agent)
graph.add_node("writer", write_agent)
graph.add_node("reviewer", review_agent)
graph.add_node("editor", editor_agent)
graph.add_node("compile", compile_output)

graph.add_edge(START, "researcher")
graph.add_edge("researcher", "writer")
graph.add_edge("writer", "reviewer")
graph.add_conditional_edges("reviewer", route_after_review, {
    "editor": "editor",
    "compile": "compile",
})
graph.add_edge("editor", "researcher")  # editor → next research round
graph.add_edge("compile", END)

app = graph.compile()

print("\n--- TODO 1: Editor Agent ---")
print("Flow: researcher → writer → reviewer → editor → [researcher | compile]\n")

result = app.invoke({
    "topic": "UniGPS Fleet Management",
    "messages": [], "current_turn": "researcher",
    "rounds_left": 3, "final_output": "", "score": 0,
})

print(f"\nAll messages ({len(result['messages'])}):")
for msg in result["messages"]:
    print(f"  {msg[:80]}...")
print(f"\nFinal: {result['final_output'][:80]}...")
print(f"Score: {result['score']}/10")

# ============================================================
# TODO 2 Solution: Message limit
# ============================================================

print("\n\n--- TODO 2: Message Limit ---\n")

class LimitedCollabState(TypedDict):
    topic: str
    messages: Annotated[list, add]
    current_turn: str
    rounds_left: int
    max_messages: int
    final_output: str
    score: int

def ltd_researcher(state: LimitedCollabState) -> dict:
    msg = f"[Researcher] Data on {state['topic']}: 500 employees, 3 offices, 40% growth."
    print(f"  [researcher] {msg[:60]}...")
    return {"messages": [msg], "current_turn": "writer"}

def ltd_writer(state: LimitedCollabState) -> dict:
    msg = f"[Writer] {state['topic']} is a fast-growing fleet management company."
    print(f"  [writer] {msg[:60]}...")
    return {"messages": [msg], "current_turn": "reviewer"}

def ltd_reviewer(state: LimitedCollabState) -> dict:
    score = 5  # always low to force more rounds
    msg = f"[Reviewer] Score: {score}/10. Needs improvement."
    print(f"  [reviewer] Score: {score}")
    return {"messages": [msg], "current_turn": "researcher",
            "rounds_left": state["rounds_left"] - 1, "score": score}

def route_with_limit(state: LimitedCollabState) -> str:
    if len(state["messages"]) >= state["max_messages"]:
        print(f"  [route] Message limit ({state['max_messages']}) reached!")
        return "compile"
    if state["rounds_left"] <= 0 or state.get("score", 0) >= 7:
        return "compile"
    return state["current_turn"]

def ltd_compile(state: LimitedCollabState) -> dict:
    writer_msgs = [m for m in state["messages"] if m.startswith("[Writer]")]
    return {"final_output": writer_msgs[-1] if writer_msgs else "No output."}

g2 = StateGraph(LimitedCollabState)
g2.add_node("researcher", ltd_researcher)
g2.add_node("writer", ltd_writer)
g2.add_node("reviewer", ltd_reviewer)
g2.add_node("compile", ltd_compile)

g2.add_edge(START, "researcher")
g2.add_edge("researcher", "writer")
g2.add_edge("writer", "reviewer")
g2.add_conditional_edges("reviewer", route_with_limit, {
    "researcher": "researcher",
    "compile": "compile",
})
g2.add_edge("compile", END)

app2 = g2.compile()

result = app2.invoke({
    "topic": "UniGPS", "messages": [], "current_turn": "researcher",
    "rounds_left": 10, "max_messages": 6,
    "final_output": "", "score": 0,
})

print(f"\nMessages: {len(result['messages'])} (max: 6)")
print(f"Rounds left: {result['rounds_left']} (started at 10)")
print(f"→ Stopped by message limit, not round limit!")

print("\n" + "=" * 50)
print("Lab 03 Solution complete!")
print("- TODO 1: Editor agent polishes drafts between reviewer and researcher")
print("- TODO 2: max_messages stops collaboration regardless of rounds/score")
