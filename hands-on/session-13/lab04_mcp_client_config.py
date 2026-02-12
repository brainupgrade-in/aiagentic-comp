#!/usr/bin/env python3
"""
Lab 04: MCP Client Configuration

Build MCP client config JSON, create multi-server configurations,
implement a config validator, and design role-based configurations.

No external packages required — standard library only.
"""

import os
import json
import shutil
from typing import Dict, List, Any, Tuple

WORKDIR = "/tmp/aidev-lab-13-04"

# ── Cleanup & Setup ──────────────────────────────────────────────────────────
if os.path.exists(WORKDIR):
    shutil.rmtree(WORKDIR)
os.makedirs(WORKDIR, exist_ok=True)

score = 0
total = 0

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STEP 1 — MCP Client Configuration Format                                  ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("STEP 1: MCP Client Configuration Format")
print("=" * 70)
print()
print("  MCP clients (Claude Desktop, Claude Code) use JSON config files:")
print()
print('  {')
print('    "mcpServers": {')
print('      "server-name": {')
print('        "command": "npx",              // stdio transport')
print('        "args": ["-y", "package-name"],')
print('        "env": {"KEY": "value"}        // optional env vars')
print('      },')
print('      "remote-server": {')
print('        "url": "https://host/sse"      // SSE transport')
print('      }')
print('    }')
print('  }')
print()
print("  Two transport types:")
print("    stdio: command + args (local subprocess)")
print("    sse:   url (remote HTTP)")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 1 — Build a Single-Server Config                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 1: Build a single MCP server configuration")
print("=" * 70)
print()

# TODO: Create a config dict for a Postgres MCP server.
# The config should follow this format:
#   {
#       "mcpServers": {
#           "postgres": {
#               "command": "npx",
#               "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/mydb"],
#               "env": {"POSTGRES_READ_ONLY": "true"}
#           }
#       }
#   }

single_config = "___"  # Replace with the config dict

# ── Validate TODO 1 ─────────────────────────────────────────────────────────
total += 1
try:
    checks = [
        isinstance(single_config, dict),
        "mcpServers" in single_config,
        "postgres" in single_config.get("mcpServers", {}),
        single_config["mcpServers"]["postgres"].get("command") == "npx",
        len(single_config["mcpServers"]["postgres"].get("args", [])) == 3,
        "server-postgres" in single_config["mcpServers"]["postgres"]["args"][1],
        single_config["mcpServers"]["postgres"].get("env", {}).get("POSTGRES_READ_ONLY") == "true",
    ]
    if all(checks):
        score += 1
        print("[PASS] Single-server config is correct")
        out_path = os.path.join(WORKDIR, "single_config.json")
        with open(out_path, "w") as f:
            json.dump(single_config, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Config checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Config error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 2 — Build a Multi-Server Config                                      ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 2: Build a multi-server MCP configuration")
print("=" * 70)
print()

# TODO: Create a config with 3 MCP servers:
#
# {
#     "mcpServers": {
#         "postgres": {
#             "command": "npx",
#             "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://localhost:5432/mydb"]
#         },
#         "github": {
#             "command": "npx",
#             "args": ["-y", "@modelcontextprotocol/server-github"],
#             "env": {"GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"}
#         },
#         "confluence": {
#             "url": "https://mcp-gateway.internal/confluence/sse"
#         }
#     }
# }

multi_config = "___"  # Replace with the config dict

# ── Validate TODO 2 ─────────────────────────────────────────────────────────
total += 1
try:
    servers = multi_config.get("mcpServers", {}) if isinstance(multi_config, dict) else {}
    checks = [
        isinstance(multi_config, dict),
        len(servers) == 3,
        "postgres" in servers,
        "github" in servers,
        "confluence" in servers,
        servers.get("postgres", {}).get("command") == "npx",
        servers.get("github", {}).get("env", {}).get("GITHUB_TOKEN") == "ghp_xxxxxxxxxxxx",
        servers.get("confluence", {}).get("url") == "https://mcp-gateway.internal/confluence/sse",
        "command" not in servers.get("confluence", {}),  # SSE has url, not command
    ]
    if all(checks):
        score += 1
        print("[PASS] Multi-server config is correct:")
        for name, cfg in servers.items():
            transport = "stdio" if "command" in cfg else "sse"
            print(f"       {name:12s} ({transport})")
        out_path = os.path.join(WORKDIR, "multi_config.json")
        with open(out_path, "w") as f:
            json.dump(multi_config, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Multi-config checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Config error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 3 — Implement a Config Validator                                     ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 3: Implement an MCP config validator")
print("=" * 70)
print()

def validate_mcp_config(config: Dict) -> Tuple[bool, List[str]]:
    """Validate an MCP client configuration.

    Rules:
        1. Config must have "mcpServers" key (dict)
        2. Each server must have either "command" (str) or "url" (str), not both
        3. If "command" is present, "args" must be a list
        4. If "env" is present, it must be a dict with string values

    Args:
        config: The MCP config dict to validate

    Returns:
        Tuple of (is_valid: bool, errors: list of error strings)
    """
    # TODO: Implement the validator.
    #
    # Hint:
    #   errors = []
    #   if "mcpServers" not in config or not isinstance(config.get("mcpServers"), dict):
    #       errors.append("Missing or invalid 'mcpServers' key")
    #       return (False, errors)
    #
    #   for name, server in config["mcpServers"].items():
    #       has_command = "command" in server
    #       has_url = "url" in server
    #       if has_command and has_url:
    #           errors.append(f"Server '{name}': cannot have both 'command' and 'url'")
    #       elif not has_command and not has_url:
    #           errors.append(f"Server '{name}': must have 'command' or 'url'")
    #       if has_command and not isinstance(server.get("command"), str):
    #           errors.append(f"Server '{name}': 'command' must be a string")
    #       if has_command and not isinstance(server.get("args", []), list):
    #           errors.append(f"Server '{name}': 'args' must be a list")
    #       if has_url and not isinstance(server.get("url"), str):
    #           errors.append(f"Server '{name}': 'url' must be a string")
    #       if "env" in server:
    #           if not isinstance(server["env"], dict):
    #               errors.append(f"Server '{name}': 'env' must be a dict")
    #           else:
    #               for k, v in server["env"].items():
    #                   if not isinstance(v, str):
    #                       errors.append(f"Server '{name}': env['{k}'] must be a string")
    #   return (len(errors) == 0, errors)

    return "___"  # Replace with your implementation

# Test cases
test_configs = [
    # Valid config
    {
        "mcpServers": {
            "pg": {"command": "npx", "args": ["-y", "server-postgres"]},
        }
    },
    # Invalid: missing mcpServers
    {"servers": {}},
    # Invalid: has both command and url
    {
        "mcpServers": {
            "bad": {"command": "npx", "args": [], "url": "http://x"},
        }
    },
    # Invalid: env value not string
    {
        "mcpServers": {
            "bad_env": {"command": "npx", "args": [], "env": {"KEY": 123}},
        }
    },
]

# ── Validate TODO 3 ─────────────────────────────────────────────────────────
total += 1
try:
    results = [validate_mcp_config(c) for c in test_configs]
    checks = [
        results[0][0] is True and len(results[0][1]) == 0,  # valid
        results[1][0] is False,                              # missing mcpServers
        results[2][0] is False,                              # both command and url
        results[3][0] is False,                              # env value not string
    ]
    if all(checks):
        score += 1
        print("[PASS] Config validator works correctly:")
        labels = ["Valid config", "Missing mcpServers", "Both command+url", "Bad env value"]
        for label, (valid, errors) in zip(labels, results):
            status = "VALID" if valid else f"INVALID ({len(errors)} error(s))"
            print(f"       {label:22s} → {status}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Validator checks failed at indices: {failed}")
        for i, (valid, errors) in enumerate(results):
            print(f"       Config {i}: valid={valid}, errors={errors}")
except Exception as e:
    print(f"[FAIL] Validator error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  TODO 4 — Role-Based Configuration                                        ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print("TODO 4: Generate role-based MCP configurations")
print("=" * 70)
print()

# Available servers:
all_servers = {
    "postgres":   {"command": "npx", "args": ["-y", "server-postgres", "postgresql://db:5432/prod"]},
    "github":     {"command": "npx", "args": ["-y", "server-github"], "env": {"GITHUB_TOKEN": "ghp_xxx"}},
    "slack":      {"command": "npx", "args": ["-y", "server-slack"], "env": {"SLACK_TOKEN": "xoxb-xxx"}},
    "confluence": {"url": "https://mcp-gw.internal/confluence/sse"},
    "salesforce": {"url": "https://mcp-gw.internal/salesforce/sse"},
}

# Role-to-server mapping:
role_permissions = {
    "analyst":   ["postgres", "confluence"],
    "developer": ["postgres", "github", "slack"],
    "admin":     ["postgres", "github", "slack", "confluence", "salesforce"],
}

# TODO: Write a function that generates a config for a given role.
#
# def generate_role_config(role: str) -> Dict:
#     servers = role_permissions.get(role, [])
#     return {
#         "mcpServers": {
#             name: all_servers[name]
#             for name in servers
#             if name in all_servers
#         }
#     }

def generate_role_config(role: str) -> Dict:
    """Generate an MCP config for a specific role."""
    return "___"  # Replace with your implementation

# ── Validate TODO 4 ─────────────────────────────────────────────────────────
total += 1
try:
    analyst_cfg = generate_role_config("analyst")
    dev_cfg = generate_role_config("developer")
    admin_cfg = generate_role_config("admin")
    checks = [
        isinstance(analyst_cfg, dict),
        len(analyst_cfg.get("mcpServers", {})) == 2,
        "postgres" in analyst_cfg.get("mcpServers", {}),
        "confluence" in analyst_cfg.get("mcpServers", {}),
        len(dev_cfg.get("mcpServers", {})) == 3,
        "github" in dev_cfg.get("mcpServers", {}),
        len(admin_cfg.get("mcpServers", {})) == 5,
        "salesforce" in admin_cfg.get("mcpServers", {}),
    ]
    if all(checks):
        score += 1
        print("[PASS] Role-based configs generated correctly:")
        for role in ["analyst", "developer", "admin"]:
            cfg = generate_role_config(role)
            print(f"       {role:10s} → {list(cfg['mcpServers'].keys())}")
        out_path = os.path.join(WORKDIR, "role_configs.json")
        with open(out_path, "w") as f:
            json.dump({
                "analyst": analyst_cfg,
                "developer": dev_cfg,
                "admin": admin_cfg,
            }, f, indent=2)
        print(f"       Saved to {out_path}")
    else:
        failed = [i for i, c in enumerate(checks) if not c]
        print(f"[FAIL] Role config checks failed at indices: {failed}")
except Exception as e:
    print(f"[FAIL] Role config error: {e}")
print()

# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  RESULTS                                                                    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

print("=" * 70)
print(f"Lab 04 Score: {score}/{total}")
print("=" * 70)
