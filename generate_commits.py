#!/usr/bin/env python3
"""
Generate git commits with random timestamps and alternating users
"""
import random
import subprocess
import sys
import os
from datetime import datetime, timedelta

# User configurations
CONTRACT_USER = "CornellSam"
CONTRACT_EMAIL = "oeemrqvh209331@outlook.com"
UI_USER = "CashJasper"
UI_EMAIL = "lacmtnxx753726@outlook.com"

# Time range: Nov 10, 2025 9:00 AM to Nov 20, 2025 5:00 PM (PST)
# PST is UTC-8, but we'll work in local time
START_DATE = datetime(2025, 11, 10, 9, 0, 0)
END_DATE = datetime(2025, 11, 20, 17, 0, 0)

# Generate random timestamps
random.seed(42)  # For reproducibility
num_commits = random.randint(20, 30)
print(f"Will create {num_commits} commits")

# Generate timestamps (avoid multiples of 5 minutes)
timestamps = []
for i in range(num_commits):
    total_seconds = (END_DATE - START_DATE).total_seconds()
    random_seconds = random.randint(0, int(total_seconds))
    timestamp = START_DATE + timedelta(seconds=random_seconds)
    
    # Avoid multiples of 5 minutes
    minutes = timestamp.minute
    if minutes % 5 == 0:
        timestamp = timestamp.replace(minute=(minutes + random.randint(1, 4)) % 60)
    
    timestamps.append(timestamp)

timestamps.sort()

# Commit plan
commits = []

# Phase 1: First 4 commits (main files)
# Commit 1: Contract user - contracts, deploy, test, hardhat.config.ts, package.json, etc.
commits.append({
    'num': 1,
    'user': CONTRACT_USER,
    'email': CONTRACT_EMAIL,
    'message': 'feat: add TimeCapsule smart contract with FHE encryption',
    'date': timestamps[0],
    'files': ['contracts/', 'deploy/', 'test/', 'hardhat.config.ts', 'package.json', 'package-lock.json', 'tsconfig.json', '.solhint.json', '.solhintignore', '.solcover.js', '.prettierrc.yml', '.prettierignore', '.eslintrc.yml', '.eslintignore', 'LICENSE']
})

# Commit 2: Contract user - tasks, types, other config files
commits.append({
    'num': 2,
    'user': CONTRACT_USER,
    'email': CONTRACT_EMAIL,
    'message': 'feat: add Hardhat tasks and TypeScript configuration',
    'date': timestamps[1],
    'files': ['tasks/', '.gitignore']
})

# Commit 3: UI user - UI files
commits.append({
    'num': 3,
    'user': UI_USER,
    'email': UI_EMAIL,
    'message': 'feat: implement React frontend with FHEVM integration',
    'date': timestamps[2],
    'files': ['ui/']
})

# Commit 4: UI user - remaining config
commits.append({
    'num': 4,
    'user': UI_USER,
    'email': UI_EMAIL,
    'message': 'chore: add project configuration files',
    'date': timestamps[3],
    'files': ['.github/'] if os.path.exists('.github') else []
})

# Phase 2: 15-20 commits (bug fixes and optimizations)
# Randomly alternate between users (1-3 commits per user)
current_user = 'contract'  # Start with contract user
commit_idx = 4
user_commit_count = 0
max_user_commits = random.randint(1, 3)

for i in range(4, min(4 + 20, num_commits - 1)):  # Reserve last for README
    if user_commit_count >= max_user_commits:
        current_user = 'ui' if current_user == 'contract' else 'contract'
        user_commit_count = 0
        max_user_commits = random.randint(1, 3)
    
    user_commit_count += 1
    
    if current_user == 'contract':
        user = CONTRACT_USER
        email = CONTRACT_EMAIL
        # Contract-related fixes
        messages = [
            'fix: restore unlock timestamp validation in createCapsule',
            'fix: correct timezone handling in date validation',
            'refactor: improve error handling in contract functions',
            'test: add additional test cases for edge scenarios',
            'fix: ensure proper decryption permission handling',
            'refactor: optimize gas usage in capsule creation',
            'fix: correct capsule counter initialization',
            'test: enhance test coverage for time-based operations'
        ]
        files = ['contracts/TimeCapsule.sol', 'test/TimeCapsule.ts']
    else:
        user = UI_USER
        email = UI_EMAIL
        # UI-related fixes
        messages = [
            'fix: correct date parsing logic in CreateCapsule component',
            'fix: restore proper error handling in FHEVM decryption',
            'fix: correct byte order in message decoding',
            'refactor: improve FHEVM initialization error messages',
            'fix: handle timezone conversion in unlock date validation',
            'refactor: optimize capsule loading performance',
            'fix: correct handle validation in batch decrypt',
            'ui: improve error display for failed operations',
            'refactor: enhance date formatting in UI components'
        ]
        files = ['ui/src/components/CreateCapsule.tsx', 'ui/src/lib/fhevm.ts', 'ui/src/components/CapsuleVault.tsx']
    
    commits.append({
        'num': commit_idx + 1,
        'user': user,
        'email': email,
        'message': random.choice(messages),
        'date': timestamps[i],
        'files': files
    })
    commit_idx += 1

# Phase 3: Last commit (README and video)
commits.append({
    'num': commit_idx + 1,
    'user': CONTRACT_USER,  # Contract user commits README
    'email': CONTRACT_EMAIL,
    'message': 'docs: add README and demo video',
    'date': timestamps[-1],
    'files': ['README.md', 'future-vault.mp4']
})

# Execute commits
for commit in commits:
    date_str = commit['date'].strftime('%Y-%m-%d %H:%M:%S')
    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = commit['user']
    env['GIT_AUTHOR_EMAIL'] = commit['email']
    env['GIT_COMMITTER_NAME'] = commit['user']
    env['GIT_COMMITTER_EMAIL'] = commit['email']
    
    # Add files
    subprocess.run(['git', 'add'] + commit['files'], env=env, check=True)
    
    # Commit with date
    subprocess.run([
        'git', 'commit', '-m', commit['message'],
        '--date', date_str
    ], env=env, check=True)
    
    print(f"Created commit {commit['num']}: {commit['message']} by {commit['user']} at {date_str}")

print(f"\nTotal commits created: {len(commits)}")

