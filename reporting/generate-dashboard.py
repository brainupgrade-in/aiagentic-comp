#!/usr/bin/env python3
"""
Lab Submission Monitoring Dashboard Generator

Generates an interactive HTML dashboard showing lab completion status.
Updates with real-time data from GitHub Issues.

Usage: python3 generate-dashboard.py [--output dashboard.html] [--auto-refresh]
"""

import os
import re
import sys
import json
import argparse
from datetime import datetime, timezone
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

REPO_OWNER = "brainupgrade-in"
REPO_NAME = "aiagentic-comp"
CACHE_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".completion_cache.json"
)

COURSE_STRUCTURE = {
    1: ("Introduction to Agentic AI", 6),
    2: ("AI Coding Assistants & Vibe Coding", 9),
    3: ("Reasoning, Planning & Tool Use", 7),
    4: ("LangChain Fundamentals", 8),
    5: ("Building RAG Applications", 8),
    6: ("LangChain Agents & Memory", 8),
    7: ("LangGraph Stateful Workflows", 8),
    8: ("Advanced LangGraph Workflows", 8),
    9: ("Multi-Agent Systems", 8),
    10: ("Observability Fundamentals", 8),
    11: ("Production Development & Deployment", 8),
    12: ("LangFuse Observability", 9),
    13: ("Model Context Protocol (MCP)", 8),
    14: ("AI Safety & Guardrails", 8),
    15: ("Capstone Project", 8),
}


def get_github_token():
    """Get GitHub token from environment or instructor PAT file."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        pat_file = os.path.expanduser("~/.rajesh/.github_bu")
        if os.path.exists(pat_file):
            with open(pat_file) as f:
                token = f.read().strip()
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        print("Set it with: export GITHUB_TOKEN='your_token'")
        sys.exit(1)
    return token


def load_cache():
    """Load cached completion matrix from disk."""
    if not os.path.exists(CACHE_FILE):
        return defaultdict(lambda: defaultdict(dict))
    with open(CACHE_FILE) as f:
        data = json.load(f)
    matrix = defaultdict(lambda: defaultdict(dict))
    for participant, sessions in data.items():
        for session_str, labs in sessions.items():
            matrix[participant][int(session_str)] = {int(k): v for k, v in labs.items()}
    return matrix


def save_cache(matrix):
    """Persist completion matrix to disk."""
    data = {}
    for participant, sessions in matrix.items():
        data[participant] = {
            str(snum): {str(lnum): v for lnum, v in labs.items()}
            for snum, labs in sessions.items()
        }
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)


def parse_since(value):
    """Convert a local YYYY-MM-DD cutoff to a UTC timestamp comparable to created_at."""
    try:
        local_midnight = datetime.strptime(value, "%Y-%m-%d").astimezone()
    except ValueError:
        print(f"Error: --since must be YYYY-MM-DD, got '{value}'")
        sys.exit(1)
    return local_midnight.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch_lab_issues(token, session=None):
    """Fetch lab tracking issues, optionally filtered to one session."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    labels = f"lab-tracking,session-{session}" if session else "lab-tracking"

    all_issues = []
    page = 1

    while True:
        params = {"state": "all", "labels": labels, "per_page": 100, "page": page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"Error fetching issues: {response.status_code}")
            sys.exit(1)

        issues = response.json()
        if not issues:
            break

        all_issues.extend(issues)
        page += 1

    return all_issues


def fetch_issue_comments(token, issue_number):
    """Fetch all comments for a specific issue (paginated)."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    all_comments = []
    page = 1

    while True:
        response = requests.get(
            url, headers=headers, params={"per_page": 100, "page": page}
        )
        if response.status_code != 200:
            return all_comments

        comments = response.json()
        if not comments:
            break

        all_comments.extend(comments)
        page += 1

    return all_comments


def parse_issue_title(title):
    """Extract session and lab number from issue title."""
    match = re.search(r"Session (\d+) - Lab (\d+)", title)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


def extract_participant_name(comment_body):
    """Extract participant name from comment body."""
    patterns = [
        r"\*\*Participant:\*\*\s+([^\(\n]+?)\s*\([^\)]+\)",
        r"\*\*Participant:\*\*\s+([^\n]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, comment_body)
        if match:
            return match.group(1).strip()
    return None


def is_completion_comment(comment_body):
    """Check if comment indicates lab completion."""
    patterns = [
        r"✅\s+completed",
        r"completed\s+✅",
        r"\[x\].*done",
        r"all checks passed",
    ]
    comment_lower = comment_body.lower()
    return any(re.search(pattern, comment_lower) for pattern in patterns)


def fetch_issue_data(token, issue, since=None):
    """Fetch and process comments for a single issue."""
    title = issue.get("title", "")
    issue_number = issue.get("number")
    session_num, lab_num = parse_issue_title(title)

    if session_num is None or lab_num is None:
        return None

    completions = []
    for comment in fetch_issue_comments(token, issue_number):
        github_author = comment.get("user", {}).get("login", "")
        body = comment.get("body", "")
        created_at = comment.get("created_at", "")

        if github_author.endswith("[bot]"):
            continue

        if since and created_at < since:
            continue

        if is_completion_comment(body):
            participant_name = extract_participant_name(body) or github_author
            completions.append(
                (participant_name, session_num, lab_num, issue_number, created_at)
            )

    return completions


def build_completion_data(token, issues, since=None):
    """Build completion data from issues and comments (parallel fetch)."""
    completion_matrix = defaultdict(lambda: defaultdict(dict))

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(fetch_issue_data, token, issue, since): issue
            for issue in issues
        }
        for future in as_completed(futures):
            result = future.result()
            if not result:
                continue
            for (
                participant_name,
                session_num,
                lab_num,
                issue_number,
                created_at,
            ) in result:
                completion_matrix[participant_name][session_num][lab_num] = {
                    "issue_number": issue_number,
                    "completed_date": created_at,
                }

    return completion_matrix


def generate_html_dashboard(completion_matrix, output_file, auto_refresh=False):
    """Generate interactive HTML dashboard — dark industrial mission-control design."""

    total_labs = sum(count for _, count in COURSE_STRUCTURE.values())
    participants = sorted(completion_matrix.keys())
    total_participants = len(participants)
    total_completions = sum(
        len([lab for labs in sessions.values() for lab in labs])
        for sessions in completion_matrix.values()
    )
    overall_progress = (
        total_completions / (total_labs * total_participants) * 100
        if total_participants > 0
        else 0
    )
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # ── Completion matrix rows ──────────────────────────────────────────────
    matrix_rows = ""
    for participant in participants:
        sessions = completion_matrix[participant]
        total_completed = sum(len(labs) for labs in sessions.values())
        pct = (total_completed / total_labs * 100) if total_labs > 0 else 0
        bar_w = int(pct)
        p_cls = (
            "s-full"
            if pct >= 90
            else "s-high"
            if pct >= 50
            else "s-low"
            if pct > 0
            else "s-none"
        )

        matrix_rows += f'<tr data-name="{participant.lower()}">\n'
        matrix_rows += f'<td class="pname">{participant}</td>\n'

        for sn in range(1, 16):
            _, num_labs = COURSE_STRUCTURE[sn]
            done = len(sessions.get(sn, {}))
            ratio = done / num_labs if num_labs else 0
            c_cls = (
                "c-full"
                if ratio >= 0.9
                else "c-high"
                if ratio >= 0.5
                else "c-low"
                if ratio > 0
                else "c-none"
            )
            matrix_rows += (
                f'<td class="cell {c_cls}" title="S{sn}: {done}/{num_labs} labs">'
                f'{done}<span class="cell-denom">/{num_labs}</span></td>\n'
            )

        matrix_rows += (
            f'<td class="total-cell"><b>{total_completed}</b>'
            f'<span class="of-t">/{total_labs}</span></td>\n'
            f'<td class="prog-cell">'
            f'<div class="prog-track"><div class="prog-fill {p_cls}" style="width:{bar_w}%"></div></div>'
            f'<span class="prog-pct {p_cls}">{pct:.0f}%</span>'
            f"</td>\n</tr>\n"
        )

    if not matrix_rows:
        matrix_rows = (
            '<tr><td colspan="18" class="empty-msg">'
            "No submissions yet — waiting for participants to submit labs"
            "</td></tr>"
        )

    # ── Session accordion cards ─────────────────────────────────────────────
    session_cards = ""
    for sn in range(1, 16):
        title, num_labs = COURSE_STRUCTURE[sn]
        sess_done = sum(len(completion_matrix[p].get(sn, {})) for p in participants)
        sess_total = num_labs * total_participants if total_participants else num_labs
        sess_pct = (sess_done / sess_total * 100) if sess_total else 0
        bar_cls = (
            "s-full"
            if sess_pct >= 90
            else "s-high"
            if sess_pct >= 50
            else "s-low"
            if sess_pct > 0
            else "s-none"
        )

        # Build per-participant dot rows
        if participants:
            dot_headers = "".join(
                f'<th class="lab-th">L{ln:02d}</th>' for ln in range(1, num_labs + 1)
            )
            dot_rows = ""
            for p in participants:
                p_sess = completion_matrix[p].get(sn, {})
                dots = "".join(
                    f'<td class="dot-cell"><span class="dot {"dot-done" if ln in p_sess else "dot-todo"}"></span></td>'
                    for ln in range(1, num_labs + 1)
                )
                dot_rows += f'<tr><td class="pname-sm">{p}</td>{dots}</tr>\n'
            dot_table = (
                f'<div class="dot-scroll"><table class="dot-table">'
                f'<thead><tr><th class="pname-th">Participant</th>{dot_headers}</tr></thead>'
                f"<tbody>{dot_rows}</tbody></table></div>"
            )
        else:
            dot_table = '<p class="no-data">No submissions for this session</p>'

        session_cards += f"""
<div class="sess-card" data-sn="{sn}" data-title="{title.lower()}">
  <div class="sess-head" onclick="toggleSess(this)">
    <span class="sess-id">S{sn:02d}</span>
    <span class="sess-name">{title}</span>
    <div class="sess-prog-wrap">
      <div class="sess-prog-track">
        <div class="sess-prog-fill {bar_cls}" style="width:{sess_pct:.1f}%"></div>
      </div>
      <span class="sess-count {bar_cls}">{sess_done}/{sess_total}</span>
    </div>
    <button class="sess-ref-btn" id="rsess-{sn}"
            onclick="event.stopPropagation();refreshSession({sn})"
            title="Refresh session {sn}">↻</button>
    <span class="sess-chevron">›</span>
  </div>
  <div class="sess-body">{dot_table}</div>
</div>"""

    # ── Full HTML ───────────────────────────────────────────────────────────
    auto_meta = '<meta http-equiv="refresh" content="60">' if auto_refresh else ""
    participants_count = total_participants
    possible = total_labs * total_participants if total_participants else 0

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Lab Tracker · Agentic AI</title>
{auto_meta}
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root {{
  --bg:           #080b10;
  --surface:      #0e1218;
  --surface-2:    #141922;
  --border:       #1a2235;
  --border-hi:    #263048;
  --text:         #c0ccdf;
  --text-muted:   #8090b0;
  --text-dim:     #3a4860;
  --accent:       #00c9a7;
  --accent-glow:  rgba(0,201,167,.15);
  --green:        #22c55e;
  --green-bg:     rgba(34,197,94,.12);
  --green-dim:    rgba(34,197,94,.06);
  --amber:        #f59e0b;
  --amber-bg:     rgba(245,158,11,.12);
  --amber-dim:    rgba(245,158,11,.06);
  --red:          #ef4444;
  --red-bg:       rgba(239,68,68,.08);
  --font-ui:      'Syne', sans-serif;
  --font-mono:    'JetBrains Mono', monospace;
  --header-h:     52px;
  --nav-h:        40px;
}}

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html {{ scroll-behavior: smooth; }}

body {{
  font-family: var(--font-ui);
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  overflow-x: hidden;
}}

/* ── HEADER ─────────────────────────────────────── */
.dash-header {{
  position: sticky;
  top: 0;
  z-index: 100;
  height: var(--header-h);
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 0;
  padding: 0 16px;
  backdrop-filter: blur(12px);
}}

.hdr-brand {{
  display: flex;
  flex-direction: column;
  padding-right: 20px;
  border-right: 1px solid var(--border);
  min-width: 0;
  flex-shrink: 0;
}}
.hdr-title {{
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent);
  line-height: 1;
  white-space: nowrap;
}}
.hdr-sub {{
  font-size: 11px;
  color: var(--text-muted);
  font-family: var(--font-mono);
  letter-spacing: 0.04em;
  margin-top: 2px;
  white-space: nowrap;
}}

.hdr-kpis {{
  display: flex;
  align-items: stretch;
  gap: 0;
  flex: 1;
  padding: 0 16px;
  overflow: hidden;
}}
.kpi {{
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 0 16px;
  border-right: 1px solid var(--border);
  min-width: 0;
}}
.kpi:first-child {{ padding-left: 8px; }}
.kpi-val {{
  font-family: var(--font-mono);
  font-size: 18px;
  font-weight: 600;
  color: var(--text);
  line-height: 1;
}}
.kpi-val.accent {{ color: var(--accent); }}
.kpi-lbl {{
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--text-muted);
  margin-top: 2px;
}}

.hdr-progress {{
  padding: 0 16px;
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 4px;
  min-width: 120px;
  flex-shrink: 0;
}}
.overall-bar-track {{
  height: 4px;
  background: var(--border-hi);
  border-radius: 2px;
  overflow: hidden;
}}
.overall-bar-fill {{
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--green));
  border-radius: 2px;
  transition: width .6s ease;
}}
.overall-pct {{
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--accent);
  font-weight: 600;
}}

.hdr-right {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding-left: 16px;
  flex-shrink: 0;
}}
.hdr-time {{
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  white-space: nowrap;
}}
.ref-btn {{
  background: transparent;
  border: 1px solid var(--border-hi);
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.06em;
  padding: 5px 12px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all .2s ease;
  white-space: nowrap;
}}
.ref-btn:hover {{
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-glow);
}}
.ref-btn:disabled {{
  opacity: .4;
  cursor: not-allowed;
}}
.ref-icon {{ display: inline-block; transition: transform .3s; }}
.ref-btn.spinning .ref-icon {{ animation: spin .7s linear infinite; }}
@keyframes spin {{ to {{ transform: rotate(360deg); }} }}

/* ── NAV ─────────────────────────────────────────── */
.dash-nav {{
  position: sticky;
  top: var(--header-h);
  z-index: 90;
  height: var(--nav-h);
  background: var(--surface-2);
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 0;
  padding: 0 16px;
}}

.nav-tabs {{
  display: flex;
  gap: 0;
  border-right: 1px solid var(--border);
  padding-right: 16px;
  flex-shrink: 0;
}}
.tab-btn {{
  background: none;
  border: none;
  color: var(--text-muted);
  font-family: var(--font-ui);
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 0 14px;
  height: var(--nav-h);
  cursor: pointer;
  border-bottom: 2px solid transparent;
  transition: all .2s ease;
  position: relative;
  top: 1px;
}}
.tab-btn:hover {{ color: var(--text); }}
.tab-btn.active {{
  color: var(--accent);
  border-bottom-color: var(--accent);
}}

.nav-filter {{
  flex: 1;
  padding: 0 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  max-width: 360px;
}}
.filter-ico {{ color: var(--text-muted); font-size: 13px; flex-shrink: 0; }}
.filter-in {{
  flex: 1;
  background: none;
  border: none;
  border-bottom: 1px solid var(--border);
  color: var(--text);
  font-family: var(--font-mono);
  font-size: 12px;
  padding: 4px 0;
  outline: none;
  transition: border-color .2s;
}}
.filter-in::placeholder {{ color: var(--text-muted); }}
.filter-in:focus {{ border-bottom-color: var(--accent); }}
.filter-clr {{
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  font-size: 12px;
  padding: 2px;
  display: none;
  transition: color .2s;
}}
.filter-clr:hover {{ color: var(--text-muted); }}
.filter-clr.show {{ display: block; }}
.filter-stat {{
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  padding-left: 8px;
  border-left: 1px solid var(--border);
  white-space: nowrap;
}}

/* ── MAIN ─────────────────────────────────────────── */
.dash-main {{ padding: 16px; }}

.view {{ display: none; }}
.view.active {{ display: block; }}

/* ── MATRIX TABLE ─────────────────────────────────── */
.matrix-scroll {{
  overflow-x: auto;
  /* overflow-x makes this the scroll container for both axes, so the sticky
     thead below is positioned against this box — cap the height here or the
     header has no room to stick and lands on top of the first rows. */
  max-height: calc(100vh - var(--header-h) - var(--nav-h) - 32px);
  border: 1px solid var(--border);
  border-radius: 6px;
  background: var(--surface);
}}

table.matrix {{
  width: 100%;
  border-collapse: collapse;
  font-family: var(--font-mono);
  font-size: 12px;
  white-space: nowrap;
}}

table.matrix thead {{
  position: sticky;
  top: 0;  /* relative to .matrix-scroll, not the page — no header/nav offset */
  z-index: 80;
}}

table.matrix th {{
  background: var(--surface-2);
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  padding: 8px 6px;
  text-align: center;
  border-bottom: 1px solid var(--border);
  border-right: 1px solid var(--border);
}}
table.matrix th:first-child {{
  text-align: left;
  padding-left: 12px;
  min-width: 140px;
  position: sticky;
  left: 0;
  z-index: 81;
  background: var(--surface-2);
}}
table.matrix th:last-child,
table.matrix th:nth-last-child(2) {{
  border-right: none;
}}

table.matrix td {{
  padding: 6px 5px;
  text-align: center;
  border-bottom: 1px solid var(--border);
  border-right: 1px solid var(--border);
  transition: background .15s;
}}
table.matrix td:first-child {{
  text-align: left;
  padding-left: 12px;
  position: sticky;
  left: 0;
  z-index: 10;
  background: var(--surface);
  border-right: 1px solid var(--border-hi);
}}
table.matrix tr:hover td {{ background: var(--surface-2); }}
table.matrix tr:hover td:first-child {{ background: var(--surface-2); }}
table.matrix td:last-child,
table.matrix td:nth-last-child(2) {{ border-right: none; }}
table.matrix tr:last-child td {{ border-bottom: none; }}

.pname {{
  font-family: var(--font-ui);
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
}}

/* Heatmap cells */
.cell {{ font-size: 12px; font-weight: 500; }}
.cell .cell-denom {{ font-size: 11px; opacity: .75; }}
.c-full  {{ background: var(--green-bg);  color: var(--green); }}
.c-high  {{ background: var(--amber-bg);  color: var(--amber); }}
.c-low   {{ background: rgba(245,158,11,.05); color: #d49b10; }}
.c-none  {{ color: var(--text-muted); }}

.total-cell {{ font-size: 13px; font-weight: 600; color: var(--text); }}
.of-t {{ font-size: 11px; opacity: .6; font-weight: 400; }}

.prog-cell {{
  display: flex;
  align-items: center;
  gap: 6px;
  padding-right: 12px !important;
  min-width: 90px;
}}
.prog-track {{
  flex: 1;
  height: 3px;
  background: var(--border-hi);
  border-radius: 2px;
  overflow: hidden;
}}
.prog-fill {{ height: 100%; border-radius: 2px; }}
.prog-pct {{ font-size: 12px; font-weight: 600; min-width: 32px; text-align: right; }}

.s-full {{ background: var(--green); color: var(--green); }}
.s-high {{ background: var(--amber); color: var(--amber); }}
.s-low  {{ background: #d49b10; color: #d49b10; }}
.s-none {{ background: var(--text-muted); color: var(--text-muted); }}

/* For prog-fill, bg is the color */
.prog-fill.s-full {{ background: var(--green); }}
.prog-fill.s-high {{ background: var(--amber); }}
.prog-fill.s-low  {{ background: #d49b10; }}
.prog-fill.s-none {{ background: var(--border-hi); }}

.empty-msg {{
  padding: 40px;
  color: var(--text-muted);
  font-family: var(--font-mono);
  font-size: 12px;
  text-align: center;
}}

/* ── SESSION ACCORDIONS ───────────────────────────── */
.sessions-list {{
  display: flex;
  flex-direction: column;
  gap: 4px;
}}

.sess-card {{
  border: 1px solid var(--border);
  border-radius: 5px;
  background: var(--surface);
  overflow: hidden;
  transition: border-color .2s;
}}
.sess-card.open {{ border-color: var(--border-hi); }}
.sess-card.hidden {{ display: none; }}

.sess-head {{
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 9px 12px;
  cursor: pointer;
  user-select: none;
  transition: background .15s;
}}
.sess-head:hover {{ background: var(--surface-2); }}

.sess-id {{
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.06em;
  min-width: 26px;
  flex-shrink: 0;
}}
.sess-name {{
  font-size: 13px;
  font-weight: 600;
  color: var(--text);
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.sess-prog-wrap {{
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}}
.sess-prog-track {{
  width: 80px;
  height: 3px;
  background: var(--border-hi);
  border-radius: 2px;
  overflow: hidden;
}}
.sess-prog-fill {{ height: 100%; border-radius: 2px; }}
.sess-prog-fill.s-full {{ background: var(--green); }}
.sess-prog-fill.s-high {{ background: var(--amber); }}
.sess-prog-fill.s-low  {{ background: #d49b10; }}
.sess-prog-fill.s-none {{ background: var(--border-hi); }}
.sess-count {{
  font-family: var(--font-mono);
  font-size: 12px;
  font-weight: 600;
  min-width: 44px;
  text-align: right;
}}
.sess-count.s-full {{ color: var(--green); }}
.sess-count.s-high {{ color: var(--amber); }}
.sess-count.s-low  {{ color: #d49b10; }}
.sess-count.s-none {{ color: var(--text-muted); }}

.sess-ref-btn {{
  background: none;
  border: 1px solid var(--border);
  border-radius: 3px;
  color: var(--text-muted);
  font-size: 12px;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all .2s;
  flex-shrink: 0;
  line-height: 1;
}}
.sess-ref-btn:hover {{
  border-color: var(--accent);
  color: var(--accent);
  background: var(--accent-glow);
}}
.sess-ref-btn:disabled {{ opacity: .35; cursor: not-allowed; }}

.sess-chevron {{
  color: var(--text-muted);
  font-size: 16px;
  transition: transform .25s ease;
  flex-shrink: 0;
  line-height: 1;
}}
.sess-card.open .sess-chevron {{ transform: rotate(90deg); }}

.sess-body {{ display: none; border-top: 1px solid var(--border); padding: 12px; }}
.sess-card.open .sess-body {{ display: block; }}

.dot-scroll {{ overflow-x: auto; }}

table.dot-table {{
  border-collapse: collapse;
  font-family: var(--font-mono);
  font-size: 12px;
  white-space: nowrap;
}}
table.dot-table th {{
  color: var(--text-muted);
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  padding: 4px 6px;
  text-align: center;
  border-bottom: 1px solid var(--border);
}}
.pname-th {{ text-align: left !important; min-width: 130px; padding-left: 0 !important; }}
.lab-th {{ min-width: 28px; }}
table.dot-table td {{ padding: 4px 6px; border-bottom: 1px solid var(--border); }}
table.dot-table tr:last-child td {{ border-bottom: none; }}
.pname-sm {{
  font-family: var(--font-ui);
  font-size: 12px;
  font-weight: 600;
  color: var(--text);
  padding-left: 0 !important;
  white-space: nowrap;
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
}}
.dot-cell {{ text-align: center; }}
.dot {{
  display: inline-block;
  width: 11px;
  height: 11px;
  border-radius: 2px;
}}
.dot-done {{ background: var(--green); }}
.dot-todo {{ background: transparent; border: 1.5px solid var(--text-muted); }}
.no-data {{
  color: var(--text-muted);
  font-size: 12px;
  font-family: var(--font-mono);
  padding: 8px 0;
  text-align: center;
}}

/* ── FADE-IN ANIMATION ───────────────────────────── */
@keyframes fadeUp {{
  from {{ opacity: 0; transform: translateY(6px); }}
  to   {{ opacity: 1; transform: translateY(0); }}
}}
.matrix-scroll {{ animation: fadeUp .35s ease both; }}
.sess-card {{ animation: fadeUp .3s ease both; }}
.sess-card:nth-child(1)  {{ animation-delay: .02s; }}
.sess-card:nth-child(2)  {{ animation-delay: .04s; }}
.sess-card:nth-child(3)  {{ animation-delay: .06s; }}
.sess-card:nth-child(4)  {{ animation-delay: .08s; }}
.sess-card:nth-child(5)  {{ animation-delay: .10s; }}
.sess-card:nth-child(6)  {{ animation-delay: .12s; }}
.sess-card:nth-child(7)  {{ animation-delay: .14s; }}
.sess-card:nth-child(8)  {{ animation-delay: .16s; }}
.sess-card:nth-child(9)  {{ animation-delay: .18s; }}
.sess-card:nth-child(10) {{ animation-delay: .20s; }}
.sess-card:nth-child(11) {{ animation-delay: .22s; }}
.sess-card:nth-child(12) {{ animation-delay: .24s; }}
.sess-card:nth-child(13) {{ animation-delay: .26s; }}
.sess-card:nth-child(14) {{ animation-delay: .28s; }}
.sess-card:nth-child(15) {{ animation-delay: .30s; }}

@media (max-width: 600px) {{
  .hdr-kpis .kpi:nth-child(n+3) {{ display: none; }}
  .hdr-progress {{ display: none; }}
  .hdr-time {{ display: none; }}
}}
</style>
</head>
<body>

<!-- HEADER -->
<header class="dash-header">
  <div class="hdr-brand">
    <span class="hdr-title">Lab Tracker</span>
    <span class="hdr-sub">Agentic AI · 15 Sessions</span>
  </div>
  <div class="hdr-kpis">
    <div class="kpi">
      <span class="kpi-val">{participants_count}</span>
      <span class="kpi-lbl">Participants</span>
    </div>
    <div class="kpi">
      <span class="kpi-val">{total_labs}</span>
      <span class="kpi-lbl">Total Labs</span>
    </div>
    <div class="kpi">
      <span class="kpi-val">{total_completions}</span>
      <span class="kpi-lbl">Completions</span>
    </div>
    <div class="kpi">
      <span class="kpi-val">{possible}</span>
      <span class="kpi-lbl">Possible</span>
    </div>
  </div>
  <div class="hdr-progress">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px;">
      <span class="kpi-lbl" style="margin:0;">Overall</span>
      <span class="overall-pct">{overall_progress:.1f}%</span>
    </div>
    <div class="overall-bar-track">
      <div class="overall-bar-fill" style="width:{overall_progress:.1f}%"></div>
    </div>
  </div>
  <div class="hdr-right">
    <span class="hdr-time" id="clock">{now_str}</span>
    <button class="ref-btn" id="ref-all-btn" onclick="refreshDashboard()">
      <span class="ref-icon" id="ref-icon">↻</span>
      <span id="ref-label">Refresh</span>
    </button>
  </div>
</header>

<!-- NAV -->
<nav class="dash-nav">
  <div class="nav-tabs">
    <button class="tab-btn active" id="tab-matrix" onclick="switchTab('matrix')">Matrix</button>
    <button class="tab-btn" id="tab-sessions" onclick="switchTab('sessions')">Sessions</button>
  </div>
  <div class="nav-filter">
    <span class="filter-ico">⌕</span>
    <input class="filter-in" id="filter-in" type="text"
           placeholder="filter participants or sessions…"
           oninput="onFilter(this.value)"
           onkeydown="if(event.key==='Escape')clearFilter()">
    <button class="filter-clr" id="filter-clr" onclick="clearFilter()">✕</button>
  </div>
  <span class="filter-stat" id="filter-stat"></span>
</nav>

<!-- MAIN -->
<main class="dash-main">

  <!-- MATRIX VIEW -->
  <div class="view active" id="view-matrix">
    <div class="matrix-scroll">
      <table class="matrix" id="matrix-table">
        <thead>
          <tr>
            <th>Participant</th>
            {"".join(f'<th title="Session {sn}: {COURSE_STRUCTURE[sn][0]}">S{sn:02d}</th>' for sn in range(1, 16))}
            <th>Done</th>
            <th>Progress</th>
          </tr>
        </thead>
        <tbody>
{matrix_rows}        </tbody>
      </table>
    </div>
  </div>

  <!-- SESSIONS VIEW -->
  <div class="view" id="view-sessions">
    <div class="sessions-list" id="sessions-list">
{session_cards}
    </div>
    <p class="empty-msg" id="sess-empty" style="display:none;">No sessions match your filter</p>
  </div>

</main>

<script>
const SERVER = 'http://localhost:8888';

// ── Tab switching ──────────────────────────────────
let currentTab = 'matrix';
function switchTab(tab) {{
  currentTab = tab;
  document.getElementById('view-matrix').classList.toggle('active', tab === 'matrix');
  document.getElementById('view-sessions').classList.toggle('active', tab === 'sessions');
  document.getElementById('tab-matrix').classList.toggle('active', tab === 'matrix');
  document.getElementById('tab-sessions').classList.toggle('active', tab === 'sessions');
  document.getElementById('filter-in').value = '';
  clearFilter();
}}

// ── Filter ─────────────────────────────────────────
function onFilter(val) {{
  const q = val.toLowerCase().trim();
  const clr = document.getElementById('filter-clr');
  clr.classList.toggle('show', q.length > 0);

  if (currentTab === 'matrix') filterMatrix(q);
  else filterSessions(q);
}}

function clearFilter() {{
  document.getElementById('filter-in').value = '';
  document.getElementById('filter-clr').classList.remove('show');
  document.getElementById('filter-stat').textContent = '';
  if (currentTab === 'matrix') filterMatrix('');
  else filterSessions('');
}}

function filterMatrix(q) {{
  const rows = document.querySelectorAll('#matrix-table tbody tr[data-name]');
  let shown = 0;
  rows.forEach(r => {{
    const match = !q || r.dataset.name.includes(q);
    r.style.display = match ? '' : 'none';
    if (match) shown++;
  }});
  const stat = document.getElementById('filter-stat');
  stat.textContent = q ? shown + ' of {len(participants)} participants' : '';
}}

function filterSessions(q) {{
  const cards = document.querySelectorAll('#sessions-list .sess-card');
  let shown = 0;
  cards.forEach(c => {{
    const match = !q || c.dataset.title.includes(q) ||
                  ('s' + c.dataset.sn).includes(q) ||
                  ('session ' + c.dataset.sn).includes(q);
    c.classList.toggle('hidden', !match);
    if (match) shown++;
  }});
  const empty = document.getElementById('sess-empty');
  empty.style.display = (shown === 0 && q) ? 'block' : 'none';
  const stat = document.getElementById('filter-stat');
  stat.textContent = q ? shown + ' of 15 sessions' : '';
}}

// ── Session accordion ──────────────────────────────
function toggleSess(head) {{
  const card = head.closest('.sess-card');
  card.classList.toggle('open');
}}

// ── Refresh ────────────────────────────────────────
function callRefresh(url, onDone) {{
  fetch(url)
    .then(r => r.json())
    .then(d => {{
      if (d.status === 'ok') window.location.reload();
      else {{ alert('Refresh failed: ' + (d.message || 'unknown error')); if (onDone) onDone(); }}
    }})
    .catch(() => {{
      alert('Dashboard server not running.\\nStart it with:\\n  python3 reporting/server.py');
      if (onDone) onDone();
    }});
}}

function refreshDashboard() {{
  const btn = document.getElementById('ref-all-btn');
  const ico = document.getElementById('ref-icon');
  const lbl = document.getElementById('ref-label');
  btn.classList.add('spinning');
  btn.disabled = true;
  lbl.textContent = 'Refreshing…';
  ico.style.display = 'inline-block';
  ico.classList.add('ref-icon');
  btn.querySelector('.ref-icon').style.animation = 'spin .7s linear infinite';
  callRefresh(SERVER + '/refresh', () => {{
    btn.classList.remove('spinning');
    btn.disabled = false;
    lbl.textContent = 'Refresh';
  }});
}}

function refreshSession(sn) {{
  const btn = document.getElementById('rsess-' + sn);
  const orig = btn.textContent;
  btn.disabled = true;
  btn.textContent = '⏳';
  callRefresh(SERVER + '/refresh/session/' + sn, () => {{
    btn.disabled = false;
    btn.textContent = orig;
  }});
}}

// ── Live clock ─────────────────────────────────────
function updateClock() {{
  const now = new Date();
  const pad = n => String(n).padStart(2,'0');
  document.getElementById('clock').textContent =
    now.getFullYear() + '-' + pad(now.getMonth()+1) + '-' + pad(now.getDate()) +
    ' ' + pad(now.getHours()) + ':' + pad(now.getMinutes());
}}
setInterval(updateClock, 10000);

// ── Keyboard shortcuts ─────────────────────────────
document.addEventListener('keydown', e => {{
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && e.key === 'R') {{
    e.preventDefault(); refreshDashboard();
  }}
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {{
    e.preventDefault();
    document.getElementById('filter-in').focus();
  }}
  if (e.key === '1' && !e.ctrlKey && !e.metaKey && document.activeElement.tagName !== 'INPUT') switchTab('matrix');
  if (e.key === '2' && !e.ctrlKey && !e.metaKey && document.activeElement.tagName !== 'INPUT') switchTab('sessions');
}});

// ── Update stats display ───────────────────────────
filterMatrix('');
</script>
</body>
</html>"""

    with open(output_file, "w") as f:
        f.write(html)

    print(f"✓ Dashboard generated: {output_file}")
    print(f"✓ Open in browser: file://{os.path.abspath(output_file)}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate lab submission dashboard")
    parser.add_argument("--output", default="dashboard.html", help="Output HTML file")
    parser.add_argument(
        "--auto-refresh", action="store_true", help="Enable auto-refresh (60s)"
    )
    parser.add_argument("--session", type=int, help="Refresh only this session (1-15)")
    parser.add_argument(
        "--since",
        metavar="YYYY-MM-DD",
        help="Ignore submissions made before this local date (e.g. a new cohort's start)",
    )
    args = parser.parse_args()

    token = get_github_token()
    since = parse_since(args.since) if args.since else None
    if since:
        print(f"Counting submissions from {args.since} onward ({since} UTC)")

    if args.session:
        print(f"Fetching session {args.session} issues only...")
        issues = fetch_lab_issues(token, session=args.session)
        print(f"Found {len(issues)} issues for session {args.session}")

        completion_matrix = load_cache()
        for participant in list(completion_matrix.keys()):
            completion_matrix[participant].pop(args.session, None)

        new_data = build_completion_data(token, issues, since)
        for participant, sessions in new_data.items():
            completion_matrix[participant].update(sessions)
    else:
        print("Fetching all lab tracking data...")
        issues = fetch_lab_issues(token)
        print(f"Found {len(issues)} lab issues")
        print("Processing completions...")
        completion_matrix = build_completion_data(token, issues, since)

    save_cache(completion_matrix)
    print("Generating HTML dashboard...")
    generate_html_dashboard(completion_matrix, args.output, args.auto_refresh)


if __name__ == "__main__":
    main()
