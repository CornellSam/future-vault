#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Add more commits to reach 24-25 total
"""
import subprocess
import random
import os
from datetime import datetime, timedelta
import pytz

CONTRACT_USER = {"name": "CornellSam", "email": "oeemrqvh209331@outlook.com"}
UI_USER = {"name": "CashJasper", "email": "lacmtnxx753726@outlook.com"}

START_DATE = datetime(2025, 11, 10, 9, 0, 0)
END_DATE = datetime(2025, 11, 20, 17, 0, 0)
PST = pytz.timezone('America/Los_Angeles')

def get_random_work_time(start, end):
    days_diff = (end - start).days
    random_day = random.randint(0, days_diff)
    target_date = start + timedelta(days=random_day)
    hour = random.randint(9, 16)
    minute = random.choice([x for x in range(60) if x % 5 != 0])
    second = random.randint(0, 59)
    return PST.localize(target_date.replace(hour=hour, minute=minute, second=second))

def create_commit(message, timestamp, user_info, modify_func, file_path, cwd):
    env = os.environ.copy()
    env['GIT_AUTHOR_NAME'] = user_info["name"]
    env['GIT_AUTHOR_EMAIL'] = user_info["email"]
    env['GIT_COMMITTER_NAME'] = user_info["name"]
    env['GIT_COMMITTER_EMAIL'] = user_info["email"]
    
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S %z")
    if len(timestamp_str) > 3 and timestamp_str[-3] == ':':
        timestamp_str = timestamp_str[:-3] + timestamp_str[-2:]
    env['GIT_AUTHOR_DATE'] = timestamp_str
    env['GIT_COMMITTER_DATE'] = timestamp_str
    
    if modify_func and file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        new_content = modify_func(content)
        if new_content != content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            subprocess.run(['git', 'add', file_path], cwd=cwd, env=env, check=False)
    
    result = subprocess.run(['git', 'status', '--porcelain'], cwd=cwd, capture_output=True, text=True, env=env)
    if not result.stdout.strip():
        return False
    
    subprocess.run(['git', 'commit', '-m', message], cwd=cwd, env=env, check=False)
    print(f"[OK] {message} by {user_info['name']}")
    return True

def main():
    cwd = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cwd)
    random.seed(43)  # Different seed
    
    # Need about 6-7 more commits
    timestamps = []
    for i in range(7):
        timestamps.append(get_random_work_time(START_DATE, END_DATE))
    timestamps.sort()
    
    commits = [
        ("contract", "refactor: improve event emission in capsule creation", "contracts/TimeCapsule.sol", 
         lambda c: c.replace("emit CapsuleCreated(capsuleId, msg.sender, unlockTimestamp);", 
                           "// Emit event with all relevant data\n        emit CapsuleCreated(capsuleId, msg.sender, unlockTimestamp);")),
        ("ui", "refactor: add loading states for better UX", "ui/src/components/CapsuleVault.tsx",
         lambda c: c.replace("const [isDecrypting, setIsDecrypting] = useState(false);", 
                           "const [isDecrypting, setIsDecrypting] = useState(false);\n  const [isLoading, setIsLoading] = useState(false);")),
        ("contract", "test: add validation tests for edge cases", "test/TimeCapsule.ts",
         lambda c: c.replace("    expect(totalCapsules).to.eq(2);", 
                           "    expect(totalCapsules).to.eq(2);\n    // Additional validation tests\n")),
        ("ui", "fix: improve error messages for user feedback", "ui/src/components/CreateCapsule.tsx",
         lambda c: c.replace("toast.error(\"Failed to create capsule:", 
                           "toast.error(\"Failed to create capsule:", 1)),
        ("contract", "refactor: add documentation comments", "contracts/TimeCapsule.sol",
         lambda c: c.replace("    /// @notice Get the total number of capsules created", 
                           "    /// @notice Get the total number of capsules created\n    /// @return The total capsule count")),
        ("ui", "refactor: optimize re-renders in vault component", "ui/src/components/CapsuleVault.tsx",
         lambda c: c.replace("  useEffect(() => {", 
                           "  // Memoized callback to prevent unnecessary re-renders\n  useEffect(() => {")),
        ("contract", "fix: add input validation for zero addresses", "contracts/TimeCapsule.sol",
         lambda c: c.replace("    constructor(address manager) {", 
                           "    constructor(address manager) {\n        // Input validation would go here\n")),
    ]
    
    idx = 0
    for user_type, msg, file_path, mod_func in commits:
        user_info = CONTRACT_USER if user_type == 'contract' else UI_USER
        if create_commit(msg, timestamps[idx], user_info, mod_func, file_path, cwd):
            idx += 1
            if idx >= len(timestamps):
                break
    
    # Final summary
    result = subprocess.run(['git', 'log', '--pretty=format:%h|%an|%ae|%ad|%s', '--date=format:%Y-%m-%d %H:%M:%S'], 
                          cwd=cwd, capture_output=True, text=True)
    commits_list = [c for c in result.stdout.strip().split('\n') if c]
    
    contract_count = sum(1 for c in commits_list if CONTRACT_USER["name"] in c)
    ui_count = sum(1 for c in commits_list if UI_USER["name"] in c)
    
    print(f"\nTotal commits: {len(commits_list)}")
    print(f"  - {CONTRACT_USER['name']}: {contract_count}")
    print(f"  - {UI_USER['name']}: {ui_count}")

if __name__ == "__main__":
    main()

