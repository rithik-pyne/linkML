import React from 'react';

export const Header: React.FC = () => {
  return (
    <header className="bg-cpi-blue-800 text-white shadow-lg">
      <div className="container mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          {/* Logo section */}
          <div className="flex items-center gap-4">
            <img
              src="/assets/cpi-logo.png"
              alt="CPI Logo"
              className="h-12 w-auto"
            />
            <div className="border-l border-white/30 h-10" />
            <h1 className="text-2xl font-semibold">
              EGFR-NSCLC Clinical Dashboard
            </h1>
          </div>

          {/* Version badge */}
          <div className="flex items-center gap-2">
            <span className="text-sm text-cpi-blue-100">Version 1.0</span>
          </div>
        </div>
      </div>
    </header>
  );
};