"""
Lab 06: Integration & API Testing
=====================================
Goal: Test complete agent graphs and FastAPI endpoints using mocked LLMs.

What you'll learn:
- Integration test full LangGraph workflows
- Test FastAPI endpoints with TestClient
- Verify fallback chains under simulated failure
- Test validation error responses

No API key needed — all LLM calls are mocked.

Run with: python -m pytest lab06_integration_testing.py -v
Or just:  python lab06_integration_testing.py
"""

from typing import TypedDict, Annotated
from operator import add
from unittest.mock import MagicMock, patch
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

# ============================================================
# Build a complete agent system for testing
# ============================================================

llm = MagicMock()  # Module-level mock (will be configured per test)

class SupportState(TypedDict):
    request: str
    category: str
    worker_output: str
    error: str
    fallback_used: bool
    final_response: str
    audit: Annotated[list, add]

TEMPLATES = {
    "hr": "Please visit the HR portal or email hr@unigps.in.",
    "tech": "Please create a Jira ticket or contact IT at ext. 5555.",
    "finance": "Please email finance@unigps.in with details.",
    "general": "Your request has been noted. A team member will respond shortly.",
}

def supervisor_node(state: SupportState) -> dict:
    prompt = f"Classify: hr, tech, finance, general. One word.\n{state['request']}"
    try:
        response = llm.invoke(prompt)
        cat = response.content.strip().lower()
        if cat not in TEMPLATES:
            cat = "general"
    except Exception:
        cat = "general"
    return {"category": cat, "audit": [f"Classified: {cat}"]}

def worker_node(state: SupportState) -> dict:
    try:
        response = llm.invoke(f"Respond to: {state['request']}")
        return {"worker_output": response.content.strip(), "error": "",
                "fallback_used": False, "audit": [f"Worker responded"]}
    except Exception as e:
        return {"worker_output": "", "error": str(e),
                "fallback_used": False, "audit": [f"Worker error: {e}"]}

def route_after_worker(state: SupportState) -> str:
    return "fallback" if state["error"] else "finalize"

def fallback_node(state: SupportState) -> dict:
    template = TEMPLATES.get(state["category"], TEMPLATES["general"])
    return {"worker_output": template, "error": "", "fallback_used": True,
            "audit": [f"Fallback template: {state['category']}"]}

def finalize_node(state: SupportState) -> dict:
    ts = datetime.now().strftime("%H:%M:%S")
    return {"final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS | {ts}",
            "audit": [f"Done at {ts}"]}

# Build graph
from langgraph.graph import StateGraph, START, END

graph = StateGraph(SupportState)
graph.add_node("supervisor", supervisor_node)
graph.add_node("worker", worker_node)
graph.add_node("fallback", fallback_node)
graph.add_node("finalize", finalize_node)
graph.add_edge(START, "supervisor")
graph.add_edge("supervisor", "worker")
graph.add_conditional_edges("worker", route_after_worker, {
    "finalize": "finalize", "fallback": "fallback",
})
graph.add_edge("fallback", "finalize")
graph.add_edge("finalize", END)
agent = graph.compile()

# --- FastAPI App ---

app = FastAPI(title="UniGPS Agent API")

class AgentRequest(BaseModel):
    employee_name: str = Field(..., min_length=1)
    request: str = Field(..., min_length=5)

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/support")
async def handle_support(req: AgentRequest):
    result = agent.invoke({
        "request": req.request, "category": "", "worker_output": "",
        "error": "", "fallback_used": False, "final_response": "", "audit": [],
    })
    return {
        "category": result["category"],
        "response": result["final_response"],
        "fallback_used": result["fallback_used"],
        "audit": result["audit"],
    }

client = TestClient(app)


# ============================================================
# Step 1: Integration test — full graph with mocked LLM
# ============================================================

def setup_mock_llm(classify_as="hr", worker_response="Your leave is approved."):
    """Configure the mock LLM for a test."""
    responses = iter([
        MagicMock(content=classify_as),       # supervisor call
        MagicMock(content=worker_response),    # worker call
    ])
    llm.invoke.side_effect = lambda prompt: next(responses)


def test_full_graph_hr_flow():
    """Test complete HR flow through the graph."""
    setup_mock_llm(classify_as="hr", worker_response="Your leave is approved for 3 days.")

    result = agent.invoke({
        "request": "I need sick leave", "category": "", "worker_output": "",
        "error": "", "fallback_used": False, "final_response": "", "audit": [],
    })

    assert result["category"] == "hr"
    assert "leave is approved" in result["worker_output"].lower()
    assert "[HR]" in result["final_response"]
    assert result["fallback_used"] is False
    assert len(result["audit"]) >= 3  # supervisor + worker + finalize


def test_full_graph_tech_flow():
    """Test complete tech flow."""
    setup_mock_llm(classify_as="tech", worker_response="Jira ticket TECH-1234 created.")

    result = agent.invoke({
        "request": "Server is down", "category": "", "worker_output": "",
        "error": "", "fallback_used": False, "final_response": "", "audit": [],
    })

    assert result["category"] == "tech"
    assert "[TECH]" in result["final_response"]
    assert "Jira" in result["worker_output"]


def test_full_graph_audit_trail():
    """Verify audit trail tracks all steps."""
    setup_mock_llm(classify_as="finance", worker_response="Invoice processed.")

    result = agent.invoke({
        "request": "Submit invoice", "category": "", "worker_output": "",
        "error": "", "fallback_used": False, "final_response": "", "audit": [],
    })

    audit = result["audit"]
    assert any("Classified" in a for a in audit)
    assert any("Worker" in a or "responded" in a for a in audit)
    assert any("Done" in a for a in audit)


# ============================================================
# Step 2: Test FastAPI endpoints with TestClient
# ============================================================

def test_health_endpoint():
    """Health check should return 200."""
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "healthy"


def test_support_endpoint_success():
    """POST /api/support should return agent response."""
    setup_mock_llm(classify_as="hr", worker_response="Leave approved.")

    resp = client.post("/api/support", json={
        "employee_name": "Priya",
        "request": "I need sick leave",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["category"] == "hr"
    assert "response" in data
    assert "audit" in data


def test_validation_missing_field():
    """Missing required field should return 422."""
    resp = client.post("/api/support", json={"employee_name": "Priya"})
    assert resp.status_code == 422


def test_validation_short_request():
    """Too-short request should return 422."""
    resp = client.post("/api/support", json={
        "employee_name": "Priya",
        "request": "Hi",  # min_length=5
    })
    assert resp.status_code == 422


# ============================================================
# TODO 1: Test fallback chain under LLM failure
# ============================================================
# Simulate worker failure and verify the fallback path works.
#
# Hint:
#   def test_fallback_on_worker_failure():
#       """When worker LLM fails, fallback template should be used."""
#       # First call (supervisor) succeeds, second call (worker) fails
#       call_count = [0]
#       def mock_invoke(prompt):
#           call_count[0] += 1
#           if call_count[0] == 1:
#               return MagicMock(content="tech")  # supervisor classifies
#           else:
#               raise Exception("LLM API timeout")  # worker fails
#       llm.invoke.side_effect = mock_invoke
#
#       result = agent.invoke({
#           "request": "Server is down", "category": "", "worker_output": "",
#           "error": "", "fallback_used": False, "final_response": "", "audit": [],
#       })
#
#       assert result["fallback_used"] is True
#       assert result["worker_output"] == TEMPLATES["tech"]
#       assert "[TECH]" in result["final_response"]
#       assert result["final_response"]  # Should still have a response!
#
#   def test_fallback_preserves_category():
#       """Fallback should use the correct category template."""
#       for cat in ["hr", "tech", "finance"]:
#           call_count = [0]
#           def mock_invoke(prompt, c=cat):
#               call_count[0] += 1
#               if call_count[0] == 1:
#                   return MagicMock(content=c)
#               raise Exception("fail")
#           llm.invoke.side_effect = mock_invoke
#
#           result = agent.invoke({
#               "request": "test", "category": "", "worker_output": "",
#               "error": "", "fallback_used": False, "final_response": "", "audit": [],
#           })
#           assert result["worker_output"] == TEMPLATES[cat]


# ============================================================
# TODO 2: Test API error responses
# ============================================================
# Test that the API handles various error scenarios correctly.
#
# Hint:
#   def test_api_returns_fallback_info():
#       """API response should indicate when fallback was used."""
#       call_count = [0]
#       def mock_invoke(prompt):
#           call_count[0] += 1
#           if call_count[0] == 1:
#               return MagicMock(content="general")
#           raise Exception("fail")
#       llm.invoke.side_effect = mock_invoke
#
#       resp = client.post("/api/support", json={
#           "employee_name": "Test",
#           "request": "Random question here",
#       })
#       assert resp.status_code == 200
#       data = resp.json()
#       assert data["fallback_used"] is True
#
#   def test_api_empty_name():
#       """Empty employee name should fail validation."""
#       resp = client.post("/api/support", json={
#           "employee_name": "",
#           "request": "I need help with something",
#       })
#       assert resp.status_code == 422
#
#   def test_api_invalid_json():
#       """Non-JSON body should return 422."""
#       resp = client.post("/api/support", content="not json",
#                          headers={"Content-Type": "application/json"})
#       assert resp.status_code == 422


# ============================================================
# Run tests when executed directly
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  Integration & API Testing")
    print("=" * 50)

    test_functions = [
        (name, obj) for name, obj in globals().items()
        if name.startswith("test_") and callable(obj)
    ]

    passed = 0
    failed = 0
    for name, func in sorted(test_functions):
        try:
            func()
            print(f"  PASS  {name}")
            passed += 1
        except AssertionError as e:
            print(f"  FAIL  {name}: {e}")
            failed += 1
        except Exception as e:
            print(f"  ERROR {name}: {e}")
            failed += 1

    print(f"\n  Results: {passed} passed, {failed} failed, {passed + failed} total")
    print("\n" + "=" * 50)
    print("Lab 06 complete!")
    print("Patterns: integration testing, TestClient, fallback validation, error scenarios")
