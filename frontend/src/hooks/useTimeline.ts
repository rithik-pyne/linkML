import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { QUERY_KEYS } from '../config/constants';
import type { Timeline } from '../types/timeline';

export function useTimeline(patientId: string | null) {
  return useQuery({
    queryKey: [QUERY_KEYS.timeline, patientId],
    queryFn: async () => {
      if (!patientId) throw new Error('Patient ID required');
      const response = await apiClient.get<Timeline>(
        `/api/patients/${patientId}/timeline`
      );
      return response.data;
    },
    enabled: !!patientId,
  });
}