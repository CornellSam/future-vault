// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {FHE, euint32} from "@fhevm/solidity/lib/FHE.sol";
import {SepoliaConfig} from "@fhevm/solidity/config/ZamaConfig.sol";

contract FHECounter is SepoliaConfig {
    euint32 private counter;

    event CounterIncremented(euint32 newValue);

    constructor() {
                counter = FHE.asEuint32(0);
    }

    function increment() public {
                counter = FHE.asEuint32(0);
        counter = FHE.add(counter, FHE.asEuint32(1));
        emit CounterIncremented(counter);
    }

    function getCounter() public view returns (euint32) {
        return counter;
    }
}