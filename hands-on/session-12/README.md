# Session 12: AI-Specific Observability with LangFuse — Hands-on Labs

## Prerequisites

- Setup complete (`source scripts/setup.sh` — installs everything for all 5 days)
- No infrastructure needed — labs generate config files and validate YAML

```bash
bash scripts/setup.sh --verify
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs Infra? |
|-----|-------|-------------------|--------------|
| 01 | LangFuse Fundamentals | Architecture, trace hierarchy, mock LangFuse setup | No |
| 02 | LangFuse Setup | SDK configuration, environment variables, mock mode | No |
| 03 | LangChain Integration | CallbackHandler, RAG tracing, handler config | No |
| 04 | Tracing Agents | Multi-step traces, bottleneck analysis, debugging | No |
| 05 | Feedback & Evaluation | User scores, automated eval, quality tracking | No |
| 06 | Prompt Management | Version control, runtime fetching, A/B testing | No |
| 07 | Cost & Token Analysis | Cost tracking, LangFuse cost dashboard, token analytics | No |
| 08 | **Challenge** | Complete pipeline: instrumentation + bridge + alerts | No |
| 09 | **Production Integration** | FastAPI + LangGraph + LangFuse (Session 11 + 12) | No |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-12/
├── lab01_langfuse_fundamentals.ipynb        ← Start here
├── lab02_langfuse_setup.ipynb
├── lab03_langchain_integration.ipynb
├── lab04_tracing_agents.ipynb
├── lab05_feedback_evaluation.ipynb
├── lab06_prompt_management.ipynb
├── lab07_cost_analysis.ipynb
├── lab08_challenge.ipynb
├── lab09_production_observability.ipynb     ← Production capstone
└── solutions/                               ← Completed versions
    ├── lab01_langfuse_fundamentals.ipynb
    ├── ...
    ├── lab08_challenge.ipynb
    └── lab09_production_observability.ipynb
```

1. Open the notebook in VS Code
2. Select the kernel: **Python 3 (Gheware Agentic AI)**
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- All 9 labs work WITHOUT any running services (use MockLangfuse)
- **Read the markdown cells** — they explain LangFuse concepts step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- Labs 01-03 cover LangFuse setup and LangChain integration
- Labs 04-06 cover tracing, feedback, and prompt management
- Lab 07 covers cost analysis with LangFuse API
- Lab 08 is the challenge combining all concepts
- **Lab 09 is the production capstone** — integrates Session 11 FastAPI app with LangFuse
- Generated files appear in `/tmp/ailab-12-XX/` or `/tmp/prod-lab-12-XX/` directories
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck

## Estimated Time

- Labs 01-08: ~60-75 minutes
- Lab 09 (Production Integration): ~30-40 minutes
- **Total:** ~90-115 minutes for all labs
