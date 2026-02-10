"""
Lab 08 Challenge Solution: Complete UniGPS Production Agent API
=================================================================
"""

import os
import json
import time
from typing import TypedDict, Annotated
from operator import add
from functools import lru_cache
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

print("=" * 60)
print("  Challenge Solution: UniGPS Production Agent API")
print("=" * 60)

# ============================================================
# 1. LLM Setup (connection pooling — one client shared everywhere)
# ============================================================

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# ============================================================
# 2. Agent State
# ============================================================

class SupportState(TypedDict):
    request: str
    employee_name: str
    category: str
    worker_output: str
    error: str
    fallback_used: bool
    final_response: str
    timings: Annotated[list, add]
    audit: Annotated[list, add]

# ============================================================
# 3. Templates
# ============================================================

TEMPLATES = {
    "hr": "Please visit the HR portal or email hr@unigps.in.",
    "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
    "finance": "Please email finance@unigps.in with details.",
    "general": "Your request has been noted. A team member will respond shortly.",
}

# ============================================================
# 4. Cached classification
# ============================================================

@lru_cache(maxsize=200)
def cached_classify(request_text: str) -> str:
    """Classify with caching for repeated queries."""
    response = llm.invoke(
        f"Classify as: hr, tech, finance, general. One word.\n{request_text}")
    cat = response.content.strip().lower()
    return cat if cat in TEMPLATES else "general"

# ============================================================
# 5. Agent Nodes
# ============================================================

def supervisor(state: SupportState) -> dict:
    """LLM supervisor with timing and caching."""
    start = time.time()
    try:
        cat = cached_classify(state["request"])
    except Exception:
        cat = "general"
    elapsed = time.time() - start
    flag = " [SLOW]" if elapsed > 5 else ""
    return {
        "category": cat,
        "error": "",
        "timings": [{"agent": "supervisor", "seconds": round(elapsed, 2)}],
        "audit": [f"Supervisor: {cat} ({elapsed:.2f}s{flag})"],
    }

def worker(state: SupportState) -> dict:
    """Domain worker with fallback."""
    start = time.time()
    prompt = (
        f"You are UniGPS {state['category']} support.\n"
        f"Employee: {state['employee_name']}\n"
        f"Request: {state['request']}\n"
        f"Reply helpfully in 2 sentences."
    )
    try:
        response = llm.invoke(prompt)
        output = response.content.strip()
        error = ""
    except Exception as e:
        output = ""
        error = str(e)
    elapsed = time.time() - start
    flag = " [SLOW]" if elapsed > 5 else ""
    return {
        "worker_output": output,
        "error": error,
        "fallback_used": False,
        "timings": [{"agent": f"worker_{state['category']}", "seconds": round(elapsed, 2)}],
        "audit": [f"Worker ({state['category']}): {elapsed:.2f}s{flag}"],
    }

def route_after_worker(state: SupportState) -> str:
    return "fallback" if state["error"] else "finalize"

def fallback(state: SupportState) -> dict:
    template = TEMPLATES.get(state["category"], TEMPLATES["general"])
    return {
        "worker_output": template,
        "error": "",
        "fallback_used": True,
        "audit": [f"Fallback template: {state['category']}"],
    }

def finalize(state: SupportState) -> dict:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = sum(t["seconds"] for t in state["timings"])
    flag = " [SLOW TOTAL]" if total > 10 else ""
    return {
        "final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS | {ts}",
        "timings": [{"agent": "total", "seconds": round(total, 2)}],
        "audit": [f"Finalized: {total:.2f}s total{flag}"],
    }

# ============================================================
# 6. Build LangGraph
# ============================================================

graph = StateGraph(SupportState)
graph.add_node("supervisor", supervisor)
graph.add_node("worker", worker)
graph.add_node("fallback", fallback)
graph.add_node("finalize", finalize)

graph.add_edge(START, "supervisor")
graph.add_edge("supervisor", "worker")
graph.add_conditional_edges("worker", route_after_worker, {
    "finalize": "finalize",
    "fallback": "fallback",
})
graph.add_edge("fallback", "finalize")
graph.add_edge("finalize", END)

agent = graph.compile()

# ============================================================
# 7. Pydantic Models
# ============================================================

class SupportRequest(BaseModel):
    employee_name: str = Field(..., min_length=2, max_length=100)
    request: str = Field(..., min_length=5, max_length=1000)

class SupportResponse(BaseModel):
    ticket_id: str
    category: str
    response: str
    fallback_used: bool
    timing_seconds: float
    audit: list[str]

class TicketInfo(BaseModel):
    ticket_id: str
    employee_name: str
    request: str
    category: str
    response: str
    fallback_used: bool
    timestamp: str

# ============================================================
# 8. Ticket Store
# ============================================================

ticket_store = {}
request_count = 0
start_time = datetime.now()

# ============================================================
# 9. FastAPI App
# ============================================================

app = FastAPI(
    title="UniGPS Production Agent API",
    version="2.0.0",
    description="Production-ready multi-agent support system",
)

@app.get("/health")
async def health():
    uptime = (datetime.now() - start_time).total_seconds()
    return {
        "status": "healthy",
        "agent": "ready",
        "version": "2.0.0",
        "uptime_seconds": round(uptime, 1),
        "total_requests": request_count,
    }

@app.post("/api/support", response_model=SupportResponse)
async def handle_support(req: SupportRequest):
    """Batch endpoint: returns full response."""
    global request_count
    request_count += 1

    req_start = time.time()
    result = agent.invoke({
        "request": req.request, "employee_name": req.employee_name,
        "category": "", "worker_output": "", "error": "",
        "fallback_used": False, "final_response": "",
        "timings": [], "audit": [],
    })
    elapsed = time.time() - req_start

    ticket_id = f"TKT-{request_count:04d}"
    ticket_store[ticket_id] = TicketInfo(
        ticket_id=ticket_id,
        employee_name=req.employee_name,
        request=req.request,
        category=result["category"],
        response=result["final_response"],
        fallback_used=result["fallback_used"],
        timestamp=datetime.now().isoformat(),
    ).model_dump()

    return SupportResponse(
        ticket_id=ticket_id,
        category=result["category"],
        response=result["final_response"],
        fallback_used=result["fallback_used"],
        timing_seconds=round(elapsed, 2),
        audit=result["audit"],
    )

@app.post("/api/support/stream")
async def stream_support(req: SupportRequest):
    """Streaming endpoint: SSE events per agent node."""
    def generate():
        yield f"data: {json.dumps({'event': 'start', 'employee': req.employee_name})}\n\n"

        init_state = {
            "request": req.request, "employee_name": req.employee_name,
            "category": "", "worker_output": "", "error": "",
            "fallback_used": False, "final_response": "",
            "timings": [], "audit": [],
        }
        try:
            for event in agent.stream(init_state):
                for node_name, output in event.items():
                    yield f"data: {json.dumps({'event': 'node', 'node': node_name, 'output': output})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'event': 'error', 'message': str(e)})}\n\n"

        yield f"data: {json.dumps({'event': 'done'})}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")

@app.get("/api/tickets")
async def list_tickets(category: str = None, limit: int = 10):
    """List recent tickets, optionally filtered by category."""
    tickets = list(ticket_store.values())
    if category:
        tickets = [t for t in tickets if t["category"] == category]
    return {"tickets": tickets[-limit:], "total": len(tickets)}

@app.get("/api/tickets/{ticket_id}")
async def get_ticket(ticket_id: str):
    """Get a ticket by ID."""
    if ticket_id not in ticket_store:
        raise HTTPException(status_code=404, detail=f"Ticket '{ticket_id}' not found")
    return ticket_store[ticket_id]

@app.get("/api/stats")
async def get_stats():
    """Return cache stats and request counts."""
    cache_info = cached_classify.cache_info()
    return {
        "total_requests": request_count,
        "total_tickets": len(ticket_store),
        "cache": {
            "hits": cache_info.hits,
            "misses": cache_info.misses,
            "size": cache_info.currsize,
            "maxsize": cache_info.maxsize,
            "hit_rate": f"{(cache_info.hits / max(cache_info.hits + cache_info.misses, 1) * 100):.1f}%",
        },
    }

# ============================================================
# 10. Tests
# ============================================================

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "healthy"
    assert "uptime_seconds" in data
    print(f"  PASS test_health: {data}")

def test_support_success():
    resp = client.post("/api/support", json={
        "employee_name": "Priya",
        "request": "I need sick leave for 3 days",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] in ["hr", "tech", "finance", "general"]
    assert data["ticket_id"].startswith("TKT-")
    assert data["timing_seconds"] > 0
    assert len(data["audit"]) >= 3
    print(f"  PASS test_support_success: {data['ticket_id']} → {data['category']} ({data['timing_seconds']}s)")

def test_validation_error():
    resp = client.post("/api/support", json={
        "employee_name": "P",
        "request": "Hi",
    })
    assert resp.status_code == 422
    print(f"  PASS test_validation_error: got 422 as expected")

def test_ticket_retrieval():
    # Create a ticket
    resp = client.post("/api/support", json={
        "employee_name": "Vikram",
        "request": "Server is down in production",
    })
    ticket_id = resp.json()["ticket_id"]

    # Retrieve it
    resp = client.get(f"/api/tickets/{ticket_id}")
    assert resp.status_code == 200
    assert resp.json()["employee_name"] == "Vikram"
    print(f"  PASS test_ticket_retrieval: retrieved {ticket_id}")

def test_ticket_not_found():
    resp = client.get("/api/tickets/FAKE-9999")
    assert resp.status_code == 404
    print(f"  PASS test_ticket_not_found: got 404 as expected")

def test_ticket_list():
    resp = client.get("/api/tickets")
    assert resp.status_code == 200
    data = resp.json()
    assert "tickets" in data
    assert data["total"] >= 0
    print(f"  PASS test_ticket_list: {data['total']} tickets")

def test_ticket_filter():
    resp = client.get("/api/tickets?category=hr")
    assert resp.status_code == 200
    tickets = resp.json()["tickets"]
    for t in tickets:
        assert t["category"] == "hr"
    print(f"  PASS test_ticket_filter: {len(tickets)} HR tickets")

def test_stats_endpoint():
    resp = client.get("/api/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "cache" in data
    assert "total_requests" in data
    assert data["total_requests"] >= 0
    print(f"  PASS test_stats_endpoint: {data}")

def test_streaming():
    events = []
    with client.stream("POST", "/api/support/stream",
                        json={"employee_name": "Rahul", "request": "Where is my salary?"}) as resp:
        for line in resp.iter_lines():
            if line.startswith("data: "):
                data = json.loads(line[6:])
                events.append(data.get("event", "unknown"))

    assert "start" in events
    assert "done" in events
    assert events.count("node") >= 2  # at least supervisor + worker
    print(f"  PASS test_streaming: events={events}")

# --- Run All Tests ---

print("\n--- Running Tests ---\n")

test_functions = [
    test_health,
    test_support_success,
    test_validation_error,
    test_ticket_retrieval,
    test_ticket_not_found,
    test_ticket_list,
    test_ticket_filter,
    test_stats_endpoint,
    test_streaming,
]

passed = 0
failed = 0
for func in test_functions:
    try:
        func()
        passed += 1
    except AssertionError as e:
        print(f"  FAIL {func.__name__}: {e}")
        failed += 1
    except Exception as e:
        print(f"  ERROR {func.__name__}: {e}")
        failed += 1

print(f"\n  Results: {passed} passed, {failed} failed, {passed + failed} total")

# --- Demo Run ---

print("\n\n--- Demo: Full Request Flow ---\n")

test_scenarios = [
    ("Priya", "I need sick leave for 3 days"),
    ("Vikram", "Server is down in production"),
    ("Anita", "Submit my expense report for March"),
    ("Rahul", "Where is the cafeteria?"),
]

for name, request in test_scenarios:
    resp = client.post("/api/support", json={
        "employee_name": name, "request": request
    })
    data = resp.json()
    print(f"  {name}: '{request}'")
    print(f"    → {data['ticket_id']} | {data['category']} | {data['timing_seconds']}s")
    print(f"    Fallback: {data['fallback_used']} | Audit: {len(data['audit'])} entries")
    print()

# Cache test (repeated query)
print("  Cache test (repeated query):")
resp1 = client.post("/api/support", json={
    "employee_name": "Meera", "request": "I need sick leave for 3 days"
})
resp2 = client.get("/api/stats")
stats = resp2.json()
print(f"  Stats after repeated query: {stats['cache']}")

print("\n" + "=" * 60)
print("Challenge Solution complete!")
print("- 6 endpoints: health, support, stream, tickets, ticket/{id}, stats")
print("- LangGraph agent with supervisor + worker + fallback + finalize")
print("- lru_cache for classification, per-request timing")
print(f"- {passed}/{passed + failed} tests passing")
