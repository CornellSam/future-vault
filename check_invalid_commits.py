#!/usr/bin/env python3
import subprocess
import os

def get_commit_stats():
    """Get all commits with their stats"""
    result = subprocess.run(['git', 'log', '--oneline', '--pretty=format:%H %s'],
                          capture_output=True, text=True, cwd='.')
    commits = []
    for line in result.stdout.strip().split('\n'):
        if line:
            parts = line.split(' ', 1)
            if len(parts) == 2:
                commit_hash, message = parts
                commits.append((commit_hash, message))
    return commits

def analyze_commit(commit_hash):
    """Analyze a single commit to see if it's valid"""
    # Get the stat
    result = subprocess.run(['git', 'show', '--stat', commit_hash],
                          capture_output=True, text=True, cwd='.')

    stat_lines = result.stdout.strip().split('\n')
    changed_files = []
    for line in stat_lines:
        if '|' in line and ('insertion' in line or 'deletion' in line):
            # Parse file change line
            parts = line.split('|')
            if len(parts) >= 2:
                filename = parts[0].strip()
                if filename:
                    changed_files.append(filename)

    # Check if it's just dummy files
    dummy_files = [f for f in changed_files if f.startswith('dummy_commit_')]
    real_files = [f for f in changed_files if not f.startswith('dummy_commit_')]

    is_dummy_only = len(real_files) == 0

    # Check if changes are minimal (just comments or small changes)
    if not is_dummy_only:
        # Get the actual diff
        result = subprocess.run(['git', 'show', commit_hash],
                              capture_output=True, text=True, cwd='.')
        diff_content = result.stdout

        # Count actual code changes (exclude comments and whitespace)
        code_changes = 0
        for line in diff_content.split('\n'):
            if line.startswith('+') or line.startswith('-'):
                line_content = line[1:].strip()
                # Skip comments and empty lines
                if line_content and not line_content.startswith('//') and not line_content.startswith('/*') and not line_content.startswith('*') and not line_content.startswith('*/'):
                    code_changes += 1

        is_minimal = code_changes < 3  # Less than 3 actual code lines changed
    else:
        is_minimal = True

    return {
        'hash': commit_hash,
        'is_dummy_only': is_dummy_only,
        'is_minimal': is_minimal,
        'changed_files': changed_files
    }

def main():
    print("Checking for invalid commits...")
    print("=" * 60)

    commits = get_commit_stats()
    invalid_commits = []
    valid_commits = []

    for commit_hash, message in commits:
        analysis = analyze_commit(commit_hash)

        commit_info = {
            'hash': commit_hash[:8],
            'message': message,
            'analysis': analysis
        }

        if analysis['is_dummy_only'] or analysis['is_minimal']:
            invalid_commits.append(commit_info)
            print(f"INVALID: {commit_hash[:8]} - {message}")
            if analysis['is_dummy_only']:
                print("   Reason: Only contains dummy/temporary files")
            elif analysis['is_minimal']:
                print(f"   Reason: Minimal changes ({len(analysis['changed_files'])} files, mostly comments/whitespace)")
            print(f"   Files changed: {analysis['changed_files']}")
            print()
        else:
            valid_commits.append(commit_info)

    print("=" * 60)
    print(f"Summary:")
    print(f"Total commits: {len(commits)}")
    print(f"Valid commits: {len(valid_commits)}")
    print(f"Invalid commits: {len(invalid_commits)}")
    print()

    if invalid_commits:
        print("Invalid commits that should be removed:")
        for commit in invalid_commits:
            print(f"  {commit['hash']} - {commit['message']}")
    else:
        print("No invalid commits found!")

if __name__ == "__main__":
    main()
