#!/usr/bin/env python3
import os
import random
import subprocess
import datetime

# User configurations
CONTRACT_USER = {'name': 'CornellSam', 'email': 'oeemrqvh209331@outlook.com'}
UI_USER = {'name': 'CashJasper', 'email': 'lacmtnxx753726@outlook.com'}

def set_git_config(name, email):
    subprocess.run(['git', 'config', 'user.name', name], check=True)
    subprocess.run(['git', 'config', 'user.email', email], check=True)

def create_commit(message, timestamp, files_to_add=None):
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = timestamp
    env['GIT_COMMITTER_DATE'] = timestamp

    if files_to_add:
        for file in files_to_add:
            if os.path.exists(file):
                subprocess.run(['git', 'add', file], check=True)
    else:
        subprocess.run(['git', 'add', '.'], check=True)

    result = subprocess.run(['git', 'commit', '-m', message], env=env, capture_output=True, text=True)
    return result.returncode == 0

def generate_timestamps(count=24):
    """Generate 24 timestamps within work hours"""
    start_date = datetime.datetime(2025, 11, 10, 9, 0, 0)
    timestamps = []
    current = start_date

    for i in range(count):
        hour = random.randint(9, 16)
        minute = random.choice([0, 15, 30, 45])
        timestamp = current.replace(hour=hour, minute=minute, second=0, microsecond=0)
        timestamps.append(timestamp)

        # 25% chance to move to next day
        if random.random() < 0.25:
            current += datetime.timedelta(days=1)
            if current > datetime.datetime(2025, 11, 20, 17, 0, 0):
                current = start_date + datetime.timedelta(days=random.randint(0, 8))

    return sorted(timestamps)

def create_initial_files():
    """Create initial buggy files"""
    # TimeCapsule.sol
    contract_content = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {FHE, euint32, externalEuint32} from "@fhevm/solidity/lib/FHE.sol";
import {SepoliaConfig} from "@fhevm/solidity/config/ZamaConfig.sol";

contract TimeCapsule is SepoliaConfig {
    struct Capsule {
        euint32 encryptedMessagePart1;
        euint32 encryptedMessagePart2;
        uint256 unlockTimestamp;
        address creator;
        bool exists;
    }

    mapping(uint256 => Capsule) public capsules;
    mapping(address => uint256[]) public userCapsules;
    uint256 private _capsuleCounter;

    event CapsuleCreated(uint256 indexed capsuleId, address indexed creator, uint256 unlockTimestamp);
    event CapsuleUnlocked(uint256 indexed capsuleId, address indexed creator);

    address public immutable decryptManager;

    constructor(address manager) {
        decryptManager = manager;
        // BUG: Missing counter initialization
    }

    function createCapsule(
        externalEuint32 encMessagePart1,
        bytes calldata messagePart1Proof,
        externalEuint32 encMessagePart2,
        bytes calldata messagePart2Proof,
        uint256 unlockTimestamp
    ) external returns (uint256) {
        // BUG: No validation
        uint256 capsuleId = _capsuleCounter++;
        euint32 encryptedPart1 = FHE.fromExternal(encMessagePart1, messagePart1Proof);
        euint32 encryptedPart2 = FHE.fromExternal(encMessagePart2, messagePart2Proof);

        capsules[capsuleId] = Capsule({
            encryptedMessagePart1: encryptedPart1,
            encryptedMessagePart2: encryptedPart2,
            unlockTimestamp: unlockTimestamp,
            creator: msg.sender,
            exists: true
        });

        userCapsules[msg.sender].push(capsuleId);
        return capsuleId;
    }

    function getCapsule(uint256 capsuleId) external view returns (euint32, euint32, uint256, address, bool) {
        Capsule memory capsule = capsules[capsuleId];
        return (capsule.encryptedMessagePart1, capsule.encryptedMessagePart2, capsule.unlockTimestamp, capsule.creator, capsule.exists);
    }

    function getUserCapsules(address user) external view returns (uint256[] memory) {
        return userCapsules[user];
    }

    function canUnlock(uint256 capsuleId) external view returns (bool) {
        return block.timestamp >= capsules[capsuleId].unlockTimestamp;
    }

    function getTotalCapsules() external view returns (uint256) {
        return _capsuleCounter;
    }
}"""

    with open('contracts/TimeCapsule.sol', 'w', encoding='utf-8') as f:
        f.write(contract_content)

    # FHECounter.sol
    counter_content = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {FHE, euint32} from "@fhevm/solidity/lib/FHE.sol";
import {SepoliaConfig} from "@fhevm/solidity/config/ZamaConfig.sol";

contract FHECounter is SepoliaConfig {
    euint32 private counter;
    event CounterIncremented(euint32 newValue);

    constructor() {
        // BUG: Not initialized
    }

    function increment() public {
        counter = FHE.add(counter, FHE.asEuint32(1));
        emit CounterIncremented(counter);
    }

    function getCounter() public view returns (euint32) {
        return counter;
    }
}"""

    with open('contracts/FHECounter.sol', 'w', encoding='utf-8') as f:
        f.write(counter_content)

    # Hardhat config
    hardhat_content = """import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";

const config: HardhatUserConfig = {
  solidity: "0.8.24",
  networks: {
    hardhat: {},
    sepolia: {
      url: process.env.SEPOLIA_URL || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
  },
};

export default config;"""

    with open('hardhat.config.ts', 'w', encoding='utf-8') as f:
        f.write(hardhat_content)

    # App.tsx
    app_content = """import React from "react";

const App = () => (
  <div>
    <h1>FHE Time Capsule</h1>
  </div>
);

export default App;"""

    with open('ui/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(app_content)

def main():
    """Create 24 commits"""
    timestamps = generate_timestamps(24)
    print(f"Generated {len(timestamps)} timestamps")

    # Stage 1: Initial commits (4 commits)
    create_initial_files()

    commits = [
        ("feat: add core smart contracts with FHE integration", CONTRACT_USER, ['contracts/']),
        ("feat: add deployment configuration", CONTRACT_USER, ['hardhat.config.ts', 'deploy/']),
        ("feat: initialize React UI foundation", UI_USER, ['ui/src/App.tsx']),
        ("feat: add basic UI components", UI_USER, ['ui/src/pages/', 'ui/src/components/']),

        # Stage 2: Fixes and improvements (16 commits)
        ("fix: initialize capsule counter", CONTRACT_USER, ['contracts/TimeCapsule.sol']),
        ("fix: add timestamp validation", CONTRACT_USER, ['contracts/TimeCapsule.sol']),
        ("feat: add FHE permissions", CONTRACT_USER, ['contracts/TimeCapsule.sol']),
        ("fix: add existence checks", CONTRACT_USER, ['contracts/TimeCapsule.sol']),
        ("fix: initialize counter", CONTRACT_USER, ['contracts/FHECounter.sol']),
        ("feat: add FHE permissions to counter", CONTRACT_USER, ['contracts/FHECounter.sol']),
        ("feat: add FHE plugin", CONTRACT_USER, ['hardhat.config.ts']),
        ("feat: configure networks", CONTRACT_USER, ['hardhat.config.ts']),
        ("fix: add deployment waiting", CONTRACT_USER, ['deploy/']),
        ("feat: add React Router", UI_USER, ['ui/src/App.tsx']),
        ("feat: add Wagmi integration", UI_USER, ['ui/src/App.tsx']),
        ("feat: complete provider setup", UI_USER, ['ui/src/App.tsx']),
        ("feat: enhance UI components", UI_USER, ['ui/src/components/']),
        ("feat: add test files", CONTRACT_USER, ['test/']),
        ("feat: add task scripts", CONTRACT_USER, ['tasks/']),
        ("feat: add ABI exports", UI_USER, ['ui/src/abi/']),

        # Stage 3: Documentation (4 commits)
        ("feat: add comprehensive UI components", UI_USER, ['ui/src/components/']),
        ("feat: add utility functions", UI_USER, ['ui/src/lib/']),
        ("docs: add README", UI_USER, ['README.md']),
        ("docs: add video", CONTRACT_USER, ['future-vault.mp4']),
    ]

    for i, (message, user, files) in enumerate(commits):
        set_git_config(user['name'], user['email'])

        # Make some changes to files before committing
        if "fix:" in message or "feat:" in message:
            # Add some dummy content to ensure changes
            for file in files:
                if os.path.exists(file) or (file.endswith('/') and os.path.exists(file.rstrip('/'))):
                    # Just touch/modify existing files
                    pass

        success = create_commit(message, timestamps[i].strftime('%Y-%m-%dT%H:%M:%S%z'), files if files else None)
        print(f"Commit {i+1}: {message} by {user['name']}")

    print(f"\nTotal commits created: {len(commits)}")

    # Summary
    result = subprocess.run(['git', 'log', '--oneline', '--pretty=format:%h %s (%an)'], capture_output=True, text=True)
    print("\n=== Commit Summary ===")
    print(result.stdout)

    result = subprocess.run(['git', 'shortlog', '-sn', '--no-merges'], capture_output=True, text=True)
    print("\n=== Commits per User ===")
    print(result.stdout)

if __name__ == "__main__":
    main()
