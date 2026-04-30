// Use relative URL to leverage Vite proxy and avoid CORS issues
// In production, set VITE_API_BASE_URL environment variable
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export const COLORS = {
  cpi: {
    blue: '#0058AA',
    navy: '#001d38',
    red: '#d3353d',
    orange: '#ff9200',
    teal: '#007169',
  },
  severity: {
    critical: '#d3353d',
    high: '#ff9200',
    medium: '#0072dd',
    low: '#007169',
  },
  evidence: {
    levelI: '#007169',    // Teal - Level I (RCT)
    levelII: '#0072dd',   // Blue - Level II (Phase II)
    levelIII: '#ff9200',  // Orange - Level III (Retrospective)
    levelIV: '#d1d5db',   // Gray - Level IV (Expert opinion)
  },
} as const;

export const QUERY_KEYS = {
  patients: 'patients',
  patientSummary: 'patient-summary',
  molecular: 'molecular-profile',
  timeline: 'timeline',
  decisions: 'decisions',
  alerts: 'alerts',
} as const;