# Session 15: Prometheus & Grafana — Hands-on Labs

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
| 01 | Prometheus Basics | Pull-based architecture, text format, scrape config | No |
| 02 | Exposing Metrics | prometheus_client: Counter, Histogram, Gauge in Python | No |
| 03 | PromQL Queries | rate, sum, histogram_quantile, absent, error rate | No |
| 04 | AI-Specific Metrics | Token tracking, cost estimation, LLM metrics | No |
| 05 | Alert Rules | Alert expressions, Alertmanager routing, severity | No |
| 06 | Dashboard Design | RED/USE methods, Grafana panel types, layout | No |
| 07 | K8s Monitoring | kube-prometheus-stack, pod annotations, architecture | No |
| 08 | **Challenge** | Complete monitoring: metrics + alerts + dashboard design | No |

## How to Run

```bash
cd hands-on/session-15

# Run a lab
python lab01_prometheus_basics.py

# Check the solution
python solutions/lab01_prometheus_basics.py
```

## Tips

- All 8 labs work WITHOUT a Kubernetes cluster
- Look for `# TODO` markers — that's where you write code or YAML
- Labs 01-03 cover Prometheus fundamentals
- Labs 04-06 cover AI metrics and dashboarding
- Lab 07 covers K8s deployment
- Lab 08 is the challenge combining all concepts
- Generated files appear in `/tmp/k8s-lab-15-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
