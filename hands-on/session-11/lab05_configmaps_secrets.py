"""
Lab 05: ConfigMaps and Secrets
================================
Separate configuration from container images using ConfigMaps and Secrets.

No Kubernetes cluster required — generates and validates YAML files.
"""

import os
import shutil
import textwrap
import base64

WORKDIR = "/tmp/k8s-lab-05"

print("=" * 50)
print("  Lab 05: ConfigMaps and Secrets")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

# ============================================================
# Step 1: Why separate config from images?
# ============================================================

print("\n--- Step 1: Why ConfigMaps & Secrets? ---\n")

print("  Problem: Hardcoding config in Docker images")
print("    - Different REDIS_URL for dev vs staging vs prod")
print("    - API keys baked into the image = security risk")
print("    - Changing one setting requires rebuilding the image")
print()
print("  Solution: Kubernetes ConfigMaps and Secrets")
print("    - Config stored OUTSIDE the image")
print("    - Injected as environment variables or files at runtime")
print("    - Same image runs in dev, staging, and prod")
print("    - Secrets are base64-encoded (separate from plaintext config)")


# ============================================================
# Step 2: ConfigMap YAML
# ============================================================

print("\n\n--- Step 2: ConfigMap YAML ---\n")

configmap_yaml = textwrap.dedent("""\
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: agent-config
    data:
      LOG_LEVEL: "info"
      APP_VERSION: "2.0.0"
      REDIS_URL: "redis://redis-svc:6379"
      MAX_RETRIES: "3"
      CORS_ORIGINS: "https://unigps.in,https://app.unigps.in"
""")

with open(os.path.join(WORKDIR, "configmap.yaml"), "w") as f:
    f.write(configmap_yaml)

print("  ConfigMap — non-sensitive configuration:")
for line in configmap_yaml.strip().split("\n"):
    print(f"    {line}")

print()
print("  All values under 'data:' are key-value string pairs.")
print("  They become environment variables when injected into a pod.")


# ============================================================
# Step 3: Secrets and base64 encoding
# ============================================================

print("\n\n--- Step 3: Secrets (base64-encoded) ---\n")

# Demonstrate base64 encoding
secrets_plain = {
    "GROQ_API_KEY": "gsk_abc123def456",
    "DB_PASSWORD": "super-secret-pwd",
}

print("  Secrets store sensitive data as base64-encoded values.")
print("  base64 is NOT encryption — it's encoding for safe YAML transport.\n")

secrets_encoded = {}
for key, value in secrets_plain.items():
    encoded = base64.b64encode(value.encode()).decode()
    secrets_encoded[key] = encoded
    print(f"  {key}:")
    print(f"    Plain:   {value}")
    print(f"    base64:  {encoded}")
    print(f"    Decode:  {base64.b64decode(encoded).decode()}")
    print()

secret_yaml = textwrap.dedent(f"""\
    apiVersion: v1
    kind: Secret
    metadata:
      name: agent-secrets
    type: Opaque
    data:
      GROQ_API_KEY: {secrets_encoded['GROQ_API_KEY']}
      DB_PASSWORD: {secrets_encoded['DB_PASSWORD']}
""")

with open(os.path.join(WORKDIR, "secret.yaml"), "w") as f:
    f.write(secret_yaml)

print("  Generated: secret.yaml")
print()
print("  IMPORTANT: base64 != encrypted!")
print("  Anyone with kubectl access can decode secrets.")
print("  For real security, use external secret managers")
print("  (AWS Secrets Manager, HashiCorp Vault, etc.)")


# ============================================================
# Step 4: Using ConfigMap and Secret in Pods
# ============================================================

print("\n\n--- Step 4: Injecting Config into Pods ---\n")

print("  Method 1: envFrom (inject ALL keys as env vars)")
print("  Method 2: env with valueFrom (pick specific keys)")
print("  Method 3: volume mount (inject as files)\n")

deployment_with_config = textwrap.dedent("""\
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

            # Method 1: Inject ALL keys from ConfigMap/Secret
            envFrom:
            - configMapRef:
                name: agent-config
            - secretRef:
                name: agent-secrets

            # Method 2: Pick individual keys (optional)
            env:
            - name: PYTHONUNBUFFERED
              value: "1"
            - name: API_KEY
              valueFrom:
                secretKeyRef:
                  name: agent-secrets
                  key: GROQ_API_KEY

            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "512Mi"
                cpu: "500m"
""")

with open(os.path.join(WORKDIR, "deployment-with-config.yaml"), "w") as f:
    f.write(deployment_with_config)

print("  Deployment with ConfigMap + Secret injection:")
print()
print("    envFrom:                         # All keys become env vars")
print("    - configMapRef:")
print("        name: agent-config           # LOG_LEVEL, APP_VERSION, REDIS_URL...")
print("    - secretRef:")
print("        name: agent-secrets          # GROQ_API_KEY, DB_PASSWORD")
print()
print("    env:                             # Individual keys")
print("    - name: API_KEY")
print("      valueFrom:")
print("        secretKeyRef:")
print("          name: agent-secrets")
print("          key: GROQ_API_KEY")
print()
print("  Generated: deployment-with-config.yaml")


# ============================================================
# Step 5: Validators
# ============================================================

print("\n\n--- Step 5: ConfigMap & Secret Validators ---\n")

def validate_configmap(content: str) -> list:
    checks = []
    checks.append(("apiVersion: v1", "apiVersion: v1" in content))
    checks.append(("kind: ConfigMap", "kind: ConfigMap" in content))
    checks.append(("Has metadata.name", "metadata:" in content and "name:" in content))
    checks.append(("Has data section", "data:" in content))
    return checks

def validate_secret(content: str) -> list:
    checks = []
    checks.append(("apiVersion: v1", "apiVersion: v1" in content))
    checks.append(("kind: Secret", "kind: Secret" in content))
    checks.append(("Has metadata.name", "metadata:" in content and "name:" in content))
    checks.append(("Has type: Opaque", "type: Opaque" in content))
    checks.append(("Has data section", "data:" in content))
    return checks

for name, content, validator in [
    ("ConfigMap", configmap_yaml, validate_configmap),
    ("Secret", secret_yaml, validate_secret),
]:
    results = validator(content)
    passed = sum(1 for _, ok in results if ok)
    print(f"  {name} ({passed}/{len(results)}):")
    for check_name, ok in results:
        print(f"    [{'PASS' if ok else 'FAIL'}] {check_name}")
    print()


# ============================================================
# TODO 1: Create ConfigMap for different environments
# ============================================================

print("\n--- TODO 1: Create Environment-Specific ConfigMaps ---\n")

print("  Create two ConfigMaps — one for dev, one for prod.")
print("  Same keys, different values. Same image, different config.\n")

print("  Dev ConfigMap (agent-config-dev):")
print("    LOG_LEVEL: debug")
print("    APP_VERSION: 2.0.0-dev")
print("    REDIS_URL: redis://localhost:6379")
print("    ENABLE_SWAGGER: 'true'\n")

print("  Prod ConfigMap (agent-config-prod):")
print("    LOG_LEVEL: warning")
print("    APP_VERSION: 2.0.0")
print("    REDIS_URL: redis://redis-svc:6379")
print("    ENABLE_SWAGGER: 'false'\n")

# YOUR CODE HERE: Create both ConfigMaps
dev_configmap = textwrap.dedent("""\
    # TODO: Create agent-config-dev ConfigMap
    # with dev-specific values listed above

""")

prod_configmap = textwrap.dedent("""\
    # TODO: Create agent-config-prod ConfigMap
    # with prod-specific values listed above

""")

with open(os.path.join(WORKDIR, "configmap-dev.yaml"), "w") as f:
    f.write(dev_configmap)
with open(os.path.join(WORKDIR, "configmap-prod.yaml"), "w") as f:
    f.write(prod_configmap)

for env_name, content in [("Dev", dev_configmap), ("Prod", prod_configmap)]:
    results = validate_configmap(content)
    passed = sum(1 for _, ok in results if ok)
    print(f"  {env_name} ConfigMap ({passed}/{len(results)}):")
    for check_name, ok in results:
        print(f"    [{'PASS' if ok else 'FAIL'}] {check_name}")
    print()


# ============================================================
# TODO 2: Create a Secret with encoded values
# ============================================================

print("\n--- TODO 2: Create a Secret with base64-encoded Values ---\n")

print("  Create a Secret named 'agent-api-keys' with:")
print("    GROQ_API_KEY: gsk_test_key_12345")
print("    OPENAI_API_KEY: sk-test-openai-key-67890")
print()
print("  Remember: values must be base64-encoded in the YAML!\n")

# Helper: encode a value
def encode_secret(value):
    return base64.b64encode(value.encode()).decode()

print(f"  Hint — base64 values:")
print(f"    gsk_test_key_12345:      {encode_secret('gsk_test_key_12345')}")
print(f"    sk-test-openai-key-67890: {encode_secret('sk-test-openai-key-67890')}")
print()

# YOUR CODE HERE: Create the Secret YAML with base64-encoded values
api_keys_secret = textwrap.dedent("""\
    # TODO: Create agent-api-keys Secret
    # Use the base64-encoded values from the hints above
    # type: Opaque

""")

with open(os.path.join(WORKDIR, "secret-api-keys.yaml"), "w") as f:
    f.write(api_keys_secret)

results = validate_secret(api_keys_secret)
passed = sum(1 for _, ok in results if ok)
print(f"  Secret validation ({passed}/{len(results)}):")
for check_name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {check_name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 05 Summary ---\n")
print("  Key concepts:")
print("    1. ConfigMap: non-sensitive config (LOG_LEVEL, REDIS_URL)")
print("    2. Secret: sensitive data (API keys) — base64-encoded")
print("    3. envFrom: inject ALL keys as environment variables")
print("    4. valueFrom: pick individual keys from ConfigMap/Secret")
print("    5. Same image + different ConfigMap = different environment")
print("    6. base64 is NOT encryption — use external secret managers")
print(f"\n  Files generated in {WORKDIR}/:")
for f in sorted(os.listdir(WORKDIR)):
    size = os.path.getsize(os.path.join(WORKDIR, f))
    print(f"    {f:<35} ({size} bytes)")
