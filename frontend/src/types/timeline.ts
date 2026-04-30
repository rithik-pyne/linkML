export interface TimelineEvent {
  date: string;
  event_type: 'molecular_test' | 'treatment_start' | 'treatment_end' | 'response_assessment' | 'imaging' | 'clinical_assessment';
  description: string;
  data: Record<string, any>;
}

export interface VAFDataPoint {
  date: string;
  gene_symbol: string;
  mutation_type: string;
  vaf_percent: number;
  specimen_source: string;
}

export interface RECISTDataPoint {
  date: string;
  tumor_diameter_mm: number;
  ajcc_stage: string;
  imaging_modality: string;
  recist_response: string | null;
}

export interface ECOGDataPoint {
  date: string;
  ecog_status: number;
}

export interface Timeline {
  patient_id: string;
  diagnosis_date: string;
  timeline_events: TimelineEvent[];
  vaf_series: VAFDataPoint[];
  recist_series: RECISTDataPoint[];
  ecog_series: ECOGDataPoint[];
}