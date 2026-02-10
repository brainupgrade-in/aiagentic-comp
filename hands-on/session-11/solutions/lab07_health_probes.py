"""
Lab 07 Solution: Health Probes
================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-07"

print("=" * 50)
print("  Lab 07 Solution: Health Probes")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: Redis Health Probes
# ============================================================

print("\n--- TODO 1 Solution: Redis Probes ---\n")

redis_probe_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: redis
      labels:
        app: redis
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: redis
      template:
        metadata:
          labels:
            app: redis
        spec:
          containers:
          - name: redis
            image: redis:7-alpine
            ports:
            - containerPort: 6379
            resources:
              requests:
                memory: "64Mi"
                cpu: "100m"
              limits:
                memory: "128Mi"
                cpu: "200m"

            livenessProbe:
              tcpSocket:
                port: 6379
              initialDelaySeconds: 5
              periodSeconds: 10
              failureThreshold: 3

            readinessProbe:
              exec:
                command:
                - redis-cli
                - ping
              initialDelaySeconds: 5
              periodSeconds: 10
              failureThreshold: 3
""")

with open(os.path.join(WORKDIR, "redis-deployment-probes.yaml"), "w") as f:
    f.write(redis_probe_yaml)

redis_checks = [
    ("Has livenessProbe", "livenessProbe:" in redis_probe_yaml),
    ("Has readinessProbe", "readinessProbe:" in redis_probe_yaml),
    ("Uses tcpSocket", "tcpSocket:" in redis_probe_yaml),
    ("Uses exec command", "exec:" in redis_probe_yaml),
    ("Has initialDelaySeconds", "initialDelaySeconds:" in redis_probe_yaml),
    ("Has periodSeconds", "periodSeconds:" in redis_probe_yaml),
]

passed = sum(1 for _, ok in redis_checks if ok)
print(f"  Redis probe validation ({passed}/{len(redis_checks)}):")
for name, ok in redis_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Redis probe strategy:")
print("    Liveness:  tcpSocket on 6379 — is Redis accepting connections?")
print("    Readiness: exec 'redis-cli ping' — can Redis respond to commands?")
print("    Why different? A TCP connection might succeed even if Redis is overloaded.")
print("    The PING command verifies Redis can actually serve requests.")


# ============================================================
# TODO 2 Solution: Probe Timing for Slow AI Model
# ============================================================

print("\n\n--- TODO 2 Solution: Slow Model Probe Timing ---\n")

readiness_initial_delay = 10    # Start checking early, let K8s detect when ready
readiness_period = 5            # Check frequently during startup
readiness_failure_threshold = 12  # Tolerate 12 failures × 5s = 60s startup

liveness_initial_delay = 120    # Model needs 60-90s, add buffer → 120s
liveness_period = 20            # Check every 20s once alive
liveness_failure_threshold = 3  # 3 failures × 20s = 60s before restart

timing_checks = [
    ("Readiness initialDelay >= 10 (give model time to start)",
     readiness_initial_delay >= 10),
    ("Readiness period 5-15s (check frequently during startup)",
     5 <= readiness_period <= 15),
    ("Readiness failureThreshold >= 3 (tolerate slow startup)",
     readiness_failure_threshold >= 3),
    ("Liveness initialDelay >= 90 (model needs 60-90s!)",
     liveness_initial_delay >= 90),
    ("Liveness period 15-30s (don't restart too aggressively)",
     15 <= liveness_period <= 30),
    ("Liveness failureThreshold >= 3 (give recovery time)",
     liveness_failure_threshold >= 3),
]

passed = sum(1 for _, ok in timing_checks if ok)
print(f"  Timing validation ({passed}/{len(timing_checks)}):")
for name, ok in timing_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print(f"\n  Values:")
print(f"    Readiness: initialDelay={readiness_initial_delay}s, "
      f"period={readiness_period}s, failures={readiness_failure_threshold}")
print(f"    Liveness:  initialDelay={liveness_initial_delay}s, "
      f"period={liveness_period}s, failures={liveness_failure_threshold}")

print(f"\n  Why initialDelay=120 for liveness?")
print(f"    Model loads in 60-90s. If liveness starts at 30s:")
print(f"      t=30s: probe fails (model loading)")
print(f"      t=50s: probe fails")
print(f"      t=70s: probe fails → K8s RESTARTS the pod!")
print(f"      The model never finishes loading → infinite restart loop!")
print(f"    With initialDelay=120s:")
print(f"      t=0-120s: no liveness checks (model loads safely)")
print(f"      t=120s+: liveness checks begin (model is ready)")

# Generate the YAML with these timings
timing_yaml = textwrap.dedent(f"""\
    # Probe configuration for AI agent with 60-90s model loading
    readinessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: {readiness_initial_delay}
      periodSeconds: {readiness_period}
      failureThreshold: {readiness_failure_threshold}
      timeoutSeconds: 5

    livenessProbe:
      httpGet:
        path: /health
        port: 8000
      initialDelaySeconds: {liveness_initial_delay}
      periodSeconds: {liveness_period}
      failureThreshold: {liveness_failure_threshold}
      timeoutSeconds: 5
""")

with open(os.path.join(WORKDIR, "probe-timing.yaml"), "w") as f:
    f.write(timing_yaml)

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 07 Solution complete!")
print("- TODO 1: Redis probes (tcpSocket liveness + exec readiness)")
print(f"- TODO 2: AI model timing (liveness initialDelay=120s, readiness period=5s)")
