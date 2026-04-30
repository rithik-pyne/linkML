import React from 'react';
import { AlertTriangle } from 'lucide-react';

export const DisclaimerBanner: React.FC = () => {
  return (
    <div className="bg-cpi-red border-l-4 border-cpi-red-dark">
      <div className="container mx-auto px-6 py-3">
        <div className="flex items-start gap-3">
          <AlertTriangle className="h-5 w-5 text-white flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-white text-sm font-semibold leading-relaxed">
              ⚠️ FOR DEMONSTRATION PURPOSES ONLY - This clinical decision support
              system is a simplified mock implementation for proof-of-concept
              demonstration. It is NOT validated for clinical use and must NOT
              be used for real patient care decisions. All treatment recommendations
              should be made by qualified oncologists following current evidence-based
              guidelines.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};