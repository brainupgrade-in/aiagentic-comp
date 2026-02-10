"""
Lab 05 Solution: ConfigMaps and Secrets
=========================================
"""

import os
import shutil
import textwrap
import base64

WORKDIR = "/tmp/k8s-lab-05"

print("=" * 50)
print("  Lab 05 Solution: ConfigMaps and Secrets")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


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


# ============================================================
# TODO 1 Solution: Environment-Specific ConfigMaps
# ============================================================

print("\n--- TODO 1 Solution: Environment ConfigMaps ---\n")

dev_configmap = textwrap.dedent("""\
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: agent-config-dev
    data:
      LOG_LEVEL: "debug"
      APP_VERSION: "2.0.0-dev"
      REDIS_URL: "redis://localhost:6379"
      ENABLE_SWAGGER: "true"
""")

prod_configmap = textwrap.dedent("""\
    apiVersion: v1
    kind: ConfigMap
    metadata:
      name: agent-config-prod
    data:
      LOG_LEVEL: "warning"
      APP_VERSION: "2.0.0"
      REDIS_URL: "redis://redis-svc:6379"
      ENABLE_SWAGGER: "false"
""")

with open(os.path.join(WORKDIR, "configmap-dev.yaml"), "w") as f:
    f.write(dev_configmap)
with open(os.path.join(WORKDIR, "configmap-prod.yaml"), "w") as f:
    f.write(prod_configmap)

for env_name, content in [("Dev", dev_configmap), ("Prod", prod_configmap)]:
    results = validate_configmap(content)
    passed = sum(1 for _, ok in results if ok)
    print(f"  {env_name} ConfigMap ({passed}/{len(results)}):")
    for name, ok in results:
        print(f"    [{'PASS' if ok else 'FAIL'}] {name}")
    print()

print("  Key pattern: Same image, different ConfigMap per environment")
print("    Dev:  kubectl apply -f configmap-dev.yaml")
print("    Prod: kubectl apply -f configmap-prod.yaml")
print("    Both use the same Deployment with envFrom: configMapRef")


# ============================================================
# TODO 2 Solution: Secret with base64 Values
# ============================================================

print("\n\n--- TODO 2 Solution: API Keys Secret ---\n")

groq_b64 = base64.b64encode(b"gsk_test_key_12345").decode()
openai_b64 = base64.b64encode(b"sk-test-openai-key-67890").decode()

api_keys_secret = textwrap.dedent(f"""\
    apiVersion: v1
    kind: Secret
    metadata:
      name: agent-api-keys
    type: Opaque
    data:
      GROQ_API_KEY: {groq_b64}
      OPENAI_API_KEY: {openai_b64}
""")

with open(os.path.join(WORKDIR, "secret-api-keys.yaml"), "w") as f:
    f.write(api_keys_secret)

results = validate_secret(api_keys_secret)
passed = sum(1 for _, ok in results if ok)
print(f"  Secret validation ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print(f"\n  base64 values:")
print(f"    GROQ_API_KEY:   {groq_b64}")
print(f"    OPENAI_API_KEY: {openai_b64}")
print()
print("  Verify decode:")
print(f"    GROQ_API_KEY:   {base64.b64decode(groq_b64).decode()}")
print(f"    OPENAI_API_KEY: {base64.b64decode(openai_b64).decode()}")
print()
print("  Tip: Create secrets from CLI without base64 encoding:")
print("    kubectl create secret generic agent-api-keys \\")
print("      --from-literal=GROQ_API_KEY=gsk_test_key_12345 \\")
print("      --from-literal=OPENAI_API_KEY=sk-test-openai-key-67890")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 05 Solution complete!")
print("- TODO 1: Dev + Prod ConfigMaps (same keys, different values)")
print("- TODO 2: Secret with base64-encoded API keys")
