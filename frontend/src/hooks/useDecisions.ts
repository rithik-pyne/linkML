import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { QUERY_KEYS } from '../config/constants';
import type { DecisionsResponse } from '../types/decisions';

export function useDecisions(patientId: string | null) {
  return useQuery({
    queryKey: [QUERY_KEYS.decisions, patientId],
    queryFn: async () => {
      if (!patientId) throw new Error('Patient ID required');
      const response = await apiClient.get<DecisionsResponse>(
        `/api/patients/${patientId}/decisions`
      );
      return response.data;
    },
    enabled: !!patientId,
  });
}