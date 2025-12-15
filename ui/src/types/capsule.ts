export interface TimeCapsule {
  id: number;
  encryptedMessagePart1: string;
  encryptedMessagePart2: string;
  unlockTimestamp: number;
  creator: string;
  exists: boolean;
  isLocked: boolean;
  canUnlock: boolean;
  decryptedMessage?: string;
}

export interface CapsuleStats {
  total: number;
  locked: number;
  unlocked: number;
  userTotal: number;
  userLocked: number;
  userUnlocked: number;
  averageLockDuration: number;
  capsulesUnlockingSoon: number;
  recentActivity: ActivityItem[];
  unlockTimeline: TimelineItem[];
}

export interface ActivityItem {
  id: number;
  type: "created" | "unlocked";
  timestamp: number;
  creator: string;
}

export interface TimelineItem {
  date: string;
  count: number;
  locked: number;
  unlocked: number;
}

export interface DashboardData {
  stats: CapsuleStats;
  capsules: TimeCapsule[];
  loading: boolean;
  error: string | null;
}
