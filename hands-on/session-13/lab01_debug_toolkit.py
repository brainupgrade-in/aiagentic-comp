"""
Lab 01: Debug Toolkit
======================
Master the kubectl debug toolkit — the commands you need when things go wrong.

No Kubernetes cluster required — this lab teaches debugging workflows via Python.
"""

import os
import shutil
WORKDIR = "/tmp/k8s-lab-13-01"

print("=" * 50)
print("  Lab 01: Debug Toolkit")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Debug toolkit reference
# ============================================================

print("\n--- Step 1: kubectl Debug Commands Reference ---\n")

debug_commands = [
    ("kubectl get pods",
     "List pods — see status (Running, Pending, CrashLoopBackOff)",
     "First thing to run: what's happening?"),
    ("kubectl get pods -o wide",
     "List pods with node name and IP",
     "See which node each pod is on"),
    ("kubectl describe pod POD",
     "Detailed pod info + events timeline",
     "Shows WHY a pod is stuck (events section at bottom)"),
    ("kubectl logs POD",
     "View container stdout/stderr",
     "See application errors and stack traces"),
    ("kubectl logs POD --previous",
     "View logs from PREVIOUS crashed container",
     "Critical for CrashLoopBackOff — see what happened before crash"),
    ("kubectl logs POD -c CONTAINER",
     "View logs from a specific container (multi-container pod)",
     "Init containers, sidecars each have their own logs"),
    ("kubectl exec -it POD -- bash",
     "Open a shell inside a running container",
     "Check files, test connectivity, inspect environment"),
    ("kubectl exec POD -- env",
     "Print environment variables inside the container",
     "Verify ConfigMap/Secret injection"),
    ("kubectl top pods",
     "Show CPU/memory usage per pod (requires metrics-server)",
     "Find pods using too much memory or CPU"),
    ("kubectl top nodes",
     "Show CPU/memory usage per node",
     "Find overloaded nodes"),
    ("kubectl get events --sort-by=.lastTimestamp",
     "Show cluster events sorted by time",
     "See scheduling failures, image pull errors, OOM kills"),
    ("kubectl describe node NODE",
     "Detailed node info — capacity, allocatable, conditions",
     "Check if node has resources, taints, or disk pressure"),
]

for cmd, desc, tip in debug_commands:
    print(f"  {cmd}")
    print(f"    What: {desc}")
    print(f"    When: {tip}")
    print()

# Save reference as a cheat sheet
cheatsheet = "# kubectl Debug Cheat Sheet\n\n"
for cmd, desc, tip in debug_commands:
    cheatsheet += f"## {cmd}\n- {desc}\n- When: {tip}\n\n"

with open(os.path.join(WORKDIR, "debug-cheatsheet.md"), "w") as f:
    f.write(cheatsheet)

print("  Generated: debug-cheatsheet.md")


# ============================================================
# Step 2: Debug workflow simulation
# ============================================================

print("\n\n--- Step 2: Debug Workflow — The Investigation Flow ---\n")

class DebugWorkflow:
    """Simulates the standard Kubernetes debug flow."""
    def __init__(self, pod_name, status, events, logs, env_vars):
        self.pod_name = pod_name
        self.status = status
        self.events = events
        self.logs = logs
        self.env_vars = env_vars

    def step_get(self):
        """Step 1: kubectl get pods"""
        return f"NAME            STATUS              RESTARTS   AGE\n{self.pod_name}   {self.status}   3          5m"

    def step_describe(self):
        """Step 2: kubectl describe pod"""
        header = f"Name: {self.pod_name}\nStatus: {self.status}\n\nEvents:"
        event_lines = "\n".join(f"  {e}" for e in self.events)
        return f"{header}\n{event_lines}"

    def step_logs(self):
        """Step 3: kubectl logs"""
        return "\n".join(self.logs)

    def step_exec(self):
        """Step 4: kubectl exec -- env"""
        return "\n".join(f"{k}={v}" for k, v in self.env_vars.items())


# Example: CrashLoopBackOff scenario
crash_scenario = DebugWorkflow(
    pod_name="agent-7f8b9c-x2k4l",
    status="CrashLoopBackOff",
    events=[
        "Normal   Scheduled  Successfully assigned to node-1",
        "Normal   Pulled     Container image pulled successfully",
        "Normal   Created    Created container agent",
        "Warning  BackOff    Back-off restarting failed container",
    ],
    logs=[
        "Traceback (most recent call last):",
        '  File "/app/main.py", line 15, in <module>',
        "    api_key = os.environ['GROQ_API_KEY']",
        "KeyError: 'GROQ_API_KEY'",
    ],
    env_vars={
        "REDIS_URL": "redis://redis-svc:6379",
        "LOG_LEVEL": "info",
        "GROQ_API_KEY": "<not set>",
    }
)

print("  Workflow: get --> describe --> logs --> exec\n")

print("  Step 1: kubectl get pods")
print("  " + "-" * 40)
for line in crash_scenario.step_get().split("\n"):
    print(f"    {line}")

print("\n  Step 2: kubectl describe pod agent-7f8b9c-x2k4l")
print("  " + "-" * 40)
for line in crash_scenario.step_describe().split("\n"):
    print(f"    {line}")

print("\n  Step 3: kubectl logs agent-7f8b9c-x2k4l --previous")
print("  " + "-" * 40)
for line in crash_scenario.step_logs().split("\n"):
    print(f"    {line}")

print("\n  Step 4: kubectl exec agent-7f8b9c-x2k4l -- env")
print("  " + "-" * 40)
for line in crash_scenario.step_exec().split("\n"):
    print(f"    {line}")

print("\n  Diagnosis: Missing GROQ_API_KEY environment variable.")
print("  Fix: Add the Secret/ConfigMap that provides GROQ_API_KEY.")


# ============================================================
# TODO 1: Map symptoms to kubectl commands
# ============================================================

print("\n\n--- TODO 1: Symptom-to-Command Mapping ---\n")

print("  When you see a symptom, which kubectl command do you run FIRST?\n")

symptom_mappings = {
    "Pod keeps restarting (CrashLoopBackOff)": "_______________",
    # Answer: kubectl logs POD --previous
    "Pod stuck in Pending state": "_______________",
    # Answer: kubectl describe pod POD
    "Pod running but returning 500 errors": "_______________",
    # Answer: kubectl logs POD
    "Pod killed with OOMKilled": "_______________",
    # Answer: kubectl top pods
    "Cannot pull container image": "_______________",
    # Answer: kubectl describe pod POD
    "Service not routing traffic to pods": "_______________",
    # Answer: kubectl get endpoints SERVICE
}

# YOUR CODE HERE: Replace the blank values with the correct kubectl commands
# Hints:
#   - CrashLoopBackOff: need to see WHY it crashed (previous logs)
#   - Pending: need to see events (scheduling failure)
#   - 500 errors: need to see current application logs
#   - OOMKilled: need to see memory usage
#   - Image pull: need to see events (image name, registry auth)
#   - Service routing: need to check if endpoints exist

# symptom_mappings["Pod keeps restarting (CrashLoopBackOff)"] = ???
# symptom_mappings["Pod stuck in Pending state"] = ???
# symptom_mappings["Pod running but returning 500 errors"] = ???
# symptom_mappings["Pod killed with OOMKilled"] = ???
# symptom_mappings["Cannot pull container image"] = ???
# symptom_mappings["Service not routing traffic to pods"] = ???


# Validate
print("  Your mappings:")
filled = 0
for symptom, command in symptom_mappings.items():
    is_filled = command != "_______________"
    if is_filled:
        filled += 1
    status = "PASS" if is_filled else "FAIL"
    print(f"    [{status}] {symptom}")
    print(f"           -> {command}")

print(f"\n  Completed: {filled}/{len(symptom_mappings)} mappings")


# ============================================================
# TODO 2: Debug workflow quiz
# ============================================================

print("\n\n--- TODO 2: Debug Workflow Quiz ---\n")

print("  For each scenario, name the kubectl command sequence to diagnose it.\n")

quiz = [
    {
        "scenario": "Pod is in CrashLoopBackOff — what command shows WHY it crashed?",
        "answer": "___",
        "correct": "kubectl logs POD --previous",
    },
    {
        "scenario": "Pod stuck in Pending — what command shows scheduling events?",
        "answer": "___",
        "correct": "kubectl describe pod POD",
    },
    {
        "scenario": "Pod was OOMKilled — what command checks current memory usage?",
        "answer": "___",
        "correct": "kubectl top pods",
    },
    {
        "scenario": "You suspect a wrong environment variable — what command checks it?",
        "answer": "___",
        "correct": "kubectl exec POD -- env",
    },
    {
        "scenario": "Multiple pods failing across the cluster — what shows recent events?",
        "answer": "___",
        "correct": "kubectl get events --sort-by=.lastTimestamp",
    },
    {
        "scenario": "Node seems overloaded — what command shows node resource usage?",
        "answer": "___",
        "correct": "kubectl top nodes",
    },
]

# YOUR CODE HERE: Fill in the answer field for each quiz question
# quiz[0]["answer"] = "kubectl logs POD --previous"
# quiz[1]["answer"] = ???
# ... etc

score = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].strip().lower() == q["correct"].strip().lower()
    if is_correct:
        score += 1
    status = "PASS" if is_correct else "FAIL"
    print(f"    [{status}] Q{i}: {q['scenario']}")
    if is_correct:
        print(f"           Your answer: {q['answer']}")
    else:
        print(f"           Your answer: {q['answer']}  (fill in the kubectl command)")

print(f"\n  Score: {score}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 01 Summary ---\n")
print("  Key concepts:")
print("    1. Debug flow: get -> describe -> logs -> exec")
print("    2. kubectl logs --previous shows WHY a crashed container failed")
print("    3. kubectl describe shows events (scheduling, image pull, OOM)")
print("    4. kubectl top shows real-time resource usage")
print("    5. kubectl get events shows cluster-wide issues")
print(f"\n  TODO 1: {filled}/{len(symptom_mappings)} symptom mappings completed")
print(f"  TODO 2: {score}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<40} ({size} bytes)")
