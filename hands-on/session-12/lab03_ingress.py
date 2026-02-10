"""
Lab 03: Ingress & Traffic Routing
===================================
Learn how Ingress provides HTTP routing,
path-based routing, and TLS termination.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-03"

print("=" * 50)
print("  Lab 03: Ingress & Traffic Routing")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Why Ingress?
# ============================================================

print("\n--- Step 1: Why Ingress? ---\n")

print("  Problem: LoadBalancer Service = 1 external IP per service")
print("    agent-svc  → LoadBalancer → $10/month")
print("    grafana-svc → LoadBalancer → $10/month")
print("    langfuse-svc → LoadBalancer → $10/month")
print("    Total: 3 IPs × $10 = $30/month\n")

print("  Solution: Ingress = 1 external IP, route by path/host")
print("    Ingress (1 IP) → /api/*     → agent-svc")
print("                   → /grafana/* → grafana-svc")
print("                   → /langfuse  → langfuse-svc")
print("    Total: 1 IP × $10 = $10/month")

comparison = [
    ("Feature",           "LoadBalancer Service", "Ingress"),
    ("External IPs",      "1 per service",        "1 for all"),
    ("Path routing",      "No",                   "Yes"),
    ("Host routing",      "No",                   "Yes"),
    ("TLS termination",   "No (need extra LB)",   "Yes (built-in)"),
    ("Cost",              "$$ (per service)",      "$ (shared)"),
    ("HTTP features",     "None",                 "Rewrites, redirects, rate limiting"),
]

print(f"\n  {'Feature':<22} {'LoadBalancer':<24} {'Ingress'}")
print(f"  {'-'*68}")
for feat, lb, ing in comparison[1:]:
    print(f"  {feat:<22} {lb:<24} {ing}")


# ============================================================
# Step 2: Ingress Architecture
# ============================================================

print("\n\n--- Step 2: Ingress Architecture ---\n")

print("  Internet")
print("     │")
print("     ▼")
print("  ┌─────────────────────────┐")
print("  │  Ingress Controller     │  (nginx, traefik, or cloud LB)")
print("  │  (runs as a pod)        │")
print("  └─────────┬───────────────┘")
print("            │")
print("       Ingress Rules")
print("       ┌────┼────┐")
print("       ▼    ▼    ▼")
print("     /api  /ui  /metrics")
print("       │    │    │")
print("       ▼    ▼    ▼")
print("    agent  web  prometheus")
print("    -svc   -svc  -svc")

print("\n  Components:")
print("    1. Ingress Controller — the actual reverse proxy (nginx pod)")
print("    2. Ingress Resource  — YAML rules (which path → which service)")
print("    3. Services          — backend targets (ClusterIP services)")


# ============================================================
# Step 3: Example Ingress YAML
# ============================================================

print("\n\n--- Step 3: Example Ingress YAML ---\n")

example_ingress = textwrap.dedent("""\
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: ai-stack-ingress
      annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /
    spec:
      ingressClassName: nginx
      rules:
      - host: ai.example.com
        http:
          paths:
          - path: /api
            pathType: Prefix
            backend:
              service:
                name: agent-svc
                port:
                  number: 80
          - path: /grafana
            pathType: Prefix
            backend:
              service:
                name: grafana-svc
                port:
                  number: 3000
""")

print("  Example with path-based routing:")
for line in example_ingress.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "example-ingress.yaml"), "w") as f:
    f.write(example_ingress)


# ============================================================
# TODO 1: Create an Ingress for the AI Stack
# ============================================================

print("\n\n--- TODO 1: Create AI Stack Ingress ---\n")

print("  Create an Ingress with path-based routing:")
print("    - apiVersion: networking.k8s.io/v1")
print("    - name: ai-stack-ingress")
print("    - ingressClassName: nginx")
print("    - host: ai.example.com")
print("    - path /api  → agent-svc:80 (Prefix)")
print("    - path /docs → chromadb-svc:8000 (Prefix)")
print("    - TLS with secretName: ai-tls-secret, host: ai.example.com")

todo1_yaml = textwrap.dedent("""\
    # TODO: Create an Ingress for the AI stack
    # Requirements:
    #   apiVersion: networking.k8s.io/v1
    #   kind: Ingress
    #   name: ai-stack-ingress
    #   ingressClassName: nginx
    #   TLS: secretName: ai-tls-secret, hosts: [ai.example.com]
    #   Rules for host ai.example.com:
    #     /api  → agent-svc port 80 (Prefix)
    #     /docs → chromadb-svc port 8000 (Prefix)

""")

with open(os.path.join(WORKDIR, "ai-ingress.yaml"), "w") as f:
    f.write(todo1_yaml)

def validate_ingress(content):
    return [
        ("Has networking.k8s.io/v1", "networking.k8s.io/v1" in content),
        ("Has kind: Ingress", "kind: Ingress" in content),
        ("Has ingressClassName: nginx", "nginx" in content),
        ("Has host ai.example.com", "ai.example.com" in content),
        ("Has path /api", "/api" in content),
        ("Has path /docs", "/docs" in content),
        ("Has agent-svc backend", "agent-svc" in content),
        ("Has chromadb-svc backend", "chromadb-svc" in content),
        ("Has TLS section", "tls:" in content.lower() or "tls:" in content),
        ("Has TLS secret name", "ai-tls-secret" in content),
    ]

results = validate_ingress(todo1_yaml)
passed = sum(1 for _, ok in results if ok)
print(f"\n  Validating your Ingress ({passed}/{len(results)}):")
for name, ok in results:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Ingress vs LoadBalancer Quiz
# ============================================================

print("\n\n--- TODO 2: Ingress Concepts Quiz ---\n")

quiz = [
    {
        "question": "How many external IPs does an Ingress use for 5 services?",
        "answer": "___",
        "correct": "1",
    },
    {
        "question": "What component actually runs as a pod to handle traffic?",
        "answer": "___",
        "correct": "ingress controller",
    },
    {
        "question": "What pathType matches /api and /api/chat but not /apiary?",
        "answer": "___",
        "correct": "prefix",
    },
    {
        "question": "What Ingress field configures HTTPS termination?",
        "answer": "___",
        "correct": "tls",
    },
]

# YOUR CODE HERE: Fill in the answers
# quiz[0]["answer"] = "1"
# quiz[1]["answer"] = ???
# quiz[2]["answer"] = ???
# quiz[3]["answer"] = ???

score = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].lower().strip() == q["correct"].lower().strip()
    if q["answer"] == "___":
        status = "TODO"
    elif is_correct:
        status = "PASS"
        score += 1
    else:
        status = "FAIL"
    print(f"    [{status}] Q{i}: {q['question']}")

print(f"\n  Score: {score}/{len(quiz)}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 03 Summary ---\n")
print("  Key concepts:")
print("    1. Ingress provides HTTP routing to multiple services via 1 IP")
print("    2. Ingress Controller (nginx) runs as a pod that handles traffic")
print("    3. Path-based and host-based routing reduce cost")
print("    4. TLS termination built into Ingress spec")
print(f"\n  TODO 1: {passed}/{len(results)} checks passed")
print(f"  TODO 2: {score}/{len(quiz)} answers correct")
print(f"\n  Files generated in {WORKDIR}/")
