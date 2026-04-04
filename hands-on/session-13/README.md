# Session 13: Model Context Protocol (MCP) -- Hands-on Labs

## Prerequisites

- Python 3.10+ installed
- No external packages needed -- these labs simulate MCP concepts using standard library

```bash
python --version  # 3.10+
```

## Labs Overview

| Lab | Topic | What You'll Learn |
|-----|-------|-------------------|
| 01 | MCP Architecture | Protocol fundamentals, primitives, N+M math, JSON-RPC methods |
| 02 | Enterprise Use Cases | Map business functions to MCP servers, ROI calculation, prioritization |
| 03 | Ecosystem Discovery | Catalog MCP servers, match to enterprise needs, readiness scoring |
| 04 | MCP Client Config | Build config JSON, multi-server config, validator, role-based configs |
| 05 | MCP Client Workflows | Mock client lifecycle, enterprise workflow, tool routing |
| 06 | LangChain Bridge | MCP-to-LangChain adapter, multi-tool bridge, agent tool selection |
| 07 | Security & Governance | Input validation, RBAC access control, audit logger |
| 08 | **Challenge** | Full enterprise agent: catalog + config + security + workflow + audit |

## How to Run

Labs are Jupyter notebooks (`.ipynb`). Open them in **VS Code** (built-in Jupyter support) or any Jupyter-compatible tool.

```
hands-on/session-13/
├── lab01_mcp_architecture.ipynb             ← Start here
├── lab02_enterprise_use_cases.ipynb
├── lab03_ecosystem_discovery.ipynb
├── lab04_mcp_client_config.ipynb
├── lab05_mcp_client_workflows.ipynb
├── lab06_langchain_bridge.ipynb
├── lab07_security_governance.ipynb
├── lab08_challenge.ipynb
└── solutions/                              ← Completed versions
    ├── lab01_mcp_architecture.ipynb
    ├── ...
    └── lab08_challenge.ipynb
```

1. Open the notebook in VS Code
2. Select the kernel: **Python 3 (Gheware Agentic AI)**
3. Run cells one at a time with **Shift+Enter**
4. Fill in the TODO sections, then compare with `solutions/`

## Tips

- Labs 01-03 cover MCP architecture and enterprise use cases
- Labs 04-06 cover consuming MCP (config, workflows, LangChain bridge)
- Lab 07 covers security and governance
- Lab 08 is the comprehensive challenge combining all concepts
- **Read the markdown cells** — they explain MCP concepts step by step
- **Look for `# TODO` markers and `"___"` placeholders** — that's where you write code
- **Run frequently** — don't wait until you've written everything; run after each TODO
- Generated files appear in `/tmp/aidev-lab-13-XX/` directories
- **Compare with solutions** — solutions are in the `solutions/` folder if you get stuck

## Estimated Time

~60-75 minutes for all labs (including the challenge)
