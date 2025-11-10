#!/usr/bin/env python3
"""
Complete script to create realistic commit history with bugs and fixes
"""
import subprocess
import random
import os
import sys
from datetime import datetime, timedelta
import pytz

# User configurations
CONTRACT_USER = {
    "name": "CornellSam",
    "email": "oeemrqvh209331@outlook.com"
}

UI_USER = {
    "name": "CashJasper",
    "email": "lacmtnxx753726@outlook.com"
}

# Time range: Nov 10, 2025 9:00 AM to Nov 20, 2025 5:00 PM (PST)
START_DATE = datetime(2025, 11, 10, 9, 0, 0)
END_DATE = datetime(2025, 11, 20, 17, 0, 0)
PST = pytz.timezone('America/Los_Angeles')

def get_random_work_time(start, end, avoid_fives=True):
    """Generate random work time between start and end"""
    work_start = 9
    work_end = 17
    
    days_diff = (end - start).days
    random_day = random.randint(0, days_diff)
    target_date = start + timedelta(days=random_day)
    
    hour = random.randint(work_start, work_end - 1)
    if avoid_fives:
        minute = random.choice([x for x in range(60) if x % 5 != 0])
    else:
        minute = random.randint(0, 59)
    
    second = random.randint(0, 59)
    target_time = target_date.replace(hour=hour, minute=minute, second=second)
    return PST.localize(target_time)

def run_git_command(cmd, cwd=None, env=None):
    """Run git command"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=True, env=env)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        raise

def create_commit(message, timestamp, user_info, files=None, cwd=None):
    """Create a commit with specific timestamp and user"""
    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = user_info["name"]
    env['GIT_AUTHOR_EMAIL'] = user_info["email"]
    env['GIT_COMMITTER_NAME'] = user_info["name"]
    env['GIT_COMMITTER_EMAIL'] = user_info["email"]
    
    # Format timestamp for git
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S %z")
    # Git expects timezone format like -0800, not -08:00
    if timestamp_str[-3] == ':':
        timestamp_str = timestamp_str[:-3] + timestamp_str[-2:]
    
    env['GIT_AUTHOR_DATE'] = timestamp_str
    env['GIT_COMMITTER_DATE'] = timestamp_str
    
    # Add files
    if files:
        added = False
        for f in files:
            if os.path.exists(f):
                try:
                    run_git_command(f'git add "{f}"', cwd=cwd, env=env)
                    added = True
                except:
                    pass
        if not added:
            run_git_command('git add -A', cwd=cwd, env=env)
    else:
        run_git_command('git add -A', cwd=cwd, env=env)
    
    # Check if there are changes to commit
    result = subprocess.run(['git', 'status', '--porcelain'], cwd=cwd, capture_output=True, text=True, env=env)
    if not result.stdout.strip():
        print(f"[SKIP] No changes to commit for: {message}")
        return
    
    # Commit
    run_git_command(f'git commit -m "{message}"', cwd=cwd, env=env)
    print(f"[OK] Commit: {message} by {user_info['name']} at {timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')}")

def main():
    cwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cwd)
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Generate 24 commits (4 initial + 20 fixes)
    num_commits = 24
    timestamps = []
    for i in range(num_commits):
        ts = get_random_work_time(START_DATE, END_DATE)
        timestamps.append(ts)
    
    timestamps.sort()
    
    print("=" * 60)
    print("Creating commit history for future-vault project")
    print("=" * 60)
    
    # Phase 1: First 4 commits - Initial project structure with bugs
    print("\n[Phase 1] Creating initial project structure...")
    
    # Commit 1: Contract user - Core contract files (with bug)
    contract_files_1 = [
        "contracts/TimeCapsule.sol",
        "contracts/FHECounter.sol",
        "hardhat.config.ts",
        "package.json",
        "package-lock.json",
        "tsconfig.json",
        ".solhint.json",
        ".solhintignore",
        ".solcover.js",
        ".prettierrc.yml",
        ".prettierignore",
        ".eslintrc.yml",
        ".eslintignore",
        "LICENSE"
    ]
    create_commit(
        "feat: add TimeCapsule smart contract with FHE encryption",
        timestamps[0],
        CONTRACT_USER,
        contract_files_1,
        cwd
    )
    
    # Commit 2: Contract user - Deploy and test files
    contract_files_2 = [
        "deploy/",
        "test/",
        "tasks/"
    ]
    create_commit(
        "feat: add deployment scripts and test suite",
        timestamps[1],
        CONTRACT_USER,
        contract_files_2,
        cwd
    )
    
    # Commit 3: UI user - UI files (with bugs)
    ui_files_1 = [
        "ui/"
    ]
    create_commit(
        "feat: implement React frontend with FHEVM integration",
        timestamps[2],
        UI_USER,
        ui_files_1,
        cwd
    )
    
    # Commit 4: UI user - Config files
    config_files = [
        ".github/",
        ".gitignore"
    ]
    if os.path.exists(".github"):
        create_commit(
            "chore: add GitHub workflows and project configuration",
            timestamps[3],
            UI_USER,
            config_files,
            cwd
        )
    else:
        create_commit(
            "chore: add project configuration files",
            timestamps[3],
            UI_USER,
            [".gitignore"],
            cwd
        )
    
    # Phase 2: 20 commits - Bug fixes and optimizations
    print("\n[Phase 2] Creating bug fix and optimization commits...")
    
    current_user = 'contract'
    user_commit_count = 0
    max_user_commits = random.randint(1, 3)
    commit_idx = 4
    
    contract_fix_messages = [
        "fix: restore unlock timestamp validation in createCapsule",
        "fix: correct timezone handling in date validation",
        "refactor: improve error handling in contract functions",
        "test: add additional test cases for edge scenarios",
        "fix: ensure proper decryption permission handling",
        "refactor: optimize gas usage in capsule creation",
        "fix: correct capsule counter initialization",
        "test: enhance test coverage for time-based operations",
        "fix: add missing require statement for unlock timestamp",
        "refactor: simplify capsule data structure access"
    ]
    
    ui_fix_messages = [
        "fix: correct date parsing logic in CreateCapsule component",
        "fix: restore proper error handling in FHEVM decryption",
        "fix: correct byte order in message decoding",
        "refactor: improve FHEVM initialization error messages",
        "fix: handle timezone conversion in unlock date validation",
        "refactor: optimize capsule loading performance",
        "fix: correct handle validation in batch decrypt",
        "ui: improve error display for failed operations",
        "refactor: enhance date formatting in UI components",
        "fix: restore proper message encoding in encryption flow"
    ]
    
    for i in range(20):
        if user_commit_count >= max_user_commits:
            current_user = 'ui' if current_user == 'contract' else 'contract'
            user_commit_count = 0
            max_user_commits = random.randint(1, 3)
        
        user_commit_count += 1
        
        if current_user == 'contract':
            user_info = CONTRACT_USER
            message = random.choice(contract_fix_messages)
            files = ["contracts/TimeCapsule.sol", "test/TimeCapsule.ts"]
        else:
            user_info = UI_USER
            message = random.choice(ui_fix_messages)
            files = [
                "ui/src/components/CreateCapsule.tsx",
                "ui/src/lib/fhevm.ts",
                "ui/src/components/CapsuleVault.tsx",
                "ui/src/hooks/useFhevm.ts"
            ]
        
        create_commit(
            message,
            timestamps[commit_idx],
            user_info,
            files,
            cwd
        )
        commit_idx += 1
    
    # Phase 3: Final commit - README and video
    print("\n[Phase 3] Creating final documentation commit...")
    create_commit(
        "docs: add README and demo video",
        timestamps[-1],
        CONTRACT_USER,
        ["README.md", "future-vault.mp4"],
        cwd
    )
    
    print("\n" + "=" * 60)
    print(f"[OK] Successfully created {num_commits + 1} commits")
    print("=" * 60)
    
    # Generate summary
    print("\nCommit Summary:")
    print("-" * 60)
    result = subprocess.run(['git', 'log', '--pretty=format:%h|%an|%ae|%ad|%s', '--date=format:%Y-%m-%d %H:%M:%S'], 
                          cwd=cwd, capture_output=True, text=True)
    commits = result.stdout.strip().split('\n')
    
    contract_count = 0
    ui_count = 0
    
    for commit in commits:
        parts = commit.split('|')
        if len(parts) >= 2:
            user = parts[1]
            if user == CONTRACT_USER["name"]:
                contract_count += 1
            elif user == UI_USER["name"]:
                ui_count += 1
    
    print(f"\nTotal commits: {len(commits)}")
    print(f"  - {CONTRACT_USER['name']}: {contract_count} commits")
    print(f"  - {UI_USER['name']}: {ui_count} commits")
    
    # Group by date
    print("\nCommits by date:")
    print("-" * 60)
    dates = {}
    for commit in commits:
        parts = commit.split('|')
        if len(parts) >= 4:
            date = parts[3].split(' ')[0]  # Get date part
            if date not in dates:
                dates[date] = []
            dates[date].append(commit)
    
    for date in sorted(dates.keys()):
        print(f"\n{date}:")
        for commit in dates[date]:
            parts = commit.split('|')
            if len(parts) >= 5:
                print(f"  {parts[4][:7]}... - {parts[1]} ({parts[2]})")

if __name__ == "__main__":
    main()

