# Session 2: AI Coding Agents & Vibe Coding — Hands-on Labs

## Prerequisites

- Setup complete (`source scripts/setup.sh` — installs everything for all 5 days)
- No external packages needed — these labs use only the Python standard library

```bash
bash scripts/setup.sh --verify
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Coding Agent Anatomy | Agent loop model: plan/code/test, tool registry |
| 02 | Tool Calling Patterns | File R/W/search tools, tool dispatcher, multi-step chains |
| 03 | Context Management | Token budgeting, priority file selector, CLAUDE.md generation |
| 04 | Prompt Engineering for Code | Vague vs precise prompts, structured prompt templates |
| 05 | Vibe Coding Simulation | NL parser → file structure → pseudo-code generation |
| 06 | Safety & Sandboxing | Command classification, allowlist/blocklist, permission escalation |
| 07 | Code Review Basics | AST-based issue detection, structured review report |
| 08 | Iterative Refinement | Quality metrics, code improvement loop, reflect-iterate cycle |
| 09 | **Challenge** | End-to-end coding agent simulation |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-2/
├── lab01_coding_agent_anatomy.ipynb     ← Start here
├── lab02_tool_calling_patterns.ipynb
├── lab03_context_management.ipynb
├── lab04_prompt_engineering_code.ipynb
├── lab05_vibe_coding_simulation.ipynb
├── lab06_safety_sandboxing.ipynb
├── lab07_code_review_basics.ipynb
├── lab08_iterative_refinement.ipynb
├── lab09_challenge.ipynb
└── solutions/                           ← Completed versions
    ├── lab01_coding_agent_anatomy.ipynb
    ├── ...
    └── lab09_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the kernel: **Python 3 (Gheware Agentic AI)**
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- Look for `# TODO` markers and `"___"` placeholders — that's where you write code
- Labs 01-03 cover agent internals
- Labs 04-05 cover prompt engineering and vibe coding
- Lab 06 covers safety & sandboxing — how agents protect your system
- Lab 07 covers AST-based code review — the foundation for automated analysis
- Lab 08 covers iterative refinement — the reflect-iterate loop (builds on Lab 07's AST skills)
- Lab 09 is the comprehensive challenge
- Generated files appear in `/tmp/aidev-lab-02-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~75-90 minutes for all labs (including the challenge)
