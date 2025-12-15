import { useState, useEffect, useCallback } from "react";
import { BrowserProvider, Contract } from "ethers";
import { TimeCapsuleABI } from "../abi/TimeCapsuleABI";
import { TIMECAPSULE_ADDRESSES } from "../abi/TimeCapsuleAddresses";
import type { TimeCapsule, CapsuleStats, ActivityItem, TimelineItem } from "../types/capsule";

export function useContract() {
  const [contract, setContract] = useState<Contract | null>(null);
  const [provider, setProvider] = useState<BrowserProvider | null>(null);
  const [chainId, setChainId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const init = async () => {
      try {
        if (typeof window !== "undefined" && (window as any).ethereum) {
          const browserProvider = new BrowserProvider((window as any).ethereum);
          const network = await browserProvider.getNetwork();
          const currentChainId = Number(network.chainId);
          
          setProvider(browserProvider);
          setChainId(currentChainId);
          
          const contractAddress = TIMECAPSULE_ADDRESSES[currentChainId];
          if (contractAddress) {
            const signer = await browserProvider.getSigner();
            const timeCapsuleContract = new Contract(contractAddress, TimeCapsuleABI, signer);
            setContract(timeCapsuleContract);
          }
        }
      } catch (err: any) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    init();
  }, []);

  const getTotalCapsules = useCallback(async (): Promise<number> => {
    if (!contract) return 0;
    try {
      const total = await contract.getTotalCapsules();
      return Number(total);
    } catch {
      return 0;
    }
  }, [contract]);

  const getCapsule = useCallback(async (id: number): Promise<TimeCapsule | null> => {
    if (!contract) return null;
    try {
      const capsule = await contract.getCapsule(id);
      const canUnlockResult = await contract.canUnlock(id);
      const now = Math.floor(Date.now() / 1000);
      
      return {
        id,
        encryptedMessagePart1: capsule[0],
        encryptedMessagePart2: capsule[1],
        unlockTimestamp: Number(capsule[2]),
        creator: capsule[3],
        exists: capsule[4],
        isLocked: Number(capsule[2]) > now,
        canUnlock: canUnlockResult,
      };
    } catch {
      return null;
    }
  }, [contract]);

  const getUserCapsules = useCallback(async (address: string): Promise<number[]> => {
    if (!contract) return [];
    try {
      const capsuleIds = await contract.getUserCapsules(address);
      return capsuleIds.map((id: bigint) => Number(id));
    } catch {
      return [];
    }
  }, [contract]);

  const getAllCapsules = useCallback(async (): Promise<TimeCapsule[]> => {
    if (!contract) return [];
    try {
      const total = await getTotalCapsules();
      const capsules: TimeCapsule[] = [];
      
      for (let i = 0; i < total; i++) {
        const capsule = await getCapsule(i);
        if (capsule && capsule.exists) {
          capsules.push(capsule);
        }
      }
      
      return capsules;
    } catch {
      return [];
    }
  }, [contract, getTotalCapsules, getCapsule]);

  const getStats = useCallback(async (userAddress?: string): Promise<CapsuleStats> => {
    const capsules = await getAllCapsules();
    const now = Math.floor(Date.now() / 1000);
    const oneDayFromNow = now + 86400;
    
    const locked = capsules.filter(c => c.isLocked);
    const unlocked = capsules.filter(c => !c.isLocked);
    
    let userCapsules: TimeCapsule[] = [];
    if (userAddress) {
      userCapsules = capsules.filter(
        c => c.creator.toLowerCase() === userAddress.toLowerCase()
      );
    }
    
    const userLocked = userCapsules.filter(c => c.isLocked);
    const userUnlocked = userCapsules.filter(c => !c.isLocked);
    
    // Calculate average lock duration
    let totalDuration = 0;
    capsules.forEach(c => {
      totalDuration += c.unlockTimestamp - now;
    });
    const averageLockDuration = capsules.length > 0 ? totalDuration / capsules.length : 0;
    
    // Capsules unlocking soon (within 24 hours)
    const unlockingSoon = locked.filter(c => c.unlockTimestamp <= oneDayFromNow).length;
    
    // Recent activity (simulated from capsule data)
    const recentActivity: ActivityItem[] = capsules
      .slice(-10)
      .map(c => ({
        id: c.id,
        type: c.isLocked ? "created" : "unlocked",
        timestamp: c.unlockTimestamp,
        creator: c.creator,
      }))
      .reverse();
    
    // Timeline data for charts
    const timelineMap = new Map<string, TimelineItem>();
    capsules.forEach(c => {
      const date = new Date(c.unlockTimestamp * 1000).toLocaleDateString("en-US", {
        month: "short",
        day: "numeric",
      });
      
      const existing = timelineMap.get(date) || { date, count: 0, locked: 0, unlocked: 0 };
      existing.count++;
      if (c.isLocked) {
        existing.locked++;
      } else {
        existing.unlocked++;
      }
      timelineMap.set(date, existing);
    });
    
    const unlockTimeline = Array.from(timelineMap.values()).slice(-7);
    
    return {
      total: capsules.length,
      locked: locked.length,
      unlocked: unlocked.length,
      userTotal: userCapsules.length,
      userLocked: userLocked.length,
      userUnlocked: userUnlocked.length,
      averageLockDuration,
      capsulesUnlockingSoon: unlockingSoon,
      recentActivity,
      unlockTimeline,
    };
  }, [getAllCapsules]);

  return {
    contract,
    provider,
    chainId,
    loading,
    error,
    getTotalCapsules,
    getCapsule,
    getUserCapsules,
    getAllCapsules,
    getStats,
  };
}
