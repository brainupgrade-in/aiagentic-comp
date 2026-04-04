#!/bin/bash
# Quick dashboard update script
# Usage: ./update-dashboard.sh [--auto-refresh] [--open]

set -e

# Check for GitHub token
if [ -z "$GITHUB_TOKEN" ]; then
    # Try to load from file
    if [ -f ~/.rajesh/.github_bu ]; then
        export GITHUB_TOKEN=$(cat ~/.rajesh/.github_bu | tr -d ' \n')
        echo "✓ Loaded token from ~/.rajesh/.github_bu"
    else
        echo "Error: GITHUB_TOKEN not set"
        echo "Please run: export GITHUB_TOKEN='your_token'"
        exit 1
    fi
fi

# Parse arguments
AUTO_REFRESH=""
OPEN_BROWSER=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --auto-refresh)
            AUTO_REFRESH="--auto-refresh"
            shift
            ;;
        --open)
            OPEN_BROWSER="yes"
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--auto-refresh] [--open]"
            exit 1
            ;;
    esac
done

# Activate virtual environment if present
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$SCRIPT_DIR/../.venv/bin/python3"
if [ -f "$VENV_PYTHON" ]; then
    PYTHON="$VENV_PYTHON"
else
    PYTHON="python3"
fi

# Create archive directory if needed
mkdir -p archive

# Archive previous dashboard before regenerating
if [ -f dashboard.html ]; then
    cp dashboard.html "archive/dashboard-$(date +%Y%m%d-%H%M%S).html" 2>/dev/null || true
fi

# Generate dashboard
echo "Generating dashboard..."
"$PYTHON" "$SCRIPT_DIR/generate-dashboard.py" --output dashboard.html $AUTO_REFRESH

echo ""
echo "✓ Dashboard updated: dashboard.html"
echo "✓ Open in browser: file://$(pwd)/dashboard.html"

# Open in browser if requested
if [ "$OPEN_BROWSER" = "yes" ]; then
    if command -v firefox &> /dev/null; then
        firefox dashboard.html &
        echo "✓ Opened in Firefox"
    elif command -v google-chrome &> /dev/null; then
        google-chrome dashboard.html &
        echo "✓ Opened in Chrome"
    elif command -v xdg-open &> /dev/null; then
        xdg-open dashboard.html &
        echo "✓ Opened in default browser"
    else
        echo "⚠ Could not auto-open browser"
    fi
fi

echo ""
echo "💡 Tips:"
echo "  - Refresh browser to see latest data"
echo "  - Use --auto-refresh for automatic updates"
echo "  - Archived versions in archive/ directory"
