"""
Lab 04 Solution: Code Review Agent State Design

Learn to design the state structure and node/edge plan for a code
review agent, following the LangGraph StateGraph pattern using plain
Python dicts (no external dependencies).

Key concepts:
- TypedDict-style state schema design
- Node functions that transform state
- Conditional edge routing based on state values

Uses only Python standard library (json, os, textwrap).
"""

import json
import os
import shutil
import textwrap

WORKDIR = "/tmp/aidev-lab-12-04"

# ── Cleanup and Setup ──────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ── Step 1: TypedDict Pattern for Graph State ─────────────────────
print("=" * 70)
print("STEP 1: State Design Pattern (TypedDict-Style)")
print("=" * 70)

print("""
In LangGraph, agents use a TypedDict to define their state schema.
Here we simulate this with plain dicts and a schema validator.

  LangGraph pattern:
  ┌──────────────────────────────────────────────────────────────────┐
  │ from typing import TypedDict, List                             │
  │                                                                │
  │ class ReviewState(TypedDict):                                  │
  │     diff: str              # The code diff to review           │
  │     file_analyses: list    # Per-file analysis results         │
  │     test_results: str      # Test execution output             │
  │     issues: list           # Detected issues                   │
  │     review_summary: str    # Final review text                 │
  │     severity: str          # "approve" | "request_changes"     │
  └──────────────────────────────────────────────────────────────────┘

  Our simulation approach:
  - Define the schema as a dict of field_name -> (type, default_value)
  - Validate states against the schema
  - Node functions receive state dict and return updated state dict
""")

# ── Step 2: Node and Edge Concepts ────────────────────────────────
print("=" * 70)
print("STEP 2: Nodes and Edges in a Review Graph")
print("=" * 70)

print("""
A review workflow graph has:

  Nodes (functions that transform state):
  ┌──────────────────────┬──────────────────────────────────────────┐
  │ Node                 │ Responsibility                           │
  ├──────────────────────┼──────────────────────────────────────────┤
  │ analyze_node         │ Parse diff, analyze code structure       │
  │ test_node            │ Run / simulate tests on the diff         │
  │ review_node          │ Synthesize findings into a review        │
  │ suggest_fixes_node   │ Generate fix suggestions (if needed)     │
  └──────────────────────┴──────────────────────────────────────────┘

  Edges (transitions between nodes):
  ┌──────────────────────┬──────────────────────────────────────────┐
  │ Edge                 │ Condition                                │
  ├──────────────────────┼──────────────────────────────────────────┤
  │ analyze → test       │ Always (sequential)                      │
  │ test → review        │ Always (sequential)                      │
  │ review → suggest     │ If severity == "request_changes"         │
  │ review → done        │ If severity == "approve"                 │
  └──────────────────────┴──────────────────────────────────────────┘
""")

# ── Sample diff for testing ───────────────────────────────────────

SAMPLE_DIFF = textwrap.dedent("""\
    --- a/app/api.py
    +++ b/app/api.py
    @@ -10,6 +10,15 @@
     from fastapi import FastAPI
    +import os
    +
    +def get_db_password():
    +    return os.environ.get("DB_PASSWORD", "admin123")
    +
    +def process_data(data):
    +    result = eval(data["expression"])
    +    return {"result": result}
    +
     app = FastAPI()
""")


# ── TODO 1: Define ReviewState Schema ─────────────────────────────
print("=" * 70)
print("TODO 1: Define ReviewState schema and create_state/validate_state")
print("=" * 70)

print("""
Define the schema for a code review state.

  REVIEW_STATE_SCHEMA should be a dict mapping field names to their
  default values:
    {
        "diff": "",
        "file_analyses": [],
        "test_results": "",
        "issues": [],
        "review_summary": "",
        "severity": "pending"
    }

  create_state(diff) should return a new state dict initialized with
  the schema defaults and the given diff.

  validate_state(state) should return True if all schema keys are present
  and each value is the correct type (str for str defaults, list for list
  defaults).
""")

REVIEW_STATE_SCHEMA = {
    "diff": "",
    "file_analyses": [],
    "test_results": "",
    "issues": [],
    "review_summary": "",
    "severity": "pending",
}


def create_state(diff: str) -> dict:
    """Create a new review state initialized with defaults."""
    state = {}
    for key, default in REVIEW_STATE_SCHEMA.items():
        if isinstance(default, list):
            state[key] = list(default)  # New list copy
        else:
            state[key] = default
    state["diff"] = diff
    return state


def validate_state(state: dict) -> bool:
    """Validate that state has all required fields with correct types."""
    for key, default in REVIEW_STATE_SCHEMA.items():
        if key not in state:
            return False
        if isinstance(default, str) and not isinstance(state[key], str):
            return False
        if isinstance(default, list) and not isinstance(state[key], list):
            return False
    return True


# Validate TODO 1
total += 1
try:
    if isinstance(REVIEW_STATE_SCHEMA, dict) and len(REVIEW_STATE_SCHEMA) == 6:
        print(f"  [PASS] REVIEW_STATE_SCHEMA has 6 fields")
        score += 1
    else:
        print(f"  [FAIL] Expected 6-field dict, got: {REVIEW_STATE_SCHEMA}")
except Exception as e:
    print(f"  [FAIL] REVIEW_STATE_SCHEMA error: {e}")

total += 1
try:
    state = create_state("test diff")
    if isinstance(state, dict) and state.get("diff") == "test diff" and state.get("severity") == "pending":
        print(f"  [PASS] create_state returns valid state with diff and defaults")
        score += 1
    else:
        print(f"  [FAIL] create_state returned: {state}")
except Exception as e:
    print(f"  [FAIL] create_state raised: {e}")

total += 1
try:
    state = create_state("x")
    valid = validate_state(state)
    if valid is True:
        print(f"  [PASS] validate_state accepts valid state")
        score += 1
    else:
        print(f"  [FAIL] validate_state returned {valid} for valid state")
except Exception as e:
    print(f"  [FAIL] validate_state raised: {e}")

total += 1
try:
    bad_state = {"diff": "x"}  # Missing fields
    valid = validate_state(bad_state)
    if valid is False:
        print(f"  [PASS] validate_state rejects incomplete state")
        score += 1
    else:
        print(f"  [FAIL] validate_state should reject incomplete state")
except Exception as e:
    print(f"  [FAIL] validate_state raised: {e}")


# ── TODO 2: Node Functions ────────────────────────────────────────
print()
print("=" * 70)
print("TODO 2: Implement analyze_node and test_node")
print("=" * 70)

print("""
Node functions receive the state dict and return an updated copy.

  analyze_node(state):
    - Read state["diff"]
    - Look for security issues in the diff text:
      * "eval(" -> issue: "dangerous_eval"
      * "exec(" -> issue: "dangerous_exec"
      * "password" (case-insensitive) -> issue: "hardcoded_credential"
      * "import os" with "system(" -> issue: "os_command_injection"
    - Add found issues to state["issues"]
    - Set state["file_analyses"] to a list with one dict:
      {"file": "diff", "issue_count": <count>, "issues": <issue_names>}
    - Return the updated state

  test_node(state):
    - Simulate test execution based on issues found
    - If any issues exist, set state["test_results"] to
      "3 passed, 1 failed, 1 warning"
    - If no issues, set to "5 passed, 0 failed"
    - Return the updated state
""")


def analyze_node(state: dict) -> dict:
    """Analyze the diff and populate issues and file_analyses."""
    updated = dict(state)
    updated["issues"] = list(state.get("issues", []))
    updated["file_analyses"] = list(state.get("file_analyses", []))

    diff = state.get("diff", "")
    found_issues = []

    if "eval(" in diff:
        found_issues.append("dangerous_eval")
    if "exec(" in diff:
        found_issues.append("dangerous_exec")
    if "password" in diff.lower():
        found_issues.append("hardcoded_credential")
    if "import os" in diff and "system(" in diff:
        found_issues.append("os_command_injection")

    updated["issues"] = found_issues
    updated["file_analyses"] = [{
        "file": "diff",
        "issue_count": len(found_issues),
        "issues": found_issues,
    }]

    return updated


def test_node(state: dict) -> dict:
    """Simulate test execution and populate test_results."""
    updated = dict(state)

    if state.get("issues"):
        updated["test_results"] = "3 passed, 1 failed, 1 warning"
    else:
        updated["test_results"] = "5 passed, 0 failed"

    return updated


# Validate TODO 2
total += 1
try:
    state = create_state(SAMPLE_DIFF)
    if isinstance(state, dict):
        result = analyze_node(state)
        issues = result.get("issues", []) if isinstance(result, dict) else []
        if len(issues) >= 2:
            print(f"  [PASS] analyze_node found {len(issues)} issues in sample diff")
            score += 1
        else:
            print(f"  [FAIL] Expected >= 2 issues, got: {issues}")
    else:
        print(f"  [FAIL] create_state failed")
except Exception as e:
    print(f"  [FAIL] analyze_node raised: {e}")

total += 1
try:
    state = create_state(SAMPLE_DIFF)
    if isinstance(state, dict):
        analyzed = analyze_node(state)
        if isinstance(analyzed, dict):
            tested = test_node(analyzed)
            if isinstance(tested, dict) and "failed" in tested.get("test_results", ""):
                print(f"  [PASS] test_node set results with failures for buggy code")
                score += 1
            else:
                print(f"  [FAIL] test_node results: {tested}")
        else:
            print(f"  [FAIL] analyze_node returned non-dict")
    else:
        print(f"  [FAIL] create_state failed")
except Exception as e:
    print(f"  [FAIL] test_node raised: {e}")


# ── TODO 3: Routing Function ─────────────────────────────────────
print()
print("=" * 70)
print("TODO 3: Implement route_review(state)")
print("=" * 70)

print("""
After the review node sets the severity, a routing function decides
the next step.

  route_review(state):
    - If state["severity"] == "request_changes" -> return "suggest_fixes"
    - If state["severity"] == "approve" -> return "done"
    - Otherwise -> return "manual_review"
""")


def route_review(state: dict) -> str:
    """Route based on review severity."""
    severity = state.get("severity", "")
    if severity == "request_changes":
        return "suggest_fixes"
    elif severity == "approve":
        return "done"
    else:
        return "manual_review"


# Validate TODO 3
total += 1
try:
    result = route_review({"severity": "request_changes"})
    if result == "suggest_fixes":
        print(f"  [PASS] route_review('request_changes') -> 'suggest_fixes'")
        score += 1
    else:
        print(f"  [FAIL] Expected 'suggest_fixes', got: {result}")
except Exception as e:
    print(f"  [FAIL] route_review raised: {e}")

total += 1
try:
    result = route_review({"severity": "approve"})
    if result == "done":
        print(f"  [PASS] route_review('approve') -> 'done'")
        score += 1
    else:
        print(f"  [FAIL] Expected 'done', got: {result}")
except Exception as e:
    print(f"  [FAIL] route_review raised: {e}")

total += 1
try:
    result = route_review({"severity": "pending"})
    if result == "manual_review":
        print(f"  [PASS] route_review('pending') -> 'manual_review'")
        score += 1
    else:
        print(f"  [FAIL] Expected 'manual_review', got: {result}")
except Exception as e:
    print(f"  [FAIL] route_review raised: {e}")


# ── Write State Flow Diagram ─────────────────────────────────────
print()
print("=" * 70)
print("Writing State Flow")
print("=" * 70)

try:
    state = create_state(SAMPLE_DIFF)
    if isinstance(state, dict):
        analyzed = analyze_node(state) if isinstance(state, dict) else state
        tested = test_node(analyzed) if isinstance(analyzed, dict) else analyzed
        # Simulate review setting severity
        if isinstance(tested, dict):
            tested["severity"] = "request_changes" if tested.get("issues") else "approve"
            route = route_review(tested) if isinstance(tested, dict) else "unknown"
        else:
            route = "unknown"
            tested = {}
    else:
        tested = {}
        route = "unknown"

    flow = {
        "initial_state": create_state(SAMPLE_DIFF) if isinstance(REVIEW_STATE_SCHEMA, dict) else {},
        "after_analyze": analyzed if isinstance(analyzed, dict) else {},
        "after_test": tested if isinstance(tested, dict) else {},
        "route_decision": route,
    }
except Exception:
    flow = {"error": "state flow failed"}

flow_path = os.path.join(WORKDIR, "state_flow.json")
with open(flow_path, "w") as f:
    json.dump(flow, f, indent=2, default=str)
print(f"  State flow written to: {flow_path}")


# ── Summary ───────────────────────────────────────────────────────
print()
print("=" * 70)
print(f"Lab 04 Score: {score}/{total}")
print("=" * 70)
