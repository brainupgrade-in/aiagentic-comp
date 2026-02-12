#!/usr/bin/env python3
"""
Lab 07: MCP Security & Governance

Implement input validation for MCP tool arguments, role-based access
control (RBAC), and audit logging for enterprise MCP deployments.

No external packages required — standard library only.
"""

import os
import json
import shutil
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

WORKDIR = "/tmp/aidev-lab-13-07"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Enterprise MCP Security Layers                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: Enterprise MCP Security Layers")
print("=" * 70)
print()
print("  Defense in depth for MCP deployments:")
print()
print("  ┌────────────────────────────────────────────────────────────────────┐")
print("  │  Layer 1: INPUT VALIDATION                                        │")
print("  │    Sanitize all tool arguments before execution                   │")
print("  │    Block: SQL injection, path traversal, oversized payloads       │")
print("  ├────────────────────────────────────────────────────────────────────┤")
print("  │  Layer 2: ACCESS CONTROL (RBAC)                                   │")
print("  │    Role-based server and tool permissions                         │")
print("  │    Analysts → data only, Developers → code + CI/CD               │")
print("  ├────────────────────────────────────────────────────────────────────┤")
print("  │  Layer 3: AUDIT LOGGING                                           │")
print("  │    Log every tool call: who, what, when, result                   │")
print("  │    Compliance: SOC2, GDPR, HIPAA                                 │")
print("  └────────────────────────────────────────────────────────────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Input Validation                                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Implement input validation for MCP tool arguments")
print("=" * 70)
print()

def validate_tool_input(tool_name: str, arguments: Dict) -> Tuple[bool, str]:
    """Validate tool arguments before execution.

    Rules:
        1. For "query_db": SQL must start with SELECT (read-only),
           must not contain ";--" or "DROP" or "DELETE" or "UPDATE" or "INSERT"
           (case-insensitive check)
        2. For any tool: string arguments must not contain "../" (path traversal)
        3. For any tool: string arguments must be <= 1000 characters
        4. All arguments must be strings (for simplicity)

    Args:
        tool_name: Name of the tool being called
        arguments: Dict of argument name → value

    Returns:
        Tuple of (is_valid: bool, message: str)
        If valid: (True, "ok")
        If invalid: (False, "description of the violation")
    """
    # TODO: Implement input validation.
    #
    # Hint:
    #   # Check all values are strings
    #   for key, value in arguments.items():
    #       if not isinstance(value, str):
    #           return (False, f"Argument '{key}' must be a string")
    #
    #   # Check string length
    #   for key, value in arguments.items():
    #       if len(value) > 1000:
    #           return (False, f"Argument '{key}' exceeds 1000 character limit")
    #
    #   # Check path traversal
    #   for key, value in arguments.items():
    #       if "../" in value:
    #           return (False, f"Argument '{key}' contains path traversal")
    #
    #   # SQL-specific checks
    #   if tool_name == "query_db":
    #       sql = arguments.get("sql", "").strip().upper()
    #       if not sql.startswith("SELECT"):
    #           return (False, "SQL must start with SELECT (read-only)")
    #       dangerous = [";--", "DROP", "DELETE", "UPDATE", "INSERT"]
    #       for kw in dangerous:
    #           if kw in sql:
    #               return (False, f"SQL contains forbidden keyword: {kw}")
    #
    #   return (True, "ok")

    return "___"  # Replace with your implementation

# Test cases
test_cases = [
    ("query_db", {"sql": "SELECT * FROM users"}, True),
    ("query_db", {"sql": "DROP TABLE users"}, False),
    ("query_db", {"sql": "SELECT * FROM users;-- comment"}, False),
    ("query_db", {"sql": "DELETE FROM users WHERE id=1"}, False),
    ("search_code", {"query": "../../etc/passwd"}, False),
    ("search_code", {"query": "auth handler"}, True),
    ("send_message", {"channel": "general", "text": "Hello"}, True),
    ("send_message", {"channel": "general", "text": "x" * 1001}, False),
    ("query_db", {"sql": 123}, False),  # not a string
]

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    results = []
    for tool, args, expected_valid in test_cases:
        is_valid, msg = validate_tool_input(tool, args)
        results.append((is_valid == expected_valid, tool, is_valid, msg))

    all_correct = all(r[0] for r in results)
    if all_correct:
        score += 1
        print("[PASS] Input validation works correctly:")
        for correct, tool, valid, msg in results:
            status = "VALID" if valid else f"BLOCKED: {msg}"
            print(f"       {tool:15s} → {status}")
    else:
        print("[FAIL] Some validation checks failed:")
        for i, (correct, tool, valid, msg) in enumerate(results):
            expected = test_cases[i][2]
            mark = "OK" if correct else "WRONG"
            print(f"       [{mark}] {tool}: valid={valid} (expected {expected}) msg={msg}")
except Exception as e:
    print(f"[FAIL] Validation error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Role-Based Access Control                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Implement role-based access control (RBAC)")
print("=" * 70)
print()

# Role definitions
rbac_policy = {
    "analyst": {
        "allowed_servers": ["postgres"],
        "allowed_tools": ["query_db", "list_tables"],
        "max_calls_per_hour": 100,
    },
    "developer": {
        "allowed_servers": ["postgres", "github", "slack"],
        "allowed_tools": ["query_db", "list_tables", "search_code", "create_pr", "send_message"],
        "max_calls_per_hour": 500,
    },
    "admin": {
        "allowed_servers": ["postgres", "github", "slack", "confluence", "salesforce"],
        "allowed_tools": ["*"],  # wildcard = all tools
        "max_calls_per_hour": 1000,
    },
}

def check_access(role: str, server: str, tool: str) -> Tuple[bool, str]:
    """Check if a role is allowed to call a specific tool on a server.

    Args:
        role: User role (analyst, developer, admin)
        server: MCP server name
        tool: Tool name to call

    Returns:
        Tuple of (allowed: bool, reason: str)
    """
    # TODO: Implement RBAC check.
    #
    # Hint:
    #   policy = rbac_policy.get(role)
    #   if policy is None:
    #       return (False, f"Unknown role: {role}")
    #   if server not in policy["allowed_servers"]:
    #       return (False, f"Role '{role}' cannot access server '{server}'")
    #   if "*" not in policy["allowed_tools"] and tool not in policy["allowed_tools"]:
    #       return (False, f"Role '{role}' cannot use tool '{tool}'")
    #   return (True, "Access granted")

    return "___"  # Replace with your implementation

# Test cases
access_tests = [
    ("analyst",   "postgres", "query_db",     True),
    ("analyst",   "github",   "search_code",  False),
    ("developer", "github",   "search_code",  True),
    ("developer", "salesforce", "query_crm",  False),
    ("admin",     "salesforce", "query_crm",  True),
    ("intern",    "postgres",  "query_db",    False),
]

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    results = []
    for role, server, tool, expected in access_tests:
        allowed, reason = check_access(role, server, tool)
        results.append((allowed == expected, role, server, tool, allowed, reason))

    all_correct = all(r[0] for r in results)
    if all_correct:
        score += 1
        print("[PASS] RBAC works correctly:")
        for correct, role, server, tool, allowed, reason in results:
            status = "GRANTED" if allowed else f"DENIED: {reason}"
            print(f"       {role:10s} → {server:12s} → {tool:15s} → {status}")
    else:
        print("[FAIL] Some RBAC checks failed:")
        for i, (correct, role, server, tool, allowed, reason) in enumerate(results):
            mark = "OK" if correct else "WRONG"
            print(f"       [{mark}] {role} → {server} → {tool}: allowed={allowed} (expected {access_tests[i][3]})")
except Exception as e:
    print(f"[FAIL] RBAC error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Audit Logger                                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Implement an audit logger for MCP tool calls")
print("=" * 70)
print()

class AuditLogger:
    """Logs all MCP tool calls for compliance and monitoring."""

    def __init__(self, log_dir: str):
        """Initialize the audit logger.

        Args:
            log_dir: Directory to write audit logs
        """
        self.log_dir = log_dir
        self.entries = []
        os.makedirs(log_dir, exist_ok=True)

    def log_call(self, user: str, role: str, server: str, tool: str,
                 arguments: Dict, allowed: bool, result: str) -> Dict:
        """Log a tool call attempt.

        Args:
            user: Username making the call
            role: User's role
            server: MCP server name
            tool: Tool name
            arguments: Tool arguments
            allowed: Whether RBAC allowed the call
            result: "success", "denied", or "validation_failed"

        Returns:
            The log entry dict
        """
        # TODO: Create a log entry and append it to self.entries.
        #
        # The entry should be a dict with:
        #   timestamp: datetime.now().isoformat()
        #   user: user
        #   role: role
        #   server: server
        #   tool: tool
        #   arguments: arguments
        #   allowed: allowed
        #   result: result
        #
        # Also write the entry as a JSON line to {log_dir}/audit.jsonl
        #
        # Hint:
        #   entry = {
        #       "timestamp": datetime.now().isoformat(),
        #       "user": user,
        #       "role": role,
        #       "server": server,
        #       "tool": tool,
        #       "arguments": arguments,
        #       "allowed": allowed,
        #       "result": result,
        #   }
        #   self.entries.append(entry)
        #   log_path = os.path.join(self.log_dir, "audit.jsonl")
        #   with open(log_path, "a") as f:
        #       f.write(json.dumps(entry) + "\n")
        #   return entry

        return "___"  # Replace with your implementation

    def get_summary(self) -> Dict[str, Any]:
        """Generate a summary of audit log entries.

        Returns:
            Dict with: total_calls, allowed_count, denied_count,
            calls_by_user (dict), calls_by_server (dict)
        """
        # TODO: Summarize the audit log.
        #
        # Hint:
        #   allowed_count = sum(1 for e in self.entries if e["allowed"])
        #   denied_count = len(self.entries) - allowed_count
        #   calls_by_user = {}
        #   calls_by_server = {}
        #   for e in self.entries:
        #       calls_by_user[e["user"]] = calls_by_user.get(e["user"], 0) + 1
        #       calls_by_server[e["server"]] = calls_by_server.get(e["server"], 0) + 1
        #   return {
        #       "total_calls": len(self.entries),
        #       "allowed_count": allowed_count,
        #       "denied_count": denied_count,
        #       "calls_by_user": calls_by_user,
        #       "calls_by_server": calls_by_server,
        #   }

        return "___"  # Replace with your implementation

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    logger = AuditLogger(os.path.join(WORKDIR, "audit"))

    # Simulate some tool calls
    logger.log_call("alice", "analyst", "postgres", "query_db",
                    {"sql": "SELECT * FROM sales"}, True, "success")
    logger.log_call("alice", "analyst", "github", "search_code",
                    {"query": "auth"}, False, "denied")
    logger.log_call("bob", "developer", "github", "create_pr",
                    {"title": "Fix bug"}, True, "success")
    logger.log_call("bob", "developer", "postgres", "query_db",
                    {"sql": "DROP TABLE users"}, True, "validation_failed")
    logger.log_call("carol", "admin", "salesforce", "query_crm",
                    {"query": "pipeline"}, True, "success")

    summary = logger.get_summary()

    checks = [
        len(logger.entries) == 5,
        isinstance(logger.entries[0], dict),
        "timestamp" in logger.entries[0],
        logger.entries[0]["user"] == "alice",
        isinstance(summary, dict),
        summary.get("total_calls") == 5,
        summary.get("allowed_count") == 4,
        summary.get("denied_count") == 1,
        summary.get("calls_by_user", {}).get("alice") == 2,
        summary.get("calls_by_user", {}).get("bob") == 2,
        summary.get("calls_by_server", {}).get("postgres") == 2,
        os.path.exists(os.path.join(WORKDIR, "audit", "audit.jsonl")),
    ]
    if all(checks):
        score += 1
        print("[PASS] Audit logger works correctly:")
        print(f"       Total calls:  {summary['total_calls']}")
        print(f"       Allowed:      {summary['allowed_count']}")
        print(f"       Denied:       {summary['denied_count']}")
        print(f"       By user:      {summary['calls_by_user']}")
        print(f"       By server:    {summary['calls_by_server']}")
        print(f"       Log file:     {os.path.join(WORKDIR, 'audit', 'audit.jsonl')}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Audit checks failed at indices: {failed}")
        if isinstance(summary, dict):
            print(f"       Summary: {json.dumps(summary, indent=2)}")
except Exception as e:
    print(f"[FAIL] Audit error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 07 Score: {score}/{total}")
print("=" * 70)
