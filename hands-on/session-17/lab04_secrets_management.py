"""
Lab 04: Secrets & Configuration Management
=============================================
Secure API key handling with Kubernetes Secrets
and environment variable injection.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-17-04"

print("=" * 50)
print("  Lab 04: Secrets & Configuration Management")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Wrong vs Right
# ============================================================

print("\n--- Step 1: Secrets — Wrong vs Right ---\n")

print("  WRONG (hardcoded in code):")
print('    GROQ_API_KEY = "gsk_abc123..."  # Anyone with code access can see')
print()
print("  WRONG (ConfigMap — not encrypted):")
print("    kind: ConfigMap")
print("    data:")
print('      API_KEY: "gsk_abc123..."  # Visible to all with kubectl access')
print()
print("  RIGHT (Kubernetes Secret):")
print("    kind: Secret")
print("    type: Opaque")
print("    data:")
print("      GROQ_API_KEY: Z3NrX2FiYzEyMy4uLg==  # base64 encoded")
print()
print("  RIGHT (injected via envFrom):")
print("    envFrom:")
print("    - secretRef:")
print("        name: api-keys")


# ============================================================
# Step 2: Secret Creation and Injection
# ============================================================

print("\n\n--- Step 2: Secret YAML Reference ---\n")

secret_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: Secret
    metadata:
      name: api-keys
      namespace: ai-stack
    type: Opaque
    data:
      GROQ_API_KEY: Z3NrX2FiYzEyMy4uLg==
      LANGFUSE_SECRET_KEY: c2stbGYtLi4u
      LANGFUSE_PUBLIC_KEY: cGstbGYtLi4u
""")

print("  Secret manifest:\n")
for line in secret_yaml.strip().split("\n"):
    print(f"    {line}")

print("\n  Injection in Deployment:")

inject_yaml = textwrap.dedent("""\
    containers:
    - name: agent
      env:
      - name: GROQ_API_KEY
        valueFrom:
          secretKeyRef:
            name: api-keys
            key: GROQ_API_KEY
      # Or inject ALL keys from the secret:
      envFrom:
      - secretRef:
          name: api-keys
""")

for line in inject_yaml.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "secret-reference.yaml"), "w") as f:
    f.write(secret_yaml)


# ============================================================
# Step 3: Base64 Encoding
# ============================================================

print("\n\n--- Step 3: Base64 Encoding ---\n")

print("  Kubernetes Secrets store values as base64:\n")
print("    echo -n 'gsk_abc123' | base64")
print("    → Z3NrX2FiYzEyMw==")
print()
print("    echo 'Z3NrX2FiYzEyMw==' | base64 -d")
print("    → gsk_abc123")
print()
print("  Note: base64 is NOT encryption — it's just encoding.")
print("  Secrets are stored encrypted at rest in etcd (if configured).")


# ============================================================
# TODO 1: Create Secret manifest
# ============================================================

print("\n\n--- TODO 1: Create Secret Manifest ---\n")

print("  Create a K8s Secret with:")
print("    - name: api-keys, namespace: ai-stack")
print("    - type: Opaque")
print("    - Keys: GROQ_API_KEY, LANGFUSE_SECRET_KEY, LANGFUSE_PUBLIC_KEY")
print("    - All values base64 encoded")
print("    - Deployment snippet showing secretKeyRef injection\n")

todo1_yaml = textwrap.dedent("""\
    # TODO: Secret manifest for API keys + Deployment injection

""")

with open(os.path.join(WORKDIR, "secret.yaml"), "w") as f:
    f.write(todo1_yaml)

checks1 = [
    ("Has kind: Secret",           "kind: Secret" in todo1_yaml),
    ("Has type: Opaque",           "Opaque" in todo1_yaml),
    ("Has namespace: ai-stack",    "ai-stack" in todo1_yaml),
    ("Has GROQ_API_KEY",           "GROQ_API_KEY" in todo1_yaml),
    ("Has LANGFUSE_SECRET_KEY",    "LANGFUSE_SECRET_KEY" in todo1_yaml),
    ("Has LANGFUSE_PUBLIC_KEY",    "LANGFUSE_PUBLIC_KEY" in todo1_yaml),
    ("Has data section",           "data:" in todo1_yaml),
    ("Has secretKeyRef",           "secretKeyRef" in todo1_yaml or "secretRef" in todo1_yaml),
    ("Has valueFrom",              "valueFrom" in todo1_yaml or "envFrom" in todo1_yaml),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Secrets quiz
# ============================================================

print("\n\n--- TODO 2: Secrets Management Quiz ---\n")

quiz = [
    {
        "question": "What K8s object type should API keys be stored in?",
        "answer": "___",
        "correct": "secret",
    },
    {
        "question": "What encoding does K8s use for Secret data values?",
        "answer": "___",
        "correct": "base64",
    },
    {
        "question": "What field in a container spec references a Secret key?",
        "answer": "___",
        "correct": "secretkeyref",
        "check": "secretkeyref",
    },
    {
        "question": "Is base64 encryption or encoding?",
        "answer": "___",
        "correct": "encoding",
    },
    {
        "question": "What K8s field injects ALL keys from a Secret?",
        "answer": "___",
        "correct": "envfrom",
        "check": "envfrom",
    },
]

# YOUR CODE HERE: Fill in quiz answers

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

print(f"\n\n--- Lab 04 Summary ---\n")
print("  Key concepts:")
print("    1. Never hardcode API keys — use K8s Secrets")
print("    2. Secrets store base64-encoded values (not encrypted)")
print("    3. Inject via secretKeyRef (single key) or envFrom (all keys)")
print("    4. ConfigMap for non-sensitive config, Secret for credentials")
print(f"\n  TODO 1: {score1}/{len(checks1)} secret manifest checks")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
