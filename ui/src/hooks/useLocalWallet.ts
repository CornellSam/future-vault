import { useState, useCallback } from "react";
import { BrowserProvider, JsonRpcProvider } from "ethers";
import { LOCAL_NETWORK_CONFIG, TEST_ACCOUNTS } from "../lib/localNetwork";

export function useLocalWallet() {
  const [address, setAddress] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const connectToLocalNetwork = useCallback(async () => {
    setLoading(true);
    setError(null);

    try {
      // 检查是否有 MetaMask
      if (!(window as any).ethereum) {
        throw new Error("Please install MetaMask");
      }

      // 添加本地网络到 MetaMask
      await (window as any).ethereum.request({
        method: "wallet_addEthereumChain",
        params: [
          {
            chainId: `0x${LOCAL_NETWORK_CONFIG.chainId.toString(16)}`,
            chainName: LOCAL_NETWORK_CONFIG.chainName,
            rpcUrls: [LOCAL_NETWORK_CONFIG.rpcUrl],
            nativeCurrency: LOCAL_NETWORK_CONFIG.nativeCurrency,
          },
        ],
      });

      // 切换到本地网络
      await (window as any).ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: `0x${LOCAL_NETWORK_CONFIG.chainId.toString(16)}` }],
      });

      // 请求账户
      const accounts = await (window as any).ethereum.request({
        method: "eth_requestAccounts",
      });

      if (accounts.length > 0) {
        setAddress(accounts[0]);
        setIsConnected(true);
      }
    } catch (err: any) {
      setError(err.message);
      console.error("Failed to connect to local network:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  const importTestAccount = useCallback(async (accountIndex: number = 0) => {
    if (accountIndex >= TEST_ACCOUNTS.length) {
      setError("Invalid account index");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      if (!(window as any).ethereum) {
        throw new Error("Please install MetaMask");
      }

      const account = TEST_ACCOUNTS[accountIndex];

      // 导入私钥
      await (window as any).ethereum.request({
        method: "eth_importRawKey",
        params: [account.privateKey, "password"],
      });

      setAddress(account.address);
      setIsConnected(true);
    } catch (err: any) {
      // eth_importRawKey 可能不被支持，这是正常的
      console.log("Note: Direct key import not supported, use MetaMask UI instead");
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  const disconnect = useCallback(() => {
    setAddress(null);
    setIsConnected(false);
  }, []);

  return {
    address,
    isConnected,
    loading,
    error,
    connectToLocalNetwork,
    importTestAccount,
    disconnect,
    testAccounts: TEST_ACCOUNTS,
  };
}
