# Quick Reference - Lab Submission

## Setup (One-Time)

```bash
# 1. Install GitHub CLI
sudo apt install gh              # Ubuntu/Debian
brew install gh                  # macOS

# 2. Authenticate (use token from Zoom)
gh auth login

# 3. Clone repository
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp

# 4. Setup Python environment
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Daily Workflow

```bash
# 1. Pull updates & activate environment
cd ~/aiagentic-comp
git pull
source .venv/bin/activate

# 2. Open labs
jupyter notebook hands-on/session-N/

# 3. Complete labs (fill ___ placeholders, verify [PASS])

# 4. Submit each lab
gh issue comment <issue-number> \
  --repo brainupgrade-in/aiagentic-comp \
  --body "✅ Completed"
```

---

## Issue Numbers

| Session | Lab 01 | Lab 02 | Lab 03 | Lab 04 | Lab 05 | Lab 06 | Lab 07 | Lab 08 | Lab 09 |
|---------|--------|--------|--------|--------|--------|--------|--------|--------|--------|
| **1** | #1 | #2 | #3 | #4 | #5 | #6 | - | - | - |
| **2** | #7 | #8 | #9 | #10 | #11 | #12 | #13 | #14 | - |
| **3** | #15 | #16 | #17 | #18 | #19 | #20 | #21 | - | - |
| **4** | #22 | #23 | #24 | #25 | #26 | #27 | #28 | #29 | - |
| **5** | #30 | #31 | #32 | #33 | #34 | #35 | #36 | #37 | - |
| **6** | #38 | #39 | #40 | #41 | #42 | #43 | #44 | #45 | - |
| **7** | #46 | #47 | #48 | #49 | #50 | #51 | #52 | #53 | - |
| **8** | #54 | #55 | #56 | #57 | #58 | #59 | #60 | #61 | - |
| **9** | #62 | #63 | #64 | #65 | #66 | #67 | #68 | #69 | - |
| **10** | #70 | #71 | #72 | #73 | #74 | #75 | #76 | #77 | - |
| **11** | #78 | #79 | #80 | #81 | #82 | #83 | #84 | #85 | - |
| **12** | #86 | #87 | #88 | #89 | #90 | #91 | #92 | #93 | #94 |
| **13** | #95 | #96 | #97 | #98 | #99 | #100 | #101 | #102 | - |
| **14** | #103 | #104 | #105 | #106 | #107 | #108 | #109 | #110 | - |
| **15** | #111 | #112 | #113 | #114 | #115 | #116 | #117 | #118 | - |

---

## Common Commands

```bash
# View issue details
gh issue view <number> --repo brainupgrade-in/aiagentic-comp

# Check your submissions
gh issue list --repo brainupgrade-in/aiagentic-comp --search "commenter:@me"

# List all Session 1 labs
gh issue list --repo brainupgrade-in/aiagentic-comp --label "session-1"

# View all lab issues
https://github.com/brainupgrade-in/aiagentic-comp/issues?q=is:issue+label:lab-tracking
```

---

## Submission Template

**Basic:**
```bash
gh issue comment <issue-number> \
  --repo brainupgrade-in/aiagentic-comp \
  --body "✅ Completed"
```

**Detailed (recommended):**
```bash
gh issue comment <issue-number> \
  --repo brainupgrade-in/aiagentic-comp \
  --body "✅ Completed

**Validation:** All checks passed
**Notes:** [Your notes]"
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `gh: command not found` | Install: `sudo apt install gh` |
| Token error | Re-run: `gh auth login` with Zoom token |
| Module not found | Activate venv: `source .venv/bin/activate` |
| Wrong issue number | Check table above |

---

## Support

- **Zoom chat:** Questions during session
- **Instructor:** Technical issues during breaks
- **Repository:** https://github.com/brainupgrade-in/aiagentic-comp

---

**🎯 Goal:** Comment "✅ Completed" on all 118 lab issues!
