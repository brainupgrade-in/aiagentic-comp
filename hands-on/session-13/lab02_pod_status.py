"""
Lab 02: Pod Status Diagnosis
==============================
Understand every pod status and what it means for debugging.

No Kubernetes cluster required — this lab teaches pod lifecycle via Python.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-02"

print("=" * 50)
print("  Lab 02: Pod Status Diagnosis")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Pod status reference table
# ============================================================

print("\n--- Step 1: Pod Status Reference ---\n")

statuses = [
    {
        "status": "Running",
        "meaning": "All containers started and at least one is running",
        "action": "Normal — no action needed unless app misbehaving",
        "severity": "OK",
    },
    {
        "status": "Pending",
        "meaning": "Pod accepted but not yet scheduled or pulling images",
        "action": "Check: insufficient resources, node selectors, PVC not bound",
        "severity": "WARNING",
    },
    {
        "status": "CrashLoopBackOff",
        "meaning": "Container keeps crashing, K8s backs off restart attempts",
        "action": "Check: kubectl logs --previous, fix app error or config",
        "severity": "ERROR",
    },
    {
        "status": "ImagePullBackOff",
        "meaning": "Cannot pull container image from registry",
        "action": "Check: image name/tag, registry auth, network connectivity",
        "severity": "ERROR",
    },
    {
        "status": "OOMKilled",
        "meaning": "Container exceeded memory limit and was killed by kernel",
        "action": "Increase memory limits or fix memory leak in application",
        "severity": "ERROR",
    },
    {
        "status": "Init:0/1",
        "meaning": "Init container has not completed yet",
        "action": "Check init container logs: kubectl logs POD -c init-container-name",
        "severity": "WARNING",
    },
    {
        "status": "Terminating",
        "meaning": "Pod is shutting down (graceful termination period)",
        "action": "Normal during deploys; stuck = check finalizers or preStop hooks",
        "severity": "INFO",
    },
    {
        "status": "Evicted",
        "meaning": "Node under resource pressure, pod removed",
        "action": "Check node disk/memory pressure: kubectl describe node",
        "severity": "WARNING",
    },
]

print(f"  {'Status':<22} {'Severity':<10} {'Meaning'}")
print(f"  {'-'*22} {'-'*10} {'-'*50}")
for s in statuses:
    print(f"  {s['status']:<22} {s['severity']:<10} {s['meaning']}")

print()
for s in statuses:
    if s["severity"] in ("ERROR", "WARNING"):
        print(f"  {s['status']}: {s['action']}")


# ============================================================
# Step 2: Pod status simulation
# ============================================================

print("\n\n--- Step 2: Pod Status Simulation ---\n")

class PodStatus:
    """Simulates pod lifecycle and status transitions."""
    def __init__(self, name, image, memory_limit_mi=512, has_node_resources=True,
                 image_exists=True, app_starts_ok=True, has_init_container=False,
                 init_succeeds=True, memory_usage_mi=256):
        self.name = name
        self.image = image
        self.memory_limit_mi = memory_limit_mi
        self.has_node_resources = has_node_resources
        self.image_exists = image_exists
        self.app_starts_ok = app_starts_ok
        self.has_init_container = has_init_container
        self.init_succeeds = init_succeeds
        self.memory_usage_mi = memory_usage_mi
        self.restart_count = 0

    def simulate(self):
        """Walk through pod lifecycle and return final status."""
        phases = []

        # Phase 1: Scheduling
        if not self.has_node_resources:
            phases.append(("Scheduling", "FAIL", "No node has sufficient resources"))
            return "Pending", phases

        phases.append(("Scheduling", "OK", f"Assigned to node-1"))

        # Phase 2: Image pull
        if not self.image_exists:
            phases.append(("Image Pull", "FAIL", f"Failed to pull image: {self.image}"))
            return "ImagePullBackOff", phases

        phases.append(("Image Pull", "OK", f"Pulled {self.image}"))

        # Phase 3: Init containers
        if self.has_init_container:
            if not self.init_succeeds:
                phases.append(("Init Container", "FAIL", "Init container exited with error"))
                return "Init:0/1", phases
            phases.append(("Init Container", "OK", "Init container completed"))

        # Phase 4: Container start
        if not self.app_starts_ok:
            phases.append(("Container Start", "FAIL", "Application crashed on startup"))
            self.restart_count += 1
            return "CrashLoopBackOff", phases

        phases.append(("Container Start", "OK", "Container started"))

        # Phase 5: Runtime
        if self.memory_usage_mi > self.memory_limit_mi:
            phases.append(("Runtime", "FAIL",
                          f"Memory usage {self.memory_usage_mi}Mi > limit {self.memory_limit_mi}Mi"))
            return "OOMKilled", phases

        phases.append(("Runtime", "OK", "Container running normally"))
        return "Running", phases


# Simulate different scenarios
scenarios = [
    PodStatus("agent-ok", "agent:2.0"),
    PodStatus("agent-pending", "agent:2.0", has_node_resources=False),
    PodStatus("agent-imgpull", "agent:9.9.9", image_exists=False),
    PodStatus("agent-crash", "agent:2.0", app_starts_ok=False),
    PodStatus("agent-oom", "agent:2.0", memory_limit_mi=128, memory_usage_mi=256),
    PodStatus("agent-init", "agent:2.0", has_init_container=True, init_succeeds=False),
]

for pod in scenarios:
    status, phases = pod.simulate()
    print(f"  Pod: {pod.name} -> Status: {status}")
    for phase_name, result, detail in phases:
        indicator = "OK" if result == "OK" else "!!"
        print(f"    [{indicator}] {phase_name}: {detail}")
    print()


# ============================================================
# TODO 1: Match pod statuses to causes
# ============================================================

print("\n--- TODO 1: Match Pod Statuses to Root Causes ---\n")

print("  For each status, identify the most likely root cause.\n")

status_cause_map = {
    "CrashLoopBackOff": "_______________",
    # Answer: Application error (missing env var, wrong command, unhandled exception)
    "Pending": "_______________",
    # Answer: Insufficient cluster resources (CPU/memory) or PVC not bound
    "ImagePullBackOff": "_______________",
    # Answer: Wrong image name/tag or missing registry credentials
    "OOMKilled": "_______________",
    # Answer: Container exceeded memory limit (memory leak or limit too low)
    "Init:0/1": "_______________",
    # Answer: Init container failed (dependency not ready, wrong command)
    "Evicted": "_______________",
    # Answer: Node under resource pressure (disk or memory)
}

# YOUR CODE HERE: Replace blank values with the root cause
# Hints:
#   CrashLoopBackOff -> something about application errors
#   Pending -> something about cluster resources
#   ImagePullBackOff -> something about wrong image name
#   OOMKilled -> something about memory
#   Init:0/1 -> something about init container
#   Evicted -> something about node pressure

# status_cause_map["CrashLoopBackOff"] = ???
# status_cause_map["Pending"] = ???
# status_cause_map["ImagePullBackOff"] = ???
# status_cause_map["OOMKilled"] = ???
# status_cause_map["Init:0/1"] = ???
# status_cause_map["Evicted"] = ???


# Validate
print("  Your mappings:")
filled = 0
for status, cause in status_cause_map.items():
    is_filled = cause != "_______________"
    if is_filled:
        filled += 1
    check = "PASS" if is_filled else "FAIL"
    print(f"    [{check}] {status:<22} -> {cause}")

print(f"\n  Completed: {filled}/{len(status_cause_map)} mappings")


# ============================================================
# TODO 2: Match pod statuses to fix commands
# ============================================================

print("\n\n--- TODO 2: Match Pod Statuses to Fix Commands ---\n")

print("  For each status, what kubectl command helps you fix it?\n")

status_fix_map = {
    "CrashLoopBackOff": "_______________",
    # Answer: kubectl logs POD --previous
    "Pending": "_______________",
    # Answer: kubectl describe pod POD (check Events section)
    "ImagePullBackOff": "_______________",
    # Answer: kubectl describe pod POD (check image name in Events)
    "OOMKilled": "_______________",
    # Answer: kubectl top pods (check actual memory usage)
    "Init:0/1": "_______________",
    # Answer: kubectl logs POD -c init-container-name
    "Evicted": "_______________",
    # Answer: kubectl describe node NODE (check Conditions)
}

# YOUR CODE HERE: Replace blank values with the kubectl command to diagnose/fix
# status_fix_map["CrashLoopBackOff"] = ???
# status_fix_map["Pending"] = ???
# status_fix_map["ImagePullBackOff"] = ???
# status_fix_map["OOMKilled"] = ???
# status_fix_map["Init:0/1"] = ???
# status_fix_map["Evicted"] = ???


# Validate
print("  Your mappings:")
filled_fix = 0
for status, fix in status_fix_map.items():
    is_filled = fix != "_______________"
    if is_filled:
        filled_fix += 1
    check = "PASS" if is_filled else "FAIL"
    print(f"    [{check}] {status:<22} -> {fix}")

print(f"\n  Completed: {filled_fix}/{len(status_fix_map)} mappings")

# Save reference file
reference = textwrap.dedent("""\
    # Pod Status Quick Reference
    #
    # Status             | First Command                | What to Look For
    # -------------------|------------------------------|------------------
    # CrashLoopBackOff   | kubectl logs POD --previous  | App errors, missing env vars
    # Pending            | kubectl describe pod POD     | Events: scheduling failures
    # ImagePullBackOff   | kubectl describe pod POD     | Events: image name, auth
    # OOMKilled          | kubectl top pods             | Memory usage vs limits
    # Init:0/1           | kubectl logs POD -c INIT     | Init container errors
    # Evicted            | kubectl describe node NODE   | Conditions: disk/mem pressure
""")

with open(os.path.join(WORKDIR, "pod-status-reference.txt"), "w") as f:
    f.write(reference)

print("\n  Generated: pod-status-reference.txt")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 02 Summary ---\n")
print("  Key concepts:")
print("    1. Pod status tells you WHERE in the lifecycle the problem is")
print("    2. CrashLoopBackOff = app crash; check logs --previous")
print("    3. Pending = scheduling problem; check describe events")
print("    4. ImagePullBackOff = wrong image or auth; check describe events")
print("    5. OOMKilled = memory exceeded; increase limits or fix leak")
print("    6. Init:0/1 = init container stuck; check init container logs")
print(f"\n  TODO 1: {filled}/{len(status_cause_map)} status-to-cause mappings completed")
print(f"  TODO 2: {filled_fix}/{len(status_fix_map)} status-to-fix mappings completed")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<40} ({size} bytes)")
