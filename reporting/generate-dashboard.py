#!/usr/bin/env python3
"""
Lab Submission Monitoring Dashboard Generator

Generates an interactive HTML dashboard showing lab completion status.
Updates with real-time data from GitHub Issues.

Usage: python3 generate-dashboard.py [--output dashboard.html] [--auto-refresh]
"""

import os
import sys
import json
import argparse
from datetime import datetime
from collections import defaultdict
import requests

REPO_OWNER = "brainupgrade-in"
REPO_NAME = "aiagentic-comp"

COURSE_STRUCTURE = {
    1: ("Introduction to Agentic AI", 6),
    2: ("AI Coding Assistants & Vibe Coding", 8),
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
    """Get GitHub token from environment."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    return token

def fetch_lab_issues(token):
    """Fetch all lab tracking issues."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    all_issues = []
    page = 1

    while True:
        params = {
            "state": "all",
            "labels": "lab-tracking",
            "per_page": 100,
            "page": page
        }
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
    """Fetch all comments for a specific issue."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    response = requests.get(url, headers=headers, params={"per_page": 100})
    if response.status_code != 200:
        return []

    return response.json()

def parse_issue_title(title):
    """Extract session and lab number from issue title."""
    import re
    match = re.search(r'Session (\d+) - Lab (\d+)', title)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

def is_completion_comment(comment_body):
    """Check if comment indicates lab completion."""
    import re
    patterns = [
        r'✅.*completed',
        r'completed.*✅',
        r'\[x\].*done',
        r'done',
        r'finished',
        r'all checks passed',
    ]
    comment_lower = comment_body.lower()
    return any(re.search(pattern, comment_lower) for pattern in patterns)

def build_completion_data(token, issues):
    """Build completion data from issues and comments."""
    completion_matrix = defaultdict(lambda: defaultdict(dict))

    for issue in issues:
        title = issue.get("title", "")
        issue_number = issue.get("number")
        session_num, lab_num = parse_issue_title(title)

        if session_num is None or lab_num is None:
            continue

        comments = fetch_issue_comments(token, issue_number)

        for comment in comments:
            author = comment.get("user", {}).get("login", "")
            body = comment.get("body", "")
            created_at = comment.get("created_at", "")

            if author.endswith("[bot]"):
                continue

            if is_completion_comment(body):
                if session_num not in completion_matrix[author]:
                    completion_matrix[author][session_num] = {}

                completion_matrix[author][session_num][lab_num] = {
                    "issue_number": issue_number,
                    "completed_date": created_at,
                }

    return completion_matrix

def generate_html_dashboard(completion_matrix, output_file, auto_refresh=False):
    """Generate interactive HTML dashboard."""

    total_labs = sum(count for _, count in COURSE_STRUCTURE.values())
    participants = sorted(completion_matrix.keys())

    # Calculate statistics
    total_participants = len(participants)
    total_completions = sum(
        len([lab for labs in sessions.values() for lab in labs])
        for sessions in completion_matrix.values()
    )

    overall_progress = (total_completions / (total_labs * total_participants) * 100) if total_participants > 0 else 0

    # Generate HTML
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lab Submission Dashboard - Agentic AI Course</title>
    {'<meta http-equiv="refresh" content="60">' if auto_refresh else ''}
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}

        .header h1 {{
            color: #2d3748;
            font-size: 2em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            color: #718096;
            font-size: 1.1em;
        }}

        .header .last-updated {{
            color: #a0aec0;
            font-size: 0.9em;
            margin-top: 10px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}

        .stat-card {{
            background: white;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        .stat-card .label {{
            color: #718096;
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }}

        .stat-card .value {{
            color: #2d3748;
            font-size: 2.5em;
            font-weight: bold;
        }}

        .stat-card .sub-value {{
            color: #a0aec0;
            font-size: 0.9em;
            margin-top: 5px;
        }}

        .stat-card.progress {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}

        .stat-card.progress .label,
        .stat-card.progress .value,
        .stat-card.progress .sub-value {{
            color: white;
        }}

        .progress-bar {{
            background: rgba(255,255,255,0.3);
            height: 10px;
            border-radius: 5px;
            margin-top: 15px;
            overflow: hidden;
        }}

        .progress-bar-fill {{
            background: white;
            height: 100%;
            border-radius: 5px;
            transition: width 0.3s ease;
        }}

        .section {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }}

        .section h2 {{
            color: #2d3748;
            font-size: 1.5em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e2e8f0;
        }}

        .completion-matrix {{
            overflow-x: auto;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9em;
        }}

        th {{
            background: #f7fafc;
            color: #4a5568;
            font-weight: 600;
            padding: 12px 8px;
            text-align: left;
            position: sticky;
            top: 0;
            border-bottom: 2px solid #e2e8f0;
        }}

        td {{
            padding: 10px 8px;
            border-bottom: 1px solid #e2e8f0;
        }}

        tr:hover {{
            background: #f7fafc;
        }}

        .status-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: 600;
        }}

        .status-complete {{
            background: #c6f6d5;
            color: #22543d;
        }}

        .status-partial {{
            background: #feebc8;
            color: #7c2d12;
        }}

        .status-none {{
            background: #fed7d7;
            color: #742a2a;
        }}

        .session-progress {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .session-progress-bar {{
            flex: 1;
            background: #e2e8f0;
            height: 8px;
            border-radius: 4px;
            overflow: hidden;
        }}

        .session-progress-fill {{
            background: linear-gradient(90deg, #48bb78, #38a169);
            height: 100%;
            border-radius: 4px;
        }}

        .session-progress-text {{
            font-size: 0.85em;
            color: #718096;
            min-width: 60px;
            text-align: right;
        }}

        .lab-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
            gap: 4px;
        }}

        .lab-cell {{
            width: 100%;
            aspect-ratio: 1;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75em;
            font-weight: 600;
        }}

        .lab-cell.completed {{
            background: #48bb78;
            color: white;
        }}

        .lab-cell.pending {{
            background: #e2e8f0;
            color: #a0aec0;
        }}

        .participant-name {{
            font-weight: 600;
            color: #2d3748;
        }}

        .session-section {{
            margin-bottom: 30px;
        }}

        .session-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .session-title {{
            font-size: 1.2em;
            font-weight: 600;
            color: #2d3748;
        }}

        @media (max-width: 768px) {{
            .stats-grid {{
                grid-template-columns: 1fr;
            }}

            .lab-grid {{
                grid-template-columns: repeat(auto-fill, minmax(30px, 1fr));
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Lab Submission Dashboard</h1>
            <div class="subtitle">Agentic AI Course - Real-time Completion Tracking</div>
            <div class="last-updated">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="label">Total Participants</div>
                <div class="value">{total_participants}</div>
                <div class="sub-value">Enrolled in course</div>
            </div>

            <div class="stat-card">
                <div class="label">Total Labs</div>
                <div class="value">{total_labs}</div>
                <div class="sub-value">Across 15 sessions</div>
            </div>

            <div class="stat-card">
                <div class="label">Completions</div>
                <div class="value">{total_completions}</div>
                <div class="sub-value">Out of {total_labs * total_participants if total_participants > 0 else 0} possible</div>
            </div>

            <div class="stat-card progress">
                <div class="label">Overall Progress</div>
                <div class="value">{overall_progress:.1f}%</div>
                <div class="progress-bar">
                    <div class="progress-bar-fill" style="width: {overall_progress}%"></div>
                </div>
            </div>
        </div>
"""

    # Completion Matrix
    html += """
        <div class="section">
            <h2>Completion Matrix</h2>
            <div class="completion-matrix">
                <table>
                    <thead>
                        <tr>
                            <th>Participant</th>
"""

    for session_num in range(1, 16):
        html += f"                            <th>S{session_num}</th>\n"

    html += """                            <th>Total</th>
                            <th>Progress</th>
                        </tr>
                    </thead>
                    <tbody>
"""

    if not participants:
        html += """                        <tr>
                            <td colspan="18" style="text-align: center; color: #a0aec0; padding: 40px;">
                                No submissions yet. Waiting for participants to submit labs...
                            </td>
                        </tr>
"""
    else:
        for participant in participants:
            sessions = completion_matrix[participant]
            total_completed = sum(len(labs) for labs in sessions.values())
            progress_pct = (total_completed / total_labs * 100) if total_labs > 0 else 0

            html += f"""                        <tr>
                            <td class="participant-name">{participant}</td>
"""

            for session_num in range(1, 16):
                _, num_labs = COURSE_STRUCTURE[session_num]
                completed = len(sessions.get(session_num, {}))
                html += f"                            <td>{completed}/{num_labs}</td>\n"

            status_class = "status-complete" if progress_pct >= 90 else "status-partial" if progress_pct >= 50 else "status-none"

            html += f"""                            <td><strong>{total_completed}/{total_labs}</strong></td>
                            <td>
                                <span class="status-badge {status_class}">{progress_pct:.0f}%</span>
                            </td>
                        </tr>
"""

    html += """                    </tbody>
                </table>
            </div>
        </div>
"""

    # Session Details
    html += """
        <div class="section">
            <h2>Session Details</h2>
"""

    for session_num in range(1, 16):
        session_title, num_labs = COURSE_STRUCTURE[session_num]

        # Calculate session completion
        session_completions = 0
        for participant in participants:
            session_completions += len(completion_matrix[participant].get(session_num, {}))

        session_total = num_labs * total_participants if total_participants > 0 else num_labs
        session_progress = (session_completions / session_total * 100) if session_total > 0 else 0

        html += f"""
            <div class="session-section">
                <div class="session-header">
                    <div class="session-title">Session {session_num}: {session_title}</div>
                    <div class="session-progress">
                        <div class="session-progress-bar">
                            <div class="session-progress-fill" style="width: {session_progress}%"></div>
                        </div>
                        <div class="session-progress-text">{session_completions}/{session_total}</div>
                    </div>
                </div>
"""

        if participants:
            html += """                <table>
                    <thead>
                        <tr>
                            <th>Participant</th>
"""

            for lab_num in range(1, num_labs + 1):
                html += f"                            <th>L{lab_num:02d}</th>\n"

            html += """                        </tr>
                    </thead>
                    <tbody>
"""

            for participant in participants:
                html += f"""                        <tr>
                            <td class="participant-name">{participant}</td>
"""

                participant_session = completion_matrix[participant].get(session_num, {})
                for lab_num in range(1, num_labs + 1):
                    completed = lab_num in participant_session
                    symbol = "✅" if completed else "—"
                    html += f"                            <td style='text-align: center;'>{symbol}</td>\n"

                html += """                        </tr>
"""

            html += """                    </tbody>
                </table>
"""
        else:
            html += """                <p style="color: #a0aec0; text-align: center; padding: 20px;">No submissions yet</p>
"""

        html += """            </div>
"""

    html += """        </div>
    </div>
</body>
</html>
"""

    # Write HTML file
    with open(output_file, 'w') as f:
        f.write(html)

    print(f"✓ Dashboard generated: {output_file}")
    print(f"✓ Open in browser: file://{os.path.abspath(output_file)}")

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Generate lab submission dashboard")
    parser.add_argument("--output", default="dashboard.html", help="Output HTML file")
    parser.add_argument("--auto-refresh", action="store_true", help="Enable auto-refresh (60s)")
    args = parser.parse_args()

    print("Fetching lab tracking data...")
    token = get_github_token()
    issues = fetch_lab_issues(token)
    print(f"Found {len(issues)} lab issues")

    print("Processing completions...")
    completion_matrix = build_completion_data(token, issues)

    print("Generating HTML dashboard...")
    generate_html_dashboard(completion_matrix, args.output, args.auto_refresh)

if __name__ == "__main__":
    main()
