# Session 13: Observability Fundamentals — Hands-on Labs

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
| 01 | Three Pillars | Metrics, Logs, Traces — when to use which | No |
| 02 | Metric Types | Counter, Gauge, Histogram, Summary | No |
| 03 | Structured Logging | JSON logs, trace_id correlation, AI log fields | No |
| 04 | Distributed Traces | Trace/span hierarchy, AI trace patterns | No |
| 05 | OpenTelemetry Setup | TracerProvider, exporters, OTel Collector config | No |
| 06 | Instrumentation | Auto vs manual instrumentation, custom spans | No |
| 07 | OTel Collector | Collector deployment, K8s integration | No |
| 08 | **Challenge** | Complete observability stack: Collector + Agent + design | No |

## How to Run

```bash
cd hands-on/session-13

# Run a lab
python lab01_three_pillars.py

# Check the solution
python solutions/lab01_three_pillars.py
```

## Tips

- All 8 labs work WITHOUT a Kubernetes cluster
- Look for `# TODO` markers — that's where you write code or YAML
- Labs 01-04 cover observability concepts
- Labs 05-07 cover OpenTelemetry implementation
- Lab 08 is the challenge combining all concepts
- Generated files appear in `/tmp/k8s-lab-13-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
