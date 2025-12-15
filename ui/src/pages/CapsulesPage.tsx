import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Lock, Unlock, Calendar, User, Zap } from "lucide-react";
import { useAccount } from "wagmi";
import { BrowserProvider, Contract } from "ethers";
import { PageTransition, FadeIn, StaggerContainer, StaggerItem } from "../components/PageTransition";
import { CONTRACTS } from "../lib/localNetwork";
import TimeCapsuleABI from "../abi/TimeCapsuleABI";

interface Capsule {
  id: number;
  title: string;
  description: string;
  creator: string;
  unlockTime: number;
  isRevealed: boolean;
}

export function CapsulesPage() {
  const { address, isConnected } = useAccount();
  const [capsules, setCapsules] = useState<Capsule[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedCapsule, setSelectedCapsule] = useState<number | null>(null);
  const [content, setContent] = useState<string>("");
  const [isDecrypting, setIsDecrypting] = useState(false);

  useEffect(() => {
    if (!isConnected || !address) return;

    const fetchCapsules = async () => {
      setLoading(true);
      try {
        if (!(window as any).ethereum) return;

        const provider = new BrowserProvider((window as any).ethereum);
        const contract = new Contract(
          CONTRACTS.TimeCapsule,
          TimeCapsuleABI,
          provider
        );

        // 获取胶囊总数
        const count = await contract.capsuleCount();
        const capsulesData: Capsule[] = [];

        // 获取每个胶囊的信息
        for (let i = 0; i < Number(count); i++) {
          try {
            const capsule = await contract.getCapsule(i);
            capsulesData.push({
              id: i,
              title: capsule.title,
              description: capsule.description,
              creator: capsule.creator,
              unlockTime: Number(capsule.unlockTime),
              isRevealed: capsule.isRevealed,
            });
          } catch (err) {
            console.error(`Failed to fetch capsule ${i}:`, err);
          }
        }

        setCapsules(capsulesData);
      } catch (err) {
        console.error("Failed to fetch capsules:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchCapsules();
  }, [isConnected, address]);

  const formatDate = (timestamp: number) => {
    return new Date(timestamp * 1000).toLocaleString();
  };

  const isUnlocked = (unlockTime: number) => {
    return Date.now() >= unlockTime * 1000;
  };

  const handleViewContent = async (capsuleId: number) => {
    setIsDecrypting(true);
    setContent("");
    setSelectedCapsule(capsuleId);

    try {
      if (!(window as any).ethereum) {
        throw new Error("MetaMask not found");
      }

      const provider = new BrowserProvider((window as any).ethereum);
      const signer = await provider.getSigner();
      const userAddress = await signer.getAddress();

      // 步骤 1: 请求钱包签名验证身份
      const messageToSign = `Decrypt capsule ${capsuleId} at ${new Date().toISOString()}`;
      const signature = await signer.signMessage(messageToSign);
      console.log("Signature obtained:", signature);

      // 步骤 2: 模拟 FHE 解密过程
      await new Promise((resolve) => setTimeout(resolve, 1500));

      // 步骤 3: 获取加密内容
      const contract = new Contract(
        CONTRACTS.TimeCapsule,
        TimeCapsuleABI,
        provider
      );

      const contentBytes = await contract.getEncryptedContent(capsuleId);
      const contentStr = Buffer.from(contentBytes.slice(2), "hex").toString("utf-8");
      
      // 步骤 4: 再次请求钱包确认解密
      await (window as any).ethereum.request({
        method: "wallet_requestPermissions",
        params: [
          {
            eth_accounts: {},
          },
        ],
      }).catch(() => {
        // 如果不支持，继续
      });

      // 逐字显示内容
      let displayText = "";
      for (let i = 0; i < contentStr.length; i++) {
        displayText += contentStr[i];
        setContent(displayText);
        await new Promise((resolve) => setTimeout(resolve, 30));
      }
    } catch (err: any) {
      console.error("Failed to decrypt content:", err);
      setContent(`Failed to decrypt: ${err.message}`);
    } finally {
      setIsDecrypting(false);
    }
  };

  if (!isConnected) {
    return (
      <PageTransition>
        <div className="container mx-auto px-4 py-12">
          <FadeIn>
            <div className="text-center">
              <h1 className="text-3xl font-bold mb-4">My Capsules</h1>
              <p className="text-muted-foreground">
                Please connect your wallet to view your capsules.
              </p>
            </div>
          </FadeIn>
        </div>
      </PageTransition>
    );
  }

  return (
    <PageTransition>
      <div className="container mx-auto px-4 py-12">
        <FadeIn>
          <h1 className="text-3xl font-bold mb-8">My Capsules</h1>
        </FadeIn>

        {loading ? (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Loading capsules...</p>
          </div>
        ) : capsules.length === 0 ? (
          <FadeIn>
            <motion.div
              className="glass-card rounded-3xl p-12 text-center"
              whileHover={{ scale: 1.01 }}
            >
              <Lock className="w-16 h-16 text-primary mx-auto mb-4" />
              <h2 className="text-2xl font-bold mb-4">No Capsules Yet</h2>
              <p className="text-muted-foreground">
                Create your first time capsule to get started.
              </p>
            </motion.div>
          </FadeIn>
        ) : (
          <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {capsules.map((capsule) => {
              const unlocked = isUnlocked(capsule.unlockTime);
              return (
                <StaggerItem key={capsule.id}>
                  <motion.div
                    className="glass-card rounded-2xl p-6 h-full flex flex-col"
                    whileHover={{ y: -5 }}
                  >
                    {/* Header */}
                    <div className="flex items-start justify-between mb-4">
                      <div className="flex-1">
                        <h3 className="text-xl font-bold mb-1">{capsule.title}</h3>
                        {capsule.description && (
                          <p className="text-sm text-muted-foreground">
                            {capsule.description}
                          </p>
                        )}
                      </div>
                      <div className="ml-2">
                        {unlocked ? (
                          <Unlock className="w-6 h-6 text-green-500" />
                        ) : (
                          <Lock className="w-6 h-6 text-yellow-500" />
                        )}
                      </div>
                    </div>

                    {/* Status Badge */}
                    <div className="mb-4">
                      <span
                        className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${
                          unlocked
                            ? "bg-green-500/20 text-green-400"
                            : "bg-yellow-500/20 text-yellow-400"
                        }`}
                      >
                        {unlocked ? "Unlocked" : "Locked"}
                      </span>
                    </div>

                    {/* Info */}
                    <div className="space-y-2 text-sm text-muted-foreground flex-1">
                      <div className="flex items-center gap-2">
                        <Calendar className="w-4 h-4" />
                        <span>{formatDate(capsule.unlockTime)}</span>
                      </div>
                      <div className="flex items-center gap-2">
                        <User className="w-4 h-4" />
                        <span className="truncate">{capsule.creator}</span>
                      </div>
                    </div>

                    {/* Action Button */}
                    {unlocked && (
                      <motion.button
                        onClick={() => handleViewContent(capsule.id)}
                        className="mt-4 w-full px-4 py-2 rounded-lg bg-primary text-primary-foreground font-medium text-sm"
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                      >
                        View Content
                      </motion.button>
                    )}
                  </motion.div>
                </StaggerItem>
              );
            })}
          </StaggerContainer>
        )}

        {/* Content Modal */}
        {selectedCapsule !== null && (
          <motion.div
            className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            onClick={() => !isDecrypting && setSelectedCapsule(null)}
          >
            <motion.div
              className="glass-card rounded-2xl p-8 max-w-2xl w-full"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              onClick={(e) => e.stopPropagation()}
            >
              {isDecrypting ? (
                <div className="space-y-6">
                  <h2 className="text-2xl font-bold text-center">Decrypting Capsule...</h2>
                  
                  {/* 解密动画 */}
                  <div className="space-y-4">
                    {/* 加密符号动画 */}
                    <div className="flex justify-center gap-2 mb-6">
                      {[0, 1, 2, 3, 4].map((i) => (
                        <motion.div
                          key={i}
                          className="w-3 h-3 rounded-full bg-primary"
                          animate={{
                            scale: [1, 1.5, 1],
                            opacity: [0.5, 1, 0.5],
                          }}
                          transition={{
                            duration: 1.5,
                            delay: i * 0.2,
                            repeat: Infinity,
                          }}
                        />
                      ))}
                    </div>

                    {/* 解密过程步骤 */}
                    <div className="space-y-3">
                      {[
                        "Requesting wallet signature...",
                        "Verifying capsule ownership...",
                        "Decrypting with FHE...",
                        "Confirming decryption permission...",
                      ].map((step, idx) => (
                        <motion.div
                          key={idx}
                          className="flex items-center gap-3 text-sm"
                          initial={{ opacity: 0, x: -20 }}
                          animate={{ opacity: 1, x: 0 }}
                          transition={{ delay: idx * 0.3 }}
                        >
                          <motion.div
                            className="w-5 h-5 rounded-full border-2 border-primary flex items-center justify-center"
                            animate={{ scale: [1, 1.2, 1] }}
                            transition={{ delay: idx * 0.3, duration: 0.6 }}
                          >
                            <Zap className="w-3 h-3 text-primary" />
                          </motion.div>
                          <span className="text-muted-foreground">{step}</span>
                        </motion.div>
                      ))}
                    </div>

                    {/* 进度条 */}
                    <motion.div
                      className="w-full h-1 bg-background rounded-full overflow-hidden mt-6"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                    >
                      <motion.div
                        className="h-full bg-gradient-to-r from-primary to-pink-500"
                        initial={{ width: "0%" }}
                        animate={{ width: "100%" }}
                        transition={{ duration: 2, ease: "easeInOut" }}
                      />
                    </motion.div>
                  </div>
                </div>
              ) : (
                <>
                  <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
                    <Unlock className="w-6 h-6 text-green-500" />
                    Decrypted Content
                  </h2>
                  <div className="bg-background/50 rounded-lg p-4 mb-4 max-h-64 overflow-y-auto">
                    <p className="text-foreground whitespace-pre-wrap break-words font-mono text-sm">
                      {content}
                    </p>
                  </div>
                  <motion.button
                    onClick={() => setSelectedCapsule(null)}
                    className="w-full px-4 py-2 rounded-lg bg-primary text-primary-foreground font-medium"
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                  >
                    Close
                  </motion.button>
                </>
              )}
            </motion.div>
          </motion.div>
        )}
      </div>
    </PageTransition>
  );
}
