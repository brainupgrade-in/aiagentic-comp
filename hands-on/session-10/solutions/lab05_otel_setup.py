"""
Lab 05: OpenTelemetry Setup
=============================
Learn how to configure OpenTelemetry SDK for Python —
TracerProvider, MeterProvider, and exporters.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-10-05"

print("=" * 50)
print("  Lab 05: OpenTelemetry Setup")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: OpenTelemetry Architecture
# ============================================================

print("\n--- Step 1: OpenTelemetry Architecture ---\n")

print("  OpenTelemetry (OTel) = vendor-neutral observability framework\n")
print("  Architecture:")
print("    App (SDK) ──OTLP──> OTel Collector ──> Backends")
print("                          │")
print("                     ┌────┴────────────────────────┐")
print("                     │  receivers → processors →    │")
print("                     │              exporters       │")
print("                     └──────────────────────────────┘")
print("                          │         │         │")
print("                      LangFuse  LangFuse   LangFuse")
print("                      (traces)  (metrics)  (logs)")
print()
print("  OTLP Protocols:")
print("    gRPC   port 4317 — binary protobuf (default, fastest)")
print("    HTTP   port 4318 — HTTP/protobuf (firewall-friendly)")


# ============================================================
# Step 2: Python OTel Packages
# ============================================================

print("\n\n--- Step 2: Python OTel Packages ---\n")

packages = [
    ("opentelemetry-api",                       "Core API (tracing, metrics)"),
    ("opentelemetry-sdk",                       "SDK implementation"),
    ("opentelemetry-exporter-otlp",             "OTLP exporter (gRPC + HTTP)"),
    ("opentelemetry-instrumentation-fastapi",   "Auto-instrument FastAPI"),
    ("opentelemetry-instrumentation-requests",  "Auto-instrument HTTP requests"),
    ("opentelemetry-instrumentation-redis",     "Auto-instrument Redis calls"),
    ("opentelemetry-instrumentation-logging",   "Inject trace_id into logs"),
]

print(f"  {'Package':<50} {'Purpose'}")
print(f"  {'-'*80}")
for pkg, purpose in packages:
    print(f"  {pkg:<50} {purpose}")

print("\n  Quick install:")
print("    pip install opentelemetry-distro")
print("    opentelemetry-bootstrap -a install")


# ============================================================
# Step 3: TracerProvider Setup Code
# ============================================================

print("\n\n--- Step 3: TracerProvider Setup ---\n")

print("  The TracerProvider is the core of OTel tracing:\n")

setup_code = textwrap.dedent("""\
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.resources import Resource

    resource = Resource.create({
        "service.name": "agent-api",
        "service.version": "2.0.0",
        "deployment.environment": "production",
    })

    provider = TracerProvider(resource=resource)
    processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint="http://otel-collector:4317")
    )
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    tracer = trace.get_tracer("agent.api")
""")

for line in setup_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# TODO 1: Create OTel Configuration YAML
# ============================================================

print("\n\n--- TODO 1: OTel Collector Configuration ---\n")

print("  Create an OTel Collector configuration with:")
print("    - Receiver: OTLP (gRPC on 4317, HTTP on 4318)")
print("    - Processor: batch (timeout 5s, batch_size 1000)")
print("    - Processor: memory_limiter (limit_mib 512)")
print("    - Exporter: otlp/langfuse (endpoint langfuse:4317, insecure)")
print("    - Pipeline traces: otlp → memory_limiter,batch → otlp/langfuse")
print("    - Pipeline metrics: otlp → memory_limiter,batch → otlp/langfuse")

todo1_yaml = textwrap.dedent("""\
    receivers:
      otlp:
        protocols:
          grpc:
            endpoint: 0.0.0.0:4317
          http:
            endpoint: 0.0.0.0:4318

    processors:
      batch:
        timeout: 5s
        send_batch_size: 1000
      memory_limiter:
        limit_mib: 512

    exporters:
      otlp/langfuse:
        endpoint: langfuse:4317
        tls:
          insecure: true

    service:
      pipelines:
        traces:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [otlp/langfuse]
        metrics:
          receivers: [otlp]
          processors: [memory_limiter, batch]
          exporters: [otlp/langfuse]
""")

with open(os.path.join(WORKDIR, "otel-collector-config.yaml"), "w") as f:
    f.write(todo1_yaml)

collector_checks = [
    ("Has receivers section",       "receivers:" in todo1_yaml),
    ("Has OTLP receiver",           "otlp:" in todo1_yaml),
    ("Has gRPC port 4317",          "4317" in todo1_yaml),
    ("Has HTTP port 4318",          "4318" in todo1_yaml),
    ("Has processors section",      "processors:" in todo1_yaml),
    ("Has batch processor",         "batch:" in todo1_yaml),
    ("Has memory_limiter",          "memory_limiter:" in todo1_yaml),
    ("Has exporters section",       "exporters:" in todo1_yaml),
    ("Has langfuse exporter",       "langfuse" in todo1_yaml),
    ("Has service.pipelines",       "pipelines:" in todo1_yaml),
    ("Has traces pipeline",         "traces:" in todo1_yaml),
    ("Has metrics pipeline",        "metrics:" in todo1_yaml),
]

score1 = sum(1 for _, ok in collector_checks if ok)
print(f"\n  Validating Collector Config ({score1}/{len(collector_checks)}):\n")
for name, ok in collector_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Python Launch Script with OTel env vars
# ============================================================

print("\n\n--- TODO 2: Python Launch Script with OTel Environment ---\n")

print("  Create a Python launch script that configures OTel env vars")
print("  and starts a uvicorn server (no Docker required):")
print("    - Set OTEL_SERVICE_NAME: agent-api")
print("    - Set OTEL_EXPORTER_OTLP_ENDPOINT: http://localhost:4317")
print("    - Set OTEL_RESOURCE_ATTRIBUTES: deployment.environment=production")
print("    - Set OTEL_TRACES_SAMPLER: parentbased_traceidratio")
print("    - Set OTEL_TRACES_SAMPLER_ARG: 0.1")
print("    - Launch uvicorn on host 0.0.0.0, port 8000")

todo2_code = textwrap.dedent("""\
    import os
    import uvicorn

    # OTel environment configuration
    os.environ["OTEL_SERVICE_NAME"] = "agent-api"
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4317"
    os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment=production"
    os.environ["OTEL_TRACES_SAMPLER"] = "parentbased_traceidratio"
    os.environ["OTEL_TRACES_SAMPLER_ARG"] = "0.1"

    # Launch uvicorn on port 8000
    if __name__ == "__main__":
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            log_level="info",
        )
""")

with open(os.path.join(WORKDIR, "launch_agent_otel.py"), "w") as f:
    f.write(todo2_code)

deploy_checks = [
    ("Has os.environ usage",        "os.environ" in todo2_code),
    ("Has OTEL_SERVICE_NAME",       "OTEL_SERVICE_NAME" in todo2_code),
    ("Has OTEL_EXPORTER_OTLP_ENDPOINT", "OTEL_EXPORTER_OTLP_ENDPOINT" in todo2_code),
    ("Has localhost endpoint",      "localhost" in todo2_code),
    ("Has OTEL_RESOURCE_ATTRIBUTES", "OTEL_RESOURCE_ATTRIBUTES" in todo2_code),
    ("Has OTEL_TRACES_SAMPLER",     "OTEL_TRACES_SAMPLER" in todo2_code),
    ("Has sampling ratio 0.1",      "0.1" in todo2_code),
    ("Has uvicorn config",          "uvicorn" in todo2_code),
]

score2 = sum(1 for _, ok in deploy_checks if ok)
print(f"\n  Validating Launch Script ({score2}/{len(deploy_checks)}):\n")
for name, ok in deploy_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 05 Summary ---\n")
print("  Key concepts:")
print("    1. OTel SDK → OTLP → Collector → Backends (LangFuse)")
print("    2. TracerProvider + BatchSpanProcessor + OTLPSpanExporter")
print("    3. Resource identifies service (name, version, environment)")
print("    4. OTEL_* env vars configure SDK without code changes")
print(f"\n  TODO 1: {score1}/{len(collector_checks)} collector config checks passed")
print(f"  TODO 2: {score2}/{len(deploy_checks)} launch script checks passed")
print(f"\n  Files generated in {WORKDIR}/")
