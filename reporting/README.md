# Lab Submission Monitoring Dashboard

Real-time interactive dashboard for tracking lab submission progress across the Agentic AI course.

## Features

- 📊 **Real-time statistics** - Total participants, completions, overall progress
- 📈 **Completion matrix** - Visual grid showing participant progress across all sessions
- 🎯 **Session details** - Per-lab breakdown for each session
- 🎨 **Modern UI** - Responsive design with color-coded status indicators
- ♻️ **Auto-refresh** - Optional automatic updates every 60 seconds
- 📱 **Mobile friendly** - Responsive layout works on all devices

## Quick Start

```bash
# Generate dashboard
export GITHUB_TOKEN='your_token'
python3 generate-dashboard.py

# Open in browser
firefox dashboard.html
```

## Usage

### Basic Generation

```bash
python3 generate-dashboard.py
```

This creates `dashboard.html` in the current directory.

### Custom Output File

```bash
python3 generate-dashboard.py --output reports/daily-report.html
```

### Auto-Refresh Mode

```bash
python3 generate-dashboard.py --auto-refresh
```

Enables automatic page refresh every 60 seconds (useful for live monitoring during course).

### Full Example

```bash
# Set your GitHub token
export GITHUB_TOKEN='ghp_your_token_here'

# Generate dashboard with auto-refresh
python3 generate-dashboard.py --output dashboard.html --auto-refresh

# Open in browser (Linux)
firefox dashboard.html

# Or (macOS)
open dashboard.html

# Or manually open in any browser
```

## Dashboard Sections

### 1. Summary Cards

- **Total Participants** - Number of unique participants
- **Total Labs** - 118 labs across 15 sessions
- **Completions** - Total lab submissions
- **Overall Progress** - Percentage complete with progress bar

### 2. Completion Matrix

Table view showing:
- Participant names
- Completion count per session (e.g., "6/6" for Session 1)
- Total completions (e.g., "45/118")
- Overall progress percentage with color-coded badge:
  - 🟢 Green (90%+): Excellent progress
  - 🟡 Yellow (50-89%): Good progress
  - 🔴 Red (<50%): Needs attention

### 3. Session Details

For each session:
- Session title and progress bar
- Per-participant lab completion grid
- ✅ = Completed
- — = Pending

## Automated Reporting

### Daily Reports

Schedule daily dashboard generation:

```bash
# Add to crontab
crontab -e

# Add this line for daily 6 PM generation
0 18 * * * cd /home/rajesh/Training/Oracle/reporting && export GITHUB_TOKEN='your_token' && python3 generate-dashboard.py --output daily-$(date +\%Y\%m\%d).html
```

### Course Monitoring

Keep a browser tab open with auto-refresh during course delivery:

```bash
python3 generate-dashboard.py --output live-dashboard.html --auto-refresh
firefox live-dashboard.html
```

The dashboard will update every 60 seconds automatically.

## Integration with Tracking Script

The dashboard uses the same data source as `scripts/track-lab-comments.py`:

```bash
# Generate both text report and visual dashboard
export GITHUB_TOKEN='your_token'

# Text report
python3 scripts/track-lab-comments.py > reports/text-report.md

# Visual dashboard
python3 reporting/generate-dashboard.py --output reports/dashboard.html
```

## Customization

### Update Refresh Interval

Edit `generate-dashboard.py` line 269:

```python
# Change from 60 seconds to 30 seconds
{'<meta http-equiv="refresh" content="30">' if auto_refresh else ''}
```

### Color Scheme

Edit the CSS section in `generate-dashboard.py`:

```python
# Gradient background (lines ~210-215)
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

# Status colors (lines ~450-470)
.status-complete { background: #c6f6d5; color: #22543d; }  # Green
.status-partial { background: #feebc8; color: #7c2d12; }   # Orange
.status-none { background: #fed7d7; color: #742a2a; }      # Red
```

## Troubleshooting

### "Error: GITHUB_TOKEN environment variable not set"

**Solution:**
```bash
export GITHUB_TOKEN='your_token_here'
```

### Dashboard shows "No submissions yet"

**Causes:**
- No participants have commented on issues yet
- Token doesn't have access to repository
- Issues don't have `lab-tracking` label

**Verify:**
```bash
# Check if issues exist
gh issue list --repo brainupgrade-in/aiagentic-comp --label lab-tracking --limit 5

# Check if comments exist
gh issue view 1 --repo brainupgrade-in/aiagentic-comp --comments
```

### Dashboard doesn't update

**Solution:**
- Regenerate the dashboard (it's static HTML, not live-connected)
- Use `--auto-refresh` for automatic updates
- Or manually refresh the browser page after regenerating

### Browser doesn't open file

**Manual open:**
1. Open your browser
2. Press Ctrl+O (or Cmd+O on Mac)
3. Navigate to `reporting/dashboard.html`
4. Open the file

## Output Files

Generated files are standalone HTML (no external dependencies):
- **dashboard.html** - Main dashboard file
- Self-contained: All CSS and JavaScript inline
- No network requests (works offline)
- Can be emailed, shared, or archived

## Example Workflow

**Morning check:**
```bash
cd ~/Training/Oracle/reporting
export GITHUB_TOKEN='your_token'
python3 generate-dashboard.py --output morning-check.html
firefox morning-check.html
```

**After each session:**
```bash
python3 generate-dashboard.py --output session-1-complete.html
```

**End of day:**
```bash
python3 generate-dashboard.py --output daily-summary-$(date +%Y%m%d).html
```

**End of course:**
```bash
python3 generate-dashboard.py --output final-completion-report.html
```

## Dashboard URL Structure

If hosting on a web server:

```bash
# Generate to web server directory
python3 generate-dashboard.py --output /var/www/html/agentic-ai-dashboard.html

# Accessible at:
# http://your-server/agentic-ai-dashboard.html
```

For continuous monitoring, set up a cron job to regenerate every 5-10 minutes.

## Performance

- **Generation time:** ~5-10 seconds (depends on API response time)
- **File size:** ~50-100 KB (varies with number of participants)
- **Browser performance:** Smooth with up to 100 participants
- **API calls:** ~120 (1 for issue list + 1 per lab issue for comments)

## Security Notes

- Dashboard is **read-only** (only displays data)
- Token only needs **read** access to issues
- Generated HTML is **static** (no active code execution)
- Safe to share dashboard HTML file with stakeholders

## Dependencies

- Python 3.6+
- `requests` library (installed via `requirements.txt`)
- GitHub token with read access to repository

## Related Tools

- `scripts/track-lab-comments.py` - Text-based completion report
- `scripts/create-lab-issues.py` - Create lab tracking issues
- GitHub Issues UI - Manual issue browsing

---

**Questions?** Refer to main course documentation in `LAB-TRACKING-COMMENT-BASED.md`
