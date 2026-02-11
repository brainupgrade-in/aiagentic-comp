# Session 15: Capstone & Production Readiness — Hands-on Labs

## Prerequisites

- Python 3.10+ installed
- No Kubernetes cluster needed — labs generate config files and validate YAML

```bash
# No pip packages needed — these labs generate configs and validate answers
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs K8s? |
|-----|-------|-------------------|------------|
| 01 | Production Checklist | Six categories, deployment order, resource recommendations | No |
| 02 | Health Checks & Probes | /health endpoint, readiness/liveness/startup probes | No |
| 03 | Resource & Autoscaling | Requests/limits, HPA, PodDisruptionBudget | No |
| 04 | Secrets Management | K8s Secrets, base64, secretKeyRef injection | No |
| 05 | Structured Logging | JSON logs, trace_id correlation, AI log fields | No |
| 06 | Alerting Configuration | Alert rules, severity levels, Alertmanager routing | No |
| 07 | Backup & Recovery | PVC snapshots, pg_dump, GitOps, RTO/RPO | No |
| 08 | **Challenge** | Complete production deployment: Deployment + StatefulSet + HA | No |

## How to Run

```bash
cd hands-on/session-15

# Run a lab
python lab01_production_checklist.py

# Check the solution
python solutions/lab01_production_checklist.py
```

## Tips

- All 8 labs work WITHOUT a Kubernetes cluster
- Look for `# TODO` markers — that's where you write code or YAML
- Labs 01-04 cover production fundamentals (health, resources, secrets)
- Labs 05-06 cover logging and alerting
- Lab 07 covers backup and disaster recovery
- Lab 08 is the challenge combining all concepts
- Generated files appear in `/tmp/k8s-lab-15-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
