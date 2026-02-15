# Lab Submission Instructions - Agentic AI Course

## Overview

You'll submit labs by **commenting on GitHub issues**. Each lab has its own issue where you'll post "✅ Completed" when done.

**Token:** You'll receive a shared access token during the Zoom session

---

## One-Time Setup (Before Day 1)

### Step 1: Install GitHub CLI

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install gh
```

**macOS:**
```bash
brew install gh
```

**Windows:**
Download from: https://cli.github.com/

### Step 2: Authenticate with Shared Token

```bash
# Start authentication
gh auth login

# Select these options:
# - What account? → GitHub.com
# - Protocol? → HTTPS
# - Authenticate? → Paste an authentication token
# - Paste token: [USE THE TOKEN SHARED IN ZOOM]

# Verify it works
gh auth status
```

Expected output:
```
✓ Logged in to github.com as your-username
✓ Token: github_pat_...
```

### Step 3: Clone Course Repository

```bash
# Clone repository (read-only access)
git clone https://github.com/brainupgrade-in/aiagentic-comp.git

# Navigate to course directory
cd aiagentic-comp

# Verify access
gh issue list --repo brainupgrade-in/aiagentic-comp --limit 5
```

### Step 4: Setup Python Environment

```bash
# Create virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
jupyter --version
```

---

## Daily Workflow

### 1. Pull Latest Updates

```bash
cd ~/aiagentic-comp
git pull origin main
source .venv/bin/activate
```

### 2. Complete Labs

```bash
# Open Jupyter
jupyter notebook hands-on/session-1/

# Work through labs
# Fill in ___ placeholders
# Run all cells
# Verify [PASS] markers appear
```

### 3. Submit Completion

**After completing each lab:**

```bash
# Example: Completed Session 1 Lab 01

# Find the issue number (reference table below)
# Session 1 Lab 01 = Issue #1

# Submit completion comment
gh issue comment 1 \
  --repo brainupgrade-in/aiagentic-comp \
  --body "✅ Completed

**Validation:** All checks passed"
```

**That's it!** Your GitHub username is automatically recorded.

---

## Issue Number Reference

| Session | Labs | Issue Numbers |
|---------|------|---------------|
| 1 | 1-6 | #1 - #6 |
| 2 | 1-8 | #7 - #14 |
| 3 | 1-7 | #15 - #21 |
| 4 | 1-8 | #22 - #29 |
| 5 | 1-8 | #30 - #37 |
| 6 | 1-8 | #38 - #45 |
| 7 | 1-8 | #46 - #53 |
| 8 | 1-8 | #54 - #61 |
| 9 | 1-8 | #62 - #69 |
| 10 | 1-8 | #70 - #77 |
| 11 | 1-8 | #78 - #85 |
| 12 | 1-9 | #86 - #94 |
| 13 | 1-8 | #95 - #102 |
| 14 | 1-8 | #103 - #110 |
| 15 | 1-8 | #111 - #118 |

**Quick formula:**
- Session 1 Lab 01 = Issue #1
- Session 2 Lab 01 = Issue #7
- Session 3 Lab 01 = Issue #15
- etc.

---

## Submission Examples

### Basic Submission

```bash
gh issue comment 1 --repo brainupgrade-in/aiagentic-comp --body "✅ Completed"
```

### Detailed Submission (Recommended)

```bash
gh issue comment 1 --repo brainupgrade-in/aiagentic-comp --body "✅ Completed

**Validation:** All checks passed ([PASS] markers present)
**Time taken:** ~20 minutes
**Notes:** Great introduction to AI agents!"
```

### With Screenshot

```bash
# Take screenshot of validation output
# Then comment:
gh issue comment 1 --repo brainupgrade-in/aiagentic-comp --body "✅ Completed

**Validation:** All checks passed
**Screenshot:** Attached below"

# Upload image in web UI at:
# https://github.com/brainupgrade-in/aiagentic-comp/issues/1
```

### Reporting Issues

```bash
gh issue comment 1 --repo brainupgrade-in/aiagentic-comp --body "✅ Completed

**Validation:** Mostly passed
**Note:** Lab 01 TODO section 3 was unclear about the expected format.
Made my best guess and it passed validation."
```

---

## Quick Commands

### Find Issue Number

**Method 1: Use the reference table above**

**Method 2: Search by title**
```bash
# List all Session 1 issues
gh issue list --repo brainupgrade-in/aiagentic-comp --label "session-1"

# Search for specific lab
gh issue list --repo brainupgrade-in/aiagentic-comp --search "Session 1 - Lab 01"
```

### View Issue Details

```bash
# View issue in terminal
gh issue view 1 --repo brainupgrade-in/aiagentic-comp

# View issue in browser
gh issue view 1 --repo brainupgrade-in/aiagentic-comp --web
```

### Check Your Submissions

```bash
# See all your comments across all issues
gh issue list --repo brainupgrade-in/aiagentic-comp \
  --label lab-tracking \
  --search "commenter:@me"
```

---

## Tips & Best Practices

### ✅ Do

- Submit immediately after validation passes
- Include brief notes about challenges or learnings
- Use the exact issue numbers from the reference table
- Keep comments concise but informative
- Mention if you found any unclear instructions

### ❌ Don't

- Submit without running validation (all [PASS] markers)
- Leave TODO placeholders (___) unfilled
- Post multiple "completed" comments on same issue
- Use issues for asking questions (use Zoom chat or discussions)

---

## Completion Tracking

**View all lab issues:**
https://github.com/brainupgrade-in/aiagentic-comp/issues?q=is:issue+label:lab-tracking

**Your progress is visible to the instructor who tracks:**
- Which labs you've completed (based on your comments)
- When you completed them (comment timestamp)
- Your completion rate across all sessions

---

## Troubleshooting

### "Resource not accessible by personal access token"

**Fix:** Token expired or has wrong permissions. Get a new token from instructor.

### "gh: command not found"

**Fix:** Install GitHub CLI:
```bash
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh
```

### "Repository not found"

**Fix:** Token not authenticated properly. Re-run:
```bash
gh auth login
# Use the token shared in Zoom
```

### "Cannot find issue #X"

**Fix:** Check the reference table above for correct issue number.

### Forgot to activate virtual environment

**Symptoms:** `ModuleNotFoundError` when running labs

**Fix:**
```bash
cd ~/aiagentic-comp
source .venv/bin/activate
```

---

## Example: Complete Session 1 Workflow

```bash
# Day 1 morning
cd ~/aiagentic-comp
git pull
source .venv/bin/activate
jupyter notebook hands-on/session-1/

# Complete Lab 01
# ... work through notebook ...
# All validation cells show [PASS]

# Submit Lab 01 (Issue #1)
gh issue comment 1 --repo brainupgrade-in/aiagentic-comp --body "✅ Completed

**Validation:** All checks passed"

# Complete Lab 02
# ... work through notebook ...

# Submit Lab 02 (Issue #2)
gh issue comment 2 --repo brainupgrade-in/aiagentic-comp --body "✅ Completed

**Validation:** All checks passed"

# Continue for Labs 03-06 (Issues #3-6)

# End of Session 1: You should have commented on Issues #1-6
```

---

## Support

**During sessions:**
- Ask questions in Zoom chat
- Raise hand for clarification

**Technical issues:**
- Check this troubleshooting section first
- Contact instructor during breaks

**GitHub issues:**
- Only use for lab submissions
- Not for questions or discussion

---

## Quick Reference Card

```bash
# Setup (once)
gh auth login                    # Use token from Zoom
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Daily workflow
cd ~/aiagentic-comp
git pull
source .venv/bin/activate
jupyter notebook                 # Complete labs

# Submit (for each lab)
gh issue comment <issue-number> \
  --repo brainupgrade-in/aiagentic-comp \
  --body "✅ Completed"

# Check progress
gh issue list --repo brainupgrade-in/aiagentic-comp \
  --search "commenter:@me"
```

---

**Ready to start?** Complete the setup steps before Day 1!

**Questions?** Ask in Zoom before we begin.

---

**Course Repository:** https://github.com/brainupgrade-in/aiagentic-comp
**Lab Issues:** https://github.com/brainupgrade-in/aiagentic-comp/issues?q=is:issue+label:lab-tracking
**Sessions:** 15 sessions × 6-9 labs = 118 total labs to complete
