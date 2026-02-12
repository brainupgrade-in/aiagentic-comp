#!/usr/bin/env python3
"""
Lab 07 Solution: Testing & Validation

Write a test plan as structured data: unit test list, integration test
scenarios, and load test thresholds. Match test types to components,
fill in expected behaviors, and define SLA values.

No external packages required -- standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any

WORKDIR = "/tmp/capstone-lab-15-07"

# -- Cleanup & Setup ---------------------------------------------------------
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ============================================================================
# STEP 1 -- Testing Pyramid for AI Agents
# ============================================================================

print("=" * 70)
print("STEP 1: Testing Pyramid for AI Agent Applications")
print("=" * 70)
print()
print("  Testing pyramid (bottom = most tests, top = fewest):")
print()
print("         /\\")
print("        /  \\       E2E Tests (smoke tests, user flows)")
print("       /----\\")
print("      /      \\     Integration Tests (API + agent + DB)")
print("     /--------\\")
print("    /          \\   Unit Tests (functions, models, tools)")
print("   /____________\\")
print()
print("  +------------------+------+-------------------------------------+")
print("  | Test Type        | Count| What It Tests                       |")
print("  +------------------+------+-------------------------------------+")
print("  | Unit             | Many | Individual functions, pure logic    |")
print("  | Integration      | Some | Component interactions, API calls   |")
print("  | E2E / Smoke      | Few  | Full user flow, critical paths     |")
print("  | Load / Perf      | Few  | Throughput, latency under stress   |")
print("  +------------------+------+-------------------------------------+")
print()

# ============================================================================
# STEP 2 -- SLA Definitions
# ============================================================================

print("=" * 70)
print("STEP 2: Service Level Agreements (SLAs)")
print("=" * 70)
print()
print("  Production AI agents need clear SLAs:")
print()
print("  +---------------------------+----------+-------------------------+")
print("  | Metric                    | Target   | Measurement             |")
print("  +---------------------------+----------+-------------------------+")
print("  | Availability              | 99.9%    | Uptime over 30 days     |")
print("  | Response time (p50)       | < 2s     | 50th percentile         |")
print("  | Response time (p99)       | < 10s    | 99th percentile         |")
print("  | Error rate                | < 1%     | 5xx responses / total   |")
print("  | Throughput                | 100 rps  | Sustained requests/sec  |")
print("  +---------------------------+----------+-------------------------+")
print()

# ============================================================================
# TODO 1 -- Define Unit Test Plan
# ============================================================================

print("=" * 70)
print("TODO 1: Define the unit test plan")
print("=" * 70)
print()

unit_tests = [
    {"name": "test_support_request_validation", "component": "api",
     "description": "Validate SupportRequest model accepts valid input",
     "expected_result": "pass"},
    {"name": "test_support_request_missing_question", "component": "api",
     "description": "Validate SupportRequest rejects missing question field",
     "expected_result": "validation_error"},
    {"name": "test_search_knowledge_tool_schema", "component": "mcp",
     "description": "Validate search_knowledge tool schema structure",
     "expected_result": "pass"},
    {"name": "test_ticket_creation", "component": "agent",
     "description": "Validate agent creates ticket with required fields",
     "expected_result": "pass"},
    {"name": "test_cost_calculation", "component": "observability",
     "description": "Validate LLM cost calculation formula",
     "expected_result": "pass"},
]

# -- Validate TODO 1 --------------------------------------------------------
total += 1
expected_unit_tests = [
    {"name": "test_support_request_validation", "component": "api",
     "description": "Validate SupportRequest model accepts valid input",
     "expected_result": "pass"},
    {"name": "test_support_request_missing_question", "component": "api",
     "description": "Validate SupportRequest rejects missing question field",
     "expected_result": "validation_error"},
    {"name": "test_search_knowledge_tool_schema", "component": "mcp",
     "description": "Validate search_knowledge tool schema structure",
     "expected_result": "pass"},
    {"name": "test_ticket_creation", "component": "agent",
     "description": "Validate agent creates ticket with required fields",
     "expected_result": "pass"},
    {"name": "test_cost_calculation", "component": "observability",
     "description": "Validate LLM cost calculation formula",
     "expected_result": "pass"},
]
if unit_tests == expected_unit_tests:
    score += 1
    print(f"[PASS] Unit test plan has {len(unit_tests)} tests")
    for t in unit_tests:
        print(f"       {t['name']} ({t['component']})")
else:
    print("[FAIL] Expected:", json.dumps(expected_unit_tests, indent=2))
    print("       Got:     ", json.dumps(unit_tests, indent=2) if isinstance(unit_tests, list) else unit_tests)
print()

# ============================================================================
# TODO 2 -- Define Integration Test Scenarios
# ============================================================================

print("=" * 70)
print("TODO 2: Define integration test scenarios")
print("=" * 70)
print()

integration_tests = [
    {"name": "test_api_to_agent_flow",
     "components": ["fastapi", "langgraph"],
     "description": "POST /api/support triggers agent and returns response",
     "steps": ["Send POST request", "Agent processes query", "Return response"],
     "expected_result": "200 OK with SupportResponse body"},
    {"name": "test_agent_rag_retrieval",
     "components": ["langgraph", "chromadb"],
     "description": "Agent retrieves context from ChromaDB before answering",
     "steps": ["Agent receives query", "Query ChromaDB", "Use context in prompt"],
     "expected_result": "Response includes relevant source documents"},
    {"name": "test_observability_pipeline",
     "components": ["fastapi", "langfuse", "prometheus"],
     "description": "Request generates traces in LangFuse and metrics in Prometheus",
     "steps": ["Send request", "Check LangFuse trace", "Check Prometheus metric"],
     "expected_result": "Trace and metric both recorded"},
]

# -- Validate TODO 2 --------------------------------------------------------
total += 1
expected_integration = [
    {"name": "test_api_to_agent_flow",
     "components": ["fastapi", "langgraph"],
     "description": "POST /api/support triggers agent and returns response",
     "steps": ["Send POST request", "Agent processes query", "Return response"],
     "expected_result": "200 OK with SupportResponse body"},
    {"name": "test_agent_rag_retrieval",
     "components": ["langgraph", "chromadb"],
     "description": "Agent retrieves context from ChromaDB before answering",
     "steps": ["Agent receives query", "Query ChromaDB", "Use context in prompt"],
     "expected_result": "Response includes relevant source documents"},
    {"name": "test_observability_pipeline",
     "components": ["fastapi", "langfuse", "prometheus"],
     "description": "Request generates traces in LangFuse and metrics in Prometheus",
     "steps": ["Send request", "Check LangFuse trace", "Check Prometheus metric"],
     "expected_result": "Trace and metric both recorded"},
]
if integration_tests == expected_integration:
    score += 1
    print(f"[PASS] Integration test plan has {len(integration_tests)} scenarios")
    for t in integration_tests:
        print(f"       {t['name']}: {t['components']}")
else:
    print("[FAIL] Expected:", json.dumps(expected_integration, indent=2))
    print("       Got:     ", json.dumps(integration_tests, indent=2) if isinstance(integration_tests, list) else integration_tests)
print()

# ============================================================================
# TODO 3 -- Define Load Test Thresholds
# ============================================================================

print("=" * 70)
print("TODO 3: Define load test thresholds")
print("=" * 70)
print()

load_test_config = {
    "tool": "locust",
    "target_url": "http://localhost:8000",
    "scenarios": [
        {"name": "steady_state", "users": 50, "spawn_rate": 5, "duration_seconds": 300},
        {"name": "peak_load", "users": 200, "spawn_rate": 20, "duration_seconds": 120},
    ],
    "thresholds": {
        "p50_response_ms": 2000,
        "p99_response_ms": 10000,
        "error_rate_percent": 1.0,
        "min_throughput_rps": 100,
    },
}

# -- Validate TODO 3 --------------------------------------------------------
total += 1
expected_load = {
    "tool": "locust",
    "target_url": "http://localhost:8000",
    "scenarios": [
        {"name": "steady_state", "users": 50, "spawn_rate": 5, "duration_seconds": 300},
        {"name": "peak_load", "users": 200, "spawn_rate": 20, "duration_seconds": 120},
    ],
    "thresholds": {
        "p50_response_ms": 2000,
        "p99_response_ms": 10000,
        "error_rate_percent": 1.0,
        "min_throughput_rps": 100,
    },
}
if load_test_config == expected_load:
    score += 1
    print("[PASS] Load test configuration is correct")
    for s in load_test_config["scenarios"]:
        print(f"       {s['name']}: {s['users']} users, {s['duration_seconds']}s")
    t = load_test_config["thresholds"]
    print(f"       Thresholds: p50<{t['p50_response_ms']}ms, p99<{t['p99_response_ms']}ms, errors<{t['error_rate_percent']}%")
else:
    print("[FAIL] Expected:", json.dumps(expected_load, indent=2))
    print("       Got:     ", json.dumps(load_test_config, indent=2) if isinstance(load_test_config, dict) else load_test_config)
print()

# ============================================================================
# TODO 4 -- Define SLA Targets
# ============================================================================

print("=" * 70)
print("TODO 4: Define SLA targets for the support agent")
print("=" * 70)
print()

sla_targets = {
    "availability_percent": 99.9,
    "p50_latency_seconds": 2.0,
    "p99_latency_seconds": 10.0,
    "error_rate_percent": 1.0,
    "throughput_rps": 100,
    "measurement_window_days": 30,
    "escalation_policy": {
        "warning_threshold": 99.5,
        "critical_threshold": 99.0,
        "notification_channels": ["pagerduty", "slack"],
    },
}

# -- Validate TODO 4 --------------------------------------------------------
total += 1
expected_sla = {
    "availability_percent": 99.9,
    "p50_latency_seconds": 2.0,
    "p99_latency_seconds": 10.0,
    "error_rate_percent": 1.0,
    "throughput_rps": 100,
    "measurement_window_days": 30,
    "escalation_policy": {
        "warning_threshold": 99.5,
        "critical_threshold": 99.0,
        "notification_channels": ["pagerduty", "slack"],
    },
}
if sla_targets == expected_sla:
    score += 1
    print("[PASS] SLA targets are correct")
    print(f"       Availability: {sla_targets['availability_percent']}%")
    print(f"       p50 latency:  {sla_targets['p50_latency_seconds']}s")
    print(f"       p99 latency:  {sla_targets['p99_latency_seconds']}s")
    print(f"       Error rate:   <{sla_targets['error_rate_percent']}%")
else:
    print("[FAIL] Expected:", json.dumps(expected_sla, indent=2))
    print("       Got:     ", json.dumps(sla_targets, indent=2) if isinstance(sla_targets, dict) else sla_targets)
print()

# ============================================================================
# TODO 5 -- Map Test Types to Components
# ============================================================================

print("=" * 70)
print("TODO 5: Map test types to the components they cover")
print("=" * 70)
print()

test_coverage_map = {
    "unit":        ["api_models", "tool_schemas", "cost_calculation", "state_logic"],
    "integration": ["api_to_agent", "agent_to_chromadb", "agent_to_llm", "observability"],
    "e2e":         ["full_support_flow", "ticket_lifecycle"],
    "load":        ["api_throughput", "concurrent_agents"],
}

# -- Validate TODO 5 --------------------------------------------------------
total += 1
expected_coverage = {
    "unit":        ["api_models", "tool_schemas", "cost_calculation", "state_logic"],
    "integration": ["api_to_agent", "agent_to_chromadb", "agent_to_llm", "observability"],
    "e2e":         ["full_support_flow", "ticket_lifecycle"],
    "load":        ["api_throughput", "concurrent_agents"],
}
if test_coverage_map == expected_coverage:
    score += 1
    print("[PASS] Test coverage mapping is correct")
    for test_type, components in test_coverage_map.items():
        print(f"       {test_type}: {components}")
else:
    print("[FAIL] Expected:", json.dumps(expected_coverage, indent=2))
    print("       Got:     ", json.dumps(test_coverage_map, indent=2) if isinstance(test_coverage_map, dict) else test_coverage_map)
print()

# ============================================================================
# Save test plan to WORKDIR
# ============================================================================

if score == total:
    test_plan = {
        "unit_tests": unit_tests,
        "integration_tests": integration_tests,
        "load_test_config": load_test_config,
        "sla_targets": sla_targets,
        "test_coverage_map": test_coverage_map,
    }
    out_path = os.path.join(WORKDIR, "test_plan.json")
    with open(out_path, "w") as f:
        json.dump(test_plan, f, indent=2)
    print(f"Complete test plan saved to {out_path}")
    print()

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print(f"Lab 07 Score: {score}/{total}")
print("=" * 70)
