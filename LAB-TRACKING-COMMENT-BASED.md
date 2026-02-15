# Lab Tracking System - Comment-Based Approach

## Overview

**Architecture:**
- **117 lab issues** created by instructor (one per lab)
- **20 participants** comment "done" on each issue when completed
- **Dashboard/filters** track completion per participant per lab

**Benefits:**
- ✅ Centralized tracking (117 issues vs 300+ individual submissions)
- ✅ Easy filtering by specific lab
- ✅ All questions/discussion about a lab in one place
- ✅ Simple participant workflow (just comment)
- ✅ Visual dashboard with GitHub Projects
- ✅ Automatic username tracking (no manual entry)

---

## Token Setup

### Option A: Individual Tokens (Recommended - More Secure)

**Each participant creates their own token:**
- **Contents:** Read-only
- **Issues:** Read and write
- **Repository:** `brainupgrade-in/aiagentic-comp`

**Benefits:**
- If one token leaked, only that participant affected
- Better security audit trail
- Standard GitHub best practice

### Option B: Shared Token (Simpler - Less Secure)

**You create one token and share with all participants:**
- **Contents:** Read-only
- **Issues:** Read and write

**Risks:**
- ⚠️ If token leaked, all participants affected
- ⚠️ Need to regenerate and reshare if compromised
- ⚠️ Cannot track individual token usage

**Recommendation:** Use **Option A** unless you have specific constraints

---

## Instructor Setup (One-Time)

### Step 1: Create Labels

```bash
export GITHUB_TOKEN="your_admin_token"

# Create tracking label
gh label create "lab-tracking" \
  --repo brainupgrade-in/aiagentic-comp \
  --color "1D76DB" \
  --description "Lab completion tracking issue"

# Create session labels (1-15)
for i in {1..15}; do
  gh label create "session-$i" \
    --repo brainupgrade-in/aiagentic-comp \
    --color "0E8A16" \
    --description "Session $i labs"
done

# Create lab labels (01-09)
for i in $(seq -w 1 9); do
  gh label create "lab-$i" \
    --repo brainupgrade-in/aiagentic-comp \
    --color "FBCA04" \
    --description "Lab $i"
done
```

### Step 2: Create 117 Lab Issues

```bash
# Install dependencies
pip install requests

# Run issue creation script
python3 scripts/create-lab-issues.py
```

**Output:**
```
Creating lab tracking issues...
Repository: brainupgrade-in/aiagentic-comp
Total issues to create: 117

Session 1: Introduction to Agentic AI (6 labs)
  ✓ Created issue #101: Session 1 Lab 01
  ✓ Created issue #102: Session 1 Lab 02
  ...

Session 15: Capstone Project (8 labs)
  ✓ Created issue #217: Session 15 Lab 08

Summary:
  Created: 117
  Failed: 0
  Total: 117

View issues: https://github.com/brainupgrade-in/aiagentic-comp/issues?q=is:issue+label:lab-tracking
```

### Step 3: Setup GitHub Projects Dashboard

**Create project:**
1. Go to repository → **Projects** → **New project**
2. Name: "Lab Completion Tracker"
3. Select **Table** view

**Configure columns:**
- Issue number (default)
- Title (default)
- Status (default)
- Labels (default)
- Assignees (default)

**Add automation:**
1. **Workflow:** Item added to project
   - Action: Set status to "📝 Awaiting Completions"

2. **Workflow:** Item closed
   - Action: Set status to "✅ All Completed"

**Filter examples:**
- Session 1 labs: `label:session-1`
- Lab 01 across all sessions: `label:lab-01`
- Specific lab: `Session 3 - Lab 05`

---

## Participant Workflow

### Setup (One-Time)

**1. Create fine-grained token** (if using Option A):
- Go to: https://github.com/settings/tokens?type=beta
- Token name: "Agentic AI Course"
- Repository: `brainupgrade-in/aiagentic-comp`
- Permissions:
  - Contents: Read-only
  - Issues: Read and write

**2. Authenticate GitHub CLI:**
```bash
gh auth login
# Paste your token
```

**3. Clone repository:**
```bash
git clone https://github.com/brainupgrade-in/aiagentic-comp.git
cd aiagentic-comp
```

### Daily Workflow

**After completing each lab:**

```bash
# Example: Completed Session 1 Lab 01

# Method 1: Using GitHub CLI (recommended)
gh issue comment <issue-number> \
  --repo brainupgrade-in/aiagentic-comp \
  --body "✅ Completed

**Validation:** All checks passed ([PASS] markers present)
**Notes:** Great introduction to agentic AI concepts!"

# Method 2: Using GitHub web UI
# 1. Go to issue page
# 2. Add comment
# 3. Submit
```

**Find issue number:**
```bash
# List all Session 1 labs
gh issue list \
  --repo brainupgrade-in/aiagentic-comp \
  --label "session-1,lab-tracking"

# Search for specific lab
gh issue list \
  --repo brainupgrade-in/aiagentic-comp \
  --search "Session 1 - Lab 01"
```

**Comment template:**
```markdown
✅ Completed

**Validation:** All checks passed
**Screenshot:** [Optional: Attach output screenshot]
**Challenges:** [Optional: Any difficulties faced]
**Time taken:** [Optional: Approximate time]
**Notes:** [Optional: Key learnings]
```

---

## Instructor Tracking

### Daily Quick Check

**View pending labs (no completions yet):**
```bash
gh issue list \
  --repo brainupgrade-in/aiagentic-comp \
  --label lab-tracking \
  --state open \
  --json number,title,comments \
  --jq '.[] | select(.comments == 0) | .number, .title'
```

**Check Session 1 progress:**
```bash
gh issue list \
  --label "session-1,lab-tracking" \
  --json number,title,comments
```

### Generate Completion Matrix

**Full report:**
```bash
export GITHUB_TOKEN="your_read_only_token"
python3 scripts/track-lab-comments.py
```

**Filter by session:**
```bash
python3 scripts/track-lab-comments.py --session 1
```

**Filter by participant:**
```bash
python3 scripts/track-lab-comments.py --participant john-doe
```

**Example output:**
```
# Lab Completion Report (Comment-Based)

**Generated:** 2026-02-15 10:00:00
**Repository:** brainupgrade-in/aiagentic-comp

**Total Participants:** 20
**Total Lab Completions:** 450

## Completion Matrix

| Participant | S1 | S2 | S3 | S4 | S5 | ... | Total | Progress |
|-------------|----|----|----|----|----|----|-------|----------|
| john-doe    | 6/6 | 8/8 | 5/7 | 0/8 | 0/8 | ... | 19/117 | 16% |
| jane-smith  | 6/6 | 8/8 | 7/7 | 8/8 | 0/8 | ... | 29/117 | 25% |
| bob-jones   | 6/6 | 7/8 | 0/7 | 0/8 | 0/8 | ... | 13/117 | 11% |

## Session Details

### Session 1: Introduction to Agentic AI

| Lab | john-doe | jane-smith | bob-jones | ... |
|-----|----------|------------|-----------|-----|
| 01  | ✅       | ✅         | ✅        | ... |
| 02  | ✅       | ✅         | ✅        | ... |
| 03  | ✅       | ✅         | ✅        | ... |
| 04  | ✅       | ✅         | ✅        | ... |
| 05  | ✅       | ✅         | ✅        | ... |
| 06  | ✅       | ✅         | ✅        | ... |

### Session 2: AI Coding Assistants & Vibe Coding

| Lab | john-doe | jane-smith | bob-jones | ... |
|-----|----------|------------|-----------|-----|
| 01  | ✅       | ✅         | ✅        | ... |
| 02  | ✅       | ✅         | ✅        | ... |
| 03  | ✅       | ✅         | ✅        | ... |
| 04  | ✅       | ✅         | ✅        | ... |
| 05  | ✅       | ✅         | ✅        | ... |
| 06  | ✅       | ✅         | ✅        | ... |
| 07  | ✅       | ✅         | ✅        | ... |
| 08  | ✅       | ✅         | —         | ... |

## Pending Labs

### bob-jones
- Session 2 Lab 08
- Session 3 Lab 01
- Session 3 Lab 02
- ... and 104 more
```

### GitHub Projects Dashboard

**View in browser:**
1. Go to: https://github.com/brainupgrade-in/aiagentic-comp/projects/1
2. Filter by:
   - Session: `label:session-1`
   - Specific lab: `Session 1 - Lab 01`

**Table view shows:**
- Issue title (e.g., "Session 1 - Lab 01")
- Number of comments (completion count)
- Labels (session, lab)
- Status (open/closed)

**Board view shows:**
- Columns: No Completions, Some Completions, All Completed
- Drag issues between columns manually or auto-based on comment count

### Review Participant Work

**View who completed a specific lab:**
```bash
# Example: Session 1 Lab 01
gh issue view <issue-number> --comments

# See all usernames who commented
```

**Check participant's overall progress:**
```bash
# Search all labs for participant's comments
gh issue list \
  --label lab-tracking \
  --search "commenter:john-doe" \
  --json number,title
```

---

## Advanced Features

### Auto-Close Issues

When all 20 participants complete a lab, auto-close the issue:

```bash
# Check comment count
gh api /repos/brainupgrade-in/aiagentic-comp/issues/<issue-number> \
  --jq '.comments'

# If comments >= 20 (all participants completed)
gh issue close <issue-number> \
  --comment "✅ All participants completed this lab!"
```

### Weekly Progress Report

```bash
# Generate weekly report
python3 scripts/track-lab-comments.py > weekly-report-$(date +%Y%m%d).md

# Email to stakeholders or save for records
```

### Identify Lagging Participants

```bash
# Participants with < 10% completion
python3 scripts/track-lab-comments.py | \
  grep -E "[0-9]+%" | \
  awk -F'|' '$NF ~ /[0-9]%/ && $NF !~ /[1-9][0-9]%/ {print $2}' | \
  tr -d ' '
```

### Export to CSV

```bash
# Export issue data
gh issue list \
  --label lab-tracking \
  --state all \
  --limit 1000 \
  --json number,title,labels,comments,state \
  --jq '.[] | [.number, .title, .comments, .state] | @csv' \
  > lab-tracking-export.csv
```

---

## Comparison: Comment vs PR-Based Tracking

| Aspect | Comment-Based (This Approach) | PR-Based (Previous) |
|--------|------------------------------|---------------------|
| **Issues Created** | 117 (one per lab) | 300+ (20 participants × 15 sessions) |
| **Participant Workflow** | Comment on issue | Create PR with branch |
| **Centralization** | All feedback for Lab 01 in one place | Scattered across 20 PRs |
| **Filtering** | Easy: `label:lab-01` | Harder: Need to aggregate |
| **Token Needed** | Read + Issue write | Read + Contents write |
| **GitHub Skills** | Minimal (just comment) | Higher (branch, commit, PR) |
| **Merge Conflicts** | None | Possible |
| **Best For** | Non-git-savvy participants, quick tracking | Git learning, code review practice |

---

## Troubleshooting

### Participant can't comment

**Check:**
1. Token has **Issues: Read and write** permission
2. Token scoped to correct repository
3. Re-authenticate: `gh auth login`

### Issue not found

**Find issue number:**
```bash
gh issue list \
  --label lab-tracking \
  --search "Session 1 Lab 01" \
  --json number,title
```

### Tracking script shows no data

**Check:**
1. Issues have `lab-tracking` label
2. Comments contain completion markers (`✅`, `completed`, `done`)
3. GITHUB_TOKEN is set correctly

---

## Best Practices

### For Participants

- ✅ Comment immediately after validation passes
- ✅ Include screenshot if output is visual
- ✅ Mention challenges to help instructor improve course
- ❌ Don't spam multiple comments for same lab
- ❌ Don't use issue for questions (use discussions or separate issues)

### For Instructor

- ✅ Run tracking script daily during course
- ✅ Check dashboard for lagging participants
- ✅ Provide encouragement in issue comments
- ✅ Close issues when all participants complete
- ✅ Export final data for certificates/records

---

## Quick Reference

```bash
# Instructor: Create all 117 issues
python3 scripts/create-lab-issues.py

# Instructor: Generate completion report
python3 scripts/track-lab-comments.py

# Instructor: Check Session 1 progress
python3 scripts/track-lab-comments.py --session 1

# Participant: Find issue number
gh issue list --label "session-1" --search "Lab 01"

# Participant: Submit completion
gh issue comment <number> --body "✅ Completed"

# View dashboard
https://github.com/brainupgrade-in/aiagentic-comp/projects/1
```

---

**Ready to implement?**
1. Create labels
2. Run `create-lab-issues.py`
3. Set up GitHub Projects dashboard
4. Share participant instructions
5. Start tracking!
