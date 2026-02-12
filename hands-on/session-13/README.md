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

```bash
cd hands-on/session-13

# Run a lab
python lab01_mcp_architecture.py

# Check the solution
python solutions/lab01_mcp_architecture.py
```

## Tips

- Look for `# TODO` markers -- that's where you write code
- Labs 01-03 cover MCP architecture and enterprise use cases
- Labs 04-06 cover consuming MCP (config, workflows, LangChain bridge)
- Lab 07 covers security and governance
- Lab 08 is the comprehensive challenge combining all concepts
- Generated files appear in `/tmp/aidev-lab-13-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
