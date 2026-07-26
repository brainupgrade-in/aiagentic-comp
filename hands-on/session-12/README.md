# Session 12: AI-Specific Observability with LangFuse — Hands-on Labs

## Prerequisites

- Setup complete (`source scripts/setup.sh` — installs everything for all 5 days)
- Labs 01-08 need no infrastructure — they generate config files and validate code patterns
- **Lab 09 needs your own LangFuse Cloud keys** — self-register at
  [cloud.langfuse.com](https://cloud.langfuse.com) and put `LANGFUSE_PUBLIC_KEY`,
  `LANGFUSE_SECRET_KEY`, `LANGFUSE_HOST` in `.env`. It also calls Groq.

```bash
bash scripts/setup.sh --verify
```

> **SDK version:** these labs teach the **langfuse v4** API
> (`langfuse.langchain.CallbackHandler`, `create_trace_id` + `trace_context`,
> `create_score`, `start_as_current_observation`, `api.trace.list`).
> The v2 API (`langfuse.callback`, `langfuse.score()`, `handler.get_trace_id()`,
> `langfuse.trace()`, `fetch_traces()`) no longer exists in the installed SDK.

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
| 09 | **Production Integration** | FastAPI + LangGraph + LangFuse (Session 11 + 12) | **Yes** — LangFuse Cloud keys + Groq |

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

- Labs 01-08 work WITHOUT any running services (they use MockLangfuse); Lab 09 sends real traces to LangFuse Cloud
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
