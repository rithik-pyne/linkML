import React from 'react';
import { NavLink } from 'react-router-dom';

interface TabNavigationProps {
  patientId: string;
}

export const TabNavigation: React.FC<TabNavigationProps> = ({ patientId }) => {
  const baseClass = "px-6 py-3 font-medium text-sm border-b-2 transition-colors";
  const activeClass = "border-cpi-blue text-cpi-blue bg-blue-50";
  const inactiveClass = "border-transparent text-gray-600 hover:text-gray-900 hover:border-gray-300";

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="flex gap-1">
        <NavLink
          to="/"
          end
          className={({ isActive }) =>
            `${baseClass} ${isActive ? activeClass : inactiveClass}`
          }
        >
          Overview
        </NavLink>
        <NavLink
          to={`/patient/${patientId}/imaging`}
          className={({ isActive }) =>
            `${baseClass} ${isActive ? activeClass : inactiveClass}`
          }
        >
          Imaging Studies
        </NavLink>
      </div>
    </nav>
  );
};