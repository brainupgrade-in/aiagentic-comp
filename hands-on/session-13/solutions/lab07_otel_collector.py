"""
Lab 07: OTel Collector & K8s Integration
==========================================
Deploy the OpenTelemetry Collector on Kubernetes and
connect it to backends (Jaeger, Prometheus).
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-07"

print("=" * 50)
print("  Lab 07: OTel Collector & K8s Integration")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Collector Architecture
# ============================================================

print("\n--- Step 1: Collector Architecture ---\n")

print("  The OTel Collector has 3 components:\n")

components = [
    ("Receivers",   "Ingest data from apps (OTLP, Prometheus, Jaeger format)"),
    ("Processors",  "Transform data (batch, filter, add attributes, memory limit)"),
    ("Exporters",   "Send data to backends (Jaeger, Prometheus, Loki, cloud)"),
]

for name, desc in components:
    print(f"    {name:<14} {desc}")

print("\n  Data flow:")
print("    Receivers → Processors → Exporters")
print("    (ingest)    (transform)  (output)")
print()
print("  Collector modes:")
print("    Agent mode:    DaemonSet — one per node (collect node logs/metrics)")
print("    Gateway mode:  Deployment — central aggregation point")


# ============================================================
# Step 2: Collector K8s Deployment
# ============================================================

print("\n\n--- Step 2: K8s Deployment Pattern ---\n")

print("  Monitoring namespace layout:\n")
print("    monitoring/")
print("    ├── otel-collector (Deployment, port 4317/4318)")
print("    ├── otel-collector-svc (ClusterIP)")
print("    ├── jaeger (Deployment, port 16686)")
print("    ├── prometheus (StatefulSet, port 9090)")
print("    └── grafana (Deployment, port 3000)")
print()
print("  Apps connect to: otel-collector.monitoring:4317")


# ============================================================
# Step 3: ConfigMap for Collector
# ============================================================

print("\n\n--- Step 3: Collector ConfigMap ---\n")

print("  The collector config is mounted as a ConfigMap:\n")

example_cm = textwrap.dedent("""\
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: otel-collector-config
      namespace: monitoring
    data:
      config.yaml: |
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
          memory_limiter:
            limit_mib: 512
        exporters:
          otlp/jaeger:
            endpoint: jaeger:4317
            tls:
              insecure: true
          prometheus:
            endpoint: 0.0.0.0:8889
        service:
          pipelines:
            traces:
              receivers: [otlp]
              processors: [memory_limiter, batch]
              exporters: [otlp/jaeger]
            metrics:
              receivers: [otlp]
              processors: [memory_limiter, batch]
              exporters: [prometheus]
""")

for line in example_cm.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "otel-collector-configmap-example.yaml"), "w") as f:
    f.write(example_cm)


# ============================================================
# TODO 1: Create Collector Deployment + Service
# ============================================================

print("\n\n--- TODO 1: Collector Deployment + Service ---\n")

print("  Create K8s manifests for the OTel Collector:")
print("  1. Deployment:")
print("     - name: otel-collector, namespace: monitoring")
print("     - image: otel/opentelemetry-collector:latest")
print('     - args: ["--config=/conf/config.yaml"]')
print("     - ports: 4317 (grpc), 4318 (http), 8889 (prometheus)")
print("     - volumeMount: config → /conf")
print("     - volume: configMap otel-collector-config")
print("     - resources: requests 256Mi/250m, limits 512Mi/500m")
print("  2. Service:")
print("     - name: otel-collector, namespace: monitoring")
print("     - type: ClusterIP")
print("     - ports: 4317, 4318, 8889")

todo1_deploy = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: otel-collector
      namespace: monitoring
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: otel-collector
      template:
        metadata:
          labels:
            app: otel-collector
        spec:
          containers:
          - name: otel-collector
            image: otel/opentelemetry-collector:latest
            args: ["--config=/conf/config.yaml"]
            ports:
            - containerPort: 4317
              name: grpc
            - containerPort: 4318
              name: http
            - containerPort: 8889
              name: prometheus
            volumeMounts:
            - name: config
              mountPath: /conf
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "512Mi"
                cpu: "500m"
          volumes:
          - name: config
            configMap:
              name: otel-collector-config
""")

todo1_svc = textwrap.dedent("""\
    apiVersion: v1
    kind: Service
    metadata:
      name: otel-collector
      namespace: monitoring
    spec:
      type: ClusterIP
      selector:
        app: otel-collector
      ports:
      - name: grpc
        port: 4317
        targetPort: 4317
      - name: http
        port: 4318
        targetPort: 4318
      - name: prometheus
        port: 8889
        targetPort: 8889
""")

with open(os.path.join(WORKDIR, "otel-collector-deployment.yaml"), "w") as f:
    f.write(todo1_deploy)
with open(os.path.join(WORKDIR, "otel-collector-service.yaml"), "w") as f:
    f.write(todo1_svc)

deploy_checks = [
    ("Deployment: kind",            "kind: Deployment" in todo1_deploy),
    ("Deployment: namespace",       "monitoring" in todo1_deploy),
    ("Deployment: image",           "opentelemetry-collector" in todo1_deploy),
    ("Deployment: args config",     "--config" in todo1_deploy),
    ("Deployment: port 4317",       "4317" in todo1_deploy),
    ("Deployment: port 4318",       "4318" in todo1_deploy),
    ("Deployment: volumeMount",     "volumeMount" in todo1_deploy or "volumeMounts" in todo1_deploy),
    ("Deployment: resources",       "resources:" in todo1_deploy),
]

svc_checks = [
    ("Service: kind",               "kind: Service" in todo1_svc),
    ("Service: otel-collector",     "otel-collector" in todo1_svc),
    ("Service: port 4317",          "4317" in todo1_svc),
    ("Service: port 4318",          "4318" in todo1_svc),
    ("Service: port 8889",          "8889" in todo1_svc),
]

all_checks = deploy_checks + svc_checks
score1 = sum(1 for _, ok in all_checks if ok)

print(f"\n  Validating Deployment ({sum(1 for _, ok in deploy_checks if ok)}/{len(deploy_checks)}):")
for name, ok in deploy_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")
print(f"\n  Validating Service ({sum(1 for _, ok in svc_checks if ok)}/{len(svc_checks)}):")
for name, ok in svc_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Observability architecture quiz
# ============================================================

print("\n\n--- TODO 2: Architecture Quiz ---\n")

quiz = [
    {
        "question": "What port does the OTel Collector use for gRPC OTLP?",
        "answer": "___",
        "correct": "4317",
    },
    {
        "question": "What Collector component ingests data from apps?",
        "answer": "___",
        "correct": "receivers",
    },
    {
        "question": "What K8s namespace should monitoring tools be in?",
        "answer": "___",
        "correct": "monitoring",
    },
    {
        "question": "DaemonSet collector mode: agent or gateway?",
        "answer": "___",
        "correct": "agent",
    },
    {
        "question": "What K8s object stores the collector config?",
        "answer": "___",
        "correct": "configmap",
    },
]

# YOUR CODE HERE: Fill in the answers
quiz[0]["answer"] = "4317"
quiz[1]["answer"] = "receivers"
quiz[2]["answer"] = "monitoring"
quiz[3]["answer"] = "agent"
quiz[4]["answer"] = "configmap"

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
print("    1. Collector: Receivers → Processors → Exporters")
print("    2. Deploy as Deployment (gateway) or DaemonSet (agent)")
print("    3. Config via ConfigMap, mounted at /conf/config.yaml")
print("    4. Apps connect to otel-collector.monitoring:4317")
print(f"\n  TODO 1: {score1}/{len(all_checks)} deployment checks passed")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
