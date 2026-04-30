import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { QUERY_KEYS } from '../config/constants';
import type { PatientsResponse } from '../types/patient';

export function usePatients() {
  return useQuery({
    queryKey: [QUERY_KEYS.patients],
    queryFn: async () => {
      const response = await apiClient.get<PatientsResponse>('/api/patients');
      return response.data;
    },
  });
}