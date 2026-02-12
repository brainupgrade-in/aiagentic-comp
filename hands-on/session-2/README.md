# Session 2: AI Coding Agents & Vibe Coding — Hands-on Labs

## Prerequisites

- Python 3.10+ installed
- No external packages needed — these labs use only the Python standard library

```bash
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Coding Agent Anatomy | Agent loop model: plan/code/test, tool registry |
| 02 | Tool Calling Patterns | File R/W/search tools, tool dispatcher, multi-step chains |
| 03 | Context Management | Token budgeting, priority file selector, CLAUDE.md generation |
| 04 | Prompt Engineering for Code | Vague vs precise prompts, structured prompt templates |
| 05 | Vibe Coding Simulation | NL parser → file structure → pseudo-code generation |
| 06 | Agent Comparison | Feature scoring for OpenCode/Claude Code/Copilot/Cursor |
| 07 | Code Review Basics | AST-based issue detection, structured review report |
| 08 | **Challenge** | End-to-end coding agent simulation |

## How to Run

```bash
cd hands-on/session-2

# Run a lab
python lab01_coding_agent_anatomy.py

# Check the solution
python solutions/lab01_coding_agent_anatomy.py
```

## Tips

- Look for `# TODO` markers — that's where you write code
- Labs 01-03 cover agent internals
- Labs 04-06 cover prompt engineering and vibe coding
- Lab 07 covers code review
- Lab 08 is the comprehensive challenge
- Generated files appear in `/tmp/aidev-lab-02-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
