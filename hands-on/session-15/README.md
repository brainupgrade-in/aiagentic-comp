# Session 15: AI-Specific Observability with LangFuse — Hands-on Labs

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
| 01 | LangFuse Fundamentals | Architecture, trace hierarchy, tool comparison | No |
| 02 | LangFuse Setup | Docker Compose deployment, environment variables | No |
| 03 | LangChain Integration | CallbackHandler, RAG tracing, handler config | No |
| 04 | Tracing Agents | Multi-step traces, bottleneck analysis, debugging | No |
| 05 | Feedback & Evaluation | User scores, automated eval, quality tracking | No |
| 06 | Prompt Management | Version control, runtime fetching, A/B testing | No |
| 07 | Cost & Token Analysis | Cost tracking, Prometheus bridge, dashboard PromQL | No |
| 08 | **Challenge** | Complete pipeline: instrumentation + bridge + alerts | No |

## How to Run

```bash
cd hands-on/session-15

# Run a lab
python lab01_langfuse_fundamentals.py

# Check the solution
python solutions/lab01_langfuse_fundamentals.py
```

## Tips

- All 8 labs work WITHOUT a Kubernetes cluster
- Look for `# TODO` markers — that's where you write code or YAML
- Labs 01-03 cover LangFuse setup and LangChain integration
- Labs 04-06 cover tracing, feedback, and prompt management
- Lab 07 covers cost analysis with Prometheus bridge
- Lab 08 is the challenge combining all concepts
- Generated files appear in `/tmp/k8s-lab-15-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
