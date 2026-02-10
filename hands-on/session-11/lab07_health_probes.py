"""
Lab 07: Health Probes
======================
Configure readiness and liveness probes for AI workloads on Kubernetes.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-07"

print("=" * 50)
print("  Lab 07: Health Probes")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Why probes? The AI model loading problem
# ============================================================

print("\n--- Step 1: The Model Loading Problem ---\n")

class AIAgentPod:
    """Simulates an AI agent pod with model loading time."""
    def __init__(self, name, model_load_seconds=30):
        self.name = name
        self.model_load_seconds = model_load_seconds
        self.elapsed_seconds = 0
        self.is_alive = True
        self.model_loaded = False

    def tick(self, seconds=5):
        self.elapsed_seconds += seconds
        if self.elapsed_seconds >= self.model_load_seconds:
            self.model_loaded = True

    @property
    def ready_for_traffic(self):
        return self.model_loaded and self.is_alive

    def handle_request(self):
        if not self.model_loaded:
            return 503, "Service Unavailable: model still loading"
        if not self.is_alive:
            return 500, "Internal Server Error: process stuck"
        return 200, "OK: processed request"


print("  Scenario: AI agent takes 30 seconds to load embeddings.\n")

# Without readiness probe
pod_no_probe = AIAgentPod("agent-no-probe", model_load_seconds=30)
print("  WITHOUT readiness probe (K8s sends traffic immediately):")
for sec in range(0, 40, 5):
    pod_no_probe.tick(5 if sec > 0 else 0)
    status_code, message = pod_no_probe.handle_request()
    ready = "READY" if pod_no_probe.ready_for_traffic else "NOT READY"
    indicator = "  ✓" if status_code == 200 else "  ✗"
    print(f"    t={sec:>2}s: [{ready:>9}] Request → {status_code} {message}{indicator}")

print()

# With readiness probe
pod_with_probe = AIAgentPod("agent-with-probe", model_load_seconds=30)
print("  WITH readiness probe (K8s waits until ready):")
for sec in range(0, 40, 5):
    pod_with_probe.tick(5 if sec > 0 else 0)
    if pod_with_probe.ready_for_traffic:
        status_code, message = pod_with_probe.handle_request()
        print(f"    t={sec:>2}s: [    READY] Traffic routed → {status_code} {message}  ✓")
    else:
        print(f"    t={sec:>2}s: [NOT READY] K8s holds traffic — no requests sent")


# ============================================================
# Step 2: Liveness vs Readiness
# ============================================================

print("\n\n--- Step 2: Liveness vs Readiness Probes ---\n")

probes = [
    {
        "type": "Readiness Probe",
        "question": "Is this pod READY for traffic?",
        "failure_action": "Remove from Service endpoints (no traffic)",
        "use_case": "Model loading, cache warming, dependency checks",
        "restore": "Pod is added back when probe passes again",
    },
    {
        "type": "Liveness Probe",
        "question": "Is this pod ALIVE?",
        "failure_action": "RESTART the container",
        "use_case": "Deadlocks, stuck LLM calls, infinite loops",
        "restore": "New container starts fresh",
    },
]

for probe in probes:
    print(f"  {probe['type']}")
    print(f"    Question:     {probe['question']}")
    print(f"    On failure:   {probe['failure_action']}")
    print(f"    Use case:     {probe['use_case']}")
    print(f"    Recovery:     {probe['restore']}")
    print()


# ============================================================
# Step 3: Probe types
# ============================================================

print("\n--- Step 3: Probe Types ---\n")

probe_types = [
    {
        "type": "httpGet",
        "desc": "HTTP GET to a path — 200-399 = success",
        "example": "httpGet:\n  path: /health\n  port: 8000",
        "best_for": "Web apps, APIs (most common for AI agents)",
    },
    {
        "type": "tcpSocket",
        "desc": "TCP connection attempt — success if port is open",
        "example": "tcpSocket:\n  port: 6379",
        "best_for": "Databases, Redis, services without HTTP",
    },
    {
        "type": "exec",
        "desc": "Run a command — exit code 0 = success",
        "example": "exec:\n  command:\n  - cat\n  - /tmp/healthy",
        "best_for": "Custom health checks, file-based signals",
    },
]

for pt in probe_types:
    print(f"  {pt['type']}")
    print(f"    How:      {pt['desc']}")
    print(f"    Best for: {pt['best_for']}")
    print(f"    Example:  {pt['example'].split(chr(10))[0]}...")
    print()


# ============================================================
# Step 4: Probe parameters
# ============================================================

print("\n--- Step 4: Probe Parameters ---\n")

params = [
    ("initialDelaySeconds", "10", "Wait before first probe (model loading time)"),
    ("periodSeconds", "15", "How often to probe (check interval)"),
    ("timeoutSeconds", "5", "Max wait for probe response"),
    ("failureThreshold", "3", "Consecutive failures before action"),
    ("successThreshold", "1", "Consecutive successes to be ready"),
]

for name, default, desc in params:
    print(f"  {name:<24} (e.g., {default:>3}) — {desc}")

print()
print("  For AI agents:")
print("    - initialDelaySeconds should be >= model load time")
print("    - timeoutSeconds should handle slow /health checks")
print("    - failureThreshold=3 gives transient errors time to clear")


# ============================================================
# Step 5: Complete probe YAML
# ============================================================

print("\n\n--- Step 5: Complete Probe Configuration ---\n")

probe_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: unigps-agent
    spec:
      replicas: 3
      selector:
        matchLabels:
          app: agent
      template:
        metadata:
          labels:
            app: agent
        spec:
          containers:
          - name: agent
            image: unigps-agent:2.0
            ports:
            - containerPort: 8000
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "1000m"

            # Liveness: Is the process alive?
            livenessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 15
              periodSeconds: 20
              timeoutSeconds: 5
              failureThreshold: 3

            # Readiness: Is it ready for traffic?
            readinessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 5
              periodSeconds: 10
              timeoutSeconds: 3
              failureThreshold: 3
              successThreshold: 1
""")

with open(os.path.join(WORKDIR, "deployment-probes.yaml"), "w") as f:
    f.write(probe_yaml)

print("  Generated: deployment-probes.yaml")
print()
print("  Liveness probe:")
print("    - Checks /health every 20s (after initial 15s delay)")
print("    - 3 failures → restart container")
print("    - Catches: deadlocks, stuck LLM calls")
print()
print("  Readiness probe:")
print("    - Checks /health every 10s (after initial 5s delay)")
print("    - 3 failures → remove from Service (no traffic)")
print("    - Catches: model loading, dependency startup")


# ============================================================
# Step 6: Liveness failure simulation
# ============================================================

print("\n\n--- Step 6: Liveness Failure Simulation ---\n")

class ProbeSimulator:
    """Simulates K8s probe behavior."""
    def __init__(self, pod_name, initial_delay, period, failure_threshold):
        self.pod_name = pod_name
        self.initial_delay = initial_delay
        self.period = period
        self.failure_threshold = failure_threshold
        self.consecutive_failures = 0
        self.restarts = 0

    def check(self, elapsed_seconds, probe_succeeds):
        if elapsed_seconds < self.initial_delay:
            return f"t={elapsed_seconds:>3}s: Waiting (initialDelaySeconds={self.initial_delay})"

        if probe_succeeds:
            self.consecutive_failures = 0
            return f"t={elapsed_seconds:>3}s: Probe OK ✓"
        else:
            self.consecutive_failures += 1
            if self.consecutive_failures >= self.failure_threshold:
                self.restarts += 1
                self.consecutive_failures = 0
                return (f"t={elapsed_seconds:>3}s: Probe FAILED "
                        f"({self.failure_threshold}/{self.failure_threshold}) "
                        f"→ RESTART #{self.restarts}")
            return (f"t={elapsed_seconds:>3}s: Probe FAILED "
                    f"({self.consecutive_failures}/{self.failure_threshold})")


print("  Scenario: Agent's LLM call hangs at t=60s\n")

sim = ProbeSimulator("agent-abc12", initial_delay=15, period=20, failure_threshold=3)

# Simulate: healthy until t=60, then stuck
events = []
for t in range(0, 160, 20):
    healthy = t < 60  # LLM call hangs at t=60
    if t < 15:
        result = sim.check(t, True)
    else:
        result = sim.check(t, healthy)
    events.append(result)

for event in events:
    print(f"    {event}")

print()
print("  Without liveness probe: pod appears 'Running' but is dead.")
print("  With liveness probe: K8s detects failure and restarts automatically.")


# ============================================================
# TODO 1: Configure probes for Redis
# ============================================================

print("\n\n--- TODO 1: Redis Health Probes ---\n")

print("  Redis doesn't have HTTP endpoints. Use a TCP socket probe.")
print("  Requirements:")
print("    - Liveness: tcpSocket on port 6379")
print("    - Readiness: exec command: redis-cli ping")
print("    - initialDelaySeconds: 5 (Redis starts fast)")
print("    - periodSeconds: 10")
print("    - failureThreshold: 3\n")

# YOUR CODE HERE: Create Redis deployment with probes
redis_probe_yaml = textwrap.dedent("""\
    # TODO: Create Redis Deployment with health probes
    # Use tcpSocket for liveness and exec for readiness
    #
    # livenessProbe:
    #   tcpSocket:
    #     port: 6379
    #   ...
    #
    # readinessProbe:
    #   exec:
    #     command:
    #     - redis-cli
    #     - ping
    #   ...

""")

with open(os.path.join(WORKDIR, "redis-deployment-probes.yaml"), "w") as f:
    f.write(redis_probe_yaml)

redis_checks = [
    ("Has livenessProbe", "livenessProbe:" in redis_probe_yaml),
    ("Has readinessProbe", "readinessProbe:" in redis_probe_yaml),
    ("Uses tcpSocket", "tcpSocket:" in redis_probe_yaml),
    ("Uses exec command", "exec:" in redis_probe_yaml or "command:" in redis_probe_yaml),
    ("Has initialDelaySeconds", "initialDelaySeconds:" in redis_probe_yaml),
    ("Has periodSeconds", "periodSeconds:" in redis_probe_yaml),
]

passed = sum(1 for _, ok in redis_checks if ok)
print(f"  Redis probe validation ({passed}/{len(redis_checks)}):")
for name, ok in redis_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Design probe timing for a slow-starting AI model
# ============================================================

print("\n\n--- TODO 2: Probe Timing for Slow AI Model ---\n")

print("  Your AI agent loads a large embedding model at startup.")
print("  It takes 60-90 seconds before /health returns 200.")
print()
print("  Design probe parameters to handle this:\n")

# YOUR CODE HERE: Set the probe timing values
readiness_initial_delay = 0   # TODO: How long to wait before first readiness check?
readiness_period = 0          # TODO: How often to check readiness?
readiness_failure_threshold = 0  # TODO: How many failures before removing?

liveness_initial_delay = 0    # TODO: How long to wait before first liveness check?
liveness_period = 0           # TODO: How often to check liveness?
liveness_failure_threshold = 0   # TODO: How many failures before restart?

# Validation
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
    print(f"    [{'PASS' if ok else 'TODO'}] {name}")

print()
print("  Key insight for liveness: initialDelaySeconds MUST be >= startup time.")
print("  If liveness checks start before the model is loaded, K8s will")
print("  restart the pod in an infinite loop (CrashLoopBackOff)!")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 07 Summary ---\n")
print("  Key concepts:")
print("    1. Readiness probe: 'Ready for traffic?' → removes from Service if no")
print("    2. Liveness probe: 'Is it alive?' → restarts container if no")
print("    3. AI models need longer initialDelaySeconds (model loading)")
print("    4. httpGet for web apps, tcpSocket for databases, exec for custom")
print("    5. Liveness initialDelay MUST exceed startup time (avoid crash loops)")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<40} ({size} bytes)")
