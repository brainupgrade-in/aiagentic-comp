#!/usr/bin/env python3
"""
Lab 02: Enterprise MCP Use Cases

Map business functions to MCP servers, calculate ROI for MCP adoption,
prioritize implementation, and design multi-tool agent configurations.

No external packages required — standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any

WORKDIR = "/tmp/aidev-lab-13-02"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Enterprise MCP Use Case Categories                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: Enterprise MCP Use Case Categories")
print("=" * 70)
print()
print("  Fortune 500 companies adopt MCP in three main areas:")
print()
print("  ┌───────────────────────┬────────────────────────────────────────────┐")
print("  │ Category              │ Example MCP Servers                        │")
print("  ├───────────────────────┼────────────────────────────────────────────┤")
print("  │ Enterprise Data       │ Postgres, Snowflake, BigQuery, MongoDB    │")
print("  │ Developer Productivity│ GitHub, Jira, CI/CD, Sentry               │")
print("  │ Knowledge & Customer  │ Confluence, Salesforce, Zendesk, Slack    │")
print("  └───────────────────────┴────────────────────────────────────────────┘")
print()
print("  Each server exposes domain-specific Tools, Resources, and Prompts")
print("  that any MCP-compatible AI agent can discover and use.")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — ROI Framework                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: ROI Framework for MCP Adoption")
print("=" * 70)
print()
print("  Cost-Benefit Analysis:")
print()
print("  ┌──────────────────────┬───────────────────────────────────────────┐")
print("  │ Factor               │ Measurement                               │")
print("  ├──────────────────────┼───────────────────────────────────────────┤")
print("  │ Integration Cost     │ Hours saved: (old_weeks × 40) - new_hours│")
print("  │ Productivity Gain    │ Context switches reduced per hour         │")
print("  │ Data Access          │ Time-to-answer: days → minutes           │")
print("  │ Vendor Lock-in       │ Switching cost: high → low               │")
print("  │ Security Posture     │ Audit points: N×M → centralized          │")
print("  └──────────────────────┴───────────────────────────────────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 3 — Tools vs Resources: Who Controls What?                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 3: Tools vs Resources — The Key Distinction")
print("=" * 70)
print()
print("  The difference is WHO INITIATES the interaction:")
print()
print("  ┌────────────┬───────────────────┬──────────────────────────────────┐")
print("  │ Primitive  │ Controlled By     │ Description                      │")
print("  ├────────────┼───────────────────┼──────────────────────────────────┤")
print("  │ Tool       │ The MODEL decides │ Actions: query, create, send,    │")
print("  │            │ when to call it   │ update. May have side effects.   │")
print("  ├────────────┼───────────────────┼──────────────────────────────────┤")
print("  │ Resource   │ The APP decides   │ Context: schema, pages, config.  │")
print("  │            │ when to load it   │ Read-only, no side effects.      │")
print("  └────────────┴───────────────────┴──────────────────────────────────┘")
print()
print("  Example — Postgres MCP server:")
print("    Tool:     query_db(sql)   → model decides to run a query")
print("    Resource: db://schema     → app pre-loads table structure as context")
print()
print("  Example — Jira MCP server:")
print("    Tool:     create_issue()  → model decides to create a ticket")
print("    Resource: jira://board    → app pre-loads sprint board as context")
print()
print("  The same data CAN be exposed as either — it depends on whether")
print("  the model or the application should control when it's accessed.")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Map Business Functions to MCP Servers                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Map business functions to MCP server configurations")
print("=" * 70)
print()

# TODO: For each business function, specify the MCP server name and
#       which primitives it uses: "tool", "resource", or "both".
#
#       Ask: does the model need to PERFORM ACTIONS? → tool
#            does the app need to PROVIDE CONTEXT?   → resource
#            both?                                   → both
#
#   "database_analytics"    → server: "postgres",    primitives: "both"
#       Tools: query_db (model runs SQL)  |  Resources: db://schema (app loads schema)
#   "code_management"       → server: "github",      primitives: "both"
#       Tools: create_pr, search_code     |  Resources: repo://structure (app loads repo info)
#   "ticket_tracking"       → server: "jira",        primitives: "both"
#       Tools: create_issue, update       |  Resources: jira://board (app loads sprint data)
#   "knowledge_base"        → server: "confluence",  primitives: "resource"
#       Resources only: wiki://pages, wiki://spaces (app loads docs as context)
#   "team_communication"    → server: "slack",        primitives: "tool"
#       Tools only: send_message, search (model performs actions, no pre-loaded context)

business_to_mcp = {
    "database_analytics": {"server": "___", "primitives": "___"},
    "code_management":    {"server": "___", "primitives": "___"},
    "ticket_tracking":    {"server": "___", "primitives": "___"},
    "knowledge_base":     {"server": "___", "primitives": "___"},
    "team_communication": {"server": "___", "primitives": "___"},
}

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
expected_mapping = {
    "database_analytics": {"server": "postgres",   "primitives": "both"},
    "code_management":    {"server": "github",     "primitives": "both"},
    "ticket_tracking":    {"server": "jira",       "primitives": "both"},
    "knowledge_base":     {"server": "confluence", "primitives": "resource"},
    "team_communication": {"server": "slack",      "primitives": "tool"},
}
if business_to_mcp == expected_mapping:
    score += 1
    print("[PASS] Business-to-MCP mapping is correct")
    for func, cfg in business_to_mcp.items():
        print(f"       {func:25s} → {cfg['server']:12s} (primitives: {cfg['primitives']})")
else:
    print("[FAIL] Expected:", json.dumps(expected_mapping, indent=2))
    print("       Got:     ", json.dumps(business_to_mcp, indent=2))
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Calculate ROI for MCP Adoption                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Calculate ROI for MCP adoption")
print("=" * 70)
print()

# Scenario: A company has 4 AI agents and 6 enterprise tools.
# Old approach: custom integration takes 3 weeks (120 hours) per pair.
# New approach: MCP server setup takes 16 hours per tool, MCP client takes 8 hours per agent.

agents = 4
tools = 6
old_hours_per_integration = 120  # 3 weeks × 40 hours/week

# TODO: Calculate the following:
#   old_total = agents * tools * old_hours_per_integration
#   new_total = (tools * 16) + (agents * 8)  # 16h per server + 8h per client
#   hours_saved = old_total - new_total
#   roi_percentage = round((hours_saved / old_total) * 100, 1)

old_total       = "___"
new_total       = "___"
hours_saved     = "___"
roi_percentage  = "___"

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
checks = [
    old_total == 2880,       # 4 * 6 * 120
    new_total == 128,        # (6 * 16) + (4 * 8) = 96 + 32
    hours_saved == 2752,     # 2880 - 128
    roi_percentage == 95.6,  # round((2752 / 2880) * 100, 1)
]
if all(checks):
    score += 1
    print(f"[PASS] ROI calculation correct:")
    print(f"       Old total: {old_total} hours")
    print(f"       New total: {new_total} hours")
    print(f"       Saved:     {hours_saved} hours ({roi_percentage}% reduction)")
else:
    print(f"[FAIL] Expected: old=2880, new=128, saved=2752, roi=95.6")
    print(f"       Got: old={old_total}, new={new_total}, saved={hours_saved}, roi={roi_percentage}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Prioritize MCP Server Implementation                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Prioritize MCP server implementations")
print("=" * 70)
print()

# Given the following servers with their impact and effort scores:
servers = [
    {"name": "postgres",   "impact": 9, "effort": 3, "category": "data"},
    {"name": "github",     "impact": 8, "effort": 4, "category": "developer"},
    {"name": "slack",      "impact": 6, "effort": 2, "category": "communication"},
    {"name": "confluence", "impact": 7, "effort": 5, "category": "knowledge"},
    {"name": "jira",       "impact": 7, "effort": 3, "category": "developer"},
    {"name": "salesforce", "impact": 8, "effort": 7, "category": "customer"},
]

# TODO: Calculate priority_score = impact / effort for each server,
#       round to 2 decimal places, then return the list sorted by
#       priority_score descending (highest priority first).
#       Add a "priority_score" key to each dict.
#
# Hint:
#   for s in servers:
#       s["priority_score"] = round(s["impact"] / s["effort"], 2)
#   prioritized = sorted(servers, key=lambda x: x["priority_score"], reverse=True)

prioritized = "___"  # Replace with your implementation

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    checks = [
        isinstance(prioritized, list),
        len(prioritized) == 6,
        prioritized[0]["name"] == "postgres",   # 9/3 = 3.0
        prioritized[1]["name"] == "slack",       # 6/2 = 3.0 (but slack has lower impact, check order)
    ]
    # Actually: postgres=3.0, slack=3.0, jira=2.33, github=2.0, confluence=1.4, salesforce=1.14
    # When scores are equal, original order is preserved by stable sort
    expected_order = ["postgres", "slack", "jira", "github", "confluence", "salesforce"]
    actual_order = [s["name"] for s in prioritized] if isinstance(prioritized, list) else []
    if actual_order == expected_order:
        score += 1
        print("[PASS] Prioritization order correct:")
        for s in prioritized:
            print(f"       {s['name']:12s} score={s['priority_score']:.2f} "
                  f"(impact={s['impact']}, effort={s['effort']})")
    else:
        print(f"[FAIL] Expected order: {expected_order}")
        print(f"       Got order:     {actual_order}")
except Exception as e:
    print(f"[FAIL] Prioritization error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 4 — Design Multi-Tool Agent Configuration                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 4: Design a multi-tool agent configuration")
print("=" * 70)
print()

# TODO: Build a configuration dict that represents an enterprise AI agent
#       connected to multiple MCP servers. The config should have:
#
#   {
#       "agent_name": "enterprise-assistant",
#       "mcp_servers": {
#           "postgres":   {"transport": "stdio",  "tools": ["query_db"],           "resources": ["db://schema"]},
#           "github":     {"transport": "stdio",  "tools": ["search_code", "create_pr"], "resources": ["repo://structure"]},
#           "slack":      {"transport": "stdio",  "tools": ["send_message", "search_messages"], "resources": []},
#           "confluence": {"transport": "sse",    "tools": [],                      "resources": ["wiki://pages", "wiki://spaces"]},
#       },
#       "total_tools": 5,
#       "total_resources": 4,
#   }

agent_config = "___"  # Replace with the config dict above

# ── Validate TODO 4 ─────────────────────────────────────────────────────────
total += 1
try:
    checks = [
        isinstance(agent_config, dict),
        agent_config.get("agent_name") == "enterprise-assistant",
        len(agent_config.get("mcp_servers", {})) == 4,
        agent_config.get("total_tools") == 5,
        agent_config.get("total_resources") == 4,
        "postgres" in agent_config.get("mcp_servers", {}),
        "github" in agent_config.get("mcp_servers", {}),
        "slack" in agent_config.get("mcp_servers", {}),
        "confluence" in agent_config.get("mcp_servers", {}),
        agent_config.get("mcp_servers", {}).get("confluence", {}).get("transport") == "sse",
    ]
    if all(checks):
        score += 1
        print("[PASS] Multi-tool agent configuration correct:")
        print(f"       Agent: {agent_config['agent_name']}")
        print(f"       Servers: {list(agent_config['mcp_servers'].keys())}")
        print(f"       Total tools: {agent_config['total_tools']}")
        print(f"       Total resources: {agent_config['total_resources']}")
        out_path = os.path.join(WORKDIR, "agent_config.json")
        with open(out_path, "w") as f:
            json.dump(agent_config, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Config checks failed at indices: {failed}")
        print(f"       Got: {json.dumps(agent_config, indent=2) if isinstance(agent_config, dict) else agent_config}")
except Exception as e:
    print(f"[FAIL] Config error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 02 Score: {score}/{total}")
print("=" * 70)
