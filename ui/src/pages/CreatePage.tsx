import { useState } from "react";
import { motion } from "framer-motion";
import { Calendar, Clock, Lock, Send, FileText, AlertCircle, CheckCircle } from "lucide-react";
import { useAccount } from "wagmi";
import { BrowserProvider, Contract, ethers } from "ethers";
import { PageTransition, FadeIn } from "../components/PageTransition";
import { CONTRACTS } from "../lib/localNetwork";
import TimeCapsuleABI from "../abi/TimeCapsuleABI";

export function CreatePage() {
  const { address, isConnected } = useAccount();
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [content, setContent] = useState("");
  const [unlockDate, setUnlockDate] = useState("");
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<"idle" | "success" | "error">("idle");
  const [message, setMessage] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!isConnected || !address) {
      setStatus("error");
      setMessage("Please connect your wallet first");
      return;
    }

    if (!title || !content || !unlockDate) {
      setStatus("error");
      setMessage("Please fill in all required fields");
      return;
    }

    setLoading(true);
    setStatus("idle");

    try {
      // 获取 provider 和 signer
      if (!(window as any).ethereum) {
        throw new Error("MetaMask not found");
      }

      const provider = new BrowserProvider((window as any).ethereum);
      const signer = await provider.getSigner();

      // 创建合约实例
      const contract = new Contract(
        CONTRACTS.TimeCapsule,
        TimeCapsuleABI,
        signer
      );

      // 转换日期为时间戳
      const unlockTimestamp = Math.floor(new Date(unlockDate).getTime() / 1000);
      const now = Math.floor(Date.now() / 1000);

      if (unlockTimestamp <= now) {
        throw new Error("Unlock date must be in the future");
      }

      // 调用合约
      const tx = await contract.createCapsule(
        title,
        description,
        ethers.toUtf8Bytes(content),
        unlockTimestamp
      );

      // 等待交易确认
      const receipt = await tx.wait();

      if (receipt) {
        setStatus("success");
        setMessage("Capsule created successfully!");
        // 清空表单
        setTitle("");
        setDescription("");
        setContent("");
        setUnlockDate("");
        
        // 3秒后重置状态
        setTimeout(() => setStatus("idle"), 3000);
      }
    } catch (err: any) {
      setStatus("error");
      setMessage(err.message || "Failed to create capsule");
      console.error("Error creating capsule:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <PageTransition>
      <div className="container mx-auto px-4 py-12">
        <FadeIn>
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-12">
              <motion.div
                className="w-20 h-20 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-6"
                whileHover={{ rotate: 10 }}
              >
                <Lock className="w-10 h-10 text-primary" />
              </motion.div>
              <h1 className="text-3xl md:text-4xl font-bold mb-4">
                Create Time Capsule
              </h1>
              <p className="text-muted-foreground">
                Lock your message until a future date using FHE encryption.
              </p>
            </div>

            {!isConnected && (
              <motion.div
                className="mb-6 p-4 rounded-xl bg-yellow-500/10 border border-yellow-500/20 flex items-center gap-3"
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
              >
                <AlertCircle className="w-5 h-5 text-yellow-500 flex-shrink-0" />
                <p className="text-sm text-yellow-400">
                  Please connect your wallet to create a capsule
                </p>
              </motion.div>
            )}

            <motion.form
              onSubmit={handleSubmit}
              className="glass-card rounded-2xl p-8 space-y-6"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
            >
              {/* Title */}
              <div>
                <label className="flex items-center gap-2 text-sm font-medium mb-2">
                  <FileText className="w-4 h-4" />
                  Title
                </label>
                <input
                  type="text"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Give your capsule a name"
                  className="w-full px-4 py-3 rounded-xl bg-background border border-border focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-colors"
                  required
                  disabled={loading}
                />
              </div>

              {/* Description */}
              <div>
                <label className="flex items-center gap-2 text-sm font-medium mb-2">
                  <FileText className="w-4 h-4" />
                  Description (Public)
                </label>
                <input
                  type="text"
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="A brief description (visible to everyone)"
                  className="w-full px-4 py-3 rounded-xl bg-background border border-border focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-colors"
                  disabled={loading}
                />
              </div>

              {/* Secret Content */}
              <div>
                <label className="flex items-center gap-2 text-sm font-medium mb-2">
                  <Lock className="w-4 h-4" />
                  Secret Message (Encrypted)
                </label>
                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  placeholder="This message will be encrypted and only revealed after the unlock date"
                  rows={4}
                  className="w-full px-4 py-3 rounded-xl bg-background border border-border focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-colors resize-none"
                  required
                  disabled={loading}
                />
              </div>

              {/* Unlock Date */}
              <div>
                <label className="flex items-center gap-2 text-sm font-medium mb-2">
                  <Calendar className="w-4 h-4" />
                  Unlock Date
                </label>
                <input
                  type="datetime-local"
                  value={unlockDate}
                  onChange={(e) => setUnlockDate(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl bg-background border border-border focus:border-primary focus:ring-1 focus:ring-primary outline-none transition-colors"
                  required
                  disabled={loading}
                />
              </div>

              {/* Status Messages */}
              {status === "success" && (
                <motion.div
                  className="p-4 rounded-xl bg-green-500/10 border border-green-500/20 flex items-center gap-3"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <CheckCircle className="w-5 h-5 text-green-500 flex-shrink-0" />
                  <p className="text-sm text-green-400">{message}</p>
                </motion.div>
              )}

              {status === "error" && (
                <motion.div
                  className="p-4 rounded-xl bg-red-500/10 border border-red-500/20 flex items-center gap-3"
                  initial={{ opacity: 0, y: -10 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0" />
                  <p className="text-sm text-red-400">{message}</p>
                </motion.div>
              )}

              {/* Submit Button */}
              <motion.button
                type="submit"
                disabled={loading || !isConnected}
                className="w-full flex items-center justify-center gap-2 px-8 py-4 rounded-xl bg-primary text-primary-foreground font-semibold text-lg glow-primary disabled:opacity-50 disabled:cursor-not-allowed"
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                <Clock className="w-5 h-5" />
                {loading ? "Creating..." : "Create Capsule"}
                <Send className="w-5 h-5" />
              </motion.button>
            </motion.form>
          </div>
        </FadeIn>
      </div>
    </PageTransition>
  );
}
