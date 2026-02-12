#!/usr/bin/env python3
"""
Lab 08: Challenge — Enterprise MCP Agent System

Build a complete enterprise MCP agent system that combines:
server catalog, client configuration, security pipeline, and
a multi-server workflow with full audit logging.

No external packages required — standard library only.
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional

WORKDIR = "/tmp/aidev-lab-13-08"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

print("=" * 70)
print("CHALLENGE: Build a Complete Enterprise MCP Agent System")
print("=" * 70)
print()
print("  You will build:")
print("    1. Enterprise server catalog with readiness scoring")
print("    2. Role-based multi-server config generator")
print("    3. Security pipeline (validation + RBAC + audit)")
print("    4. Full enterprise agent workflow tying it all together")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Enterprise Server Catalog with Scoring                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Build an enterprise server catalog with readiness scores")
print("=" * 70)
print()

def build_catalog() -> List[Dict[str, Any]]:
    """Build an MCP server catalog with readiness scores.

    Each server entry has:
        name, category, tools (list), resources (list),
        maturity ("stable"/"beta"/"experimental"),
        readiness_score (stable=1.0, beta=0.7, experimental=0.3)

    Returns:
        List of 5 server entries, sorted by readiness_score descending
    """
    # TODO: Build the catalog with these 5 servers:
    #
    #   1. name="postgres", category="data", tools=["query_db", "list_tables"],
    #      resources=["db://schema", "db://stats"], maturity="stable"
    #   2. name="github", category="developer", tools=["search_code", "create_pr", "list_issues"],
    #      resources=["repo://files"], maturity="stable"
    #   3. name="slack", category="communication", tools=["send_message", "search_messages"],
    #      resources=[], maturity="stable"
    #   4. name="confluence", category="knowledge", tools=["search_pages"],
    #      resources=["wiki://pages"], maturity="beta"
    #   5. name="kubernetes", category="cloud", tools=["get_pods", "get_logs"],
    #      resources=["k8s://namespaces"], maturity="beta"
    #
    # Add readiness_score based on maturity: stable=1.0, beta=0.7, experimental=0.3
    # Sort by readiness_score descending (stable first)
    #
    # Hint:
    #   maturity_scores = {"stable": 1.0, "beta": 0.7, "experimental": 0.3}
    #   catalog = [
    #       {"name": "postgres", "category": "data",
    #        "tools": ["query_db", "list_tables"], "resources": ["db://schema", "db://stats"],
    #        "maturity": "stable", "readiness_score": 1.0},
    #       ...
    #   ]
    #   return sorted(catalog, key=lambda x: x["readiness_score"], reverse=True)

    return "___"  # Replace with your implementation

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    catalog = build_catalog()
    checks = [
        isinstance(catalog, list),
        len(catalog) == 5,
        catalog[0]["maturity"] == "stable",  # stable comes first
        catalog[-1]["maturity"] == "beta",   # beta comes last
        all("readiness_score" in s for s in catalog),
        sum(1 for s in catalog if s["readiness_score"] == 1.0) == 3,
        sum(1 for s in catalog if s["readiness_score"] == 0.7) == 2,
        any(s["name"] == "postgres" for s in catalog),
        any(s["name"] == "kubernetes" for s in catalog),
    ]
    if all(checks):
        score += 1
        print("[PASS] Enterprise catalog built:")
        for s in catalog:
            print(f"       {s['name']:12s} [{s['category']:13s}] "
                  f"score={s['readiness_score']:.1f}  "
                  f"{len(s['tools'])} tools, {len(s['resources'])} resources")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Catalog checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Catalog error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Role-Based Config Generator                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Generate role-based MCP client configurations")
print("=" * 70)
print()

role_permissions = {
    "analyst":   ["postgres"],
    "developer": ["postgres", "github", "slack"],
    "sre":       ["postgres", "github", "slack", "kubernetes"],
    "admin":     ["postgres", "github", "slack", "confluence", "kubernetes"],
}

server_configs = {
    "postgres":   {"command": "npx", "args": ["-y", "server-postgres", "postgresql://db/prod"]},
    "github":     {"command": "npx", "args": ["-y", "server-github"], "env": {"GITHUB_TOKEN": "ghp_xxx"}},
    "slack":      {"command": "npx", "args": ["-y", "server-slack"], "env": {"SLACK_TOKEN": "xoxb_xxx"}},
    "confluence": {"url": "https://mcp-gw.internal/confluence/sse"},
    "kubernetes": {"command": "npx", "args": ["-y", "server-kubernetes"], "env": {"KUBECONFIG": "/etc/kube/config"}},
}

def generate_configs(roles: List[str]) -> Dict[str, Dict]:
    """Generate MCP configs for multiple roles.

    Args:
        roles: List of role names

    Returns:
        Dict mapping role → MCP config ({"mcpServers": {...}})
    """
    # TODO: For each role, build a config with only the allowed servers.
    #
    # Hint:
    #   configs = {}
    #   for role in roles:
    #       allowed = role_permissions.get(role, [])
    #       configs[role] = {
    #           "mcpServers": {
    #               name: server_configs[name]
    #               for name in allowed
    #               if name in server_configs
    #           }
    #       }
    #   return configs

    return "___"  # Replace with your implementation

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    configs = generate_configs(["analyst", "developer", "sre", "admin"])
    checks = [
        isinstance(configs, dict),
        len(configs) == 4,
        len(configs.get("analyst", {}).get("mcpServers", {})) == 1,
        len(configs.get("developer", {}).get("mcpServers", {})) == 3,
        len(configs.get("sre", {}).get("mcpServers", {})) == 4,
        len(configs.get("admin", {}).get("mcpServers", {})) == 5,
        "kubernetes" in configs.get("sre", {}).get("mcpServers", {}),
        "confluence" in configs.get("admin", {}).get("mcpServers", {}),
    ]
    if all(checks):
        score += 1
        print("[PASS] Role-based configs generated:")
        for role, cfg in configs.items():
            servers = list(cfg["mcpServers"].keys())
            print(f"       {role:10s} → {servers}")
        out_path = os.path.join(WORKDIR, "role_configs.json")
        with open(out_path, "w") as f:
            json.dump(configs, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Config checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Config error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Security Pipeline                                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Build a security pipeline (validation + RBAC + audit)")
print("=" * 70)
print()

class SecurityPipeline:
    """Combines input validation, RBAC, and audit logging."""

    def __init__(self, log_dir: str):
        self.log_dir = log_dir
        self.audit_log = []
        os.makedirs(log_dir, exist_ok=True)

    def validate_input(self, tool: str, arguments: Dict) -> Tuple[bool, str]:
        """Validate tool arguments.

        Rules:
            - All argument values must be strings
            - No argument value may contain "../"
            - For query_db: SQL must start with SELECT (case-insensitive)
        """
        for key, value in arguments.items():
            if not isinstance(value, str):
                return (False, f"Argument '{key}' must be a string")
            if "../" in value:
                return (False, f"Argument '{key}' contains path traversal")
        if tool == "query_db":
            sql = arguments.get("sql", "").strip().upper()
            if not sql.startswith("SELECT"):
                return (False, "SQL must start with SELECT")
        return (True, "ok")

    def check_rbac(self, role: str, server: str, tool: str) -> Tuple[bool, str]:
        """Check RBAC permissions."""
        policy = role_permissions.get(role)
        if policy is None:
            return (False, f"Unknown role: {role}")
        if server not in policy:
            return (False, f"Role '{role}' cannot access server '{server}'")
        return (True, "Access granted")

    def process_call(self, user: str, role: str, server: str,
                     tool: str, arguments: Dict) -> Dict[str, Any]:
        """Process a tool call through the full security pipeline.

        Pipeline:
            1. Validate input
            2. Check RBAC
            3. "Execute" the tool (simulate with a success message)
            4. Log everything to audit trail

        Args:
            user, role, server, tool, arguments

        Returns:
            Dict with: user, role, server, tool, input_valid, access_granted,
            executed, result, timestamp
        """
        # TODO: Implement the security pipeline.
        #
        # Hint:
        #   timestamp = datetime.now().isoformat()
        #
        #   # Step 1: Validate
        #   input_valid, validation_msg = self.validate_input(tool, arguments)
        #   if not input_valid:
        #       entry = {"user": user, "role": role, "server": server, "tool": tool,
        #                "input_valid": False, "access_granted": False, "executed": False,
        #                "result": f"Validation failed: {validation_msg}", "timestamp": timestamp}
        #       self.audit_log.append(entry)
        #       return entry
        #
        #   # Step 2: RBAC
        #   access_granted, rbac_msg = self.check_rbac(role, server, tool)
        #   if not access_granted:
        #       entry = {"user": user, "role": role, "server": server, "tool": tool,
        #                "input_valid": True, "access_granted": False, "executed": False,
        #                "result": f"Access denied: {rbac_msg}", "timestamp": timestamp}
        #       self.audit_log.append(entry)
        #       return entry
        #
        #   # Step 3: Execute (simulated)
        #   execution_result = f"Executed {tool} on {server} with {arguments}"
        #   entry = {"user": user, "role": role, "server": server, "tool": tool,
        #            "input_valid": True, "access_granted": True, "executed": True,
        #            "result": execution_result, "timestamp": timestamp}
        #   self.audit_log.append(entry)
        #
        #   # Step 4: Write to log file
        #   log_path = os.path.join(self.log_dir, "security_audit.jsonl")
        #   with open(log_path, "a") as f:
        #       f.write(json.dumps(entry) + "\n")
        #
        #   return entry

        return "___"  # Replace with your implementation

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    pipeline = SecurityPipeline(os.path.join(WORKDIR, "security"))

    # Test cases
    r1 = pipeline.process_call("alice", "analyst", "postgres", "query_db", {"sql": "SELECT * FROM sales"})
    r2 = pipeline.process_call("alice", "analyst", "github", "search_code", {"query": "auth"})
    r3 = pipeline.process_call("bob", "developer", "postgres", "query_db", {"sql": "DROP TABLE users"})
    r4 = pipeline.process_call("bob", "developer", "github", "search_code", {"query": "../../etc/passwd"})
    r5 = pipeline.process_call("carol", "admin", "slack", "send_message", {"channel": "ops", "text": "Deployed v2"})

    checks = [
        isinstance(r1, dict),
        r1.get("executed") is True,       # analyst can query postgres
        r2.get("access_granted") is False, # analyst can't access github
        r3.get("input_valid") is False,    # DROP TABLE blocked
        r4.get("input_valid") is False,    # path traversal blocked
        r5.get("executed") is True,        # admin can do anything
        len(pipeline.audit_log) == 5,
        "timestamp" in r1,
    ]
    if all(checks):
        score += 1
        print("[PASS] Security pipeline works correctly:")
        for entry in pipeline.audit_log:
            status = "EXECUTED" if entry["executed"] else ("DENIED" if not entry["access_granted"] else "INVALID")
            print(f"       {entry['user']:8s} [{entry['role']:9s}] "
                  f"{entry['server']:10s}/{entry['tool']:15s} → {status}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Pipeline checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Pipeline error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 4 — Full Enterprise Agent Workflow                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 4: Run a full enterprise agent workflow")
print("=" * 70)
print()

def run_enterprise_agent(user: str, role: str, tasks: List[Dict],
                         pipeline: SecurityPipeline) -> Dict[str, Any]:
    """Execute a full enterprise agent workflow.

    The agent processes a list of tasks, each specifying a server,
    tool, and arguments. Each task goes through the security pipeline.

    Args:
        user: Username
        role: User role
        tasks: List of dicts with server, tool, arguments
        pipeline: SecurityPipeline instance

    Returns:
        Dict with:
            user: username
            role: role
            total_tasks: number of tasks
            executed: count of successfully executed tasks
            denied: count of access-denied tasks
            invalid: count of validation-failed tasks
            task_results: list of pipeline results
            summary: string description
    """
    # TODO: Process each task through the pipeline and build the report.
    #
    # Hint:
    #   task_results = []
    #   executed = 0
    #   denied = 0
    #   invalid = 0
    #   for task in tasks:
    #       result = pipeline.process_call(user, role, task["server"], task["tool"], task["arguments"])
    #       task_results.append(result)
    #       if result.get("executed"):
    #           executed += 1
    #       elif not result.get("input_valid"):
    #           invalid += 1
    #       else:
    #           denied += 1
    #   summary = (f"Agent '{user}' ({role}): {executed}/{len(tasks)} executed, "
    #              f"{denied} denied, {invalid} invalid")
    #   return {
    #       "user": user,
    #       "role": role,
    #       "total_tasks": len(tasks),
    #       "executed": executed,
    #       "denied": denied,
    #       "invalid": invalid,
    #       "task_results": task_results,
    #       "summary": summary,
    #   }

    return "___"  # Replace with your implementation

# ── Validate TODO 4 ─────────────────────────────────────────────────────────
total += 1
try:
    challenge_pipeline = SecurityPipeline(os.path.join(WORKDIR, "challenge_audit"))

    dev_tasks = [
        {"server": "postgres", "tool": "query_db", "arguments": {"sql": "SELECT COUNT(*) FROM orders"}},
        {"server": "github", "tool": "search_code", "arguments": {"query": "payment handler"}},
        {"server": "github", "tool": "create_pr", "arguments": {"title": "Fix payment bug"}},
        {"server": "slack", "tool": "send_message", "arguments": {"channel": "dev", "text": "PR ready for review"}},
        {"server": "salesforce", "tool": "query_crm", "arguments": {"query": "pipeline"}},  # should be denied
    ]

    report = run_enterprise_agent("dave", "developer", dev_tasks, challenge_pipeline)
    checks = [
        isinstance(report, dict),
        report.get("user") == "dave",
        report.get("role") == "developer",
        report.get("total_tasks") == 5,
        report.get("executed") == 4,
        report.get("denied") == 1,
        report.get("invalid") == 0,
        len(report.get("task_results", [])) == 5,
        isinstance(report.get("summary"), str),
        "dave" in report.get("summary", ""),
    ]
    if all(checks):
        score += 1
        print("[PASS] Enterprise agent workflow completed!")
        print(f"       {report['summary']}")
        print(f"       Task details:")
        for i, result in enumerate(report["task_results"]):
            status = "EXECUTED" if result["executed"] else ("DENIED" if not result["access_granted"] else "INVALID")
            print(f"         {i+1}. [{result['server']}/{result['tool']}] → {status}")
        # Save full report
        out_path = os.path.join(WORKDIR, "challenge_report.json")
        with open(out_path, "w") as f:
            json.dump(report, f, indent=2, default=str)
        print(f"       Report saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Workflow checks failed at indices: {failed}")
        if isinstance(report, dict):
            print(f"       Got: executed={report.get('executed')}, denied={report.get('denied')}, invalid={report.get('invalid')}")
except Exception as e:
    print(f"[FAIL] Workflow error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Challenge Lab 08 Score: {score}/{total}")
print("=" * 70)
if score == total:
    print("Congratulations! You completed the Enterprise MCP Challenge!")
else:
    print(f"Keep going — {total - score} check(s) remaining.")
print("=" * 70)
