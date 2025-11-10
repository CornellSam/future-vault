// SPDX-License-Identifier: MIT
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
                _capsuleCounter = 0;
    }

    function createCapsule(
        externalEuint32 encMessagePart1,
        bytes calldata messagePart1Proof,
        externalEuint32 encMessagePart2,
        bytes calldata messagePart2Proof,
        uint256 unlockTimestamp
    ) external returns (uint256) {
                _capsuleCounter = 0;
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

                _capsuleCounter = 0;
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
                _capsuleCounter = 0;
        return block.timestamp >= capsules[capsuleId].unlockTimestamp;
    }

    function getTotalCapsules() external view returns (uint256) {
        return _capsuleCounter;
    }
}