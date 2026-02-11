"""
Lab 08 (Challenge): Complete AI Dev Tool Suite

Combine code quality analysis, tool registry, sandboxed execution, and
review workflow into a unified AI development tool suite.

This is the comprehensive challenge lab that ties together all concepts
from Session 12.

Uses only Python standard library (ast, json, os, re, subprocess, textwrap).
"""

import ast
import json
import os
import re
import shutil
import subprocess
import textwrap

WORKDIR = "/tmp/aidev-lab-12-08"

# ── Cleanup and Setup ──────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

print("=" * 70)
print("CHALLENGE: Complete AI Dev Tool Suite")
print("=" * 70)

print("""
In this challenge you will build a complete AI dev tool suite that:

  1. Has a tool registry with 4 tools
  2. Wraps each tool in sandboxed execution
  3. Runs a full review workflow on sample code
  4. Generates a comprehensive report

  Architecture:
  ┌──────────────────────────────────────────────────────────────────┐
  │                        DevToolSuite                             │
  │  ┌──────────────┐  ┌──────────────┐  ┌────────────────────┐   │
  │  │ ToolRegistry │  │ Sandbox      │  │ ReviewWorkflow     │   │
  │  │  - register  │  │  - is_safe   │  │  - analyze_code    │   │
  │  │  - discover  │  │  - exec      │  │  - run_tests       │   │
  │  │  - route     │  │  - validate  │  │  - generate_review │   │
  │  └──────────────┘  └──────────────┘  └────────────────────┘   │
  └──────────────────────────────────────────────────────────────────┘
""")

# ── Sample code to analyze ────────────────────────────────────────

SAMPLE_PROJECT_CODE = textwrap.dedent("""\
    import os
    import json
    import pickle

    API_KEY = "sk-prod-abc123xyz789"

    def load_user_data(filepath):
        with open(filepath, 'rb') as f:
            return pickle.load(f)

    def process_query(query):
        result = eval(query)
        return {"result": result}

    def search_items(items, query, limit=100):
        matches = []
        for item in items:
            for field in item.values():
                if query.lower() in str(field).lower():
                    matches.append(item)
        return matches[:limit]

    def save_report(data, path):
        with open(path, 'w') as f:
            json.dump(data, f)

    def get_config():
        return {
            "db_host": os.environ.get("DB_HOST", "localhost"),
            "db_password": "admin123",
            "debug": True
        }
""")


# ── TODO 1: Create Tool Registry with 4 Tools ────────────────────
print()
print("=" * 70)
print("TODO 1: Create a ToolRegistry with 4 tools")
print("=" * 70)

print("""
Build a ToolRegistry class (or reuse your Lab 06 design) and register
4 tools:

  1. "analyze_code" — Analyze Python source for issues using ast
     Tags: ["analysis", "code_quality"]
     Handler: Takes source(str), returns dict with "issues" list and "stats" dict

  2. "run_tests" — Simulate running tests on code
     Tags: ["testing", "validation"]
     Handler: Takes source(str), returns dict with "total", "passed", "failed"

  3. "generate_docs" — Extract documentation from source
     Tags: ["docs", "code_quality"]
     Handler: Takes source(str), returns dict with "functions" list and "undocumented" list

  4. "search_files" — Search for patterns in source code
     Tags: ["search", "analysis"]
     Handler: Takes source(str), pattern(str), returns dict with "matches" list

Each handler should be a real function that does actual work (not a stub).

Store the registry in a variable called `registry`.
""")


class ToolRegistry:
    """Tool registry for the dev suite."""

    def __init__(self):
        self._tools = {}

    def register(self, name, handler, description="", tags=None):
        self._tools[name] = {
            "name": name,
            "handler": handler,
            "description": description,
            "tags": tags or [],
        }
        return self

    def discover(self, query=None, tags=None):
        results = []
        for tool in self._tools.values():
            if query and query.lower() not in tool["description"].lower():
                continue
            if tags and not all(t in tool["tags"] for t in tags):
                continue
            results.append({"name": tool["name"], "description": tool["description"], "tags": tool["tags"]})
        return results

    def route(self, tool_name, **kwargs):
        if tool_name not in self._tools:
            return {"error": f"Tool '{tool_name}' not found"}
        return self._tools[tool_name]["handler"](**kwargs)

    def list_all(self):
        return sorted(self._tools.keys())


# TODO: Implement the 4 handler functions
# TODO: Create a ToolRegistry instance called `registry`
# TODO: Register all 4 tools

def analyze_code_tool(source: str) -> dict:
    """Analyze Python source code for issues."""
    # TODO: Use ast and string matching to find:
    #   - Security issues: eval, exec, pickle.load, hardcoded strings with "sk-" or "password"
    #   - Performance issues: nested for loops
    #   - Style issues: functions missing docstrings
    # Return: {"issues": [...], "stats": {"functions": N, "classes": N, "lines": N}}
    return "___"


def run_tests_tool(source: str) -> dict:
    """Simulate test execution on source code."""
    # TODO: Count functions in source using ast
    # TODO: Simulate: 1 test per function, functions with issues -> failed
    #   Issues = function uses eval/exec or has no docstring
    # Return: {"total": N, "passed": N, "failed": N, "details": [...]}
    return "___"


def generate_docs_tool(source: str) -> dict:
    """Extract documentation from source code."""
    # TODO: Use ast to extract function names and docstrings
    # Return: {"functions": [{"name": N, "docstring": D}], "undocumented": [names...]}
    return "___"


def search_files_tool(source: str, pattern: str = "") -> dict:
    """Search for a pattern in source code."""
    # TODO: Search each line of source for the pattern (case-insensitive)
    # Return: {"pattern": pattern, "matches": [{"line_num": N, "line": text}]}
    return "___"


# Create and populate registry
registry = "___"


# Validate TODO 1
total += 1
try:
    if isinstance(registry, ToolRegistry) and len(registry.list_all()) == 4:
        print(f"  [PASS] Registry has 4 tools: {registry.list_all()}")
        score += 1
    else:
        tools = registry.list_all() if isinstance(registry, ToolRegistry) else "not a registry"
        print(f"  [FAIL] Expected 4 tools, got: {tools}")
except Exception as e:
    print(f"  [FAIL] Registry check raised: {e}")

total += 1
try:
    result = registry.route("analyze_code", source=SAMPLE_PROJECT_CODE)
    if isinstance(result, dict) and "issues" in result and len(result["issues"]) >= 3:
        print(f"  [PASS] analyze_code found {len(result['issues'])} issues")
        score += 1
    else:
        print(f"  [FAIL] analyze_code result: {result}")
except Exception as e:
    print(f"  [FAIL] analyze_code raised: {e}")

total += 1
try:
    result = registry.route("generate_docs", source=SAMPLE_PROJECT_CODE)
    if isinstance(result, dict) and "undocumented" in result and len(result["undocumented"]) >= 3:
        print(f"  [PASS] generate_docs found {len(result['undocumented'])} undocumented functions")
        score += 1
    else:
        print(f"  [FAIL] generate_docs result: {result}")
except Exception as e:
    print(f"  [FAIL] generate_docs raised: {e}")

total += 1
try:
    result = registry.route("search_files", source=SAMPLE_PROJECT_CODE, pattern="eval")
    if isinstance(result, dict) and len(result.get("matches", [])) >= 1:
        print(f"  [PASS] search_files found 'eval' in source")
        score += 1
    else:
        print(f"  [FAIL] search_files result: {result}")
except Exception as e:
    print(f"  [FAIL] search_files raised: {e}")


# ── TODO 2: Sandboxed Execution Wrapper ──────────────────────────
print()
print("=" * 70)
print("TODO 2: Implement sandboxed execution wrapper")
print("=" * 70)

print("""
Create a sandboxed_tool_call function that wraps registry.route calls:

  sandboxed_tool_call(registry, tool_name, **kwargs):
    1. Check that tool_name exists in registry (list_all)
       → If not: return {"status": "error", "reason": "Unknown tool"}
    2. Try to call registry.route(tool_name, **kwargs)
    3. If successful, return {"status": "success", "tool": tool_name, "result": <result>}
    4. If exception, return {"status": "error", "tool": tool_name, "reason": str(e)}
    5. Wrap in a try/except to catch ALL exceptions
""")


def sandboxed_tool_call(reg: ToolRegistry, tool_name: str, **kwargs) -> dict:
    """Execute a tool call with error handling."""
    # TODO: Validate tool exists
    # TODO: Call registry.route with try/except
    # TODO: Return structured result
    result = "___"
    return result


# Validate TODO 2
total += 1
try:
    result = sandboxed_tool_call(registry, "analyze_code", source="print('hello')")
    if isinstance(result, dict) and result.get("status") == "success":
        print(f"  [PASS] sandboxed_tool_call succeeds for valid tool")
        score += 1
    else:
        print(f"  [FAIL] Expected success: {result}")
except Exception as e:
    print(f"  [FAIL] sandboxed_tool_call raised: {e}")

total += 1
try:
    result = sandboxed_tool_call(registry, "nonexistent_tool")
    if isinstance(result, dict) and result.get("status") == "error":
        print(f"  [PASS] sandboxed_tool_call handles unknown tool")
        score += 1
    else:
        print(f"  [FAIL] Expected error for unknown tool: {result}")
except Exception as e:
    print(f"  [FAIL] sandboxed_tool_call raised: {e}")


# ── TODO 3: Complete Review Workflow ──────────────────────────────
print()
print("=" * 70)
print("TODO 3: Run complete review workflow on sample code")
print("=" * 70)

print("""
Execute a full review workflow using the registered tools:

  1. Run analyze_code on SAMPLE_PROJECT_CODE via sandboxed_tool_call
  2. Run run_tests on SAMPLE_PROJECT_CODE via sandboxed_tool_call
  3. Run generate_docs on SAMPLE_PROJECT_CODE via sandboxed_tool_call
  4. Run search_files for pattern "eval" via sandboxed_tool_call

  5. Determine severity:
     - If any security issues in analysis → "request_changes"
     - Else if any issues at all → "comment"
     - Else → "approve"

  6. Build a review dict:
     {
         "code_analysis": <result from step 1>,
         "test_results": <result from step 2>,
         "documentation": <result from step 3>,
         "security_scan": <result from step 4>,
         "severity": <from step 5>,
         "summary": <multi-line string summarizing all findings>
     }

  Store in variable `review_result`.
""")

# TODO: Run the 4 tool calls
# TODO: Determine severity
# TODO: Build the review dict
review_result = "___"


# Validate TODO 3
total += 1
try:
    if isinstance(review_result, dict) and "code_analysis" in review_result:
        print(f"  [PASS] review_result has code_analysis")
        score += 1
    else:
        print(f"  [FAIL] Missing code_analysis: {type(review_result)}")
except Exception as e:
    print(f"  [FAIL] review_result check raised: {e}")

total += 1
try:
    if isinstance(review_result, dict) and review_result.get("severity") == "request_changes":
        print(f"  [PASS] review_result severity='request_changes' (correct for sample code)")
        score += 1
    else:
        sev = review_result.get("severity") if isinstance(review_result, dict) else "N/A"
        print(f"  [FAIL] Expected severity='request_changes', got: {sev}")
except Exception as e:
    print(f"  [FAIL] severity check raised: {e}")

total += 1
try:
    if isinstance(review_result, dict) and "summary" in review_result and len(review_result["summary"]) > 50:
        print(f"  [PASS] review_result has detailed summary ({len(review_result['summary'])} chars)")
        score += 1
    else:
        print(f"  [FAIL] Missing or short summary")
except Exception as e:
    print(f"  [FAIL] summary check raised: {e}")


# ── TODO 4: Generate Comprehensive Report ─────────────────────────
print()
print("=" * 70)
print("TODO 4: Generate comprehensive report")
print("=" * 70)

print("""
Create a comprehensive JSON report and save it to WORKDIR/dev_tool_report.json.

The report should contain:
  {
      "tool_suite": {
          "registered_tools": <list from registry.list_all()>,
          "discoverable_by_analysis": <list of names from discover(tags=["analysis"])>,
      },
      "review": <review_result from TODO 3>,
      "execution_log": [
          {"tool": <name>, "status": <success/error>}
          for each of the 4 tool calls
      ],
      "recommendations": [
          <list of 1-line string recommendations based on findings>
          e.g., "Remove eval() usage in process_query function"
          e.g., "Remove hardcoded API key from source code"
          e.g., "Add docstrings to all functions"
      ]
  }

Store in `final_report` and write to WORKDIR/dev_tool_report.json.
""")

# TODO: Build the final_report dict
# TODO: Write to JSON file
final_report = "___"


# Write the report
report_path = os.path.join(WORKDIR, "dev_tool_report.json")
try:
    with open(report_path, "w") as f:
        json.dump(final_report if isinstance(final_report, dict) else {"error": str(final_report)}, f, indent=2, default=str)
    print(f"  Report written to: {report_path}")
except Exception as e:
    print(f"  Failed to write report: {e}")


# Validate TODO 4
total += 1
try:
    if os.path.exists(report_path):
        with open(report_path) as f:
            data = json.load(f)
        if "tool_suite" in data and "review" in data:
            print(f"  [PASS] dev_tool_report.json has tool_suite and review sections")
            score += 1
        else:
            print(f"  [FAIL] Report missing sections: {list(data.keys())}")
    else:
        print(f"  [FAIL] Report file not found")
except Exception as e:
    print(f"  [FAIL] Report validation raised: {e}")

total += 1
try:
    with open(report_path) as f:
        data = json.load(f)
    recs = data.get("recommendations", [])
    if isinstance(recs, list) and len(recs) >= 2:
        print(f"  [PASS] Report has {len(recs)} recommendations")
        score += 1
    else:
        print(f"  [FAIL] Expected >= 2 recommendations: {recs}")
except Exception as e:
    print(f"  [FAIL] Recommendations check raised: {e}")

total += 1
try:
    with open(report_path) as f:
        data = json.load(f)
    log = data.get("execution_log", [])
    if isinstance(log, list) and len(log) == 4:
        print(f"  [PASS] Execution log has 4 entries")
        score += 1
    else:
        print(f"  [FAIL] Expected 4 log entries: {log}")
except Exception as e:
    print(f"  [FAIL] Execution log check raised: {e}")


# ── Summary ───────────────────────────────────────────────────────
print()
print("=" * 70)
print(f"Challenge Lab 08 Score: {score}/{total}")
print("=" * 70)

if score == total:
    print("\nCongratulations! You completed the full AI Dev Tool Suite challenge!")
elif score >= total * 0.7:
    print("\nGreat progress! Review the failing checks and refine your implementation.")
else:
    print("\nKeep going! Work through each TODO step by step.")
