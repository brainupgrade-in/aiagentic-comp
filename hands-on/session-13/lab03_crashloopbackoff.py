"""
Lab 03: CrashLoopBackOff Debugging
====================================
Deep-dive into the most common Kubernetes error and how to fix it.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-03"

print("=" * 50)
print("  Lab 03: CrashLoopBackOff Debugging")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: What is CrashLoopBackOff?
# ============================================================

print("\n--- Step 1: What is CrashLoopBackOff? ---\n")

print("  CrashLoopBackOff is K8s telling you:")
print("    'Your container keeps crashing. I'm slowing down restarts.'\n")

class BackoffSimulator:
    """Simulates the Kubernetes exponential backoff pattern."""
    def __init__(self, max_backoff=300):
        self.max_backoff = max_backoff  # cap at 5 minutes
        self.attempt = 0
        self.total_time = 0

    def next_restart(self):
        self.attempt += 1
        if self.attempt == 1:
            backoff = 0  # first crash: immediate restart
        else:
            # exponential: 10s, 20s, 40s, 80s, 160s, 300s (cap)
            backoff = min(10 * (2 ** (self.attempt - 2)), self.max_backoff)
        self.total_time += backoff
        return self.attempt, backoff, self.total_time

sim = BackoffSimulator()

print("  Backoff pattern:")
print(f"  {'Attempt':<10} {'Wait':<12} {'Total Time':<15} {'Status'}")
print(f"  {'-'*10} {'-'*12} {'-'*15} {'-'*20}")

for _ in range(8):
    attempt, backoff, total = sim.next_restart()
    status = "CrashLoopBackOff" if attempt > 1 else "Running (briefly)"
    print(f"  {attempt:<10} {backoff:>4}s{'':<7} {total:>5}s{'':<9} {status}")

print()
print("  Key insight: By attempt 6, K8s waits 5 minutes between restarts.")
print("  The pod APPEARS to be doing nothing. It's actually waiting to retry.")
print("  This is why CrashLoopBackOff feels 'stuck' — it's just backing off.")


# ============================================================
# Step 2: Common causes
# ============================================================

print("\n\n--- Step 2: Common Causes of CrashLoopBackOff ---\n")

causes = [
    {
        "cause": "Missing environment variable",
        "example": "KeyError: 'DATABASE_URL'",
        "fix": "Add ConfigMap or Secret with the missing variable",
        "frequency": "Very Common",
    },
    {
        "cause": "Wrong command or entrypoint",
        "example": "exec: 'pytohn': executable file not found (typo!)",
        "fix": "Fix the command in the Deployment YAML",
        "frequency": "Common",
    },
    {
        "cause": "Dependency not ready",
        "example": "ConnectionRefusedError: Redis at redis-svc:6379",
        "fix": "Add init container to wait for dependency, or handle retry in app",
        "frequency": "Common",
    },
    {
        "cause": "OOM (Out of Memory)",
        "example": "Container killed: OOMKilled (exit code 137)",
        "fix": "Increase memory limits in resources section",
        "frequency": "Common",
    },
    {
        "cause": "Permission denied",
        "example": "PermissionError: [Errno 13] Permission denied: '/data/models'",
        "fix": "Fix volume permissions or securityContext (runAsUser/fsGroup)",
        "frequency": "Moderate",
    },
    {
        "cause": "Config file missing or invalid",
        "example": "FileNotFoundError: /etc/config/app.yaml",
        "fix": "Mount ConfigMap as volume at the expected path",
        "frequency": "Moderate",
    },
]

for c in causes:
    print(f"  [{c['frequency']}] {c['cause']}")
    print(f"    Log example: {c['example']}")
    print(f"    Fix: {c['fix']}")
    print()

# Save causes reference
causes_ref = "# CrashLoopBackOff Common Causes\n\n"
for c in causes:
    causes_ref += f"## {c['cause']} ({c['frequency']})\n"
    causes_ref += f"- Example log: {c['example']}\n"
    causes_ref += f"- Fix: {c['fix']}\n\n"

with open(os.path.join(WORKDIR, "crashloop-causes.md"), "w") as f:
    f.write(causes_ref)

print("  Generated: crashloop-causes.md")


# ============================================================
# TODO 1: Analyze crash scenarios
# ============================================================

print("\n\n--- TODO 1: Diagnose CrashLoopBackOff Scenarios ---\n")

print("  For each scenario, analyze the logs and identify the root cause.\n")

scenarios = [
    {
        "name": "Scenario A: AI Agent Pod",
        "logs": [
            "INFO:     Starting AI Agent v2.0",
            "INFO:     Loading configuration...",
            "Traceback (most recent call last):",
            '  File "/app/main.py", line 22, in startup',
            "    client = Groq(api_key=os.environ['GROQ_API_KEY'])",
            "KeyError: 'GROQ_API_KEY'",
        ],
        "answer": "_______________",
        # Answer: Missing environment variable GROQ_API_KEY
    },
    {
        "name": "Scenario B: Redis Pod",
        "logs": [
            "oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo",
            "Fatal error: Can't open the config file '/etc/redis/redis.conf'",
            "No such file or directory",
        ],
        "answer": "_______________",
        # Answer: Config file missing — ConfigMap not mounted at /etc/redis/redis.conf
    },
    {
        "name": "Scenario C: Web API Pod",
        "logs": [
            "exec /usr/local/bin/pytohn: no such file or directory",
        ],
        "answer": "_______________",
        # Answer: Wrong command/entrypoint — typo 'pytohn' instead of 'python'
    },
    {
        "name": "Scenario D: ML Model Pod",
        "logs": [
            "INFO: Loading embedding model (768 dimensions)...",
            "INFO: Model requires 2.1 GB memory",
            "INFO: Allocating tensors...",
            "Killed",
        ],
        "answer": "_______________",
        # Answer: OOMKilled — memory limit too low for model that needs 2.1 GB
    },
]

# YOUR CODE HERE: For each scenario, analyze the logs and write the root cause
# scenarios[0]["answer"] = "Missing environment variable GROQ_API_KEY"
# scenarios[1]["answer"] = ???
# scenarios[2]["answer"] = ???
# scenarios[3]["answer"] = ???

score = 0
for scenario in scenarios:
    print(f"  {scenario['name']}")
    print(f"  Logs:")
    for log_line in scenario["logs"]:
        print(f"    | {log_line}")
    is_filled = scenario["answer"] != "_______________"
    if is_filled:
        score += 1
    status = "PASS" if is_filled else "FAIL"
    print(f"  [{status}] Your diagnosis: {scenario['answer']}")
    print()

print(f"  Diagnosed: {score}/{len(scenarios)} scenarios")


# ============================================================
# TODO 2: Write fix manifests
# ============================================================

print("\n\n--- TODO 2: Fix a Broken Deployment ---\n")

print("  The following Deployment keeps CrashLoopBackOff-ing.")
print("  It has THREE problems. Fix all of them.\n")

broken_yaml = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ai-agent
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
            image: ai-agent:latest
            command: ["pytohn", "main.py"]
            ports:
            - containerPort: 8000
            resources:
              requests:
                memory: "64Mi"
                cpu: "100m"
              limits:
                memory: "128Mi"
                cpu: "500m"
""")

print("  Broken Deployment (3 problems):")
for i, line in enumerate(broken_yaml.strip().split("\n"), 1):
    print(f"    {i:>2}: {line}")

print()
print("  Problems to fix:")
print("    1. Wrong command: 'pytohn' should be 'python'")
print("    2. Image tag 'latest' is risky — use a specific version like 'ai-agent:2.0'")
print("    3. Memory limit 128Mi is too low for an AI agent — increase to 512Mi")
print()

# YOUR CODE HERE: Create the FIXED Deployment YAML
fixed_yaml = textwrap.dedent("""\
    # TODO: Fix the broken Deployment above
    # Fix 1: Change 'pytohn' to 'python' in command
    # Fix 2: Change image from 'ai-agent:latest' to 'ai-agent:2.0'
    # Fix 3: Increase memory limit from 128Mi to 512Mi
    # Also add the missing GROQ_API_KEY env var from a Secret

""")

with open(os.path.join(WORKDIR, "fixed-deployment.yaml"), "w") as f:
    f.write(fixed_yaml)

# Validate fixes
fix_checks = [
    ("Command fixed: 'python' not 'pytohn'",
     "python" in fixed_yaml and "pytohn" not in fixed_yaml),
    ("Image has specific version (not :latest)",
     "image:" in fixed_yaml and ":latest" not in fixed_yaml and ":" in fixed_yaml.split("image:")[-1].split("\n")[0]),
    ("Memory limit increased (512Mi or more)",
     "512Mi" in fixed_yaml or "1Gi" in fixed_yaml or "1024Mi" in fixed_yaml),
    ("Has GROQ_API_KEY env var",
     "GROQ_API_KEY" in fixed_yaml),
    ("Has apiVersion: apps/v1",
     "apiVersion: apps/v1" in fixed_yaml),
    ("Has kind: Deployment",
     "kind: Deployment" in fixed_yaml),
]

passed = sum(1 for _, ok in fix_checks if ok)
print(f"  Fixed Deployment validation ({passed}/{len(fix_checks)}):")
for name, ok in fix_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 03 Summary ---\n")
print("  Key concepts:")
print("    1. CrashLoopBackOff = container crashes + exponential backoff (10s..5min)")
print("    2. Always check: kubectl logs POD --previous (see the crash reason)")
print("    3. Top causes: missing env vars, wrong command, OOM, missing configs")
print("    4. Fix the root cause, not the symptom (don't just increase restarts)")
print("    5. Use specific image tags, not :latest (reproducibility)")
print(f"\n  TODO 1: {score}/{len(scenarios)} crash scenarios diagnosed")
print(f"  TODO 2: {passed}/{len(fix_checks)} fixes validated")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<40} ({size} bytes)")
