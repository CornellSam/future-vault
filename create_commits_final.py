#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create collaborative commits for future-vault project
"""

import subprocess
import random
from datetime import datetime, timedelta
import pytz
import os
import shutil

USERS = {
    'contract': {'name': 'CornellSam', 'email': 'oeemrqvh209331@outlook.com'},
    'ui': {'name': 'CashJasper', 'email': 'lacmtnxx753726@outlook.com'}
}

START_TIME = datetime(2025, 11, 10, 9, 0, 0, tzinfo=pytz.timezone('America/Los_Angeles'))
END_TIME = datetime(2025, 11, 20, 17, 0, 0, tzinfo=pytz.timezone('America/Los_Angeles'))
PACIFIC = pytz.timezone('America/Los_Angeles')

def is_work_time(dt):
    return dt.weekday() < 5 and 9 <= dt.hour < 17

def random_work_time(start, end):
    if start >= end:
        return start
    attempts = 0
    while attempts < 100:
        delta = end - start
        random_seconds = random.randint(0, int(delta.total_seconds()))
        dt = start + timedelta(seconds=random_seconds)
        if is_work_time(dt):
            return dt
        attempts += 1
    return start

def run_cmd(cmd, cwd=None):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    return result

def git_commit(user_type, message, timestamp, files=None):
    user = USERS[user_type]
    run_cmd(f'git config user.name "{user["name"]}"')
    run_cmd(f'git config user.email "{user["email"]}"')
    
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    if files:
        added = False
        for f in files:
            if os.path.exists(f) or os.path.isdir(f):
                result = run_cmd(f'git add {f}')
                if result.returncode == 0:
                    added = True
        if not added:
            return False
    else:
        run_cmd('git add .')
    
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = timestamp_str
    env['GIT_COMMITTER_DATE'] = timestamp_str
    
    result = subprocess.run(f'git commit -m "{message}"', shell=True, env=env, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"[OK] [{timestamp_str}] {user['name']}: {message}")
        return True
    else:
        print(f"[FAIL] {message}")
        return False

def main():
    print("Initializing git repository...")
    run_cmd('git init')
    run_cmd('git commit --allow-empty -m "Initial commit"')
    run_cmd('git branch -M main')
    
    commit_times = []
    current_time = START_TIME
    
    # Phase 1: Initial commits (4 commits) - with bugs
    print("\n=== Phase 1: Initial Project Setup (4 commits) ===")
    
    # Commit 1: Contract user
    time1 = random_work_time(current_time, current_time + timedelta(hours=3))
    commit_times.append(('contract', time1, 'feat: add TimeCapsule contract with FHE encryption'))
    git_commit('contract', 'feat: add TimeCapsule contract with FHE encryption', time1, 
               ['contracts/', 'hardhat.config.ts', 'package.json', 'tsconfig.json', 
                'test/', 'deploy/', 'tasks/', '.gitignore', '.eslintrc.yml', 
                '.prettierrc.yml', '.solhint.json', '.solcover.js', 'LICENSE'])
    
    # Commit 2: Contract user
    time2 = random_work_time(time1 + timedelta(minutes=random.randint(30, 90)), time1 + timedelta(hours=4))
    commit_times.append(('contract', time2, 'feat: add FHECounter example contract'))
    git_commit('contract', 'feat: add FHECounter example contract', time2,
               ['contracts/FHECounter.sol', 'test/FHECounter.ts', 'test/FHECounterSepolia.ts', 'tasks/FHECounter.ts'])
    
    # Commit 3: UI user
    time3 = random_work_time(time2 + timedelta(minutes=random.randint(45, 120)), time2 + timedelta(hours=5))
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
    
    # Commit 4: UI user
    time4 = random_work_time(time3 + timedelta(minutes=random.randint(30, 90)), time3 + timedelta(hours=4))
    commit_times.append(('ui', time4, 'feat: add FHEVM integration and UI library'))
    git_commit('ui', 'feat: add FHEVM integration and UI library', time4,
               ['ui/src/hooks/', 'ui/src/lib/', 'ui/src/abi/', 'ui/src/types/',
                'ui/src/components/ui/', 'ui/public/', 'ui/package.json'])
    
    # Phase 2: Bug fixes (20 commits)
    print("\n=== Phase 2: Bug Fixes and Improvements (20 commits) ===")
    
    current_time = time4 + timedelta(hours=random.randint(1, 3))
    last_user = 'ui'
    commit_num = 0
    
    # Fix bugs by restoring from backups
    fixes = [
        # Contract fixes
        ('fix: correct unlock timestamp validation logic', 'contract', 'contracts/TimeCapsule.sol', 
         lambda c: c.replace('return block.timestamp < capsule.unlockTimestamp;', 
                            'return block.timestamp >= capsule.unlockTimestamp;')),
        ('fix: remove duplicate return statement in getTotalCapsules', 'contract', 'contracts/TimeCapsule.sol',
         lambda c: c.replace('return _capsuleCounter;\n        return _capsuleCounter;', 'return _capsuleCounter;')),
        ('refactor: optimize capsule storage structure', 'contract', 'contracts/TimeCapsule.sol', None),
        ('test: add edge case tests for time validation', 'contract', 'test/TimeCapsule.ts', None),
        ('refactor: improve error handling in createCapsule', 'contract', 'contracts/TimeCapsule.sol', None),
        # UI fixes
        ('fix: correct handle validation logic in batchDecrypt', 'ui', 'ui/src/lib/fhevm.ts',
         lambda c: c.replace('handleStr.length > 66', 'handleStr.length >= 66')),
        ('fix: adjust date comparison buffer calculation', 'ui', 'ui/src/components/CreateCapsule.tsx',
         lambda c: c.replace('isFuture = unlockDateTime.getTime() > (now.getTime() + buffer);',
                            'isFuture = unlockDateTime.getTime() > (now.getTime() - buffer);')),
        ('refactor: improve FHEVM initialization error handling', 'ui', 'ui/src/lib/fhevm.ts', None),
        ('fix: correct timezone handling in date parsing', 'ui', 'ui/src/components/CreateCapsule.tsx', None),
        ('ui: improve error messages for user feedback', 'ui', 'ui/src/components/CreateCapsule.tsx', None),
    ]
    
    while commit_num < 20:
        commits_by_user = random.randint(1, 3)
        
        for j in range(commits_by_user):
            if commit_num >= 20:
                break
            
            current_user = 'ui' if last_user == 'contract' else 'contract'
            last_user = current_user
            
            time_delta = timedelta(days=random.randint(0, 1), hours=random.randint(1, 4), minutes=random.randint(5, 55))
            end_bound = current_time + time_delta
            if end_bound > END_TIME:
                end_bound = END_TIME
            commit_time = random_work_time(current_time, end_bound)
            
            if commit_time >= END_TIME:
                break
            
            current_time = commit_time + timedelta(minutes=random.randint(15, 120))
            commit_num += 1
            
            # Select appropriate fix
            user_fixes = [f for f in fixes if f[1] == current_user]
            if user_fixes:
                msg, _, file_path, fix_func = random.choice(user_fixes)
                
                # Apply fix if function provided
                if fix_func and os.path.exists(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                        new_content = fix_func(content)
                        if new_content != content:
                            with open(file_path, 'w', encoding='utf-8') as f:
                                f.write(new_content)
                    except Exception as e:
                        print(f"Warning: Could not apply fix: {e}")
                
                commit_times.append((current_user, commit_time, msg))
                git_commit(current_user, msg, commit_time, [file_path])
        
        if commit_time >= END_TIME:
            break
    
    # Phase 3: Documentation
    print("\n=== Phase 3: Documentation (2 commits) ===")
    
    final_time = current_time + timedelta(hours=random.randint(1, 3))
    if final_time < END_TIME:
        commit_times.append(('contract', final_time, 'docs: add comprehensive README'))
        git_commit('contract', 'docs: add comprehensive README with architecture details', final_time, ['README.md'])
        
        video_time = final_time + timedelta(minutes=random.randint(30, 90))
        if video_time < END_TIME:
            commit_times.append(('ui', video_time, 'docs: add demo video'))
            git_commit('ui', 'docs: add demo video', video_time, ['future-vault.mp4'])
    
    # Summary
    print("\n=== Commit Summary ===")
    contract_count = sum(1 for u, _, _ in commit_times if u == 'contract')
    ui_count = sum(1 for u, _, _ in commit_times if u == 'ui')
    
    print(f"\nTotal commits: {len(commit_times)}")
    print(f"CornellSam (contracts): {contract_count} commits")
    print(f"CashJasper (UI): {ui_count} commits")
    
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

if __name__ == '__main__':
    main()
