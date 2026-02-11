#!/usr/bin/env python3
"""
Lab 02 Solution: MCP Protocol — JSON-RPC 2.0 Messages

Learn the JSON-RPC 2.0 message format used by MCP: requests, responses,
error codes, and MCP-specific method names.

No external packages required — standard library only.
"""

import os
import json
import shutil
from typing import Any, Dict, Optional, Tuple

WORKDIR = "/tmp/aidev-lab-11-02"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — JSON-RPC 2.0 Message Structure                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: JSON-RPC 2.0 Message Structure")
print("=" * 70)
print()
print("  Request:  { jsonrpc: '2.0', id: 1, method: '...', params: {...} }")
print("  Response: { jsonrpc: '2.0', id: 1, result: {...} }")
print("  Error:    { jsonrpc: '2.0', id: 1, error: {code, message} }")
print()
print("  Required fields in a request:")
print("    - jsonrpc  (must be '2.0')")
print("    - id       (integer or string, correlates request to response)")
print("    - method   (string, the RPC method name)")
print()
print("  Optional:")
print("    - params   (object or array, method arguments)")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — MCP Method Names                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: MCP-Specific Method Names")
print("=" * 70)
print()
print("  ┌─────────────────────┬────────────────────────────────────────────┐")
print("  │ Method              │ Purpose                                    │")
print("  ├─────────────────────┼────────────────────────────────────────────┤")
print("  │ initialize          │ Handshake: exchange capabilities           │")
print("  │ tools/list          │ Discover available tools                   │")
print("  │ tools/call          │ Invoke a tool with arguments               │")
print("  │ resources/list      │ Discover available resources               │")
print("  │ resources/read      │ Read a specific resource by URI            │")
print("  │ prompts/list        │ Discover available prompt templates        │")
print("  │ prompts/get         │ Retrieve a prompt with arguments filled    │")
print("  └─────────────────────┴────────────────────────────────────────────┘")
print()
print("  Standard JSON-RPC error codes:")
print("    -32700  Parse error")
print("    -32600  Invalid request")
print("    -32601  Method not found")
print("    -32602  Invalid params")
print("    -32603  Internal error")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Build a tools/list Request                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Build a valid JSON-RPC request for 'tools/list'")
print("=" * 70)
print()

tools_list_request = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
}

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    serialized = json.dumps(tools_list_request)
    parsed = json.loads(serialized)
    checks = [
        parsed.get("jsonrpc") == "2.0",
        parsed.get("id") == 1,
        parsed.get("method") == "tools/list",
    ]
    if all(checks):
        score += 1
        print("[PASS] tools/list request is valid JSON-RPC 2.0")
    else:
        print("[FAIL] Request does not match expected structure")
        print("       Got:", json.dumps(parsed, indent=2))
except Exception as e:
    print(f"[FAIL] JSON serialization error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Build a tools/call Request                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Build a tools/call request for 'search_code'")
print("=" * 70)
print()

tools_call_request = {
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/call",
    "params": {
        "name": "search_code",
        "arguments": {
            "query": "def main",
            "path": "src/",
        }
    }
}

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    serialized = json.dumps(tools_call_request)
    parsed = json.loads(serialized)
    checks = [
        parsed.get("jsonrpc") == "2.0",
        parsed.get("id") == 2,
        parsed.get("method") == "tools/call",
        parsed.get("params", {}).get("name") == "search_code",
        parsed.get("params", {}).get("arguments", {}).get("query") == "def main",
        parsed.get("params", {}).get("arguments", {}).get("path") == "src/",
    ]
    if all(checks):
        score += 1
        print("[PASS] tools/call request for search_code is valid")
    else:
        print("[FAIL] Request does not match expected structure")
        print("       Got:", json.dumps(parsed, indent=2))
except Exception as e:
    print(f"[FAIL] JSON serialization error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Build a JSON-RPC Error Response                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Build a JSON-RPC error response (method not found)")
print("=" * 70)
print()

error_response = {
    "jsonrpc": "2.0",
    "id": 99,
    "error": {
        "code": -32601,
        "message": "Method not found",
    }
}

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    serialized = json.dumps(error_response)
    parsed = json.loads(serialized)
    checks = [
        parsed.get("jsonrpc") == "2.0",
        parsed.get("id") == 99,
        parsed.get("error", {}).get("code") == -32601,
        parsed.get("error", {}).get("message") == "Method not found",
        "result" not in parsed,
    ]
    if all(checks):
        score += 1
        print("[PASS] Error response is valid JSON-RPC 2.0")
    else:
        print("[FAIL] Error response does not match expected structure")
        print("       Got:", json.dumps(parsed, indent=2))
except Exception as e:
    print(f"[FAIL] JSON serialization error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 4 — Implement validate_jsonrpc_request()                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 4: Implement validate_jsonrpc_request(msg)")
print("=" * 70)
print()

def validate_jsonrpc_request(msg: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate that msg is a well-formed JSON-RPC 2.0 request.

    Returns:
        (True, "ok") if valid
        (False, reason) if invalid
    """
    if not isinstance(msg, dict):
        return (False, "Message must be a dict")
    if msg.get("jsonrpc") != "2.0":
        return (False, "jsonrpc must be '2.0'")
    if "id" not in msg or not isinstance(msg["id"], (int, str)):
        return (False, "id must be an int or str")
    if "method" not in msg or not isinstance(msg["method"], str):
        return (False, "method must be a string")
    return (True, "ok")

# ── Validate TODO 4 ─────────────────────────────────────────────────────────
total += 1
test_cases = [
    ({"jsonrpc": "2.0", "id": 1, "method": "tools/list"}, True),
    ({"jsonrpc": "2.0", "id": "abc", "method": "initialize"}, True),
    ("not a dict", False),
    ({"id": 1, "method": "test"}, False),                    # missing jsonrpc
    ({"jsonrpc": "1.0", "id": 1, "method": "test"}, False),  # wrong version
    ({"jsonrpc": "2.0", "method": "test"}, False),            # missing id
    ({"jsonrpc": "2.0", "id": 1}, False),                     # missing method
    ({"jsonrpc": "2.0", "id": 1, "method": 123}, False),     # method not str
]

all_passed = True
for msg, expected_valid in test_cases:
    try:
        result = validate_jsonrpc_request(msg)
        is_valid = result[0] if isinstance(result, tuple) else False
        if is_valid != expected_valid:
            all_passed = False
            print(f"  [FAIL] Input: {msg}")
            print(f"         Expected valid={expected_valid}, got valid={is_valid}")
    except Exception as e:
        all_passed = False
        print(f"  [FAIL] Exception for input {msg}: {e}")

if all_passed:
    score += 1
    print("[PASS] validate_jsonrpc_request handles all test cases")
else:
    print("[FAIL] Some test cases did not pass")
print()

# ── Save all messages to file ────────────────────────────────────────────────
messages = {
    "tools_list_request": tools_list_request,
    "tools_call_request": tools_call_request,
    "error_response": error_response,
}
out_path = os.path.join(WORKDIR, "messages.json")
with open(out_path, "w") as f:
    json.dump(messages, f, indent=2)
print(f"Messages saved to {out_path}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 02 Score: {score}/{total}")
print("=" * 70)
