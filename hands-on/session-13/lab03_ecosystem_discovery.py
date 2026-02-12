#!/usr/bin/env python3
"""
Lab 03: MCP Ecosystem Discovery

Catalog MCP servers from the ecosystem, match them to enterprise needs,
and evaluate organizational readiness for MCP adoption.

No external packages required — standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any

WORKDIR = "/tmp/aidev-lab-13-03"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — MCP Server Ecosystem Overview                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: MCP Server Ecosystem Overview")
print("=" * 70)
print()
print("  The MCP ecosystem has grown to 1,000+ servers across categories:")
print()
print("  ┌─────────────────┬──────────────────────────────────────────────────┐")
print("  │ Category        │ Examples                                         │")
print("  ├─────────────────┼──────────────────────────────────────────────────┤")
print("  │ Databases       │ Postgres, SQLite, MySQL, MongoDB, Redis         │")
print("  │ Developer Tools │ GitHub, GitLab, Linear, Sentry, Docker          │")
print("  │ Cloud & Infra   │ AWS, Kubernetes, Terraform, Cloudflare          │")
print("  │ Knowledge       │ Confluence, Notion, Google Drive, Obsidian      │")
print("  │ Communication   │ Slack, Gmail, Discord, Microsoft Teams          │")
print("  │ Web & Data      │ Puppeteer, Brave Search, Fetch                  │")
print("  │ Productivity    │ Google Calendar, Todoist, Linear                │")
print("  └─────────────────┴──────────────────────────────────────────────────┘")
print()
print("  Registry: github.com/modelcontextprotocol/servers  |  mcp.so")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Build an MCP Server Catalog                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Build an MCP server catalog")
print("=" * 70)
print()

# TODO: Create a catalog of 6 MCP servers. Each entry should be a dict with:
#   - name: server name (str)
#   - category: one of "database", "developer", "cloud", "knowledge", "communication", "web"
#   - transport: "stdio" or "sse"
#   - tools: list of tool names (str)
#   - resources: list of resource URIs (str)
#   - maturity: "stable", "beta", or "experimental"
#
# Build the following catalog:
#
#   1. name="postgres", category="database", transport="stdio",
#      tools=["query", "list_tables"], resources=["db://schema"],
#      maturity="stable"
#
#   2. name="github", category="developer", transport="stdio",
#      tools=["create_issue", "search_code", "create_pr"],
#      resources=["repo://files"], maturity="stable"
#
#   3. name="slack", category="communication", transport="stdio",
#      tools=["send_message", "search_messages"],
#      resources=[], maturity="stable"
#
#   4. name="confluence", category="knowledge", transport="sse",
#      tools=["search_pages"], resources=["wiki://pages", "wiki://spaces"],
#      maturity="beta"
#
#   5. name="kubernetes", category="cloud", transport="stdio",
#      tools=["get_pods", "get_logs", "describe_resource"],
#      resources=["k8s://namespaces"], maturity="beta"
#
#   6. name="puppeteer", category="web", transport="stdio",
#      tools=["navigate", "screenshot", "click"],
#      resources=[], maturity="experimental"

catalog = "___"  # Replace with a list of 6 dicts

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    checks = [
        isinstance(catalog, list),
        len(catalog) == 6,
        catalog[0]["name"] == "postgres",
        catalog[0]["category"] == "database",
        catalog[0]["maturity"] == "stable",
        len(catalog[0]["tools"]) == 2,
        catalog[1]["name"] == "github",
        len(catalog[1]["tools"]) == 3,
        catalog[3]["name"] == "confluence",
        catalog[3]["transport"] == "sse",
        catalog[4]["name"] == "kubernetes",
        catalog[4]["category"] == "cloud",
        catalog[5]["name"] == "puppeteer",
        catalog[5]["maturity"] == "experimental",
    ]
    if all(checks):
        score += 1
        print("[PASS] MCP server catalog built correctly:")
        for s in catalog:
            print(f"       {s['name']:12s} [{s['category']:13s}] "
                  f"{s['maturity']:12s} {len(s['tools'])} tools, "
                  f"{len(s['resources'])} resources")
        out_path = os.path.join(WORKDIR, "mcp_catalog.json")
        with open(out_path, "w") as f:
            json.dump(catalog, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Catalog checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Catalog error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Match MCP Servers to Enterprise Needs                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Match MCP servers to enterprise team needs")
print("=" * 70)
print()

# An enterprise has these teams with specific needs:
teams = {
    "data_engineering": {
        "needs": ["query databases", "inspect schemas"],
        "priority": "high",
    },
    "platform_engineering": {
        "needs": ["manage kubernetes", "monitor infrastructure"],
        "priority": "high",
    },
    "product_development": {
        "needs": ["manage code", "track issues", "communicate"],
        "priority": "medium",
    },
}

# TODO: For each team, return a list of recommended MCP server names
#       from the catalog that match their needs.
#
#   "data_engineering"      → ["postgres"]
#   "platform_engineering"  → ["kubernetes"]
#   "product_development"   → ["github", "slack"]

team_recommendations = {
    "data_engineering":      "___",
    "platform_engineering":  "___",
    "product_development":   "___",
}

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
expected_recs = {
    "data_engineering":      ["postgres"],
    "platform_engineering":  ["kubernetes"],
    "product_development":   ["github", "slack"],
}
if team_recommendations == expected_recs:
    score += 1
    print("[PASS] Team recommendations correct:")
    for team, servers in team_recommendations.items():
        print(f"       {team:25s} → {servers}")
else:
    print(f"[FAIL] Expected: {json.dumps(expected_recs)}")
    print(f"       Got:      {json.dumps(team_recommendations) if isinstance(team_recommendations, dict) else team_recommendations}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Evaluate Ecosystem Readiness Score                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Evaluate ecosystem readiness for an enterprise")
print("=" * 70)
print()

# Given an enterprise's required capabilities and the catalog,
# calculate a readiness score.

required_capabilities = [
    "query databases",           # → postgres (stable)
    "manage source code",        # → github (stable)
    "search knowledge base",     # → confluence (beta)
    "send team messages",        # → slack (stable)
    "manage cloud resources",    # → kubernetes (beta)
    "automate browser testing",  # → puppeteer (experimental)
]

# Scoring: stable = 1.0, beta = 0.7, experimental = 0.3, missing = 0.0
# The mapping from capabilities to servers/maturity:
#   "query databases"           → postgres    → stable        → 1.0
#   "manage source code"        → github      → stable        → 1.0
#   "search knowledge base"     → confluence  → beta          → 0.7
#   "send team messages"        → slack       → stable        → 1.0
#   "manage cloud resources"    → kubernetes  → beta          → 0.7
#   "automate browser testing"  → puppeteer   → experimental  → 0.3

# TODO: Calculate the readiness_score as the average of the individual
#       scores, rounded to 2 decimal places.
#       Individual scores: [1.0, 1.0, 0.7, 1.0, 0.7, 0.3]
#       Average = sum / len = 4.7 / 6 = 0.78

readiness_score = "___"  # Replace with the calculated score (float)

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
if readiness_score == 0.78:
    score += 1
    print(f"[PASS] Readiness score: {readiness_score}")
    print(f"       Breakdown: stable×3 (3.0) + beta×2 (1.4) + experimental×1 (0.3) = 4.7/6")
    report = {
        "required_capabilities": len(required_capabilities),
        "readiness_score": readiness_score,
        "coverage": {
            "stable": 3,
            "beta": 2,
            "experimental": 1,
            "missing": 0,
        },
    }
    out_path = os.path.join(WORKDIR, "readiness_report.json")
    with open(out_path, "w") as f:
        json.dump(report, f, indent=2)
    print(f"       Saved to {out_path}")
else:
    print(f"[FAIL] Expected readiness_score=0.78, got {readiness_score}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 03 Score: {score}/{total}")
print("=" * 70)
