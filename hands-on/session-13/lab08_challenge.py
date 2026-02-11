"""
Lab 08 Challenge: Complete Observability Stack
================================================
Design and configure a complete observability setup
for an AI agent application: metrics, logs, traces.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-08"

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
print("    AI Stack:")
print("      agent-api (3 replicas) → ChromaDB + Redis")
print()
print("    Observability Stack (monitoring namespace):")
print("      OTel Collector → Jaeger (traces)")
print("                     → Prometheus (metrics)")
print("                     → Loki (logs)")
print("      Grafana ← all three backends")
print()
print("    Deliverables:")
print("      1. OTel Collector ConfigMap")
print("      2. Agent Deployment with OTel env vars")
print("      3. Observability design (what to instrument)")


# ============================================================
# TODO 1: OTel Collector ConfigMap
# ============================================================

print("\n\n--- TODO 1: OTel Collector ConfigMap ---\n")

print("  Create a complete OTel Collector ConfigMap:")
print("    - Receiver: OTLP (gRPC 4317, HTTP 4318)")
print("    - Processors: batch (timeout 5s), memory_limiter (512 MiB)")
print("    - Exporter traces: otlp/jaeger (endpoint jaeger:4317)")
print("    - Exporter metrics: prometheus (endpoint 0.0.0.0:8889)")
print("    - Pipeline traces: otlp → memory_limiter,batch → otlp/jaeger")
print("    - Pipeline metrics: otlp → memory_limiter,batch → prometheus")

todo1_yaml = textwrap.dedent("""\
    # TODO: Complete OTel Collector ConfigMap
    # apiVersion: v1, kind: ConfigMap
    # name: otel-collector-config, namespace: monitoring
    # data.config.yaml with full collector config

""")

with open(os.path.join(WORKDIR, "otel-collector-configmap.yaml"), "w") as f:
    f.write(todo1_yaml)


# ============================================================
# TODO 2: Agent Deployment with OTel
# ============================================================

print("\n\n--- TODO 2: Agent Deployment with OTel ---\n")

print("  Create a K8s Deployment for agent-api with full OTel config:")
print("    - name: agent-api, replicas: 3, image: agent-api:2.0")
print("    - containerPort: 8000")
print("    - env OTEL_SERVICE_NAME: agent-api")
print("    - env OTEL_EXPORTER_OTLP_ENDPOINT: http://otel-collector.monitoring:4317")
print("    - env OTEL_RESOURCE_ATTRIBUTES: deployment.environment=production,service.version=2.0")
print("    - env OTEL_TRACES_SAMPLER: parentbased_traceidratio")
print("    - env OTEL_TRACES_SAMPLER_ARG: 0.1")
print("    - Prometheus annotations: scrape=true, port=8000, path=/metrics")
print("    - readinessProbe: /health port 8000 (delay=5, period=10)")
print("    - resources: requests 256Mi/250m, limits 1Gi/1000m")

todo2_yaml = textwrap.dedent("""\
    # TODO: Agent Deployment with OTel env vars and Prometheus annotations

""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo2_yaml)


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
# design[0]["metrics"] = "request count, latency histogram, error rate"
# design[0]["logs"] = "request received, response sent, errors with trace_id"
# design[0]["traces"] = "chat_request span with child spans for each step"
# ...


# ============================================================
# Validation
# ============================================================

print("\n\n--- Challenge Validation ---\n")

results = []

# TODO 1: ConfigMap
results.append(("ConfigMap: kind",              "kind: ConfigMap" in todo1_yaml))
results.append(("ConfigMap: namespace",          "monitoring" in todo1_yaml))
results.append(("ConfigMap: receivers",          "receivers:" in todo1_yaml))
results.append(("ConfigMap: OTLP receiver",      "otlp:" in todo1_yaml))
results.append(("ConfigMap: port 4317",          "4317" in todo1_yaml))
results.append(("ConfigMap: port 4318",          "4318" in todo1_yaml))
results.append(("ConfigMap: batch processor",    "batch:" in todo1_yaml))
results.append(("ConfigMap: memory_limiter",     "memory_limiter:" in todo1_yaml))
results.append(("ConfigMap: jaeger exporter",    "jaeger" in todo1_yaml))
results.append(("ConfigMap: prometheus exporter", "prometheus:" in todo1_yaml))
results.append(("ConfigMap: pipelines",          "pipelines:" in todo1_yaml))

# TODO 2: Deployment
results.append(("Deploy: kind Deployment",       "kind: Deployment" in todo2_yaml))
results.append(("Deploy: replicas 3",            "replicas: 3" in todo2_yaml))
results.append(("Deploy: agent-api image",       "agent-api:2.0" in todo2_yaml))
results.append(("Deploy: OTEL_SERVICE_NAME",     "OTEL_SERVICE_NAME" in todo2_yaml))
results.append(("Deploy: OTLP endpoint",         "OTEL_EXPORTER_OTLP_ENDPOINT" in todo2_yaml))
results.append(("Deploy: resource attributes",   "OTEL_RESOURCE_ATTRIBUTES" in todo2_yaml))
results.append(("Deploy: sampler config",        "OTEL_TRACES_SAMPLER" in todo2_yaml))
results.append(("Deploy: prometheus.io/scrape",  "prometheus.io/scrape" in todo2_yaml))
results.append(("Deploy: readinessProbe",        "readinessProbe:" in todo2_yaml))
results.append(("Deploy: resources",             "resources:" in todo2_yaml))

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

print(f"\n  Deploy order on a real cluster:")
print(f"    1. kubectl apply -f otel-collector-configmap.yaml")
print(f"    2. kubectl apply -f otel-collector-deployment.yaml")
print(f"    3. kubectl apply -f agent-deployment.yaml")
print(f"    4. kubectl port-forward -n monitoring svc/jaeger 16686:16686")

print("\n" + "=" * 60)
print("Challenge complete!")
print(f"- OTel Collector: ConfigMap with receivers/processors/exporters")
print(f"- Agent: Deployment with OTEL_* env vars + Prometheus annotations")
print(f"- Design: Metrics/logs/traces for 4 AI components")
print(f"- {passed}/{total} validation checks passing")
