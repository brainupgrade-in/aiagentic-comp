#!/usr/bin/env python3
"""
Lab 01 Solution: Capstone Architecture Design

Design the architecture for a production AI agent system. Identify the
components (FastAPI, LangGraph, ChromaDB, Prometheus, Grafana, LangFuse),
map data flows, and determine monitoring points.

No external packages required -- standard library only.
"""

import os
import json
import shutil
from typing import Dict, List

WORKDIR = "/tmp/capstone-lab-15-01"

# -- Cleanup & Setup ---------------------------------------------------------
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ============================================================================
# STEP 1 -- System Components Overview
# ============================================================================

print("=" * 70)
print("STEP 1: Production AI Agent System -- Components")
print("=" * 70)
print()
print("  A production AI agent system has six core components:")
print()
print("  +--------------------+----------------------------------------------+")
print("  | Component          | Role                                         |")
print("  +--------------------+----------------------------------------------+")
print("  | FastAPI            | HTTP API gateway -- receives requests,       |")
print("  |                    | returns responses, exposes health probes     |")
print("  +--------------------+----------------------------------------------+")
print("  | LangGraph Agent    | Stateful workflow engine -- orchestrates     |")
print("  |                    | reasoning, tool calls, and decision logic    |")
print("  +--------------------+----------------------------------------------+")
print("  | ChromaDB           | Vector store -- stores and retrieves         |")
print("  |                    | document embeddings for RAG                  |")
print("  +--------------------+----------------------------------------------+")
print("  | Prometheus         | Metrics collector -- scrapes /metrics,       |")
print("  |                    | stores time-series data, fires alerts        |")
print("  +--------------------+----------------------------------------------+")
print("  | Grafana            | Dashboard -- visualizes Prometheus metrics,  |")
print("  |                    | shows latency, throughput, error rates       |")
print("  +--------------------+----------------------------------------------+")
print("  | LangFuse           | LLM observability -- traces agent runs,     |")
print("  |                    | tracks token usage, cost, and quality        |")
print("  +--------------------+----------------------------------------------+")
print()

# ============================================================================
# STEP 2 -- Data Flow Architecture
# ============================================================================

print("=" * 70)
print("STEP 2: Data Flow Architecture")
print("=" * 70)
print()
print("  Request flow through the system:")
print()
print("  User Request")
print("       |")
print("       v")
print("  [FastAPI]  --metrics-->  [Prometheus]  --query-->  [Grafana]")
print("       |")
print("       v")
print("  [LangGraph Agent]  --traces-->  [LangFuse]")
print("       |        |")
print("       |        +--retrieve-->  [ChromaDB]")
print("       |")
print("       v")
print("  [LLM API (Groq)]")
print("       |")
print("       v")
print("  Response to User")
print()
print("  Key data flows:")
print("    1. User -> FastAPI -> LangGraph -> LLM -> FastAPI -> User")
print("    2. LangGraph -> ChromaDB (RAG retrieval)")
print("    3. FastAPI -> Prometheus (metrics scrape)")
print("    4. LangGraph -> LangFuse (trace/span/generation)")
print("    5. Prometheus -> Grafana (dashboard visualization)")
print()

# ============================================================================
# STEP 3 -- Component Dependencies
# ============================================================================

print("=" * 70)
print("STEP 3: Component Startup Order (Dependency Graph)")
print("=" * 70)
print()
print("  Components must start in dependency order:")
print()
print("  Level 0 (no deps):   ChromaDB, Prometheus, LangFuse (+ PostgreSQL)")
print("  Level 1 (needs L0):  Grafana (needs Prometheus)")
print("  Level 2 (needs L0):  LangGraph Agent (needs ChromaDB, LangFuse)")
print("  Level 3 (needs L2):  FastAPI (needs LangGraph Agent)")
print()
print("  Startup sequence: ChromaDB -> Prometheus -> LangFuse -> Grafana")
print("                    ChromaDB -> LangGraph -> FastAPI")
print()

# ============================================================================
# TODO 1 -- Map Components to Roles
# ============================================================================

print("=" * 70)
print("TODO 1: Map each component to its primary role")
print("=" * 70)
print()

component_roles = {
    "fastapi":    "api_gateway",
    "langgraph":  "workflow_engine",
    "chromadb":   "vector_store",
    "prometheus": "metrics_collector",
    "grafana":    "dashboard",
    "langfuse":   "llm_observability",
}

# -- Validate TODO 1 --------------------------------------------------------
total += 1
expected_roles = {
    "fastapi":    "api_gateway",
    "langgraph":  "workflow_engine",
    "chromadb":   "vector_store",
    "prometheus": "metrics_collector",
    "grafana":    "dashboard",
    "langfuse":   "llm_observability",
}
if component_roles == expected_roles:
    score += 1
    print("[PASS] Component-to-role mapping is correct")
else:
    print("[FAIL] Expected:", expected_roles)
    print("       Got:     ", component_roles)
print()

# ============================================================================
# TODO 2 -- Define the Startup Order
# ============================================================================

print("=" * 70)
print("TODO 2: Define the correct startup order levels")
print("=" * 70)
print()

startup_order = {
    "level_0": ["chromadb", "prometheus", "langfuse"],
    "level_1": ["grafana"],
    "level_2": ["langgraph"],
    "level_3": ["fastapi"],
}

# -- Validate TODO 2 --------------------------------------------------------
total += 1
expected_order = {
    "level_0": ["chromadb", "prometheus", "langfuse"],
    "level_1": ["grafana"],
    "level_2": ["langgraph"],
    "level_3": ["fastapi"],
}
order_ok = True
for level in expected_order:
    got = startup_order.get(level, [])
    if not isinstance(got, list) or sorted(got) != sorted(expected_order[level]):
        order_ok = False
        break

if order_ok:
    score += 1
    print("[PASS] Startup order is correct")
    for level, components in startup_order.items():
        print(f"       {level}: {components}")
else:
    print("[FAIL] Expected:", expected_order)
    print("       Got:     ", startup_order)
print()

# ============================================================================
# TODO 3 -- Identify Data Flows
# ============================================================================

print("=" * 70)
print("TODO 3: Identify the five primary data flows")
print("=" * 70)
print()

data_flows = {
    "request_path":    ["user", "fastapi"],
    "agent_to_llm":    ["langgraph", "llm_api"],
    "rag_retrieval":   ["langgraph", "chromadb"],
    "metrics_scrape":  ["prometheus", "fastapi"],
    "trace_collection": ["langgraph", "langfuse"],
}

# -- Validate TODO 3 --------------------------------------------------------
total += 1
expected_flows = {
    "request_path":    ["user", "fastapi"],
    "agent_to_llm":    ["langgraph", "llm_api"],
    "rag_retrieval":   ["langgraph", "chromadb"],
    "metrics_scrape":  ["prometheus", "fastapi"],
    "trace_collection": ["langgraph", "langfuse"],
}
if data_flows == expected_flows:
    score += 1
    print("[PASS] Data flows are correct")
    for name, flow in data_flows.items():
        print(f"       {name}: {flow[0]} -> {flow[1]}")
else:
    print("[FAIL] Expected:", expected_flows)
    print("       Got:     ", data_flows)
print()

# ============================================================================
# TODO 4 -- Identify Monitoring Points
# ============================================================================

print("=" * 70)
print("TODO 4: Identify monitoring points for each component")
print("=" * 70)
print()

monitoring_points = {
    "fastapi":    ["request_latency", "error_rate", "request_count"],
    "langgraph":  ["step_duration", "tool_call_count", "agent_errors"],
    "chromadb":   ["query_latency", "collection_size", "retrieval_count"],
    "llm_api":    ["token_usage", "response_time", "cost_per_request"],
}

# -- Validate TODO 4 --------------------------------------------------------
total += 1
expected_monitoring = {
    "fastapi":    ["request_latency", "error_rate", "request_count"],
    "langgraph":  ["step_duration", "tool_call_count", "agent_errors"],
    "chromadb":   ["query_latency", "collection_size", "retrieval_count"],
    "llm_api":    ["token_usage", "response_time", "cost_per_request"],
}
if monitoring_points == expected_monitoring:
    score += 1
    print("[PASS] Monitoring points are correct")
    for comp, points in monitoring_points.items():
        print(f"       {comp}: {points}")
else:
    print("[FAIL] Expected:", expected_monitoring)
    print("       Got:     ", monitoring_points)
print()

# ============================================================================
# TODO 5 -- Build Architecture Document
# ============================================================================

print("=" * 70)
print("TODO 5: Build the complete architecture document")
print("=" * 70)
print()

architecture_doc = {
    "project_name": "ai-support-agent",
    "components": component_roles,
    "startup_order": startup_order,
    "data_flows": data_flows,
    "monitoring_points": monitoring_points,
}

# -- Validate TODO 5 --------------------------------------------------------
total += 1
try:
    checks = [
        isinstance(architecture_doc, dict),
        architecture_doc.get("project_name") == "ai-support-agent",
        architecture_doc.get("components") == expected_roles,
        isinstance(architecture_doc.get("startup_order"), dict),
        isinstance(architecture_doc.get("data_flows"), dict),
        isinstance(architecture_doc.get("monitoring_points"), dict),
    ]
    if all(checks):
        score += 1
        out_path = os.path.join(WORKDIR, "architecture.json")
        with open(out_path, "w") as f:
            json.dump(architecture_doc, f, indent=2)
        print(f"[PASS] Architecture document saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Architecture doc checks failed at indices: {failed}")
        print(f"       Got: {architecture_doc}")
except Exception as e:
    print(f"[FAIL] Architecture doc exception: {e}")
print()

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print(f"Lab 01 Score: {score}/{total}")
print("=" * 70)
