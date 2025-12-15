export const TimeCapsuleABI = [
  {
    inputs: [
      { internalType: "string", name: "title", type: "string" },
      { internalType: "string", name: "description", type: "string" },
      { internalType: "bytes", name: "content", type: "bytes" },
      { internalType: "uint256", name: "unlockTime", type: "uint256" },
    ],
    name: "createCapsule",
    outputs: [{ internalType: "uint256", name: "", type: "uint256" }],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [{ internalType: "uint256", name: "capsuleId", type: "uint256" }],
    name: "revealCapsule",
    outputs: [],
    stateMutability: "nonpayable",
    type: "function",
  },
  {
    inputs: [{ internalType: "uint256", name: "capsuleId", type: "uint256" }],
    name: "getCapsule",
    outputs: [
      { internalType: "address", name: "creator", type: "address" },
      { internalType: "uint256", name: "unlockTime", type: "uint256" },
      { internalType: "bool", name: "isRevealed", type: "bool" },
      { internalType: "string", name: "title", type: "string" },
      { internalType: "string", name: "description", type: "string" },
    ],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [{ internalType: "uint256", name: "capsuleId", type: "uint256" }],
    name: "getEncryptedContent",
    outputs: [{ internalType: "bytes", name: "", type: "bytes" }],
    stateMutability: "view",
    type: "function",
  },
  {
    inputs: [],
    name: "capsuleCount",
    outputs: [{ internalType: "uint256", name: "", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
  {
    anonymous: false,
    inputs: [
      { indexed: true, internalType: "uint256", name: "capsuleId", type: "uint256" },
      { indexed: true, internalType: "address", name: "creator", type: "address" },
      { indexed: false, internalType: "uint256", name: "unlockTime", type: "uint256" },
    ],
    name: "CapsuleCreated",
    type: "event",
  },
  {
    anonymous: false,
    inputs: [
      { indexed: true, internalType: "uint256", name: "capsuleId", type: "uint256" },
    ],
    name: "CapsuleRevealed",
    type: "event",
  },
] as const;

export default TimeCapsuleABI;
