# EGFR-NSCLC Clinical Decision Support Dashboard

A demonstration clinical decision support system for EGFR-mutated non-small cell lung cancer (NSCLC) patients.

## ⚠️ Important Disclaimer

**FOR DEMONSTRATION PURPOSES ONLY**

This system is a simplified proof-of-concept implementation. It is **NOT validated for clinical use** and must **NOT be used for real patient care decisions**. All treatment recommendations should be made by qualified oncologists following current evidence-based guidelines.

## Project Overview

This repository contains:
- **Backend API**: FastAPI-based REST API serving clinical data
- **Frontend Dashboard**: React/TypeScript dashboard for data visualization
- **Sample Data**: 5 synthetic patient cases with complete clinical histories

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- npm 9+

### Backend Setup

```bash
# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r backend/requirements.txt

# Start backend server
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

Frontend will be available at: http://localhost:5173

## Features

### Dashboard Components
- **Patient Selector**: Choose from 5 sample patients
- **Patient Summary**: Demographics, baseline labs, current status
- **Molecular Profile**: Driver mutations, resistance mutations, PD-L1 status
- **Disease Timeline**: VAF trends, tumor diameter, clinical events
- **Treatment Recommendations**: Evidence-based suggestions
- **Alert Panel**: Critical clinical alerts

### Technology Stack
- **Backend**: FastAPI, SQLite, Pydantic
- **Frontend**: React 18, TypeScript, Vite, TanStack Query, Recharts
- **Styling**: Tailwind CSS 4 with CPI brand colors

## Documentation

- **[00-SYSTEM-SPEC.md](00-SYSTEM-SPEC.md)**: System architecture and clinical context
- **[02-backend-api.md](02-backend-api.md)**: API endpoint documentation
- **[DATABASE_COMPLETE.md](DATABASE_COMPLETE.md)**: Database schema
- **[CPI_BRAND_GUIDELINES.md](CPI_BRAND_GUIDELINES.md)**: UI/UX branding guidelines
- **[FRONTEND_IMPLEMENTATION_GUIDE.md](FRONTEND_IMPLEMENTATION_GUIDE.md)**: Complete frontend implementation guide
- **[frontend/README.md](frontend/README.md)**: Frontend-specific documentation

## Project Structure

```
link_ml/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── api/                 # API endpoints
│   │   └── utils/               # Helper functions
│   ├── clinical_data.db         # SQLite database (5 patients)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── hooks/               # Custom React hooks
│   │   ├── types/               # TypeScript definitions
│   │   └── api/                 # API client
│   ├── package.json
│   └── README.md
└── README.md                    # This file
```

## Sample Patients

- **NGDX-001**: 73yo Female, Stage IVB (Complex case with resistance mutations)
- **NGDX-002**: 69yo Female, Stage CR
- **NGDX-003**: 62yo Male, Stage CR (Surgical resection)
- **NGDX-004**: 69yo Male, Stage CR (Early stage)
- **NGDX-005**: 79yo Male, Stage CR

## API Endpoints

```
GET  /api/patients                      # List all patients
GET  /api/patients/{id}/summary         # Patient demographics
GET  /api/patients/{id}/molecular       # Molecular profile
GET  /api/patients/{id}/timeline        # Disease timeline
GET  /api/patients/{id}/decisions       # Treatment recommendations
GET  /api/patients/{id}/alerts          # Clinical alerts
```

## Development

### Backend
```bash
# Run with auto-reload
uvicorn backend.app.main:app --reload

# Access API docs
http://localhost:8000/docs
```

### Frontend
```bash
cd frontend
npm run dev          # Development server
npm run build        # Production build
npm run preview      # Preview production build
```

## Testing

All 5 patients have been tested with:
- Complete clinical data
- Molecular profiles
- Timeline data (VAF + RECIST)
- Treatment recommendations
- Clinical alerts

## Known Limitations

- Demo system with 5 synthetic patients only
- Read-only (no data editing)
- No authentication/authorization
- Not validated for clinical use
- Requires both backend and frontend running locally

## License

Educational/demonstration purposes only.

## Support

For questions or issues, refer to the documentation files in this repository.
