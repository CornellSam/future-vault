import { useState, useEffect, useCallback } from "react";
import { BrowserProvider } from "ethers";

export interface WalletState {
  address: string | null;
  isConnected: boolean;
  chainId: number | null;
  balance: string | null;
}

export function useWallet() {
  const [state, setState] = useState<WalletState>({
    address: null,
    isConnected: false,
    chainId: null,
    balance: null,
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const updateWalletState = useCallback(async () => {
    if (typeof window === "undefined" || !(window as any).ethereum) {
      return;
    }

    try {
      const provider = new BrowserProvider((window as any).ethereum);
      const accounts = await provider.listAccounts();
      
      if (accounts.length > 0) {
        const signer = accounts[0];
        const address = await signer.getAddress();
        const network = await provider.getNetwork();
        const balance = await provider.getBalance(address);
        
        setState({
          address,
          isConnected: true,
          chainId: Number(network.chainId),
          balance: (Number(balance) / 1e18).toFixed(4),
        });
      } else {
        setState({
          address: null,
          isConnected: false,
          chainId: null,
          balance: null,
        });
      }
    } catch (err: any) {
      setError(err.message);
    }
  }, []);

  const connect = useCallback(async () => {
    if (typeof window === "undefined" || !(window as any).ethereum) {
      setError("Please install MetaMask or another Web3 wallet");
      return;
    }

    setLoading(true);
    setError(null);

    try {
      await (window as any).ethereum.request({ method: "eth_requestAccounts" });
      await updateWalletState();
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [updateWalletState]);

  const disconnect = useCallback(() => {
    setState({
      address: null,
      isConnected: false,
      chainId: null,
      balance: null,
    });
  }, []);

  const switchNetwork = useCallback(async (chainId: number) => {
    if (!(window as any).ethereum) return;

    try {
      await (window as any).ethereum.request({
        method: "wallet_switchEthereumChain",
        params: [{ chainId: `0x${chainId.toString(16)}` }],
      });
    } catch (err: any) {
      setError(err.message);
    }
  }, []);

  useEffect(() => {
    updateWalletState();

    if ((window as any).ethereum) {
      (window as any).ethereum.on("accountsChanged", updateWalletState);
      (window as any).ethereum.on("chainChanged", updateWalletState);

      return () => {
        (window as any).ethereum.removeListener("accountsChanged", updateWalletState);
        (window as any).ethereum.removeListener("chainChanged", updateWalletState);
      };
    }
  }, [updateWalletState]);

  return {
    ...state,
    loading,
    error,
    connect,
    disconnect,
    switchNetwork,
  };
}
