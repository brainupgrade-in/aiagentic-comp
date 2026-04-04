# Lab Submission Monitoring Dashboard

Real-time interactive dashboard for tracking lab submission progress across the Agentic AI course.

## Features

- Real-time statistics — total participants, completions, overall progress
- Completion matrix — visual grid showing participant progress across all sessions
- Session details — per-lab breakdown for each session
- Modern UI — responsive design with color-coded status indicators
- Auto-refresh — optional automatic updates every 60 seconds
- Mobile friendly — responsive layout works on all devices

## Quick Start

```bash
# Generate dashboard
export GITHUB_TOKEN='your_token'
python3 reporting/generate-dashboard.py

# Open in browser
firefox reporting/dashboard.html
```

## Usage

### Basic Generation

```bash
cd ~/aiagentic-comp
python3 reporting/generate-dashboard.py
```

Creates `reporting/dashboard.html`.

### Custom Output File

```bash
python3 reporting/generate-dashboard.py --output reports/daily-report.html
```

### Auto-Refresh Mode

```bash
python3 reporting/generate-dashboard.py --auto-refresh
```

Enables automatic page refresh every 60 seconds (useful for live monitoring during course).

## Dashboard Sections

### 1. Summary Cards

- **Total Participants** — number of unique participants
- **Total Labs** — 119 labs across 15 sessions
- **Completions** — total lab submissions
- **Overall Progress** — percentage complete with progress bar

### 2. Completion Matrix

Table showing participant completion per session (e.g., "6/6" for Session 1), total completions (e.g., "45/119"), and progress percentage with color-coded badge:
- Green (90%+): Excellent progress
- Yellow (50-89%): Good progress
- Red (<50%): Needs attention

### 3. Session Details

For each session: title, progress bar, and per-participant lab completion grid (checked = completed, dash = pending).

## Automated Reporting

### Daily Reports

```bash
# Add to crontab
crontab -e

# Daily 6 PM generation
0 18 * * * cd ~/aiagentic-comp && export GITHUB_TOKEN='your_token' && python3 reporting/generate-dashboard.py --output reporting/daily-$(date +\%Y\%m\%d).html
```

### Course Monitoring

Keep a browser tab open with auto-refresh during course delivery:

```bash
python3 reporting/generate-dashboard.py --output reporting/live-dashboard.html --auto-refresh
firefox reporting/live-dashboard.html
```

## Integration with Tracking Script

```bash
export GITHUB_TOKEN='your_token'

# Text report
python3 scripts/track-lab-comments.py > reports/text-report.md

# Visual dashboard
python3 reporting/generate-dashboard.py --output reports/dashboard.html
```

## Customization

Edit `generate-dashboard.py` to adjust:
- **Refresh interval** (default: 60 seconds) — change the meta refresh value
- **Color scheme** — edit the CSS section (gradient background, status colors)

## Troubleshooting

### "Error: GITHUB_TOKEN environment variable not set"

```bash
export GITHUB_TOKEN='your_token_here'
```

### Dashboard shows "No submissions yet"

- No participants have commented on issues yet, or
- Token doesn't have read access to the repository, or
- Issues don't have the `lab-tracking` label

```bash
# Verify issues exist
gh issue list --repo brainupgrade-in/aiagentic-comp --label lab-tracking --limit 5

# Verify comments exist
gh issue view 1 --repo brainupgrade-in/aiagentic-comp --comments
```

### Dashboard doesn't update

The dashboard is static HTML — regenerate it to refresh data. Use `--auto-refresh` so the browser reloads the file automatically.

## Output Files

Generated HTML files are standalone (all CSS and JavaScript inline, no external dependencies). Safe to email or share.

## Example Workflow

**Morning check:**
```bash
cd ~/aiagentic-comp
export GITHUB_TOKEN='your_token'
python3 reporting/generate-dashboard.py --output reporting/morning-check.html
firefox reporting/morning-check.html
```

**After each session:**
```bash
python3 reporting/generate-dashboard.py --output reporting/session-1-complete.html
```

**End of course:**
```bash
python3 reporting/generate-dashboard.py --output reporting/final-completion-report.html
```

## Performance

- **Generation time:** ~5-10 seconds (depends on GitHub API response time)
- **File size:** ~50-100 KB (varies with number of participants)
- **API calls:** ~120 (1 for issue list + 1 per lab issue for comments)

## Security Notes

- Dashboard is read-only (only displays data)
- Token only needs read access to issues
- Generated HTML is static — no active code execution

## Dependencies

- Python 3.6+
- `requests` library (installed via `requirements.txt`)
- GitHub token with read access to repository

## Related Tools

- `scripts/track-lab-comments.py` — text-based completion report
- `scripts/create-lab-issues.py` — create lab tracking issues
- `LAB-TRACKING-COMMENT-BASED.md` — full tracking system documentation
