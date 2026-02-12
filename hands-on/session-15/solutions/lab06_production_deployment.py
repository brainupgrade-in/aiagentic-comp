#!/usr/bin/env python3
"""
Lab 06 Solution: Production Deployment Config

Write complete Kubernetes deployment configuration as structured data:
Deployment, Service, HPA, and Secret. Fill in resource limits,
HPA thresholds, and secret references.

No external packages required -- standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any

WORKDIR = "/tmp/capstone-lab-15-06"

# -- Cleanup & Setup ---------------------------------------------------------
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ============================================================================
# STEP 1 -- Kubernetes Deployment Spec
# ============================================================================

print("=" * 70)
print("STEP 1: Kubernetes Deployment Spec for AI Agent")
print("=" * 70)
print()
print("  A production Deployment spec includes:")
print()
print("  +------------------------+----------------------------------------+")
print("  | Field                  | Purpose                                |")
print("  +------------------------+----------------------------------------+")
print("  | replicas               | Number of pod copies (2+ for HA)       |")
print("  | resources.requests     | Minimum guaranteed CPU/memory          |")
print("  | resources.limits       | Maximum allowed CPU/memory             |")
print("  | env / envFrom          | Config and secrets injection           |")
print("  | probes                 | liveness + readiness + startup         |")
print("  | strategy               | RollingUpdate with maxSurge/maxUnavail |")
print("  +------------------------+----------------------------------------+")
print()
print("  Resource guidelines for AI agent pods (2-core Codespace):")
print("    requests: 256Mi memory, 250m CPU")
print("    limits:   512Mi memory, 500m CPU")
print()

# ============================================================================
# STEP 2 -- HPA (Horizontal Pod Autoscaler)
# ============================================================================

print("=" * 70)
print("STEP 2: Horizontal Pod Autoscaler (HPA)")
print("=" * 70)
print()
print("  HPA auto-scales pods based on metrics:")
print()
print("  +------------------------+----------------------------------------+")
print("  | Field                  | Typical Value                          |")
print("  +------------------------+----------------------------------------+")
print("  | minReplicas            | 2  (minimum for HA)                    |")
print("  | maxReplicas            | 10 (cost ceiling)                      |")
print("  | targetCPUPercent       | 70 (scale up at 70% CPU usage)         |")
print("  | targetMemoryPercent    | 80 (scale up at 80% memory usage)      |")
print("  | scaleDown.stabilize    | 300s (wait 5 min before scaling down)  |")
print("  +------------------------+----------------------------------------+")
print()

# ============================================================================
# STEP 3 -- Secrets Management
# ============================================================================

print("=" * 70)
print("STEP 3: Kubernetes Secrets for AI Agents")
print("=" * 70)
print()
print("  Secrets store sensitive configuration:")
print()
print("  +------------------------+----------------------------------------+")
print("  | Secret Key             | What It Stores                         |")
print("  +------------------------+----------------------------------------+")
print("  | GROQ_API_KEY           | LLM provider API key                   |")
print("  | LANGFUSE_PUBLIC_KEY    | LangFuse observability public key      |")
print("  | LANGFUSE_SECRET_KEY    | LangFuse observability secret key      |")
print("  | CHROMADB_AUTH_TOKEN    | Vector database auth token             |")
print("  +------------------------+----------------------------------------+")
print()
print("  Best practice: Use envFrom + secretRef (not inline env values)")
print()

# ============================================================================
# TODO 1 -- Define Deployment Spec
# ============================================================================

print("=" * 70)
print("TODO 1: Define the Kubernetes Deployment spec")
print("=" * 70)
print()

deployment_spec = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "support-agent",
        "namespace": "production",
        "labels": {
            "app": "support-agent",
            "version": "1.0.0",
        },
    },
    "spec": {
        "replicas": 2,
        "strategy": {
            "type": "RollingUpdate",
            "rollingUpdate": {
                "maxSurge": 1,
                "maxUnavailable": 0,
            },
        },
    },
}

# -- Validate TODO 1 --------------------------------------------------------
total += 1
expected_deployment = {
    "apiVersion": "apps/v1",
    "kind": "Deployment",
    "metadata": {
        "name": "support-agent",
        "namespace": "production",
        "labels": {
            "app": "support-agent",
            "version": "1.0.0",
        },
    },
    "spec": {
        "replicas": 2,
        "strategy": {
            "type": "RollingUpdate",
            "rollingUpdate": {
                "maxSurge": 1,
                "maxUnavailable": 0,
            },
        },
    },
}
if deployment_spec == expected_deployment:
    score += 1
    print("[PASS] Deployment spec is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_deployment, indent=2))
    print("       Got:     ", json.dumps(deployment_spec, indent=2) if isinstance(deployment_spec, dict) else deployment_spec)
print()

# ============================================================================
# TODO 2 -- Define Container Resource Limits
# ============================================================================

print("=" * 70)
print("TODO 2: Define container resource requests and limits")
print("=" * 70)
print()

container_spec = {
    "name": "support-agent",
    "image": "support-agent:1.0.0",
    "ports": [
        {
            "containerPort": 8000,
            "name": "http",
            "protocol": "TCP",
        }
    ],
    "resources": {
        "requests": {
            "memory": "256Mi",
            "cpu": "250m",
        },
        "limits": {
            "memory": "512Mi",
            "cpu": "500m",
        },
    },
}

# -- Validate TODO 2 --------------------------------------------------------
total += 1
expected_container = {
    "name": "support-agent",
    "image": "support-agent:1.0.0",
    "ports": [
        {
            "containerPort": 8000,
            "name": "http",
            "protocol": "TCP",
        }
    ],
    "resources": {
        "requests": {
            "memory": "256Mi",
            "cpu": "250m",
        },
        "limits": {
            "memory": "512Mi",
            "cpu": "500m",
        },
    },
}
if container_spec == expected_container:
    score += 1
    print("[PASS] Container resource spec is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_container, indent=2))
    print("       Got:     ", json.dumps(container_spec, indent=2) if isinstance(container_spec, dict) else container_spec)
print()

# ============================================================================
# TODO 3 -- Define Service Spec
# ============================================================================

print("=" * 70)
print("TODO 3: Define the Kubernetes Service spec")
print("=" * 70)
print()

service_spec = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {
        "name": "support-agent",
        "namespace": "production",
    },
    "spec": {
        "type": "ClusterIP",
        "selector": {
            "app": "support-agent",
        },
        "ports": [
            {
                "port": 80,
                "targetPort": 8000,
                "protocol": "TCP",
                "name": "http",
            }
        ],
    },
}

# -- Validate TODO 3 --------------------------------------------------------
total += 1
expected_service = {
    "apiVersion": "v1",
    "kind": "Service",
    "metadata": {
        "name": "support-agent",
        "namespace": "production",
    },
    "spec": {
        "type": "ClusterIP",
        "selector": {
            "app": "support-agent",
        },
        "ports": [
            {
                "port": 80,
                "targetPort": 8000,
                "protocol": "TCP",
                "name": "http",
            }
        ],
    },
}
if service_spec == expected_service:
    score += 1
    print("[PASS] Service spec is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_service, indent=2))
    print("       Got:     ", json.dumps(service_spec, indent=2) if isinstance(service_spec, dict) else service_spec)
print()

# ============================================================================
# TODO 4 -- Define HPA Spec
# ============================================================================

print("=" * 70)
print("TODO 4: Define the Horizontal Pod Autoscaler spec")
print("=" * 70)
print()

hpa_spec = {
    "apiVersion": "autoscaling/v2",
    "kind": "HorizontalPodAutoscaler",
    "metadata": {
        "name": "support-agent-hpa",
        "namespace": "production",
    },
    "spec": {
        "scaleTargetRef": {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "name": "support-agent",
        },
        "minReplicas": 2,
        "maxReplicas": 10,
        "metrics": [
            {
                "type": "Resource",
                "resource": {
                    "name": "cpu",
                    "target": {
                        "type": "Utilization",
                        "averageUtilization": 70,
                    },
                },
            },
            {
                "type": "Resource",
                "resource": {
                    "name": "memory",
                    "target": {
                        "type": "Utilization",
                        "averageUtilization": 80,
                    },
                },
            },
        ],
    },
}

# -- Validate TODO 4 --------------------------------------------------------
total += 1
expected_hpa = {
    "apiVersion": "autoscaling/v2",
    "kind": "HorizontalPodAutoscaler",
    "metadata": {
        "name": "support-agent-hpa",
        "namespace": "production",
    },
    "spec": {
        "scaleTargetRef": {
            "apiVersion": "apps/v1",
            "kind": "Deployment",
            "name": "support-agent",
        },
        "minReplicas": 2,
        "maxReplicas": 10,
        "metrics": [
            {
                "type": "Resource",
                "resource": {
                    "name": "cpu",
                    "target": {
                        "type": "Utilization",
                        "averageUtilization": 70,
                    },
                },
            },
            {
                "type": "Resource",
                "resource": {
                    "name": "memory",
                    "target": {
                        "type": "Utilization",
                        "averageUtilization": 80,
                    },
                },
            },
        ],
    },
}
if hpa_spec == expected_hpa:
    score += 1
    print("[PASS] HPA spec is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_hpa, indent=2))
    print("       Got:     ", json.dumps(hpa_spec, indent=2) if isinstance(hpa_spec, dict) else hpa_spec)
print()

# ============================================================================
# TODO 5 -- Define Secret Spec
# ============================================================================

print("=" * 70)
print("TODO 5: Define the Kubernetes Secret spec")
print("=" * 70)
print()

secret_spec = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {
        "name": "support-agent-secrets",
        "namespace": "production",
    },
    "type": "Opaque",
    "stringData": {
        "GROQ_API_KEY": "<groq-api-key>",
        "LANGFUSE_PUBLIC_KEY": "<langfuse-public-key>",
        "LANGFUSE_SECRET_KEY": "<langfuse-secret-key>",
        "CHROMADB_AUTH_TOKEN": "<chromadb-auth-token>",
    },
}

# -- Validate TODO 5 --------------------------------------------------------
total += 1
expected_secret = {
    "apiVersion": "v1",
    "kind": "Secret",
    "metadata": {
        "name": "support-agent-secrets",
        "namespace": "production",
    },
    "type": "Opaque",
    "stringData": {
        "GROQ_API_KEY": "<groq-api-key>",
        "LANGFUSE_PUBLIC_KEY": "<langfuse-public-key>",
        "LANGFUSE_SECRET_KEY": "<langfuse-secret-key>",
        "CHROMADB_AUTH_TOKEN": "<chromadb-auth-token>",
    },
}
if secret_spec == expected_secret:
    score += 1
    print("[PASS] Secret spec is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_secret, indent=2))
    print("       Got:     ", json.dumps(secret_spec, indent=2) if isinstance(secret_spec, dict) else secret_spec)
print()

# ============================================================================
# Save all specs to WORKDIR
# ============================================================================

if score == total:
    specs = {
        "deployment": deployment_spec,
        "container": container_spec,
        "service": service_spec,
        "hpa": hpa_spec,
        "secret": {k: v for k, v in expected_secret.items() if k != "stringData"},
    }
    out_path = os.path.join(WORKDIR, "k8s_manifests.json")
    with open(out_path, "w") as f:
        json.dump(specs, f, indent=2)
    print(f"Kubernetes manifests saved to {out_path}")
    print()

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print(f"Lab 06 Score: {score}/{total}")
print("=" * 70)
