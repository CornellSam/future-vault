require(unlockTimestamp > block.timestamp + 1 hours, "Unlock time must be at least 1 hour in future");
        require(encMessagePart1.length > 0, "Message part 1 cannot be empty");