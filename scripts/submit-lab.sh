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

# Validate lab number (basic range)
if ! [[ "$LAB" =~ ^[0-9]+$ ]] || [ "$LAB" -lt 1 ] || [ "$LAB" -gt 9 ]; then
    echo -e "${RED}Error: Lab must be between 1 and 9${NC}"
    exit 1
fi

# Per-session lab counts
SESSION_LAB_COUNT=(0 6 9 7 8 8 8 8 8 8 8 8 9 8 8 8)
MAX_LAB=${SESSION_LAB_COUNT[$SESSION]}
if [ "$LAB" -gt "$MAX_LAB" ]; then
    echo -e "${RED}Error: Session $SESSION only has $MAX_LAB labs (lab must be 1-$MAX_LAB)${NC}"
    exit 1
fi

# Calculate issue number
# Session 1:  Labs 1-6  = Issues 1-6    (6 labs)
# Session 2:  Labs 1-9  = Issues 7-15   (9 labs)
# Session 3:  Labs 1-7  = Issues 16-22  (7 labs)
# Session 4:  Labs 1-8  = Issues 23-30  (8 labs)
# Session 5:  Labs 1-8  = Issues 31-38  (8 labs)
# Session 6:  Labs 1-8  = Issues 39-46  (8 labs)
# Session 7:  Labs 1-8  = Issues 47-54  (8 labs)
# Session 8:  Labs 1-8  = Issues 55-62  (8 labs)
# Session 9:  Labs 1-8  = Issues 63-70  (8 labs)
# Session 10: Labs 1-8  = Issues 71-78  (8 labs)
# Session 11: Labs 1-8  = Issues 79-86  (8 labs)
# Session 12: Labs 1-9  = Issues 87-95  (9 labs)
# Session 13: Labs 1-8  = Issues 96-103 (8 labs)
# Session 14: Labs 1-8  = Issues 104-111 (8 labs)
# Session 15: Labs 1-8  = Issues 112-119 (8 labs)

ISSUE_MAP=(
    0    # placeholder
    1    # Session 1 starts at issue 1
    7    # Session 2 starts at issue 7
    16   # Session 3 starts at issue 16
    23   # Session 4 starts at issue 23
    31   # Session 5 starts at issue 31
    39   # Session 6 starts at issue 39
    47   # Session 7 starts at issue 47
    55   # Session 8 starts at issue 55
    63   # Session 9 starts at issue 63
    71   # Session 10 starts at issue 71
    79   # Session 11 starts at issue 79
    87   # Session 12 starts at issue 87
    96   # Session 13 starts at issue 96
    104  # Session 14 starts at issue 104
    112  # Session 15 starts at issue 112
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

if [ -z "$USERNAME" ]; then
    echo -e "${RED}Error: Could not detect GitHub username${NC}"
    echo ""
    echo "Please set your username in this repository:"
    echo "  git config user.name \"your-github-username\""
    echo "  git config user.email \"your-email@example.com\""
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ Username: $USERNAME${NC}"
if [ -n "$EMAIL" ]; then
    echo -e "${GREEN}✓ Email: $EMAIL${NC}"
fi
echo ""

# Load GITHUB_TOKEN — try 3 sources in order:
# 1. Already set in environment
# 2. .env file
# 3. Embedded in git remote URL (e.g. cloned via https://<token>@github.com/...)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ENV_FILE="$SCRIPT_DIR/../.env"

if [ -z "$GITHUB_TOKEN" ] && [ -f "$ENV_FILE" ]; then
    GITHUB_TOKEN=$(grep -E '^GITHUB_TOKEN=' "$ENV_FILE" | cut -d'=' -f2- | tr -d '"' | tr -d "'")
fi

if [ -z "$GITHUB_TOKEN" ]; then
    REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")
    if [[ "$REMOTE_URL" =~ https://([^@]+)@github\.com ]]; then
        GITHUB_TOKEN="${BASH_REMATCH[1]}"
    fi
fi

if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${RED}Error: GITHUB_TOKEN not set${NC}"
    echo ""
    echo "Either export it:"
    echo "  export GITHUB_TOKEN=ghp_xxxx"
    echo ""
    echo "Or add it to .env:"
    echo "  GITHUB_TOKEN=ghp_xxxx"
    echo ""
    exit 1
fi

echo -e "${GREEN}✓ GitHub token found${NC}"
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

RESPONSE_FILE=$(mktemp)
HTTP_CODE=$(curl -s -o "$RESPONSE_FILE" -w "%{http_code}" \
    -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github+json" \
    -H "Content-Type: application/json" \
    "https://api.github.com/repos/$REPO/issues/$ISSUE_NUMBER/comments" \
    -d "{\"body\": $(echo "$COMMENT_BODY" | python3 -c 'import json,sys; print(json.dumps(sys.stdin.read()))')}")
RESPONSE_BODY=$(cat "$RESPONSE_FILE")
rm -f "$RESPONSE_FILE"

COMMENT_URL=""
if [ "$HTTP_CODE" = "201" ]; then
    COMMENT_URL=$(echo "$RESPONSE_BODY" | python3 -c 'import json,sys; print(json.load(sys.stdin).get("html_url",""))' 2>/dev/null || echo "")
fi

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
    echo "HTTP status: $HTTP_CODE"
    echo "API response: $(echo "$RESPONSE_BODY" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("message", d))' 2>/dev/null || echo "$RESPONSE_BODY")"
    echo ""
    echo "Please check:"
    echo "  1. GITHUB_TOKEN is a fine-grained PAT with 'Issues' read/write permission"
    echo "  2. You have access to the repository"
    echo "  3. Issue #$ISSUE_NUMBER exists"
    echo ""
    exit 1
fi

# Check your progress
echo -e "${BLUE}💡 Tip:${NC} Check your progress:"
echo "  https://github.com/$REPO/issues?q=label%3Alab-tracking"
echo ""
