import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { QUERY_KEYS } from '../config/constants';
import type { MolecularProfile } from '../types/molecular';

export function useMolecularProfile(patientId: string | null) {
  return useQuery({
    queryKey: [QUERY_KEYS.molecular, patientId],
    queryFn: async () => {
      if (!patientId) throw new Error('Patient ID required');
      const response = await apiClient.get<MolecularProfile>(
        `/api/patients/${patientId}/molecular`
      );
      return response.data;
    },
    enabled: !!patientId,
  });
}