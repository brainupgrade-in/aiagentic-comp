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
| 01 | MCP Fundamentals | Resource/Tool/Prompt class models, MCP architecture |
| 02 | MCP Protocol | JSON-RPC 2.0 messages, request/response validation |
| 03 | MCP Server Skeleton | Generate complete MCP server file from templates |
| 04 | MCP Tool Implementation | Typed tool functions: file_search, code_metrics |
| 05 | MCP Resources | Static + dynamic resources, URI templates |
| 06 | MCP Transport | stdio encoding/decoding, SSE event formatting |
| 07 | MCP Client | Client discovery + multi-step tool workflow |
| 08 | **Challenge** | Complete MCP server (3 tools, 2 resources, 1 prompt) + client |

## How to Run

```bash
cd hands-on/session-13

# Run a lab
python lab01_mcp_fundamentals.py

# Check the solution
python solutions/lab01_mcp_fundamentals.py
```

## Tips

- Look for `# TODO` markers -- that's where you write code
- Labs 01-03 cover MCP architecture and protocol
- Labs 04-06 cover building MCP primitives
- Lab 07 covers the client side
- Lab 08 is the comprehensive challenge
- Generated files appear in `/tmp/aidev-lab-13-XX/` directories
- Compare your work with `solutions/` when done

## Estimated Time

~60-75 minutes for all labs (including the challenge)
