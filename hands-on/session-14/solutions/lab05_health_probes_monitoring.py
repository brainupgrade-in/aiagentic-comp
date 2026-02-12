#!/usr/bin/env python3
"""
Lab 05 Solution: Configure Health Probes & Monitoring

Write Kubernetes probe YAML and Prometheus scrape configuration for
the capstone support agent. Fill in probe types, timing values,
scrape intervals, and metric names.

No external packages required -- standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any

WORKDIR = "/tmp/capstone-lab-14-05"

# -- Cleanup & Setup ---------------------------------------------------------
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ============================================================================
# STEP 1 -- Kubernetes Health Probes
# ============================================================================

print("=" * 70)
print("STEP 1: Kubernetes Health Probes")
print("=" * 70)
print()
print("  Kubernetes uses three types of probes:")
print()
print("  +-------------------+--------------------------------------------+")
print("  | Probe Type        | Purpose                                    |")
print("  +-------------------+--------------------------------------------+")
print("  | livenessProbe     | Is the container alive? Restart if not.    |")
print("  | readinessProbe    | Is it ready to serve traffic? Remove from  |")
print("  |                   | service endpoints if not.                  |")
print("  | startupProbe      | Has it finished starting? Disables other   |")
print("  |                   | probes until success.                      |")
print("  +-------------------+--------------------------------------------+")
print()
print("  Probe parameters:")
print("  +---------------------+----+--------------------------------------+")
print("  | Parameter           | Ex | Meaning                              |")
print("  +---------------------+----+--------------------------------------+")
print("  | initialDelaySeconds | 10 | Wait before first probe              |")
print("  | periodSeconds       | 15 | Time between probes                  |")
print("  | timeoutSeconds      |  5 | Max time to wait for response        |")
print("  | failureThreshold    |  3 | Consecutive failures before action   |")
print("  | successThreshold    |  1 | Consecutive successes to pass        |")
print("  +---------------------+----+--------------------------------------+")
print()

# ============================================================================
# STEP 2 -- Prometheus Scrape Configuration
# ============================================================================

print("=" * 70)
print("STEP 2: Prometheus Scrape Configuration")
print("=" * 70)
print()
print("  Prometheus scrapes metrics from application /metrics endpoint.")
print()
print("  scrape_configs:")
print("    - job_name: 'support-agent'")
print("      scrape_interval: 15s")
print("      metrics_path: '/metrics'")
print("      static_configs:")
print("        - targets: ['support-agent:8000']")
print()
print("  Key metric types for AI agents:")
print()
print("  +----------------------------+------+-----------------------------+")
print("  | Metric                     | Type | What It Measures            |")
print("  +----------------------------+------+-----------------------------+")
print("  | request_duration_seconds   | hist | API response latency        |")
print("  | requests_total             | cntr | Total request count         |")
print("  | request_errors_total       | cntr | Total error count           |")
print("  | agent_invocations_total    | cntr | LangGraph agent runs        |")
print("  | llm_tokens_total           | cntr | Total LLM tokens consumed   |")
print("  | active_requests            | gaug | Current in-flight requests  |")
print("  +----------------------------+------+-----------------------------+")
print()

# ============================================================================
# TODO 1 -- Define Liveness Probe Configuration
# ============================================================================

print("=" * 70)
print("TODO 1: Define the Kubernetes liveness probe configuration")
print("=" * 70)
print()

liveness_probe = {
    "probe_type": "livenessProbe",
    "httpGet": {
        "path": "/healthz",
        "port": 8000,
    },
    "initialDelaySeconds": 10,
    "periodSeconds": 15,
    "timeoutSeconds": 5,
    "failureThreshold": 3,
}

# -- Validate TODO 1 --------------------------------------------------------
total += 1
expected_liveness = {
    "probe_type": "livenessProbe",
    "httpGet": {
        "path": "/healthz",
        "port": 8000,
    },
    "initialDelaySeconds": 10,
    "periodSeconds": 15,
    "timeoutSeconds": 5,
    "failureThreshold": 3,
}
if liveness_probe == expected_liveness:
    score += 1
    print("[PASS] Liveness probe configuration is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_liveness, indent=2))
    print("       Got:     ", json.dumps(liveness_probe, indent=2) if isinstance(liveness_probe, dict) else liveness_probe)
print()

# ============================================================================
# TODO 2 -- Define Readiness Probe Configuration
# ============================================================================

print("=" * 70)
print("TODO 2: Define the Kubernetes readiness probe configuration")
print("=" * 70)
print()

readiness_probe = {
    "probe_type": "readinessProbe",
    "httpGet": {
        "path": "/readyz",
        "port": 8000,
    },
    "initialDelaySeconds": 5,
    "periodSeconds": 10,
    "timeoutSeconds": 3,
    "failureThreshold": 3,
    "successThreshold": 1,
}

# -- Validate TODO 2 --------------------------------------------------------
total += 1
expected_readiness = {
    "probe_type": "readinessProbe",
    "httpGet": {
        "path": "/readyz",
        "port": 8000,
    },
    "initialDelaySeconds": 5,
    "periodSeconds": 10,
    "timeoutSeconds": 3,
    "failureThreshold": 3,
    "successThreshold": 1,
}
if readiness_probe == expected_readiness:
    score += 1
    print("[PASS] Readiness probe configuration is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_readiness, indent=2))
    print("       Got:     ", json.dumps(readiness_probe, indent=2) if isinstance(readiness_probe, dict) else readiness_probe)
print()

# ============================================================================
# TODO 3 -- Define Startup Probe Configuration
# ============================================================================

print("=" * 70)
print("TODO 3: Define the Kubernetes startup probe configuration")
print("=" * 70)
print()

startup_probe = {
    "probe_type": "startupProbe",
    "httpGet": {
        "path": "/healthz",
        "port": 8000,
    },
    "initialDelaySeconds": 0,
    "periodSeconds": 5,
    "timeoutSeconds": 5,
    "failureThreshold": 30,
}

# -- Validate TODO 3 --------------------------------------------------------
total += 1
expected_startup = {
    "probe_type": "startupProbe",
    "httpGet": {
        "path": "/healthz",
        "port": 8000,
    },
    "initialDelaySeconds": 0,
    "periodSeconds": 5,
    "timeoutSeconds": 5,
    "failureThreshold": 30,
}
if startup_probe == expected_startup:
    score += 1
    print("[PASS] Startup probe configuration is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_startup, indent=2))
    print("       Got:     ", json.dumps(startup_probe, indent=2) if isinstance(startup_probe, dict) else startup_probe)
print()

# ============================================================================
# TODO 4 -- Define Prometheus Scrape Configuration
# ============================================================================

print("=" * 70)
print("TODO 4: Define the Prometheus scrape configuration")
print("=" * 70)
print()

prometheus_scrape = {
    "job_name": "support-agent",
    "scrape_interval": "15s",
    "metrics_path": "/metrics",
    "static_configs": [
        {
            "targets": ["support-agent:8000"],
            "labels": {
                "environment": "production",
                "service": "ai-support",
            },
        }
    ],
}

# -- Validate TODO 4 --------------------------------------------------------
total += 1
expected_scrape = {
    "job_name": "support-agent",
    "scrape_interval": "15s",
    "metrics_path": "/metrics",
    "static_configs": [
        {
            "targets": ["support-agent:8000"],
            "labels": {
                "environment": "production",
                "service": "ai-support",
            },
        }
    ],
}
if prometheus_scrape == expected_scrape:
    score += 1
    print("[PASS] Prometheus scrape configuration is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_scrape, indent=2))
    print("       Got:     ", json.dumps(prometheus_scrape, indent=2) if isinstance(prometheus_scrape, dict) else prometheus_scrape)
print()

# ============================================================================
# TODO 5 -- Define Key Metrics
# ============================================================================

print("=" * 70)
print("TODO 5: Define the key application metrics")
print("=" * 70)
print()

metrics = {
    "request_duration": {
        "name": "request_duration_seconds",
        "type": "histogram",
        "description": "API response latency in seconds",
        "buckets": [0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
    },
    "request_count": {
        "name": "requests_total",
        "type": "counter",
        "description": "Total number of API requests",
        "labels": ["method", "endpoint", "status_code"],
    },
    "llm_tokens": {
        "name": "llm_tokens_total",
        "type": "counter",
        "description": "Total LLM tokens consumed",
        "labels": ["model", "type"],
    },
    "active_requests": {
        "name": "active_requests",
        "type": "gauge",
        "description": "Number of currently active requests",
    },
}

# -- Validate TODO 5 --------------------------------------------------------
total += 1
expected_metrics = {
    "request_duration": {
        "name": "request_duration_seconds",
        "type": "histogram",
        "description": "API response latency in seconds",
        "buckets": [0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
    },
    "request_count": {
        "name": "requests_total",
        "type": "counter",
        "description": "Total number of API requests",
        "labels": ["method", "endpoint", "status_code"],
    },
    "llm_tokens": {
        "name": "llm_tokens_total",
        "type": "counter",
        "description": "Total LLM tokens consumed",
        "labels": ["model", "type"],
    },
    "active_requests": {
        "name": "active_requests",
        "type": "gauge",
        "description": "Number of currently active requests",
    },
}
if metrics == expected_metrics:
    score += 1
    print("[PASS] Application metrics are correct")
    for key, m in metrics.items():
        print(f"       {m['name']} ({m['type']}): {m['description']}")
else:
    print("[FAIL] Expected:", json.dumps(expected_metrics, indent=2))
    print("       Got:     ", json.dumps(metrics, indent=2) if isinstance(metrics, dict) else metrics)
print()

# ============================================================================
# Save all configs to WORKDIR
# ============================================================================

all_configs = {
    "probes": {
        "liveness": liveness_probe,
        "readiness": readiness_probe,
        "startup": startup_probe,
    },
    "prometheus": prometheus_scrape,
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
