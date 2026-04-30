export interface Recommendation {
  recommendation_id: string;
  recommendation: string;
  rationale: string;
  evidence_level: string;
  guideline_reference: string;
  confidence: 'High' | 'Moderate' | 'Low';
  applicable: boolean;
  priority: 'Urgent' | 'High' | 'Medium' | 'Low';
  supporting_data: Record<string, any>;
}

export interface Alert {
  alert_id: string;
  alert_type: string;
  severity: 'Critical' | 'High' | 'Medium' | 'Low';
  message: string;
  trigger_date: string;
  requires_action: boolean;
  action_recommendation: string;
  supporting_data?: Record<string, any>;
}

export interface DecisionsResponse {
  patient_id: string;
  current_treatment_line: number;
  current_stage: string;
  recommendations: Recommendation[];
  alerts: Alert[];
}