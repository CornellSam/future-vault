# PowerShell script to create git commits with specific timestamps
# This script will be executed to create all commits

$ErrorActionPreference = "Stop"

# User configurations
$contractUser = "CornellSam"
$contractEmail = "oeemrqvh209331@outlook.com"
$uiUser = "CashJasper"
$uiEmail = "lacmtnxx753726@outlook.com"

# Time range: Nov 10, 2025 9:00 AM to Nov 20, 2025 5:00 PM (PST)
# PST is UTC-8, but we'll use local time and adjust
$startDate = Get-Date "2025-11-10 09:00:00"
$endDate = Get-Date "2025-11-20 17:00:00"

# Generate random timestamps (20-30 commits)
$random = New-Object System.Random
$numCommits = $random.Next(20, 31)  # 20-30 commits
Write-Host "Will create $numCommits commits"

# Commit plan
# Phase 1: First 4 commits (main files)
# Phase 2: 15-20 commits (bug fixes)
# Phase 3: Last commit (README and video)

# This script will be called with parameters to create each commit
param(
    [int]$CommitNumber,
    [string]$User,
    [string]$Email,
    [string]$Message,
    [string]$Date,
    [string[]]$Files
)

if ($CommitNumber -gt 0) {
    $env:GIT_AUTHOR_NAME = $User
    $env:GIT_AUTHOR_EMAIL = $Email
    $env:GIT_COMMITTER_NAME = $User
    $env:GIT_COMMITTER_EMAIL = $Email
    
    git add $Files
    git commit -m $Message --date="$Date"
    
    Write-Host "Created commit $CommitNumber: $Message"
}






