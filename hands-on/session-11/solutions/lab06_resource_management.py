"""
Lab 06 Solution: Resource Management
=======================================
"""

import os
import shutil
import textwrap

WORKDIR = "/tmp/k8s-lab-06"

print("=" * 50)
print("  Lab 06 Solution: Resource Management")
print("=" * 50)

if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)


# ============================================================
# TODO 1 Solution: Resource Configuration for AI Stack
# ============================================================

print("\n--- TODO 1 Solution: AI Stack Resources ---\n")

agent_resources = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: unigps-agent
      labels:
        app: agent
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
            resources:
              requests:
                memory: "256Mi"
                cpu: "250m"
              limits:
                memory: "1Gi"
                cpu: "1000m"
""")

redis_resources = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: redis
      labels:
        app: redis
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: redis
      template:
        metadata:
          labels:
            app: redis
        spec:
          containers:
          - name: redis
            image: redis:7-alpine
            ports:
            - containerPort: 6379
            resources:
              requests:
                memory: "64Mi"
                cpu: "100m"
              limits:
                memory: "128Mi"
                cpu: "200m"
""")

chromadb_resources = textwrap.dedent("""\
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: chromadb
      labels:
        app: chromadb
    spec:
      replicas: 1
      selector:
        matchLabels:
          app: chromadb
      template:
        metadata:
          labels:
            app: chromadb
        spec:
          containers:
          - name: chromadb
            image: chromadb/chroma:latest
            ports:
            - containerPort: 8000
            resources:
              requests:
                memory: "512Mi"
                cpu: "500m"
              limits:
                memory: "2Gi"
                cpu: "1000m"
""")

for name, content in [("agent", agent_resources), ("redis", redis_resources), ("chromadb", chromadb_resources)]:
    filepath = os.path.join(WORKDIR, f"{name}-deployment.yaml")
    with open(filepath, "w") as f:
        f.write(content)

    has_requests = "requests:" in content
    has_limits = "limits:" in content
    has_memory = "memory:" in content
    has_cpu = "cpu:" in content
    checks = [has_requests, has_limits, has_memory, has_cpu]
    passed = sum(checks)
    print(f"  {name}: {passed}/4 resource checks passed")

print("\n  Resource breakdown:")
print("    Agent:   requests 256Mi/250m, limits 1Gi/1000m (3 replicas)")
print("    Redis:   requests 64Mi/100m,  limits 128Mi/200m (1 replica)")
print("    ChromaDB: requests 512Mi/500m, limits 2Gi/1000m (1 replica)")


# ============================================================
# TODO 2 Solution: Cluster Capacity Calculator
# ============================================================

print("\n\n--- TODO 2 Solution: Cluster Capacity ---\n")

stack = [
    {"name": "agent", "replicas": 3, "mem_request_mi": 256, "cpu_request_m": 250},
    {"name": "redis", "replicas": 1, "mem_request_mi": 64, "cpu_request_m": 100},
    {"name": "chromadb", "replicas": 1, "mem_request_mi": 512, "cpu_request_m": 500},
]

total_memory_mi = sum(comp["replicas"] * comp["mem_request_mi"] for comp in stack)
total_cpu_m = sum(comp["replicas"] * comp["cpu_request_m"] for comp in stack)

print("  Stack:")
for comp in stack:
    mem = comp["replicas"] * comp["mem_request_mi"]
    cpu = comp["replicas"] * comp["cpu_request_m"]
    print(f"    {comp['name']:>10}: {comp['replicas']} × {comp['mem_request_mi']}Mi = {mem}Mi, "
          f"{comp['replicas']} × {comp['cpu_request_m']}m = {cpu}m")

print(f"\n  Totals:")
print(f"    Memory: {total_memory_mi} Mi ({total_memory_mi/1024:.1f} Gi)")
print(f"    CPU:    {total_cpu_m}m ({total_cpu_m/1000:.2f} cores)")

expected_mem = 3*256 + 1*64 + 1*512
expected_cpu = 3*250 + 1*100 + 1*500
print(f"\n    [{'PASS' if total_memory_mi == expected_mem else 'FAIL'}] Memory: {total_memory_mi} Mi (expected {expected_mem} Mi)")
print(f"    [{'PASS' if total_cpu_m == expected_cpu else 'FAIL'}] CPU: {total_cpu_m}m (expected {expected_cpu}m)")

print(f"\n  Cluster sizing:")
print(f"    Minimum: 1 node with 2Gi RAM + 2 CPU cores")
print(f"    Recommended: 2+ nodes for HA (survive node failure)")
print(f"    With system overhead (~500Mi + 500m), use 3Gi + 3 CPU nodes")

print(f"\n  Files saved to {WORKDIR}/")

print("\n" + "=" * 50)
print("Lab 06 Solution complete!")
print("- TODO 1: Resource config for agent, redis, chromadb")
print(f"- TODO 2: Cluster needs {total_memory_mi}Mi memory + {total_cpu_m}m CPU")
