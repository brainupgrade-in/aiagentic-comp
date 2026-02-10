"""
Lab 02: FastAPI + LangGraph Agent
====================================
Goal: Connect FastAPI endpoints to a LangGraph multi-agent system.

What you'll learn:
- Exposing LangGraph agents via REST endpoints
- Async request handling with run_in_executor
- Proper error handling with HTTP status codes

Needs: GROQ_API_KEY in .env
"""

import os
import asyncio
from typing import TypedDict, Annotated
from operator import add
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

print("=" * 50)
print("  FastAPI + LangGraph Agent")
print("=" * 50)

# ============================================================
# Step 1: LangGraph agent exposed via FastAPI
# ============================================================

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# --- Agent State ---

class SupportState(TypedDict):
    request: str
    category: str
    worker_output: str
    error: str
    final_response: str
    audit: Annotated[list, add]

# --- Agent Nodes ---

TEMPLATES = {
    "hr": "Please visit the HR portal or email hr@unigps.in.",
    "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
    "finance": "Please email finance@unigps.in with details.",
    "general": "Your request has been noted. A team member will respond shortly.",
}

def supervisor(state: SupportState) -> dict:
    prompt = f"Classify as: hr, tech, finance, general. One word.\n{state['request']}"
    try:
        response = llm.invoke(prompt)
        cat = response.content.strip().lower()
        if cat not in ["hr", "tech", "finance", "general"]:
            cat = "general"
    except Exception:
        cat = "general"
    return {"category": cat, "error": "",
            "audit": [f"Supervisor: classified as {cat}"]}

def worker(state: SupportState) -> dict:
    prompt = (
        f"You are UniGPS {state['category']} support.\n"
        f"Request: {state['request']}\n"
        f"Reply helpfully in 2 sentences."
    )
    try:
        response = llm.invoke(prompt)
        return {"worker_output": response.content.strip(), "error": "",
                "audit": [f"Worker ({state['category']}) responded"]}
    except Exception as e:
        return {"worker_output": TEMPLATES.get(state["category"], TEMPLATES["general"]),
                "error": str(e), "audit": [f"Worker error, used template"]}

def finalize(state: SupportState) -> dict:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS | {ts}",
            "audit": [f"Finalized at {ts}"]}

# --- Build Graph ---

graph = StateGraph(SupportState)
graph.add_node("supervisor", supervisor)
graph.add_node("worker", worker)
graph.add_node("finalize", finalize)
graph.add_edge(START, "supervisor")
graph.add_edge("supervisor", "worker")
graph.add_edge("worker", "finalize")
graph.add_edge("finalize", END)
agent = graph.compile()

# --- FastAPI App ---

app = FastAPI(title="UniGPS Agent API", version="1.0.0")

class AgentRequest(BaseModel):
    employee_name: str
    request: str

class AgentResponse(BaseModel):
    category: str
    response: str
    audit: list[str]

@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "ready"}

@app.post("/api/support", response_model=AgentResponse)
async def handle_support(req: AgentRequest):
    """Synchronous agent call — blocks the event loop."""
    result = agent.invoke({
        "request": req.request, "category": "", "worker_output": "",
        "error": "", "final_response": "", "audit": [],
    })
    return AgentResponse(
        category=result["category"],
        response=result["final_response"],
        audit=result["audit"],
    )

# --- Test ---

client = TestClient(app)

print("\n--- Step 1: LangGraph via FastAPI ---\n")

resp = client.get("/health")
print(f"  GET /health → {resp.json()}")

resp = client.post("/api/support", json={
    "employee_name": "Priya", "request": "I need sick leave"
})
data = resp.json()
print(f"  POST /api/support → {data['category']}")
print(f"  Response: {data['response'][:80]}...")
print(f"  Audit trail: {data['audit']}")


# ============================================================
# Step 2: Async handling with run_in_executor
# ============================================================

print("\n\n--- Step 2: Async Agent Endpoint ---\n")

@app.post("/api/support/async", response_model=AgentResponse)
async def handle_support_async(req: AgentRequest):
    """Non-blocking — runs agent in thread pool."""
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: agent.invoke({
            "request": req.request, "category": "", "worker_output": "",
            "error": "", "final_response": "", "audit": [],
        })
    )
    return AgentResponse(
        category=result["category"],
        response=result["final_response"],
        audit=result["audit"],
    )

resp = client.post("/api/support/async", json={
    "employee_name": "Vikram", "request": "VPN keeps disconnecting"
})
data = resp.json()
print(f"  POST /api/support/async → {data['category']}")
print(f"  Response: {data['response'][:80]}...")


# ============================================================
# TODO 1: Add error handling with proper HTTP status codes
# ============================================================
# Create an endpoint /api/support/safe that:
# - Returns 400 if request text is empty or too short (< 5 chars)
# - Returns 503 if the agent encounters an error (use error field in state)
# - Returns 200 with the normal response on success
#
# Hint:
#   @app.post("/api/support/safe")
#   async def handle_safe(req: AgentRequest):
#       if len(req.request.strip()) < 5:
#           raise HTTPException(status_code=400,
#               detail={"error": "Request too short", "min_length": 5})
#
#       loop = asyncio.get_event_loop()
#       result = await loop.run_in_executor(None, lambda: agent.invoke({...}))
#
#       if result["error"]:
#           raise HTTPException(status_code=503,
#               detail={"error": "Agent processing failed",
#                        "message": result["error"]})
#
#       return AgentResponse(...)
#
# Test:
#   client.post("/api/support/safe", json={"employee_name": "X", "request": "Hi"})
#   → 400
#   client.post("/api/support/safe", json={"employee_name": "Priya", "request": "I need leave"})
#   → 200


# ============================================================
# TODO 2: Add conversation threading via thread_id
# ============================================================
# Store conversation results by thread_id and allow retrieval.
#
# Hint:
#   conversations = {}
#
#   class ThreadedRequest(BaseModel):
#       employee_name: str
#       request: str
#       thread_id: str = None  # optional, auto-generated if not provided
#
#   @app.post("/api/support/threaded")
#   async def handle_threaded(req: ThreadedRequest):
#       import uuid
#       thread_id = req.thread_id or str(uuid.uuid4())[:8]
#       loop = asyncio.get_event_loop()
#       result = await loop.run_in_executor(None, lambda: agent.invoke({...}))
#       conversations[thread_id] = {
#           "thread_id": thread_id,
#           "employee_name": req.employee_name,
#           "request": req.request,
#           "category": result["category"],
#           "response": result["final_response"],
#           "audit": result["audit"],
#       }
#       return conversations[thread_id]
#
#   @app.get("/api/support/thread/{thread_id}")
#   async def get_thread(thread_id: str):
#       if thread_id not in conversations:
#           raise HTTPException(status_code=404, detail="Thread not found")
#       return conversations[thread_id]
#
# Test:
#   1. POST to /api/support/threaded → get thread_id
#   2. GET /api/support/thread/{thread_id} → retrieve conversation


print("\n" + "=" * 50)
print("Lab 02 complete!")
print("Patterns: LangGraph + FastAPI, async handling, TestClient")
