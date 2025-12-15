import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Clock, Lock, Unlock, Plus, ArrowRight } from "lucide-react";
import { useAccount } from "wagmi";
import { BrowserProvider, Contract } from "ethers";
import { PageTransition, FadeIn, StaggerContainer, StaggerItem } from "../components/PageTransition";
import { CONTRACTS } from "../lib/localNetwork";
import TimeCapsuleABI from "../abi/TimeCapsuleABI";

interface DashboardStats {
  total: number;
  locked: number;
  unlocked: number;
}

export function DashboardPage() {
  const { address, isConnected } = useAccount();
  const [stats, setStats] = useState<DashboardStats>({
    total: 0,
    locked: 0,
    unlocked: 0,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!isConnected || !address) return;

    const fetchStats = async () => {
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
        let locked = 0;
        let unlocked = 0;

        // 统计锁定和已解锁的胶囊
        for (let i = 0; i < Number(count); i++) {
          try {
            const capsule = await contract.getCapsule(i);
            const unlockTime = Number(capsule.unlockTime);
            if (Date.now() >= unlockTime * 1000) {
              unlocked++;
            } else {
              locked++;
            }
          } catch (err) {
            console.error(`Failed to fetch capsule ${i}:`, err);
          }
        }

        setStats({
          total: Number(count),
          locked,
          unlocked,
        });
      } catch (err) {
        console.error("Failed to fetch stats:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
    // 每 10 秒刷新一次统计
    const interval = setInterval(fetchStats, 10000);
    return () => clearInterval(interval);
  }, [isConnected, address]);
  return (
    <PageTransition>
      <div className="container mx-auto px-4 py-12">
        <FadeIn>
          <div className="flex items-center justify-between mb-8">
            <h1 className="text-3xl md:text-4xl font-bold">Dashboard</h1>
            <Link to="/create">
              <motion.button
                className="flex items-center gap-2 px-6 py-3 rounded-xl bg-primary text-primary-foreground font-semibold"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                <Plus className="w-5 h-5" />
                New Capsule
              </motion.button>
            </Link>
          </div>
        </FadeIn>

        {!isConnected ? (
          <FadeIn>
            <motion.div
              className="glass-card rounded-3xl p-12 text-center"
              whileHover={{ scale: 1.01 }}
            >
              <Clock className="w-16 h-16 text-primary mx-auto mb-4" />
              <h2 className="text-2xl font-bold mb-4">Connect Your Wallet</h2>
              <p className="text-muted-foreground">
                Please connect your wallet to view your dashboard.
              </p>
            </motion.div>
          </FadeIn>
        ) : (
          <>
            {/* Stats Cards */}
            <StaggerContainer className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
              <StaggerItem>
                <motion.div
                  className="glass-card rounded-2xl p-6"
                  whileHover={{ y: -5 }}
                >
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center">
                      <Clock className="w-6 h-6 text-primary" />
                    </div>
                    <div>
                      <p className="text-muted-foreground text-sm">Total Capsules</p>
                      <p className="text-2xl font-bold">{stats.total}</p>
                    </div>
                  </div>
                </motion.div>
              </StaggerItem>

              <StaggerItem>
                <motion.div
                  className="glass-card rounded-2xl p-6"
                  whileHover={{ y: -5 }}
                >
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-yellow-500/10 flex items-center justify-center">
                      <Lock className="w-6 h-6 text-yellow-500" />
                    </div>
                    <div>
                      <p className="text-muted-foreground text-sm">Locked</p>
                      <p className="text-2xl font-bold">{stats.locked}</p>
                    </div>
                  </div>
                </motion.div>
              </StaggerItem>

              <StaggerItem>
                <motion.div
                  className="glass-card rounded-2xl p-6"
                  whileHover={{ y: -5 }}
                >
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 rounded-xl bg-green-500/10 flex items-center justify-center">
                      <Unlock className="w-6 h-6 text-green-500" />
                    </div>
                    <div>
                      <p className="text-muted-foreground text-sm">Unlocked</p>
                      <p className="text-2xl font-bold">{stats.unlocked}</p>
                    </div>
                  </div>
                </motion.div>
              </StaggerItem>
            </StaggerContainer>

            {/* Empty State or Quick Actions */}
            {stats.total === 0 ? (
              <FadeIn delay={0.3}>
                <motion.div
                  className="glass-card rounded-3xl p-12 text-center"
                  whileHover={{ scale: 1.01 }}
                >
                  <div className="w-20 h-20 rounded-2xl bg-primary/10 flex items-center justify-center mx-auto mb-6">
                    <Clock className="w-10 h-10 text-primary" />
                  </div>
                  <h2 className="text-2xl font-bold mb-4">No Capsules Yet</h2>
                  <p className="text-muted-foreground mb-8 max-w-md mx-auto">
                    Create your first time capsule to store encrypted messages that unlock at a future date.
                  </p>
                  <Link to="/create">
                    <motion.button
                      className="flex items-center gap-2 px-8 py-4 rounded-xl bg-primary text-primary-foreground font-semibold mx-auto"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      Create Your First Capsule
                      <ArrowRight className="w-5 h-5" />
                    </motion.button>
                  </Link>
                </motion.div>
              </FadeIn>
            ) : (
              <FadeIn delay={0.3}>
                <motion.div
                  className="glass-card rounded-3xl p-12 text-center"
                  whileHover={{ scale: 1.01 }}
                >
                  <h2 className="text-2xl font-bold mb-4">Manage Your Capsules</h2>
                  <p className="text-muted-foreground mb-8">
                    View all your capsules and manage their content.
                  </p>
                  <Link to="/capsules">
                    <motion.button
                      className="flex items-center gap-2 px-8 py-4 rounded-xl bg-primary text-primary-foreground font-semibold mx-auto"
                      whileHover={{ scale: 1.05 }}
                      whileTap={{ scale: 0.95 }}
                    >
                      View All Capsules
                      <ArrowRight className="w-5 h-5" />
                    </motion.button>
                  </Link>
                </motion.div>
              </FadeIn>
            )}
          </>
        )}
      </div>
    </PageTransition>
  );
}
