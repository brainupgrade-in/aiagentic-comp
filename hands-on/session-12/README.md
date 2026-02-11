# Session 12: Building Custom AI Dev Tools -- Hands-on Labs

## Prerequisites

- Python 3.10+ installed
- No external packages needed -- these labs use only the Python standard library

```bash
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | Code Quality Server | Lint + complexity analysis using ast module |
| 02 | Test Runner Server | Test execution simulation, pytest output parsing |
| 03 | Doc Generator Server | Docstring extraction + README generation |
| 04 | Review Agent State | TypedDict state design + node/edge planning |
| 05 | Review Agent Workflow | Full review workflow: analyze -> test -> review |
| 06 | Tool Registry | Register, discover, route tool calls dynamically |
| 07 | Sandboxed Execution | Restricted subprocess with timeouts + validation |
| 08 | **Challenge** | Complete AI dev tool suite: MCP + review + registry + sandbox |

## How to Run

```bash
cd hands-on/session-12

# Run a lab
python lab01_code_quality_server.py

# Check the solution
python solutions/lab01_code_quality_server.py
```

## Tips

- Look for `# TODO` markers -- that's where you write code
- Labs 01-03 cover MCP server implementations for dev workflows
- Labs 04-05 cover code review agent design
- Labs 06-07 cover tool infrastructure
- Lab 08 is the comprehensive challenge
- Generated files appear in `/tmp/aidev-lab-12-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
