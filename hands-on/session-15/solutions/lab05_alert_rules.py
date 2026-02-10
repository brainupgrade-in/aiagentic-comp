"""
Lab 05: Alert Rules
====================
Create Prometheus alert rules and Alertmanager
configuration for AI application monitoring.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-05"

print("=" * 50)
print("  Lab 05: Alert Rules")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Alert Architecture
# ============================================================

print("\n--- Step 1: Alert Architecture ---\n")

print("  Prometheus alerting flow:\n")
print("    1. Alert Rule:    PromQL expression evaluated every 15s")
print("    2. Pending:       Expression is true (waiting for 'for' duration)")
print("    3. Firing:        Expression true for 'for' duration → send alert")
print("    4. Alertmanager:  Receives alert → deduplicate → route → notify")
print("    5. Notification:  Slack, PagerDuty, email, webhook")
print()
print("  Alert states:")
print("    Inactive → Pending → Firing → Resolved")


# ============================================================
# Step 2: Alert Rule Structure
# ============================================================

print("\n\n--- Step 2: Alert Rule Structure ---\n")

example_rule = textwrap.dedent("""\
    groups:
    - name: agent-alerts
      rules:
      - alert: HighErrorRate              # Alert name
        expr: |                           # PromQL expression
          sum(rate(agent_requests_total{status=~"5.."}[5m]))
          / sum(rate(agent_requests_total[5m])) > 0.05
        for: 5m                           # Must be true this long
        labels:
          severity: critical              # Routing label
        annotations:
          summary: "Error rate above 5% for 5 minutes"
          description: "Current error rate: {{ $value | humanizePercentage }}"
""")

print("  Alert rule example:\n")
for line in example_rule.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "alert-rule-example.yaml"), "w") as f:
    f.write(example_rule)


# ============================================================
# Step 3: Alertmanager Routing
# ============================================================

print("\n\n--- Step 3: Alertmanager Routing ---\n")

print("  Alertmanager routes alerts based on labels:\n")

routing = textwrap.dedent("""\
    route:
      receiver: slack-default               # Default receiver
      routes:
      - match:
          severity: critical                # Critical → PagerDuty
        receiver: pagerduty-oncall
      - match:
          severity: warning                 # Warning → Slack
        receiver: slack-warnings

    receivers:
    - name: slack-default
      slack_configs:
      - channel: "#monitoring"
    - name: pagerduty-oncall
      pagerduty_configs:
      - service_key: "<key>"
    - name: slack-warnings
      slack_configs:
      - channel: "#alerts-warning"
""")

for line in routing.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# Step 4: AI-Specific Alerts
# ============================================================

print("\n\n--- Step 4: AI-Specific Alerts ---\n")

ai_alerts = [
    ("HighErrorRate",     "critical", 'Error rate > 5%',
     'sum(rate(requests{status=~"5.."}[5m])) / sum(rate(requests[5m])) > 0.05'),
    ("HighLatency",       "warning",  'p99 > 5s',
     'histogram_quantile(0.99, rate(duration_bucket[5m])) > 5'),
    ("AgentDown",         "critical", 'Target unreachable',
     'up{job="agent-api"} == 0'),
    ("HighTokenBurn",     "warning",  'Token rate > 2x normal',
     'rate(tokens_total[10m]) > 2 * avg_over_time(rate(tokens_total[10m])[24h:1h])'),
    ("HighCostRate",      "critical", 'Cost > $5/hour',
     'rate(cost_usd[1h]) * 3600 > 5'),
    ("ChromaDBDown",      "critical", 'Vector store unreachable',
     'up{job="chromadb"} == 0'),
]

print(f"  {'Alert':<22} {'Severity':<12} {'Condition':<25} {'PromQL'}")
print(f"  {'-'*100}")
for name, sev, cond, promql in ai_alerts:
    print(f"  {name:<22} {sev:<12} {cond:<25} {promql[:45]}")


# ============================================================
# TODO 1: Create alert rules YAML
# ============================================================

print("\n\n--- TODO 1: Create Alert Rules ---\n")

print("  Create an alert rules file with these alerts:")
print("    1. HighErrorRate: error rate > 5% for 5m (critical)")
print("    2. HighLatency: p99 > 5s for 10m (warning)")
print("    3. AgentDown: up == 0 for 1m (critical)")
print("    4. HighTokenBurn: cost rate > $5/hour for 30m (warning)")

todo1_yaml = textwrap.dedent("""\
    groups:
    - name: agent-alerts
      rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(agent_requests_total{status=~"5.."}[5m]))
          / sum(rate(agent_requests_total[5m])) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "Error rate above 5% for 5 minutes"
          description: "Current error rate: {{ $value | humanizePercentage }}"

      - alert: HighLatency
        expr: histogram_quantile(0.99, rate(agent_request_duration_seconds_bucket[5m])) > 5
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "p99 latency above 5 seconds for 10 minutes"
          description: "Current p99 latency: {{ $value }}s"

      - alert: AgentDown
        expr: up{job="agent-api"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Agent API target is down"
          description: "agent-api has been unreachable for more than 1 minute"

      - alert: HighTokenBurn
        expr: rate(agent_estimated_cost_usd[1h]) * 3600 > 5
        for: 30m
        labels:
          severity: warning
        annotations:
          summary: "Cost rate exceeds $5/hour for 30 minutes"
          description: "Current cost rate: ${{ $value }}/hour"
""")

with open(os.path.join(WORKDIR, "alerting-rules.yaml"), "w") as f:
    f.write(todo1_yaml)

alert_checks = [
    ("Has groups section",          "groups:" in todo1_yaml),
    ("Has alert: HighErrorRate",    "HighErrorRate" in todo1_yaml),
    ("Has error rate expression",   "status" in todo1_yaml and "5" in todo1_yaml),
    ("Has for: 5m",                 "for:" in todo1_yaml),
    ("Has severity: critical",      "critical" in todo1_yaml),
    ("Has alert: HighLatency",      "HighLatency" in todo1_yaml),
    ("Has histogram_quantile",      "histogram_quantile" in todo1_yaml),
    ("Has severity: warning",       "warning" in todo1_yaml),
    ("Has alert: AgentDown",        "AgentDown" in todo1_yaml),
    ("Has up == 0",                 "up" in todo1_yaml and "0" in todo1_yaml),
    ("Has annotations",             "annotations:" in todo1_yaml),
    ("Has summary",                 "summary:" in todo1_yaml),
]

score1 = sum(1 for _, ok in alert_checks if ok)
print(f"\n  Validating Alert Rules ({score1}/{len(alert_checks)}):\n")
for name, ok in alert_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Alertmanager configuration
# ============================================================

print("\n\n--- TODO 2: Alertmanager Configuration ---\n")

print("  Create an Alertmanager config:")
print("    - Default receiver: slack-default (channel #monitoring)")
print("    - Route critical → pagerduty-oncall")
print("    - Route warning → slack-warnings (channel #alerts-warning)")

todo2_yaml = textwrap.dedent("""\
    route:
      receiver: slack-default
      routes:
      - match:
          severity: critical
        receiver: pagerduty-oncall
      - match:
          severity: warning
        receiver: slack-warnings

    receivers:
    - name: slack-default
      slack_configs:
      - channel: "#monitoring"
    - name: pagerduty-oncall
      pagerduty_configs:
      - service_key: "<key>"
    - name: slack-warnings
      slack_configs:
      - channel: "#alerts-warning"
""")

with open(os.path.join(WORKDIR, "alertmanager.yaml"), "w") as f:
    f.write(todo2_yaml)

am_checks = [
    ("Has route section",           "route:" in todo2_yaml),
    ("Has receiver field",          "receiver:" in todo2_yaml),
    ("Has routes",                  "routes:" in todo2_yaml),
    ("Has severity match",          "severity" in todo2_yaml),
    ("Has critical routing",        "critical" in todo2_yaml),
    ("Has warning routing",         "warning" in todo2_yaml),
    ("Has receivers section",       "receivers:" in todo2_yaml),
    ("Has slack config",            "slack" in todo2_yaml),
]

score2 = sum(1 for _, ok in am_checks if ok)
print(f"\n  Validating Alertmanager ({score2}/{len(am_checks)}):\n")
for name, ok in am_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 05 Summary ---\n")
print("  Key concepts:")
print("    1. Alert rules: PromQL expr + 'for' duration + severity labels")
print("    2. Alertmanager: deduplicate → route by severity → notify")
print("    3. AI-specific alerts: error rate, latency, cost, token burn, target down")
print("    4. severity: critical → PagerDuty, warning → Slack")
print(f"\n  TODO 1: {score1}/{len(alert_checks)} alert rules checks passed")
print(f"  TODO 2: {score2}/{len(am_checks)} alertmanager checks passed")
print(f"\n  Files generated in {WORKDIR}/")
