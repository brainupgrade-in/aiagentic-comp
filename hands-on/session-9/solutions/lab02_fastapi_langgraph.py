"""
Lab 02 Solution: FastAPI + LangGraph Agent
=============================================
"""

import os
import uuid
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
print("  FastAPI + LangGraph Agent (Solution)")
print("=" * 50)

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# --- Agent ---

class SupportState(TypedDict):
    request: str
    category: str
    worker_output: str
    error: str
    final_response: str
    audit: Annotated[list, add]

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
        if cat not in TEMPLATES:
            cat = "general"
    except Exception:
        cat = "general"
    return {"category": cat, "error": "", "audit": [f"Supervisor: {cat}"]}

def worker(state: SupportState) -> dict:
    prompt = (
        f"You are UniGPS {state['category']} support.\n"
        f"Request: {state['request']}\nReply helpfully in 2 sentences."
    )
    try:
        response = llm.invoke(prompt)
        return {"worker_output": response.content.strip(), "error": "",
                "audit": [f"Worker ({state['category']}) responded"]}
    except Exception as e:
        return {"worker_output": TEMPLATES.get(state["category"], TEMPLATES["general"]),
                "error": str(e), "audit": ["Worker error, used template"]}

def finalize(state: SupportState) -> dict:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {"final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS | {ts}",
            "audit": [f"Finalized at {ts}"]}

graph = StateGraph(SupportState)
graph.add_node("supervisor", supervisor)
graph.add_node("worker", worker)
graph.add_node("finalize", finalize)
graph.add_edge(START, "supervisor")
graph.add_edge("supervisor", "worker")
graph.add_edge("worker", "finalize")
graph.add_edge("finalize", END)
agent = graph.compile()

# --- FastAPI ---

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
    result = agent.invoke({
        "request": req.request, "category": "", "worker_output": "",
        "error": "", "final_response": "", "audit": [],
    })
    return AgentResponse(
        category=result["category"],
        response=result["final_response"],
        audit=result["audit"],
    )

@app.post("/api/support/async", response_model=AgentResponse)
async def handle_support_async(req: AgentRequest):
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

# ============================================================
# TODO 1 Solution: Error handling with HTTP status codes
# ============================================================

@app.post("/api/support/safe")
async def handle_safe(req: AgentRequest):
    if len(req.request.strip()) < 5:
        raise HTTPException(
            status_code=400,
            detail={"error": "Request too short", "min_length": 5}
        )

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: agent.invoke({
            "request": req.request, "category": "", "worker_output": "",
            "error": "", "final_response": "", "audit": [],
        })
    )

    if result["error"]:
        raise HTTPException(
            status_code=503,
            detail={"error": "Agent processing failed", "message": result["error"]}
        )

    return AgentResponse(
        category=result["category"],
        response=result["final_response"],
        audit=result["audit"],
    )

# ============================================================
# TODO 2 Solution: Conversation threading
# ============================================================

conversations = {}

class ThreadedRequest(BaseModel):
    employee_name: str
    request: str
    thread_id: str = None

@app.post("/api/support/threaded")
async def handle_threaded(req: ThreadedRequest):
    thread_id = req.thread_id or str(uuid.uuid4())[:8]

    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(
        None,
        lambda: agent.invoke({
            "request": req.request, "category": "", "worker_output": "",
            "error": "", "final_response": "", "audit": [],
        })
    )

    conversation = {
        "thread_id": thread_id,
        "employee_name": req.employee_name,
        "request": req.request,
        "category": result["category"],
        "response": result["final_response"],
        "audit": result["audit"],
        "timestamp": datetime.now().isoformat(),
    }
    conversations[thread_id] = conversation
    return conversation

@app.get("/api/support/thread/{thread_id}")
async def get_thread(thread_id: str):
    if thread_id not in conversations:
        raise HTTPException(status_code=404, detail="Thread not found")
    return conversations[thread_id]

# --- Tests ---

client = TestClient(app)

print("\n--- Step 1 & 2: Agent Endpoints ---\n")

resp = client.get("/health")
print(f"  GET /health → {resp.json()}")

resp = client.post("/api/support", json={
    "employee_name": "Priya", "request": "I need sick leave"
})
data = resp.json()
print(f"  POST /api/support → {data['category']}")
print(f"  Response: {data['response'][:80]}...")

resp = client.post("/api/support/async", json={
    "employee_name": "Vikram", "request": "VPN disconnects"
})
data = resp.json()
print(f"  POST /api/support/async → {data['category']}")

print("\n--- TODO 1: Error Handling ---\n")

resp = client.post("/api/support/safe", json={
    "employee_name": "X", "request": "Hi"
})
print(f"  Too short → {resp.status_code} (expected 400)")

resp = client.post("/api/support/safe", json={
    "employee_name": "Priya", "request": "I need sick leave for next week"
})
print(f"  Valid → {resp.status_code}: {resp.json()['category']}")

print("\n--- TODO 2: Threading ---\n")

resp = client.post("/api/support/threaded", json={
    "employee_name": "Anita", "request": "Submit my expense report"
})
thread_id = resp.json()["thread_id"]
print(f"  Created thread: {thread_id}")

resp = client.get(f"/api/support/thread/{thread_id}")
print(f"  Retrieved thread: {resp.json()['employee_name']} → {resp.json()['category']}")

resp = client.get("/api/support/thread/FAKE-ID")
print(f"  Missing thread → {resp.status_code} (expected 404)")

print("\n" + "=" * 50)
print("Lab 02 Solution complete!")
print("- TODO 1: 400 for short requests, 503 for agent errors")
print("- TODO 2: Thread-based conversation storage and retrieval")
