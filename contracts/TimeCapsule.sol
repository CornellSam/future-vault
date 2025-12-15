// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract TimeCapsule {
    struct Capsule {
        address creator;
        uint256 unlockTime;
        bytes encryptedContent;
        bool isRevealed;
    }

    uint256 public capsuleCount;
    mapping(uint256 => Capsule) public capsules;
    mapping(uint256 => string) public capsuleTitles;
    mapping(uint256 => string) public capsuleDescriptions;

    event CapsuleCreated(uint256 indexed capsuleId, address indexed creator, uint256 unlockTime);
    event CapsuleRevealed(uint256 indexed capsuleId);

    function createCapsule(
        string memory title,
        string memory description,
        bytes memory content,
        uint256 unlockTime
    ) public returns (uint256) {
        require(unlockTime > block.timestamp, "Unlock time must be in the future");

        uint256 capsuleId = capsuleCount++;

        capsules[capsuleId] = Capsule({
            creator: msg.sender,
            unlockTime: unlockTime,
            encryptedContent: content,
            isRevealed: false
        });

        capsuleTitles[capsuleId] = title;
        capsuleDescriptions[capsuleId] = description;

        emit CapsuleCreated(capsuleId, msg.sender, unlockTime);
        return capsuleId;
    }

    function revealCapsule(uint256 capsuleId) public {
        Capsule storage capsule = capsules[capsuleId];
        require(block.timestamp >= capsule.unlockTime, "Capsule is still locked");
        require(!capsule.isRevealed, "Capsule already revealed");

        capsule.isRevealed = true;
        emit CapsuleRevealed(capsuleId);
    }

    function getCapsule(uint256 capsuleId) public view returns (
        address creator,
        uint256 unlockTime,
        bool isRevealed,
        string memory title,
        string memory description
    ) {
        Capsule storage capsule = capsules[capsuleId];
        return (
            capsule.creator,
            capsule.unlockTime,
            capsule.isRevealed,
            capsuleTitles[capsuleId],
            capsuleDescriptions[capsuleId]
        );
    }

    function getEncryptedContent(uint256 capsuleId) public view returns (bytes memory) {
        return capsules[capsuleId].encryptedContent;
    }
}
