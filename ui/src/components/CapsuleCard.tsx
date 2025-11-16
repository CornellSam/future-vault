import React from 'react';
export const CapsuleCard = ({ capsule, loading, error }) => {
  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  
  return (
    <div className="bg-white rounded-lg shadow-md p-4">
      <h3>{capsule.title}</h3>
      <p>Unlocks: {capsule.unlockDate}</p>
    </div>
  );
};