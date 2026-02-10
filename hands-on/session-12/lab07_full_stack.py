"""
Lab 07: Full Stack Deployment
==============================
Deploy the complete AI stack with all advanced
K8s objects: Deployments, StatefulSets, Services, Ingress.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-07"

print("=" * 50)
print("  Lab 07: Full Stack Deployment")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Stack Architecture
# ============================================================

print("\n--- Step 1: Stack Architecture ---\n")

print("  ┌──────────────────────────────────────────┐")
print("  │              Ingress                      │")
print("  │  /api → agent-svc   /docs → chromadb-svc │")
print("  └────────────┬──────────────┬───────────────┘")
print("               │              │")
print("  ┌────────────▼────┐   ┌─────▼──────────────┐")
print("  │  Agent API (x3) │   │  ChromaDB (x1)     │")
print("  │  Deployment     │   │  StatefulSet + PVC  │")
print("  │  + HPA + PDB    │   │  + Headless Svc     │")
print("  └────────┬────────┘   └─────────────────────┘")
print("           │")
print("  ┌────────▼────────┐")
print("  │  Redis (x1)     │")
print("  │  Deployment     │")
print("  │  ClusterIP Svc  │")
print("  └─────────────────┘")


# ============================================================
# Step 2: Deployment Order (Dependencies First)
# ============================================================

print("\n\n--- Step 2: Deployment Order ---\n")

deploy_order = [
    ("1. ConfigMap + Secret",       "Config must exist before pods reference it"),
    ("2. Redis Deployment + Svc",   "Cache layer — agent depends on this"),
    ("3. ChromaDB StatefulSet+Svc", "Vector store — agent depends on this"),
    ("4. Agent Deployment + Svc",   "Application layer — depends on Redis + ChromaDB"),
    ("5. HPA + PDB",                "Scaling and disruption protection for agent"),
    ("6. Ingress",                  "External access — needs services to exist"),
]

for step, reason in deploy_order:
    print(f"  {step}")
    print(f"    Why: {reason}\n")


# ============================================================
# Step 3: AI Storage Patterns Reference
# ============================================================

print("\n--- Step 3: AI Storage Patterns ---\n")

patterns = [
    ("Agent API",    "Deployment",   "None (stateless)",     "3 replicas, HPA"),
    ("Redis",        "Deployment",   "None (cache, ok to lose)", "1 replica"),
    ("ChromaDB",     "StatefulSet",  "PVC 10Gi (embeddings)", "1 replica"),
    ("PostgreSQL",   "StatefulSet",  "PVC 20Gi (LangFuse)",  "1 replica"),
    ("Model files",  "N/A",          "PVC (read-only mount)", "Shared across pods"),
]

print(f"  {'Component':<14} {'K8s Object':<14} {'Storage':<26} {'Scaling'}")
print(f"  {'-'*72}")
for comp, obj, storage, scaling in patterns:
    print(f"  {comp:<14} {obj:<14} {storage:<26} {scaling}")


# ============================================================
# TODO 1: Create Agent Deployment with envFrom
# ============================================================

print("\n\n--- TODO 1: Agent Deployment with envFrom ---\n")

print("  Create the agent-api Deployment:")
print("    - name: agent-api, labels: app: agent, component: api")
print("    - replicas: 3")
print("    - strategy: RollingUpdate, maxSurge: 1, maxUnavailable: 0")
print("    - image: agent-api:2.0, containerPort: 8000")
print("    - envFrom: configMapRef: agent-config")
print("    - envFrom: secretRef: agent-secrets")
print("    - resources: requests 256Mi/250m, limits 1Gi/1000m")
print("    - readinessProbe: httpGet /health port 8000 (delay=5, period=10)")
print("    - livenessProbe: httpGet /health port 8000 (delay=15, period=20)")

todo1_yaml = textwrap.dedent("""\
    # TODO: Create agent-api Deployment
    # Include ALL requirements listed above:
    #   rolling update, envFrom (configMap + secret), resources, probes

""")

with open(os.path.join(WORKDIR, "agent-deployment.yaml"), "w") as f:
    f.write(todo1_yaml)

def validate_agent_deploy(content):
    return [
        ("Has kind: Deployment", "kind: Deployment" in content),
        ("Has replicas: 3", "replicas: 3" in content),
        ("Has RollingUpdate strategy", "RollingUpdate" in content),
        ("Has maxUnavailable: 0", "maxUnavailable: 0" in content),
        ("Has image agent-api", "agent-api" in content),
        ("Has envFrom section", "envFrom:" in content),
        ("Has configMapRef", "configMapRef:" in content),
        ("Has secretRef", "secretRef:" in content),
        ("Has resources", "resources:" in content),
        ("Has readinessProbe", "readinessProbe:" in content),
        ("Has livenessProbe", "livenessProbe:" in content),
        ("Has /health path", "/health" in content),
    ]

results = validate_agent_deploy(todo1_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"\n  Validating your Agent Deployment ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Create Deploy Script (kubectl apply order)
# ============================================================

print("\n\n--- TODO 2: Write Deployment Order ---\n")

print("  Fill in the correct kubectl apply order.")
print("  Hint: dependencies must be applied before the things that use them.\n")

# Fill in the correct file names in the right order
deploy_steps = [
    "___",   # Step 1: config — what files? (configmap.yaml + secret.yaml)
    "___",   # Step 2: cache layer
    "___",   # Step 3: vector store
    "___",   # Step 4: application
    "___",   # Step 5: scaling + protection
    "___",   # Step 6: external access
]

# YOUR CODE HERE: Replace the blanks with the correct manifest files
# deploy_steps[0] = "configmap.yaml + secret.yaml"
# deploy_steps[1] = ???
# deploy_steps[2] = ???
# deploy_steps[3] = ???
# deploy_steps[4] = ???
# deploy_steps[5] = ???

expected = [
    "configmap.yaml + secret.yaml",
    "redis-deployment.yaml + redis-service.yaml",
    "chromadb-statefulset.yaml + chromadb-headless-svc.yaml + chromadb-svc.yaml",
    "agent-deployment.yaml + agent-service.yaml",
    "agent-hpa.yaml + agent-pdb.yaml",
    "ingress.yaml",
]

step_labels = [
    "Config & Secrets",
    "Redis (cache)",
    "ChromaDB (vector store)",
    "Agent API (application)",
    "HPA + PDB (scaling)",
    "Ingress (external access)",
]

passed2 = 0
for i, (step, exp, label) in enumerate(zip(deploy_steps, expected, step_labels)):
    # Flexible matching: check key terms
    key_terms = {
        0: ["configmap", "secret"],
        1: ["redis"],
        2: ["chromadb", "statefulset"],
        3: ["agent", "deployment"],
        4: ["hpa", "pdb"],
        5: ["ingress"],
    }
    matches = all(term in step.lower() for term in key_terms[i])
    if matches:
        passed2 += 1
    status = "PASS" if matches else "FAIL"
    print(f"    [{status}] Step {i+1}: {label}")
    if not matches:
        print(f"           Your answer: {step}")

print(f"\n  Deploy order: {passed2}/{len(deploy_steps)} steps correct")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 07 Summary ---\n")
print("  Key concepts:")
print("    1. Deploy dependencies first (config → data → app → ingress)")
print("    2. Agent: Deployment + HPA + PDB (stateless, scalable)")
print("    3. ChromaDB: StatefulSet + dual Services + PVC (stateful)")
print("    4. Redis: Deployment + ClusterIP (cache, ephemeral)")
print(f"\n  TODO 1: {passed}/{len(results)} checks passed")
print(f"  TODO 2: {passed2}/{len(deploy_steps)} deploy order correct")
print(f"\n  Files generated in {WORKDIR}/")
