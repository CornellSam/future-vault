#!/usr/bin/env python3
import os
import random
import subprocess
import datetime

CONTRACT_USER = {'name': 'CornellSam', 'email': 'oeemrqvh209331@outlook.com'}
UI_USER = {'name': 'CashJasper', 'email': 'lacmtnxx753726@outlook.com'}

def set_git_config(name, email):
    subprocess.run(['git', 'config', 'user.name', name], check=True)
    subprocess.run(['git', 'config', 'user.email', email], check=True)

def create_commit(message, timestamp):
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = timestamp
    env['GIT_COMMITTER_DATE'] = timestamp

    # Check if there are changes to commit
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if not result.stdout.strip():
        print(f"No changes to commit for: {message}")
        return False

    subprocess.run(['git', 'add', '.'], check=True)
    result = subprocess.run(['git', 'commit', '-m', message], env=env, capture_output=True, text=True)
    return result.returncode == 0

def generate_timestamps(count=24):
    start_date = datetime.datetime(2025, 11, 10, 9, 0, 0)
    timestamps = []

    for i in range(count):
        hour = random.randint(9, 16)
        minute = random.choice([0, 15, 30, 45])
        timestamp = start_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
        timestamps.append(timestamp)

        # Move to next day occasionally
        if random.random() < 0.2:
            start_date += datetime.timedelta(days=1)

    return sorted(timestamps)

def main():
    timestamps = generate_timestamps(24)

    # Initial files
    with open('contracts/TimeCapsule.sol', 'w', encoding='utf-8') as f:
        f.write('// Contract file')

    set_git_config(CONTRACT_USER['name'], CONTRACT_USER['email'])
    create_commit("feat: add TimeCapsule contract", timestamps[0].strftime('%Y-%m-%dT%H:%M:%S%z'))

    with open('contracts/FHECounter.sol', 'w', encoding='utf-8') as f:
        f.write('// Counter contract')

    set_git_config(CONTRACT_USER['name'], CONTRACT_USER['email'])
    create_commit("feat: add FHECounter contract", timestamps[1].strftime('%Y-%m-%dT%H:%M:%S%z'))

    with open('hardhat.config.ts', 'w', encoding='utf-8') as f:
        f.write('// Hardhat config')

    set_git_config(CONTRACT_USER['name'], CONTRACT_USER['email'])
    create_commit("feat: add Hardhat configuration", timestamps[2].strftime('%Y-%m-%dT%H:%M:%S%z'))

    with open('ui/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write('// React App')

    set_git_config(UI_USER['name'], UI_USER['email'])
    create_commit("feat: initialize React app", timestamps[3].strftime('%Y-%m-%dT%H:%M:%S%z'))

    # More commits
    for i in range(4, 24):
        user = CONTRACT_USER if i % 3 != 0 else UI_USER  # Mix users
        set_git_config(user['name'], user['email'])

        # Create or modify a file
        filename = f"file_{i}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Content for commit {i}")

        create_commit(f"feat: add feature {i}", timestamps[i].strftime('%Y-%m-%dT%H:%M:%S%z'))

    print("=== Final Summary ===")
    result = subprocess.run(['git', 'log', '--oneline'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    print(f"Total commits: {len(lines)}")

    result = subprocess.run(['git', 'shortlog', '-sn', '--no-merges'], capture_output=True, text=True)
    print("\n=== Commits per User ===")
    print(result.stdout)

if __name__ == "__main__":
    main()
