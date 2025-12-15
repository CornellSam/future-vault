import { motion } from "framer-motion";
import { AlertCircle, CheckCircle, Copy } from "lucide-react";
import { useLocalWallet } from "../hooks/useLocalWallet";
import { LOCAL_NETWORK_CONFIG, TEST_ACCOUNTS } from "../lib/localNetwork";

export function LocalNetworkSetup() {
  const { connectToLocalNetwork, isConnected, address, loading, error, testAccounts } =
    useLocalWallet();

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <motion.div
      className="fixed bottom-4 right-4 max-w-md glass-card rounded-2xl p-6 z-40"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: 20 }}
    >
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          {isConnected ? (
            <CheckCircle className="w-5 h-5 text-green-500" />
          ) : (
            <AlertCircle className="w-5 h-5 text-yellow-500" />
          )}
          <h3 className="font-semibold">Local Network Setup</h3>
        </div>

        {!isConnected ? (
          <div className="space-y-3">
            <p className="text-sm text-muted-foreground">
              Connect to Hardhat local network for testing
            </p>

            <motion.button
              onClick={connectToLocalNetwork}
              disabled={loading}
              className="w-full px-4 py-2 rounded-lg bg-primary text-primary-foreground font-medium disabled:opacity-50"
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              {loading ? "Connecting..." : "Connect to Local Network"}
            </motion.button>

            <div className="text-xs text-muted-foreground space-y-1">
              <p>RPC: {LOCAL_NETWORK_CONFIG.rpcUrl}</p>
              <p>Chain ID: {LOCAL_NETWORK_CONFIG.chainId}</p>
            </div>

            <div className="border-t border-border pt-3">
              <p className="text-xs font-medium mb-2">Test Accounts:</p>
              {testAccounts.map((account, idx) => (
                <div key={idx} className="text-xs space-y-1 mb-2">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-muted-foreground">Account {idx}:</span>
                    <button
                      onClick={() => copyToClipboard(account.address)}
                      className="p-1 hover:bg-secondary rounded"
                    >
                      <Copy className="w-3 h-3" />
                    </button>
                  </div>
                  <code className="block bg-background/50 p-1 rounded text-xs break-all">
                    {account.address}
                  </code>
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="space-y-2">
            <p className="text-sm text-green-400">✓ Connected to Local Network</p>
            <code className="block bg-background/50 p-2 rounded text-xs break-all">
              {address}
            </code>
          </div>
        )}

        {error && (
          <p className="text-xs text-red-400 bg-red-500/10 p-2 rounded">{error}</p>
        )}
      </div>
    </motion.div>
  );
}
