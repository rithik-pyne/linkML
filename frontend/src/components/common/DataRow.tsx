import React from 'react';

interface DataRowProps {
  label: string;
  value: React.ReactNode;
  className?: string;
}

export const DataRow: React.FC<DataRowProps> = ({ label, value, className = '' }) => {
  return (
    <div className={`flex justify-between items-center py-2 border-b border-gray-100 last:border-0 ${className}`}>
      <span className="text-sm text-gray-600 font-medium">{label}:</span>
      <span className="text-sm text-gray-900 font-semibold">{value}</span>
    </div>
  );
};