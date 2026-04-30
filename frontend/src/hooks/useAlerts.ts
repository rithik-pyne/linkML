import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { QUERY_KEYS } from '../config/constants';
import type { Alert } from '../types/decisions';

interface AlertsResponse {
  patient_id: string;
  alerts: Alert[];
  overdue_tests: string[];
  total_active_alerts: number;
}

export function useAlerts(patientId: string | null) {
  return useQuery({
    queryKey: [QUERY_KEYS.alerts, patientId],
    queryFn: async () => {
      if (!patientId) throw new Error('Patient ID required');
      const response = await apiClient.get<AlertsResponse>(
        `/api/patients/${patientId}/alerts`
      );
      return response.data;
    },
    enabled: !!patientId,
  });
}