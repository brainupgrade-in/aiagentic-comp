# Session 13: Kubernetes Operations — Hands-on Labs

## Prerequisites

- Session 11 & 12 completed (K8s fundamentals, networking, storage)
- Python 3.10+ installed
- No Kubernetes cluster needed — labs generate and validate YAML files

```bash
# No pip packages needed — these labs generate K8s manifests
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs K8s? |
|-----|-------|-------------------|------------|
| 01 | Debug Toolkit | kubectl debug commands, investigation workflow | No |
| 02 | Pod Status Diagnosis | Running, Pending, CrashLoopBackOff, OOMKilled status meanings | No |
| 03 | CrashLoopBackOff | Backoff pattern, common causes, fixing broken deployments | No |
| 04 | Resource Debugging | OOMKilled diagnosis, Pending pods, resource fix strategies | No |
| 05 | HPA Tuning | Stabilization windows, anti-patterns, production HPA config | No |
| 06 | Pod Disruption Budgets | Voluntary disruptions, minAvailable vs maxUnavailable | No |
| 07 | Production Readiness | Reliability/scalability/observability/security checklist | No |
| 08 | **Challenge** | Diagnose 4 broken pods + build complete HA configuration | Optional |

## How to Run

```bash
cd hands-on/session-13

# Run a lab (generates YAML files in /tmp/k8s-lab-13-XX/)
python lab01_debug_toolkit.py

# Check the solution
python solutions/lab01_debug_toolkit.py

# If kubectl is available, lab 08 YAML can be applied:
python solutions/lab08_challenge.py
# Then: cd /tmp/k8s-lab-13-08 && kubectl apply -f .
```

## Tips

- All 8 labs work WITHOUT a Kubernetes cluster — they generate and validate YAML
- If kubectl is available, you can apply the generated manifests
- Look for `# TODO` markers — that's where you write code or YAML content
- Labs 01-04 cover Debugging & Troubleshooting
- Labs 05-07 cover Scaling & High Availability
- Lab 08 combines both topics in a challenge
- Generated YAML files appear in `/tmp/k8s-lab-13-XX/` directories
- Compare your work with `solutions/` when done

## What Gets Generated

Each lab creates reference files and Kubernetes YAML manifests:
- `debug-cheatsheet.md` — kubectl debug command reference
- `pod-status-reference.txt` — Pod status quick-reference table
- `hpa.yaml` — Horizontal Pod Autoscaler configuration
- `agent-pdb.yaml` — Pod Disruption Budget
- `ha-deployment.yaml` — High-availability Deployment
- `fixed-deployment.yaml` — Fixed CrashLoopBackOff Deployment
- `production-deployment-reference.yaml` — Production-ready Deployment template

## Estimated Time

~60-75 minutes for all labs (including the challenge)
