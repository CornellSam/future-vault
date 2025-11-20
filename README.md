# Future Vault - Time Capsule with FHEVM Encryption

[![Live Demo](https://img.shields.io/badge/Live%20Demo-View%20App-blue?style=for-the-badge)](https://fadet-box-3afw.vercel.app/)
[![Demo Video](https://img.shields.io/badge/Demo%20Video-Watch%20Now-red?style=for-the-badge)](https://github.com/CornellSam/future-vault/blob/main/future-vault.mp4)

A revolutionary time capsule dApp built on FHEVM (Fully Homomorphic Encryption Virtual Machine) that allows users to create encrypted messages that can only be decrypted after a specified future date. Leveraging Zama's groundbreaking FHE technology, Future Vault ensures that your messages remain completely private until their designated unlock time.

## ✨ Features

- 🔐 **End-to-End Encryption**: Messages are encrypted using FHEVM before being stored on-chain
- ⏰ **Time-Locked Decryption**: Messages can only be decrypted after the specified unlock date
- 🛡️ **Privacy-First**: Even the blockchain cannot read your encrypted messages
- 🌐 **Cross-Chain Support**: Works on both local Hardhat network and Sepolia testnet
- 🎨 **Beautiful UI**: Modern React interface with smooth animations
- 📱 **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Live Demo

Experience Future Vault in action: **[https://fadet-box-3afw.vercel.app/](https://fadet-box-3afw.vercel.app/)**

Connect your wallet and try creating your own encrypted time capsule!

## 📹 Demo Video

Watch a complete walkthrough: **[https://github.com/CornellSam/future-vault/blob/main/future-vault.mp4](https://github.com/CornellSam/future-vault/blob/main/future-vault.mp4)**

## 🏗️ Architecture

### Smart Contracts

#### TimeCapsule.sol

The core smart contract that manages encrypted time capsules:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {FHE, euint32, externalEuint32} from "@fhevm/solidity/lib/FHE.sol";
import {SepoliaConfig} from "@fhevm/solidity/config/ZamaConfig.sol";

contract TimeCapsule is SepoliaConfig {
    address public immutable decryptManager;

    struct Capsule {
        euint32 encryptedMessagePart1;  // Encrypted first part of the message (4 bytes)
        euint32 encryptedMessagePart2;  // Encrypted second part of the message (4 bytes, optional)
        uint256 unlockTimestamp;        // Unix timestamp when capsule can be unlocked
        address creator;                // Address of the capsule creator
        bool exists;                    // Whether the capsule exists
    }

    mapping(uint256 => Capsule) public capsules;
    mapping(address => uint256[]) public userCapsules;
    uint256 private _capsuleCounter;

    event CapsuleCreated(
        uint256 indexed capsuleId,
        address indexed creator,
        uint256 unlockTimestamp
    );

    event CapsuleUnlocked(uint256 indexed capsuleId, address indexed creator);

    constructor(address manager) {
        decryptManager = manager;
        _capsuleCounter = 0;
    }

    function createCapsule(
        externalEuint32 encMessagePart1,
        bytes calldata messagePart1Proof,
        externalEuint32 encMessagePart2,
        bytes calldata messagePart2Proof,
        uint256 unlockTimestamp
    ) external returns (uint256);

    function getCapsule(uint256 capsuleId)
        external
        view
        returns (
            euint32 encryptedMessagePart1,
            euint32 encryptedMessagePart2,
            uint256 unlockTimestamp,
            address creator,
            bool exists
        );

    function getUserCapsules(address user) external view returns (uint256[] memory);

    function canUnlock(uint256 capsuleId) external view returns (bool);

    function getTotalCapsules() external view returns (uint256);
}
```

**Key Functions:**

- `createCapsule()`: Creates a new encrypted time capsule with two encrypted message parts, validates unlock timestamp, and sets up decryption permissions
- `getCapsule()`: Retrieves capsule metadata including encrypted data handles (encrypted data remains private)
- `canUnlock()`: Checks if a capsule can be decrypted (current time >= unlockTimestamp)
- `getUserCapsules()`: Returns all capsule IDs owned by a user
- `getTotalCapsules()`: Returns the total number of capsules created

**Security Features:**
- Uses `externalEuint32` and proof verification for encrypted inputs
- Grants decryption permissions to creator and optional decryptManager
- Validates unlock timestamp must be in the future
- Stores encrypted data as `euint32` handles that cannot be read without decryption

### Encryption & Decryption Flow

#### Message Encoding Process

1. **Input Processing**: User enters a text message (up to 8 characters)
2. **UTF-8 Encoding**: Message is converted to UTF-8 bytes using `ethers.toUtf8Bytes()`
3. **Data Splitting**: Message is split into two 4-byte parts
4. **Numeric Conversion**: Each 4-byte chunk is converted to a uint32 number using bit shifting

```typescript
// Example: "Hello" → [72, 101, 108, 108, 111]
// Part 1: [72, 101, 108, 108] → 1819043144 (uint32)
// Part 2: [111, 0, 0, 0] → 111 (uint32, padded with zeros)

const messageBytes = ethers.toUtf8Bytes(message);

// Encode first 4 bytes as uint32 (Part 1)
let messageNum1 = 0;
for (let i = 0; i < Math.min(4, messageBytes.length); i++) {
    messageNum1 = (messageNum1 << 8) | messageBytes[i];
}

// Encode next 4 bytes as uint32 (Part 2)
let messageNum2 = 0;
for (let i = 4; i < Math.min(8, messageBytes.length); i++) {
    messageNum2 = (messageNum2 << 8) | messageBytes[i];
}
```

#### FHEVM Encryption

1. **FHEVM Initialization**: Initialize FHEVM instance based on network (local or Sepolia)
2. **FHE Encryption**: Each uint32 number is encrypted using FHEVM's `createEncryptedInput()`
3. **Handle Generation**: Encrypted values are represented as bytes32 handles
4. **Proof Creation**: Zero-knowledge input proofs are generated for verification
5. **On-Chain Storage**: Encrypted handles and proofs are stored in the smart contract

```typescript
// Encryption using FHEVM
const encrypted1 = await fhe.encrypt(contractAddress, address, messageNum1);
const encrypted2 = await fhe.encrypt(contractAddress, address, messageNum2);

// Under the hood (from fhevm.ts):
const encryptedInput = fhevm
    .createEncryptedInput(contractAddress, userAddress)
    .add32(messageHash);

const encrypted = await encryptedInput.encrypt();

// Returns handles and inputProof
const handles = encrypted.handles.map(handle => ethers.hexlify(handle));
const inputProof = ethers.hexlify(encrypted.inputProof);
```

**Network-Specific Implementation:**
- **Local Network (31337)**: Uses `@fhevm/mock-utils` with Hardhat plugin for testing
- **Sepolia (11155111)**: Uses `@zama-fhe/relayer-sdk` with real FHE operations

#### Decryption Process

1. **Time Validation**: Check if current time >= unlockTimestamp
2. **Permission Check**: Verify user has decryption permissions (creator or decryptManager)
3. **FHE Decryption**: Encrypted handles are decrypted back to uint32 numbers
4. **Data Reconstruction**: uint32 numbers are converted back to bytes
5. **UTF-8 Decoding**: Bytes are converted back to the original text message

```typescript
// Decryption using FHEVM
const decryptedNum1 = await fhe.decrypt(
    capsule.encryptedMessagePart1,
    contractAddress,
    address,
    chainId
);

const decryptedNum2 = await fhe.decrypt(
    capsule.encryptedMessagePart2,
    contractAddress,
    address,
    chainId
);

// Decode numbers back to message text
const decodeNumber = (num: number): string => {
    const bytes: number[] = [];
    let n = num;
    
    // Extract bytes from the number (big-endian)
    for (let i = 0; i < 4; i++) {
        bytes.unshift(n & 0xFF);
        n = n >>> 8;
    }
    
    // Convert bytes to string, filtering out null bytes (padding)
    return bytes
        .filter(b => b !== 0)
        .map(b => String.fromCharCode(b))
        .join('');
};

const messagePart1 = decodeNumber(decryptedNum1);
const messagePart2 = decodeNumber(decryptedNum2);
const decryptedMessage = messagePart1 + messagePart2;
```

**Network-Specific Decryption:**
- **Local Network**: Uses `userDecryptHandleBytes32` from `@fhevm/mock-utils`
- **Sepolia**: Uses `userDecrypt()` with EIP712 signature for authorization

## 🔧 Quick Start

### Prerequisites

- **Node.js**: Version 20 or higher
- **npm**: Version 9.x or higher
- **MetaMask** or **Rainbow Wallet** browser extension
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/CornellSam/future-vault.git
   cd future-vault
   ```

2. **Install dependencies**
   ```bash
   npm install
   cd ui && npm install && cd ..
   ```

3. **Set up environment variables**
   ```bash
   npx hardhat vars set MNEMONIC
   npx hardhat vars set INFURA_API_KEY
   npx hardhat vars set ETHERSCAN_API_KEY  # Optional, for contract verification
   ```

### Local Development

1. **Start Hardhat Node**
   ```bash
   npx hardhat node
   ```

2. **Deploy Contract**
   ```bash
   npx hardhat deploy --tags TimeCapsule --network localhost
   ```

3. **Update Contract Address** (if different from default)
   - Check deployment output for contract address
   - Update `ui/src/abi/TimeCapsuleAddresses.ts` if necessary

4. **Start Frontend**
   ```bash
   cd ui && npm run dev
   ```

5. **Open Browser**
   - Visit `http://localhost:8080`
   - Connect your wallet
   - Create your first encrypted time capsule!

### Sepolia Testnet Deployment

1. **Deploy to Sepolia**
   ```bash
   npx hardhat deploy --tags TimeCapsule --network sepolia
   ```

2. **Update Contract Address**
   - Update `ui/src/abi/TimeCapsuleAddresses.ts` with the deployed address

3. **Verify Contract** (optional)
   ```bash
   npx hardhat verify --network sepolia <CONTRACT_ADDRESS> <DECRYPT_MANAGER_ADDRESS>
   ```

4. **Build and Deploy Frontend**
   ```bash
   cd ui && npm run build
   ```

## 📁 Project Structure

```
future-vault/
├── contracts/
│   ├── TimeCapsule.sol          # Main time capsule contract with FHE
│   └── FHECounter.sol           # Example FHE counter (reference)
├── deploy/
│   └── deploy_timecapsule.ts    # Contract deployment script
├── test/
│   ├── TimeCapsule.ts           # Local network tests
│   └── TimeCapsuleSepolia.ts    # Sepolia network tests
├── tasks/
│   └── TimeCapsule.ts           # CLI interaction tasks
├── ui/                          # React frontend application
│   ├── src/
│   │   ├── components/
│   │   │   ├── CreateCapsule.tsx    # Capsule creation interface
│   │   │   ├── CapsuleVault.tsx     # Capsule management interface
│   │   │   ├── Hero.tsx            # Landing page hero section
│   │   │   └── ...                  # Additional UI components
│   │   ├── hooks/
│   │   │   └── useFhevm.ts         # FHEVM integration hook
│   │   ├── lib/
│   │   │   └── fhevm.ts           # FHEVM encryption/decryption utilities
│   │   └── abi/
│   │       ├── TimeCapsuleABI.ts       # Contract ABI
│   │       └── TimeCapsuleAddresses.ts # Contract addresses
│   └── package.json
├── hardhat.config.ts           # Hardhat configuration
├── package.json                # Root package configuration
└── README.md                   # This file
```

## 🔒 Security Features

- **Fully Homomorphic Encryption**: Messages are encrypted on the client-side using FHEVM before being sent to the blockchain
- **Time-Locked Access**: Cryptographic guarantees that messages cannot be decrypted before the unlock time
- **Permission-Based Decryption**: Only capsule creators and authorized decryptManager can decrypt messages
- **Zero-Knowledge Proofs**: All encrypted inputs are verified with zero-knowledge proofs without revealing sensitive data
- **On-Chain Privacy**: Encrypted data stored as `euint32` handles cannot be read by anyone without proper decryption permissions

## 🧪 Testing

### Local Tests
```bash
npm run test
```

### Sepolia Tests
```bash
npm run test:sepolia
```

### Coverage Report
```bash
npm run coverage
```

## 📚 Documentation

- [FHEVM Documentation](https://docs.zama.ai/fhevm)
- [FHEVM Hardhat Plugin](https://docs.zama.ai/protocol/solidity-guides/development-guide/hardhat)
- [Zama Developer Portal](https://docs.zama.ai)

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

This project is licensed under the BSD-3-Clause-Clear License. See the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/CornellSam/future-vault/issues)
- **Documentation**: [FHEVM Docs](https://docs.zama.ai)
- **Community**: [Zama Discord](https://discord.gg/zama)

---

**Built with ❤️ using Zama's FHEVM technology**
