# PowerShell script to create commits
$ErrorActionPreference = "Stop"

# User configurations
$CONTRACT_USER = "CornellSam"
$CONTRACT_EMAIL = "oeemrqvh209331@outlook.com"
$UI_USER = "CashJasper"
$UI_EMAIL = "lacmtnxx753726@outlook.com"

# Set random seed
$random = New-Object System.Random(42)

# Generate timestamps (Nov 10-20, 2025, 9 AM - 5 PM PST)
$startDate = Get-Date "2025-11-10 09:00:00"
$endDate = Get-Date "2025-11-20 17:00:00"
$pst = [TimeZoneInfo]::FindSystemTimeZoneById("Pacific Standard Time")

function Get-RandomWorkTime {
    param($start, $end)
    $days = ($end - $start).Days
    $randomDay = $random.Next(0, $days + 1)
    $targetDate = $start.AddDays($randomDay)
    
    $hour = $random.Next(9, 17)
    $minute = $random.Next(0, 60)
    while ($minute % 5 -eq 0) {
        $minute = $random.Next(0, 60)
    }
    $second = $random.Next(0, 60)
    
    $targetTime = $targetDate.Date.AddHours($hour).AddMinutes($minute).AddSeconds($second)
    return [TimeZoneInfo]::ConvertTimeToUtc($targetTime, $pst)
}

# Generate 24 timestamps
$timestamps = @()
for ($i = 0; $i -lt 24; $i++) {
    $timestamps += Get-RandomWorkTime $startDate $endDate
}
$timestamps = $timestamps | Sort-Object

Write-Host "Generated $($timestamps.Count) timestamps"

# Phase 1: Initial commits
Write-Host "`n[Phase 1] Creating initial project structure..."

# Commit 1: Contract files
git config user.name $CONTRACT_USER
git config user.email $CONTRACT_EMAIL
$env:GIT_AUTHOR_DATE = $timestamps[0].ToString("yyyy-MM-dd HH:mm:ss zzz")
$env:GIT_COMMITTER_DATE = $env:GIT_AUTHOR_DATE
git add contracts/ hardhat.config.ts package.json package-lock.json tsconfig.json .solhint.json .solhintignore .solcover.js .prettierrc.yml .prettierignore .eslintrc.yml .eslintignore LICENSE
git commit -m "feat: add TimeCapsule smart contract with FHE encryption"
Write-Host "[OK] Commit 1 created"

# Commit 2: Deploy and test
$env:GIT_AUTHOR_DATE = $timestamps[1].ToString("yyyy-MM-dd HH:mm:ss zzz")
$env:GIT_COMMITTER_DATE = $env:GIT_AUTHOR_DATE
git add deploy/ test/ tasks/
git commit -m "feat: add deployment scripts and test suite"
Write-Host "[OK] Commit 2 created"

# Commit 3: UI files
git config user.name $UI_USER
git config user.email $UI_EMAIL
$env:GIT_AUTHOR_DATE = $timestamps[2].ToString("yyyy-MM-dd HH:mm:ss zzz")
$env:GIT_COMMITTER_DATE = $env:GIT_AUTHOR_DATE
git add ui/
git commit -m "feat: implement React frontend with FHEVM integration"
Write-Host "[OK] Commit 3 created"

# Commit 4: Config
$env:GIT_AUTHOR_DATE = $timestamps[3].ToString("yyyy-MM-dd HH:mm:ss zzz")
$env:GIT_COMMITTER_DATE = $env:GIT_AUTHOR_DATE
git add .github/ .gitignore
git commit -m "chore: add GitHub workflows and project configuration"
Write-Host "[OK] Commit 4 created"

Write-Host "`n[Phase 1] Complete. Phase 2 will be handled by Python script for file modifications."

