import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';
import { QUERY_KEYS } from '../config/constants';

export interface ImagingStudy {
  imaging_study_id: string;
  patient_id: string;
  scan_date: string;
  imaging_modality: string;
  study_description: string;
  t_stage: string;
  n_stage: string;
  m_stage: string;
  ajcc_stage: string;
  primary_tumor_diameter_mm: number | null;
  suv_max: number | null;
  brain_metastasis_present: boolean;
  brain_lesion_count: number | null;
  brain_largest_lesion_mm: number | null;
  study_uid: string;
  accession_number: string;
  dicom_file_path: string | null;
  thumbnail_image_path: string | null;
}

export interface ImagingResponse {
  patient_id: string;
  imaging_studies: ImagingStudy[];
  total_scans: number;
}

export const useImagingStudies = (patientId: string | null) => {
  return useQuery<ImagingResponse>({
    queryKey: [QUERY_KEYS.patients, patientId, 'imaging'],
    queryFn: async () => {
      const response = await apiClient.get(`/api/patients/${patientId}/imaging`);
      return response.data;
    },
    enabled: !!patientId,
  });
};