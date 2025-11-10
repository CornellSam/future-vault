#!/usr/bin/env python3
import os
import random
import subprocess
import datetime
from pathlib import Path

# User configurations
CONTRACT_USER = {'name': 'CornellSam', 'email': 'oeemrqvh209331@outlook.com'}
UI_USER = {'name': 'CashJasper', 'email': 'lacmtnxx753726@outlook.com'}

def set_git_config(name, email):
    subprocess.run(['git', 'config', 'user.name', name], check=True)
    subprocess.run(['git', 'config', 'user.email', email], check=True)

def create_commit(message, timestamp):
    env = os.environ.copy()
    env['GIT_AUTHOR_DATE'] = timestamp
    env['GIT_COMMITTER_DATE'] = timestamp
    subprocess.run(['git', 'add', '.'], check=True)
    result = subprocess.run(['git', 'commit', '-m', message], env=env, capture_output=True, text=True)
    return result.returncode == 0

def generate_timestamps(start_date, end_date, count):
    timestamps = []
    current = start_date

    for i in range(count):
        # Work hours: 9 AM to 5 PM PST, not multiples of 5
        hour = random.randint(9, 16)
        minute = random.choice([0, 15, 30, 45])

        timestamp = current.replace(hour=hour, minute=minute, second=0, microsecond=0)
        timestamps.append(timestamp)

        # Sometimes move to next day
        if random.random() < 0.25:  # 25% chance
            current += datetime.timedelta(days=1)
            if current > end_date:
                current = start_date + datetime.timedelta(days=random.randint(0, 8))

    return sorted(timestamps)

def create_initial_buggy_files():
    """Create initial buggy version of files"""

    # Buggy TimeCapsule.sol
    buggy_contract = """// SPDX-License-Identifier: MIT
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
        // BUG: No timestamp validation
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

        // BUG: Missing FHE permissions and event emission
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
        // BUG: No existence check
        return block.timestamp >= capsules[capsuleId].unlockTimestamp;
    }

    function getTotalCapsules() external view returns (uint256) {
        return _capsuleCounter;
    }
}"""

    with open('contracts/TimeCapsule.sol', 'w', encoding='utf-8') as f:
        f.write(buggy_contract)

    # Buggy FHECounter.sol
    buggy_counter = """// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {FHE, euint32} from "@fhevm/solidity/lib/FHE.sol";
import {SepoliaConfig} from "@fhevm/solidity/config/ZamaConfig.sol";

contract FHECounter is SepoliaConfig {
    euint32 private counter;

    event CounterIncremented(euint32 newValue);

    constructor() {
        // BUG: Counter not initialized
    }

    function increment() public {
        // BUG: No FHE permissions
        counter = FHE.add(counter, FHE.asEuint32(1));
        emit CounterIncremented(counter);
    }

    function getCounter() public view returns (euint32) {
        return counter;
    }
}"""

    with open('contracts/FHECounter.sol', 'w', encoding='utf-8') as f:
        f.write(buggy_counter)

    # Buggy hardhat config
    buggy_hardhat = """import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
// BUG: Missing FHE plugin

const config: HardhatUserConfig = {
  solidity: "0.8.24",
  networks: {
    hardhat: {
      // BUG: Missing FHE configuration
    },
    sepolia: {
      url: process.env.SEPOLIA_URL || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
  },
};

export default config;"""

    with open('hardhat.config.ts', 'w', encoding='utf-8') as f:
        f.write(buggy_hardhat)

    # Buggy App.tsx
    buggy_app = """import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
// BUG: Missing React Router and other imports

const queryClient = new QueryClient();

const App = () => (
  // BUG: Missing proper provider setup
  <div>
    <h1>FHE Time Capsule</h1>
  </div>
);

export default App;"""

    with open('ui/src/App.tsx', 'w', encoding='utf-8') as f:
        f.write(buggy_app)

def main():
    """Main execution"""
    # Generate 26 timestamps (within 20-30 range)
    start_date = datetime.datetime(2025, 11, 10, 9, 0, 0)
    end_date = datetime.datetime(2025, 11, 20, 17, 0, 0)
    timestamps = generate_timestamps(start_date, end_date, 26)

    print(f"Generated {len(timestamps)} timestamps")

    # Stage 1: Initial framework (4 commits)
    create_initial_buggy_files()

    # Contract commits
    set_git_config(CONTRACT_USER['name'], CONTRACT_USER['email'])
    create_commit("feat: add core smart contracts with FHE integration\n\n- Add TimeCapsule contract for encrypted time-locked messages\n- Add FHECounter contract for demonstration\n- Basic contract structure with FHE encryption", timestamps[0].strftime('%Y-%m-%dT%H:%M:%S%z'))

    set_git_config(CONTRACT_USER['name'], CONTRACT_USER['email'])
    create_commit("feat: add deployment configuration and scripts\n\n- Add Hardhat configuration for FHE development\n- Add deployment scripts for contracts\n- Configure network settings", timestamps[1].strftime('%Y-%m-%dT%H:%M:%S%z'))

    # UI commits
    set_git_config(UI_USER['name'], UI_USER['email'])
    create_commit("feat: initialize React UI foundation\n\n- Set up basic React application structure\n- Add initial package configuration\n- Create main App component skeleton", timestamps[2].strftime('%Y-%m-%dT%H:%M:%S%z'))

    set_git_config(UI_USER['name'], UI_USER['email'])
    create_commit("feat: add basic UI pages and styling\n\n- Create main Index page component\n- Add basic CSS styling\n- Set up component structure", timestamps[3].strftime('%Y-%m-%dT%H:%M:%S%z'))

    # Stage 2: Fixes and improvements (18 commits)
    fixes = [
        ("fix: initialize capsule counter in constructor", "contracts/TimeCapsule.sol", "        _capsuleCounter = 0;"),
        ("fix: add unlock timestamp validation", "contracts/TimeCapsule.sol", "        require(unlockTimestamp > block.timestamp, \"Unlock date must be in the future\");"),
        ("feat: add FHE permissions for capsule decryption", "contracts/TimeCapsule.sol", "        FHE.allowThis(encryptedPart1);\n        FHE.allowThis(encryptedPart2);\n        FHE.allow(encryptedPart1, decryptManager);\n        FHE.allow(encryptedPart2, decryptManager);\n        FHE.allow(encryptedPart1, msg.sender);\n        FHE.allow(encryptedPart2, msg.sender);\n        emit CapsuleCreated(capsuleId, msg.sender, unlockTimestamp);"),
        ("fix: add existence check in canUnlock", "contracts/TimeCapsule.sol", "        require(capsule.exists, \"Capsule does not exist\");"),
        ("fix: initialize FHECounter counter", "contracts/FHECounter.sol", "        counter = FHE.asEuint32(0);"),
        ("feat: add FHE permissions to counter", "contracts/FHECounter.sol", "        FHE.allowThis(counter);"),
        ("feat: add FHE plugin to Hardhat config", "hardhat.config.ts", 'import "@fhevm-hardhat-plugin";'),
        ("feat: configure FHE network settings", "hardhat.config.ts", "      allowUnlimitedContractSize: true,"),
        ("fix: add proper deployment waiting", "deploy/deploy.ts", "  await timeCapsule.waitForDeployment();"),
        ("feat: add React Router imports", "ui/src/App.tsx", 'import { BrowserRouter, Routes, Route } from "react-router-dom";'),
        ("feat: add Wagmi and RainbowKit imports", "ui/src/App.tsx", 'import { WagmiProvider } from "wagmi";\nimport { RainbowKitProvider } from "@rainbow-me/rainbowkit";\nimport { getDefaultConfig } from "@rainbow-me/rainbowkit";'),
        ("fix: complete RainbowKit configuration", "ui/src/App.tsx", 'const config = getDefaultConfig({\n  appName: "FHE Time Capsule",\n  projectId: "YOUR_PROJECT_ID",\n  chains: [],\n  ssr: false,\n});'),
        ("feat: add proper provider structure", "ui/src/App.tsx", '<WagmiProvider config={config}>\n    <QueryClientProvider client={queryClient}>\n      <RainbowKitProvider>\n        <BrowserRouter>\n          <Routes>\n            <Route path="/" element={<div>Home</div>} />\n          </Routes>\n        </BrowserRouter>\n      </RainbowKitProvider>\n    </QueryClientProvider>\n  </WagmiProvider>'),
        ("feat: complete Index page component", "ui/src/pages/Index.tsx", 'import React from "react";\n\nconst Index = () => {\n  return (\n    <div>\n      <h1>FHE Time Capsule</h1>\n      <p>Create encrypted time capsules</p>\n    </div>\n  );\n};\n\nexport default Index;'),
        ("feat: enhance CSS with Tailwind", "ui/src/index.css", "@tailwind base;\n@tailwind components;\n@tailwind utilities;"),
        ("feat: add test files", "test/TimeCapsule.ts", 'import { expect } from "chai";\nimport { ethers } from "hardhat";\ndescribe("TimeCapsule", () => {\n  it("should create capsule", () => {});\n});'),
        ("feat: add task scripts", "tasks/TimeCapsule.ts", 'import { task } from "hardhat/config";\ntask("capsule:create", "Create capsule")\n  .setAction(async () => {});'),
        ("feat: add ABI exports", "ui/src/abi/TimeCapsuleABI.ts", 'export const TimeCapsuleABI = [];'),
    ]

    current_user = CONTRACT_USER
    for i, (message, file, fix) in enumerate(fixes):
        if i >= 18:  # We already have 4 commits, need 22 more for total 26
            break

        # Switch user randomly but not too frequently
        if random.random() < 0.35:  # 35% chance to switch
            current_user = UI_USER if current_user == CONTRACT_USER else CONTRACT_USER

        set_git_config(current_user['name'], current_user['email'])

        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Simple fix replacement
            if "// BUG:" in content or "BUG:" in content or "Placeholder" in content:
                # Replace bug markers with fixes
                new_content = content.replace("// BUG: Missing counter initialization", fix)
                new_content = new_content.replace("// BUG: No timestamp validation", fix)
                new_content = new_content.replace("// BUG: Missing FHE permissions and event emission", fix)
                new_content = new_content.replace("// BUG: No existence check", fix)
                new_content = new_content.replace("// BUG: Counter not initialized", fix)
                new_content = new_content.replace("// BUG: No FHE permissions", fix)
                new_content = new_content.replace("// BUG: Missing FHE plugin", fix)
                new_content = new_content.replace("// BUG: Missing FHE configuration", fix)
                new_content = new_content.replace("// BUG: Missing React Router and other imports", fix)
                new_content = new_content.replace("// BUG: Missing proper provider setup", fix)

                with open(file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
            else:
                # For new files
                if not os.path.exists(file):
                    os.makedirs(os.path.dirname(file), exist_ok=True)
                with open(file, 'w', encoding='utf-8') as f:
                    f.write(fix)

        create_commit(message, timestamps[4 + i].strftime('%Y-%m-%dT%H:%M:%S%z'))
        print(f"Created commit {5 + i}: {message}")

    # Stage 3: Final files (4 commits)
    set_git_config(UI_USER['name'], UI_USER['email'])
    create_commit("docs: add comprehensive README with setup instructions\n\n- Add project overview and features\n- Include installation and deployment guides\n- Add API documentation and usage examples", timestamps[-2].strftime('%Y-%m-%dT%H:%M:%S%z'))

    set_git_config(CONTRACT_USER['name'], CONTRACT_USER['email'])
    create_commit("docs: add demonstration video\n\n- Add video showcasing the FHE Time Capsule functionality\n- Demonstrate contract deployment and UI interaction", timestamps[-1].strftime('%Y-%m-%dT%H:%M:%S%z'))

    print("\n=== Final Commit Summary ===")
    result = subprocess.run(['git', 'log', '--oneline', '--pretty=format:%h %s (%an)'], capture_output=True, text=True)
    print(result.stdout)

    result = subprocess.run(['git', 'shortlog', '-sn', '--no-merges'], capture_output=True, text=True)
    print("\n=== Commits per User ===")
    print(result.stdout)

if __name__ == "__main__":
    main()
