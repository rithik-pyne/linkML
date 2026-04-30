// Basic patient info for list view
export interface Patient {
  patient_id: string;
  age_at_diagnosis: number;
  sex: string;
  diagnosis_date: string;
  current_stage: string;
  current_treatment: string;
  treatment_line: number;
}

// Response from GET /api/patients
export interface PatientsResponse {
  patients: Patient[];
  total: number;
}

// Treatment info
export interface Treatment {
  treatment_id: string;
  drug_name: string;
  treatment_line: number;
  treatment_start_date: string;
  treatment_end_date?: string;
  treatment_intent: string;
  drug_dose_mg?: number;
  drug_frequency?: string;
  drug_route?: string;
}

// Detailed patient summary from GET /api/patients/{id}/summary
export interface PatientSummary {
  patient_id: string;
  nhs_number: string;
  age_at_diagnosis: number;
  sex: string;
  ethnicity_code: string;
  diagnosis_date: string;
  diagnosis_pathway: string;
  smoking_status: string;
  pack_years: number;
  family_history_lung_cancer: boolean;
  ecog_baseline: number;
  baseline_egfr: number;
  baseline_wbc: number;
  baseline_hemoglobin: number;
  baseline_platelets: number;
  baseline_alt: number;
  baseline_ast: number;
  latest_ecog: number;
  latest_ecog_date: string;
  current_stage: string;
  current_treatment: Treatment;
}