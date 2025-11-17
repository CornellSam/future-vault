import React from 'react';
export const Dashboard = ({ stats }) => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900">Total Capsules</h3>
        <p className="text-3xl font-bold text-blue-600">{stats.total}</p>
      </div>
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900">Locked Capsules</h3>
        <p className="text-3xl font-bold text-orange-600">{stats.locked}</p>
      </div>
      <div className="bg-white rounded-lg shadow-md p-6">
        <h3 className="text-lg font-semibold text-gray-900">Unlocked Capsules</h3>
        <p className="text-3xl font-bold text-green-600">{stats.unlocked}</p>
      </div>
    </div>
  );
};