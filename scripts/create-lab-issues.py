#!/usr/bin/env python3
"""
Create GitHub Issues for all labs in the course.
One issue per lab (119 total) for participants to comment on when completed.

Usage: python3 create-lab-issues.py
Requires: GITHUB_TOKEN environment variable with repo write access
"""

import os
import sys
import time
import requests

REPO_OWNER = "brainupgrade-in"
REPO_NAME = "aiagentic-comp"

# Lab structure: session_number -> (session_title, num_labs)
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
        print("This requires a token with 'Issues: Write' permission")
        sys.exit(1)
    return token


def create_issue(token, session_num, lab_num, session_title):
    """Create a single lab issue."""
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    title = f"Session {session_num} - Lab {lab_num:02d}"

    body = f"""## Session {session_num}: {session_title}
### Lab {lab_num:02d}

**📁 Location:** `hands-on/session-{session_num}/lab{lab_num:02d}_*.ipynb`

---

## Instructions for Participants

When you complete this lab:

1. **Run all validation cells** in your notebook
2. **Verify all checks pass** ([PASS] markers present)
3. **Comment below** with:
   ```
   ✅ Completed

   **Validation:** All checks passed
   **Screenshot/Evidence:** [Optional: Attach screenshot of output]
   **Notes:** [Optional: Any challenges or learnings]
   ```

---

## Completion Checklist

Comment below when done. Your GitHub username will be recorded automatically.

**Status:** Open for submissions
"""

    labels = ["lab-tracking", f"session-{session_num}", f"lab-{lab_num:02d}"]

    payload = {"title": title, "body": body, "labels": labels}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        issue_data = response.json()
        return True, issue_data["number"], issue_data["html_url"]
    else:
        return False, None, response.json()


def main():
    """Main function."""
    print("Creating lab tracking issues...")
    print(f"Repository: {REPO_OWNER}/{REPO_NAME}")
    print(
        f"Total issues to create: {sum(count for _, count in COURSE_STRUCTURE.values())}"
    )
    print()

    token = get_github_token()

    created_count = 0
    failed_count = 0

    for session_num in sorted(COURSE_STRUCTURE.keys()):
        session_title, num_labs = COURSE_STRUCTURE[session_num]
        print(f"Session {session_num}: {session_title} ({num_labs} labs)")

        for lab_num in range(1, num_labs + 1):
            success, issue_num, url = create_issue(
                token, session_num, lab_num, session_title
            )

            if success:
                created_count += 1
                print(
                    f"  ✓ Created issue #{issue_num}: Session {session_num} Lab {lab_num:02d}"
                )
            else:
                failed_count += 1
                print(f"  ✗ Failed: Session {session_num} Lab {lab_num:02d}")
                print(f"    Error: {url}")

            # Rate limiting: GitHub allows 5000 requests/hour for authenticated users
            # But let's be conservative and add a small delay
            time.sleep(0.5)

        print()

    print("=" * 60)
    print(f"Summary:")
    print(f"  Created: {created_count}")
    print(f"  Failed: {failed_count}")
    print(f"  Total: {created_count + failed_count}")
    print()

    if created_count > 0:
        print(
            f"View issues: https://github.com/{REPO_OWNER}/{REPO_NAME}/issues?q=is:issue+label:lab-tracking"
        )


if __name__ == "__main__":
    main()
