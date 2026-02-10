"""
Lab 01: Prometheus Basics
==========================
Learn pull-based metrics collection, the Prometheus
text format, and scrape configuration.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-01"

print("=" * 50)
print("  Lab 01: Prometheus Basics")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Pull-Based Architecture
# ============================================================

print("\n--- Step 1: Pull-Based Architecture ---\n")

print("  Prometheus PULLS metrics from your app on a schedule:\n")
print("    Prometheus ─── scrape every 15s ──→ agent-api:8000/metrics")
print("    Prometheus ─── scrape every 15s ──→ chromadb:8000/metrics")
print("    Prometheus ─── scrape every 15s ──→ redis-exporter:9121/metrics")
print()
print("  Pull vs Push:")
print(f"    {'Pull (Prometheus)':<35} {'Push (StatsD, CloudWatch)'}")
print(f"    {'Server scrapes targets':<35} {'Apps push to collector'}")
print(f"    {'Simpler app code':<35} {'App manages send logic'}")
print(f"    {'Detects target down (no data)':<35} {'Cannot detect down targets'}")
print(f"    {'Prometheus, Thanos':<35} {'StatsD, Datadog Agent'}")


# ============================================================
# Step 2: Prometheus Text Format
# ============================================================

print("\n\n--- Step 2: Prometheus Text Format ---\n")

print("  What GET /metrics returns:\n")

metrics_text = textwrap.dedent("""\
    # HELP agent_requests_total Total number of agent requests
    # TYPE agent_requests_total counter
    agent_requests_total{endpoint="/chat",status="200"} 1247
    agent_requests_total{endpoint="/chat",status="500"} 13
    agent_requests_total{endpoint="/health"} 85432

    # HELP agent_active_connections Current active connections
    # TYPE agent_active_connections gauge
    agent_active_connections 42

    # HELP agent_request_duration_seconds Request duration histogram
    # TYPE agent_request_duration_seconds histogram
    agent_request_duration_seconds_bucket{le="0.1"} 210
    agent_request_duration_seconds_bucket{le="0.5"} 890
    agent_request_duration_seconds_bucket{le="1.0"} 1150
    agent_request_duration_seconds_bucket{le="+Inf"} 1247
    agent_request_duration_seconds_sum 523.47
    agent_request_duration_seconds_count 1247
""")

for line in metrics_text.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "sample-metrics.txt"), "w") as f:
    f.write(metrics_text)

print("\n  Format rules:")
print("    # HELP <name> <description>")
print("    # TYPE <name> <type>")
print("    <name>{<labels>} <value>")


# ============================================================
# Step 3: Prometheus Components
# ============================================================

print("\n\n--- Step 3: Prometheus Components ---\n")

components = [
    ("Prometheus Server", "9090",  "Scraper + TSDB + Rules engine"),
    ("Alertmanager",      "9093",  "Deduplication, routing, notification"),
    ("Grafana",           "3000",  "Visualization and dashboards"),
    ("Node Exporter",     "9100",  "Host-level metrics (CPU, disk, network)"),
    ("kube-state-metrics","8080",  "K8s object state (pods, deployments, nodes)"),
]

print(f"  {'Component':<22} {'Port':<8} {'Purpose'}")
print(f"  {'-'*65}")
for name, port, purpose in components:
    print(f"  {name:<22} {port:<8} {purpose}")


# ============================================================
# TODO 1: Create Prometheus scrape config
# ============================================================

print("\n\n--- TODO 1: Prometheus Scrape Configuration ---\n")

print("  Create a prometheus.yml with these scrape configs:")
print("    global: scrape_interval 15s, evaluation_interval 15s")
print("    job 1: agent-api, target agent-api:8000, path /metrics")
print("    job 2: redis, target redis-exporter:9121")
print("    job 3: kubernetes-pods (SD with prometheus.io/scrape annotation)")

todo1_yaml = textwrap.dedent("""\
    global:
      scrape_interval: 15s
      evaluation_interval: 15s

    scrape_configs:
    - job_name: agent-api
      metrics_path: /metrics
      static_configs:
      - targets:
        - agent-api:8000

    - job_name: redis
      static_configs:
      - targets:
        - redis-exporter:9121

    - job_name: kubernetes-pods
      kubernetes_sd_configs:
      - role: pod
      relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_port]
        action: replace
        target_label: __address__
        regex: (.+)
""")

with open(os.path.join(WORKDIR, "prometheus.yml"), "w") as f:
    f.write(todo1_yaml)

config_checks = [
    ("Has global section",          "global:" in todo1_yaml),
    ("Has scrape_interval",         "scrape_interval:" in todo1_yaml),
    ("Has scrape_configs",          "scrape_configs:" in todo1_yaml),
    ("Has agent-api job",           "agent-api" in todo1_yaml),
    ("Has target 8000",             "8000" in todo1_yaml),
    ("Has redis job",               "redis" in todo1_yaml),
    ("Has target 9121",             "9121" in todo1_yaml),
    ("Has kubernetes-pods job",     "kubernetes" in todo1_yaml),
    ("Has prometheus.io/scrape",    "prometheus.io/scrape" in todo1_yaml or "prometheus_io_scrape" in todo1_yaml),
]

score1 = sum(1 for _, ok in config_checks if ok)
print(f"\n  Validating Config ({score1}/{len(config_checks)}):\n")
for name, ok in config_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Prometheus concepts quiz
# ============================================================

print("\n\n--- TODO 2: Prometheus Concepts Quiz ---\n")

quiz = [
    {
        "question": "Does Prometheus pull or push metrics?",
        "answer": "pull",
        "correct": "pull",
    },
    {
        "question": "What HTTP endpoint do apps expose for Prometheus?",
        "answer": "/metrics",
        "correct": "/metrics",
    },
    {
        "question": "What port does Prometheus server run on?",
        "answer": "9090",
        "correct": "9090",
    },
    {
        "question": "What happens when Prometheus can't scrape a target?",
        "answer": "up=0",
        "correct": "up=0",
        "hint": "The 'up' metric goes to 0 for that target",
    },
    {
        "question": "What K8s annotation tells Prometheus to scrape a pod?",
        "answer": "prometheus.io/scrape",
        "correct": "prometheus.io/scrape",
    },
]

# Answers filled in above

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace(" ", "")
    correct = q["correct"].lower().replace(" ", "")
    is_correct = answer == correct

    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score2 += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")
    if status == "TODO" and "hint" in q:
        print(f"           Hint: {q['hint']}")

print(f"\n  Score: {score2}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 01 Summary ---\n")
print("  Key concepts:")
print("    1. Prometheus is pull-based — scrapes /metrics endpoints")
print("    2. Text format: # HELP, # TYPE, metric{labels} value")
print("    3. scrape_configs define what to monitor and how often")
print("    4. K8s pod annotations enable auto-discovery")
print(f"\n  TODO 1: {score1}/{len(config_checks)} config checks passed")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
