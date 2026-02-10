"""
Lab 02: Exposing Prometheus Metrics
=====================================
Learn how to expose Counter, Gauge, and Histogram
metrics from a Python FastAPI application.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-15-02"

print("=" * 50)
print("  Lab 02: Exposing Prometheus Metrics")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: prometheus_client Library
# ============================================================

print("\n--- Step 1: prometheus_client Library ---\n")

print("  Python's prometheus_client library creates metrics:\n")

code = textwrap.dedent("""\
    from prometheus_client import Counter, Histogram, Gauge, generate_latest
    from fastapi import FastAPI, Response

    app = FastAPI()

    # Define metrics
    REQUEST_COUNT = Counter(
        "agent_requests_total",
        "Total agent requests",
        ["endpoint", "status"]         # Labels
    )
    REQUEST_LATENCY = Histogram(
        "agent_request_duration_seconds",
        "Request duration in seconds",
        ["endpoint"],
        buckets=[0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0]
    )
    ACTIVE_REQUESTS = Gauge(
        "agent_active_requests",
        "Currently processing requests"
    )

    @app.get("/metrics")
    def metrics():
        return Response(generate_latest(), media_type="text/plain")
""")

for line in code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# Step 2: Recording Metrics in Handlers
# ============================================================

print("\n\n--- Step 2: Recording Metrics ---\n")

print("  How to record metrics in request handlers:\n")

handler_code = textwrap.dedent("""\
    import time

    @app.post("/chat")
    async def chat(query: str):
        ACTIVE_REQUESTS.inc()           # Gauge: +1 when request starts
        start = time.time()

        try:
            result = await agent.process(query)
            REQUEST_COUNT.labels(
                endpoint="/chat", status="200"
            ).inc()                     # Counter: +1 on success
            return {"response": result}

        except Exception as e:
            REQUEST_COUNT.labels(
                endpoint="/chat", status="500"
            ).inc()                     # Counter: +1 on error
            raise

        finally:
            duration = time.time() - start
            REQUEST_LATENCY.labels(
                endpoint="/chat"
            ).observe(duration)         # Histogram: record duration
            ACTIVE_REQUESTS.dec()       # Gauge: -1 when done
""")

for line in handler_code.strip().split("\n"):
    print(f"    {line}")


# ============================================================
# Step 3: Metric Naming Conventions
# ============================================================

print("\n\n--- Step 3: Naming Conventions ---\n")

conventions = [
    ("Suffix _total",    "Counter",    "agent_requests_total"),
    ("Suffix _seconds",  "Histogram",  "agent_request_duration_seconds"),
    ("Suffix _bytes",    "Histogram",  "agent_response_size_bytes"),
    ("No special suffix", "Gauge",     "agent_active_connections"),
    ("Prefix app_name",  "All types",  "agent_*, chromadb_*, redis_*"),
]

print(f"  {'Convention':<22} {'Type':<14} {'Example'}")
print(f"  {'-'*55}")
for conv, typ, example in conventions:
    print(f"  {conv:<22} {typ:<14} {example}")

print("\n  Labels add dimensions:")
print('    agent_requests_total{endpoint="/chat",status="200"} 1247')
print('    agent_requests_total{endpoint="/chat",status="500"} 13')


# ============================================================
# TODO 1: Write metrics endpoint code
# ============================================================

print("\n\n--- TODO 1: Write Metrics Endpoint ---\n")

print("  Create a complete metrics.py file for an AI agent:")
print("    - Counter: agent_requests_total (labels: endpoint, status)")
print("    - Counter: agent_tokens_total (labels: model, direction)")
print("    - Histogram: agent_request_duration_seconds (labels: endpoint)")
print("    - Histogram: agent_llm_duration_seconds (labels: model)")
print("    - Gauge: agent_active_requests")
print("    - /metrics endpoint using generate_latest()")

todo1_code = textwrap.dedent("""\
    # TODO: Complete metrics.py for AI agent
    # Define all 5 metrics listed above
    # Include /metrics endpoint

""")

with open(os.path.join(WORKDIR, "metrics.py"), "w") as f:
    f.write(todo1_code)

code_checks = [
    ("Has Counter import",          "Counter" in todo1_code),
    ("Has Histogram import",        "Histogram" in todo1_code),
    ("Has Gauge import",            "Gauge" in todo1_code),
    ("Has generate_latest",         "generate_latest" in todo1_code),
    ("Has agent_requests_total",    "agent_requests_total" in todo1_code),
    ("Has agent_tokens_total",      "agent_tokens_total" in todo1_code),
    ("Has duration_seconds",        "duration_seconds" in todo1_code),
    ("Has agent_active_requests",   "agent_active_requests" in todo1_code),
    ("Has /metrics endpoint",       "/metrics" in todo1_code),
    ("Has labels",                  "endpoint" in todo1_code and "status" in todo1_code),
]

score1 = sum(1 for _, ok in code_checks if ok)
print(f"\n  Validating Code ({score1}/{len(code_checks)}):\n")
for name, ok in code_checks:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Metric recording patterns quiz
# ============================================================

print("\n\n--- TODO 2: Metric Patterns Quiz ---\n")

quiz = [
    {
        "question": "What method records a value in a Histogram?",
        "answer": "___",
        "correct": "observe",
    },
    {
        "question": "What method increments a Counter by 1?",
        "answer": "___",
        "correct": "inc",
    },
    {
        "question": "What method decreases a Gauge?",
        "answer": "___",
        "correct": "dec",
    },
    {
        "question": "What method selects label values on a metric?",
        "answer": "___",
        "correct": "labels",
    },
    {
        "question": "Should Counter values ever decrease? (yes/no)",
        "answer": "___",
        "correct": "no",
    },
]

# YOUR CODE HERE: Fill in the answers

score2 = 0
for i, q in enumerate(quiz, 1):
    is_correct = q["answer"].strip().lower() == q["correct"].lower()
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

print(f"\n\n--- Lab 02 Summary ---\n")
print("  Key concepts:")
print("    1. prometheus_client: Counter, Histogram, Gauge, generate_latest")
print("    2. Counter.inc(), Histogram.observe(), Gauge.inc()/dec()")
print("    3. .labels(key=value) selects label dimensions")
print("    4. Expose /metrics endpoint returning generate_latest()")
print(f"\n  TODO 1: {score1}/{len(code_checks)} code checks passed")
print(f"  TODO 2: {score2}/{len(quiz)} quiz answers correct")
print(f"\n  Files generated in {WORKDIR}/")
