"""
Lab 03: Streaming Responses
==============================
Goal: Build FastAPI endpoints that stream agent responses in real-time
      using Server-Sent Events (SSE).

What you'll learn:
- StreamingResponse with text/event-stream
- Streaming LangGraph state updates per node
- Progress events for multi-step agent workflows

Needs: GROQ_API_KEY in .env
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
print("  Streaming Responses")
print("=" * 50)

# ============================================================
# Step 1: Basic SSE streaming from LangGraph
# ============================================================

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
        if cat not in ["hr", "tech", "finance", "general"]:
            cat = "general"
    except Exception:
        cat = "general"
    return {"category": cat, "audit": [f"Classified: {cat}"]}

def worker(state: AgentState) -> dict:
    prompt = (
        f"You are UniGPS {state['category']} support.\n"
        f"Request: {state['request']}\nReply in 2 sentences."
    )
    try:
        response = llm.invoke(prompt)
        return {"worker_output": response.content.strip(),
                "audit": [f"Worker responded"]}
    except Exception:
        return {"worker_output": TEMPLATES[state["category"]],
                "audit": ["Used template fallback"]}

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

# --- FastAPI with Streaming ---

app = FastAPI(title="UniGPS Streaming API")

class StreamRequest(BaseModel):
    employee_name: str
    request: str

def stream_agent_events(request_text: str):
    """Generator that yields SSE events from LangGraph stream."""
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
    """Stream agent node outputs as SSE events."""
    return StreamingResponse(
        stream_agent_events(req.request),
        media_type="text/event-stream",
    )

# --- Test streaming ---

client = TestClient(app)

print("\n--- Step 1: Basic SSE Streaming ---\n")

with client.stream("POST", "/api/support/stream",
                    json={"employee_name": "Priya", "request": "I need sick leave"}) as resp:
    print("  Streaming events:")
    for line in resp.iter_lines():
        if line.startswith("data: ") and line != "data: [DONE]":
            data = json.loads(line[6:])
            node = data["node"]
            # Show a summary of each node's output
            keys = list(data["output"].keys())
            print(f"    [{node}] → keys: {keys}")
        elif line == "data: [DONE]":
            print("    [DONE] Stream complete")


# ============================================================
# Step 2: Streaming with progress events
# ============================================================

print("\n\n--- Step 2: Progress Events ---\n")

def stream_with_progress(request_text: str, employee_name: str):
    """Yield progress + data events."""
    steps = ["supervisor", "worker", "finalize"]

    # Send initial progress
    yield f"data: {json.dumps({'type': 'progress', 'step': 0, 'total': len(steps), 'message': 'Starting...'})}\n\n"

    init_state = {
        "request": request_text, "category": "", "worker_output": "",
        "error": "", "final_response": "", "audit": [],
    }

    step_idx = 0
    for event in agent.stream(init_state):
        for node_name, output in event.items():
            step_idx += 1
            # Progress event
            yield f"data: {json.dumps({'type': 'progress', 'step': step_idx, 'total': len(steps), 'message': f'Running {node_name}...'})}\n\n"
            # Data event
            yield f"data: {json.dumps({'type': 'data', 'node': node_name, 'output': output})}\n\n"

    yield f"data: {json.dumps({'type': 'done', 'message': 'Complete'})}\n\n"

@app.post("/api/support/stream/v2")
async def stream_with_progress_endpoint(req: StreamRequest):
    return StreamingResponse(
        stream_with_progress(req.request, req.employee_name),
        media_type="text/event-stream",
    )

with client.stream("POST", "/api/support/stream/v2",
                    json={"employee_name": "Vikram", "request": "Server is slow"}) as resp:
    print("  Streaming with progress:")
    for line in resp.iter_lines():
        if line.startswith("data: "):
            data = json.loads(line[6:])
            if data.get("type") == "progress":
                print(f"    Progress: {data['step']}/{data['total']} — {data['message']}")
            elif data.get("type") == "data":
                print(f"    Data: [{data['node']}] → {list(data['output'].keys())}")
            elif data.get("type") == "done":
                print(f"    Done: {data['message']}")


# ============================================================
# TODO 1: Add a non-streaming fallback endpoint
# ============================================================
# Some clients can't handle SSE. Create an endpoint that uses the same
# agent but returns a single JSON response with timing info.
#
# Hint:
#   @app.post("/api/support/batch")
#   async def batch_support(req: StreamRequest):
#       import time
#       start = time.time()
#       result = agent.invoke({
#           "request": req.request, "category": "", "worker_output": "",
#           "error": "", "final_response": "", "audit": [],
#       })
#       elapsed = time.time() - start
#       return {
#           "category": result["category"],
#           "response": result["final_response"],
#           "audit": result["audit"],
#           "timing": {"total_seconds": round(elapsed, 2)},
#       }
#
# Test: POST to /api/support/batch and verify timing is included


# ============================================================
# TODO 2: Stream with typed event categories
# ============================================================
# Create a richer streaming protocol with event types:
# - "start": initial event with request info
# - "classification": supervisor result with category
# - "response": worker output (the actual answer)
# - "metadata": finalize info (timestamp, audit)
# - "error": if anything fails
# - "done": stream complete
#
# Hint:
#   def stream_typed_events(request_text: str, employee_name: str):
#       yield f"data: {json.dumps({'event': 'start', 'employee': employee_name, 'request': request_text})}\n\n"
#
#       init_state = {...}
#       for event in agent.stream(init_state):
#           for node_name, output in event.items():
#               if node_name == "supervisor":
#                   yield f"data: {json.dumps({'event': 'classification', 'category': output.get('category', '')})}\n\n"
#               elif node_name == "worker":
#                   yield f"data: {json.dumps({'event': 'response', 'text': output.get('worker_output', '')})}\n\n"
#               elif node_name == "finalize":
#                   yield f"data: {json.dumps({'event': 'metadata', 'response': output.get('final_response', ''), 'audit': output.get('audit', [])})}\n\n"
#
#       yield f"data: {json.dumps({'event': 'done'})}\n\n"
#
# Test: Verify each event type appears in order


print("\n" + "=" * 50)
print("Lab 03 complete!")
print("Patterns: SSE streaming, progress events, real-time agent output")
