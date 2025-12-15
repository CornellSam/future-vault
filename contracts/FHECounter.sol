// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

contract FHECounter {
    uint64 private counter;

    constructor() {
        counter = 0;
    }

    function increment() public {
        counter += 1;
    }

    function getCounter() public view returns (uint64) {
        return counter;
    }
}
