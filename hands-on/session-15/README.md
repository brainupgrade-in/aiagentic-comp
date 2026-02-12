# Session 15: Capstone Project -- Hands-on Labs

## Prerequisites

- Python 3.10+ installed
- No external packages needed -- these labs use only the Python standard library
- Completion of Sessions 1-14

```bash
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Capstone Architecture Design | System components, data flows, startup order, monitoring points |
| 02 | Build MCP Server with Tools | Tool schemas, resource URIs, server specification |
| 03 | Create FastAPI Endpoint | Health checks, API endpoints, response models, error handling |
| 04 | Add LangFuse Instrumentation | Callback handler, trace hierarchy, cost tracking |
| 05 | Health Probes & Monitoring | K8s probes, Prometheus scrape config, metric definitions |
| 06 | Production Deployment Config | Deployment, Service, HPA, Secret YAML specs |
| 07 | Testing & Validation | Unit/integration/load tests, SLA targets, test coverage |
| 08 | **Final Integration Challenge** | Complete production readiness report (scored across all categories) |

## How to Run

```bash
cd hands-on/session-15

# Run a lab (fill in the TODO sections)
python lab01_capstone_architecture.py

# Check the solution (all checks pass)
python solutions/lab01_capstone_architecture.py
```

## Tips

- This is a comprehensive capstone integrating all 5 days of the course
- Labs build on each other -- complete them in order
- Labs 01-02 cover architecture and MCP design
- Labs 03-04 cover API and observability code
- Labs 05-06 cover Kubernetes deployment configuration
- Lab 07 covers testing strategy and SLA targets
- Lab 08 is the final integration challenge (scored across all categories)
- Generated files appear in `/tmp/capstone-lab-15-XX/` directories
- Compare your work with `solutions/` when done
- Use 2 time slots for this session (Slots C+D on Day 5)

## Estimated Time

~90-120 minutes for all labs (2 time slots)
