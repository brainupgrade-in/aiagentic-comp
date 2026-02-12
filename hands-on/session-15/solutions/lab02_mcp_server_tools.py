#!/usr/bin/env python3
"""
Lab 02 Solution: Build MCP Server with Tools

Design an MCP server specification with tools for the capstone project.
Define tool schemas (JSON), map tool names to descriptions, and specify
resource URIs. All output written as JSON files to WORKDIR.

No external packages required -- standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any

WORKDIR = "/tmp/capstone-lab-15-02"

# -- Cleanup & Setup ---------------------------------------------------------
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ============================================================================
# STEP 1 -- MCP Tool Schema Structure
# ============================================================================

print("=" * 70)
print("STEP 1: MCP Tool Schema Structure")
print("=" * 70)
print()
print("  Every MCP tool has a JSON schema with these fields:")
print()
print("  +------------------+----------------------------------------------+")
print("  | Field            | Description                                  |")
print("  +------------------+----------------------------------------------+")
print("  | name             | Unique tool identifier (snake_case)          |")
print("  | description      | What the tool does (for LLM to understand)  |")
print("  | inputSchema      | JSON Schema for the tool's parameters       |")
print("  |   type           | Always 'object'                             |")
print("  |   properties     | Dict of parameter name -> {type, desc}      |")
print("  |   required       | List of required parameter names            |")
print("  +------------------+----------------------------------------------+")
print()
print("  Example tool schema:")
print()
print('  {')
print('    "name": "search_docs",')
print('    "description": "Search knowledge base documents",')
print('    "inputSchema": {')
print('      "type": "object",')
print('      "properties": {')
print('        "query": {"type": "string", "description": "Search query"}')
print('      },')
print('      "required": ["query"]')
print('    }')
print('  }')
print()

# ============================================================================
# STEP 2 -- MCP Resource URI Patterns
# ============================================================================

print("=" * 70)
print("STEP 2: MCP Resource URI Patterns")
print("=" * 70)
print()
print("  Resources use URI schemes to identify data sources:")
print()
print("  +---------------------+------------------------------------------+")
print("  | URI Pattern         | Example                                  |")
print("  +---------------------+------------------------------------------+")
print("  | file://{path}       | file://knowledge-base/docs               |")
print("  | db://{table}        | db://tickets                             |")
print("  | config://{section}  | config://agent-settings                  |")
print("  | api://{service}     | api://support-history                    |")
print("  +---------------------+------------------------------------------+")
print()

# ============================================================================
# STEP 3 -- Capstone Tool Requirements
# ============================================================================

print("=" * 70)
print("STEP 3: Capstone Support Agent -- Required Tools")
print("=" * 70)
print()
print("  Our AI Support Agent needs four tools:")
print()
print("  1. search_knowledge  -- Search the knowledge base for answers")
print("  2. create_ticket     -- Create a new support ticket")
print("  3. get_ticket_status -- Look up status of an existing ticket")
print("  4. escalate_ticket   -- Escalate a ticket to a human agent")
print()

# ============================================================================
# TODO 1 -- Define search_knowledge Tool Schema
# ============================================================================

print("=" * 70)
print("TODO 1: Define the search_knowledge tool schema")
print("=" * 70)
print()

search_knowledge_tool = {
    "name": "search_knowledge",
    "description": "Search the knowledge base for relevant support articles",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query text"},
            "max_results": {"type": "integer", "description": "Maximum number of results to return"},
        },
        "required": ["query"],
    },
}

# -- Validate TODO 1 --------------------------------------------------------
total += 1
expected_search = {
    "name": "search_knowledge",
    "description": "Search the knowledge base for relevant support articles",
    "inputSchema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "The search query text"},
            "max_results": {"type": "integer", "description": "Maximum number of results to return"},
        },
        "required": ["query"],
    },
}
if search_knowledge_tool == expected_search:
    score += 1
    print("[PASS] search_knowledge tool schema is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_search, indent=2))
    print("       Got:     ", json.dumps(search_knowledge_tool, indent=2) if isinstance(search_knowledge_tool, dict) else search_knowledge_tool)
print()

# ============================================================================
# TODO 2 -- Define create_ticket Tool Schema
# ============================================================================

print("=" * 70)
print("TODO 2: Define the create_ticket tool schema")
print("=" * 70)
print()

create_ticket_tool = {
    "name": "create_ticket",
    "description": "Create a new support ticket for the customer",
    "inputSchema": {
        "type": "object",
        "properties": {
            "subject": {"type": "string", "description": "Ticket subject line"},
            "description": {"type": "string", "description": "Detailed description of the issue"},
            "priority": {"type": "string", "description": "Ticket priority: low, medium, high, critical"},
            "customer_email": {"type": "string", "description": "Customer email address"},
        },
        "required": ["subject", "description", "priority"],
    },
}

# -- Validate TODO 2 --------------------------------------------------------
total += 1
expected_create = {
    "name": "create_ticket",
    "description": "Create a new support ticket for the customer",
    "inputSchema": {
        "type": "object",
        "properties": {
            "subject": {"type": "string", "description": "Ticket subject line"},
            "description": {"type": "string", "description": "Detailed description of the issue"},
            "priority": {"type": "string", "description": "Ticket priority: low, medium, high, critical"},
            "customer_email": {"type": "string", "description": "Customer email address"},
        },
        "required": ["subject", "description", "priority"],
    },
}
if create_ticket_tool == expected_create:
    score += 1
    print("[PASS] create_ticket tool schema is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_create, indent=2))
    print("       Got:     ", json.dumps(create_ticket_tool, indent=2) if isinstance(create_ticket_tool, dict) else create_ticket_tool)
print()

# ============================================================================
# TODO 3 -- Define get_ticket_status and escalate_ticket Schemas
# ============================================================================

print("=" * 70)
print("TODO 3: Define get_ticket_status and escalate_ticket tool schemas")
print("=" * 70)
print()

get_ticket_status_tool = {
    "name": "get_ticket_status",
    "description": "Retrieve the current status of a support ticket",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ticket_id": {"type": "string", "description": "The unique ticket identifier"},
        },
        "required": ["ticket_id"],
    },
}

escalate_ticket_tool = {
    "name": "escalate_ticket",
    "description": "Escalate a ticket to a human support agent",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ticket_id": {"type": "string", "description": "The unique ticket identifier"},
            "reason": {"type": "string", "description": "Reason for escalation"},
        },
        "required": ["ticket_id", "reason"],
    },
}

# -- Validate TODO 3 --------------------------------------------------------
total += 1
expected_get_status = {
    "name": "get_ticket_status",
    "description": "Retrieve the current status of a support ticket",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ticket_id": {"type": "string", "description": "The unique ticket identifier"},
        },
        "required": ["ticket_id"],
    },
}
expected_escalate = {
    "name": "escalate_ticket",
    "description": "Escalate a ticket to a human support agent",
    "inputSchema": {
        "type": "object",
        "properties": {
            "ticket_id": {"type": "string", "description": "The unique ticket identifier"},
            "reason": {"type": "string", "description": "Reason for escalation"},
        },
        "required": ["ticket_id", "reason"],
    },
}
if get_ticket_status_tool == expected_get_status and escalate_ticket_tool == expected_escalate:
    score += 1
    print("[PASS] get_ticket_status and escalate_ticket schemas are correct")
else:
    if get_ticket_status_tool != expected_get_status:
        print("[FAIL] get_ticket_status mismatch")
        print("       Expected:", json.dumps(expected_get_status, indent=2))
    if escalate_ticket_tool != expected_escalate:
        print("[FAIL] escalate_ticket mismatch")
        print("       Expected:", json.dumps(expected_escalate, indent=2))
print()

# ============================================================================
# TODO 4 -- Define Resource URIs
# ============================================================================

print("=" * 70)
print("TODO 4: Define the MCP resource URIs for the support agent")
print("=" * 70)
print()

resources = [
    {
        "uri": "file://knowledge-base/articles",
        "name": "knowledge_base",
        "description": "Support knowledge base articles",
        "mimeType": "application/json",
    },
    {
        "uri": "db://tickets",
        "name": "ticket_store",
        "description": "Customer support ticket database",
        "mimeType": "application/json",
    },
]

# -- Validate TODO 4 --------------------------------------------------------
total += 1
expected_resources = [
    {
        "uri": "file://knowledge-base/articles",
        "name": "knowledge_base",
        "description": "Support knowledge base articles",
        "mimeType": "application/json",
    },
    {
        "uri": "db://tickets",
        "name": "ticket_store",
        "description": "Customer support ticket database",
        "mimeType": "application/json",
    },
]
if resources == expected_resources:
    score += 1
    print("[PASS] Resource URIs are correct")
    for r in resources:
        print(f"       {r['uri']} -> {r['name']}")
else:
    print("[FAIL] Expected:", json.dumps(expected_resources, indent=2))
    print("       Got:     ", json.dumps(resources, indent=2) if isinstance(resources, list) else resources)
print()

# ============================================================================
# TODO 5 -- Assemble Full Server Specification
# ============================================================================

print("=" * 70)
print("TODO 5: Assemble the complete MCP server specification")
print("=" * 70)
print()

server_spec = {
    "name": "support-agent-mcp",
    "version": "1.0.0",
    "description": "MCP server for AI support agent capstone project",
    "tools": [search_knowledge_tool, create_ticket_tool,
              get_ticket_status_tool, escalate_ticket_tool],
    "resources": resources,
}

# -- Validate TODO 5 --------------------------------------------------------
total += 1
try:
    checks = [
        isinstance(server_spec, dict),
        server_spec.get("name") == "support-agent-mcp",
        server_spec.get("version") == "1.0.0",
        server_spec.get("description") == "MCP server for AI support agent capstone project",
        isinstance(server_spec.get("tools"), list),
        len(server_spec.get("tools", [])) == 4,
        isinstance(server_spec.get("resources"), list),
        len(server_spec.get("resources", [])) == 2,
    ]
    if all(checks):
        score += 1
        out_path = os.path.join(WORKDIR, "mcp_server_spec.json")
        with open(out_path, "w") as f:
            json.dump(server_spec, f, indent=2)
        print(f"[PASS] Server specification saved to {out_path}")
        print(f"       Tools: {[t.get('name', '?') for t in server_spec['tools']]}")
        print(f"       Resources: {[r.get('uri', '?') for r in server_spec['resources']]}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Server spec checks failed at indices: {failed}")
        print(f"       Got: {server_spec}")
except Exception as e:
    print(f"[FAIL] Server spec exception: {e}")
print()

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print(f"Lab 02 Score: {score}/{total}")
print("=" * 70)
