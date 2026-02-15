# Lab Tracking System - Instructor Summary

## ✅ What's Been Created

### GitHub Issues
- **118 lab tracking issues** created (#1 - #118)
- **Labels created:**
  - `lab-tracking` (main label)
  - `session-1` through `session-15`
  - `lab-01` through `lab-09`

### Documentation Files
1. **`PARTICIPANT-INSTRUCTIONS.md`** - Complete setup and usage guide (share this)
2. **`PARTICIPANT-QUICK-REFERENCE.md`** - One-page cheat sheet (print/share this)
3. **`LAB-TRACKING-COMMENT-BASED.md`** - Full system documentation
4. **`INSTRUCTOR-SUMMARY.md`** - This file

### Scripts
1. **`scripts/create-lab-issues.py`** - ✅ Already executed (118 issues created)
2. **`scripts/track-lab-comments.py`** - Track completion by parsing comments

---

## 🎯 How It Works

### Participant Workflow
1. **Setup:** Authenticate with shared token (you'll share via Zoom)
2. **Complete labs:** Work through Jupyter notebooks
3. **Submit:** Comment "✅ Completed" on the corresponding issue
4. **Done:** Their GitHub username is automatically recorded

### Your Tracking Workflow
```bash
# Daily check - see who completed what
export GITHUB_TOKEN='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'
python3 scripts/track-lab-comments.py

# Check specific session
python3 scripts/track-lab-comments.py --session 1

# Check specific participant
python3 scripts/track-lab-comments.py --participant john-doe
```

---

## 📋 Before Day 1

### Share with Participants (via Zoom/Email)

**1. Send these files:**
- `PARTICIPANT-INSTRUCTIONS.md` (main guide)
- `PARTICIPANT-QUICK-REFERENCE.md` (cheat sheet)

**2. Share the token during Zoom session:**
```
Token for GitHub authentication:
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

Permissions: Read repo + Comment on issues
Valid until: [Set expiration when you created it]
```

⚠️ **Note:** This token should be created fresh with proper expiration. The one above is your admin token - you should create a separate read-only token for participants.

**3. Participant setup checklist (before Day 1):**
- [ ] Install GitHub CLI (`gh`)
- [ ] Authenticate with shared token
- [ ] Clone repository
- [ ] Setup Python virtual environment
- [ ] Install dependencies

---

## 📊 Daily Tracking During Course

### Quick Dashboard View

**Browser:** https://github.com/brainupgrade-in/aiagentic-comp/issues?q=is:issue+label:lab-tracking

**Filter by session:**
- Session 1: Add `label:session-1` to search
- Session 2: Add `label:session-2` to search

**Check specific lab:**
```bash
gh issue view 1 --repo brainupgrade-in/aiagentic-comp --comments
```

### Generate Reports

**After Session 1 (end of Day 1):**
```bash
python3 scripts/track-lab-comments.py --session 1
```

**Output example:**
```
| Participant | S1 | Completed |
|-------------|-----|-----------|
| john-doe    | 6/6 | 6/6      |
| jane-smith  | 5/6 | 5/6      |
| bob-jones   | 4/6 | 4/6      |

## Session 1 Details

| Lab | john-doe | jane-smith | bob-jones |
|-----|----------|------------|-----------|
| 01  | ✅       | ✅         | ✅        |
| 02  | ✅       | ✅         | ✅        |
| 03  | ✅       | ✅         | ✅        |
| 04  | ✅       | ✅         | ✅        |
| 05  | ✅       | ✅         | —         |
| 06  | ✅       | —          | —         |
```

**Weekly (end of each day):**
```bash
python3 scripts/track-lab-comments.py > reports/day-1-completion.md
```

**Final (end of course):**
```bash
python3 scripts/track-lab-comments.py > final-completion-report.md
```

---

## 🔍 Common Queries

### Who completed Session 1 Lab 01?
```bash
gh issue view 1 --repo brainupgrade-in/aiagentic-comp --comments
```

### Who hasn't submitted any labs yet?
```bash
# Run tracking script and look for participants with 0/118
python3 scripts/track-lab-comments.py | grep "0/118"
```

### How many completed Session 1?
```bash
gh issue list --label "session-1" --json number,comments | \
  jq '.[] | {issue: .number, completions: .comments}'
```

### Export all data to CSV
```bash
gh issue list \
  --label lab-tracking \
  --state all \
  --limit 200 \
  --json number,title,comments,labels \
  > lab-tracking-data.json
```

---

## 🎓 Certificate/Completion Criteria

**Full completion:** 118/118 labs
**Partial completion:** Define your own threshold (e.g., 80% = 95/118)

**End of course - identify completers:**
```bash
python3 scripts/track-lab-comments.py | grep -E "118/118|11[0-7]/118"
```

---

## 📞 Support During Course

### Participant asks: "How do I submit?"
**Answer:** "Comment '✅ Completed' on the issue. For Session 1 Lab 01, that's issue #1. Use the quick reference card."

### Participant asks: "What's the issue number for Session X Lab Y?"
**Answer:** "Check the table in the quick reference or run: `gh issue list --label session-X`"

### Participant asks: "Token doesn't work"
**Solution:**
1. Verify they're using correct token (shared in Zoom)
2. Re-authenticate: `gh auth login`
3. Test: `gh issue list --repo brainupgrade-in/aiagentic-comp --limit 3`

### Participant asks: "Can I see my progress?"
**Answer:** "Yes! Run: `gh issue list --repo brainupgrade-in/aiagentic-comp --search 'commenter:@me'`"

---

## 🔒 Security Note

**Shared Token:**
- ✅ Convenient (one token for all)
- ⚠️ If leaked, affects all participants
- 🔄 Can be regenerated if needed (participants re-authenticate)

**Best practice:**
- Set token expiration to course end date + 7 days
- Monitor for unusual activity
- Revoke after course ends

**To regenerate if compromised:**
1. Delete old token in GitHub settings
2. Create new token with same permissions
3. Share new token with participants
4. Participants re-run: `gh auth login`

---

## 📂 File Locations

```
Oracle/
├── PARTICIPANT-INSTRUCTIONS.md          # Share with participants
├── PARTICIPANT-QUICK-REFERENCE.md       # Print/share as cheat sheet
├── LAB-TRACKING-COMMENT-BASED.md       # Full documentation
├── INSTRUCTOR-SUMMARY.md                # This file
├── scripts/
│   ├── create-lab-issues.py            # ✅ Already run
│   ├── track-lab-comments.py           # Run daily
│   └── ...
└── .github/
    └── ISSUE_TEMPLATE/
        └── lab-submission.yml           # (Not used for comment-based approach)
```

---

## ✅ Pre-Course Checklist

- [x] Created 118 lab tracking issues
- [x] Created all necessary labels
- [x] Created participant instructions
- [x] Created quick reference guide
- [x] Tested tracking script
- [ ] Create participant-specific read-only token (recommended vs sharing admin token)
- [ ] Share instructions with participants (via email/LMS)
- [ ] Share token during Zoom session
- [ ] Test with one participant before Day 1
- [ ] Create reports/ directory for daily tracking exports

---

## 🚀 Day 1 Checklist

**Before session:**
- [ ] Verify all 118 issues are visible
- [ ] Have token ready to share
- [ ] Open participant instructions for screen sharing

**During session:**
- [ ] Share token in Zoom chat
- [ ] Walk through setup steps (5-10 minutes)
- [ ] Have 1-2 participants test submission on first lab
- [ ] Verify comments appear on issues

**After session:**
- [ ] Run tracking script
- [ ] Check for participants who didn't submit
- [ ] Follow up with lagging participants

---

## 📈 Success Metrics

Track these throughout the course:
- **Daily completion rate:** % of participants completing that day's labs
- **Cumulative completion:** Total labs completed / 118
- **Lagging participants:** Who's falling behind?
- **Popular issues:** Which labs have most comments/questions?

---

## Quick Command Reference

```bash
# Your daily routine
export GITHUB_TOKEN='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'
cd ~/Training/Oracle

# Generate report
python3 scripts/track-lab-comments.py

# Check specific session
python3 scripts/track-lab-comments.py --session 1

# View issues in browser
firefox 'https://github.com/brainupgrade-in/aiagentic-comp/issues?q=is:issue+label:lab-tracking'

# Quick check via CLI
gh issue list --repo brainupgrade-in/aiagentic-comp --label "session-1"
```

---

**System is ready!** Share instructions with participants and you're good to go! 🎉

**Questions?** Refer to `LAB-TRACKING-COMMENT-BASED.md` for detailed documentation.
