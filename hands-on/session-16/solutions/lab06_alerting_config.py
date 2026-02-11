"""
Lab 06: Alerting Configuration
=================================
Create production alert rules with severity levels
and Alertmanager routing.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-17-06"

print("=" * 50)
print("  Lab 06: Alerting Configuration")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Alert Severity Levels
# ============================================================

print("\n--- Step 1: Alert Severity Levels ---\n")

print("  Critical alerts (page immediately):\n")
critical = [
    ("AgentDown",      "up{job='agent-api'} == 0",           "1m"),
    ("HighErrorRate",  "error_rate > 5%",                     "5m"),
    ("PodOOMKilled",   "kube_pod_container_status_last_terminated_reason{reason='OOMKilled'}", "0m"),
]
for name, expr, duration in critical:
    print(f"    {name:<18} {expr:<55} for: {duration}")

print("\n  Warning alerts (Slack notification):\n")
warning = [
    ("HighLatency",    "p99 > 10s",                           "10m"),
    ("CostSpike",      "cost > 2x daily average",             "30m"),
    ("StorageHigh",    "PVC > 80% full",                      "15m"),
]
for name, expr, duration in warning:
    print(f"    {name:<18} {expr:<55} for: {duration}")


# ============================================================
# Step 2: Alertmanager Routing
# ============================================================

print("\n\n--- Step 2: Alertmanager Routing ---\n")

routing_yaml = textwrap.dedent("""\
    route:
      receiver: default-slack
      group_by: [alertname, namespace]
      group_wait: 30s
      group_interval: 5m
      repeat_interval: 4h
      routes:
      - match:
          severity: critical
        receiver: pagerduty-critical
      - match:
          severity: warning
        receiver: slack-warnings

    receivers:
    - name: pagerduty-critical
      pagerduty_configs:
      - service_key: "<pagerduty-key>"
    - name: slack-warnings
      slack_configs:
      - api_url: "<slack-webhook>"
        channel: "#ai-alerts"
    - name: default-slack
      slack_configs:
      - api_url: "<slack-webhook>"
        channel: "#monitoring"
""")

print("  Alertmanager routing config:\n")
for line in routing_yaml.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "alertmanager-reference.yaml"), "w") as f:
    f.write(routing_yaml)


# ============================================================
# TODO 1: Create alert rules
# ============================================================

print("\n\n--- TODO 1: Alert Rules ---\n")

print("  Create Prometheus alert rules with:")
print("    1. AgentDown: up{job='agent-api'} == 0 for 1m (critical)")
print("    2. HighErrorRate: error rate > 5% for 5m (critical)")
print("    3. HighLatency: p99 > 10s for 10m (warning)")
print("    4. CostSpike: hourly cost > $5 for 30m (warning)")
print("    5. PVCNearlyFull: PVC > 80% for 15m (warning)")
print("    Each alert needs: expr, for, labels (severity), annotations\n")

todo1_yaml = textwrap.dedent("""\
    groups:
    - name: ai-stack-alerts
      rules:
      - alert: AgentDown
        expr: up{job="agent-api"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Agent API is down"
          description: "Agent API has been unreachable for more than 1 minute."

      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate on Agent API"
          description: "Error rate is above 5% for the last 5 minutes."

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(http_request_duration_seconds_bucket[5m])) > 10
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "High p99 latency on Agent API"
          description: "p99 latency is above 10 seconds for the last 10 minutes."

      - alert: CostSpike
        expr: sum(rate(llm_cost_usd_total[1h])) > 5
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "LLM cost spike detected"
          description: "Hourly LLM cost exceeds $5 for the last 30 minutes."

      - alert: PVCNearlyFull
        expr: kubelet_volume_stats_used_bytes / kubelet_volume_stats_capacity_bytes > 0.80
        for: 15m
        labels:
          severity: warning
        annotations:
          summary: "PVC is nearly full"
          description: "PVC usage is above 80% for the last 15 minutes."
""")

with open(os.path.join(WORKDIR, "alert-rules.yaml"), "w") as f:
    f.write(todo1_yaml)

checks1 = [
    ("Has groups section",          "groups:" in todo1_yaml),
    ("Has AgentDown",               "AgentDown" in todo1_yaml),
    ("Has HighErrorRate",           "HighErrorRate" in todo1_yaml),
    ("Has HighLatency",             "HighLatency" in todo1_yaml),
    ("Has CostSpike",               "CostSpike" in todo1_yaml),
    ("Has PVCNearlyFull",           "PVC" in todo1_yaml),
    ("Has severity: critical",      "critical" in todo1_yaml),
    ("Has severity: warning",       "warning" in todo1_yaml),
    ("Has for: duration",           "for:" in todo1_yaml),
    ("Has annotations",             "annotations:" in todo1_yaml),
    ("Has expr field",              "expr:" in todo1_yaml),
    ("Has summary annotation",      "summary" in todo1_yaml),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Alerting quiz
# ============================================================

print("\n\n--- TODO 2: Alerting Quiz ---\n")

quiz = [
    {
        "question": "What severity should 'agent is down' use?",
        "answer": "critical",
        "correct": "critical",
    },
    {
        "question": "What severity should 'latency is high' use?",
        "answer": "warning",
        "correct": "warning",
    },
    {
        "question": "What Alertmanager field routes alerts to receivers?",
        "answer": "route",
        "correct": "route",
    },
    {
        "question": "What field in alert rules specifies how long condition must hold?",
        "answer": "for",
        "correct": "for",
    },
    {
        "question": "Critical alerts should go to PagerDuty or Slack?",
        "answer": "pagerduty",
        "correct": "pagerduty",
        "check": "pagerduty",
    },
]

score2 = 0
for i, q in enumerate(quiz, 1):
    answer = q["answer"].strip().lower().replace(" ", "").replace("-", "").replace("_", "")
    check = q.get("check", q["correct"].lower().replace(" ", "").replace("-", "").replace("_", ""))
    is_correct = check in answer

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

print(f"\n\n--- Lab 06 Summary ---\n")
print("  Key concepts:")
print("    1. Critical alerts (down, errors, OOM) -> PagerDuty (page immediately)")
print("    2. Warning alerts (latency, cost, storage) -> Slack")
print("    3. Alert rules: expr + for duration + severity label + annotations")
print("    4. Alertmanager routes by severity to different receivers")
print(f"\n  TODO 1: {score1}/{len(checks1)} alert rule checks")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
