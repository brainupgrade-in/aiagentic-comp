#!/usr/bin/env python3
"""
Lab 05 Solution: Safety Monitoring — Metrics, Alerts, and Dashboards

Define safety metric classes (counters, gauges), implement alert threshold
checking, and generate a monitoring dashboard configuration.

No external packages required — standard library only.
"""

import os
import json
import shutil
import time

WORKDIR = "/tmp/safety-lab-14-05"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — Safety Metrics                                                   ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: Safety Metrics for AI Systems")
print("=" * 70)
print()
print("  Monitoring safety requires purpose-built metrics:")
print()
print("  ┌─────────────────────────┬──────────┬────────────────────────────┐")
print("  │ Metric                  │ Type     │ Description                │")
print("  ├─────────────────────────┼──────────┼────────────────────────────┤")
print("  │ injection_attempts      │ Counter  │ Total injection attempts   │")
print("  │ jailbreak_attempts      │ Counter  │ Total jailbreak attempts   │")
print("  │ pii_leaks_detected      │ Counter  │ Total PII leaks caught     │")
print("  │ policy_violations       │ Counter  │ Total policy violations    │")
print("  │ requests_blocked        │ Counter  │ Total requests blocked     │")
print("  ├─────────────────────────┼──────────┼────────────────────────────┤")
print("  │ active_safety_alerts    │ Gauge    │ Current open safety alerts │")
print("  │ safety_score            │ Gauge    │ Current system safety 0-1  │")
print("  │ guard_latency_ms        │ Gauge    │ Current guard pipeline ms  │")
print("  └─────────────────────────┴──────────┴────────────────────────────┘")
print()
print("  Counter: only increases (monotonic). Good for total event counts.")
print("  Gauge:   can increase or decrease. Good for current state.")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 2 — Alert Thresholds and Escalation                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 2: Alert Thresholds and Escalation")
print("=" * 70)
print()
print("  ┌───────────┬──────────┬─────────────────────────────────────────┐")
print("  │ Level     │ Action   │ Trigger Example                        │")
print("  ├───────────┼──────────┼─────────────────────────────────────────┤")
print("  │ INFO      │ Log      │ First injection attempt detected       │")
print("  │ WARNING   │ Alert    │ 5+ injection attempts in 10 minutes    │")
print("  │ CRITICAL  │ Page     │ 20+ attempts in 10 min, PII leak, or   │")
print("  │           │          │ safety_score drops below 0.5           │")
print("  └───────────┴──────────┴─────────────────────────────────────────┘")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Define Safety Metric Classes                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Define Counter and Gauge metric classes")
print("=" * 70)
print()

# TODO: Implement the Counter class.
#   - __init__(self, name, description): set name, description, _value=0
#   - increment(self, amount=1): add amount to _value (amount must be >= 0)
#   - value property: return _value
#   - to_dict(self): return {"name": ..., "type": "counter",
#     "value": ..., "description": ...}

class Counter:
    """A monotonically increasing counter metric."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._value = 0

    def increment(self, amount: int = 1):
        if amount < 0:
            raise ValueError("Counter can only increase")
        self._value += amount

    @property
    def value(self):
        return self._value

    def to_dict(self):
        return {
            "name": self.name,
            "type": "counter",
            "value": self._value,
            "description": self.description,
        }


# TODO: Implement the Gauge class.
#   - __init__(self, name, description): set name, description, _value=0.0
#   - set_value(self, value): set _value to value
#   - increment(self, amount=1.0): add amount to _value
#   - decrement(self, amount=1.0): subtract amount from _value
#   - value property: return _value
#   - to_dict(self): return {"name": ..., "type": "gauge",
#     "value": ..., "description": ...}

class Gauge:
    """A metric that can increase and decrease."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self._value = 0.0

    def set_value(self, value: float):
        self._value = value

    def increment(self, amount: float = 1.0):
        self._value += amount

    def decrement(self, amount: float = 1.0):
        self._value -= amount

    @property
    def value(self):
        return self._value

    def to_dict(self):
        return {
            "name": self.name,
            "type": "gauge",
            "value": self._value,
            "description": self.description,
        }

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    c = Counter("injection_attempts", "Total injection attempts detected")
    c.increment()
    c.increment(3)

    g = Gauge("safety_score", "Current system safety score")
    g.set_value(0.95)
    g.decrement(0.1)

    checks = [
        c.value == 4,
        c.to_dict()["type"] == "counter",
        c.to_dict()["name"] == "injection_attempts",
        abs(g.value - 0.85) < 0.001,
        g.to_dict()["type"] == "gauge",
        g.to_dict()["name"] == "safety_score",
    ]
    if all(checks):
        score += 1
        print("[PASS] Counter and Gauge classes work correctly")
        print(f"       Counter: {c.to_dict()}")
        print(f"       Gauge:   {g.to_dict()}")
    else:
        print(f"[FAIL] counter={c.to_dict()}, gauge={g.to_dict()}")
except Exception as e:
    print(f"[FAIL] Metric class exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Implement Alert Threshold Checking                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Implement alert threshold checking")
print("=" * 70)
print()

def check_alerts(metrics: dict) -> list:
    """Evaluate safety metrics against alert thresholds.

    Alert rules:
        1. injection_attempts >= 20  → CRITICAL "High injection volume"
        2. injection_attempts >= 5   → WARNING  "Elevated injection attempts"
        3. pii_leaks_detected >= 1   → CRITICAL "PII leak detected"
        4. safety_score < 0.5        → CRITICAL "Safety score critically low"
        5. safety_score < 0.8        → WARNING  "Safety score degraded"

    Args:
        metrics: Dict mapping metric names to their current values

    Returns:
        List of alert dicts with keys: 'level', 'metric', 'value', 'message'
        Sorted by severity (CRITICAL first, then WARNING)
    """
    # TODO: Implement the alert checking logic.
    #   Check each rule and collect alerts.
    #   Sort: CRITICAL before WARNING.

    alerts = []

    inj = metrics.get("injection_attempts", 0)
    if inj >= 20:
        alerts.append({
            "level": "CRITICAL",
            "metric": "injection_attempts",
            "value": inj,
            "message": "High injection volume",
        })
    elif inj >= 5:
        alerts.append({
            "level": "WARNING",
            "metric": "injection_attempts",
            "value": inj,
            "message": "Elevated injection attempts",
        })

    pii = metrics.get("pii_leaks_detected", 0)
    if pii >= 1:
        alerts.append({
            "level": "CRITICAL",
            "metric": "pii_leaks_detected",
            "value": pii,
            "message": "PII leak detected",
        })

    ss = metrics.get("safety_score", 1.0)
    if ss < 0.5:
        alerts.append({
            "level": "CRITICAL",
            "metric": "safety_score",
            "value": ss,
            "message": "Safety score critically low",
        })
    elif ss < 0.8:
        alerts.append({
            "level": "WARNING",
            "metric": "safety_score",
            "value": ss,
            "message": "Safety score degraded",
        })

    # Sort: CRITICAL first
    severity = {"CRITICAL": 0, "WARNING": 1, "INFO": 2}
    alerts.sort(key=lambda a: severity.get(a["level"], 99))

    return alerts

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    m1 = {"injection_attempts": 25, "pii_leaks_detected": 2, "safety_score": 0.3}
    m2 = {"injection_attempts": 7, "pii_leaks_detected": 0, "safety_score": 0.75}
    m3 = {"injection_attempts": 1, "pii_leaks_detected": 0, "safety_score": 0.95}

    a1 = check_alerts(m1)
    a2 = check_alerts(m2)
    a3 = check_alerts(m3)

    checks = [
        len(a1) == 3,  # injection CRITICAL + pii CRITICAL + score CRITICAL
        all(a["level"] == "CRITICAL" for a in a1),
        len(a2) == 2,  # injection WARNING + score WARNING
        all(a["level"] == "WARNING" for a in a2),
        len(a3) == 0,  # all within bounds
    ]
    if all(checks):
        score += 1
        print("[PASS] Alert threshold checking works correctly")
        print(f"       High risk:  {len(a1)} alerts (all CRITICAL)")
        print(f"       Medium:     {len(a2)} alerts (all WARNING)")
        print(f"       Normal:     {len(a3)} alerts")
    else:
        print(f"[FAIL] a1={a1}, a2={a2}, a3={a3}")
except Exception as e:
    print(f"[FAIL] check_alerts exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Build a Safety Dashboard Config Generator                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Generate a safety monitoring dashboard config (JSON)")
print("=" * 70)
print()

def generate_dashboard_config(metrics_list: list, alerts: list) -> dict:
    """Generate a monitoring dashboard configuration.

    Args:
        metrics_list: List of metric dicts (from Counter/Gauge.to_dict())
        alerts: List of active alert dicts

    Returns:
        Dict with keys:
            - dashboard_name (str): "AI Safety Monitor"
            - panels (list): One panel per metric, with fields:
                name, metric_name, metric_type, current_value, panel_type
            - active_alerts (list): The alerts list
            - summary (dict): total_metrics, total_alerts,
                critical_count, warning_count
    """
    # TODO: Build the dashboard config from the metrics and alerts.
    #   panel_type should be "graph" for counters and "stat" for gauges.

    panels = []
    for m in metrics_list:
        panel_type = "graph" if m["type"] == "counter" else "stat"
        panels.append({
            "name": m["name"].replace("_", " ").title(),
            "metric_name": m["name"],
            "metric_type": m["type"],
            "current_value": m["value"],
            "panel_type": panel_type,
        })

    critical_count = sum(1 for a in alerts if a["level"] == "CRITICAL")
    warning_count = sum(1 for a in alerts if a["level"] == "WARNING")

    return {
        "dashboard_name": "AI Safety Monitor",
        "panels": panels,
        "active_alerts": alerts,
        "summary": {
            "total_metrics": len(metrics_list),
            "total_alerts": len(alerts),
            "critical_count": critical_count,
            "warning_count": warning_count,
        },
    }

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    # Create sample metrics
    c1 = Counter("injection_attempts", "Total injection attempts")
    c1.increment(12)
    c2 = Counter("pii_leaks_detected", "Total PII leaks caught")
    c2.increment(1)
    g1 = Gauge("safety_score", "Current safety score")
    g1.set_value(0.72)

    metrics_list = [c1.to_dict(), c2.to_dict(), g1.to_dict()]
    sample_alerts = check_alerts({
        "injection_attempts": c1.value,
        "pii_leaks_detected": c2.value,
        "safety_score": g1.value,
    })

    dashboard = generate_dashboard_config(metrics_list, sample_alerts)

    checks = [
        dashboard["dashboard_name"] == "AI Safety Monitor",
        len(dashboard["panels"]) == 3,
        any(p["panel_type"] == "graph" for p in dashboard["panels"]),
        any(p["panel_type"] == "stat" for p in dashboard["panels"]),
        dashboard["summary"]["total_metrics"] == 3,
        dashboard["summary"]["total_alerts"] == len(sample_alerts),
        isinstance(dashboard["active_alerts"], list),
    ]
    if all(checks):
        score += 1
        print("[PASS] Dashboard config generator works correctly")
        print(f"       Name: {dashboard['dashboard_name']}")
        print(f"       Panels: {len(dashboard['panels'])}")
        print(f"       Alerts: {dashboard['summary']['total_alerts']}")
        out_path = os.path.join(WORKDIR, "dashboard_config.json")
        with open(out_path, "w") as f:
            json.dump(dashboard, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        print(f"[FAIL] dashboard={json.dumps(dashboard, indent=2)}")
except Exception as e:
    print(f"[FAIL] generate_dashboard_config exception: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 05 Score: {score}/{total}")
print("=" * 70)
