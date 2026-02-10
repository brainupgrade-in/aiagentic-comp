"""
Lab 04: Unit Testing Agent Nodes
===================================
Goal: Test individual agent nodes, routing functions, and formatters
      without making any LLM calls.

What you'll learn:
- Testing pure routing functions directly
- Testing formatter and finalize nodes
- Testing state validators
- Running tests with pytest

No API key needed — all tests use deterministic logic.

Run with: python -m pytest lab04_unit_testing.py -v
Or just:  python lab04_unit_testing.py
"""

from typing import TypedDict, Annotated
from operator import add
from datetime import datetime

# ============================================================
# The agent code we're testing (no LLM needed)
# ============================================================

class SupportState(TypedDict):
    request: str
    category: str
    assigned_to: str
    worker_output: str
    error: str
    quality_ok: bool
    final_response: str
    audit: Annotated[list, add]


def classify_request(text: str) -> str:
    """Keyword-based request classification."""
    msg = text.lower()
    if any(w in msg for w in ["leave", "sick", "wfh", "policy", "hr"]):
        return "hr"
    elif any(w in msg for w in ["server", "bug", "deploy", "laptop", "vpn"]):
        return "tech"
    elif any(w in msg for w in ["expense", "salary", "invoice", "budget"]):
        return "finance"
    return "general"


def route_to_worker(state: SupportState) -> str:
    """Returns the name of the worker node to route to."""
    return state["assigned_to"]


def finalize(state: SupportState) -> dict:
    """Format the final response."""
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return {
        "final_response": f"[{state['category'].upper()}] {state['worker_output']}\n— UniGPS | {ts}",
        "audit": [f"Finalized at {ts}"],
    }


def quality_check(state: SupportState) -> dict:
    """Check if worker output meets quality standards."""
    output = state["worker_output"]
    errors = []
    if len(output) < 20:
        errors.append("Response too short (min 20 chars)")
    if not output.strip():
        errors.append("Response is empty")
    ok = len(errors) == 0
    return {
        "quality_ok": ok,
        "error": "; ".join(errors) if errors else "",
        "audit": [f"Quality: {'PASS' if ok else 'FAIL'}"],
    }


def route_after_quality(state: SupportState) -> str:
    """Route based on quality check result."""
    return "finalize" if state["quality_ok"] else "fallback"


# ============================================================
# Step 1: Test routing functions
# ============================================================

def test_classify_hr_requests():
    """HR keywords should classify as 'hr'."""
    assert classify_request("I need sick leave") == "hr"
    assert classify_request("What is the WFH policy?") == "hr"
    assert classify_request("HR question about benefits") == "hr"


def test_classify_tech_requests():
    """Tech keywords should classify as 'tech'."""
    assert classify_request("The server is down") == "tech"
    assert classify_request("Found a bug in production") == "tech"
    assert classify_request("My laptop won't start") == "tech"


def test_classify_finance_requests():
    """Finance keywords should classify as 'finance'."""
    assert classify_request("Submit expense report") == "finance"
    assert classify_request("When is my salary due?") == "finance"
    assert classify_request("Need to pay an invoice") == "finance"


def test_classify_general_fallback():
    """Unknown requests should classify as 'general'."""
    assert classify_request("Where is the cafeteria?") == "general"
    assert classify_request("Hello world") == "general"
    assert classify_request("Random question") == "general"


def test_route_to_worker():
    """Route function should return the assigned_to value."""
    assert route_to_worker({"assigned_to": "hr"}) == "hr"
    assert route_to_worker({"assigned_to": "tech"}) == "tech"
    assert route_to_worker({"assigned_to": "general"}) == "general"


# ============================================================
# Step 2: Test formatter and quality check
# ============================================================

def test_finalize_includes_category():
    """Finalize should include the uppercase category."""
    state = {
        "category": "tech",
        "worker_output": "Your Jira ticket has been created",
    }
    result = finalize(state)
    assert "[TECH]" in result["final_response"]
    assert "UniGPS" in result["final_response"]


def test_finalize_includes_worker_output():
    """Finalize should include the worker's response."""
    state = {
        "category": "hr",
        "worker_output": "Your leave request has been processed",
    }
    result = finalize(state)
    assert "leave request has been processed" in result["final_response"]


def test_quality_check_pass():
    """Long enough output should pass quality check."""
    state = {"worker_output": "This is a detailed response that meets the minimum length requirement."}
    result = quality_check(state)
    assert result["quality_ok"] is True
    assert result["error"] == ""


def test_quality_check_fail_short():
    """Too-short output should fail quality check."""
    state = {"worker_output": "OK"}
    result = quality_check(state)
    assert result["quality_ok"] is False
    assert "too short" in result["error"].lower()


def test_quality_check_fail_empty():
    """Empty output should fail quality check."""
    state = {"worker_output": ""}
    result = quality_check(state)
    assert result["quality_ok"] is False


def test_route_after_quality_pass():
    """Quality pass should route to finalize."""
    assert route_after_quality({"quality_ok": True}) == "finalize"


def test_route_after_quality_fail():
    """Quality fail should route to fallback."""
    assert route_after_quality({"quality_ok": False}) == "fallback"


# ============================================================
# TODO 1: Test classify_request with edge cases
# ============================================================
# Write tests for tricky inputs that might break classification.
#
# Hint:
#   def test_classify_case_insensitive():
#       """Classification should be case-insensitive."""
#       assert classify_request("SICK LEAVE PLEASE") == "hr"
#       assert classify_request("SERVER DOWN") == "tech"
#
#   def test_classify_empty_string():
#       """Empty string should classify as 'general'."""
#       assert classify_request("") == "general"
#
#   def test_classify_multiple_keywords():
#       """When multiple keywords match, first match wins."""
#       # "leave" and "server" both present — "leave" (hr) appears first in checks
#       result = classify_request("I need leave but also the server is down")
#       assert result in ["hr", "tech"]  # depends on check order
#
#   def test_classify_special_characters():
#       """Should handle special characters gracefully."""
#       assert classify_request("???") == "general"
#       assert classify_request("!!!sick!!!") == "hr"


# ============================================================
# TODO 2: Test finalize with various state combinations
# ============================================================
# Write tests for edge cases in the finalize function.
#
# Hint:
#   def test_finalize_adds_audit():
#       """Finalize should add an audit entry."""
#       state = {"category": "general", "worker_output": "Response here"}
#       result = finalize(state)
#       assert len(result["audit"]) == 1
#       assert "Finalized" in result["audit"][0]
#
#   def test_finalize_timestamp_format():
#       """Finalize should include a timestamp in the response."""
#       state = {"category": "hr", "worker_output": "Done"}
#       result = finalize(state)
#       # Should contain date pattern like 2024-01-15
#       import re
#       assert re.search(r"\d{4}-\d{2}-\d{2}", result["final_response"])
#
#   def test_finalize_all_categories():
#       """Test finalize with each category."""
#       for cat in ["hr", "tech", "finance", "general"]:
#           state = {"category": cat, "worker_output": "Test output"}
#           result = finalize(state)
#           assert f"[{cat.upper()}]" in result["final_response"]


# ============================================================
# Run tests when executed directly
# ============================================================

if __name__ == "__main__":
    print("=" * 50)
    print("  Unit Testing Agent Nodes")
    print("=" * 50)

    # Collect and run all test functions
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
    print("Lab 04 complete!")
    print("Patterns: pure function testing, routing, formatting, quality checks")
