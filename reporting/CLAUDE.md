# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This directory contains reporting tools for the Agentic AI course — specifically for tracking lab submission progress across 15 sessions and 119 labs. Data comes from GitHub Issues (label: `lab-tracking`) in `brainupgrade-in/aiagentic-comp`. Participants submit via `scripts/submit-lab.sh`, which posts structured comments to per-lab issues.

## Commands

```bash
# Generate HTML dashboard (reads ~/.rajesh/.github_bu or $GITHUB_TOKEN automatically)
python3 generate-dashboard.py --output dashboard.html

# Generate with auto-refresh (browser reloads every 60s)
python3 generate-dashboard.py --output dashboard.html --auto-refresh

# Filter to one session only
python3 generate-dashboard.py --session 3

# Shell wrapper (archives previous dashboard, activates venv if present)
./update-dashboard.sh [--auto-refresh] [--open]

# Live server (http://localhost:8888) with on-demand refresh via /refresh or /refresh/session/N
python3 server.py

# Text-only completion report (saved to /tmp/lab-completion-comments.md)
python3 track-lab-comments.py [--session N] [--participant username]
```

## Architecture

**Data flow:** GitHub Issues API → parse issue comments → build completion matrix → render HTML/text.

- `generate-dashboard.py` — main entry point; fetches issues in parallel (`ThreadPoolExecutor`), builds a `completion_matrix[participant][session][lab]` dict, then renders a self-contained HTML file (all CSS/JS inline). Caches results to `.completion_cache.json` to reduce API calls on repeated runs.
- `track-lab-comments.py` — same GitHub fetch logic but outputs Markdown tables to stdout/file instead of HTML.
- `server.py` — minimal `http.server` wrapper that serves `dashboard.html` and triggers `generate-dashboard.py` subprocess on `/refresh` or `/refresh/session/N` GET requests. No external dependencies.
- `update-dashboard.sh` — convenience wrapper: loads token, archives old `dashboard.html` to `archive/`, runs `generate-dashboard.py`, optionally opens browser.

## Key Constants

`COURSE_STRUCTURE` dict (in both `generate-dashboard.py` and `track-lab-comments.py`) maps session number → `(title, num_labs)`. Total: 119 labs across 15 sessions. Keep both files in sync if the course structure changes.

## GitHub Auth

Token is read from `$GITHUB_TOKEN` env var or `~/.rajesh/.github_bu` file (read-only access to issues is sufficient). `generate-dashboard.py` auto-detects the file; `track-lab-comments.py` only reads `$GITHUB_TOKEN`.

## Completion Comment Format

`is_completion_comment()` matches comments containing `✅ completed`, `completed ✅`, `[x] done`, or `all checks passed` (case-insensitive). Participant name is extracted from `**Participant:** Name (email)` pattern in the comment body; falls back to GitHub username.

Issue titles must follow the format `Session N - Lab MM` (e.g. `Session 3 - Lab 07`) for `parse_issue_title()` to extract session/lab numbers correctly.

## Output Files

- `dashboard.html` — current dashboard (overwritten each run)
- `dashboard-live.html` — alias used during live course delivery
- `archive/` — timestamped snapshots created by `update-dashboard.sh`
- `.completion_cache.json` — API response cache (gitignored)

## Dependencies

`requests` library — installed via `../requirements.txt`. Python 3.12+. No other external deps (`server.py` uses stdlib only).

## Troubleshooting

```bash
# Verify lab-tracking issues exist
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/brainupgrade-in/aiagentic-comp/issues?labels=lab-tracking&per_page=5" \
  | python3 -c "import json,sys; [print(i['number'], i['title']) for i in json.load(sys.stdin)]"

# Dashboard shows no data: check GITHUB_TOKEN has read access to issues
# track-lab-comments.py reads $GITHUB_TOKEN (env var or .env file)
```
