// SPDX-License-Identifier: MIT
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
}