import { getDefaultConfig } from "@rainbow-me/rainbowkit";
import { QueryClient } from "@tanstack/react-query";
import { defineChain } from "viem";
import {
  mainnet,
  polygon,
  optimism,
  arbitrum,
  base,
  sepolia,
} from "wagmi/chains";

export const queryClient = new QueryClient();

// 本地 Hardhat 网络配置
const hardhat = defineChain({
  id: 31337,
  name: "Hardhat",
  nativeCurrency: { name: "Ether", symbol: "ETH", decimals: 18 },
  rpcUrls: {
    default: { http: ["http://127.0.0.1:8545"] },
  },
  blockExplorers: {
    default: { name: "Hardhat", url: "http://localhost:8545" },
  },
});

export const wagmiConfig = getDefaultConfig({
  appName: "Future Vault",
  projectId: "YOUR_WALLETCONNECT_PROJECT_ID",
  chains: [hardhat, sepolia, mainnet, polygon, optimism, arbitrum, base],
  ssr: false,
});
