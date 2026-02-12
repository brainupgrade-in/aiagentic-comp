#!/usr/bin/env python3
"""
Lab 01: MCP Architecture — Protocol Fundamentals

Understand the Model Context Protocol architecture: Hosts, Clients, Servers,
Transports, and the three core primitives (Tools, Resources, Prompts).

No external packages required — standard library only.
"""

import os
import json
import shutil
from dataclasses import dataclass, field, asdict
from typing import List

WORKDIR = "/tmp/aidev-lab-13-01"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — MCP Architecture Components                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: MCP Architecture Components")
print("=" * 70)
print()
print("The Model Context Protocol defines four key roles:")
print()
print("  ┌────────────┬──────────────────────────────────────────────────────┐")
print("  │ Component  │ Description                                        │")
print("  ├────────────┼──────────────────────────────────────────────────────┤")
print("  │ Host       │ The application (IDE, chatbot) running the LLM     │")
print("  │ Client     │ Protocol connector inside the host (1:1 w/ server) │")
print("  │ Server     │ Exposes tools/resources/prompts over MCP           │")
print("  │ Transport  │ Communication layer (stdio, HTTP+SSE)              │")
print("  └────────────┴──────────────────────────────────────────────────────┘")
print()
print("  Host (e.g. Claude Desktop)")
print("    └── MCP Client  ──transport──▶  MCP Server  ──▶  Data/APIs")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — The Three Primitives                                              ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: The Three MCP Primitives")
print("=" * 70)
print()
print("  ┌───────────┬─────────────┬──────────────────────────┬──────────────┐")
print("  │ Primitive │ Controlled  │ Purpose                  │ Analogy      │")
print("  │           │ By          │                          │              │")
print("  ├───────────┼─────────────┼──────────────────────────┼──────────────┤")
print("  │ Tools     │ Model (LLM) │ Actions the model can    │ POST endpoint│")
print("  │           │             │ invoke (search, compute) │              │")
print("  ├───────────┼─────────────┼──────────────────────────┼──────────────┤")
print("  │ Resources │ Application │ Data the app can read    │ GET endpoint │")
print("  │           │             │ (files, DB rows, configs)│              │")
print("  ├───────────┼─────────────┼──────────────────────────┼──────────────┤")
print("  │ Prompts   │ User        │ Templates the user       │ Slash command│")
print("  │           │             │ selects (/review, /fix)  │              │")
print("  └───────────┴─────────────┴──────────────────────────┴──────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 3 — MCP vs Direct Integration                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 3: MCP vs Direct Integration (N*M vs N+M)")
print("=" * 70)
print()
print("  Without MCP:  Each agent needs a custom integration per tool")
print("    Integrations = N agents  x  M tools  =  N * M")
print()
print("  With MCP:  Each agent connects via MCP; each tool exposes MCP")
print("    Integrations = N agents  +  M tools  =  N + M")
print()
print("  Example:  3 agents, 4 tools")
print("    Without MCP:  3 * 4 = 12 integrations")
print("    With MCP:     3 + 4 =  7 integrations")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Map Primitives to Controllers                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Map each MCP primitive to who controls it")
print("=" * 70)
print()

# TODO: Replace each "___" with the correct controller.
#   "tools"     → controlled by the model (LLM decides when to call)
#   "resources" → controlled by the application (app decides what to expose)
#   "prompts"   → controlled by the user (user selects the template)

primitive_controllers = {
    "tools":     "___",
    "resources": "___",
    "prompts":   "___",
}

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
expected_controllers = {"tools": "model", "resources": "application", "prompts": "user"}
if primitive_controllers == expected_controllers:
    score += 1
    print("[PASS] Primitive-to-controller mapping is correct")
else:
    print("[FAIL] Expected:", expected_controllers)
    print("       Got:     ", primitive_controllers)
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Calculate Integration Counts                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Calculate N*M vs N+M integration counts")
print("=" * 70)
print()

N = 5   # number of agents
M = 10  # number of tools

# TODO: Calculate the number of integrations with and without MCP.
without_mcp = "___"  # Replace with N * M
with_mcp    = "___"  # Replace with N + M

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
if without_mcp == 50 and with_mcp == 15:
    score += 1
    print(f"[PASS] Without MCP = {without_mcp}, With MCP = {with_mcp}")
else:
    print(f"[FAIL] Expected without_mcp=50, with_mcp=15")
    print(f"       Got without_mcp={without_mcp}, with_mcp={with_mcp}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Build an MCPServerInfo Data Structure                            ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Build an MCPServerInfo dataclass instance")
print("=" * 70)
print()

@dataclass
class MCPServerInfo:
    """Describes an MCP server's capabilities."""
    name: str = ""
    version: str = ""
    tools: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    prompts: List[str] = field(default_factory=list)

# TODO: Create an instance of MCPServerInfo with:
#   name      = "code-assistant"
#   version   = "1.0.0"
#   tools     = ["search_code", "run_linter", "analyze_deps"]
#   resources = ["file://project", "config://settings"]
#   prompts   = ["code_review", "explain_function"]

server_info = MCPServerInfo(
    name="___",
    version="___",
    tools=["___"],
    resources=["___"],
    prompts=["___"],
)

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
info_dict = asdict(server_info)
checks = [
    info_dict["name"] == "code-assistant",
    info_dict["version"] == "1.0.0",
    info_dict["tools"] == ["search_code", "run_linter", "analyze_deps"],
    info_dict["resources"] == ["file://project", "config://settings"],
    info_dict["prompts"] == ["code_review", "explain_function"],
]
if all(checks):
    score += 1
    print("[PASS] MCPServerInfo is correct")
    out_path = os.path.join(WORKDIR, "server_info.json")
    with open(out_path, "w") as f:
        json.dump(info_dict, f, indent=2)
    print(f"       Saved to {out_path}")
else:
    print("[FAIL] MCPServerInfo does not match expected values")
    print("       Got:", json.dumps(info_dict, indent=2))
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 4 — Classify JSON-RPC Methods by Primitive                           ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 4: Classify JSON-RPC methods by MCP primitive type")
print("=" * 70)
print()
print("  MCP uses these JSON-RPC methods:")
print()
print("  ┌─────────────────┬────────────────────────────────────────────┐")
print("  │ Method           │ Description                              │")
print("  ├─────────────────┼────────────────────────────────────────────┤")
print("  │ tools/list       │ List available tools                     │")
print("  │ tools/call       │ Execute a tool                           │")
print("  │ resources/list   │ List available resources                 │")
print("  │ resources/read   │ Read a resource's content                │")
print("  │ prompts/list     │ List available prompt templates          │")
print("  │ prompts/get      │ Retrieve a prompt template               │")
print("  │ initialize       │ Handshake with capabilities exchange     │")
print("  └─────────────────┴────────────────────────────────────────────┘")
print()

# TODO: Classify each method into the correct category.
#   "tool"      → methods that operate on tools
#   "resource"  → methods that operate on resources
#   "prompt"    → methods that operate on prompts
#   "lifecycle" → connection management methods

method_classification = {
    "tools/list":     "___",
    "tools/call":     "___",
    "resources/list": "___",
    "resources/read": "___",
    "prompts/list":   "___",
    "prompts/get":    "___",
    "initialize":     "___",
}

# ── Validate TODO 4 ─────────────────────────────────────────────────────────
total += 1
expected_classification = {
    "tools/list":     "tool",
    "tools/call":     "tool",
    "resources/list": "resource",
    "resources/read": "resource",
    "prompts/list":   "prompt",
    "prompts/get":    "prompt",
    "initialize":     "lifecycle",
}
if method_classification == expected_classification:
    score += 1
    print("[PASS] Method classification is correct")
    out_path = os.path.join(WORKDIR, "method_classification.json")
    with open(out_path, "w") as f:
        json.dump(method_classification, f, indent=2)
    print(f"       Saved to {out_path}")
else:
    print("[FAIL] Expected:", json.dumps(expected_classification, indent=2))
    print("       Got:     ", json.dumps(method_classification, indent=2))
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 01 Score: {score}/{total}")
print("=" * 70)
