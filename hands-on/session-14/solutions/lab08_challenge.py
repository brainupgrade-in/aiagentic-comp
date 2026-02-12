#!/usr/bin/env python3
"""
Lab 08 Solution: Final Integration Challenge -- Capstone Project

Comprehensive challenge combining all previous labs. Fill in a complete
production deployment checklist with scoring across all categories:
API design, observability, security, reliability, and testing.

No external packages required -- standard library only.
"""

import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Any

WORKDIR = "/tmp/capstone-lab-14-08"

# -- Cleanup & Setup ---------------------------------------------------------
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

print("=" * 70)
print("CHALLENGE: Production AI Support Agent -- Final Integration")
print("=" * 70)
print()
print("  Integrate everything from Labs 01-07 into a complete")
print("  production deployment specification for the AI Support Agent.")
print()
print("  Scoring categories:")
print("    1. Architecture & API Design")
print("    2. MCP Tool Integration")
print("    3. Observability & Instrumentation")
print("    4. Security & Secrets")
print("    5. Reliability & Scaling")
print("    6. Testing & Validation")
print()

# ============================================================================
# TODO 1 -- Architecture & API Design
# ============================================================================

print("=" * 70)
print("TODO 1: Architecture & API Design (from Labs 01, 03)")
print("=" * 70)
print()

api_design = {
    "project_name": "ai-support-agent",
    "version": "1.0.0",
    "framework": "fastapi",
    "base_url": "http://localhost:8000",
    "endpoints": [
        {"method": "GET",  "path": "/healthz",              "purpose": "liveness_probe"},
        {"method": "GET",  "path": "/readyz",               "purpose": "readiness_probe"},
        {"method": "POST", "path": "/api/support",          "purpose": "submit_question"},
        {"method": "GET",  "path": "/api/tickets",          "purpose": "list_tickets"},
        {"method": "GET",  "path": "/api/tickets/{id}",     "purpose": "get_ticket"},
        {"method": "GET",  "path": "/metrics",              "purpose": "prometheus_metrics"},
    ],
    "components": {
        "api_gateway": "fastapi",
        "workflow_engine": "langgraph",
        "vector_store": "chromadb",
        "llm_provider": "groq",
    },
}

# -- Validate TODO 1 --------------------------------------------------------
total += 1
expected_api = {
    "project_name": "ai-support-agent",
    "version": "1.0.0",
    "framework": "fastapi",
    "base_url": "http://localhost:8000",
    "endpoints": [
        {"method": "GET",  "path": "/healthz",              "purpose": "liveness_probe"},
        {"method": "GET",  "path": "/readyz",               "purpose": "readiness_probe"},
        {"method": "POST", "path": "/api/support",          "purpose": "submit_question"},
        {"method": "GET",  "path": "/api/tickets",          "purpose": "list_tickets"},
        {"method": "GET",  "path": "/api/tickets/{id}",     "purpose": "get_ticket"},
        {"method": "GET",  "path": "/metrics",              "purpose": "prometheus_metrics"},
    ],
    "components": {
        "api_gateway": "fastapi",
        "workflow_engine": "langgraph",
        "vector_store": "chromadb",
        "llm_provider": "groq",
    },
}
if api_design == expected_api:
    score += 1
    print("[PASS] API design specification is correct")
    print(f"       {len(api_design['endpoints'])} endpoints defined")
    print(f"       {len(api_design['components'])} components mapped")
else:
    print("[FAIL] API design mismatch")
    if isinstance(api_design, dict):
        print(f"       Keys: {list(api_design.keys())}")
    else:
        print(f"       Got: {api_design}")
print()

# ============================================================================
# TODO 2 -- MCP Tool Integration
# ============================================================================

print("=" * 70)
print("TODO 2: MCP Tool Integration (from Lab 02)")
print("=" * 70)
print()

mcp_tools = [
    {"name": "search_knowledge",  "purpose": "Search KB for answers",
     "required_params": ["query"]},
    {"name": "create_ticket",     "purpose": "Create support ticket",
     "required_params": ["subject", "description", "priority"]},
    {"name": "get_ticket_status", "purpose": "Check ticket status",
     "required_params": ["ticket_id"]},
    {"name": "escalate_ticket",   "purpose": "Escalate to human agent",
     "required_params": ["ticket_id", "reason"]},
]

# -- Validate TODO 2 --------------------------------------------------------
total += 1
expected_tools = [
    {"name": "search_knowledge",  "purpose": "Search KB for answers",
     "required_params": ["query"]},
    {"name": "create_ticket",     "purpose": "Create support ticket",
     "required_params": ["subject", "description", "priority"]},
    {"name": "get_ticket_status", "purpose": "Check ticket status",
     "required_params": ["ticket_id"]},
    {"name": "escalate_ticket",   "purpose": "Escalate to human agent",
     "required_params": ["ticket_id", "reason"]},
]
if mcp_tools == expected_tools:
    score += 1
    print(f"[PASS] MCP tools: {len(mcp_tools)} tools defined")
    for t in mcp_tools:
        print(f"       {t['name']}: {t['required_params']}")
else:
    print("[FAIL] MCP tools mismatch")
    print("       Expected:", json.dumps(expected_tools, indent=2))
print()

# ============================================================================
# TODO 3 -- Observability & Instrumentation
# ============================================================================

print("=" * 70)
print("TODO 3: Observability & Instrumentation (from Labs 04, 05)")
print("=" * 70)
print()

observability = {
    "langfuse": {
        "trace_name": "support-agent",
        "hierarchy": ["trace", "span", "generation"],
        "cost_tracking": True,
    },
    "prometheus": {
        "scrape_interval": "15s",
        "metrics_path": "/metrics",
        "key_metrics": ["request_duration_seconds", "requests_total",
                        "llm_tokens_total", "active_requests"],
    },
    "grafana": {
        "dashboards": ["api_overview", "agent_performance", "cost_tracking"],
        "alert_rules": ["high_error_rate", "high_latency", "token_budget_exceeded"],
    },
}

# -- Validate TODO 3 --------------------------------------------------------
total += 1
expected_obs = {
    "langfuse": {
        "trace_name": "support-agent",
        "hierarchy": ["trace", "span", "generation"],
        "cost_tracking": True,
    },
    "prometheus": {
        "scrape_interval": "15s",
        "metrics_path": "/metrics",
        "key_metrics": ["request_duration_seconds", "requests_total",
                        "llm_tokens_total", "active_requests"],
    },
    "grafana": {
        "dashboards": ["api_overview", "agent_performance", "cost_tracking"],
        "alert_rules": ["high_error_rate", "high_latency", "token_budget_exceeded"],
    },
}
if observability == expected_obs:
    score += 1
    print("[PASS] Observability configuration is correct")
    print(f"       LangFuse: {observability['langfuse']['hierarchy']}")
    print(f"       Prometheus: {len(observability['prometheus']['key_metrics'])} metrics")
    print(f"       Grafana: {len(observability['grafana']['dashboards'])} dashboards")
else:
    print("[FAIL] Observability mismatch")
    print("       Expected:", json.dumps(expected_obs, indent=2))
print()

# ============================================================================
# TODO 4 -- Security & Secrets
# ============================================================================

print("=" * 70)
print("TODO 4: Security & Secrets (from Lab 06)")
print("=" * 70)
print()

security = {
    "secrets": {
        "method": "kubernetes_secret",
        "secret_name": "support-agent-secrets",
        "keys": ["GROQ_API_KEY", "LANGFUSE_PUBLIC_KEY",
                 "LANGFUSE_SECRET_KEY", "CHROMADB_AUTH_TOKEN"],
    },
    "network_policies": {
        "ingress_allowed": ["api-gateway"],
        "egress_allowed": ["groq-api", "chromadb", "langfuse", "prometheus"],
    },
    "best_practices": [
        "Never hardcode secrets in source code",
        "Use envFrom with secretRef in pod spec",
        "Rotate API keys every 90 days",
        "Enable RBAC for Kubernetes namespace access",
    ],
}

# -- Validate TODO 4 --------------------------------------------------------
total += 1
expected_security = {
    "secrets": {
        "method": "kubernetes_secret",
        "secret_name": "support-agent-secrets",
        "keys": ["GROQ_API_KEY", "LANGFUSE_PUBLIC_KEY",
                 "LANGFUSE_SECRET_KEY", "CHROMADB_AUTH_TOKEN"],
    },
    "network_policies": {
        "ingress_allowed": ["api-gateway"],
        "egress_allowed": ["groq-api", "chromadb", "langfuse", "prometheus"],
    },
    "best_practices": [
        "Never hardcode secrets in source code",
        "Use envFrom with secretRef in pod spec",
        "Rotate API keys every 90 days",
        "Enable RBAC for Kubernetes namespace access",
    ],
}
if security == expected_security:
    score += 1
    print("[PASS] Security configuration is correct")
    print(f"       Secrets: {security['secrets']['keys']}")
    print(f"       Best practices: {len(security['best_practices'])} items")
else:
    print("[FAIL] Security mismatch")
    print("       Expected:", json.dumps(expected_security, indent=2))
print()

# ============================================================================
# TODO 5 -- Reliability & Scaling
# ============================================================================

print("=" * 70)
print("TODO 5: Reliability & Scaling (from Labs 05, 06)")
print("=" * 70)
print()

reliability = {
    "replicas": {"min": 2, "max": 10},
    "hpa_targets": {
        "cpu_utilization_percent": 70,
        "memory_utilization_percent": 80,
    },
    "probes": {
        "liveness":  {"path": "/healthz", "period_seconds": 15},
        "readiness": {"path": "/readyz",  "period_seconds": 10},
        "startup":   {"path": "/healthz", "period_seconds": 5, "failure_threshold": 30},
    },
    "resource_limits": {
        "requests": {"memory": "256Mi", "cpu": "250m"},
        "limits":   {"memory": "512Mi", "cpu": "500m"},
    },
    "update_strategy": {
        "type": "RollingUpdate",
        "max_surge": 1,
        "max_unavailable": 0,
    },
}

# -- Validate TODO 5 --------------------------------------------------------
total += 1
expected_reliability = {
    "replicas": {"min": 2, "max": 10},
    "hpa_targets": {
        "cpu_utilization_percent": 70,
        "memory_utilization_percent": 80,
    },
    "probes": {
        "liveness":  {"path": "/healthz", "period_seconds": 15},
        "readiness": {"path": "/readyz",  "period_seconds": 10},
        "startup":   {"path": "/healthz", "period_seconds": 5, "failure_threshold": 30},
    },
    "resource_limits": {
        "requests": {"memory": "256Mi", "cpu": "250m"},
        "limits":   {"memory": "512Mi", "cpu": "500m"},
    },
    "update_strategy": {
        "type": "RollingUpdate",
        "max_surge": 1,
        "max_unavailable": 0,
    },
}
if reliability == expected_reliability:
    score += 1
    print("[PASS] Reliability configuration is correct")
    print(f"       Replicas: {reliability['replicas']['min']}-{reliability['replicas']['max']}")
    print(f"       CPU target: {reliability['hpa_targets']['cpu_utilization_percent']}%")
    print(f"       Strategy: {reliability['update_strategy']['type']}")
else:
    print("[FAIL] Reliability mismatch")
    print("       Expected:", json.dumps(expected_reliability, indent=2))
print()

# ============================================================================
# TODO 6 -- Testing & Validation
# ============================================================================

print("=" * 70)
print("TODO 6: Testing & Validation (from Lab 07)")
print("=" * 70)
print()

testing = {
    "unit_test_count": 5,
    "integration_test_count": 3,
    "load_test_scenarios": ["steady_state", "peak_load"],
    "sla_targets": {
        "availability_percent": 99.9,
        "p50_latency_seconds": 2.0,
        "p99_latency_seconds": 10.0,
        "error_rate_percent": 1.0,
    },
    "test_coverage_areas": ["api_models", "tool_schemas", "agent_flow",
                            "observability", "full_e2e"],
}

# -- Validate TODO 6 --------------------------------------------------------
total += 1
expected_testing = {
    "unit_test_count": 5,
    "integration_test_count": 3,
    "load_test_scenarios": ["steady_state", "peak_load"],
    "sla_targets": {
        "availability_percent": 99.9,
        "p50_latency_seconds": 2.0,
        "p99_latency_seconds": 10.0,
        "error_rate_percent": 1.0,
    },
    "test_coverage_areas": ["api_models", "tool_schemas", "agent_flow",
                            "observability", "full_e2e"],
}
if testing == expected_testing:
    score += 1
    print("[PASS] Testing summary is correct")
    print(f"       Unit tests:        {testing['unit_test_count']}")
    print(f"       Integration tests: {testing['integration_test_count']}")
    print(f"       Load scenarios:    {testing['load_test_scenarios']}")
else:
    print("[FAIL] Testing mismatch")
    print("       Expected:", json.dumps(expected_testing, indent=2))
print()

# ============================================================================
# TODO 7 -- Assemble Production Readiness Report
# ============================================================================

print("=" * 70)
print("TODO 7: Assemble the final Production Readiness Report")
print("=" * 70)
print()

production_report = {
    "report_title": "AI Support Agent - Production Readiness Report",
    "version": "1.0.0",
    "generated_at": datetime.now().isoformat(),
    "sections": {
        "api_design": api_design,
        "mcp_tools": mcp_tools,
        "observability": observability,
        "security": security,
        "reliability": reliability,
        "testing": testing,
    },
    "readiness_score": f"{score}/{total}",
    "status": "READY" if score == total else "NEEDS_WORK",
}

# -- Validate TODO 7 --------------------------------------------------------
total += 1
try:
    checks = [
        isinstance(production_report, dict),
        production_report.get("report_title") == "AI Support Agent - Production Readiness Report",
        production_report.get("version") == "1.0.0",
        "generated_at" in production_report,
        isinstance(production_report.get("sections"), dict),
        "api_design" in production_report.get("sections", {}),
        "mcp_tools" in production_report.get("sections", {}),
        "observability" in production_report.get("sections", {}),
        "security" in production_report.get("sections", {}),
        "reliability" in production_report.get("sections", {}),
        "testing" in production_report.get("sections", {}),
        "readiness_score" in production_report,
        "status" in production_report,
    ]
    if all(checks):
        score += 1
        out_path = os.path.join(WORKDIR, "production_readiness_report.json")
        production_report["readiness_score"] = f"{score}/{total}"
        production_report["status"] = "READY" if score == total else "NEEDS_WORK"
        with open(out_path, "w") as f:
            json.dump(production_report, f, indent=2, default=str)
        print(f"[PASS] Production readiness report saved to {out_path}")
        print(f"       Sections: {list(production_report['sections'].keys())}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Report checks failed at indices: {failed}")
        if isinstance(production_report, dict):
            print(f"       Keys: {list(production_report.keys())}")
        else:
            print(f"       Got: {production_report}")
except Exception as e:
    print(f"[FAIL] Report exception: {e}")
print()

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print(f"Challenge Lab 08 Score: {score}/{total}")
print("=" * 70)
print()

# Category breakdown
categories = {
    "Architecture & API Design":       1 if api_design == expected_api else 0,
    "MCP Tool Integration":            1 if mcp_tools == expected_tools else 0,
    "Observability & Instrumentation": 1 if observability == expected_obs else 0,
    "Security & Secrets":              1 if security == expected_security else 0,
    "Reliability & Scaling":           1 if reliability == expected_reliability else 0,
    "Testing & Validation":            1 if testing == expected_testing else 0,
}

print("Category Breakdown:")
print("-" * 50)
for cat, passed in categories.items():
    status = "[PASS]" if passed else "[FAIL]"
    print(f"  {status} {cat}")
print("-" * 50)
cat_score = sum(categories.values())
print(f"  Categories passed: {cat_score}/{len(categories)}")
print()

if score == total:
    print("Congratulations! You completed the Capstone Challenge!")
    print("Your AI Support Agent is production-ready!")
else:
    print(f"Keep going -- {total - score} check(s) remaining.")
print("=" * 70)
