"""
Lab 05: Full Code Review Agent Workflow

Build a complete review workflow that chains together code analysis,
test execution simulation, and review generation — following graph-style
execution patterns.

Key concepts:
- Multi-step workflow execution
- AST-based code analysis in a workflow node
- Conditional routing based on analysis results
- Synthesizing findings into a structured review

Uses only Python standard library (ast, json, os, textwrap).
"""

import ast
import json
import os
import shutil
import textwrap

WORKDIR = "/tmp/aidev-lab-12-05"

# ── Cleanup and Setup ──────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ── Step 1: Graph-Like Workflow Execution ─────────────────────────
print("=" * 70)
print("STEP 1: Graph-Style Workflow Execution")
print("=" * 70)

print("""
A workflow graph executes nodes in sequence (or conditionally), passing
state between them. Without LangGraph, we simulate this with a simple
executor:

  def execute_graph(state, nodes, router=None):
      for node_fn in nodes:
          state = node_fn(state)
          if router and node_fn == review_node:
              next_step = router(state)
              if next_step == "suggest_fixes":
                  state = suggest_fixes_node(state)
      return state

  This pattern:
  ┌─────────┐   ┌──────────┐   ┌────────────┐   ┌──────────────┐
  │ analyze │ → │  test    │ → │  review    │ → │ suggest_fixes│
  └─────────┘   └──────────┘   └────────────┘   └──────────────┘
                                      │
                                      ├─ severity == "approve" → DONE
                                      └─ severity == "request_changes" → suggest_fixes
""")

# ── Step 2: Multi-Agent Review Concepts ───────────────────────────
print("=" * 70)
print("STEP 2: Multi-Reviewer Pattern")
print("=" * 70)

print("""
Production review systems use specialized reviewers:

  ┌─────────────────┬────────────────────────────────────────────┐
  │ Reviewer         │ Checks For                                │
  ├─────────────────┼────────────────────────────────────────────┤
  │ Security        │ eval/exec, hardcoded secrets, SQL inject   │
  │ Performance     │ Nested loops, large allocations, no cache  │
  │ Style           │ Naming conventions, line length, imports    │
  │ Correctness     │ Missing error handling, type mismatches    │
  └─────────────────┴────────────────────────────────────────────┘

  Each reviewer acts as a sub-node producing its own findings,
  which are merged in the review synthesis node.
""")

# ── Sample code for review ────────────────────────────────────────

SAMPLE_CODE_FOR_REVIEW = textwrap.dedent("""\
    import os
    import pickle

    def load_config(path):
        with open(path, 'rb') as f:
            return pickle.load(f)

    def get_secret():
        api_key = "sk-1234567890abcdef"
        return api_key

    def search(query, items):
        results = []
        for i in items:
            for j in items:
                if query in str(i) + str(j):
                    results.append((i, j))
        return results

    def process(data):
        result = eval(data)
        return result

    def calculate(x, y):
        return x / y
""")

CLEAN_CODE = textwrap.dedent("""\
    def add(a: int, b: int) -> int:
        \"\"\"Add two numbers.\"\"\"
        return a + b

    def greet(name: str) -> str:
        \"\"\"Return a greeting.\"\"\"
        if not name:
            return "Hello, World!"
        return f"Hello, {name}!"
""")


# ── TODO 1: Analyze Code Node ────────────────────────────────────
print("=" * 70)
print("TODO 1: Implement analyze_code_node(state)")
print("=" * 70)

print("""
This node uses ast to find issues in the code stored in state["code"].

Security checks (search in source text):
  - "eval(" or "exec(" -> {"category": "security", "issue": "dangerous_eval_exec",
                           "detail": "Use of eval/exec detected"}
  - "pickle.load" -> {"category": "security", "issue": "unsafe_deserialization",
                       "detail": "Pickle load can execute arbitrary code"}
  - String that looks like a key/token (contains "sk-" or "api_key" with a
    literal string assignment) -> {"category": "security", "issue": "hardcoded_secret",
                                    "detail": "Hardcoded secret detected"}

Performance checks (use ast):
  - Nested for loops (a For node containing another For in ast.walk of its body)
    -> {"category": "performance", "issue": "nested_loop",
        "detail": "Nested loop in function <name>"}

Style checks (use ast):
  - Function without docstring -> {"category": "style", "issue": "missing_docstring",
                                    "detail": "Function <name> lacks docstring"}

Update state:
  state["issues"] = <list of issue dicts>
  state["file_analyses"] = [{"functions_found": N, "issues_found": M}]
Return the updated state.
""")


def analyze_code_node(state: dict) -> dict:
    """Analyze code for security, performance, and style issues."""
    updated = dict(state)
    updated["issues"] = []
    updated["file_analyses"] = []
    code = state.get("code", "")

    # TODO: Security checks on source text
    # TODO: AST-based performance check (nested loops)
    # TODO: AST-based style check (missing docstrings)
    # TODO: Set updated["issues"] and updated["file_analyses"]
    updated["issues"] = "___"
    updated["file_analyses"] = "___"

    return updated


# Validate TODO 1
total += 1
try:
    state = {"code": SAMPLE_CODE_FOR_REVIEW, "issues": [], "file_analyses": [],
             "test_results": "", "review_summary": "", "severity": "pending"}
    result = analyze_code_node(state)
    issues = result.get("issues", []) if isinstance(result, dict) else []
    categories = [i["category"] for i in issues] if isinstance(issues, list) else []
    if "security" in categories:
        print(f"  [PASS] analyze_code_node found security issues")
        score += 1
    else:
        print(f"  [FAIL] Expected security issues: {issues}")
except Exception as e:
    print(f"  [FAIL] analyze_code_node raised: {e}")

total += 1
try:
    result = analyze_code_node(state)
    issues = result.get("issues", []) if isinstance(result, dict) else []
    categories = [i["category"] for i in issues] if isinstance(issues, list) else []
    if "performance" in categories:
        print(f"  [PASS] analyze_code_node found performance issues")
        score += 1
    else:
        print(f"  [FAIL] Expected performance issues: {categories}")
except Exception as e:
    print(f"  [FAIL] analyze_code_node raised: {e}")

total += 1
try:
    result = analyze_code_node(state)
    issues = result.get("issues", []) if isinstance(result, dict) else []
    categories = [i["category"] for i in issues] if isinstance(issues, list) else []
    if "style" in categories:
        print(f"  [PASS] analyze_code_node found style issues")
        score += 1
    else:
        print(f"  [FAIL] Expected style issues: {categories}")
except Exception as e:
    print(f"  [FAIL] analyze_code_node raised: {e}")


# ── TODO 2: Run Tests Node ───────────────────────────────────────
print()
print("=" * 70)
print("TODO 2: Implement run_tests_node(state)")
print("=" * 70)

print("""
Simulate test execution based on the code analysis.

Logic:
  - Count security issues from state["issues"]
  - Count total issues
  - Simulate: total_tests = 10
    passed = max(0, total_tests - total_issues)
    failed = min(total_issues, total_tests)
  - Set state["test_results"] to a summary string:
    f"{total_tests} tests: {passed} passed, {failed} failed"
  - Return updated state
""")


def run_tests_node(state: dict) -> dict:
    """Simulate test execution based on analysis findings."""
    updated = dict(state)

    # TODO: Count issues from state["issues"]
    # TODO: Calculate passed and failed
    # TODO: Set updated["test_results"]
    updated["test_results"] = "___"

    return updated


# Validate TODO 2
total += 1
try:
    state = {"code": SAMPLE_CODE_FOR_REVIEW, "issues": [
        {"category": "security", "issue": "dangerous_eval_exec"},
        {"category": "security", "issue": "hardcoded_secret"},
        {"category": "performance", "issue": "nested_loop"},
    ], "file_analyses": [], "test_results": "", "review_summary": "", "severity": "pending"}
    result = run_tests_node(state)
    tr = result.get("test_results", "") if isinstance(result, dict) else ""
    if "10 tests" in tr and "passed" in tr and "failed" in tr:
        print(f"  [PASS] run_tests_node produced: {tr}")
        score += 1
    else:
        print(f"  [FAIL] Expected test results string, got: {tr}")
except Exception as e:
    print(f"  [FAIL] run_tests_node raised: {e}")


# ── TODO 3: Generate Review Node ─────────────────────────────────
print()
print("=" * 70)
print("TODO 3: Implement generate_review_node(state)")
print("=" * 70)

print("""
Synthesize a final review from the analysis and test results.

Logic:
  - Read state["issues"] and state["test_results"]
  - Count security issues — if any security issues exist,
    set severity to "request_changes"
  - Otherwise if any issues exist, set severity to "comment"
  - Otherwise set severity to "approve"

  - Build review_summary as a multi-line string:
    "Code Review Summary\\n"
    "===================\\n"
    "Issues Found: N\\n"
    "Security: X | Performance: Y | Style: Z\\n"
    "Test Results: <test_results>\\n"
    "Verdict: <severity>\\n"
    (then list each issue on its own line)

  - Set state["review_summary"] and state["severity"]
  - Return updated state
""")


def generate_review_node(state: dict) -> dict:
    """Generate a review summary from analysis and test results."""
    updated = dict(state)

    # TODO: Count issues by category
    # TODO: Determine severity
    # TODO: Build review_summary string
    # TODO: Set updated["review_summary"] and updated["severity"]
    updated["review_summary"] = "___"
    updated["severity"] = "___"

    return updated


# Validate TODO 3
total += 1
try:
    state = {
        "code": SAMPLE_CODE_FOR_REVIEW,
        "issues": [
            {"category": "security", "issue": "dangerous_eval_exec", "detail": "eval found"},
            {"category": "performance", "issue": "nested_loop", "detail": "nested for"},
        ],
        "file_analyses": [],
        "test_results": "10 tests: 8 passed, 2 failed",
        "review_summary": "",
        "severity": "pending",
    }
    result = generate_review_node(state)
    if isinstance(result, dict) and result.get("severity") == "request_changes":
        print(f"  [PASS] generate_review_node set severity='request_changes' for security issues")
        score += 1
    else:
        print(f"  [FAIL] Expected severity='request_changes': {result}")
except Exception as e:
    print(f"  [FAIL] generate_review_node raised: {e}")

total += 1
try:
    if isinstance(result, dict) and "Issues Found:" in result.get("review_summary", ""):
        print(f"  [PASS] generate_review_node includes issue count in summary")
        score += 1
    else:
        print(f"  [FAIL] review_summary missing 'Issues Found:': {result.get('review_summary', '')[:100]}")
except Exception as e:
    print(f"  [FAIL] generate_review_node check raised: {e}")


# ── TODO 4: Execute Full Workflow ─────────────────────────────────
print()
print("=" * 70)
print("TODO 4: Implement execute_workflow(code)")
print("=" * 70)

print("""
Run the complete review workflow:

  1. Create initial state with the code
  2. Run analyze_code_node
  3. Run run_tests_node
  4. Run generate_review_node
  5. Check severity for routing:
     - "request_changes" -> add a "suggestions" field with fix hints
     - "approve" -> add "suggestions": "No changes needed"
  6. Return final state

The initial state should have keys:
  code, issues, file_analyses, test_results, review_summary, severity
""")


def execute_workflow(code: str) -> dict:
    """Execute the complete review workflow."""
    # TODO: Create initial state dict
    # TODO: Run analyze_code_node -> run_tests_node -> generate_review_node
    # TODO: Route based on severity and add suggestions
    # TODO: Return final state
    final_state = "___"
    return final_state


# Validate TODO 4
total += 1
try:
    result = execute_workflow(SAMPLE_CODE_FOR_REVIEW)
    if isinstance(result, dict) and result.get("severity") == "request_changes":
        print(f"  [PASS] execute_workflow returns 'request_changes' for problematic code")
        score += 1
    else:
        print(f"  [FAIL] Expected 'request_changes': {result}")
except Exception as e:
    print(f"  [FAIL] execute_workflow raised: {e}")

total += 1
try:
    result = execute_workflow(CLEAN_CODE)
    if isinstance(result, dict) and result.get("severity") in ("approve", "comment"):
        print(f"  [PASS] execute_workflow returns '{result['severity']}' for clean code")
        score += 1
    else:
        print(f"  [FAIL] Expected 'approve' or 'comment' for clean code: {result}")
except Exception as e:
    print(f"  [FAIL] execute_workflow raised: {e}")

total += 1
try:
    result = execute_workflow(SAMPLE_CODE_FOR_REVIEW)
    if isinstance(result, dict) and "suggestions" in result:
        print(f"  [PASS] execute_workflow includes suggestions field")
        score += 1
    else:
        print(f"  [FAIL] Missing 'suggestions' in result: {list(result.keys()) if isinstance(result, dict) else result}")
except Exception as e:
    print(f"  [FAIL] execute_workflow raised: {e}")


# ── Write Review Report ──────────────────────────────────────────
print()
print("=" * 70)
print("Writing Review Report")
print("=" * 70)

try:
    final = execute_workflow(SAMPLE_CODE_FOR_REVIEW) if callable(execute_workflow) else {}
except Exception:
    final = {"error": "workflow failed"}

report_path = os.path.join(WORKDIR, "review_report.json")
with open(report_path, "w") as f:
    json.dump(final if isinstance(final, dict) else {}, f, indent=2, default=str)
print(f"  Review report written to: {report_path}")


# ── Summary ───────────────────────────────────────────────────────
print()
print("=" * 70)
print(f"Lab 05 Score: {score}/{total}")
print("=" * 70)
