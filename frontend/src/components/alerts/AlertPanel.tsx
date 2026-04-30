import React from 'react';
import { AlertCircle, AlertTriangle, Info, Clock } from 'lucide-react';
import { useAlerts } from '../../hooks/useAlerts';
import { Card } from '../common/Card';
import { LoadingSpinner } from '../common/LoadingSpinner';
import { ErrorMessage } from '../common/ErrorMessage';
import { Badge } from '../common/Badge';
import type { Alert } from '../../types/decisions';

interface AlertCardProps {
  alert: Alert;
}

const AlertCard: React.FC<AlertCardProps> = ({ alert }) => {
  // Severity configuration
  const severityConfig = {
    Critical: {
      bg: 'bg-red-50',
      border: 'border-cpi-red',
      icon: AlertCircle,
      iconColor: 'text-cpi-red',
      textColor: 'text-red-800',
    },
    High: {
      bg: 'bg-orange-50',
      border: 'border-cpi-orange',
      icon: AlertTriangle,
      iconColor: 'text-cpi-orange',
      textColor: 'text-orange-800',
    },
    Medium: {
      bg: 'bg-blue-50',
      border: 'border-blue-400',
      icon: Info,
      iconColor: 'text-blue-600',
      textColor: 'text-blue-800',
    },
    Low: {
      bg: 'bg-gray-50',
      border: 'border-gray-300',
      icon: Clock,
      iconColor: 'text-gray-600',
      textColor: 'text-gray-800',
    },
  };

  const config = severityConfig[alert.severity] || severityConfig.Medium;
  const Icon = config.icon;

  return (
    <div className={`${config.bg} border-l-4 ${config.border} rounded-r p-4`}>
      <div className="flex items-start gap-3">
        <Icon className={`h-5 w-5 ${config.iconColor} flex-shrink-0 mt-0.5`} />

        <div className="flex-1">
          {/* Alert message */}
          <p className={`font-semibold ${config.textColor} mb-1`}>
            {alert.message}
          </p>

          {/* Trigger date */}
          <p className="text-xs text-gray-500 mb-2">
            Triggered: {new Date(alert.trigger_date).toLocaleDateString()}
          </p>

          {/* Action recommendation (if requires action) */}
          {alert.requires_action && (
            <div className="mt-3 p-3 bg-white rounded-lg border border-gray-200">
              <p className="text-xs font-medium text-gray-700 mb-1">
                Recommended Action:
              </p>
              <p className="text-sm text-gray-900">
                {alert.action_recommendation}
              </p>
            </div>
          )}

          {/* Severity badge */}
          <div className="mt-2">
            <Badge
              variant={alert.severity === 'Critical' || alert.severity === 'High' ? 'danger' : alert.severity === 'Medium' ? 'info' : 'default'}
              size="sm"
            >
              {alert.severity}
            </Badge>
          </div>
        </div>
      </div>
    </div>
  );
};

interface AlertPanelProps {
  patientId: string | null;
}

export const AlertPanel: React.FC<AlertPanelProps> = ({ patientId }) => {
  const { data, isLoading, error, refetch } = useAlerts(patientId);

  if (!patientId) {
    return (
      <Card title="Active Alerts">
        <p className="text-gray-500 text-center py-8">
          Please select a patient to view alerts
        </p>
      </Card>
    );
  }

  if (isLoading) {
    return (
      <Card title="Active Alerts">
        <LoadingSpinner message="Loading alerts..." />
      </Card>
    );
  }

  if (error) {
    return (
      <Card title="Active Alerts">
        <ErrorMessage
          message={`Failed to load alerts: ${error.message}`}
          onRetry={() => refetch()}
        />
      </Card>
    );
  }

  if (!data) {
    return (
      <Card title="Active Alerts">
        <p className="text-gray-500">No data available</p>
      </Card>
    );
  }

  return (
    <Card title="Active Alerts">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">Clinical Alerts</h3>
        <Badge variant="danger" size="lg">
          {data.total_active_alerts}
        </Badge>
      </div>

      {data.alerts.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-green-600 font-medium">✓ No active alerts</p>
          <p className="text-sm text-gray-500 mt-1">Patient status is stable</p>
        </div>
      ) : (
        <div className="space-y-3">
          {data.alerts.map(alert => (
            <AlertCard key={alert.alert_id} alert={alert} />
          ))}
        </div>
      )}
    </Card>
  );
};