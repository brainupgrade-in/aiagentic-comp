#!/usr/bin/env python3
"""
Lab 02 Solution: Enterprise MCP Use Cases

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
# ║  TODO 1 — Map Business Functions to MCP Servers                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Map business functions to MCP server configurations")
print("=" * 70)
print()

business_to_mcp = {
    "database_analytics": {"server": "postgres",   "type": "both"},
    "code_management":    {"server": "github",     "type": "both"},
    "ticket_tracking":    {"server": "jira",       "type": "tool"},
    "knowledge_base":     {"server": "confluence", "type": "resource"},
    "team_communication": {"server": "slack",      "type": "tool"},
}

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
expected_mapping = {
    "database_analytics": {"server": "postgres",   "type": "both"},
    "code_management":    {"server": "github",     "type": "both"},
    "ticket_tracking":    {"server": "jira",       "type": "tool"},
    "knowledge_base":     {"server": "confluence", "type": "resource"},
    "team_communication": {"server": "slack",      "type": "tool"},
}
if business_to_mcp == expected_mapping:
    score += 1
    print("[PASS] Business-to-MCP mapping is correct")
    for func, cfg in business_to_mcp.items():
        print(f"       {func:25s} → {cfg['server']:12s} ({cfg['type']})")
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

agents = 4
tools = 6
old_hours_per_integration = 120

old_total       = agents * tools * old_hours_per_integration  # 2880
new_total       = (tools * 16) + (agents * 8)                 # 128
hours_saved     = old_total - new_total                        # 2752
roi_percentage  = round((hours_saved / old_total) * 100, 1)   # 95.6

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
checks = [
    old_total == 2880,
    new_total == 128,
    hours_saved == 2752,
    roi_percentage == 95.6,
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

servers = [
    {"name": "postgres",   "impact": 9, "effort": 3, "category": "data"},
    {"name": "github",     "impact": 8, "effort": 4, "category": "developer"},
    {"name": "slack",      "impact": 6, "effort": 2, "category": "communication"},
    {"name": "confluence", "impact": 7, "effort": 5, "category": "knowledge"},
    {"name": "jira",       "impact": 7, "effort": 3, "category": "developer"},
    {"name": "salesforce", "impact": 8, "effort": 7, "category": "customer"},
]

for s in servers:
    s["priority_score"] = round(s["impact"] / s["effort"], 2)
prioritized = sorted(servers, key=lambda x: x["priority_score"], reverse=True)

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    checks = [
        isinstance(prioritized, list),
        len(prioritized) == 6,
        prioritized[0]["name"] == "postgres",
        prioritized[1]["name"] == "slack",
    ]
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

agent_config = {
    "agent_name": "enterprise-assistant",
    "mcp_servers": {
        "postgres":   {"transport": "stdio",  "tools": ["query_db"],           "resources": ["db://schema"]},
        "github":     {"transport": "stdio",  "tools": ["search_code", "create_pr"], "resources": ["repo://structure"]},
        "slack":      {"transport": "stdio",  "tools": ["send_message", "search_messages"], "resources": []},
        "confluence": {"transport": "sse",    "tools": [],                      "resources": ["wiki://pages", "wiki://spaces"]},
    },
    "total_tools": 5,
    "total_resources": 4,
}

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
