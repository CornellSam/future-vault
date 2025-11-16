// Optimized struct packing for gas savings
    struct Capsule {
        uint256 unlockTimestamp;
        address creator;
        bool exists;
        euint32 encryptedMessagePart1;
        euint32 encryptedMessagePart2;
    }