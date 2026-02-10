# Session 11: Kubernetes Fundamentals — Hands-on Labs

## Prerequisites

- Session 10 completed (Docker concepts understood)
- Python 3.10+ installed
- No Kubernetes cluster needed — labs generate and validate YAML files

```bash
# No pip packages needed — these labs generate K8s manifests
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs K8s? |
|-----|-------|-------------------|------------|
| 01 | K8s Concepts | Architecture, control plane, declarative model | No |
| 02 | Pod Manifests | Pod YAML structure, labels, sidecar pattern | No |
| 03 | Deployments | Replicas, self-healing, rolling updates, strategy | No |
| 04 | Services | ClusterIP, NodePort, LoadBalancer, selectors | No |
| 05 | ConfigMaps & Secrets | Environment config, base64 encoding, injection | No |
| 06 | Resource Management | Requests/limits, scheduling, OOMKill, capacity | No |
| 07 | Health Probes | Readiness, liveness, AI model loading patterns | No |
| 08 | **Challenge** | Complete AI stack deployment (all objects) | Optional |

## How to Run

```bash
cd hands-on/session-11

# Run a lab (generates YAML files in /tmp/k8s-lab-XX/)
python lab01_k8s_concepts.py

# Check the solution
python solutions/lab01_k8s_concepts.py

# If kubectl is available, lab 08 YAML can be applied:
python solutions/lab08_challenge.py
# Then: cd /tmp/k8s-lab-08 && kubectl apply -f .
```

## Tips

- All 8 labs work WITHOUT a Kubernetes cluster — they generate and validate YAML
- If kubectl is available, you can apply the generated manifests
- Look for `# TODO` markers — that's where you write YAML content
- Each lab has 2 TODOs with clear requirements
- Generated YAML files appear in `/tmp/k8s-lab-XX/` directories
- Compare your work with `solutions/` when done

## What Gets Generated

Each lab creates real Kubernetes YAML manifests you can inspect and deploy:
- `pod.yaml` — Pod definitions
- `deployment.yaml` — Deployment with replicas, strategy, probes
- `service.yaml` — Service (ClusterIP, NodePort, LoadBalancer)
- `configmap.yaml` — Non-sensitive configuration
- `secret.yaml` — Sensitive data (base64-encoded)
- `pvc.yaml` — PersistentVolumeClaim for storage

## Estimated Time

~60-75 minutes for all labs (including the challenge)
