#!/usr/bin/env python3
"""
Lab 06: Production Deployment Config

Write Python process management deployment configuration as structured
data: process specs, health checks, resource limits, environment
management, and startup sequencing. Fill in process configs and secrets.

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
# STEP 1 -- Python Process Management for AI Agents
# ============================================================================

print("=" * 70)
print("STEP 1: Python Process Management for AI Agent Deployment")
print("=" * 70)
print()
print("  A production Python process config includes:")
print()
print("  +------------------------+----------------------------------------+")
print("  | Field                  | Purpose                                |")
print("  +------------------------+----------------------------------------+")
print("  | module                 | Python module to run (e.g., app:app)   |")
print("  | host                   | Bind address (e.g., 0.0.0.0)          |")
print("  | port                   | Listen port (e.g., 8000)              |")
print("  | max_memory_mb          | Memory limit via psutil (e.g., 512)   |")
print("  | restart_policy         | Restart behavior (always, on_failure) |")
print("  | dotenv_path            | Path to .env file for secrets          |")
print("  | wait_for               | Services to wait for before starting   |")
print("  | health_config          | HealthChecker configuration            |")
print("  +------------------------+----------------------------------------+")
print()
print("  Resource guidelines for 8 GB Codespace:")
print("    FastAPI service:   512 MB max_memory_mb")
print("    LangFuse:          512 MB max_memory_mb")
print("    PostgreSQL:        256 MB max_memory_mb")
print("    ChromaDB:          256 MB max_memory_mb")
print()

# ============================================================================
# STEP 2 -- Restart Policies & Resource Monitoring
# ============================================================================

print("=" * 70)
print("STEP 2: Restart Policies & Resource Monitoring")
print("=" * 70)
print()
print("  Python process restart policies (via signal handlers):")
print()
print("  +------------------------+----------------------------------------+")
print("  | Policy                 | Behavior                               |")
print("  +------------------------+----------------------------------------+")
print("  | none                   | Never restart (default)                |")
print("  | always                 | Always restart on exit                 |")
print("  | on_failure             | Restart only on non-zero exit code     |")
print("  | unless_stopped         | Restart unless SIGTERM received        |")
print("  +------------------------+----------------------------------------+")
print()
print("  Resource monitoring via psutil prevents OOM:")
print("    max_memory_mb: 512    # Hard limit, process killed if exceeded")
print("    Monitor with: psutil.Process().memory_info().rss")
print()

# ============================================================================
# STEP 3 -- Secrets Management with python-dotenv
# ============================================================================

print("=" * 70)
print("STEP 3: Secrets Management with python-dotenv")
print("=" * 70)
print()
print("  python-dotenv loads secrets from .env files via load_dotenv():")
print()
print("  +------------------------+----------------------------------------+")
print("  | Secret Key             | What It Stores                         |")
print("  +------------------------+----------------------------------------+")
print("  | GROQ_API_KEY           | LLM provider API key                   |")
print("  | LANGFUSE_PUBLIC_KEY    | LangFuse observability public key      |")
print("  | LANGFUSE_SECRET_KEY    | LangFuse observability secret key      |")
print("  | LANGFUSE_HOST          | LangFuse server URL                    |")
print("  +------------------------+----------------------------------------+")
print()
print("  Best practice: Use .env file (gitignored) + .env.example template")
print()

# ============================================================================
# TODO 1 -- Define FastAPI Process Spec
# ============================================================================

print("=" * 70)
print("TODO 1: Define the process config for support-agent")
print("=" * 70)
print()

# TODO: Replace "___" with the correct process spec dict.
#   service_name: "support-agent"
#   module: "app:app"
#   host: "0.0.0.0"
#   port: 8000
#   max_memory_mb: 512
#   restart_policy: "unless_stopped"
#   dotenv_path: ".env"
#   wait_for: ["chromadb", "langfuse"]

service_spec = "___"

# -- Validate TODO 1 --------------------------------------------------------
total += 1
expected_service = {
    "service_name": "support-agent",
    "module": "app:app",
    "host": "0.0.0.0",
    "port": 8000,
    "max_memory_mb": 512,
    "restart_policy": "unless_stopped",
    "dotenv_path": ".env",
    "wait_for": ["chromadb", "langfuse"],
}
if service_spec == expected_service:
    score += 1
    print("[PASS] Support-agent process spec is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_service, indent=2))
    print("       Got:     ", json.dumps(service_spec, indent=2) if isinstance(service_spec, dict) else service_spec)
print()

# ============================================================================
# TODO 2 -- Define Service Health Check
# ============================================================================

print("=" * 70)
print("TODO 2: Define the health check config for support-agent")
print("=" * 70)
print()

# TODO: Replace "___" with the correct health check config dict.
#   url: "http://localhost:8000/healthz"
#   interval_seconds: 30
#   timeout_seconds: 10
#   retries: 3
#   start_delay_seconds: 15

healthcheck_spec = "___"

# -- Validate TODO 2 --------------------------------------------------------
total += 1
expected_healthcheck = {
    "url": "http://localhost:8000/healthz",
    "interval_seconds": 30,
    "timeout_seconds": 10,
    "retries": 3,
    "start_delay_seconds": 15,
}
if healthcheck_spec == expected_healthcheck:
    score += 1
    print("[PASS] Health check spec is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_healthcheck, indent=2))
    print("       Got:     ", json.dumps(healthcheck_spec, indent=2) if isinstance(healthcheck_spec, dict) else healthcheck_spec)
print()

# ============================================================================
# TODO 3 -- Define LangFuse Process Spec
# ============================================================================

print("=" * 70)
print("TODO 3: Define the process config for LangFuse")
print("=" * 70)
print()

# TODO: Replace "___" with the correct LangFuse process spec dict.
#   service_name: "langfuse"
#   module: "langfuse-server"
#   host: "0.0.0.0"
#   port: 3000
#   max_memory_mb: 512
#   restart_policy: "unless_stopped"
#   wait_for: ["langfuse-db"]
#   environment:
#     DATABASE_URL: "postgresql://langfuse:langfuse@localhost:5432/langfuse"
#     NEXTAUTH_URL: "http://localhost:3000"
#     NEXTAUTH_SECRET: "my-secret-key"

langfuse_spec = "___"

# -- Validate TODO 3 --------------------------------------------------------
total += 1
expected_langfuse = {
    "service_name": "langfuse",
    "module": "langfuse-server",
    "host": "0.0.0.0",
    "port": 3000,
    "max_memory_mb": 512,
    "restart_policy": "unless_stopped",
    "wait_for": ["langfuse-db"],
    "environment": {
        "DATABASE_URL": "postgresql://langfuse:langfuse@localhost:5432/langfuse",
        "NEXTAUTH_URL": "http://localhost:3000",
        "NEXTAUTH_SECRET": "my-secret-key",
    },
}
if langfuse_spec == expected_langfuse:
    score += 1
    print("[PASS] LangFuse process spec is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_langfuse, indent=2))
    print("       Got:     ", json.dumps(langfuse_spec, indent=2) if isinstance(langfuse_spec, dict) else langfuse_spec)
print()

# ============================================================================
# TODO 4 -- Define PostgreSQL and ChromaDB Process Configs
# ============================================================================

print("=" * 70)
print("TODO 4: Define PostgreSQL (langfuse-db) and ChromaDB process configs")
print("=" * 70)
print()

# TODO: Replace "___" with the correct dict containing both process specs.
#   "langfuse-db":
#     module: "postgresql"
#     port: 5432
#     max_memory_mb: 256
#     restart_policy: "unless_stopped"
#     environment:
#       POSTGRES_USER: "langfuse"
#       POSTGRES_PASSWORD: "langfuse"
#       POSTGRES_DB: "langfuse"
#     data_dir: "/tmp/langfuse-data"
#   "chromadb":
#     module: "chromadb"
#     port: 8001
#     max_memory_mb: 256
#     restart_policy: "unless_stopped"
#     data_dir: "/tmp/chroma-data"

infra_services = "___"

# -- Validate TODO 4 --------------------------------------------------------
total += 1
expected_infra = {
    "langfuse-db": {
        "module": "postgresql",
        "port": 5432,
        "max_memory_mb": 256,
        "restart_policy": "unless_stopped",
        "environment": {
            "POSTGRES_USER": "langfuse",
            "POSTGRES_PASSWORD": "langfuse",
            "POSTGRES_DB": "langfuse",
        },
        "data_dir": "/tmp/langfuse-data",
    },
    "chromadb": {
        "module": "chromadb",
        "port": 8001,
        "max_memory_mb": 256,
        "restart_policy": "unless_stopped",
        "data_dir": "/tmp/chroma-data",
    },
}
if infra_services == expected_infra:
    score += 1
    print("[PASS] Infrastructure process specs are correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_infra, indent=2))
    print("       Got:     ", json.dumps(infra_services, indent=2) if isinstance(infra_services, dict) else infra_services)
print()

# ============================================================================
# TODO 5 -- Define Environment File Template
# ============================================================================

print("=" * 70)
print("TODO 5: Define the .env file template for secrets")
print("=" * 70)
print()

# TODO: Replace "___" with the correct env file template dict.
#   file_name: ".env"
#   gitignored: True
#   variables:
#     GROQ_API_KEY: "<your-groq-api-key>"
#     LANGFUSE_PUBLIC_KEY: "<your-langfuse-public-key>"
#     LANGFUSE_SECRET_KEY: "<your-langfuse-secret-key>"
#     LANGFUSE_HOST: "http://localhost:3000"
#   best_practices:
#     - "Never commit .env to version control"
#     - "Use .env.example as a template with placeholder values"
#     - "Rotate API keys every 90 days"
#     - "Use different keys per environment (dev/staging/prod)"

env_template = "___"

# -- Validate TODO 5 --------------------------------------------------------
total += 1
expected_env = {
    "file_name": ".env",
    "gitignored": True,
    "variables": {
        "GROQ_API_KEY": "<your-groq-api-key>",
        "LANGFUSE_PUBLIC_KEY": "<your-langfuse-public-key>",
        "LANGFUSE_SECRET_KEY": "<your-langfuse-secret-key>",
        "LANGFUSE_HOST": "http://localhost:3000",
    },
    "best_practices": [
        "Never commit .env to version control",
        "Use .env.example as a template with placeholder values",
        "Rotate API keys every 90 days",
        "Use different keys per environment (dev/staging/prod)",
    ],
}
if env_template == expected_env:
    score += 1
    print("[PASS] Environment file template is correct")
else:
    print("[FAIL] Expected:", json.dumps(expected_env, indent=2))
    print("       Got:     ", json.dumps(env_template, indent=2) if isinstance(env_template, dict) else env_template)
print()

# ============================================================================
# Save all specs to WORKDIR
# ============================================================================

if score == total:
    specs = {
        "support_agent": service_spec,
        "healthcheck": healthcheck_spec,
        "langfuse": langfuse_spec,
        "infrastructure": infra_services,
        "env_template": {k: v for k, v in expected_env.items() if k != "variables"},
    }
    out_path = os.path.join(WORKDIR, "deployment_config.json")
    with open(out_path, "w") as f:
        json.dump(specs, f, indent=2)
    print(f"Deployment config saved to {out_path}")
    print()

# ============================================================================
# RESULTS
# ============================================================================

print("=" * 70)
print(f"Lab 06 Score: {score}/{total}")
print("=" * 70)
