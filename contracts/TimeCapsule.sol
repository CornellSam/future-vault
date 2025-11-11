        FHE.allowThis(encryptedPart1);
        FHE.allowThis(encryptedPart2);
        FHE.allow(encryptedPart1, decryptManager);
        FHE.allow(encryptedPart2, decryptManager);
        FHE.allow(encryptedPart1, msg.sender);
        FHE.allow(encryptedPart2, msg.sender);
        emit CapsuleCreated(capsuleId, msg.sender, unlockTimestamp);