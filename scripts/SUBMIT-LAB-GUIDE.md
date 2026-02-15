# Lab Submission Scripts - Usage Guide

Easy-to-use scripts for participants to submit lab completions with a single command.

## Overview

Instead of manually finding issue numbers and typing gh commands, participants can use these scripts:

- **`submit-lab.sh`** - For Linux/Mac users
- **`submit-lab.ps1`** - For Windows PowerShell users

Both scripts:
- ✅ Auto-detect your GitHub username
- ✅ Calculate correct issue number automatically
- ✅ Submit with consistent format
- ✅ Show confirmation and URL
- ✅ Colorful, user-friendly output

---

## Quick Start

### Linux / Mac

```bash
# Make executable (first time only)
chmod +x scripts/submit-lab.sh

# Submit a lab
./scripts/submit-lab.sh 1 1

# With optional notes
./scripts/submit-lab.sh 1 2 "Great lab on AI agents!"
```

### Windows PowerShell

```powershell
# Submit a lab
.\scripts\submit-lab.ps1 1 1

# With optional notes
.\scripts\submit-lab.ps1 1 2 "Great lab on AI agents!"
```

---

## Usage Examples

### Example 1: Basic Submission

```bash
./scripts/submit-lab.sh 1 1
```

**Output:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Lab Submission - Agentic AI Course
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Session: 1
Lab: 1
Issue Number: #1

Detecting your GitHub username...
✓ GitHub username: johndoe

✓ GitHub CLI authenticated

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Comment Preview:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Completed

**Participant:** johndoe
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
./scripts/submit-lab.sh 2 3 "Learned a lot about LangChain!"
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
./scripts/submit-lab.sh 12 9 "LangFuse integration works great"
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

### Username Detection

The script tries these methods in order:

1. **GitHub CLI:** `gh api user --jq '.login'`
2. **Git config:** `git config --get user.name`

**Set your username:**
```bash
# Option 1: Authenticate with gh (recommended)
gh auth login

# Option 2: Set git config
git config --global user.name "your-github-username"
```

---

## Troubleshooting

### "Could not detect GitHub username"

**Cause:** Neither gh CLI nor git config has your username

**Solution:**
```bash
# Set your GitHub username
git config --global user.name "johndoe"

# Or authenticate with gh
gh auth login
```

### "GitHub CLI not authenticated"

**Cause:** Not logged in with the shared token

**Solution:**
```bash
gh auth login
# Select: GitHub.com → HTTPS → Paste token
# Use the token shared by instructor
```

### "GitHub CLI (gh) not found"

**Cause:** GitHub CLI not installed

**Solution:**
```bash
# Ubuntu/Debian
sudo apt install gh

# macOS
brew install gh

# Windows
winget install GitHub.cli
```

### "Submission Failed"

**Possible causes:**
1. Wrong session/lab number
2. Not authenticated
3. No access to repository
4. Issue doesn't exist

**Debug:**
```bash
# Check authentication
gh auth status

# Check if you can access repo
gh repo view brainupgrade-in/aiagentic-comp

# Check if issue exists
gh issue view 1 --repo brainupgrade-in/aiagentic-comp
```

---

## Advanced Usage

### Batch Submission

Submit multiple labs at once:

```bash
# Linux/Mac
for lab in {1..6}; do
  ./scripts/submit-lab.sh 1 $lab
  sleep 1
done
```

```powershell
# Windows PowerShell
1..6 | ForEach-Object {
  .\scripts\submit-lab.ps1 1 $_
  Start-Sleep -Seconds 1
}
```

### Check Your Progress

```bash
# View all your submissions
gh issue list \
  --repo brainupgrade-in/aiagentic-comp \
  --search "commenter:@me" \
  --label lab-tracking

# Count completed labs
gh issue list \
  --repo brainupgrade-in/aiagentic-comp \
  --search "commenter:@me" \
  --label lab-tracking \
  --json number | jq 'length'
```

### Create Alias

Add to `~/.bashrc` or `~/.zshrc`:

```bash
alias submit-lab='cd ~/aiagentic-comp && ./scripts/submit-lab.sh'
```

Then use anywhere:
```bash
submit-lab 1 1
```

---

## Script Comparison

| Feature | submit-lab.sh | submit-lab.ps1 |
|---------|---------------|----------------|
| **Platform** | Linux, macOS | Windows |
| **Shell** | Bash | PowerShell 5.1+ |
| **Colors** | ✅ ANSI codes | ✅ Write-Host |
| **Auto username** | ✅ Yes | ✅ Yes |
| **Confirmation** | ✅ Yes | ✅ Yes |
| **Error handling** | ✅ Yes | ✅ Yes |

Both scripts have identical functionality!

---

## Integration with Workflow

### Daily Workflow

```bash
# 1. Pull latest updates
cd ~/aiagentic-comp
git pull

# 2. Activate environment
source .venv/bin/activate

# 3. Complete labs
jupyter notebook hands-on/session-1/

# 4. Submit completed labs
./scripts/submit-lab.sh 1 1
./scripts/submit-lab.sh 1 2
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
- ✅ Uses GitHub CLI authentication (secure)
- ✅ Shows preview before submitting
- ✅ Requires confirmation (y/N)
- ✅ No credentials stored in script

---

## Support

**Issues with script:**
- Check SUBMIT-LAB-GUIDE.md (this file)
- Verify GitHub CLI installation: `gh --version`
- Check authentication: `gh auth status`

**Issues with labs:**
- Review session presentations
- Check solution notebooks in `solutions/` directory
- Ask instructor during office hours

---

**Repository:** https://github.com/brainupgrade-in/aiagentic-comp
**Scripts Location:** `scripts/submit-lab.sh` and `scripts/submit-lab.ps1`
