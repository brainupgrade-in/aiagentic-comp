#!/bin/bash
# Lab Submission Script for Participants
# Automatically submits lab completion using your GitHub username
#
# Usage: ./submit-lab.sh <session-number> <lab-number> [notes]
#
# Examples:
#   ./submit-lab.sh 1 1
#   ./submit-lab.sh 1 2 "Great lab on AI agents!"
#   ./submit-lab.sh 2 5 "Had trouble with the API key"

set -e

REPO="brainupgrade-in/aiagentic-comp"

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}   Lab Submission - Agentic AI Course${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Check arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Error: Missing arguments${NC}"
    echo ""
    echo "Usage: $0 <session-number> <lab-number> [notes]"
    echo ""
    echo "Examples:"
    echo "  $0 1 1"
    echo "  $0 1 2 \"Great lab!\""
    echo "  $0 2 5 \"Had some questions about the API\""
    echo ""
    exit 1
fi

SESSION=$1
LAB=$2
NOTES="${3:-}"

# Validate session number
if ! [[ "$SESSION" =~ ^[0-9]+$ ]] || [ "$SESSION" -lt 1 ] || [ "$SESSION" -gt 15 ]; then
    echo -e "${RED}Error: Session must be between 1 and 15${NC}"
    exit 1
fi

# Validate lab number
if ! [[ "$LAB" =~ ^[0-9]+$ ]] || [ "$LAB" -lt 1 ] || [ "$LAB" -gt 9 ]; then
    echo -e "${RED}Error: Lab must be between 1 and 9${NC}"
    exit 1
fi

# Calculate issue number
# Session 1: Labs 1-6 = Issues 1-6
# Session 2: Labs 1-8 = Issues 7-14
# Session 3: Labs 1-7 = Issues 15-21
# etc.

ISSUE_MAP=(
    0    # placeholder
    1    # Session 1 starts at issue 1
    7    # Session 2 starts at issue 7
    15   # Session 3 starts at issue 15
    22   # Session 4 starts at issue 22
    30   # Session 5 starts at issue 30
    38   # Session 6 starts at issue 38
    46   # Session 7 starts at issue 46
    54   # Session 8 starts at issue 54
    62   # Session 9 starts at issue 62
    70   # Session 10 starts at issue 70
    78   # Session 11 starts at issue 78
    86   # Session 12 starts at issue 86
    95   # Session 13 starts at issue 95
    103  # Session 14 starts at issue 103
    111  # Session 15 starts at issue 111
)

SESSION_START=${ISSUE_MAP[$SESSION]}
ISSUE_NUMBER=$((SESSION_START + LAB - 1))

echo -e "${BLUE}Session:${NC} $SESSION"
echo -e "${BLUE}Lab:${NC} $LAB"
echo -e "${BLUE}Issue Number:${NC} #$ISSUE_NUMBER"
echo ""

# Detect GitHub username and email
echo -e "${YELLOW}Detecting your information...${NC}"

USERNAME=""
EMAIL=""

# 1st preference: Repository-level git config
USERNAME=$(git config --local user.name 2>/dev/null || echo "")
EMAIL=$(git config --local user.email 2>/dev/null || echo "")

# 2nd preference: Global git config (username or email not found in repo)
if [ -z "$USERNAME" ]; then
    USERNAME=$(git config --global user.name 2>/dev/null || echo "")
fi
if [ -z "$EMAIL" ]; then
    EMAIL=$(git config --global user.email 2>/dev/null || echo "")
fi

# 3rd preference: GitHub CLI (last resort, username only)
if [ -z "$USERNAME" ] && command -v gh &> /dev/null; then
    USERNAME=$(gh api user --jq '.login' 2>/dev/null || echo "")
fi

if [ -z "$USERNAME" ]; then
    echo -e "${RED}Error: Could not detect GitHub username${NC}"
    echo ""
    echo "Please set your username in this repository:"
    echo "  git config user.name \"your-github-username\""
    echo "  git config user.email \"your-email@example.com\""
    echo ""
    echo "Or authenticate with GitHub CLI:"
    echo "  gh auth login"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Username: $USERNAME${NC}"
if [ -n "$EMAIL" ]; then
    echo -e "${GREEN}✓ Email: $EMAIL${NC}"
fi
echo ""

# Check if gh CLI is authenticated
if ! command -v gh &> /dev/null; then
    echo -e "${RED}Error: GitHub CLI (gh) not found${NC}"
    echo ""
    echo "Please install GitHub CLI:"
    echo "  Ubuntu/Debian: sudo apt install gh"
    echo "  macOS: brew install gh"
    echo ""
    echo "Or download from: https://cli.github.com/"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}GitHub CLI not authenticated${NC}"
    echo ""
    echo "Please authenticate with the shared token:"
    echo "  gh auth login"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ GitHub CLI authenticated${NC}"
echo ""

# Build comment body
COMMENT_BODY="✅ Completed

**Participant:** $USERNAME"

if [ -n "$EMAIL" ]; then
    COMMENT_BODY="$COMMENT_BODY ($EMAIL)"
fi

COMMENT_BODY="$COMMENT_BODY
**Validation:** All checks passed"

if [ -n "$NOTES" ]; then
    COMMENT_BODY="$COMMENT_BODY
**Notes:** $NOTES"
fi

# Show preview
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}Comment Preview:${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo "$COMMENT_BODY"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# Confirm submission
read -p "Submit this lab? (y/N): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Submission cancelled${NC}"
    exit 0
fi

# Submit comment
echo ""
echo -e "${YELLOW}Submitting to Issue #$ISSUE_NUMBER...${NC}"

COMMENT_URL=$(gh issue comment "$ISSUE_NUMBER" \
    --repo "$REPO" \
    --body "$COMMENT_BODY" 2>&1 | grep -oP 'https://[^ ]+' || echo "")

if [ -n "$COMMENT_URL" ]; then
    echo ""
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${GREEN}✓ Submission Successful!${NC}"
    echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo -e "${BLUE}Session:${NC} $SESSION | ${BLUE}Lab:${NC} $LAB | ${BLUE}Issue:${NC} #$ISSUE_NUMBER"
    echo -e "${BLUE}Comment:${NC} $COMMENT_URL"
    echo ""
    echo -e "${GREEN}Your submission has been recorded!${NC}"
    echo ""
else
    echo ""
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${RED}✗ Submission Failed${NC}"
    echo -e "${RED}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
    echo "Please check:"
    echo "  1. GitHub CLI is authenticated (gh auth status)"
    echo "  2. You have access to the repository"
    echo "  3. Issue #$ISSUE_NUMBER exists"
    echo ""
    exit 1
fi

# Check your progress
echo -e "${BLUE}💡 Tip:${NC} Check your progress:"
echo "  gh issue list --repo $REPO --search \"commenter:$USERNAME\" --label lab-tracking"
echo ""
