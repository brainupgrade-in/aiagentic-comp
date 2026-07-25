# Session 10: Observability Fundamentals — Hands-on Labs

## Prerequisites

- Setup complete (`source scripts/setup.sh` — installs everything for all 5 days)
- No infrastructure needed — labs generate config files and validate YAML

```bash
bash scripts/setup.sh --verify
```

## Labs Overview

| Lab | Topic | What You'll Learn | Needs Infra? |
|-----|-------|-------------------|--------------|
| 01 | Three Pillars | Metrics, Logs, Traces — when to use which | No |
| 02 | Metric Types | Counter, Gauge, Histogram, Summary | No |
| 03 | Structured Logging | JSON logs, trace_id correlation, AI log fields | No |
| 04 | Distributed Traces | Trace/span hierarchy, AI trace patterns | No |
| 05 | OpenTelemetry Setup | TracerProvider, exporters, OTel Collector config | No |
| 06 | Instrumentation | Auto vs manual instrumentation, custom spans | No |
| 07 | OTel Collector | Collector config, Python OTel pipeline, LangFuse Integration | No |
| 08 | **Challenge** | Complete observability stack: Python OTel + Agent + design | No |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-10/
├── lab01_three_pillars.ipynb                ← Start here
├── lab02_metric_types.ipynb
├── lab03_structured_logging.ipynb
├── lab04_distributed_traces.ipynb
├── lab05_otel_setup.ipynb
├── lab06_instrumentation.ipynb
├── lab07_otel_collector.ipynb
├── lab08_challenge.ipynb
└── solutions/                               ← Completed versions
    ├── lab01_three_pillars.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the kernel: **Python 3 (Gheware Agentic AI)**
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- All 8 labs work WITHOUT any running services
- **Read the markdown cells** — they explain observability concepts step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- Labs 01-04 cover observability concepts
- Labs 05-07 cover OpenTelemetry implementation
- Lab 08 is the challenge combining all concepts
- Generated files appear in `/tmp/k8s-lab-10-XX/` directories
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck

## Estimated Time

~60-75 minutes for all labs (including the challenge)
