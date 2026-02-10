"""
Lab 07 Solution: Performance Optimization
============================================
"""

import os
import time
from typing import TypedDict, Annotated
from operator import add
from functools import lru_cache
from datetime import datetime
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

print("=" * 50)
print("  Performance Optimization (Solution)")
print("=" * 50)

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# ============================================================
# Step 1: Response caching
# ============================================================

print("\n--- Step 1: Response Caching ---\n")

def classify_no_cache(request_text: str) -> str:
    response = llm.invoke(f"Classify: hr, tech, finance, general. One word.\n{request_text}")
    cat = response.content.strip().lower()
    return cat if cat in ["hr", "tech", "finance", "general"] else "general"

@lru_cache(maxsize=100)
def classify_cached(request_text: str) -> str:
    response = llm.invoke(f"Classify: hr, tech, finance, general. One word.\n{request_text}")
    cat = response.content.strip().lower()
    return cat if cat in ["hr", "tech", "finance", "general"] else "general"

test_input = "I need sick leave"

start = time.time()
result1 = classify_cached(test_input)
first_call = time.time() - start

start = time.time()
result2 = classify_cached(test_input)
second_call = time.time() - start

print(f"  First call:  {result1} ({first_call:.3f}s) — LLM call")
print(f"  Second call: {result2} ({second_call:.6f}s) — cached!")
print(f"  Speedup: {first_call / max(second_call, 0.000001):.0f}x faster")
print(f"  Cache info: {classify_cached.cache_info()}")

classify_cached.cache_clear()

# ============================================================
# Step 2: Per-agent timing
# ============================================================

print("\n\n--- Step 2: Per-Agent Timing ---\n")

class TimedState(TypedDict):
    request: str
    category: str
    worker_output: str
    final_response: str
    timings: Annotated[list, add]
    audit: Annotated[list, add]

TEMPLATES = {
    "hr": "Please visit the HR portal or email hr@unigps.in.",
    "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
    "finance": "Please email finance@unigps.in with details.",
    "general": "Your request has been noted. A team member will respond shortly.",
}

def timed_supervisor(state: TimedState) -> dict:
    start = time.time()
    prompt = f"Classify: hr, tech, finance, general. One word.\n{state['request']}"
    try:
        response = llm.invoke(prompt)
        cat = response.content.strip().lower()
        if cat not in TEMPLATES:
            cat = "general"
    except Exception:
        cat = "general"
    elapsed = time.time() - start
    flag = " [SLOW]" if elapsed > 5 else ""
    print(f"  [supervisor] {cat} ({elapsed:.2f}s{flag})")
    return {"category": cat,
            "timings": [{"agent": "supervisor", "seconds": round(elapsed, 2)}],
            "audit": [f"Supervisor: {elapsed:.2f}s{flag}"]}

def timed_worker(state: TimedState) -> dict:
    start = time.time()
    prompt = f"You are UniGPS {state['category']} support.\n{state['request']}\nReply in 2 sentences."
    try:
        response = llm.invoke(prompt)
        output = response.content.strip()
    except Exception:
        output = TEMPLATES.get(state["category"], TEMPLATES["general"])
    elapsed = time.time() - start
    flag = " [SLOW]" if elapsed > 5 else ""
    print(f"  [worker] {state['category']} ({elapsed:.2f}s{flag})")
    return {"worker_output": output,
            "timings": [{"agent": f"worker_{state['category']}", "seconds": round(elapsed, 2)}],
            "audit": [f"Worker: {elapsed:.2f}s{flag}"]}

def timed_finalize(state: TimedState) -> dict:
    total = sum(t["seconds"] for t in state["timings"])
    flag = " [SLOW TOTAL]" if total > 10 else ""
    return {"final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS",
            "timings": [{"agent": "total", "seconds": round(total, 2)}],
            "audit": [f"Total: {total:.2f}s{flag}"]}

graph = StateGraph(TimedState)
graph.add_node("supervisor", timed_supervisor)
graph.add_node("worker", timed_worker)
graph.add_node("finalize", timed_finalize)
graph.add_edge(START, "supervisor")
graph.add_edge("supervisor", "worker")
graph.add_edge("worker", "finalize")
graph.add_edge("finalize", END)
timed_agent = graph.compile()

for req in ["I need sick leave", "Server is very slow", "Submit my expense report"]:
    result = timed_agent.invoke({
        "request": req, "category": "", "worker_output": "",
        "final_response": "", "timings": [], "audit": [],
    })
    total = [t for t in result["timings"] if t["agent"] == "total"]
    print(f"  '{req}' → {result['category']} (total: {total[0]['seconds']}s)\n")

print("  Timing Summary:")
print(f"  {'Agent':<25} {'Time':>8}")
print("  " + "-" * 35)
for t in result["timings"]:
    flag = " !" if t["agent"] != "total" and t["seconds"] > 5 else ""
    print(f"  {t['agent']:<25} {t['seconds']:>6.2f}s{flag}")


# ============================================================
# TODO 1 Solution: Cache with hit/miss tracking
# ============================================================

print("\n\n--- TODO 1: Tracked Cache ---\n")

class TrackedCache:
    def __init__(self, maxsize=100):
        self._cache = {}
        self._maxsize = maxsize
        self.hits = 0
        self.misses = 0
        self.time_saved = 0.0

    def get_or_compute(self, key: str, compute_fn):
        """Return cached value or compute and store it."""
        if key in self._cache:
            self.hits += 1
            self.time_saved += self._cache[key]["elapsed"]
            return self._cache[key]["value"]

        self.misses += 1
        start = time.time()
        value = compute_fn()
        elapsed = time.time() - start

        # Evict oldest if full
        if len(self._cache) >= self._maxsize:
            oldest = next(iter(self._cache))
            del self._cache[oldest]

        self._cache[key] = {"value": value, "elapsed": elapsed}
        return value

    def stats(self):
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100) if total > 0 else 0
        return {
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": f"{hit_rate:.1f}%",
            "time_saved": f"{self.time_saved:.2f}s",
            "cached_entries": len(self._cache),
        }

cache = TrackedCache()

# Test with repeated requests
test_requests = ["sick leave", "server down", "sick leave", "expense", "sick leave", "server down"]
for req in test_requests:
    result = cache.get_or_compute(req, lambda r=req: classify_no_cache(r))
    print(f"  '{req}' → {result}")

print(f"\n  Cache stats: {cache.stats()}")
# Expected: 3 misses (unique), 3 hits (repeated)


# ============================================================
# TODO 2 Solution: Model right-sizing comparison
# ============================================================

print("\n\n--- TODO 2: Model Right-Sizing ---\n")

fast_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
smart_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.3)

def model_comparison(request_text: str):
    # Fast model for classification
    start = time.time()
    cat_resp = fast_llm.invoke(
        f"Classify: hr, tech, finance, general. One word.\n{request_text}")
    fast_time = time.time() - start
    category = cat_resp.content.strip().lower()
    if category not in ["hr", "tech", "finance", "general"]:
        category = "general"

    # Smart model for response
    start = time.time()
    work_resp = smart_llm.invoke(
        f"You are UniGPS {category} support.\n{request_text}\nReply in 2 sentences.")
    smart_time = time.time() - start

    return {
        "category": category,
        "response": work_resp.content.strip(),
        "fast_model_time": round(fast_time, 2),
        "smart_model_time": round(smart_time, 2),
        "total_time": round(fast_time + smart_time, 2),
    }

# Comparison: right-sized vs single model
print("  Right-sized (8B router + 70B worker):")
for req in ["I need leave", "Server down", "Submit expense"]:
    result = model_comparison(req)
    print(f"    '{req}'")
    print(f"      Category: {result['category']} (8B: {result['fast_model_time']}s)")
    print(f"      Response: {result['response'][:50]}... (70B: {result['smart_model_time']}s)")
    print(f"      Total: {result['total_time']}s")
    print()

print("\n  Single model (70B for everything):")
for req in ["I need leave", "Server down", "Submit expense"]:
    start = time.time()
    cat = classify_no_cache(req)
    classify_time = time.time() - start

    start = time.time()
    resp = llm.invoke(f"You are UniGPS {cat} support.\n{req}\nReply in 2 sentences.")
    response_time = time.time() - start

    total = classify_time + response_time
    print(f"    '{req}' → {cat} ({classify_time:.2f}s + {response_time:.2f}s = {total:.2f}s)")

print("\n" + "=" * 50)
print("Lab 07 Solution complete!")
print("- TODO 1: TrackedCache with hit/miss stats and time savings")
print("- TODO 2: Model right-sizing (8B for routing, 70B for responses)")
