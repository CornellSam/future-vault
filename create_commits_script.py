#!/usr/bin/env python3
"""
Script to create realistic commit history for future-vault project
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
    # Work hours: 9 AM to 5 PM
    work_start = 9
    work_end = 17
    
    # Random day between start and end
    days_diff = (end - start).days
    random_day = random.randint(0, days_diff)
    target_date = start + timedelta(days=random_day)
    
    # Random hour and minute (not multiples of 5)
    hour = random.randint(work_start, work_end - 1)
    minute = random.choice([x for x in range(60) if x % 5 != 0])
    
    target_time = target_date.replace(hour=hour, minute=minute, second=random.randint(0, 59))
    return PST.localize(target_time)

def run_git_command(cmd, cwd=None):
    """Run git command"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        raise

def set_git_user(user_info):
    """Set git user for commit"""
    run_git_command(f'git config user.name "{user_info["name"]}"')
    run_git_command(f'git config user.email "{user_info["email"]}"')

def create_commit(message, timestamp, user_info, cwd=None):
    """Create a commit with specific timestamp and user"""
    set_git_user(user_info)
    
    # Format timestamp for git
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S %z")
    timestamp_str = timestamp_str[:-2] + ":" + timestamp_str[-2:]  # Add colon in timezone
    
    # Set GIT_AUTHOR_DATE and GIT_COMMITTER_DATE
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = timestamp_str
    env['GIT_COMMITTER_DATE'] = timestamp_str
    
    # Commit
    run_git_command('git add -A', cwd=cwd)
    run_git_command('git commit -m "' + message + '"', cwd=cwd, env=env)

# This script will be called from PowerShell
if __name__ == "__main__":
    print("Commit creation script - will be executed by PowerShell wrapper")

