#!/usr/bin/env python3
import subprocess

def check_commit_manually(commit_hash):
    """Manually check if a commit has real changes"""
    print(f"\n=== Checking commit {commit_hash[:8]} ===")

    # Get files changed
    result = subprocess.run(['git', 'show', '--name-only', commit_hash],
                          capture_output=True, text=True, cwd='.')
    files = [line.strip() for line in result.stdout.split('\n')[4:] if line.strip()]

    print(f"Files changed: {files}")

    # Check if any files are real (not dummy)
    real_files = [f for f in files if not f.startswith('dummy_commit_')]
    dummy_files = [f for f in files if f.startswith('dummy_commit_')]

    print(f"Real files: {len(real_files)} - {real_files}")
    print(f"Dummy files: {len(dummy_files)} - {dummy_files}")

    if real_files:
        # Get the diff
        result = subprocess.run(['git', 'show', commit_hash],
                              capture_output=True, text=True, cwd='.')
        diff_lines = [line for line in result.stdout.split('\n') if line.startswith('+') or line.startswith('-')]
        print(f"Diff lines: {len(diff_lines)}")
        for line in diff_lines[:10]:  # Show first 10 diff lines
            print(f"  {line}")

        return True
    else:
        return False

# Check some commits
commits_to_check = [
    '8b6e932be6448eaef880f9d54b91bcd4d0236c92',  # App.tsx changes
    'bd21f1d1f11d8acf78ec196e16a05eece02dc668',  # RainbowKit config
    '2421bc922efd7acb759587c1c67ef24dc3c89c2c',   # Contract changes
    '1de033f22df23767e56af0b0b33c3662ae28bbea',  # dummy file
]

for commit in commits_to_check:
    has_real_changes = check_commit_manually(commit)
    print(f"Result: {'VALID' if has_real_changes else 'INVALID'}")
