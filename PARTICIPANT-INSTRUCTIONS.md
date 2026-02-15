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

### Step 4: Set Your Identity (Required)

**⚠️ IMPORTANT:** This identifies YOU in submissions and dashboard tracking.

```bash
# Make sure you're in the repository directory
cd ~/aiagentic-comp

# Set YOUR GitHub username and email (for this repository only)
git config user.name "your-github-username"
git config user.email "your-email@example.com"

# Verify it's set correctly
git config user.name
git config user.email
```

**Example:**
```bash
git config user.name "johndoe"
git config user.email "johndoe@gmail.com"
```

**Important Notes:**
- ✅ Use your **actual GitHub username** (not your full name)
- ✅ This sets config **only for this repository** (doesn't affect your system)
- ✅ This is how you'll appear in the dashboard and tracking
- ✅ Include your email for verification

**Why this matters:**
- Your submissions will show as: `johndoe (johndoe@gmail.com)`
- Dashboard will track YOUR progress (not instructor's)
- Instructor can verify your identity

### Step 5: Setup Python Environment

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

**After completing each lab, use the automated submission script:**

**Linux/Mac:**
```bash
# Basic submission
./scripts/submit-lab.sh <session> <lab>

# With optional notes (recommended)
./scripts/submit-lab.sh <session> <lab> "your notes here"

# Examples
./scripts/submit-lab.sh 1 1
./scripts/submit-lab.sh 1 2 "Great lab on AI agents!"
./scripts/submit-lab.sh 2 5 "Learned about RAG"
```

**Windows PowerShell:**
```powershell
# Basic submission
.\scripts\submit-lab.ps1 <session> <lab>

# With optional notes
.\scripts\submit-lab.ps1 <session> <lab> "your notes here"

# Examples
.\scripts\submit-lab.ps1 1 1
.\scripts\submit-lab.ps1 1 2 "Great lab on AI agents!"
```

**What the script does:**
- ✅ Auto-detects your GitHub username and email (from Step 4)
- ✅ Calculates correct issue number automatically
- ✅ Shows preview before submitting
- ✅ Asks for confirmation (y/N)
- ✅ Posts comment with your information
- ✅ Provides submission URL

**Sample output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Lab Submission - Agentic AI Course
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: 1
Lab: 1
Issue Number: #1

Detecting your information...
✓ Username: johndoe
✓ Email: johndoe@gmail.com
✓ GitHub CLI authenticated

Comment Preview:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Completed

**Participant:** johndoe (johndoe@gmail.com)
**Validation:** All checks passed
**Notes:** Great introduction to AI!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Submit this lab? (y/N): y

✓ Submission Successful!
Your submission has been recorded!
```

---

## Submission Script Reference

### Quick Command Reference

**Linux/Mac:**
```bash
./scripts/submit-lab.sh <session> <lab> ["optional notes"]
```

**Windows:**
```powershell
.\scripts\submit-lab.ps1 <session> <lab> "optional notes"
```

### Common Usage Examples

**Session 1 - All Labs:**
```bash
./scripts/submit-lab.sh 1 1
./scripts/submit-lab.sh 1 2
./scripts/submit-lab.sh 1 3
./scripts/submit-lab.sh 1 4
./scripts/submit-lab.sh 1 5
./scripts/submit-lab.sh 1 6
```

**With Notes (Recommended):**
```bash
./scripts/submit-lab.sh 2 1 "Excellent introduction to LangChain"
./scripts/submit-lab.sh 2 2 "LCEL is very powerful!"
./scripts/submit-lab.sh 5 3 "RAG implementation works great"
```

**Batch Submission (After completing multiple labs):**
```bash
# Linux/Mac
for lab in {1..6}; do
  ./scripts/submit-lab.sh 1 $lab
done
```

```powershell
# Windows PowerShell
1..6 | ForEach-Object {
  .\scripts\submit-lab.ps1 1 $_
}
```

### Issue Number Mapping

**The script automatically calculates issue numbers - you don't need to look these up!**

But for reference:

| Session | Labs | Issue Range | Example |
|---------|------|-------------|---------|
| 1 | 1-6 | #1 - #6 | `./scripts/submit-lab.sh 1 1` → Issue #1 |
| 2 | 1-8 | #7 - #14 | `./scripts/submit-lab.sh 2 1` → Issue #7 |
| 3 | 1-7 | #15 - #21 | `./scripts/submit-lab.sh 3 1` → Issue #15 |
| 12 | 1-9 | #86 - #94 | `./scripts/submit-lab.sh 12 9` → Issue #94 |
| 15 | 1-8 | #111 - #118 | `./scripts/submit-lab.sh 15 8` → Issue #118 |

---

## Quick Commands

### Check Your Identity

```bash
# Verify what will be used for submissions
git config user.name
git config user.email
```

### View Your Submissions

```bash
# See all your lab submissions
gh issue list --repo brainupgrade-in/aiagentic-comp \
  --label lab-tracking \
  --search "commenter:@me"

# Count how many labs you've submitted
gh issue list --repo brainupgrade-in/aiagentic-comp \
  --search "commenter:@me" \
  --label lab-tracking \
  --json number | jq 'length'
```

### View Specific Lab Issue

```bash
# View issue in terminal
gh issue view 1 --repo brainupgrade-in/aiagentic-comp

# View issue in browser
gh issue view 1 --repo brainupgrade-in/aiagentic-comp --web
```

### Script Help

```bash
# Linux/Mac - view usage
./scripts/submit-lab.sh

# Windows - view usage
.\scripts\submit-lab.ps1
```

---

## Tips & Best Practices

### ✅ Do

- ✅ Set your git config (Step 4) before first submission
- ✅ Submit immediately after validation passes
- ✅ Include notes about challenges or key learnings
- ✅ Use the submission script (automatic and error-free)
- ✅ Verify your username/email before submitting
- ✅ Review the preview before confirming submission

### ❌ Don't

- ❌ Submit without running validation (all [PASS] markers)
- ❌ Leave TODO placeholders (___) unfilled
- ❌ Skip setting git config (submissions won't have your name)
- ❌ Post multiple "completed" comments on same issue
- ❌ Use issues for asking questions (use Zoom chat)

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

### "Could not detect GitHub username"

**Cause:** Git config not set

**Fix:**
```bash
cd ~/aiagentic-comp
git config user.name "your-github-username"
git config user.email "your-email@example.com"
```

### "Submission Failed" or "GitHub CLI not authenticated"

**Cause:** Not logged in with the shared token

**Fix:**
```bash
gh auth login
# Use the token shared by instructor
gh auth status  # Verify authentication
```

### Script shows wrong username

**Cause:** Using system-wide git config instead of repository config

**Fix:**
```bash
# Set repository-specific config (overrides global)
cd ~/aiagentic-comp
git config user.name "your-correct-username"
git config user.email "your-correct-email"

# Verify
git config user.name
git config user.email
```

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

# Open Jupyter and complete labs
jupyter notebook hands-on/session-1/

# Complete Lab 01
# ... work through notebook ...
# All validation cells show [PASS]

# Submit Lab 01
./scripts/submit-lab.sh 1 1 "Great introduction to AI agents!"
# Confirm with 'y' when prompted

# Complete Lab 02
# ... work through notebook ...
# All validation cells show [PASS]

# Submit Lab 02
./scripts/submit-lab.sh 1 2 "Learned about reasoning patterns"

# Continue for Labs 03-06
./scripts/submit-lab.sh 1 3
./scripts/submit-lab.sh 1 4
./scripts/submit-lab.sh 1 5
./scripts/submit-lab.sh 1 6

# End of Session 1: You've submitted all 6 labs
# Check your progress:
gh issue list --repo brainupgrade-in/aiagentic-comp --search "commenter:@me"
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
