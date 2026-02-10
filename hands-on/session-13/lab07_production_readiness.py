"""
Lab 07: Production Readiness Checklist
=========================================
Evaluate Kubernetes deployments against production best practices.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-13-07"

print("=" * 50)
print("  Lab 07: Production Readiness Checklist")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Production readiness checklist categories
# ============================================================

print("\n--- Step 1: Production Readiness Categories ---\n")

categories = {
    "Reliability": [
        "Health probes (liveness + readiness) configured",
        "Resource requests AND limits set",
        "PodDisruptionBudget defined",
        "Multiple replicas (>= 2 for stateless services)",
        "Rolling update strategy with maxSurge/maxUnavailable",
        "Graceful shutdown handling (preStop hook or SIGTERM handling)",
    ],
    "Scalability": [
        "HPA configured with appropriate metrics",
        "Resource requests set (HPA needs these for calculations)",
        "minReplicas >= 2 in HPA",
        "Stabilization windows to prevent flapping",
        "Stateless design (no local state — use Redis/DB)",
    ],
    "Observability": [
        "Application logs to stdout/stderr (not to files)",
        "Structured logging (JSON format)",
        "Health endpoint (/health or /healthz)",
        "Metrics endpoint (/metrics for Prometheus)",
        "Labels for identification (app, version, component, team)",
    ],
    "Security": [
        "Non-root container (runAsNonRoot: true)",
        "Read-only root filesystem where possible",
        "Secrets in K8s Secrets (not in env vars in YAML)",
        "Image from trusted registry with specific tag (not :latest)",
        "SecurityContext with minimal capabilities",
        "Network policies to restrict traffic",
    ],
}

for category, items in categories.items():
    print(f"  {category}:")
    for item in items:
        print(f"    [ ] {item}")
    print()


# ============================================================
# Step 2: Common production failures and prevention
# ============================================================

print("\n--- Step 2: Common Production Failures ---\n")

failures = [
    {
        "failure": "Deploy kills all pods at once during upgrade",
        "cause": "No rolling update strategy or PDB",
        "prevention": "Set strategy: RollingUpdate with maxUnavailable: 0 and PDB",
        "category": "Reliability",
    },
    {
        "failure": "Pods OOMKilled under load",
        "cause": "Memory limits too low or no limits set",
        "prevention": "Set memory limits based on load testing, monitor with kubectl top",
        "category": "Reliability",
    },
    {
        "failure": "Traffic sent to pods still starting up",
        "cause": "No readiness probe configured",
        "prevention": "Add readiness probe that checks /health (returns 200 only when ready)",
        "category": "Reliability",
    },
    {
        "failure": "Stuck pods never restarted",
        "cause": "No liveness probe configured",
        "prevention": "Add liveness probe with appropriate timeout and failure threshold",
        "category": "Reliability",
    },
    {
        "failure": "HPA scales to 1 pod, then node fails = outage",
        "cause": "minReplicas: 1 in HPA",
        "prevention": "Set minReplicas >= 2 so there's always a backup",
        "category": "Scalability",
    },
    {
        "failure": "Cannot debug production issues",
        "cause": "Logs written to files inside container, no structured logging",
        "prevention": "Log to stdout/stderr in JSON format, use labels for filtering",
        "category": "Observability",
    },
    {
        "failure": "Secrets visible in git history",
        "cause": "API keys hardcoded in Deployment YAML env section",
        "prevention": "Use K8s Secrets with secretKeyRef, never commit secrets to git",
        "category": "Security",
    },
    {
        "failure": "Container runs as root, attacker gets node access",
        "cause": "No securityContext set, default is root",
        "prevention": "Set runAsNonRoot: true, runAsUser: 1000 in securityContext",
        "category": "Security",
    },
]

for f in failures:
    print(f"  [{f['category']}] {f['failure']}")
    print(f"    Cause: {f['cause']}")
    print(f"    Fix:   {f['prevention']}")
    print()


# ============================================================
# TODO 1: Production checklist — match items to categories
# ============================================================

print("\n--- TODO 1: Match Checklist Items to Categories ---\n")

print("  Categorize each item as: Reliability, Scalability, Observability, or Security\n")

checklist_items = {
    "Health probes configured": "_______________",
    # Answer: Reliability
    "HPA with minReplicas >= 2": "_______________",
    # Answer: Scalability
    "Structured JSON logging": "_______________",
    # Answer: Observability
    "Non-root container": "_______________",
    # Answer: Security
    "PodDisruptionBudget defined": "_______________",
    # Answer: Reliability
    "Prometheus /metrics endpoint": "_______________",
    # Answer: Observability
    "Secrets in K8s Secrets (not env)": "_______________",
    # Answer: Security
    "Stabilization windows on HPA": "_______________",
    # Answer: Scalability
    "Rolling update strategy": "_______________",
    # Answer: Reliability
    "Resource requests AND limits": "_______________",
    # Answer: Reliability
    "Labels for app, version, team": "_______________",
    # Answer: Observability
    "Network policies": "_______________",
    # Answer: Security
}

# YOUR CODE HERE: Fill in the category for each item
# checklist_items["Health probes configured"] = "Reliability"
# checklist_items["HPA with minReplicas >= 2"] = ???
# ... etc

valid_categories = {"Reliability", "Scalability", "Observability", "Security"}
filled = 0
for item, category in checklist_items.items():
    is_filled = category in valid_categories
    if is_filled:
        filled += 1
    status = "PASS" if is_filled else "FAIL"
    print(f"    [{status}] {item:<42} -> {category}")

print(f"\n  Categorized: {filled}/{len(checklist_items)} items")


# ============================================================
# TODO 2: Review a "bad" Deployment
# ============================================================

print("\n\n--- TODO 2: Find Production Issues in This Deployment ---\n")

print("  Review the following Deployment YAML and identify 6 production issues.\n")

bad_deployment = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ai-agent
    spec:
      replicas: 1
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
            ports:
            - containerPort: 8000
            env:
            - name: GROQ_API_KEY
              value: "gsk_production_key_abc123"
            - name: DATABASE_URL
              value: "postgres://admin:password@db:5432/app"
""")

print("  Deployment YAML to review:")
for i, line in enumerate(bad_deployment.strip().split("\n"), 1):
    print(f"    {i:>2}: {line}")

with open(os.path.join(WORKDIR, "bad-deployment.yaml"), "w") as f:
    f.write(bad_deployment)

print()
print("  Find 6 production issues:\n")

issues = {
    "Issue 1": "_______________",
    # Answer: No health probes (no liveness/readiness probes)
    "Issue 2": "_______________",
    # Answer: No resource requests/limits (can OOMKill or starve other pods)
    "Issue 3": "_______________",
    # Answer: No PDB (voluntary disruptions can kill all pods)
    "Issue 4": "_______________",
    # Answer: Only 1 replica (single point of failure, no HA)
    "Issue 5": "_______________",
    # Answer: Secrets in plain text env vars (GROQ_API_KEY, DATABASE_URL visible in YAML)
    "Issue 6": "_______________",
    # Answer: No rolling update strategy (no maxSurge/maxUnavailable)
}

# YOUR CODE HERE: Identify each issue
# issues["Issue 1"] = "No health probes (liveness/readiness)"
# issues["Issue 2"] = ???
# issues["Issue 3"] = ???
# issues["Issue 4"] = ???
# issues["Issue 5"] = ???
# issues["Issue 6"] = ???

issue_score = 0
for issue_name, description in issues.items():
    is_filled = description != "_______________"
    if is_filled:
        issue_score += 1
    status = "PASS" if is_filled else "FAIL"
    print(f"    [{status}] {issue_name}: {description}")

print(f"\n  Found: {issue_score}/{len(issues)} production issues")

# Additional hints
if issue_score < 6:
    print()
    print("  Hints — look for:")
    print("    - What happens if the container hangs? (probes)")
    print("    - What happens if memory spikes? (resources)")
    print("    - What happens during node drain? (PDB)")
    print("    - What if the single pod crashes? (replicas)")
    print("    - Are credentials safe? (secrets)")
    print("    - How does a deployment rollout proceed? (strategy)")

# Save production-ready reference
production_yaml = textwrap.dedent("""\
    # Production-Ready Deployment Reference
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: ai-agent
      labels:
        app: agent
        version: "2.0"
        team: platform
    spec:
      replicas: 3
      strategy:
        type: RollingUpdate
        rollingUpdate:
          maxSurge: 1
          maxUnavailable: 0
      selector:
        matchLabels:
          app: agent
      template:
        metadata:
          labels:
            app: agent
            version: "2.0"
        spec:
          securityContext:
            runAsNonRoot: true
            runAsUser: 1000
          containers:
          - name: agent
            image: ai-agent:2.0
            ports:
            - containerPort: 8000
            envFrom:
            - configMapRef:
                name: agent-config
            - secretRef:
                name: agent-secrets
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "1000m"
            readinessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 5
              periodSeconds: 10
            livenessProbe:
              httpGet:
                path: /health
                port: 8000
              initialDelaySeconds: 15
              periodSeconds: 20
              failureThreshold: 3
""")

with open(os.path.join(WORKDIR, "production-deployment-reference.yaml"), "w") as f:
    f.write(production_yaml)

print("\n  Generated: bad-deployment.yaml, production-deployment-reference.yaml")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 07 Summary ---\n")
print("  Key concepts:")
print("    1. Production readiness spans 4 areas: Reliability, Scalability, Observability, Security")
print("    2. Minimum production requirements: probes + resources + PDB + replicas >= 2")
print("    3. Never put secrets in plain text env vars — use K8s Secrets")
print("    4. Use specific image tags (not :latest) for reproducibility")
print("    5. Always define a rolling update strategy")
print("    6. Security: non-root, read-only fs, network policies")
print(f"\n  TODO 1: {filled}/{len(checklist_items)} checklist items categorized")
print(f"  TODO 2: {issue_score}/{len(issues)} production issues identified")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<45} ({size} bytes)")
