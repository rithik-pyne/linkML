import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'default' | 'success' | 'warning' | 'danger' | 'info';
  size?: 'sm' | 'md' | 'lg';
  className?: string;
}

const variantStyles = {
  default: 'bg-gray-100 text-gray-800 border-gray-300',
  success: 'bg-green-100 text-green-800 border-green-300',
  warning: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  danger: 'bg-red-100 text-red-800 border-red-300',
  info: 'bg-blue-100 text-blue-800 border-blue-300',
};

const sizeStyles = {
  sm: 'text-xs px-2 py-0.5',
  md: 'text-sm px-2.5 py-1',
  lg: 'text-base px-3 py-1.5',
};

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'default',
  size = 'md',
  className = '',
}) => {
  return (
    <span
      className={`
        inline-flex items-center font-medium border rounded-full
        ${variantStyles[variant]}
        ${sizeStyles[size]}
        ${className}
      `}
    >
      {children}
    </span>
  );
};

// Specialized badge for ECOG status
interface ECOGBadgeProps {
  status: number;
}

export const ECOGBadge: React.FC<ECOGBadgeProps> = ({ status }) => {
  const variant = status === 0 ? 'success' : status <= 2 ? 'warning' : 'danger';
  return <Badge variant={variant}>ECOG {status}</Badge>;
};

// Specialized badge for cancer stage
interface StageBadgeProps {
  stage: string;
}

export const StageBadge: React.FC<StageBadgeProps> = ({ stage }) => {
  // Early stage (I) = green, intermediate (II/III) = yellow, advanced (IV) = red
  const variant = stage.startsWith('I') && !stage.startsWith('IV')
    ? 'success'
    : stage.startsWith('II') || stage.startsWith('III')
    ? 'warning'
    : 'danger';

  return <Badge variant={variant}>Stage {stage}</Badge>;
};