import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-gray-100 border-t border-gray-300 mt-12">
      <div className="container mx-auto px-6 py-6">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-gray-600">
            <p className="font-semibold text-cpi-blue-600">
              NG-DX Clinical Decision Support System
            </p>
            <p className="text-xs mt-1">
              Developed for demonstration purposes. Not for clinical use.
            </p>
          </div>

          <div className="flex items-center gap-6 text-xs text-gray-500">
            <span>Backend API: http://localhost:8000</span>
            <span>•</span>
            <span>Data: 5 patients (2020-2023)</span>
            <span>•</span>
            <span>Version 1.0</span>
          </div>
        </div>
      </div>
    </footer>
  );
};