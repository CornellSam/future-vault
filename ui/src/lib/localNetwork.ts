// 本地 Hardhat 网络配置
export const LOCAL_NETWORK_CONFIG = {
  chainId: 31337,
  chainName: "Hardhat Local",
  rpcUrl: "http://127.0.0.1:8545",
  nativeCurrency: {
    name: "Ether",
    symbol: "ETH",
    decimals: 18,
  },
};

// 合约地址（从 hardhat node 输出获取）
export const CONTRACTS = {
  TimeCapsule: "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
  FHECounter: "0x5FbDB2315678afecb367f032d93F642f64180aa3",
};

// 测试账户（来自 hardhat node）
export const TEST_ACCOUNTS = [
  {
    address: "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266",
    privateKey: "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80",
  },
  {
    address: "0x70997970C51812dc3A010C7d01b50e0d17dc79C8",
    privateKey: "0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d",
  },
];
