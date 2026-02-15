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

# Generate dashboard
echo "Generating dashboard..."
python3 generate-dashboard.py --output dashboard.html $AUTO_REFRESH

# Archive previous dashboard
if [ -f dashboard.html ] && [ -f dashboard-previous.html ]; then
    mv dashboard-previous.html "archive/dashboard-$(date +%Y%m%d-%H%M%S).html" 2>/dev/null || true
fi

# Create archive directory if needed
mkdir -p archive

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
