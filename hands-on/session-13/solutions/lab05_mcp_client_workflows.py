#!/usr/bin/env python3
"""
Lab 05 Solution: MCP Client Workflows

Simulate MCP client lifecycle (initialize, discover, operate), build
enterprise workflows across multiple servers, and implement tool routing.

No external packages required — standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any, Optional

WORKDIR = "/tmp/aidev-lab-13-05"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — MCP Connection Lifecycle                                         ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: MCP Connection Lifecycle")
print("=" * 70)
print()
print("  The MCP client-server connection follows 4 phases:")
print()
print("  ┌─────┬─────────────┬─────────────────────────────────────────────┐")
print("  │ #   │ Phase       │ What Happens                                │")
print("  ├─────┼─────────────┼─────────────────────────────────────────────┤")
print("  │ 1   │ Initialize  │ Exchange capabilities, agree on protocol    │")
print("  │ 2   │ Discover    │ Client calls tools/list, resources/list     │")
print("  │ 3   │ Operate     │ Client calls tools, reads resources         │")
print("  │ 4   │ Shutdown    │ Clean disconnect                            │")
print("  └─────┴─────────────┴─────────────────────────────────────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — Mock MCP Server                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: Mock MCP Server (simulates real server responses)")
print("=" * 70)
print()

class MockMCPServer:
    """Simulates an MCP server for client workflow testing."""

    def __init__(self, name: str, tools: List[Dict], resources: List[Dict]):
        self.name = name
        self.tools = tools
        self.resources = resources
        self.initialized = False

    def handle_request(self, method: str, params: Dict = None) -> Dict:
        """Handle a JSON-RPC style request."""
        if method == "initialize":
            self.initialized = True
            return {
                "protocolVersion": "2024-11-05",
                "serverInfo": {"name": self.name, "version": "1.0.0"},
                "capabilities": {
                    "tools": {"listChanged": True},
                    "resources": {"subscribe": True},
                },
            }
        elif method == "tools/list":
            return {"tools": self.tools}
        elif method == "resources/list":
            return {"resources": self.resources}
        elif method == "tools/call":
            tool_name = (params or {}).get("name", "")
            args = (params or {}).get("arguments", {})
            return {
                "content": [{"type": "text", "text": f"Executed {tool_name} with {args}"}]
            }
        elif method == "resources/read":
            uri = (params or {}).get("uri", "")
            return {
                "contents": [{"uri": uri, "text": f"Content of {uri}"}]
            }
        return {"error": f"Unknown method: {method}"}


db_server = MockMCPServer(
    name="postgres",
    tools=[
        {"name": "query_db", "description": "Execute read-only SQL"},
        {"name": "list_tables", "description": "List database tables"},
    ],
    resources=[
        {"uri": "db://schema", "name": "Database Schema"},
    ],
)

github_server = MockMCPServer(
    name="github",
    tools=[
        {"name": "search_code", "description": "Search code in repos"},
        {"name": "create_pr", "description": "Create a pull request"},
        {"name": "list_issues", "description": "List repository issues"},
    ],
    resources=[
        {"uri": "repo://files", "name": "Repository Files"},
        {"uri": "repo://branches", "name": "Repository Branches"},
    ],
)

print("  Mock servers created: postgres (2 tools, 1 resource)")
print("                        github  (3 tools, 2 resources)")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Implement Client Lifecycle                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Implement the MCP client lifecycle for a single server")
print("=" * 70)
print()

def run_client_lifecycle(server: MockMCPServer) -> Dict[str, Any]:
    """Execute the full MCP client lifecycle against a server."""
    # Phase 1: Initialize
    init_result = server.handle_request("initialize")

    # Phase 2: Discover
    tools_result = server.handle_request("tools/list")
    resources_result = server.handle_request("resources/list")
    tools = tools_result["tools"]
    resources = resources_result["resources"]

    # Phase 3: Operate
    tool_results = {}
    for tool in tools:
        result = server.handle_request("tools/call", {"name": tool["name"], "arguments": {}})
        tool_results[tool["name"]] = result

    resource_results = {}
    for res in resources:
        result = server.handle_request("resources/read", {"uri": res["uri"]})
        resource_results[res["uri"]] = result

    # Phase 4: Shutdown
    server.initialized = False

    return {
        "server_name": server.name,
        "init_result": init_result,
        "tools": [t["name"] for t in tools],
        "resources": [r["uri"] for r in resources],
        "tool_results": tool_results,
        "resource_results": resource_results,
        "phases_completed": 4,
    }

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    result = run_client_lifecycle(db_server)
    checks = [
        isinstance(result, dict),
        result.get("server_name") == "postgres",
        result.get("phases_completed") == 4,
        result.get("tools") == ["query_db", "list_tables"],
        result.get("resources") == ["db://schema"],
        "query_db" in result.get("tool_results", {}),
        "list_tables" in result.get("tool_results", {}),
        "db://schema" in result.get("resource_results", {}),
        db_server.initialized is False,
    ]
    if all(checks):
        score += 1
        print("[PASS] Client lifecycle completed for postgres:")
        print(f"       Tools:     {result['tools']}")
        print(f"       Resources: {result['resources']}")
        print(f"       Phases:    {result['phases_completed']}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Lifecycle checks failed at indices: {failed}")
        print(f"       Got: {result}")
except Exception as e:
    print(f"[FAIL] Lifecycle error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Enterprise Multi-Server Workflow                                 ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Run an enterprise workflow across multiple servers")
print("=" * 70)
print()

def run_enterprise_workflow(servers: List[MockMCPServer]) -> Dict[str, Any]:
    """Execute a workflow that spans multiple MCP servers."""
    # Step 1 & 2: Initialize and discover all servers
    all_tools = []
    all_resources = []
    unified_registry = {}

    for server in servers:
        server.handle_request("initialize")
        tools_resp = server.handle_request("tools/list")
        res_resp = server.handle_request("resources/list")
        for t in tools_resp["tools"]:
            all_tools.append(t["name"])
            unified_registry[t["name"]] = server.name
        for r in res_resp["resources"]:
            all_resources.append(r["uri"])

    # Step 3: Execute cross-server workflow
    workflow_log = []

    # Read database schema
    servers[0].handle_request("resources/read", {"uri": "db://schema"})
    workflow_log.append({"step": 1, "server": "postgres", "action": "resources/read",
                         "result_summary": "Read database schema"})

    # Query the database
    servers[0].handle_request("tools/call", {"name": "query_db", "arguments": {"sql": "SELECT * FROM errors"}})
    workflow_log.append({"step": 2, "server": "postgres", "action": "tools/call",
                         "result_summary": "Queried error table"})

    # Search code for related issue
    servers[1].handle_request("tools/call", {"name": "search_code", "arguments": {"query": "error handler"}})
    workflow_log.append({"step": 3, "server": "github", "action": "tools/call",
                         "result_summary": "Searched code for error handler"})

    # Create a PR with the fix
    servers[1].handle_request("tools/call", {"name": "create_pr", "arguments": {"title": "Fix error handling"}})
    workflow_log.append({"step": 4, "server": "github", "action": "tools/call",
                         "result_summary": "Created PR for fix"})

    # Shutdown all
    for server in servers:
        server.initialized = False

    return {
        "server_count": len(servers),
        "all_tools": sorted(all_tools),
        "all_resources": sorted(all_resources),
        "unified_registry": unified_registry,
        "workflow_log": workflow_log,
    }

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    db_server2 = MockMCPServer("postgres",
        [{"name": "query_db", "description": "SQL"}, {"name": "list_tables", "description": "Tables"}],
        [{"uri": "db://schema", "name": "Schema"}])
    gh_server2 = MockMCPServer("github",
        [{"name": "search_code", "description": "Search"}, {"name": "create_pr", "description": "PR"},
         {"name": "list_issues", "description": "Issues"}],
        [{"uri": "repo://files", "name": "Files"}, {"uri": "repo://branches", "name": "Branches"}])

    result = run_enterprise_workflow([db_server2, gh_server2])
    checks = [
        isinstance(result, dict),
        result.get("server_count") == 2,
        len(result.get("all_tools", [])) == 5,
        len(result.get("all_resources", [])) == 3,
        result.get("unified_registry", {}).get("query_db") == "postgres",
        result.get("unified_registry", {}).get("search_code") == "github",
        len(result.get("workflow_log", [])) == 4,
        result["workflow_log"][0]["server"] == "postgres",
        result["workflow_log"][2]["server"] == "github",
    ]
    if all(checks):
        score += 1
        print("[PASS] Enterprise workflow completed:")
        print(f"       Servers:   {result['server_count']}")
        print(f"       Tools:     {result['all_tools']}")
        print(f"       Resources: {result['all_resources']}")
        print(f"       Workflow steps:")
        for step in result["workflow_log"]:
            print(f"         Step {step['step']}: [{step['server']}] {step['result_summary']}")
        out_path = os.path.join(WORKDIR, "enterprise_workflow.json")
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Workflow checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Workflow error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Implement Tool Routing                                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Implement tool routing across MCP servers")
print("=" * 70)
print()

def route_tool_call(tool_name: str, arguments: Dict,
                    registry: Dict[str, str],
                    servers: Dict[str, MockMCPServer]) -> Dict[str, Any]:
    """Route a tool call to the correct MCP server."""
    server_name = registry.get(tool_name)
    if server_name is None:
        return {"tool": tool_name, "server": None, "result": {"error": f"Tool '{tool_name}' not found"}, "routed": False}
    server = servers.get(server_name)
    if server is None:
        return {"tool": tool_name, "server": server_name, "result": {"error": f"Server '{server_name}' not available"}, "routed": False}
    result = server.handle_request("tools/call", {"name": tool_name, "arguments": arguments})
    return {"tool": tool_name, "server": server_name, "result": result, "routed": True}

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    registry = {"query_db": "postgres", "search_code": "github", "create_pr": "github"}
    server_map = {"postgres": db_server, "github": github_server}

    db_server.handle_request("initialize")
    github_server.handle_request("initialize")

    r1 = route_tool_call("query_db", {"sql": "SELECT 1"}, registry, server_map)
    r2 = route_tool_call("search_code", {"query": "main"}, registry, server_map)
    r3 = route_tool_call("unknown_tool", {}, registry, server_map)

    checks = [
        r1.get("routed") is True,
        r1.get("server") == "postgres",
        r1.get("tool") == "query_db",
        r2.get("routed") is True,
        r2.get("server") == "github",
        r3.get("routed") is False,
        "not found" in str(r3.get("result", {}).get("error", "")).lower(),
    ]
    if all(checks):
        score += 1
        print("[PASS] Tool routing works correctly:")
        print(f"       query_db    → routed to {r1['server']}")
        print(f"       search_code → routed to {r2['server']}")
        print(f"       unknown     → {r3['result']}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Routing checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Routing error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 05 Score: {score}/{total}")
print("=" * 70)
