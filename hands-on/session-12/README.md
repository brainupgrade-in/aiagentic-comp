# Session 12: Kubernetes Advanced Deployments — Hands-on Labs

## Prerequisites

- Session 11 completed (K8s fundamentals)
- Python 3.10+ installed
- No Kubernetes cluster needed — labs generate and validate YAML files

```bash
# No pip packages needed — these labs generate K8s manifests
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs K8s? |
|-----|-------|-------------------|------------|
| 01 | Rolling Updates | Rolling update strategies, maxSurge/maxUnavailable, rollbacks | No |
| 02 | HPA | Horizontal Pod Autoscaler, autoscaling/v2, scaling simulation | No |
| 03 | Ingress | Path-based routing, TLS termination, Ingress vs LoadBalancer | No |
| 04 | Persistent Storage | PVC, access modes (RWO/ROX/RWX), mounting volumes | No |
| 05 | StatefulSets | StatefulSet vs Deployment, headless services, volumeClaimTemplates | No |
| 06 | ChromaDB Deployment | Dual services, production probes, resource limits | No |
| 07 | Full Stack | Deployment order, envFrom, complete AI stack architecture | No |
| 08 | **Challenge** | Production AI stack: ChromaDB + Agent + HPA + Ingress + TLS | No |

## How to Run

```bash
cd hands-on/session-12

# Run a lab (generates YAML files in /tmp/k8s-lab-12-XX/)
python lab01_rolling_updates.py

# Check the solution
python solutions/lab01_rolling_updates.py

# If kubectl is available, the generated YAML can be applied:
python solutions/lab08_challenge.py
# Then: cd /tmp/k8s-lab-12-08 && kubectl apply -f .
```

## Tips

- All 8 labs work WITHOUT a Kubernetes cluster — they generate and validate YAML
- If kubectl is available, you can apply the generated manifests
- Look for `# TODO` markers — that's where you write code or YAML content
- Labs 01-03 cover Deployment strategies and networking
- Labs 04-06 cover Storage and StatefulSets
- Lab 07 ties everything together in a full stack
- Lab 08 is the challenge combining all concepts
- Generated YAML files appear in `/tmp/k8s-lab-12-XX/` directories
- Compare your work with `solutions/` when done

## What Gets Generated

Each lab creates Kubernetes YAML manifests:
- `agent-deployment.yaml` — Deployment with rolling updates
- `agent-hpa.yaml` — Horizontal Pod Autoscaler
- `ingress.yaml` — Ingress with TLS and path routing
- `chroma-pvc.yaml` — PersistentVolumeClaim
- `chromadb-statefulset.yaml` — StatefulSet with volumeClaimTemplates
- `chromadb-headless-svc.yaml` — Headless Service for StatefulSet
- `chromadb-svc.yaml` — ClusterIP Service for clients

## Estimated Time

~60-75 minutes for all labs (including the challenge)
