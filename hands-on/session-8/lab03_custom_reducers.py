"""
Lab 03: Custom Reducers
=========================
Goal: Learn how to write custom reducer functions beyond operator.add
      for sophisticated state management.

What you'll learn:
- How reducers work: (old_value, new_value) → combined_value
- Sliding window reducer (keep last N items)
- Dictionary merge reducer
- Max/min value reducer
- When to use each pattern
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Custom Reducers")
print("=" * 50)

# ============================================================
# Step 1: Review — the default reducer (operator.add)
# ============================================================

class BasicState(TypedDict):
    log: Annotated[list, add]  # operator.add = list concatenation

def step_a(state: BasicState) -> dict:
    return {"log": ["step_a ran"]}

def step_b(state: BasicState) -> dict:
    return {"log": ["step_b ran"]}

graph1 = StateGraph(BasicState)
graph1.add_node("a", step_a)
graph1.add_node("b", step_b)
graph1.add_edge(START, "a")
graph1.add_edge("a", "b")
graph1.add_edge("b", END)
app1 = graph1.compile()

result = app1.invoke({"log": ["start"]})
print("\n--- Step 1: operator.add (list concatenation) ---")
print(f"Log: {result['log']}")
print("→ All entries accumulate. List grows forever!")

# ============================================================
# Step 2: Sliding window reducer
# ============================================================
# Keep only the last N entries. Useful for chat history.

def keep_last_5(current: list, new: list) -> list:
    """Keep only the last 5 items."""
    return (current + new)[-5:]

class WindowState(TypedDict):
    messages: Annotated[list, keep_last_5]

def add_message(state: WindowState) -> dict:
    count = len(state["messages"]) + 1
    return {"messages": [f"Message #{count}"]}

# Build a chain of 8 nodes, each adding a message
graph2 = StateGraph(WindowState)
prev = START
for i in range(8):
    name = f"node_{i}"
    graph2.add_node(name, add_message)
    graph2.add_edge(prev, name)
    prev = name
graph2.add_edge(prev, END)
app2 = graph2.compile()

result = app2.invoke({"messages": []})
print("\n--- Step 2: Sliding Window (keep last 5) ---")
print(f"After 8 nodes, messages: {result['messages']}")
print(f"Length: {len(result['messages'])} (not 8!)")
print("→ Older messages are dropped. Only last 5 survive!")

# ============================================================
# Step 3: Dictionary merge reducer
# ============================================================

def merge_dicts(current: dict, new: dict) -> dict:
    """Merge new keys into existing dict."""
    return {**current, **new}

class MetadataState(TypedDict):
    request: str
    metadata: Annotated[dict, merge_dicts]

def extract_category(state: MetadataState) -> dict:
    msg = state["request"].lower()
    cat = "hr" if "leave" in msg else "tech" if "server" in msg else "general"
    return {"metadata": {"category": cat}}

def extract_priority(state: MetadataState) -> dict:
    msg = state["request"].lower()
    pri = "HIGH" if any(w in msg for w in ["urgent", "down", "critical"]) else "LOW"
    return {"metadata": {"priority": pri}}

def extract_department(state: MetadataState) -> dict:
    return {"metadata": {"department": "UniGPS Support", "timestamp": "2024-01-15"}}

graph3 = StateGraph(MetadataState)
graph3.add_node("category", extract_category)
graph3.add_node("priority", extract_priority)
graph3.add_node("department", extract_department)

graph3.add_edge(START, "category")
graph3.add_edge("category", "priority")
graph3.add_edge("priority", "department")
graph3.add_edge("department", END)

app3 = graph3.compile()

print("\n--- Step 3: Dictionary Merge ---")
for req in ["URGENT: Server is down!", "Apply for leave"]:
    result = app3.invoke({"request": req, "metadata": {}})
    print(f"  '{req[:30]}' → metadata: {result['metadata']}")
print("→ Each node adds keys. All keys accumulate in one dict!")

# ============================================================
# Step 4: Max value reducer
# ============================================================

def take_max(current: int, new: int) -> int:
    """Keep the maximum value seen so far."""
    return max(current, new)

class ScoreState(TypedDict):
    text: str
    max_score: Annotated[int, take_max]
    scores: Annotated[list, add]

def score_clarity(state: ScoreState) -> dict:
    score = min(10, len(state["text"].split()) // 2)
    print(f"  [clarity] score: {score}")
    return {"max_score": score, "scores": [{"type": "clarity", "score": score}]}

def score_relevance(state: ScoreState) -> dict:
    keywords = ["support", "help", "issue", "request", "need"]
    score = min(10, sum(1 for w in keywords if w in state["text"].lower()) * 3)
    print(f"  [relevance] score: {score}")
    return {"max_score": score, "scores": [{"type": "relevance", "score": score}]}

def score_urgency(state: ScoreState) -> dict:
    urgent_words = ["urgent", "critical", "asap", "immediately", "down"]
    score = min(10, sum(2 for w in urgent_words if w in state["text"].lower()))
    print(f"  [urgency] score: {score}")
    return {"max_score": score, "scores": [{"type": "urgency", "score": score}]}

graph4 = StateGraph(ScoreState)
graph4.add_node("clarity", score_clarity)
graph4.add_node("relevance", score_relevance)
graph4.add_node("urgency", score_urgency)

graph4.add_edge(START, "clarity")
graph4.add_edge("clarity", "relevance")
graph4.add_edge("relevance", "urgency")
graph4.add_edge("urgency", END)

app4 = graph4.compile()

print("\n--- Step 4: Max Value Reducer ---")
for text in [
    "URGENT: Production server is down, need help immediately!",
    "How do I apply for leave?",
]:
    print(f"\nText: '{text[:50]}'")
    result = app4.invoke({"text": text, "max_score": 0, "scores": []})
    print(f"  All scores: {result['scores']}")
    print(f"  Max score: {result['max_score']}")
print("→ max_score tracks the highest value across all nodes!")

# ============================================================
# Step 5: Summary — choosing the right reducer
# ============================================================

print("\n--- Step 5: Reducer Cheat Sheet ---")
print("""
  Reducer             Use Case                     Example
  ─────────────────   ──────────────────────────   ─────────────
  operator.add        Append to list               Audit trails, logs
  keep_last_N         Sliding window               Chat history (last 10)
  merge_dicts         Accumulate key-value pairs   Metadata collection
  take_max            Track highest value           Priority scores
  take_min            Track lowest value            Error counts
  deduplicate         Unique items only             Seen categories
  (no reducer)        Overwrite each time           Current status fields
""")

# ============================================================
# TODO 1: Build a deduplication reducer
# ============================================================
# Create a reducer that only keeps unique items in a list.
# Test it with nodes that might add duplicate categories.

# def deduplicate(current: list, new: list) -> list:
#     """Keep only unique items, preserving order."""
#     seen = set()
#     result = []
#     for item in current + new:
#         if item not in seen:
#             seen.add(item)
#             result.append(item)
#     return result
#
# class DedupeState(TypedDict):
#     tags: Annotated[list, deduplicate]
#
# Test: multiple nodes adding overlapping tags like ["hr", "leave"]
# and ["hr", "urgent"]. Result should have no duplicates.

# ============================================================
# TODO 2: Build a "running average" reducer
# ============================================================
# Create a reducer that maintains a running average of scores.
# The state should store {"sum": float, "count": int, "avg": float}.
# Each node adds a new score, the reducer updates the average.

# def running_average(current: dict, new: dict) -> dict:
#     total_sum = current.get("sum", 0) + new.get("sum", 0)
#     total_count = current.get("count", 0) + new.get("count", 0)
#     return {"sum": total_sum, "count": total_count, "avg": total_sum / total_count}
#
# class AvgState(TypedDict):
#     stats: Annotated[dict, running_average]

print("\n" + "=" * 50)
print("Lab 03 complete! Key takeaways:")
print("- Reducer = function(old_value, new_value) → combined_value")
print("- operator.add: simple concatenation (grows forever)")
print("- Custom reducers: sliding window, merge, max, deduplicate")
print("- Choose based on your use case: history vs current vs aggregate")
print("- No reducer = overwrite (last write wins)")
