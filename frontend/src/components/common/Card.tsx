import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  highlighted?: boolean;
}

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  title,
  highlighted = false
}) => {
  const baseStyles = 'rounded-lg shadow-md transition-shadow hover:shadow-lg';
  const bgStyles = highlighted
    ? 'bg-cpi-blue-50 border-2 border-cpi-blue'
    : 'bg-white border border-gray-200';

  return (
    <div className={`${baseStyles} ${bgStyles} ${className}`}>
      {title && (
        <div className={`px-6 py-4 border-b ${highlighted ? 'border-cpi-blue-200' : 'border-gray-200'}`}>
          <h2 className="text-xl font-semibold text-gray-900">{title}</h2>
        </div>
      )}
      <div className="p-6">
        {children}
      </div>
    </div>
  );
};