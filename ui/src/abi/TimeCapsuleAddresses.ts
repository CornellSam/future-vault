export const TIMECAPSULE_ADDRESSES: Record<number, string> = {
  // Local development network
  31337: "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
  // Sepolia testnet
  11155111: "0x0000000000000000000000000000000000000000",
};

export const SUPPORTED_CHAINS = [31337, 11155111];

export function getContractAddress(chainId: number): string | null {
  return TIMECAPSULE_ADDRESSES[chainId] || null;
}

export function isSupportedChain(chainId: number): boolean {
  return SUPPORTED_CHAINS.includes(chainId);
}
