# EGFR-NSCLC Clinical Dashboard

React dashboard for displaying patient clinical data, molecular profiles, disease timelines, and treatment recommendations.

## Quick Start

### Prerequisites
- Node.js 18+
- npm 9+
- Backend API running on http://localhost:8000

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

Dashboard will be available at: http://localhost:5173

### Build for Production

```bash
npm run build
```

Built files will be in `dist/` directory.

## Features

- **Patient Selection**: Dropdown to select from 5 patients
- **Patient Summary**: Demographics, baseline labs, current status (3-column layout)
- **Molecular Profile**: Driver mutations, resistance mutations, co-mutations, PD-L1 status
- **Disease Timeline**: VAF trends + tumor diameter over time (Recharts)
- **Treatment Recommendations**: Evidence-based clinical decision rules
- **Alert Panel**: Active clinical alerts (rising VAF, resistance mutations)

## Technology Stack

- **React** 18.3
- **TypeScript** 5.5
- **Vite** 5.4
- **TanStack Query** 5.x (data fetching)
- **Recharts** 2.12 (charts)
- **Tailwind CSS** 3.4 (styling)
- **Lucide React** (icons)

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/          # Header, Footer, DisclaimerBanner
│   │   ├── patient/         # PatientSelector, PatientSummary, MolecularProfile
│   │   ├── timeline/        # DiseaseTimeline
│   │   ├── decisions/       # TreatmentRecommendations
│   │   ├── alerts/          # AlertPanel
│   │   ├── common/          # Card, Badge, LoadingSpinner, ErrorMessage, DataRow
│   │   └── ui/              # (future reusable UI components)
│   ├── hooks/               # usePatients, usePatientSummary, useMolecularProfile, useTimeline, useDecisions, useAlerts
│   ├── types/               # TypeScript type definitions
│   ├── api/                 # API client (Axios)
│   ├── config/              # Constants (API URL, colors)
│   ├── App.tsx              # Main dashboard layout
│   └── main.tsx             # Entry point with React Query provider
├── public/
│   └── assets/
│       └── cpi-logo.png     # CPI logo
├── tailwind.config.js       # CPI color palette
├── package.json
└── README.md
```

## API Endpoints Used

- `GET /api/patients` - List all patients
- `GET /api/patients/{id}/summary` - Patient demographics
- `GET /api/patients/{id}/molecular` - Molecular profile
- `GET /api/patients/{id}/timeline` - Timeline data
- `GET /api/patients/{id}/decisions` - Treatment recommendations
- `GET /api/patients/{id}/alerts` - Active alerts

## CPI Branding

Colors:
- Primary Blue: #0058AA
- Navy (header): #001d38
- Red (alerts): #d3353d
- Orange (warnings): #ff9200
- Teal (success): #007169

## Testing

Tested with:
- 5 patients (NGDX-001 to NGDX-005)
- All browsers (Chrome, Firefox, Safari, Edge)
- Responsive design (desktop, tablet, mobile)
- Accessibility (keyboard navigation, WCAG AA)

## Known Limitations

- Demonstration system only - NOT for clinical use
- Read-only (no data editing)
- 5 sample patients only
- Requires backend API to be running

## Support

For issues or questions, refer to:
- System Spec: `00-SYSTEM-SPEC.md`
- Backend API Spec: `02-backend-api.md`
- CPI Branding: `CPI_BRAND_GUIDELINES.md`
