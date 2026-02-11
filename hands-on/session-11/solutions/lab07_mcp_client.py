#!/usr/bin/env python3
"""
Lab 07 Solution: MCP Client — Discovery and Tool Workflows

Build a mock MCP client that discovers server capabilities and executes
multi-step tool workflows with automatic tool selection.

No external packages required — standard library only.
"""

import os
import json
import shutil
from typing import Any, Dict, List, Optional

WORKDIR = "/tmp/aidev-lab-11-07"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Client Lifecycle                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: MCP Client Lifecycle")
print("=" * 70)
print()
print("  1. connect()      — Establish transport to the server")
print("  2. initialize()   — Exchange capabilities (protocol version, etc.)")
print("  3. list_tools()   — Discover available tools")
print("  4. call_tool()    — Invoke a tool with arguments")
print("  5. disconnect()   — Clean up the connection")
print()
print("  Sequence diagram:")
print("    Client                Server")
print("      │── connect ──────────▶│")
print("      │── initialize ───────▶│")
print("      │◀── capabilities ─────│")
print("      │── tools/list ───────▶│")
print("      │◀── tool list ────────│")
print("      │── tools/call ───────▶│")
print("      │◀── result ──────────│")
print("      │── disconnect ───────▶│")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — Tool Discovery Flow                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: Tool Discovery Flow")
print("=" * 70)
print()
print("  The client calls tools/list to get available tools:")
print("  {")
print('    "tools": [')
print("      {")
print('        "name": "search_code",')
print('        "description": "Search source code for patterns",')
print('        "inputSchema": {')
print('          "type": "object",')
print('          "properties": {')
print('            "query": {"type": "string"},')
print('            "path": {"type": "string"}')
print("          }")
print("        }")
print("      }")
print("    ]")
print("  }")
print()
print("  The client (or LLM) uses the description and schema to decide")
print("  which tool to invoke and how to fill in the arguments.")
print()

# ── Server simulation data ───────────────────────────────────────────────────

SERVER_TOOLS = [
    {
        "name": "search_code",
        "description": "Search source code files for a text pattern",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search pattern"},
                "path": {"type": "string", "description": "Directory to search"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "run_tests",
        "description": "Execute test suite and return results",
        "inputSchema": {
            "type": "object",
            "properties": {
                "test_path": {"type": "string", "description": "Test file or directory"},
            },
        },
    },
    {
        "name": "analyze_deps",
        "description": "Analyze project dependencies and find issues",
        "inputSchema": {
            "type": "object",
            "properties": {
                "manifest": {"type": "string", "description": "Path to requirements.txt or package.json"},
            },
            "required": ["manifest"],
        },
    },
]

def _simulate_tool_call(name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Simulate calling a server tool — returns mock results."""
    if name == "search_code":
        return {"matches": [
            {"file": "src/main.py", "line": 10, "text": f"match for '{arguments.get('query', '')}'"},
            {"file": "src/utils.py", "line": 5, "text": f"match for '{arguments.get('query', '')}'"},
        ]}
    elif name == "run_tests":
        return {"passed": 12, "failed": 1, "skipped": 2, "total": 15}
    elif name == "analyze_deps":
        return {"total": 8, "outdated": 2, "vulnerable": 1,
                "issues": ["requests==2.25.0 has known CVE"]}
    return {"error": f"Unknown tool: {name}"}

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Implement MockMCPClient                                          ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Implement MockMCPClient class")
print("=" * 70)
print()

class MockMCPClient:
    """A mock MCP client that simulates the client lifecycle."""

    def __init__(self):
        self.connected = False
        self.server_name = ""
        self.tools: List[Dict] = []
        self._call_log: List[Dict] = []

    def connect(self) -> bool:
        """Establish connection to the server."""
        self.connected = True
        self.server_name = "code-assistant-server"
        return True

    def list_tools(self) -> List[Dict]:
        """Discover available tools from the server."""
        if not self.connected:
            raise RuntimeError("Not connected")
        self.tools = SERVER_TOOLS
        return self.tools

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Invoke a tool on the server."""
        if not self.connected:
            raise RuntimeError("Not connected")
        tool_names = [t["name"] for t in self.tools]
        if name not in tool_names:
            raise ValueError(f"Unknown tool: {name}")
        result = _simulate_tool_call(name, arguments)
        self._call_log.append({"tool": name, "arguments": arguments, "result": result})
        return result

    def disconnect(self) -> bool:
        """Close the connection."""
        self.connected = False
        return True

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    client = MockMCPClient()

    # Test connect
    assert client.connect() is True, "connect() should return True"
    assert client.connected is True, "connected should be True"
    assert client.server_name == "code-assistant-server"

    # Test list_tools
    tools = client.list_tools()
    assert len(tools) == 3, f"Expected 3 tools, got {len(tools)}"

    # Test call_tool
    result = client.call_tool("search_code", {"query": "def main"})
    assert "matches" in result, "search_code should return matches"

    # Test unknown tool
    try:
        client.call_tool("nonexistent", {})
        assert False, "Should raise ValueError"
    except ValueError:
        pass

    # Test disconnect
    assert client.disconnect() is True
    assert client.connected is False

    # Test calling when disconnected
    try:
        client.list_tools()
        assert False, "Should raise RuntimeError"
    except RuntimeError:
        pass

    score += 1
    print("[PASS] MockMCPClient implements full lifecycle correctly")
except (AssertionError, Exception) as e:
    print(f"[FAIL] {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Multi-Step Workflow                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Implement a multi-step tool workflow")
print("=" * 70)
print()

def run_workflow(client: MockMCPClient) -> Dict[str, Any]:
    """Execute a multi-step workflow using the MCP client."""
    summary = {}

    client.connect()
    tools = client.list_tools()
    summary["tools_found"] = len(tools)

    search_result = client.call_tool("search_code", {"query": "import", "path": "src/"})
    summary["search_results"] = search_result

    test_result = client.call_tool("run_tests", {"test_path": "tests/"})
    summary["test_results"] = test_result

    dep_result = client.call_tool("analyze_deps", {"manifest": "requirements.txt"})
    summary["dep_results"] = dep_result

    client.disconnect()
    summary["steps_completed"] = 6  # connect, discover, search, test, deps, disconnect
    return summary

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    wf_client = MockMCPClient()
    summary = run_workflow(wf_client)
    checks = [
        isinstance(summary, dict),
        summary.get("tools_found") == 3,
        "matches" in summary.get("search_results", {}),
        summary.get("test_results", {}).get("total") == 15,
        summary.get("dep_results", {}).get("vulnerable") == 1,
        summary.get("steps_completed") == 6,
        wf_client.connected is False,
    ]
    if all(checks):
        score += 1
        print("[PASS] Multi-step workflow executed correctly")
        print(f"       Tools found: {summary['tools_found']}")
        print(f"       Tests: {summary['test_results']['passed']} passed, "
              f"{summary['test_results']['failed']} failed")
        print(f"       Deps: {summary['dep_results']['vulnerable']} vulnerable")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Checks failed at indices: {failed}")
        print(f"       Got: {summary}")
except Exception as e:
    print(f"[FAIL] Exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Tool Selector                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Implement tool_selector(task, tools)")
print("=" * 70)
print()

def tool_selector(task_description: str, available_tools: List[Dict]) -> Optional[str]:
    """Select the best tool for a task based on keyword matching."""
    task_words = set(task_description.lower().split())
    best_tool = None
    best_score = 0
    for tool in available_tools:
        desc_words = set(tool["description"].lower().split())
        overlap = len(task_words & desc_words)
        if overlap > best_score:
            best_score = overlap
            best_tool = tool["name"]
    return best_tool if best_score > 0 else None

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
test_cases = [
    ("I need to search the source code for error handling patterns", "search_code"),
    ("Run the test suite to check for regressions", "run_tests"),
    ("Check project dependencies for security issues", "analyze_deps"),
]
all_passed = True
for task, expected in test_cases:
    selected = tool_selector(task, SERVER_TOOLS)
    if selected != expected:
        all_passed = False
        print(f"  [FAIL] Task: {task!r}")
        print(f"         Expected: {expected}, Got: {selected}")

if all_passed:
    score += 1
    print("[PASS] tool_selector picks the right tool for all tasks")
    for task, expected in test_cases:
        print(f"       '{task[:50]}...' -> {expected}")
else:
    print("[FAIL] Some tool selections were incorrect")
print()

# ── Save workflow log ────────────────────────────────────────────────────────
out_path = os.path.join(WORKDIR, "workflow_log.json")
log_data = {
    "summary": summary if isinstance(summary, dict) else {},
    "test_selections": [
        {"task": t, "expected": e, "selected": tool_selector(t, SERVER_TOOLS)}
        for t, e in test_cases
    ],
}
with open(out_path, "w") as f:
    json.dump(log_data, f, indent=2, default=str)
print(f"Workflow log saved to {out_path}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 07 Score: {score}/{total}")
print("=" * 70)
