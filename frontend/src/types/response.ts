// Response assessment types for new schema (v2.0.0)

export interface ImagingResponse {
  imaging_response_id: string;
  imaging_study_id: string;
  patient_id: string;
  treatment_id: string | null;
  assessment_date: string;
  assessment_type: 'Baseline' | 'Follow_up' | null;
  recist_response: 'CR' | 'PR' | 'SD' | 'PD' | null;
  sum_target_lesions_mm: number | null;
  percent_change_from_baseline: number | null;
  new_lesions_present: boolean | null;
}

export interface MolecularResponse {
  molecular_response_id: string;
  molecular_test_id: string;
  patient_id: string;
  treatment_id: string | null;
  assessment_date: string;
  assessment_type: 'Baseline' | 'Follow_up' | null;
  ctdna_vaf_percent: number | null;
  ctdna_tumor_fraction_percent: number | null;
  ctdna_mutation_cleared: boolean | null;
}

export interface ClinicalResponse {
  clinical_response_id: string;
  patient_id: string;
  treatment_id: string | null;
  event_date: string;
  event_type: 'Progression' | 'Resistance' | 'Transformation';
  progression_detected: boolean;
  progression_type: 'Local' | 'Distant' | 'CNS' | 'Metabolic' | null;
  time_to_progression_months: number | null;
  resistance_mutation_detected: boolean | null;
  resistance_mechanism: string | null;
  histologic_transformation: boolean | null;
}

// Response from GET /api/patients/{patient_id}/response
export interface PatientResponseData {
  patient_id: string;
  imaging_responses: ImagingResponse[];
  molecular_responses: MolecularResponse[];
  clinical_responses: ClinicalResponse[];
  total_imaging: number;
  total_molecular: number;
  total_clinical: number;
}