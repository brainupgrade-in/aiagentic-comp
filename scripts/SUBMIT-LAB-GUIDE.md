# Lab Submission Script — Usage Guide

Easy-to-use script for participants to submit lab completions with a single command.

## Overview

Instead of manually finding issue numbers and typing `gh` commands, use:

- **`submit-lab.sh`** — Linux, macOS, and Windows (Git Bash)

The script:
- Auto-detects your GitHub username
- Calculates the correct issue number automatically
- Submits with consistent format
- Shows a confirmation preview and asks before posting

---

## Quick Start

### 1. Add your GitHub PAT to `.env`

```bash
# In the repo root, open .env and add:
GITHUB_TOKEN=ghp_xxxx
```

Or export it for the session:

```bash
export GITHUB_TOKEN=ghp_xxxx
```

> Get a token at https://github.com/settings/tokens — needs **`public_repo`** scope (or use the token shared by the instructor).

### 2. Submit a lab

```bash
bash scripts/submit-lab.sh 1 1

# With optional notes
bash scripts/submit-lab.sh 1 2 "Great lab on AI agents!"
```

> **Windows users:** Open Git Bash and use the same `bash scripts/submit-lab.sh` commands as Linux/macOS.

---

## Usage Examples

### Example 1: Basic Submission

```bash
bash scripts/submit-lab.sh 1 1
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Lab Submission - Agentic AI Course
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: 1
Lab: 1
Issue Number: #1

Detecting your information...
✓ Username: johndoe
✓ Email: johndoe@example.com

✓ GitHub token found

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Comment Preview:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Completed

**Participant:** johndoe (johndoe@example.com)
**Validation:** All checks passed
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Submit this lab? (y/N): y

Submitting to Issue #1...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Submission Successful!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: 1 | Lab: 1 | Issue: #1
Comment: https://github.com/brainupgrade-in/aiagentic-comp/issues/1#issuecomment-...

Your submission has been recorded!
```

### Example 2: With Notes

```bash
bash scripts/submit-lab.sh 2 3 "Learned a lot about LangChain!"
```

**Comment posted:**
```
✅ Completed

**Participant:** johndoe
**Validation:** All checks passed
**Notes:** Learned a lot about LangChain!
```

### Example 3: Session 12 Lab 9

```bash
bash scripts/submit-lab.sh 12 9 "LangFuse integration works great"
```

Automatically submits to Issue #94 (Session 12 Lab 9).

---

## How It Works

### Issue Number Calculation

The script automatically calculates the correct issue number:

| Session | Lab Range | Issue Range |
|---------|-----------|-------------|
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

**Formula:**
```
Session 1 Lab 1 → Issue #1
Session 2 Lab 1 → Issue #7
Session 2 Lab 5 → Issue #11
etc.
```

### Username & Email Detection

The script tries these methods in order:

1. **Repository git config (preferred):** `git config --local user.name` and `user.email`
2. **Global git config:** `git config --global user.name` and `user.email`

**Set your information (recommended):**
```bash
cd ~/aiagentic-comp

git config user.name "your-github-username"
git config user.email "your-email@example.com"
```

### Token Resolution Order

1. `GITHUB_TOKEN` environment variable (if already exported)
2. `GITHUB_TOKEN=` entry in `.env` file in the repo root

---

## Troubleshooting

### "Could not detect GitHub username"

**Cause:** Git config not set

**Solution:**
```bash
git config user.name "your-github-username"
git config user.email "your-email@example.com"
```

### "GITHUB_TOKEN not set"

**Cause:** Token not in environment or `.env`

**Solution:**
```bash
# Option A: add to .env
echo 'GITHUB_TOKEN=ghp_xxxx' >> .env

# Option B: export for current session
export GITHUB_TOKEN=ghp_xxxx
```

### "Submission Failed"

**Possible causes:**
1. Token expired or lacks `public_repo` scope
2. Wrong session/lab number
3. Issue doesn't exist

**Debug:**
```bash
# Test token manually
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/brainupgrade-in/aiagentic-comp/issues/1 \
  | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('title', d.get('message')))"
```

---

## Advanced Usage

### Batch Submission

Submit multiple labs at once:

```bash
# Linux/macOS/Windows Git Bash
for lab in {1..6}; do
  bash scripts/submit-lab.sh 1 $lab
  sleep 1
done
```

### Check Your Progress

Visit:
```
https://github.com/brainupgrade-in/aiagentic-comp/issues?q=label%3Alab-tracking
```

### Create Alias

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias submit-lab='cd ~/aiagentic-comp && bash scripts/submit-lab.sh'
```

Then use anywhere:
```bash
submit-lab 1 1
```

---

## Integration with Workflow

### Daily Workflow

```bash
# 1. Pull latest updates
cd ~/aiagentic-comp
git pull

# 2. Activate environment
source .venv/bin/activate

# 3. Complete labs in VS Code
code hands-on/session-1/

# 4. Submit completed labs
bash scripts/submit-lab.sh 1 1
bash scripts/submit-lab.sh 1 2
# etc.
```

### End of Session Checklist

- [ ] All lab notebooks run without errors
- [ ] All validation cells show `[PASS]`
- [ ] Submitted all labs using the script
- [ ] Verified submissions on GitHub

---

## Security Notes

- ✅ Script only **reads** your username (no modifications)
- ✅ Token read from env or `.env` — never hardcoded in script
- ✅ Shows preview before submitting
- ✅ Requires confirmation (y/N)
- ✅ `.env` is gitignored — token stays local

---

## Support

**Issues with script:**
- Check SUBMIT-LAB-GUIDE.md (this file)
- Test your token with the curl debug command above

**Issues with labs:**
- Review session presentations
- Check solution notebooks in `solutions/` directory
- Ask instructor during office hours

---

**Repository:** https://github.com/brainupgrade-in/aiagentic-comp
**Script:** `scripts/submit-lab.sh` (Linux, macOS, Windows Git Bash)
