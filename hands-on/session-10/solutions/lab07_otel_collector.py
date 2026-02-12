"""
Lab 07: Python In-Process OTel Pipeline
=========================================
Configure an OpenTelemetry pipeline entirely in Python —
TracerProvider, ConsoleSpanExporter, BatchSpanProcessor,
and Resource configuration — no Docker required.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-10-07"

print("=" * 50)
print("  Lab 07: Python In-Process OTel Pipeline")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: OTel Pipeline Architecture (In-Process)
# ============================================================

print("\n--- Step 1: OTel Pipeline Architecture (In-Process) ---\n")

print("  The OTel SDK pipeline mirrors the Collector's 3 components:\n")

components = [
    ("TracerProvider", "Creates and manages tracers (like Collector receivers)"),
    ("SpanProcessor",  "Batches/filters spans before export (like Collector processors)"),
    ("SpanExporter",   "Sends spans to backends or console (like Collector exporters)"),
]

for name, desc in components:
    print(f"    {name:<18} {desc}")

print("\n  In-process pipeline (no external Collector needed):")
print("    TracerProvider → BatchSpanProcessor → ConsoleSpanExporter")
print("    (create spans)   (batch & queue)      (print to stdout)")
print()
print("  Deployment modes:")
print("    In-process:  SDK exports directly (simpler, good for dev/testing)")
print("    With Collector: SDK → OTLP → Collector → Backend (production)")


# ============================================================
# Step 2: Python OTel SDK Components
# ============================================================

print("\n\n--- Step 2: Python OTel SDK Components ---\n")

print("  Key classes for in-process tracing:\n")

sdk_components = [
    ("TracerProvider",       "opentelemetry.sdk.trace",        "Root of the tracing pipeline"),
    ("ConsoleSpanExporter",  "opentelemetry.sdk.trace.export", "Prints spans to stdout (dev)"),
    ("BatchSpanProcessor",   "opentelemetry.sdk.trace.export", "Batches spans for efficiency"),
    ("SimpleSpanProcessor",  "opentelemetry.sdk.trace.export", "Exports spans immediately (debug)"),
    ("Resource",             "opentelemetry.sdk.resources",    "Identifies the service"),
]

print(f"  {'Class':<25} {'Module':<38} {'Purpose'}")
print(f"  {'-'*100}")
for cls, mod, purpose in sdk_components:
    print(f"  {cls:<25} {mod:<38} {purpose}")


# ============================================================
# Step 3: Complete In-Process Setup Example
# ============================================================

print("\n\n--- Step 3: Complete In-Process OTel Setup ---\n")

print("  A full Python OTel tracing setup (no Docker):\n")

setup_code = textwrap.dedent("""\
    from opentelemetry import trace
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import (
        BatchSpanProcessor,
        ConsoleSpanExporter,
    )
    from opentelemetry.sdk.resources import Resource

    # 1. Resource: identifies this service
    resource = Resource.create({
        "service.name": "agent-api",
        "service.version": "2.0.0",
        "deployment.environment": "production",
    })

    # 2. Exporter: where spans go (console for dev)
    exporter = ConsoleSpanExporter()

    # 3. Processor: batches spans before exporting
    processor = BatchSpanProcessor(exporter)

    # 4. Provider: ties it all together
    provider = TracerProvider(resource=resource)
    provider.add_span_processor(processor)
    trace.set_tracer_provider(provider)

    # 5. Get a tracer and create spans
    tracer = trace.get_tracer("agent.api")
    with tracer.start_as_current_span("handle_request") as span:
        span.set_attribute("http.method", "POST")
        span.set_attribute("http.route", "/chat")
""")

for line in setup_code.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "otel-setup-example.py"), "w") as f:
    f.write(setup_code)


# ============================================================
# TODO 1: Create Python OTel Pipeline Configuration
# ============================================================

print("\n\n--- TODO 1: Python OTel Pipeline Configuration ---\n")

print("  Create a Python script that configures an OTel tracing pipeline:")
print("  1. Import: trace, TracerProvider, BatchSpanProcessor, ConsoleSpanExporter, Resource")
print("  2. Create Resource with service.name='agent-api' and service.version='2.0.0'")
print("  3. Create ConsoleSpanExporter instance")
print("  4. Create BatchSpanProcessor wrapping the exporter")
print("  5. Create TracerProvider with the resource")
print("  6. Add the processor to the provider")
print("  7. Set as global tracer provider with trace.set_tracer_provider()")
print("  8. Get a tracer with trace.get_tracer('agent.api')")

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

with open(os.path.join(WORKDIR, "otel_pipeline.py"), "w") as f:
    f.write(todo1_code)

pipeline_checks = [
    ("Has Resource import/usage",       "Resource" in todo1_code),
    ("Has ConsoleSpanExporter",         "ConsoleSpanExporter" in todo1_code),
    ("Has BatchSpanProcessor",          "BatchSpanProcessor" in todo1_code),
    ("Has TracerProvider",              "TracerProvider" in todo1_code),
    ("Has service.name",               "service.name" in todo1_code),
    ("Has service.version",            "service.version" in todo1_code),
    ("Has set_tracer_provider",        "set_tracer_provider" in todo1_code),
    ("Has get_tracer",                 "get_tracer" in todo1_code),
    ("Has agent.api tracer name",      "agent.api" in todo1_code),
    ("Has resource in provider",       "resource" in todo1_code.lower()),
    ("Has add_span_processor",         "add_span_processor" in todo1_code),
    ("Has exporter instance",          "exporter" in todo1_code.lower()),
]

score1 = sum(1 for _, ok in pipeline_checks if ok)

print(f"\n  Validating OTel Pipeline ({score1}/{len(pipeline_checks)}):")
for name, ok in pipeline_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Architecture Quiz
# ============================================================

print("\n\n--- TODO 2: Architecture Quiz ---\n")

quiz = [
    {
        "question": "What OTel SDK class prints spans to stdout for development?",
        "answer": "___",
        "correct": "ConsoleSpanExporter",
    },
    {
        "question": "What OTel SDK class batches spans before exporting?",
        "answer": "___",
        "correct": "BatchSpanProcessor",
    },
    {
        "question": "What method registers a TracerProvider as the global default?",
        "answer": "___",
        "correct": "set_tracer_provider",
    },
    {
        "question": "What Resource attribute identifies your service by name?",
        "answer": "___",
        "correct": "service.name",
    },
    {
        "question": "What OTel SDK class creates and manages tracers?",
        "answer": "___",
        "correct": "TracerProvider",
    },
]

# YOUR CODE HERE: Fill in the answers
quiz[0]["answer"] = "ConsoleSpanExporter"
quiz[1]["answer"] = "BatchSpanProcessor"
quiz[2]["answer"] = "set_tracer_provider"
quiz[3]["answer"] = "service.name"
quiz[4]["answer"] = "TracerProvider"

score2 = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].strip().lower().replace(" ", "") == q["correct"].lower().replace(" ", "")
    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 07 Summary ---\n")
print("  Key concepts:")
print("    1. Pipeline: TracerProvider → BatchSpanProcessor → Exporter")
print("    2. ConsoleSpanExporter for dev, OTLPSpanExporter for production")
print("    3. Resource identifies service (name, version, environment)")
print("    4. In-process pipeline needs no Docker or external Collector")
print(f"\n  TODO 1: {score1}/{len(pipeline_checks)} pipeline config checks passed")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
