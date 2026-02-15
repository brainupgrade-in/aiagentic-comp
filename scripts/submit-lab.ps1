# Lab Submission Script for Participants (PowerShell)
# Automatically submits lab completion using your GitHub username
#
# Usage: .\submit-lab.ps1 <session-number> <lab-number> [notes]
#
# Examples:
#   .\submit-lab.ps1 1 1
#   .\submit-lab.ps1 1 2 "Great lab on AI agents!"
#   .\submit-lab.ps1 2 5 "Had trouble with the API key"

param(
    [Parameter(Mandatory=$true)]
    [int]$Session,

    [Parameter(Mandatory=$true)]
    [int]$Lab,

    [Parameter(Mandatory=$false)]
    [string]$Notes = ""
)

$ErrorActionPreference = "Stop"
$Repo = "brainupgrade-in/aiagentic-comp"

# Banner
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "   Lab Submission - Agentic AI Course" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host ""

# Validate session number
if ($Session -lt 1 -or $Session -gt 15) {
    Write-Host "Error: Session must be between 1 and 15" -ForegroundColor Red
    exit 1
}

# Validate lab number
if ($Lab -lt 1 -or $Lab -gt 9) {
    Write-Host "Error: Lab must be between 1 and 9" -ForegroundColor Red
    exit 1
}

# Calculate issue number
$IssueMap = @(
    0,    # placeholder
    1,    # Session 1 starts at issue 1
    7,    # Session 2 starts at issue 7
    15,   # Session 3 starts at issue 15
    22,   # Session 4 starts at issue 22
    30,   # Session 5 starts at issue 30
    38,   # Session 6 starts at issue 38
    46,   # Session 7 starts at issue 46
    54,   # Session 8 starts at issue 54
    62,   # Session 9 starts at issue 62
    70,   # Session 10 starts at issue 70
    78,   # Session 11 starts at issue 78
    86,   # Session 12 starts at issue 86
    95,   # Session 13 starts at issue 95
    103,  # Session 14 starts at issue 103
    111   # Session 15 starts at issue 111
)

$SessionStart = $IssueMap[$Session]
$IssueNumber = $SessionStart + $Lab - 1

Write-Host "Session: " -NoNewline -ForegroundColor Blue
Write-Host $Session
Write-Host "Lab: " -NoNewline -ForegroundColor Blue
Write-Host $Lab
Write-Host "Issue Number: " -NoNewline -ForegroundColor Blue
Write-Host "#$IssueNumber"
Write-Host ""

# Detect GitHub username and email
Write-Host "Detecting your information..." -ForegroundColor Yellow

$Username = ""
$Email = ""

# 1st preference: Repository-level git config
try {
    $Username = (git config --local user.name 2>$null)
    $Email = (git config --local user.email 2>$null)
} catch {
    # Repository config not set
}

# 2nd preference: Global git config (if not found in repo)
if ([string]::IsNullOrWhiteSpace($Username)) {
    try {
        $Username = (git config --global user.name 2>$null)
        $Email = (git config --global user.email 2>$null)
    } catch {
        # Global config not set
    }
}

# 3rd preference: GitHub CLI (last resort, username only)
if ([string]::IsNullOrWhiteSpace($Username)) {
    try {
        $ghPath = Get-Command gh -ErrorAction SilentlyContinue
        if ($ghPath) {
            $Username = (gh api user --jq '.login' 2>$null)
        }
    } catch {
        # gh CLI not available or not authenticated
    }
}

if ([string]::IsNullOrWhiteSpace($Username)) {
    Write-Host "Error: Could not detect GitHub username" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please set your username in this repository:"
    Write-Host "  git config user.name `"your-github-username`""
    Write-Host "  git config user.email `"your-email@example.com`""
    Write-Host ""
    Write-Host "Or authenticate with GitHub CLI:"
    Write-Host "  gh auth login"
    Write-Host ""
    exit 1
}

Write-Host "✓ Username: $Username" -ForegroundColor Green
if (![string]::IsNullOrWhiteSpace($Email)) {
    Write-Host "✓ Email: $Email" -ForegroundColor Green
}
Write-Host ""

# Check if gh CLI is available
try {
    $ghPath = Get-Command gh -ErrorAction Stop
} catch {
    Write-Host "Error: GitHub CLI (gh) not found" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install GitHub CLI:"
    Write-Host "  Download from: https://cli.github.com/"
    Write-Host "  Or use: winget install GitHub.cli"
    Write-Host ""
    exit 1
}

# Check if authenticated
try {
    gh auth status 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Not authenticated"
    }
} catch {
    Write-Host "GitHub CLI not authenticated" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please authenticate with the shared token:"
    Write-Host "  gh auth login"
    Write-Host ""
    exit 1
}

Write-Host "✓ GitHub CLI authenticated" -ForegroundColor Green
Write-Host ""

# Build comment body
$ParticipantInfo = $Username
if (![string]::IsNullOrWhiteSpace($Email)) {
    $ParticipantInfo += " ($Email)"
}

$CommentBody = @"
✅ Completed

**Participant:** $ParticipantInfo
**Validation:** All checks passed
"@

if (![string]::IsNullOrWhiteSpace($Notes)) {
    $CommentBody += "`n**Notes:** $Notes"
}

# Show preview
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host "Comment Preview:" -ForegroundColor Blue
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host $CommentBody
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Blue
Write-Host ""

# Confirm submission
$Confirmation = Read-Host "Submit this lab? (y/N)"

if ($Confirmation -ne 'y' -and $Confirmation -ne 'Y') {
    Write-Host "Submission cancelled" -ForegroundColor Yellow
    exit 0
}

# Submit comment
Write-Host ""
Write-Host "Submitting to Issue #$IssueNumber..." -ForegroundColor Yellow

try {
    # Create temporary file for comment body (to handle multiline properly)
    $TempFile = [System.IO.Path]::GetTempFileName()
    $CommentBody | Out-File -FilePath $TempFile -Encoding UTF8

    $Output = gh issue comment $IssueNumber --repo $Repo --body-file $TempFile 2>&1

    Remove-Item $TempFile -Force

    # Extract URL from output
    $CommentUrl = ""
    if ($Output -match 'https://[^\s]+') {
        $CommentUrl = $matches[0]
    }

    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host "✓ Submission Successful!" -ForegroundColor Green
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Green
    Write-Host ""
    Write-Host "Session: " -NoNewline -ForegroundColor Blue
    Write-Host "$Session | " -NoNewline
    Write-Host "Lab: " -NoNewline -ForegroundColor Blue
    Write-Host "$Lab | " -NoNewline
    Write-Host "Issue: " -NoNewline -ForegroundColor Blue
    Write-Host "#$IssueNumber"

    if (![string]::IsNullOrWhiteSpace($CommentUrl)) {
        Write-Host "Comment: " -NoNewline -ForegroundColor Blue
        Write-Host $CommentUrl
    }

    Write-Host ""
    Write-Host "Your submission has been recorded!" -ForegroundColor Green
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host "✗ Submission Failed" -ForegroundColor Red
    Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please check:"
    Write-Host "  1. GitHub CLI is authenticated (gh auth status)"
    Write-Host "  2. You have access to the repository"
    Write-Host "  3. Issue #$IssueNumber exists"
    Write-Host ""
    Write-Host "Error: $_" -ForegroundColor Red
    Write-Host ""
    exit 1
}

# Check your progress
Write-Host "💡 Tip: Check your progress:" -ForegroundColor Blue
Write-Host "  gh issue list --repo $Repo --search `"commenter:$Username`" --label lab-tracking"
Write-Host ""
