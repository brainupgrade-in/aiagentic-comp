# Session 14: AI Safety & Guardrails -- Hands-on Labs

## Prerequisites

- Python 3.10+ installed
- No external packages needed -- these labs use only the Python standard library
- Completion of Sessions 1-13

```bash
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Prompt Injection Detection | Direct/indirect injection, detection patterns, classification |
| 02 | Output Validation | Schema validation, PII detection (email/phone/SSN/CC), content filtering |
| 03 | Jailbreak Resistance | DAN/roleplay/encoding jailbreaks, defense layers, system prompt hardening |
| 04 | Input Sanitization | Length checks, encoding normalization, content policy, sanitization pipeline |
| 05 | Safety Monitoring | Safety metrics (counters/gauges), alert thresholds, dashboard config |
| 06 | Guardrails Integration | Pre-guard/post-guard pipeline, topic restriction, format guards |
| 07 | Red Team Testing | Attack categories, test matrix, defense scoring, red team reports |
| 08 | **Comprehensive Safety Challenge** | Full safety layer combining all patterns (scored across all categories) |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-14/
├── lab01_prompt_injection_detection.ipynb    ← Start here
├── lab02_output_validation.ipynb
├── lab03_jailbreak_resistance.ipynb
├── lab04_input_sanitization.ipynb
├── lab05_safety_monitoring.ipynb
├── lab06_guardrails_integration.ipynb
├── lab07_red_team_testing.ipynb
├── lab08_challenge.ipynb
└── solutions/                              ← Completed versions
    ├── lab01_prompt_injection_detection.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the Python kernel (`~/.venv/bin/python`)
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- Labs 01-03 cover attack detection (injection, validation, jailbreaks)
- Labs 04-06 cover defense mechanisms (sanitization, monitoring, guardrails)
- Lab 07 covers red team testing methodology
- Lab 08 is the comprehensive challenge integrating all safety patterns
- **Read the markdown cells** — they explain safety concepts step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- Generated files appear in `/tmp/safety-lab-14-XX/` directories
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck

## Estimated Time

~60-75 minutes for all labs (including the challenge)
