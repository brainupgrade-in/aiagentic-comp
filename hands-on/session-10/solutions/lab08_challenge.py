"""
Lab 08 Challenge: Complete Observability Stack
================================================
Design and configure a complete observability setup
for an AI agent application: metrics, logs, traces.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-10-08"

print("=" * 60)
print("  Challenge: Complete Observability Stack")
print("=" * 60)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Challenge Overview
# ============================================================

print("\n  Design a complete observability setup for an AI agent:\n")
print("    Python In-Process OTel Pipeline:")
print("      TracerProvider → BatchSpanProcessor → ConsoleSpanExporter")
print()
print("    Application Launch:")
print("      OTEL_* env vars → uvicorn + structured logging")
print()
print("    Deliverables:")
print("      1. Python OTel pipeline setup (TracerProvider + exporter)")
print("      2. Python launch script with OTel env vars + structured logging")
print("      3. Observability design (what to instrument)")


# ============================================================
# TODO 1: Python OTel Pipeline Setup
# ============================================================

print("\n\n--- TODO 1: Python OTel Pipeline Setup ---\n")

print("  Create a Python script that configures a complete OTel tracing pipeline:")
print("    - Import: trace, TracerProvider, BatchSpanProcessor, ConsoleSpanExporter, Resource")
print("    - Create Resource with service.name='agent-api', service.version='2.0.0',")
print("      deployment.environment='production'")
print("    - Create ConsoleSpanExporter instance")
print("    - Create BatchSpanProcessor wrapping the exporter")
print("    - Create TracerProvider with the resource")
print("    - Add the processor to the provider via add_span_processor()")
print("    - Set as global with trace.set_tracer_provider()")
print("    - Get a tracer with trace.get_tracer('agent.api')")

todo1_code = textwrap.dedent("""\
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        ConsoleSpanExporter,
    )
    from opentelemetry.sdk.resources import Resource

    # Create Resource to identify the service
    resource = Resource.create({
        "service.name": "agent-api",
        "service.version": "2.0.0",
        "deployment.environment": "production",
    })

    # Create exporter (ConsoleSpanExporter for development)
    exporter = ConsoleSpanExporter()

    # Create processor (BatchSpanProcessor for efficiency)
    processor = BatchSpanProcessor(exporter)

    # Create and configure TracerProvider
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # Get a tracer
    tracer = trace.get_tracer("agent.api")
""")

with open(os.path.join(WORKDIR, "otel_setup.py"), "w") as f:
    f.write(todo1_code)


# ============================================================
# TODO 2: Agent Launch Script with OTel + Structured Logging
# ============================================================

print("\n\n--- TODO 2: Agent Launch Script with OTel + Structured Logging ---\n")

print("  Create a Python launch script for agent-api with OTel env vars")
print("  and structured logging (no Docker required):")
print("    - import os, logging, uvicorn")
print("    - Set OTEL_SERVICE_NAME: agent-api")
print("    - Set OTEL_EXPORTER_OTLP_ENDPOINT: http://localhost:4317")
print("    - Set OTEL_RESOURCE_ATTRIBUTES: deployment.environment=production,service.version=2.0")
print("    - Set OTEL_TRACES_SAMPLER: parentbased_traceidratio")
print("    - Set OTEL_TRACES_SAMPLER_ARG: 0.1")
print("    - Configure structured logging with JSON-like format")
print("    - Launch uvicorn on host 0.0.0.0, port 8000, log_level info")

todo2_code = textwrap.dedent("""\
    import os
    import logging
    import uvicorn

    # OTel environment configuration
    os.environ["OTEL_SERVICE_NAME"] = "agent-api"
    os.environ["OTEL_EXPORTER_OTLP_ENDPOINT"] = "http://localhost:4317"
    os.environ["OTEL_RESOURCE_ATTRIBUTES"] = "deployment.environment=production,service.version=2.0"
    os.environ["OTEL_TRACES_SAMPLER"] = "parentbased_traceidratio"
    os.environ["OTEL_TRACES_SAMPLER_ARG"] = "0.1"

    # Structured logging configuration
    logging.basicConfig(
        level=logging.INFO,
        format='{"time":"%(asctime)s","level":"%(levelname)s","logger":"%(name)s","message":"%(message)s"}',
    )
    logger = logging.getLogger("agent-api")
    logger.info("Starting agent-api with OTel environment configured")

    # Launch uvicorn
    if __name__ == "__main__":
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=8000,
            log_level="info",
        )
""")

with open(os.path.join(WORKDIR, "launch_agent.py"), "w") as f:
    f.write(todo2_code)


# ============================================================
# TODO 3: Observability Design
# ============================================================

print("\n\n--- TODO 3: Observability Design ---\n")

print("  For each component, define what metrics, logs, and traces to collect.\n")

design = [
    {
        "component": "Agent API /chat endpoint",
        "metrics": "___",
        "logs": "___",
        "traces": "___",
        "correct_metrics": "request count, latency histogram, error rate",
        "correct_logs": "request received, response sent, errors with trace_id",
        "correct_traces": "chat_request span with child spans for each step",
    },
    {
        "component": "LLM calls (Groq/OpenAI)",
        "metrics": "___",
        "logs": "___",
        "traces": "___",
        "correct_metrics": "tokens consumed, call duration, cost, calls by model",
        "correct_logs": "model used, token counts, errors",
        "correct_traces": "llm_call span with model, tokens, cost attributes",
    },
    {
        "component": "RAG retrieval (ChromaDB)",
        "metrics": "___",
        "logs": "___",
        "traces": "___",
        "correct_metrics": "retrieval latency, docs count, cache hit rate",
        "correct_logs": "collection queried, docs found, relevance scores",
        "correct_traces": "rag_retrieval span with collection, doc count attributes",
    },
    {
        "component": "Agent tool execution",
        "metrics": "___",
        "logs": "___",
        "traces": "___",
        "correct_metrics": "tool call count, tool duration, tool errors",
        "correct_logs": "tool name, input, output, errors",
        "correct_traces": "tool_call span with tool name, duration attributes",
    },
]

# YOUR CODE HERE: Fill in the observability design
design[0]["metrics"] = "request count, latency histogram, error rate"
design[0]["logs"] = "request received, response sent, errors with trace_id"
design[0]["traces"] = "chat_request span with child spans for each step"
design[1]["metrics"] = "tokens consumed, call duration, cost, calls by model"
design[1]["logs"] = "model used, token counts, errors"
design[1]["traces"] = "llm_call span with model, tokens, cost attributes"
design[2]["metrics"] = "retrieval latency, docs count, cache hit rate"
design[2]["logs"] = "collection queried, docs found, relevance scores"
design[2]["traces"] = "rag_retrieval span with collection, doc count attributes"
design[3]["metrics"] = "tool call count, tool duration, tool errors"
design[3]["logs"] = "tool name, input, output, errors"
design[3]["traces"] = "tool_call span with tool name, duration attributes"


# ============================================================
# Validation
# ============================================================

print("\n\n--- Challenge Validation ---\n")

results = []

# TODO 1: OTel Pipeline Setup
results.append(("OTel: has Resource",               "Resource" in todo1_code))
results.append(("OTel: has ConsoleSpanExporter",     "ConsoleSpanExporter" in todo1_code))
results.append(("OTel: has BatchSpanProcessor",      "BatchSpanProcessor" in todo1_code))
results.append(("OTel: has TracerProvider",          "TracerProvider" in todo1_code))
results.append(("OTel: has service.name",            "service.name" in todo1_code))
results.append(("OTel: has service.version",         "service.version" in todo1_code))
results.append(("OTel: has deployment.environment",  "deployment.environment" in todo1_code))
results.append(("OTel: has set_tracer_provider",     "set_tracer_provider" in todo1_code))
results.append(("OTel: has get_tracer",              "get_tracer" in todo1_code))
results.append(("OTel: has add_span_processor",      "add_span_processor" in todo1_code))
results.append(("OTel: has agent.api tracer",        "agent.api" in todo1_code))

# TODO 2: Launch Script
results.append(("Launch: has os.environ",            "os.environ" in todo2_code))
results.append(("Launch: has OTEL_SERVICE_NAME",     "OTEL_SERVICE_NAME" in todo2_code))
results.append(("Launch: has OTLP endpoint",         "OTEL_EXPORTER_OTLP_ENDPOINT" in todo2_code))
results.append(("Launch: has resource attributes",   "OTEL_RESOURCE_ATTRIBUTES" in todo2_code))
results.append(("Launch: has sampler config",        "OTEL_TRACES_SAMPLER" in todo2_code))
results.append(("Launch: has sampling ratio 0.1",    "0.1" in todo2_code))
results.append(("Launch: has logging config",        "logging" in todo2_code))
results.append(("Launch: has uvicorn",               "uvicorn" in todo2_code))

# TODO 3: Design
for d in design:
    filled_metrics = d["metrics"] != "___" and len(d["metrics"].strip()) > 5
    filled_logs = d["logs"] != "___" and len(d["logs"].strip()) > 5
    filled_traces = d["traces"] != "___" and len(d["traces"].strip()) > 5
    results.append((f"Design {d['component'][:25]}: metrics", filled_metrics))
    results.append((f"Design {d['component'][:25]}: logs",    filled_logs))
    results.append((f"Design {d['component'][:25]}: traces",  filled_traces))

passed = sum(1 for _, ok in results if ok)
total = len(results)

print(f"  Results: {passed}/{total} checks passed\n")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Challenge Complete ---\n")
print(f"  Score: {passed}/{total} ({passed/total*100:.0f}%)")
print(f"\n  Files created in {WORKDIR}/:")
for root, dirs, files in os.walk(WORKDIR):
    for f in sorted(files):
        rel = os.path.relpath(os.path.join(root, f), WORKDIR)
        size = os.path.getsize(os.path.join(root, f))
        print(f"    {rel:<45} ({size} bytes)")

print(f"\n  Run order (pure Python, no Docker):")
print(f"    1. python otel_setup.py          # Configure OTel pipeline")
print(f"    2. python launch_agent.py         # Start agent with OTel env vars")
print(f"    3. Spans appear on console (dev) or in LangFuse (production)")

print("\n" + "=" * 60)
print("Challenge complete!")
print(f"- OTel Pipeline: TracerProvider + BatchSpanProcessor + ConsoleSpanExporter")
print(f"- Launch Script: OTEL_* env vars + structured logging + uvicorn")
print(f"- Design: Metrics/logs/traces for 4 AI components")
print(f"- {passed}/{total} validation checks passing")
