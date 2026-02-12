#!/usr/bin/env python3
"""
Lab 05 Solution: Configure Health Checks & LangFuse Monitoring

Write Python HealthChecker configuration and LangFuse monitoring
setup for the capstone support agent. Fill in health check URLs,
timing values, callback settings, and trace configuration.

No external packages required -- standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any

WORKDIR = "/tmp/capstone-lab-15-05"

# -- Cleanup & Setup ---------------------------------------------------------
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ============================================================================
# STEP 1 -- Python Health Checker Pattern
# ============================================================================

print("=" * 70)
print("STEP 1: Python Health Checker Pattern")
print("=" * 70)
print()
print("  A Python HealthChecker monitors service health via HTTP probes:")
print()
print("  +-------------------+--------------------------------------------+")
print("  | Field             | Purpose                                    |")
print("  +-------------------+--------------------------------------------+")
print("  | url               | HTTP endpoint to probe (e.g., /healthz).   |")
print("  |                   | HTTP 200 = healthy, other = unhealthy.    |")
print("  | interval_seconds  | Time between health checks (e.g., 30).    |")
print("  | timeout_seconds   | Max time to wait for response (e.g., 10). |")
print("  | retries           | Consecutive failures before unhealthy.    |")
print("  | start_delay_seconds | Grace period before first check.        |")
print("  +-------------------+--------------------------------------------+")
print()
print("  Example HealthChecker config:")
print()
print("    health_config = {")
print('        "url": "http://localhost:8000/healthz",')
print('        "interval_seconds": 30,')
print('        "timeout_seconds": 10,')
print('        "retries": 3,')
print('        "start_delay_seconds": 15,')
print("    }")
print()

# ============================================================================
# STEP 2 -- LangFuse Trace Monitoring
# ============================================================================

print("=" * 70)
print("STEP 2: LangFuse Trace Monitoring")
print("=" * 70)
print()
print("  LangFuse provides LLM observability via its CallbackHandler.")
print("  It captures traces, spans, and generations automatically.")
print()
print("  Trace hierarchy:")
print("    trace -> span -> generation")
print()
print("  +----------------------------+-----------------------------------+")
print("  | LangFuse Feature           | What It Monitors                  |")
print("  +----------------------------+-----------------------------------+")
print("  | Traces                     | End-to-end request lifecycle      |")
print("  | Spans                      | Individual steps (tool calls)     |")
print("  | Generations                | LLM calls with token counts       |")
print("  | Cost tracking              | Per-request and aggregate cost    |")
print("  | Latency metrics            | Response time per trace/span      |")
print("  | Feedback scores            | User satisfaction ratings         |")
print("  +----------------------------+-----------------------------------+")
print()

# ============================================================================
# TODO 1 -- Define Health Check Config for FastAPI Service
# ============================================================================

print("=" * 70)
print("TODO 1: Define the health check config for the FastAPI service")
print("=" * 70)
print()

fastapi_healthcheck = {
    "url": "http://localhost:8000/healthz",
    "interval_seconds": 30,
    "timeout_seconds": 10,
    "retries": 3,
    "start_delay_seconds": 15,
}

# -- Validate TODO 1 --------------------------------------------------------
total += 1
expected_fastapi_hc = {
    "url": "http://localhost:8000/healthz",
    "interval_seconds": 30,
    "timeout_seconds": 10,
    "retries": 3,
    "start_delay_seconds": 15,
}
if fastapi_healthcheck == expected_fastapi_hc:
    score += 1
    print("[PASS] FastAPI health check configuration is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_fastapi_hc, indent=2))
    print("       Got:     ", json.dumps(fastapi_healthcheck, indent=2) if isinstance(fastapi_healthcheck, dict) else fastapi_healthcheck)
print()

# ============================================================================
# TODO 2 -- Define Health Check Config for ChromaDB Service
# ============================================================================

print("=" * 70)
print("TODO 2: Define the health check config for the ChromaDB service")
print("=" * 70)
print()

chromadb_healthcheck = {
    "url": "http://localhost:8001/api/v1/heartbeat",
    "interval_seconds": 30,
    "timeout_seconds": 10,
    "retries": 3,
    "start_delay_seconds": 10,
}

# -- Validate TODO 2 --------------------------------------------------------
total += 1
expected_chromadb_hc = {
    "url": "http://localhost:8001/api/v1/heartbeat",
    "interval_seconds": 30,
    "timeout_seconds": 10,
    "retries": 3,
    "start_delay_seconds": 10,
}
if chromadb_healthcheck == expected_chromadb_hc:
    score += 1
    print("[PASS] ChromaDB health check configuration is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_chromadb_hc, indent=2))
    print("       Got:     ", json.dumps(chromadb_healthcheck, indent=2) if isinstance(chromadb_healthcheck, dict) else chromadb_healthcheck)
print()

# ============================================================================
# TODO 3 -- Define Health Check Config for LangFuse Service
# ============================================================================

print("=" * 70)
print("TODO 3: Define the health check config for the LangFuse service")
print("=" * 70)
print()

langfuse_healthcheck = {
    "url": "http://localhost:3000/api/public/health",
    "interval_seconds": 30,
    "timeout_seconds": 10,
    "retries": 3,
    "start_delay_seconds": 20,
}

# -- Validate TODO 3 --------------------------------------------------------
total += 1
expected_langfuse_hc = {
    "url": "http://localhost:3000/api/public/health",
    "interval_seconds": 30,
    "timeout_seconds": 10,
    "retries": 3,
    "start_delay_seconds": 20,
}
if langfuse_healthcheck == expected_langfuse_hc:
    score += 1
    print("[PASS] LangFuse health check configuration is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_langfuse_hc, indent=2))
    print("       Got:     ", json.dumps(langfuse_healthcheck, indent=2) if isinstance(langfuse_healthcheck, dict) else langfuse_healthcheck)
print()

# ============================================================================
# TODO 4 -- Define LangFuse Callback Configuration
# ============================================================================

print("=" * 70)
print("TODO 4: Define the LangFuse callback handler configuration")
print("=" * 70)
print()

langfuse_callback = {
    "trace_name": "support-agent",
    "session_tracking": True,
    "user_tracking": True,
    "metadata_fields": ["request_id", "user_id", "session_id"],
    "cost_tracking": True,
    "feedback_enabled": True,
}

# -- Validate TODO 4 --------------------------------------------------------
total += 1
expected_callback = {
    "trace_name": "support-agent",
    "session_tracking": True,
    "user_tracking": True,
    "metadata_fields": ["request_id", "user_id", "session_id"],
    "cost_tracking": True,
    "feedback_enabled": True,
}
if langfuse_callback == expected_callback:
    score += 1
    print("[PASS] LangFuse callback configuration is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_callback, indent=2))
    print("       Got:     ", json.dumps(langfuse_callback, indent=2) if isinstance(langfuse_callback, dict) else langfuse_callback)
print()

# ============================================================================
# TODO 5 -- Define LangFuse Trace Monitoring Metrics
# ============================================================================

print("=" * 70)
print("TODO 5: Define the key LangFuse monitoring metrics")
print("=" * 70)
print()

metrics = {
    "trace_latency": {
        "name": "trace_latency_seconds",
        "source": "langfuse",
        "description": "End-to-end request latency from trace",
        "hierarchy_level": "trace",
    },
    "token_usage": {
        "name": "llm_tokens_total",
        "source": "langfuse",
        "description": "Total LLM tokens consumed per generation",
        "hierarchy_level": "generation",
    },
    "cost_per_request": {
        "name": "request_cost_usd",
        "source": "langfuse",
        "description": "Estimated cost per request in USD",
        "hierarchy_level": "trace",
    },
    "error_rate": {
        "name": "agent_error_rate",
        "source": "langfuse",
        "description": "Percentage of traces with errors",
        "hierarchy_level": "trace",
    },
}

# -- Validate TODO 5 --------------------------------------------------------
total += 1
expected_metrics = {
    "trace_latency": {
        "name": "trace_latency_seconds",
        "source": "langfuse",
        "description": "End-to-end request latency from trace",
        "hierarchy_level": "trace",
    },
    "token_usage": {
        "name": "llm_tokens_total",
        "source": "langfuse",
        "description": "Total LLM tokens consumed per generation",
        "hierarchy_level": "generation",
    },
    "cost_per_request": {
        "name": "request_cost_usd",
        "source": "langfuse",
        "description": "Estimated cost per request in USD",
        "hierarchy_level": "trace",
    },
    "error_rate": {
        "name": "agent_error_rate",
        "source": "langfuse",
        "description": "Percentage of traces with errors",
        "hierarchy_level": "trace",
    },
}
if metrics == expected_metrics:
    score += 1
    print("[PASS] LangFuse monitoring metrics are correct")
    for key, m in metrics.items():
        print(f"       {m['name']} ({m['hierarchy_level']}): {m['description']}")
else:
    print("[FAIL] Expected:", json.dumps(expected_metrics, indent=2))
    print("       Got:     ", json.dumps(metrics, indent=2) if isinstance(metrics, dict) else metrics)
print()

# ============================================================================
# Save all configs to WORKDIR
# ============================================================================

all_configs = {
    "healthchecks": {
        "fastapi": fastapi_healthcheck,
        "chromadb": chromadb_healthcheck,
        "langfuse": langfuse_healthcheck,
    },
    "langfuse_callback": langfuse_callback,
    "metrics": metrics,
}

if score == total:
    out_path = os.path.join(WORKDIR, "monitoring_config.json")
    with open(out_path, "w") as f:
        json.dump(all_configs, f, indent=2)
    print(f"Complete monitoring config saved to {out_path}")
    print()

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print(f"Lab 05 Score: {score}/{total}")
print("=" * 70)
