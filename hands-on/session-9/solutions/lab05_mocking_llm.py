"""
Lab 05 Solution: Mocking LLM Calls
=====================================
"""

from typing import TypedDict, Annotated
from operator import add
from unittest.mock import MagicMock

# ============================================================
# Agent code under test
# ============================================================

llm = None

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
        if cat not in ["hr", "tech", "finance", "general"]:
            cat = "general"
    except Exception as e:
        cat = "general"
        return {"category": cat, "error": str(e),
                "audit": [f"Supervisor error: {e}"]}
    return {"category": cat, "error": "",
            "audit": [f"Classified: {cat}"]}

def worker(state: SupportState) -> dict:
    prompt = (
        f"You are UniGPS {state['category']} support.\n"
        f"Request: {state['request']}\nReply in 2 sentences."
    )
    try:
        response = llm.invoke(prompt)
        return {"worker_output": response.content.strip(), "error": "",
                "audit": [f"Worker ({state['category']}) responded"]}
    except Exception as e:
        fallback = TEMPLATES.get(state["category"], TEMPLATES["general"])
        return {"worker_output": fallback, "error": str(e),
                "audit": [f"Worker error, used template"]}


# ============================================================
# Step 1: Mock LLM in a single node
# ============================================================

def test_supervisor_classifies_as_hr():
    global llm
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "hr"
    mock_llm.invoke.return_value = mock_response
    llm = mock_llm

    state = {"request": "I need sick leave", "category": "", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = supervisor(state)

    assert result["category"] == "hr"
    assert result["error"] == ""
    mock_llm.invoke.assert_called_once()
    llm = None

def test_supervisor_classifies_as_tech():
    global llm
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "tech"
    mock_llm.invoke.return_value = mock_response
    llm = mock_llm

    state = {"request": "Server is down", "category": "", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = supervisor(state)
    assert result["category"] == "tech"
    llm = None

def test_supervisor_handles_invalid_category():
    global llm
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "something_random"
    mock_llm.invoke.return_value = mock_response
    llm = mock_llm

    state = {"request": "Unclear request", "category": "", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = supervisor(state)
    assert result["category"] == "general"
    llm = None


# ============================================================
# Step 2: Simulate LLM failure
# ============================================================

def test_supervisor_handles_llm_failure():
    global llm
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("API timeout")
    llm = mock_llm

    state = {"request": "Any question", "category": "", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = supervisor(state)
    assert result["category"] == "general"
    assert "timeout" in result["error"].lower()
    llm = None

def test_worker_uses_template_on_failure():
    global llm
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("Rate limit exceeded")
    llm = mock_llm

    state = {"request": "I need leave", "category": "hr", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = worker(state)
    assert result["worker_output"] == TEMPLATES["hr"]
    assert result["error"]
    llm = None

def test_worker_produces_output():
    global llm
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Your leave has been approved for 3 days starting Monday."
    mock_llm.invoke.return_value = mock_response
    llm = mock_llm

    state = {"request": "I need 3 days leave", "category": "hr", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = worker(state)
    assert "leave" in result["worker_output"].lower()
    assert result["error"] == ""
    llm = None


# ============================================================
# TODO 1 Solution: Test all categories
# ============================================================

def test_supervisor_all_categories():
    """Test that supervisor correctly handles all valid categories."""
    global llm
    for expected_cat in ["hr", "tech", "finance", "general"]:
        mock_llm = MagicMock()
        mock_response = MagicMock()
        mock_response.content = expected_cat
        mock_llm.invoke.return_value = mock_response
        llm = mock_llm

        state = {"request": "test", "category": "", "worker_output": "",
                 "error": "", "final_response": "", "audit": []}
        result = supervisor(state)
        assert result["category"] == expected_cat, f"Expected {expected_cat}, got {result['category']}"

    llm = None

def test_supervisor_prompt_contains_request():
    """Verify the supervisor sends the user's request to the LLM."""
    global llm
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "hr"
    mock_llm.invoke.return_value = mock_response
    llm = mock_llm

    state = {"request": "I need sick leave", "category": "", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    supervisor(state)

    call_args = mock_llm.invoke.call_args[0][0]
    assert "sick leave" in call_args.lower()
    llm = None

def test_supervisor_strips_whitespace():
    """LLM response with whitespace should still classify correctly."""
    global llm
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "  hr  \n"
    mock_llm.invoke.return_value = mock_response
    llm = mock_llm

    state = {"request": "test", "category": "", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = supervisor(state)
    assert result["category"] == "hr"
    llm = None

def test_supervisor_handles_uppercase():
    """LLM response in uppercase should still classify correctly."""
    global llm
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "TECH"
    mock_llm.invoke.return_value = mock_response
    llm = mock_llm

    state = {"request": "test", "category": "", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = supervisor(state)
    assert result["category"] == "tech"
    llm = None


# ============================================================
# TODO 2 Solution: Worker mock scenarios
# ============================================================

def test_worker_audit_trail():
    """Worker should add audit entries."""
    global llm
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "We will fix the server."
    mock_llm.invoke.return_value = mock_response
    llm = mock_llm

    state = {"request": "Server down", "category": "tech", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = worker(state)
    assert len(result["audit"]) == 1
    assert "tech" in result["audit"][0].lower()
    llm = None

def test_worker_fallback_per_category():
    """Each category should have its own fallback template."""
    global llm
    for cat in ["hr", "tech", "finance", "general"]:
        mock_llm = MagicMock()
        mock_llm.invoke.side_effect = Exception("fail")
        llm = mock_llm

        state = {"request": "test", "category": cat, "worker_output": "",
                 "error": "", "final_response": "", "audit": []}
        result = worker(state)
        assert result["worker_output"] == TEMPLATES[cat]
    llm = None

def test_worker_error_message_recorded():
    """Worker should record the specific error message."""
    global llm
    mock_llm = MagicMock()
    mock_llm.invoke.side_effect = Exception("Connection refused")
    llm = mock_llm

    state = {"request": "test", "category": "hr", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    result = worker(state)
    assert "Connection refused" in result["error"]
    llm = None

def test_worker_prompt_includes_category():
    """Worker prompt should include the assigned category."""
    global llm
    mock_llm = MagicMock()
    mock_response = MagicMock()
    mock_response.content = "Response text"
    mock_llm.invoke.return_value = mock_response
    llm = mock_llm

    state = {"request": "test", "category": "finance", "worker_output": "",
             "error": "", "final_response": "", "audit": []}
    worker(state)

    call_args = mock_llm.invoke.call_args[0][0]
    assert "finance" in call_args.lower()
    llm = None


# ============================================================
# Run tests
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  Mocking LLM Calls (Solution)")
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
    print("Lab 05 Solution complete!")
    print("- TODO 1: All categories, prompt verification, whitespace/uppercase handling")
    print("- TODO 2: Audit trail, per-category fallback, error recording, prompt content")
