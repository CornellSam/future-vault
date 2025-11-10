import { HardhatUserConfig } from "hardhat/config";
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

export default config;