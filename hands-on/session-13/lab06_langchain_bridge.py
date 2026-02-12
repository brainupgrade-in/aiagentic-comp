#!/usr/bin/env python3
"""
Lab 06: MCP-to-LangChain Bridge

Build adapters that convert MCP tools to LangChain-compatible tools,
create a multi-tool bridge, and implement agent tool selection logic.

No external packages required — standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any, Callable, Optional

WORKDIR = "/tmp/aidev-lab-13-06"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Why Bridge MCP and LangChain?                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: Why Bridge MCP and LangChain?")
print("=" * 70)
print()
print("  MCP provides standardized tool access across agents.")
print("  LangChain/LangGraph provides orchestration and agent loops.")
print("  The bridge gives you both:")
print()
print("  ┌──────────────────────────────────────────────────────────────────┐")
print("  │  MCP Servers  ──bridge──▶  LangChain Tools  ──▶  ReAct Agent   │")
print("  │                                                                  │")
print("  │  postgres     ──────────▶  query_db tool     ──▶  Agent picks  │")
print("  │  github       ──────────▶  search_code tool  ──▶  the right    │")
print("  │  slack        ──────────▶  send_msg tool     ──▶  tool to call │")
print("  └──────────────────────────────────────────────────────────────────┘")
print()
print("  In production: langchain-mcp-adapters does this automatically.")
print("  In this lab: we build a simplified version to understand the pattern.")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — Data Structures                                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: Tool Data Structures")
print("=" * 70)
print()

# MCP tool format (as returned by tools/list)
mcp_tools = [
    {
        "name": "query_db",
        "description": "Execute read-only SQL queries against the database",
        "inputSchema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string", "description": "SQL query to execute"},
            },
            "required": ["sql"],
        },
        "server": "postgres",
    },
    {
        "name": "search_code",
        "description": "Search for code patterns across repositories",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search pattern"},
                "repo": {"type": "string", "description": "Repository name"},
            },
            "required": ["query"],
        },
        "server": "github",
    },
    {
        "name": "send_message",
        "description": "Send a message to a Slack channel",
        "inputSchema": {
            "type": "object",
            "properties": {
                "channel": {"type": "string", "description": "Channel name"},
                "text": {"type": "string", "description": "Message text"},
            },
            "required": ["channel", "text"],
        },
        "server": "slack",
    },
    {
        "name": "search_wiki",
        "description": "Search Confluence knowledge base",
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"},
            },
            "required": ["query"],
        },
        "server": "confluence",
    },
]

# LangChain tool format (simplified)
# {
#     "name": "...",
#     "description": "...",
#     "parameters": {...},  # same as inputSchema
#     "func": callable,     # function to invoke the tool
#     "source": "mcp",
#     "mcp_server": "...",
# }

# Simulated MCP client that executes tool calls
def mock_mcp_call(server: str, tool_name: str, arguments: Dict) -> str:
    """Simulate calling an MCP tool via the client."""
    return json.dumps({"server": server, "tool": tool_name, "args": arguments, "status": "ok"})

print("  MCP tools loaded: query_db, search_code, send_message, search_wiki")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Build an MCP-to-LangChain Adapter                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Convert a single MCP tool to LangChain format")
print("=" * 70)
print()

def adapt_mcp_tool(mcp_tool: Dict) -> Dict:
    """Convert an MCP tool definition to LangChain-compatible format.

    Args:
        mcp_tool: Dict with name, description, inputSchema, server

    Returns:
        Dict with: name, description, parameters, func (callable),
        source ("mcp"), mcp_server
    """
    # TODO: Create a LangChain-compatible tool dict.
    #
    # The key transformation:
    #   - "inputSchema" becomes "parameters"
    #   - Add a "func" key with a lambda that calls mock_mcp_call
    #   - Add "source": "mcp" and "mcp_server": mcp_tool["server"]
    #
    # Hint:
    #   server = mcp_tool["server"]
    #   name = mcp_tool["name"]
    #   return {
    #       "name": name,
    #       "description": mcp_tool["description"],
    #       "parameters": mcp_tool["inputSchema"],
    #       "func": lambda args, _s=server, _n=name: mock_mcp_call(_s, _n, args),
    #       "source": "mcp",
    #       "mcp_server": server,
    #   }

    return "___"  # Replace with your implementation

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    adapted = adapt_mcp_tool(mcp_tools[0])  # query_db
    checks = [
        isinstance(adapted, dict),
        adapted.get("name") == "query_db",
        adapted.get("description") == mcp_tools[0]["description"],
        adapted.get("parameters") == mcp_tools[0]["inputSchema"],
        adapted.get("source") == "mcp",
        adapted.get("mcp_server") == "postgres",
        callable(adapted.get("func")),
    ]
    # Test the func
    if callable(adapted.get("func")):
        result = adapted["func"]({"sql": "SELECT 1"})
        parsed = json.loads(result)
        checks.append(parsed.get("tool") == "query_db")
        checks.append(parsed.get("server") == "postgres")

    if all(checks):
        score += 1
        print("[PASS] MCP-to-LangChain adapter works:")
        print(f"       Name:       {adapted['name']}")
        print(f"       Source:     {adapted['source']}")
        print(f"       MCP Server: {adapted['mcp_server']}")
        test_result = adapted["func"]({"sql": "SELECT 1"})
        print(f"       Test call:  {test_result}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Adapter checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Adapter error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Build a Multi-Tool Bridge                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Bridge all MCP tools to LangChain format")
print("=" * 70)
print()

def bridge_all_tools(mcp_tools: List[Dict]) -> List[Dict]:
    """Convert all MCP tools to LangChain-compatible format.

    Args:
        mcp_tools: List of MCP tool definitions

    Returns:
        List of LangChain-compatible tool dicts
    """
    # TODO: Apply adapt_mcp_tool to each MCP tool and return the list.
    #
    # Hint:
    #   return [adapt_mcp_tool(tool) for tool in mcp_tools]

    return "___"  # Replace with your implementation

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    bridged = bridge_all_tools(mcp_tools)
    checks = [
        isinstance(bridged, list),
        len(bridged) == 4,
        all(isinstance(t, dict) for t in bridged),
        all(t.get("source") == "mcp" for t in bridged),
        [t["name"] for t in bridged] == ["query_db", "search_code", "send_message", "search_wiki"],
        all(callable(t.get("func")) for t in bridged),
    ]
    if all(checks):
        score += 1
        print("[PASS] Multi-tool bridge works:")
        for t in bridged:
            print(f"       {t['name']:15s} from {t['mcp_server']}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Bridge checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Bridge error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Agent Tool Selection Logic                                       ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Implement agent tool selection logic")
print("=" * 70)
print()

def select_tool(query: str, tools: List[Dict]) -> Optional[Dict]:
    """Select the best tool for a user query using keyword matching.

    Simple matching rules (check in order):
        - If query contains "sql" or "database" or "query" → query_db
        - If query contains "code" or "repository" or "search code" → search_code
        - If query contains "message" or "slack" or "notify" → send_message
        - If query contains "wiki" or "knowledge" or "confluence" → search_wiki
        - Otherwise → None

    Args:
        query: User's natural language query (lowercase)
        tools: List of LangChain-compatible tool dicts

    Returns:
        The matching tool dict, or None if no match
    """
    # TODO: Implement keyword-based tool selection.
    #
    # Hint:
    #   q = query.lower()
    #   tool_map = {t["name"]: t for t in tools}
    #   if any(kw in q for kw in ["sql", "database", "query"]):
    #       return tool_map.get("query_db")
    #   elif any(kw in q for kw in ["code", "repository", "search code"]):
    #       return tool_map.get("search_code")
    #   elif any(kw in q for kw in ["message", "slack", "notify"]):
    #       return tool_map.get("send_message")
    #   elif any(kw in q for kw in ["wiki", "knowledge", "confluence"]):
    #       return tool_map.get("search_wiki")
    #   return None

    return "___"  # Replace with your implementation

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    # We need bridged tools from TODO 2
    if isinstance(bridged, list) and len(bridged) == 4:
        test_tools = bridged
    else:
        # Fallback if TODO 2 not done
        test_tools = [adapt_mcp_tool(t) if callable(getattr(adapt_mcp_tool, '__call__', None)) else {} for t in mcp_tools]

    r1 = select_tool("run a sql query on the database", test_tools)
    r2 = select_tool("search the code repository for auth bugs", test_tools)
    r3 = select_tool("send a slack message to the team", test_tools)
    r4 = select_tool("find information in the wiki", test_tools)
    r5 = select_tool("make me a sandwich", test_tools)

    checks = [
        r1 is not None and r1.get("name") == "query_db",
        r2 is not None and r2.get("name") == "search_code",
        r3 is not None and r3.get("name") == "send_message",
        r4 is not None and r4.get("name") == "search_wiki",
        r5 is None,
    ]
    if all(checks):
        score += 1
        print("[PASS] Tool selection works:")
        print(f"       'sql query on database'  → {r1['name']}")
        print(f"       'search code repository'  → {r2['name']}")
        print(f"       'slack message'            → {r3['name']}")
        print(f"       'find in wiki'             → {r4['name']}")
        print(f"       'make me a sandwich'       → None (no match)")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Selection checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Selection error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 4 — Full Bridge Workflow                                             ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 4: Execute a full bridge workflow")
print("=" * 70)
print()

def run_bridge_workflow(queries: List[str], tools: List[Dict]) -> Dict[str, Any]:
    """Process a list of queries through the MCP-LangChain bridge.

    For each query:
        1. Select the best tool
        2. If found, call it with appropriate arguments
        3. Log the result

    Args:
        queries: List of user queries
        tools: List of LangChain-compatible tools

    Returns:
        Dict with:
            total_queries: number of queries
            matched: number of queries that found a tool
            unmatched: number of queries with no tool match
            results: list of dicts with query, tool_name, server, result
    """
    # TODO: Implement the bridge workflow.
    #
    # Hint:
    #   results = []
    #   matched = 0
    #   for query in queries:
    #       tool = select_tool(query, tools)
    #       if tool is not None:
    #           matched += 1
    #           # Create simple arguments based on query
    #           result = tool["func"]({"input": query})
    #           results.append({
    #               "query": query,
    #               "tool_name": tool["name"],
    #               "server": tool["mcp_server"],
    #               "result": result,
    #           })
    #       else:
    #           results.append({
    #               "query": query,
    #               "tool_name": None,
    #               "server": None,
    #               "result": "No matching tool found",
    #           })
    #   return {
    #       "total_queries": len(queries),
    #       "matched": matched,
    #       "unmatched": len(queries) - matched,
    #       "results": results,
    #   }

    return "___"  # Replace with your implementation

# ── Validate TODO 4 ─────────────────────────────────────────────────────────
total += 1
try:
    test_queries = [
        "query the database for recent orders",
        "search code for authentication bugs",
        "notify the team on slack about the deployment",
        "look up the runbook in confluence",
        "what is the meaning of life",
    ]
    if isinstance(bridged, list) and len(bridged) == 4:
        test_tools = bridged
    else:
        test_tools = []

    result = run_bridge_workflow(test_queries, test_tools)
    checks = [
        isinstance(result, dict),
        result.get("total_queries") == 5,
        result.get("matched") == 4,
        result.get("unmatched") == 1,
        len(result.get("results", [])) == 5,
        result["results"][0].get("tool_name") == "query_db",
        result["results"][1].get("tool_name") == "search_code",
        result["results"][2].get("tool_name") == "send_message",
        result["results"][3].get("tool_name") == "search_wiki",
        result["results"][4].get("tool_name") is None,
    ]
    if all(checks):
        score += 1
        print("[PASS] Bridge workflow completed:")
        print(f"       Total: {result['total_queries']}, Matched: {result['matched']}, "
              f"Unmatched: {result['unmatched']}")
        for r in result["results"]:
            status = f"→ {r['tool_name']} ({r['server']})" if r["tool_name"] else "→ No match"
            print(f"       '{r['query'][:40]:40s}' {status}")
        out_path = os.path.join(WORKDIR, "bridge_workflow.json")
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
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 06 Score: {score}/{total}")
print("=" * 70)
