"""
Lab 03 Solution: Ingress & Traffic Routing
============================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-12-03"

print("=" * 50)
print("  Lab 03 Solution: Ingress & Traffic Routing")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: Ingress with TLS
# ============================================================

print("\n--- TODO 1 Solution: AI Stack Ingress ---\n")

todo1_yaml = textwrap.dedent("""\
    apiVersion: networking.k8s.io/v1
    kind: Ingress
    metadata:
      name: ai-stack-ingress
      annotations:
        nginx.ingress.kubernetes.io/rewrite-target: /
    spec:
      ingressClassName: nginx
      tls:
      - hosts:
        - ai.example.com
        secretName: ai-tls-secret
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
          - path: /docs
            pathType: Prefix
            backend:
              service:
                name: chromadb-svc
                port:
                  number: 8000
""")

with open(os.path.join(WORKDIR, "ai-ingress.yaml"), "w") as f:
    f.write(todo1_yaml)

checks = [
    ("Has networking.k8s.io/v1", "networking.k8s.io/v1" in todo1_yaml),
    ("Has kind: Ingress", "kind: Ingress" in todo1_yaml),
    ("Has ingressClassName: nginx", "nginx" in todo1_yaml),
    ("Has host ai.example.com", "ai.example.com" in todo1_yaml),
    ("Has path /api", "/api" in todo1_yaml),
    ("Has path /docs", "/docs" in todo1_yaml),
    ("Has agent-svc backend", "agent-svc" in todo1_yaml),
    ("Has chromadb-svc backend", "chromadb-svc" in todo1_yaml),
    ("Has TLS section", "tls:" in todo1_yaml),
    ("Has TLS secret name", "ai-tls-secret" in todo1_yaml),
]

passed = sum(1 for _, ok in checks if ok)
print(f"  Ingress validation ({passed}/{len(checks)}):")
for name, ok in checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")

print("\n  Routing summary:")
print("    ai.example.com/api  -> agent-svc:80")
print("    ai.example.com/docs -> chromadb-svc:8000")
print("    TLS: ai-tls-secret for HTTPS termination")


# ============================================================
# TODO 2 Solution: Ingress Concepts Quiz
# ============================================================

print("\n\n--- TODO 2 Solution: Ingress Concepts Quiz ---\n")

quiz = [
    {
        "question": "How many external IPs does an Ingress use for 5 services?",
        "answer": "1",
        "correct": "1",
    },
    {
        "question": "What component actually runs as a pod to handle traffic?",
        "answer": "ingress controller",
        "correct": "ingress controller",
    },
    {
        "question": "What pathType matches /api and /api/chat but not /apiary?",
        "answer": "prefix",
        "correct": "prefix",
    },
    {
        "question": "What Ingress field configures HTTPS termination?",
        "answer": "tls",
        "correct": "tls",
    },
]

score = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].lower().strip() == q["correct"].lower().strip()
    if is_correct:
        score += 1
    print(f"    [PASS] Q{i}: {q['question']}")
    print(f"           Answer: {q['answer']}")

print(f"\n  Score: {score}/{len(quiz)}")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 03 Solution complete!")
print(f"- TODO 1: {passed}/{len(checks)} ingress checks passed")
print(f"- TODO 2: {score}/{len(quiz)} quiz answers correct")
