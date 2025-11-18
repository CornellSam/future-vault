import { useState, useEffect, useCallback } from "react";
import { initializeFHEVM, encryptInput, resetFHEVMInstance, decryptEuint32 } from "../lib/fhevm";
import type { FhevmInstance } from "@zama-fhe/relayer-sdk/bundle";
import { BrowserProvider } from "ethers";

export function useFhevm(chainId?: number) {
  const [instance, setInstance] = useState<FhevmInstance | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  // Initialize FHEVM
  useEffect(() => {
    let mounted = true;

    const init = async () => {
      console.log("[useFhevm] Init called, chainId:", chainId);
      setLoading(true);
      
      if (!chainId) {
        console.log("[useFhevm] No chainId, skipping initialization");
        setLoading(false);
        return;
      }

      // Only support local network and Sepolia
      if (chainId !== 31337 && chainId !== 11155111) {
        const errorMsg = `Unsupported network (${chainId}). Please switch to local network (31337) or Sepolia (11155111).`;
        console.error("[useFhevm]", errorMsg);
        setError(new Error(errorMsg));
        setLoading(false);
        return;
      }

      try {
        setError(null);

        console.log("[useFhevm] Starting FHEVM initialization, chainId:", chainId);
        
        const fhevmInstance = await initializeFHEVM(chainId);

        if (mounted) {
          setInstance(fhevmInstance);
          setLoading(false);
          console.log("[useFhevm] ✅ FHEVM initialized successfully");
        }
      } catch (err: any) {
        console.error("[useFhevm] ❌ FHEVM initialization failed:", err);
        if (mounted) {
          setError(err);
          setLoading(false);
        }
      }
    };

    init();

    return () => {
      console.log("[useFhevm] Cleanup, chainId:", chainId);
      mounted = false;
    };
  }, [chainId]);

  // Reset instance on network change
  useEffect(() => {
    return () => {
      resetFHEVMInstance();
    };
  }, [chainId]);

  // Encryption function
  const encrypt = useCallback(
    async (contractAddress: string, userAddress: string, messageHash: number) => {
      if (!instance) {
        throw new Error("FHEVM instance not initialized");
      }
      return encryptInput(instance, contractAddress, userAddress, messageHash);
    },
    [instance]
  );

  // Decryption function
  const decrypt = useCallback(
    async (handle: string, contractAddress: string, userAddress: string, chainId?: number) => {
      if (!instance) {
        throw new Error("FHEVM instance not initialized");
      }
      
      if (!handle || handle === "0x" || handle.length !== 66) {
        throw new Error(`Invalid handle format: ${handle}`);
      }
      
      const provider = new BrowserProvider((window as any).ethereum);
      const signer = await provider.getSigner();
      
      // Use effective chainId (from hook parameter or current chain)
      const effectiveChainId = chainId || (await provider.getNetwork()).chainId;
      
      return decryptEuint32(instance, handle, contractAddress, userAddress, signer, Number(effectiveChainId));
    },
    [instance]
  );

  return {
    instance,
    loading,
    error,
    isReady: !!instance && !loading,
    encrypt,
    decrypt,
  };
}

