"""
Lab 03: Health Checks & Python HealthChecker
==============================================
Implement production-grade /health endpoint
and configure Python async health checking with signal handling.
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/prod-lab-12-03"

print("=" * 50)
print("  Lab 03: Health Checks & Python HealthChecker")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# Step 1: Health Endpoint Pattern
# ============================================================

print("\n--- Step 1: Health Endpoint Pattern ---\n")

health_code = textwrap.dedent("""\
    @app.get("/health")
    async def health():
        checks = {
            "redis": await redis_client.ping(),
            "chromadb": await chroma_client.heartbeat(),
            "model_loaded": agent.is_ready(),
        }
        healthy = all(checks.values())
        return JSONResponse(
            status_code=200 if healthy else 503,
            content={
                "status": "ok" if healthy else "degraded",
                "checks": checks,
            }
        )
""")

print("  Production health endpoint:\n")
for line in health_code.strip().split("\n"):
    print(f"    {line}")

print("\n  Healthy response (200):  {\"status\": \"ok\", \"checks\": {\"redis\": true, ...}}")
print("  Degraded response (503): {\"status\": \"degraded\", \"checks\": {\"redis\": false, ...}}")


# ============================================================
# Step 2: Python Async HealthChecker Concepts
# ============================================================

print("\n\n--- Step 2: Python Async HealthChecker Concepts ---\n")

concepts = [
    ("HealthChecker",     "Is a service endpoint responding?",
                          "Fails -> marks target 'unhealthy' after retries",
                          "httpx.get(url), interval=30s, timeout=10s, retries=3"),
    ("Signal handlers",   "What happens when the process receives SIGTERM?",
                          "Graceful shutdown -> close connections, flush logs",
                          "signal.signal(SIGTERM, handler) or asyncio shutdown"),
    ("Health states",     "What are the possible application health states?",
                          "starting -> healthy -> unhealthy",
                          "Track via HealthChecker.status attribute"),
]

print(f"    {'Concept':<18} {'Question':<48} {'Behavior'}")
print(f"    {'-'*100}")
for name, question, behavior, config in concepts:
    print(f"    {name:<18} {question:<48} {behavior}")
    print(f"    {'':18} Config: {config}")
    print()


# ============================================================
# Step 3: Python Async HealthChecker Reference
# ============================================================

print("--- Step 3: Python Async HealthChecker Reference ---\n")

healthchecker_code = textwrap.dedent("""\
    import asyncio
    import signal
    import httpx

    class HealthChecker:
        def __init__(self, targets: list[dict]):
            self.targets = targets  # [{url, interval_seconds, timeout_seconds, retries, start_delay_seconds}]
            self.results = {}       # {name: "healthy" | "unhealthy" | "starting"}
            self._running = True

        async def check_one(self, name: str, url: str, timeout: float, retries: int) -> bool:
            for attempt in range(retries):
                try:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(url, timeout=timeout)
                        if resp.status_code == 200:
                            return True
                except (httpx.RequestError, httpx.TimeoutException):
                    pass
                await asyncio.sleep(1)
            return False

        async def monitor(self, target: dict):
            name = target["url"]
            self.results[name] = "starting"
            await asyncio.sleep(target.get("start_delay_seconds", 0))
            while self._running:
                healthy = await self.check_one(
                    name, target["url"],
                    target.get("timeout_seconds", 10),
                    target.get("retries", 3),
                )
                self.results[name] = "healthy" if healthy else "unhealthy"
                await asyncio.sleep(target.get("interval_seconds", 30))

        async def run(self):
            tasks = [asyncio.create_task(self.monitor(t)) for t in self.targets]
            await asyncio.gather(*tasks, return_exceptions=True)

        def shutdown(self):
            self._running = False

    # --- Signal handler for graceful shutdown ---
    checker = HealthChecker(targets=[
        {"url": "http://localhost:8000/health", "interval_seconds": 30,
         "timeout_seconds": 10, "retries": 3, "start_delay_seconds": 5},
    ])

    def handle_sigterm(signum, frame):
        print("SIGTERM received, shutting down gracefully...")
        checker.shutdown()

    signal.signal(signal.SIGTERM, handle_sigterm)
""")

for line in healthchecker_code.strip().split("\n"):
    print(f"    {line}")

with open(os.path.join(WORKDIR, "healthchecker-reference.py"), "w") as f:
    f.write(healthchecker_code)


# ============================================================
# TODO 1: Write health endpoint code
# ============================================================

print("\n\n--- TODO 1: Health Endpoint Code ---\n")

print("  Write a FastAPI /health endpoint that:")
print("    - Checks redis (redis_client.ping())")
print("    - Checks chromadb (chroma_client.heartbeat())")
print("    - Checks model (agent.is_ready())")
print("    - Returns 200 if all healthy, 503 if degraded")
print("    - Returns JSON with 'status' and 'checks' fields\n")

todo1_code = textwrap.dedent("""\
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse

    app = FastAPI()

    @app.get("/health")
    async def health():
        checks = {
            "redis": await redis_client.ping(),
            "chromadb": await chroma_client.heartbeat(),
            "model_loaded": agent.is_ready(),
        }
        healthy = all(checks.values())
        return JSONResponse(
            status_code=200 if healthy else 503,
            content={
                "status": "ok" if healthy else "degraded",
                "checks": checks,
            }
        )
""")

with open(os.path.join(WORKDIR, "health.py"), "w") as f:
    f.write(todo1_code)

checks1 = [
    ("Has /health route",          "/health" in todo1_code),
    ("Has async def",              "async def" in todo1_code or "def health" in todo1_code),
    ("Checks redis",               "redis" in todo1_code),
    ("Checks chromadb",            "chromadb" in todo1_code or "chroma" in todo1_code),
    ("Checks model",               "model" in todo1_code or "agent" in todo1_code or "ready" in todo1_code),
    ("Returns 200 or 503",         "200" in todo1_code and "503" in todo1_code),
    ("Has status field",           "status" in todo1_code),
    ("Has checks field",           "checks" in todo1_code),
]

score1 = sum(1 for _, ok in checks1 if ok)
print(f"  Validating ({score1}/{len(checks1)}):\n")
for name, ok in checks1:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# TODO 2: Python HealthChecker with signal handling
# ============================================================

print("\n\n--- TODO 2: Python HealthChecker with Signal Handling ---\n")

print("  Create a Python HealthChecker config and signal handler:")
print("    - HealthChecker target: url=http://localhost:8000/health")
print("    - Config: interval_seconds=30, timeout_seconds=10, retries=3, start_delay_seconds=15")
print("    - Signal handler: SIGTERM -> graceful shutdown")
print("    - Startup sequencing: wait for dependencies before starting app\n")

todo2_code = textwrap.dedent("""\
    import asyncio
    import signal
    import httpx

    class HealthChecker:
        def __init__(self, targets: list[dict]):
            self.targets = targets
            self.results = {}
            self._running = True

        async def check_one(self, name: str, url: str, timeout: float, retries: int) -> bool:
            for attempt in range(retries):
                try:
                    async with httpx.AsyncClient() as client:
                        resp = await client.get(url, timeout=timeout)
                        if resp.status_code == 200:
                            return True
                except (httpx.RequestError, httpx.TimeoutException):
                    pass
                await asyncio.sleep(1)
            return False

        async def monitor(self, target: dict):
            name = target["url"]
            self.results[name] = "starting"
            await asyncio.sleep(target.get("start_delay_seconds", 0))
            while self._running:
                healthy = await self.check_one(
                    name, target["url"],
                    target.get("timeout_seconds", 10),
                    target.get("retries", 3),
                )
                self.results[name] = "healthy" if healthy else "unhealthy"
                await asyncio.sleep(target.get("interval_seconds", 30))

        async def run(self):
            tasks = [asyncio.create_task(self.monitor(t)) for t in self.targets]
            await asyncio.gather(*tasks, return_exceptions=True)

        def shutdown(self):
            self._running = False

    # --- Startup sequencing: wait for dependencies ---
    async def wait_for_ready(url: str, timeout: float = 60, interval: float = 2):
        \"\"\"Wait for a dependency to become ready before starting the app.\"\"\"
        import time
        start = time.time()
        while time.time() - start < timeout:
            try:
                async with httpx.AsyncClient() as client:
                    resp = await client.get(url, timeout=5)
                    if resp.status_code == 200:
                        return True
            except (httpx.RequestError, httpx.TimeoutException):
                pass
            await asyncio.sleep(interval)
        raise RuntimeError(f"Dependency {url} not ready after {timeout}s")

    # --- HealthChecker config ---
    checker = HealthChecker(targets=[
        {
            "url": "http://localhost:8000/health",
            "interval_seconds": 30,
            "timeout_seconds": 10,
            "retries": 3,
            "start_delay_seconds": 15,
        },
    ])

    # --- Signal handler for graceful shutdown ---
    def handle_sigterm(signum, frame):
        print("SIGTERM received, shutting down gracefully...")
        checker.shutdown()

    signal.signal(signal.SIGTERM, handle_sigterm)

    # --- Main startup sequence ---
    # async def main():
    #     await wait_for_ready("http://localhost:6379")   # wait for Redis
    #     await wait_for_ready("http://localhost:8001")   # wait for ChromaDB
    #     asyncio.create_task(checker.run())              # start health monitoring
    #     # Then start uvicorn or the FastAPI app
""")

with open(os.path.join(WORKDIR, "healthchecker_config.py"), "w") as f:
    f.write(todo2_code)

checks2 = [
    ("Has HealthChecker class",    "HealthChecker" in todo2_code),
    ("Has target URL",             "localhost" in todo2_code or "/health" in todo2_code),
    ("Has interval_seconds",       "interval_seconds" in todo2_code or "interval" in todo2_code),
    ("Has timeout_seconds",        "timeout_seconds" in todo2_code or "timeout" in todo2_code),
    ("Has retries",                "retries" in todo2_code or "retry" in todo2_code),
    ("Has start_delay_seconds",    "start_delay" in todo2_code or "delay" in todo2_code),
    ("Has signal handler",         "signal" in todo2_code or "SIGTERM" in todo2_code),
    ("Has shutdown method",        "shutdown" in todo2_code or "graceful" in todo2_code),
    ("Has async/await pattern",    "async" in todo2_code or "await" in todo2_code or "asyncio" in todo2_code),
    ("Has dependency wait",        "wait" in todo2_code or "ready" in todo2_code or "startup" in todo2_code or "sequenc" in todo2_code),
]

score2 = sum(1 for _, ok in checks2 if ok)
print(f"  Validating ({score2}/{len(checks2)}):\n")
for name, ok in checks2:
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}")


# ============================================================
# Summary
# ============================================================

print(f"\n\n--- Lab 03 Summary ---\n")
print("  Key concepts:")
print("    1. /health checks all dependencies (redis, chromadb, model)")
print("    2. Returns 200 (healthy) or 503 (degraded)")
print("    3. Python async HealthChecker monitors application health")
print("    4. Signal handlers (SIGTERM) enable graceful shutdown")
print("    5. Startup sequencing with retry/wait ensures dependency order")
print(f"\n  TODO 1: {score1}/{len(checks1)} health endpoint checks")
print(f"  TODO 2: {score2}/{len(checks2)} healthchecker config checks")
print(f"\n  Files generated in {WORKDIR}/")
