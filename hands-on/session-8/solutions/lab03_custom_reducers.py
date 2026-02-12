"""
Lab 03 Solution: Custom Reducers
===================================
"""

from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, START, END

print("=" * 50)
print("  Custom Reducers (Solution)")
print("=" * 50)

# Steps 1-5 same as lab — see lab file for details

# ============================================================
# TODO 1 Solution: Deduplication reducer
# ============================================================

def deduplicate(current: list, new: list) -> list:
    """Keep only unique items, preserving insertion order."""
    seen = set()
    result = []
    for item in current + new:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

class DedupeState(TypedDict):
    text: str
    tags: Annotated[list, deduplicate]

def tag_category(state: DedupeState) -> dict:
    msg = state["text"].lower()
    tags = []
    if any(w in msg for w in ["leave", "sick"]):
        tags.extend(["hr", "leave"])
    if any(w in msg for w in ["urgent", "critical"]):
        tags.extend(["urgent", "hr"])  # "hr" might be duplicate!
    return {"tags": tags}

def tag_priority(state: DedupeState) -> dict:
    msg = state["text"].lower()
    tags = []
    if "urgent" in msg:
        tags.extend(["urgent", "high_priority"])  # "urgent" might be duplicate!
    else:
        tags.append("normal")
    return {"tags": tags}

def tag_source(state: DedupeState) -> dict:
    return {"tags": ["email", "hr"]}  # "hr" might be duplicate!

graph1 = StateGraph(DedupeState)
graph1.add_node("category", tag_category)
graph1.add_node("priority", tag_priority)
graph1.add_node("source", tag_source)

graph1.add_edge(START, "category")
graph1.add_edge("category", "priority")
graph1.add_edge("priority", "source")
graph1.add_edge("source", END)

app1 = graph1.compile()

print("\n--- TODO 1: Deduplication Reducer ---")
for text in ["Urgent sick leave request", "Normal leave application"]:
    result = app1.invoke({"text": text, "tags": []})
    print(f"  '{text}' → tags: {result['tags']}")
    print(f"    (no duplicates despite overlap!)")

# ============================================================
# TODO 2 Solution: Running average reducer
# ============================================================

def running_average(current: dict, new: dict) -> dict:
    """Maintain a running average of scores."""
    total_sum = current.get("sum", 0) + new.get("sum", 0)
    total_count = current.get("count", 0) + new.get("count", 0)
    avg = total_sum / total_count if total_count > 0 else 0
    return {"sum": total_sum, "count": total_count, "avg": round(avg, 2)}

class AvgState(TypedDict):
    text: str
    stats: Annotated[dict, running_average]

def score_length(state: AvgState) -> dict:
    score = min(10, len(state["text"].split()) // 2)
    return {"stats": {"sum": score, "count": 1}}

def score_keywords(state: AvgState) -> dict:
    keywords = ["support", "help", "issue", "request", "urgent"]
    score = min(10, sum(1 for w in keywords if w in state["text"].lower()) * 3)
    return {"stats": {"sum": score, "count": 1}}

def score_politeness(state: AvgState) -> dict:
    polite_words = ["please", "thank", "kindly", "appreciate"]
    score = min(10, sum(2 for w in polite_words if w in state["text"].lower()))
    return {"stats": {"sum": score, "count": 1}}

graph2 = StateGraph(AvgState)
graph2.add_node("length", score_length)
graph2.add_node("keywords", score_keywords)
graph2.add_node("politeness", score_politeness)

graph2.add_edge(START, "length")
graph2.add_edge("length", "keywords")
graph2.add_edge("keywords", "politeness")
graph2.add_edge("politeness", END)

app2 = graph2.compile()

print("\n--- TODO 2: Running Average Reducer ---")
for text in [
    "Please help me with an urgent support request, I would appreciate it",
    "Leave",
    "I need help with a technical issue please",
]:
    result = app2.invoke({"text": text, "stats": {"sum": 0, "count": 0, "avg": 0}})
    s = result["stats"]
    print(f"  '{text[:50]}...'")
    print(f"    sum={s['sum']}, count={s['count']}, avg={s['avg']}")

print("\n" + "=" * 50)
print("Lab 03 Solution complete!")
print("- TODO 1: Deduplication reducer removes duplicates, preserves order")
print("- TODO 2: Running average tracks sum/count/avg across nodes")
