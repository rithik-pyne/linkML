# Backend API - EGFR-NSCLC Clinical Decision Support

FastAPI REST API for EGFR-mutant NSCLC clinical data with evidence-based treatment recommendations.

## Quick Start

### 1. Activate Virtual Environment

```bash
# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Run the Server

```bash
uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: **http://localhost:8000**

### 4. Access API Documentation

FastAPI automatically generates interactive documentation:

- **Swagger UI**: http://localhost:8000/docs (interactive API testing)
- **ReDoc**: http://localhost:8000/redoc (alternative documentation)
- **OpenAPI JSON**: http://localhost:8000/openapi.json (schema)

## API Endpoints

### Health & Status
- `GET /` - Health check
- `GET /api/health` - API health status
- `GET /api/db/status` - Database connection status

### Patient Data
- `GET /api/patients` - List all patients
- `GET /api/patients/{patient_id}/summary` - Patient demographics and current status
- `GET /api/patients/{patient_id}/molecular` - Molecular profile with mutations
- `GET /api/patients/{patient_id}/imaging` - Imaging studies history
- `GET /api/patients/{patient_id}/treatments` - Treatment history
- `GET /api/patients/{patient_id}/response` - Response assessments (RECIST)
- `GET /api/patients/{patient_id}/clinical` - Clinical assessments (ECOG, labs)
- `GET /api/patients/{patient_id}/timeline` - Disease timeline (all events)
- `GET /api/patients/{patient_id}/decisions` - Treatment recommendations
- `GET /api/patients/{patient_id}/alerts` - Active clinical alerts

## Database

- **Type**: SQLite
- **Location**: `backend/clinical_data.db`
- **Tables**: 8 (Patient, ImagingStudy, Biopsy, MolecularTest, Mutation, Treatment, ResponseAssessment, ClinicalAssessment)
- **Rows**: 123 (5 patients with full longitudinal data)

## Test Suite

Run the automated test script:

```bash
bash backend/test_api.sh
```

This script tests all 12 endpoints with sample curl commands and validates responses.

## Technology Stack

- **FastAPI** 0.115+ - Modern web framework
- **Uvicorn** 0.32+ - ASGI server
- **Pydantic** 2.10+ - Data validation
- **SQLite** 3.45+ - Database
- **Python** 3.13+

## CORS Configuration

The API allows requests from:
- `http://localhost:3000` (React frontend)

Methods allowed: GET, POST, PUT, DELETE, OPTIONS

## Clinical Decision Rules

The API implements evidence-based treatment recommendations:

| Rule | Evidence Level | Reference |
|------|---------------|-----------|
| EGFR Ex19del/L858R + Stage IV → Osimertinib | Level I (RCT) | FLAURA (NEJM 2018) |
| T790M resistance → Osimertinib | Level I (RCT) | AURA3 (NEJM 2017) |
| MET amplification → Add MET inhibitor | Level II (Phase II) | GEOMETRY-E1 (2023) |
| C797S resistance → Chemotherapy | Level IV (Expert opinion) | ORCHARD (2024) |

## Alert Logic

The API generates alerts based on:

| Alert Type | Threshold | Evidence |
|-----------|-----------|----------|
| Rising ctDNA VAF | ≥2x from nadir | CHRYSALIS-2 trial |
| Overdue imaging | >84 days since last scan | Standard surveillance |
| Resistance mutations | Detected at progression | Clinical guidelines |

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app & CORS
│   ├── database.py          # SQLite connection
│   ├── api/
│   │   ├── patients.py      # Patient endpoints
│   │   ├── timeline.py      # Timeline aggregation
│   │   ├── decisions.py     # Clinical recommendations
│   │   └── alerts.py        # Alert generation
│   └── utils/
│       ├── clinical_rules.py # Decision rule engine
│       └── alerts.py         # Alert calculation logic
├── clinical_data.db         # SQLite database
├── requirements.txt         # Dependencies
└── README.md               # This file
```

## Development

### Run Tests

```bash
python -c "from backend.app.main import app; from fastapi.testclient import TestClient; client = TestClient(app); print('Test:', client.get('/api/patients').status_code == 200)"
```

### View Logs

Uvicorn outputs logs to stdout. Use `--log-level debug` for verbose logging:

```bash
uvicorn backend.app.main:app --reload --log-level debug
```

### Database Schema

To inspect the database:

```bash
sqlite3 backend/clinical_data.db
.tables
.schema Patient
```

## Troubleshooting

### Port Already in Use

If port 8000 is in use:

```bash
uvicorn backend.app.main:app --reload --port 8001
```

### Module Not Found

Ensure you're in the project root and venv is activated:

```bash
cd c:/dev/link_ml
source .venv/Scripts/activate  # or .venv\Scripts\activate on Windows
```

### Database Not Found

The database should be at `backend/clinical_data.db`. Check it exists:

```bash
ls backend/clinical_data.db
```

## Support

For issues, see the main project README or check:
- Swagger UI: http://localhost:8000/docs
- API spec: `02-backend-api.md`
- System spec: `00-system-spec.md`