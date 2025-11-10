import { useAccount } from "wagmi";
export const useWallet = () => {
  const { address, isConnected } = useAccount();
  return { address, isConnected };
};