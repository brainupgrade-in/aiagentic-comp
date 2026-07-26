#!/usr/bin/env python3
"""
Lab Completion Tracker (Comment-Based)
Tracks which participants completed which labs by parsing issue comments.

Usage: python3 track-lab-comments.py [--session N] [--participant username]
Requires: GITHUB_TOKEN environment variable with read access
"""

import os
import sys
import re
import argparse
from datetime import datetime
from collections import defaultdict
import requests

REPO_OWNER = "brainupgrade-in"
REPO_NAME = "aiagentic-comp"

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
    """Get GitHub token from environment."""
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("Error: GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    return token


def fetch_lab_issues(token, session=None):
    """Fetch all lab tracking issues."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    labels = ["lab-tracking"]
    if session:
        labels.append(f"session-{session}")

    all_issues = []
    page = 1

    while True:
        params = {
            "state": "all",
            "labels": ",".join(labels),
            "per_page": 100,
            "page": page,
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
        "X-GitHub-Api-Version": "2022-11-28",
    }

    all_comments = []
    page = 1

    while True:
        params = {"per_page": 100, "page": page}
        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            return []

        comments = response.json()
        if not comments:
            break

        all_comments.extend(comments)
        page += 1

    return all_comments


def parse_issue_title(title):
    """Extract session and lab number from issue title."""
    # Expected: "Session N - Lab MM"
    match = re.search(r"Session (\d+) - Lab (\d+)", title)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None


def extract_participant_name(comment_body):
    """Extract participant name from comment body.

    Looks for pattern: **Participant:** name (email) or **Participant:** name
    Returns the name portion, or None if not found.
    """
    # Pattern to match: **Participant:** name (email) or **Participant:** name
    patterns = [
        r"\*\*Participant:\*\*\s+([^\(\n]+?)\s*\([^\)]+\)",  # name (email)
        r"\*\*Participant:\*\*\s+([^\n]+)",  # just name
    ]

    for pattern in patterns:
        match = re.search(pattern, comment_body)
        if match:
            name = match.group(1).strip()
            return name

    return None


def is_completion_comment(comment_body):
    """Check if comment indicates lab completion.

    Matches the format produced by submit-lab.sh:
      ✅ Completed
      **Participant:** name (email)
      **Validation:** All checks passed
      **Notes:** optional notes
    """
    # Primary: exact format from submit-lab.sh
    # Secondary: manual completions with common completion phrases
    patterns = [
        r"✅\s+completed",
        r"completed\s+✅",
        r"\[x\].*done",
        r"all checks passed",
    ]

    comment_lower = comment_body.lower()
    return any(re.search(pattern, comment_lower) for pattern in patterns)


def build_completion_matrix(token, issues):
    """Build completion matrix from issues and comments."""
    completion_matrix = defaultdict(lambda: defaultdict(dict))

    total_issues = len(issues)
    print(f"Processing {total_issues} lab issues...")

    for idx, issue in enumerate(issues, 1):
        title = issue.get("title", "")
        issue_number = issue.get("number")
        session_num, lab_num = parse_issue_title(title)

        if session_num is None or lab_num is None:
            continue

        print(
            f"  [{idx}/{total_issues}] Session {session_num} Lab {lab_num:02d} (#{issue_number})...",
            end="",
        )

        # Fetch comments for this issue
        comments = fetch_issue_comments(token, issue_number)

        completed_by = []
        for comment in comments:
            github_author = comment.get("user", {}).get("login", "")
            body = comment.get("body", "")
            created_at = comment.get("created_at", "")

            # Skip bot comments
            if github_author.endswith("[bot]"):
                continue

            # Check if this is a completion comment
            if is_completion_comment(body):
                # Extract participant name from comment body
                participant_name = extract_participant_name(body)

                # If no participant name found, fall back to GitHub username
                if not participant_name:
                    participant_name = github_author

                completed_by.append(
                    {
                        "author": participant_name,
                        "date": created_at,
                        "comment_url": comment.get("html_url", ""),
                    }
                )

        print(f" {len(completed_by)} completions")

        # Store in matrix
        for completion in completed_by:
            author = completion["author"]
            if session_num not in completion_matrix[author]:
                completion_matrix[author][session_num] = {}

            completion_matrix[author][session_num][lab_num] = {
                "issue_number": issue_number,
                "completed_date": completion["date"],
                "comment_url": completion["comment_url"],
            }

    return completion_matrix


def generate_completion_report(
    completion_matrix, filter_session=None, filter_participant=None
):
    """Generate markdown completion report."""
    report = f"# Lab Completion Report (Comment-Based)\n\n"
    report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    report += f"**Repository:** {REPO_OWNER}/{REPO_NAME}\n\n"

    # Filter participants if specified
    if filter_participant:
        participants = (
            [filter_participant] if filter_participant in completion_matrix else []
        )
    else:
        participants = sorted(completion_matrix.keys())

    if not participants:
        report += "No completion data found.\n"
        return report

    # Summary stats
    total_participants = len(participants)
    total_completions = sum(
        len([lab for labs in sessions.values() for lab in labs])
        for sessions in completion_matrix.values()
    )

    report += f"**Total Participants:** {total_participants}\n"
    report += f"**Total Lab Completions:** {total_completions}\n\n"

    # Determine sessions to display
    if filter_session:
        sessions_to_show = [filter_session]
    else:
        sessions_to_show = sorted(COURSE_STRUCTURE.keys())

    # Completion matrix
    report += "## Completion Matrix\n\n"

    # Header
    report += "| Participant |"
    for session_num in sessions_to_show:
        session_title, num_labs = COURSE_STRUCTURE[session_num]
        report += f" S{session_num} |"
    if not filter_session:
        report += " Total | Progress |\n"
    else:
        report += " Completed |\n"

    # Separator
    report += "|-------------|"
    if not filter_session:
        for _ in range(len(sessions_to_show) + 2):
            report += "------|"
    else:
        for _ in range(len(sessions_to_show) + 1):
            report += "------|"
    report += "\n"

    # Participant rows
    for participant in participants:
        sessions = completion_matrix[participant]
        report += f"| {participant} |"

        total_completed = 0
        total_labs = 0

        for session_num in sessions_to_show:
            session_title, num_labs = COURSE_STRUCTURE[session_num]
            total_labs += num_labs

            if session_num in sessions:
                completed_count = len(sessions[session_num])
                total_completed += completed_count
                report += f" {completed_count}/{num_labs} |"
            else:
                report += f" 0/{num_labs} |"

        if not filter_session:
            report += f" {total_completed}/{total_labs} |"
            percentage = (total_completed / total_labs * 100) if total_labs > 0 else 0
            report += f" {percentage:.0f}% |\n"
        else:
            report += f" {total_completed}/{total_labs} |\n"

    # Detailed breakdown by session
    report += "\n## Session Details\n\n"

    for session_num in sessions_to_show:
        session_title, num_labs = COURSE_STRUCTURE[session_num]
        report += f"### Session {session_num}: {session_title}\n\n"

        # Per-lab breakdown
        report += "| Lab | " + " | ".join(participants) + " |\n"
        report += "|-----|" + "|".join(["-----" for _ in participants]) + "|\n"

        for lab_num in range(1, num_labs + 1):
            report += f"| {lab_num:02d} |"

            for participant in participants:
                if (
                    session_num in completion_matrix[participant]
                    and lab_num in completion_matrix[participant][session_num]
                ):
                    report += " ✅ |"
                else:
                    report += " — |"

            report += "\n"

        report += "\n"

    # Pending labs by participant
    report += "## Pending Labs\n\n"

    for participant in participants:
        pending = []
        for session_num in sessions_to_show:
            session_title, num_labs = COURSE_STRUCTURE[session_num]
            participant_labs = completion_matrix[participant].get(session_num, {})

            for lab_num in range(1, num_labs + 1):
                if lab_num not in participant_labs:
                    pending.append(f"Session {session_num} Lab {lab_num:02d}")

        if pending:
            report += f"### {participant}\n\n"
            for lab in pending[:10]:  # Show first 10
                report += f"- {lab}\n"
            if len(pending) > 10:
                report += f"- ... and {len(pending) - 10} more\n"
            report += "\n"

    return report


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Track lab completion via issue comments"
    )
    parser.add_argument("--session", type=int, help="Filter by session number (1-15)")
    parser.add_argument(
        "--participant", type=str, help="Filter by participant username"
    )
    args = parser.parse_args()

    token = get_github_token()

    print("Fetching lab tracking issues...")
    issues = fetch_lab_issues(token, session=args.session)
    print(f"Found {len(issues)} lab issues\n")

    completion_matrix = build_completion_matrix(token, issues)

    print("\nGenerating report...")
    report = generate_completion_report(
        completion_matrix,
        filter_session=args.session,
        filter_participant=args.participant,
    )

    # Save to file
    output_file = "/tmp/lab-completion-comments.md"
    with open(output_file, "w") as f:
        f.write(report)

    print(f"\nReport saved to: {output_file}\n")
    print("=" * 60)
    print(report)
    print("=" * 60)


if __name__ == "__main__":
    main()
