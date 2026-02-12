"""
Lab 03 Solution: Streaming Responses
=======================================
"""

import os
import json
import time
from typing import TypedDict, Annotated
from operator import add
from datetime import datetime
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.testclient import TestClient
from pydantic import BaseModel
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

load_dotenv()

print("=" * 50)
print("  Streaming Responses (Solution)")
print("=" * 50)

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

class AgentState(TypedDict):
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

def supervisor(state: AgentState) -> dict:
    prompt = f"Classify as: hr, tech, finance, general. One word.\n{state['request']}"
    try:
        response = llm.invoke(prompt)
        cat = response.content.strip().lower()
        if cat not in TEMPLATES:
            cat = "general"
    except Exception:
        cat = "general"
    return {"category": cat, "audit": [f"Classified: {cat}"]}

def worker(state: AgentState) -> dict:
    prompt = f"You are UniGPS {state['category']} support.\n{state['request']}\nReply in 2 sentences."
    try:
        response = llm.invoke(prompt)
        return {"worker_output": response.content.strip(), "audit": ["Worker responded"]}
    except Exception:
        return {"worker_output": TEMPLATES[state["category"]], "audit": ["Used template"]}

def finalize(state: AgentState) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    return {"final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS | {ts}",
            "audit": [f"Done at {ts}"]}

graph = StateGraph(AgentState)
graph.add_node("supervisor", supervisor)
graph.add_node("worker", worker)
graph.add_node("finalize", finalize)
graph.add_edge(START, "supervisor")
graph.add_edge("supervisor", "worker")
graph.add_edge("worker", "finalize")
graph.add_edge("finalize", END)
agent = graph.compile()

# --- FastAPI ---

app = FastAPI(title="UniGPS Streaming API")

class StreamRequest(BaseModel):
    employee_name: str
    request: str

# Step 1: Basic SSE streaming
def stream_agent_events(request_text: str):
    init_state = {
        "request": request_text, "category": "", "worker_output": "",
        "error": "", "final_response": "", "audit": [],
    }
    for event in agent.stream(init_state):
        for node_name, output in event.items():
            sse_data = json.dumps({"node": node_name, "output": output})
            yield f"data: {sse_data}\n\n"
    yield "data: [DONE]\n\n"

@app.post("/api/support/stream")
async def stream_support(req: StreamRequest):
    return StreamingResponse(
        stream_agent_events(req.request),
        media_type="text/event-stream",
    )

# Step 2: Progress events
def stream_with_progress(request_text: str, employee_name: str):
    steps = ["supervisor", "worker", "finalize"]
    yield f"data: {json.dumps({'type': 'progress', 'step': 0, 'total': len(steps), 'message': 'Starting...'})}\n\n"

    init_state = {
        "request": request_text, "category": "", "worker_output": "",
        "error": "", "final_response": "", "audit": [],
    }
    step_idx = 0
    for event in agent.stream(init_state):
        for node_name, output in event.items():
            step_idx += 1
            yield f"data: {json.dumps({'type': 'progress', 'step': step_idx, 'total': len(steps), 'message': f'Running {node_name}...'})}\n\n"
            yield f"data: {json.dumps({'type': 'data', 'node': node_name, 'output': output})}\n\n"

    yield f"data: {json.dumps({'type': 'done', 'message': 'Complete'})}\n\n"

@app.post("/api/support/stream/v2")
async def stream_with_progress_endpoint(req: StreamRequest):
    return StreamingResponse(
        stream_with_progress(req.request, req.employee_name),
        media_type="text/event-stream",
    )

# ============================================================
# TODO 1 Solution: Batch fallback endpoint
# ============================================================

@app.post("/api/support/batch")
async def batch_support(req: StreamRequest):
    """Non-streaming endpoint with timing info."""
    start = time.time()
    result = agent.invoke({
        "request": req.request, "category": "", "worker_output": "",
        "error": "", "final_response": "", "audit": [],
    })
    elapsed = time.time() - start
    return {
        "employee_name": req.employee_name,
        "category": result["category"],
        "response": result["final_response"],
        "audit": result["audit"],
        "timing": {"total_seconds": round(elapsed, 2)},
    }

# ============================================================
# TODO 2 Solution: Typed event streaming
# ============================================================

def stream_typed_events(request_text: str, employee_name: str):
    """Rich streaming protocol with typed events."""
    yield f"data: {json.dumps({'event': 'start', 'employee': employee_name, 'request': request_text})}\n\n"

    init_state = {
        "request": request_text, "category": "", "worker_output": "",
        "error": "", "final_response": "", "audit": [],
    }

    try:
        for event in agent.stream(init_state):
            for node_name, output in event.items():
                if node_name == "supervisor":
                    yield f"data: {json.dumps({'event': 'classification', 'category': output.get('category', '')})}\n\n"
                elif node_name == "worker":
                    yield f"data: {json.dumps({'event': 'response', 'text': output.get('worker_output', '')})}\n\n"
                elif node_name == "finalize":
                    yield f"data: {json.dumps({'event': 'metadata', 'response': output.get('final_response', ''), 'audit': output.get('audit', [])})}\n\n"
    except Exception as e:
        yield f"data: {json.dumps({'event': 'error', 'message': str(e)})}\n\n"

    yield f"data: {json.dumps({'event': 'done'})}\n\n"

@app.post("/api/support/stream/v3")
async def stream_typed(req: StreamRequest):
    return StreamingResponse(
        stream_typed_events(req.request, req.employee_name),
        media_type="text/event-stream",
    )

# --- Tests ---

client = TestClient(app)

print("\n--- Step 1: Basic SSE Streaming ---\n")

with client.stream("POST", "/api/support/stream",
                    json={"employee_name": "Priya", "request": "I need sick leave"}) as resp:
    print("  Streaming events:")
    for line in resp.iter_lines():
        if line.startswith("data: ") and line != "data: [DONE]":
            data = json.loads(line[6:])
            print(f"    [{data['node']}] → {list(data['output'].keys())}")
        elif line == "data: [DONE]":
            print("    [DONE]")

print("\n--- Step 2: Progress Events ---\n")

with client.stream("POST", "/api/support/stream/v2",
                    json={"employee_name": "Vikram", "request": "Server is slow"}) as resp:
    for line in resp.iter_lines():
        if line.startswith("data: "):
            data = json.loads(line[6:])
            if data.get("type") == "progress":
                print(f"    Progress: {data['step']}/{data['total']} — {data['message']}")
            elif data.get("type") == "done":
                print(f"    Done!")

print("\n--- TODO 1: Batch Endpoint ---\n")

resp = client.post("/api/support/batch", json={
    "employee_name": "Anita", "request": "Submit expense report"
})
data = resp.json()
print(f"  Batch: {data['category']} in {data['timing']['total_seconds']}s")

print("\n--- TODO 2: Typed Events ---\n")

with client.stream("POST", "/api/support/stream/v3",
                    json={"employee_name": "Rahul", "request": "Where is my salary?"}) as resp:
    for line in resp.iter_lines():
        if line.startswith("data: "):
            data = json.loads(line[6:])
            event_type = data.get("event", "unknown")
            if event_type == "start":
                print(f"    [start] {data['employee']}: {data['request']}")
            elif event_type == "classification":
                print(f"    [classification] → {data['category']}")
            elif event_type == "response":
                print(f"    [response] {data['text'][:60]}...")
            elif event_type == "metadata":
                print(f"    [metadata] audit: {len(data['audit'])} entries")
            elif event_type == "done":
                print(f"    [done]")

print("\n" + "=" * 50)
print("Lab 03 Solution complete!")
print("- TODO 1: Batch endpoint with timing (non-streaming fallback)")
print("- TODO 2: Typed events (start, classification, response, metadata, done)")
