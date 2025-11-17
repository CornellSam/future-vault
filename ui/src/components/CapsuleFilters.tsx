import React, { useState } from 'react';
export const CapsuleFilters = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  
  return (
    <div className="flex space-x-4 mb-4">
      <input
        type="text"
        placeholder="Search capsules..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        className="px-3 py-2 border rounded-md"
      />
      <select
        value={statusFilter}
        onChange={(e) => setStatusFilter(e.target.value)}
        className="px-3 py-2 border rounded-md"
      >
        <option value="all">All Status</option>
        <option value="locked">Locked</option>
        <option value="unlocked">Unlocked</option>
      </select>
    </div>
  );
};