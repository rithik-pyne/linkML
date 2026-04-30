import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { QUERY_KEYS } from '../config/constants';
import type { PatientSummary } from '../types/patient';

export function usePatientSummary(patientId: string | null) {
  return useQuery({
    queryKey: [QUERY_KEYS.patientSummary, patientId],
    queryFn: async () => {
      if (!patientId) throw new Error('Patient ID required');
      const response = await apiClient.get<PatientSummary>(
        `/api/patients/${patientId}/summary`
      );
      return response.data;
    },
    enabled: !!patientId, // Only fetch when patientId exists
  });
}