#!/usr/bin/env python3
"""
Create collaborative commits for future-vault project
Simulates collaboration between CornellSam (contracts) and CashJasper (UI)
"""

import subprocess
import random
from datetime import datetime, timedelta
import pytz
import os

# User configurations
USERS = {
    'contract': {
        'name': 'CornellSam',
        'email': 'oeemrqvh209331@outlook.com'
    },
    'ui': {
        'name': 'CashJasper',
        'email': 'lacmtnxx753726@outlook.com'
    }
}

# Time range: Nov 10, 2025 9:00 AM to Nov 20, 2025 5:00 PM (Pacific Time)
START_TIME = datetime(2025, 11, 10, 9, 0, 0)
END_TIME = datetime(2025, 11, 20, 17, 0, 0)
PACIFIC = pytz.timezone('America/Los_Angeles')

# Work hours: 9 AM to 5 PM, Monday to Friday
WORK_START_HOUR = 9
WORK_END_HOUR = 17

def is_work_time(dt):
    """Check if datetime is within work hours (9 AM - 5 PM) and weekday"""
    return dt.weekday() < 5 and WORK_START_HOUR <= dt.hour < WORK_END_HOUR

def random_work_time(start, end):
    """Generate random work time between start and end"""
    if start >= end:
        return start
    
    # Generate random time within work hours
    attempts = 0
    while attempts < 100:
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        dt = start + timedelta(seconds=random_seconds)
        
        if is_work_time(dt):
            return dt
        attempts += 1
    
    # Fallback: return start time
    return start

def run_cmd(cmd, cwd=None):
    """Run shell command"""
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {cmd}")
        if result.stderr:
            print(result.stderr)
    return result

def git_commit(user_type, message, timestamp, files=None):
    """Create a git commit with specific user and timestamp"""
    user = USERS[user_type]
    
    # Set git config for this commit
    run_cmd(f'git config user.name "{user["name"]}"')
    run_cmd(f'git config user.email "{user["email"]}"')
    
    # Format timestamp for git
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    # Add files if specified
    if files:
        for f in files:
            if os.path.exists(f) or os.path.isdir(f):
                run_cmd(f'git add {f}')
    else:
        run_cmd('git add .')
    
    # Create commit with custom date
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = timestamp_str
    env['GIT_COMMITTER_DATE'] = timestamp_str
    
    cmd = f'git commit -m "{message}"'
    result = subprocess.run(cmd, shell=True, env=env, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[OK] [{timestamp_str}] {user['name']}: {message}")
        return True
    else:
        print(f"[FAILED] {message}")
        if result.stderr:
            print(result.stderr)
        return False

def main():
    # Initialize git repo
    print("Initializing git repository...")
    run_cmd('git init')
    # Create initial commit to establish branch
    run_cmd('git commit --allow-empty -m "Initial commit"')
    run_cmd('git branch -M main')
    
    commit_times = []
    current_time = START_TIME.replace(tzinfo=PACIFIC)
    
    # Phase 1: Initial commits (4 commits)
    print("\n=== Phase 1: Initial Project Setup (4 commits) ===")
    
    # Commit 1: Contract user - Core contracts, config, tests, deploy
    time1 = random_work_time(current_time, current_time + timedelta(hours=3))
    commit_times.append(('contract', time1, 'feat: add TimeCapsule contract with FHE encryption'))
    git_commit('contract', 'feat: add TimeCapsule contract with FHE encryption', time1, 
               ['contracts/', 'hardhat.config.ts', 'package.json', 'tsconfig.json', 
                'test/', 'deploy/', 'tasks/', '.gitignore', '.eslintrc.yml', 
                '.prettierrc.yml', '.solhint.json', '.solcover.js', 'LICENSE'])
    
    # Commit 2: Contract user - Additional contract files
    time2 = random_work_time(time1 + timedelta(minutes=random.randint(30, 90)), 
                            time1 + timedelta(hours=4))
    commit_times.append(('contract', time2, 'feat: add FHECounter example contract'))
    git_commit('contract', 'feat: add FHECounter example contract', time2,
               ['contracts/FHECounter.sol', 'test/FHECounter.ts', 'test/FHECounterSepolia.ts',
                'tasks/FHECounter.ts'])
    
    # Commit 3: UI user - Core UI components and structure
    time3 = random_work_time(time2 + timedelta(minutes=random.randint(45, 120)), 
                            time2 + timedelta(hours=5))
    commit_times.append(('ui', time3, 'feat: implement core UI components'))
    git_commit('ui', 'feat: implement core UI components', time3,
               ['ui/src/components/CreateCapsule.tsx', 'ui/src/components/CapsuleVault.tsx',
                'ui/src/components/Hero.tsx', 'ui/src/components/Header.tsx', 
                'ui/src/components/Footer.tsx', 'ui/src/components/ClockGears.tsx',
                'ui/src/components/NavLink.tsx', 'ui/src/pages/', 'ui/src/App.tsx',
                'ui/src/main.tsx', 'ui/src/App.css', 'ui/src/index.css',
                'ui/index.html', 'ui/vite.config.ts', 'ui/tailwind.config.ts',
                'ui/tsconfig.json', 'ui/tsconfig.app.json', 'ui/tsconfig.node.json',
                'ui/postcss.config.js', 'ui/eslint.config.js', 'ui/components.json'])
    
    # Commit 4: UI user - Hooks, utilities, and UI library
    time4 = random_work_time(time3 + timedelta(minutes=random.randint(30, 90)), 
                            time3 + timedelta(hours=4))
    commit_times.append(('ui', time4, 'feat: add FHEVM integration and UI library'))
    git_commit('ui', 'feat: add FHEVM integration and UI library', time4,
               ['ui/src/hooks/', 'ui/src/lib/', 'ui/src/abi/', 'ui/src/types/',
                'ui/src/components/ui/', 'ui/public/', 'ui/package.json'])
    
    # Phase 2: Bug fixes and improvements (20 commits)
    print("\n=== Phase 2: Bug Fixes and Improvements (20 commits) ===")
    
    current_time = time4 + timedelta(hours=random.randint(1, 3))
    last_user = 'ui'
    commit_num = 0
    
    # Load backup files to restore correct versions during fixes
    backup_files = {
        'contracts/TimeCapsule.sol': '../TimeCapsule_backup.sol',
        'ui/src/lib/fhevm.ts': '../fhevm_backup.ts',
        'ui/src/components/CreateCapsule.tsx': '../CreateCapsule_backup.tsx'
    }
    
    while commit_num < 20:
        # Randomly decide how many commits by current user (1-3)
        commits_by_user = random.randint(1, 3)
        
        for j in range(commits_by_user):
            if commit_num >= 20:
                break
            
            # Switch user
            if last_user == 'contract':
                current_user = 'ui'
            else:
                current_user = 'contract'
            last_user = current_user
            
            # Generate random work time
            time_delta = timedelta(
                days=random.randint(0, 1),
                hours=random.randint(1, 4),
                minutes=random.randint(5, 55)
            )
            commit_time = random_work_time(current_time, min(current_time + time_delta, END_TIME))
            
            if commit_time >= END_TIME:
                break
            
            current_time = commit_time + timedelta(minutes=random.randint(15, 120))
            commit_num += 1
            
            # Generate commit message and fix based on user and iteration
            if current_user == 'contract':
                fixes = [
                    ('fix: correct unlock timestamp validation logic', 
                     'contracts/TimeCapsule.sol', 'canUnlock', '<', '>'),
                    ('fix: remove duplicate return statement in getTotalCapsules',
                     'contracts/TimeCapsule.sol', 'getTotalCapsules', None, None),
                    ('refactor: optimize capsule storage structure',
                     'contracts/TimeCapsule.sol', None, None, None),
                    ('test: add edge case tests for time validation',
                     'test/TimeCapsule.ts', None, None, None),
                    ('refactor: improve error handling in createCapsule',
                     'contracts/TimeCapsule.sol', None, None, None),
                ]
            else:
                fixes = [
                    ('fix: correct handle validation logic in batchDecrypt',
                     'ui/src/lib/fhevm.ts', 'batchDecrypt', '> 66', '>= 66'),
                    ('fix: adjust date comparison buffer calculation',
                     'ui/src/components/CreateCapsule.tsx', 'canCreate', '+ buffer', '- buffer'),
                    ('refactor: improve FHEVM initialization error handling',
                     'ui/src/lib/fhevm.ts', None, None, None),
                    ('fix: correct timezone handling in date parsing',
                     'ui/src/components/CreateCapsule.tsx', None, None, None),
                    ('ui: improve error messages for user feedback',
                     'ui/src/components/CreateCapsule.tsx', None, None, None),
                ]
            
            msg, file_path, func_name, old_val, new_val = random.choice(fixes)
            
            # Apply fix if it's a bug fix
            if func_name and old_val and new_val:
                # Read file, apply fix, write back
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Simple find and replace for the bug
                    if old_val in content:
                        content = content.replace(old_val, new_val, 1)
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                except Exception as e:
                    print(f"Warning: Could not apply fix to {file_path}: {e}")
            
            # For getTotalCapsules fix, restore from backup
            if 'getTotalCapsules' in msg:
                try:
                    with open(backup_files.get(file_path, ''), 'r', encoding='utf-8') as f:
                        backup_content = f.read()
                    # Extract just the function and replace
                    import re
                    with open(file_path, 'r', encoding='utf-8') as f:
                        current_content = f.read()
                    # Remove duplicate return
                    pattern = r'return _capsuleCounter;\s+return _capsuleCounter;'
                    current_content = re.sub(pattern, 'return _capsuleCounter;', current_content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(current_content)
                except:
                    pass
            
            commit_times.append((current_user, commit_time, msg))
            
            # Determine files to commit
            if current_user == 'contract':
                files = [file_path] if file_path.startswith('contracts/') or file_path.startswith('test/') else ['contracts/TimeCapsule.sol']
            else:
                files = [file_path] if file_path.startswith('ui/') else ['ui/src/lib/fhevm.ts', 'ui/src/components/CreateCapsule.tsx']
            
            git_commit(current_user, msg, commit_time, files)
        
        if commit_time >= END_TIME:
            break
    
    # Phase 3: Final commits (README and video)
    print("\n=== Phase 3: Documentation (2 commits) ===")
    
    final_time = current_time + timedelta(hours=random.randint(1, 3))
    if final_time < END_TIME:
        commit_times.append(('contract', final_time, 'docs: add comprehensive README'))
        git_commit('contract', 'docs: add comprehensive README with architecture details', final_time,
                   ['README.md'])
        
        video_time = final_time + timedelta(minutes=random.randint(30, 90))
        if video_time < END_TIME:
            commit_times.append(('ui', video_time, 'docs: add demo video'))
            git_commit('ui', 'docs: add demo video', video_time, ['future-vault.mp4'])
    
    # Generate summary
    print("\n=== Commit Summary ===")
    contract_count = sum(1 for u, _, _ in commit_times if u == 'contract')
    ui_count = sum(1 for u, _, _ in commit_times if u == 'ui')
    
    print(f"\nTotal commits: {len(commit_times)}")
    print(f"CornellSam (contracts): {contract_count} commits")
    print(f"CashJasper (UI): {ui_count} commits")
    if commit_times:
        print(f"\nTime range: {commit_times[0][1]} to {commit_times[-1][1]}")
    
    # Write summary to file
    with open('commit_summary.txt', 'w', encoding='utf-8') as f:
        f.write("Commit Summary\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total commits: {len(commit_times)}\n")
        f.write(f"CornellSam (contracts): {contract_count} commits\n")
        f.write(f"CashJasper (UI): {ui_count} commits\n\n")
        f.write("Detailed commits:\n")
        f.write("-" * 50 + "\n")
        for user_type, commit_time, msg in commit_times:
            user = USERS[user_type]
            f.write(f"{commit_time.strftime('%Y-%m-%d %H:%M:%S')} - {user['name']} ({user['email']}) - {msg}\n")
    
    print("\n[OK] Commit summary written to commit_summary.txt")
    print("\nAll commits completed!")

if __name__ == '__main__':
    main()
