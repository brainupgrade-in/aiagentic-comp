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

```bash
cd hands-on/session-14

# Run a lab (fill in the TODO sections)
python lab01_prompt_injection_detection.py

# Check the solution (all checks pass)
python solutions/lab01_prompt_injection_detection.py
```

## Tips

- Look for `# TODO` markers -- that's where you write code
- Labs 01-03 cover attack detection (injection, validation, jailbreaks)
- Labs 04-06 cover defense mechanisms (sanitization, monitoring, guardrails)
- Lab 07 covers red team testing methodology
- Lab 08 is the comprehensive challenge integrating all safety patterns
- Generated files appear in `/tmp/safety-lab-14-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
