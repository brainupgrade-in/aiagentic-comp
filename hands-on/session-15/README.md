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
| 05 | Health Probes & Monitoring | Python async HealthChecker, LangFuse monitoring, metric definitions |
| 06 | Production Deployment Config | Python process management, uvicorn config, psutil monitoring, dotenv |
| 07 | Testing & Validation | Unit/integration/load tests, SLA targets, test coverage |
| 08 | **Final Integration Challenge** | Complete production readiness report (scored across all categories) |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-15/
├── lab01_capstone_architecture.ipynb    ← Start here
├── lab02_mcp_server_tools.ipynb
├── lab03_fastapi_endpoint.ipynb
├── lab04_langfuse_instrumentation.ipynb
├── lab05_health_probes_monitoring.ipynb
├── lab06_production_deployment.ipynb
├── lab07_testing_validation.ipynb
├── lab08_challenge.ipynb
└── solutions/                           ← Completed versions
    ├── lab01_capstone_architecture.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the kernel: **Python 3 (Gheware Agentic AI)**
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- This is a comprehensive capstone integrating all 5 days of the course
- Labs build on each other -- complete them in order
- Labs 01-02 cover architecture and MCP design
- Labs 03-04 cover API and observability code
- Labs 05-06 cover Python process management and deployment configuration
- Lab 07 covers testing strategy and SLA targets
- Lab 08 is the final integration challenge (scored across all categories)
- Generated files appear in `/tmp/capstone-lab-15-XX/` directories
- Compare your work with `solutions/` when done
- Use 2 time slots for this session (Slots C+D on Day 5)

## Estimated Time

~90-120 minutes for all labs (2 time slots)
