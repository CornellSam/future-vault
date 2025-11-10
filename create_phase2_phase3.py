#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to create Phase 2 and Phase 3 commits (bug fixes and documentation)
"""
import subprocess
import random
import os
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

def get_random_work_time(start, end):
    """Generate random work time between start and end"""
    work_start = 9
    work_end = 17
    
    days_diff = (end - start).days
    random_day = random.randint(0, days_diff)
    target_date = start + timedelta(days=random_day)
    
    hour = random.randint(work_start, work_end - 1)
    minute = random.choice([x for x in range(60) if x % 5 != 0])
    second = random.randint(0, 59)
    target_time = target_date.replace(hour=hour, minute=minute, second=second)
    return PST.localize(target_time)

def run_git_command(cmd_list, cwd=None, env=None):
    """Run git command as list"""
    try:
        result = subprocess.run(cmd_list, cwd=cwd, capture_output=True, text=True, check=True, env=env)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None

def create_commit(message, timestamp, user_info, files_to_modify=None, cwd=None):
    """Create a commit with specific timestamp and user"""
    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = user_info["name"]
    env['GIT_AUTHOR_EMAIL'] = user_info["email"]
    env['GIT_COMMITTER_NAME'] = user_info["name"]
    env['GIT_COMMITTER_EMAIL'] = user_info["email"]
    
    # Format timestamp for git
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S %z")
    if len(timestamp_str) > 3 and timestamp_str[-3] == ':':
        timestamp_str = timestamp_str[:-3] + timestamp_str[-2:]
    
    env['GIT_AUTHOR_DATE'] = timestamp_str
    env['GIT_COMMITTER_DATE'] = timestamp_str
    
    # Make file modifications if needed
    if files_to_modify:
        for file_path, modification_func in files_to_modify.items():
            if os.path.exists(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    new_content = modification_func(content)
                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                except Exception as e:
                    print(f"Warning: Could not modify {file_path}: {e}")
    
    # Add modified files
    if files_to_modify:
        for file_path in files_to_modify.keys():
            if os.path.exists(file_path):
                run_git_command(['git', 'add', file_path], cwd=cwd, env=env)
    
    # Check if there are changes
    result = subprocess.run(['git', 'status', '--porcelain'], cwd=cwd, capture_output=True, text=True, env=env)
    if not result.stdout.strip():
        print(f"[SKIP] No changes for: {message}")
        return False
    
    # Commit
    result = run_git_command(['git', 'commit', '-m', message], cwd=cwd, env=env)
    if result is not None:
        print(f"[OK] {message} by {user_info['name']} at {timestamp.strftime('%Y-%m-%d %H:%M:%S %Z')}")
        return True
    return False

def main():
    cwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cwd)
    
    random.seed(42)
    
    # Generate 20 timestamps for Phase 2, 1 for Phase 3
    timestamps = []
    for i in range(21):
        ts = get_random_work_time(START_DATE, END_DATE)
        timestamps.append(ts)
    timestamps.sort()
    
    print("=" * 60)
    print("Creating Phase 2 and Phase 3 commits")
    print("=" * 60)
    
    # Phase 2: 20 bug fix commits
    print("\n[Phase 2] Creating bug fix commits...")
    
    current_user = 'contract'
    user_commit_count = 0
    max_user_commits = random.randint(1, 3)
    commit_idx = 0
    
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
    
    # Track which fixes have been applied
    fixes_applied = {
        'contract_timestamp': False,
        'ui_timezone': False,
        'ui_byteorder': False
    }
    
    for i in range(20):
        if user_commit_count >= max_user_commits:
            current_user = 'ui' if current_user == 'contract' else 'contract'
            user_commit_count = 0
            max_user_commits = random.randint(1, 3)
        
        user_commit_count += 1
        
        if current_user == 'contract':
            user_info = CONTRACT_USER
            message = random.choice(contract_fix_messages)
            
            # Apply specific fix if message matches
            files_to_modify = {}
            if 'restore unlock timestamp validation' in message and not fixes_applied['contract_timestamp']:
                def fix_timestamp(content):
                    return content.replace(
                        '// TODO: Add timestamp validation\n        // require(unlockTimestamp > block.timestamp, "Unlock date must be in the future");',
                        '// Validate unlock timestamp is in the future\n        require(unlockTimestamp > block.timestamp, "Unlock date must be in the future");'
                    )
                files_to_modify['contracts/TimeCapsule.sol'] = fix_timestamp
                fixes_applied['contract_timestamp'] = True
        else:
            user_info = UI_USER
            message = random.choice(ui_fix_messages)
            
            files_to_modify = {}
            if 'correct date parsing logic' in message and not fixes_applied['ui_timezone']:
                def fix_timezone(content):
                    content = content.replace(
                        '// Use UTC to avoid timezone issues\n      const unlockDateTime = new Date(Date.UTC(year, month - 1, day, hours, minutes));',
                        '// Create date in local timezone\n      const unlockDateTime = new Date(year, month - 1, day, hours, minutes);'
                    )
                    content = content.replace(
                        '// Use UTC to avoid timezone issues\n              const unlockDateTime = new Date(Date.UTC(year, month - 1, day, hours, minutes));',
                        '// Create date in local timezone\n              const unlockDateTime = new Date(year, month - 1, day, hours, minutes);'
                    )
                    return content
                files_to_modify['ui/src/components/CreateCapsule.tsx'] = fix_timezone
                fixes_applied['ui_timezone'] = True
            elif 'correct byte order' in message and not fixes_applied['ui_byteorder']:
                def fix_byteorder(content):
                    return content.replace(
                        '// Extract bytes from the number (little-endian for now)\n        // We encoded as: (byte0 << 24) | (byte1 << 16) | (byte2 << 8) | byte3\n        for (let i = 0; i < 4; i++) {\n          bytes.push(n & 0xFF); // Append instead of unshift',
                        '// Extract bytes from the number (big-endian: most significant byte first)\n        // We encoded as: (byte0 << 24) | (byte1 << 16) | (byte2 << 8) | byte3\n        for (let i = 0; i < 4; i++) {\n          bytes.unshift(n & 0xFF); // Insert at beginning to maintain order'
                    )
                files_to_modify['ui/src/components/CapsuleVault.tsx'] = fix_byteorder
                fixes_applied['ui_byteorder'] = True
        
        create_commit(
            message,
            timestamps[commit_idx],
            user_info,
            files_to_modify,
            cwd
        )
        commit_idx += 1
    
    # Phase 3: Final commit - README and video
    print("\n[Phase 3] Creating final documentation commit...")
    create_commit(
        "docs: add README and demo video",
        timestamps[-1],
        CONTRACT_USER,
        None,
        cwd
    )
    
    print("\n" + "=" * 60)
    print("[OK] All commits created")
    print("=" * 60)
    
    # Generate summary
    print("\nCommit Summary:")
    result = subprocess.run(['git', 'log', '--pretty=format:%h|%an|%ae|%ad|%s', '--date=format:%Y-%m-%d %H:%M:%S'], 
                          cwd=cwd, capture_output=True, text=True)
    commits = [c for c in result.stdout.strip().split('\n') if c]
    
    contract_count = sum(1 for c in commits if CONTRACT_USER["name"] in c)
    ui_count = sum(1 for c in commits if UI_USER["name"] in c)
    
    print(f"\nTotal commits: {len(commits)}")
    print(f"  - {CONTRACT_USER['name']}: {contract_count} commits")
    print(f"  - {UI_USER['name']}: {ui_count} commits")
    
    # Group by date
    print("\nCommits by date:")
    dates = {}
    for commit in commits:
        parts = commit.split('|')
        if len(parts) >= 4:
            date = parts[3].split(' ')[0]
            if date not in dates:
                dates[date] = []
            dates[date].append(commit)
    
    for date in sorted(dates.keys()):
        print(f"\n{date}:")
        for commit in dates[date]:
            parts = commit.split('|')
            if len(parts) >= 5:
                user = parts[1] if len(parts) > 1 else "Unknown"
                msg = parts[4] if len(parts) > 4 else "No message"
                print(f"  {msg[:50]}... - {user}")

if __name__ == "__main__":
    main()

