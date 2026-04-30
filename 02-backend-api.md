# Backend API Specification v1.0

**Project**: EGFR-NSCLC Clinical Decision Support System  
**API Framework**: FastAPI  
**Data Models**: Auto-generated Pydantic classes from LinkML  
**Database**: SQLite (clinical_data.db)  
**Date**: 2026-04-24

---

## 1. Architecture

```
React Frontend (localhost:3000)
    ↓ HTTP GET
FastAPI Backend (localhost:8000)
    ↓ SQL Queries
SQLite Database (clinical_data.db)
```

**Data Flow**:
- LinkML schema → Pydantic models (auto-generated)
- FastAPI uses Pydantic for validation & serialization
- All endpoints return JSON validated against Pydantic models

**Pydantic Models**: `schemas/generated/python/clinical_model.py`
- Patient, Biopsy, ImagingStudy, MolecularTest, Mutation, Treatment, ResponseAssessment, ClinicalAssessment
- All enums (AJCCStageEnum, RECISTResponseEnum, etc.)

---

## 2. API Endpoints

### 2.1 Patient List

#### GET `/api/patients`

**Purpose**: List all patients for dropdown selector (Dashboard requirement)

**Response**: 200 OK
```json
{
  "patients": [
    {
      "patient_id": "NGDX-001",
      "age_at_diagnosis": 73,
      "sex": "Female",
      "diagnosis_date": "2020-03-23",
      "current_stage": "IVB",
      "current_treatment": "Osimertinib + Savolitinib",
      "treatment_line": 2
    }
  ],
  "total": 5
}
```

**Data Model**: Uses `Patient` Pydantic class + computed fields

**Database Query**: 
- SELECT from Patient table
- JOIN latest Treatment for current_treatment
- JOIN latest ImagingStudy for current_stage

---

### 2.2 Patient Summary Panel

#### GET `/api/patients/{patient_id}/summary`

**Purpose**: Demographics, baseline data, current status (Dashboard View #1)

**Response**: 200 OK
```json
{
  "patient_id": "NGDX-001",
  "nhs_number": "4000007963",
  "age_at_diagnosis": 73,
  "sex": "Female",
  "ethnicity_code": "A",
  "diagnosis_date": "2020-03-23",
  "diagnosis_pathway": "NG12 referral",
  "smoking_status": "Non-smoker - never smoked",
  "pack_years": 0.0,
  "family_history_lung_cancer": false,
  "ecog_baseline": 0,
  "baseline_egfr": 113.0,
  "baseline_wbc": 6.8,
  "baseline_hemoglobin": 132.0,
  "baseline_platelets": 245.0,
  "baseline_alt": 23.0,
  "baseline_ast": 28.0,
  "latest_ecog": 1,
  "latest_ecog_date": "2022-08-05",
  "current_stage": "IVB",
  "current_treatment": {
    "treatment_id": "TX-NGDX-001-003",
    "drug_name": "Osimertinib + Savolitinib",
    "treatment_line": 2,
    "treatment_start_date": "2022-08-10",
    "treatment_intent": "Palliative",
    "drug_dose_mg": 80.0,
    "drug_frequency": "OD"
  }
}
```

**Data Models**: 
- `Patient` (direct from LinkML)
- `Treatment` (nested, latest treatment)
- Computed: latest_ecog, current_stage

**Database Query**: Patient + latest Treatment + latest ClinicalAssessment + latest ImagingStudy

---

### 2.3 Molecular Profile

#### GET `/api/patients/{patient_id}/molecular`

**Purpose**: Mutations, PD-L1, actionable variants (Dashboard View #2)

**Response**: 200 OK
```json
{
  "patient_id": "NGDX-001",
  "primary_driver_mutation": {
    "mutation_id": "MUT-NGDX-001-001",
    "gene_symbol": "EGFR",
    "mutation_type": "Exon 19 deletion",
    "mutation_hgvs": "p.E746_A750del",
    "vaf_percent": 38.5,
    "tumor_fraction_percent": 40.0,
    "actionable_mutation": true,
    "is_primary_driver": true,
    "detection_timepoint": "Baseline",
    "test_date": "2020-03-14",
    "specimen_source": "Tissue",
    "ngs_panel_name": "FoundationOne CDx"
  },
  "co_mutations": [
    {
      "mutation_id": "MUT-NGDX-001-002",
      "gene_symbol": "TP53",
      "mutation_type": "R273H",
      "mutation_hgvs": "p.R273H",
      "vaf_percent": 42.0,
      "actionable_mutation": false,
      "detection_timepoint": "Baseline",
      "test_date": "2020-03-14"
    }
  ],
  "resistance_mutations": [
    {
      "mutation_id": "MUT-NGDX-001-005",
      "gene_symbol": "EGFR",
      "mutation_type": "T790M",
      "mutation_hgvs": "p.T790M",
      "vaf_percent": 8.2,
      "resistance_mutation": true,
      "is_acquired_resistance": true,
      "detection_timepoint": "Progression",
      "test_date": "2022-05-14",
      "specimen_source": "ctDNA",
      "ngs_panel_name": "Guardant360"
    },
    {
      "mutation_id": "MUT-NGDX-001-006",
      "gene_symbol": "MET",
      "mutation_type": "Amplification",
      "resistance_mutation": true,
      "is_acquired_resistance": true,
      "detection_timepoint": "Progression",
      "test_date": "2022-05-14"
    }
  ],
  "pdl1_status": {
    "tps_percent": 3,
    "antibody_clone": "22C3",
    "test_date": "2020-03-12"
  },
  "actionable_mutations_count": 3,
  "latest_ngs_test": {
    "molecular_test_id": "MOL-NGDX-001-002",
    "test_date": "2022-05-14",
    "specimen_source": "ctDNA",
    "ngs_panel_name": "Guardant360",
    "ngs_panel_version": "v2.0",
    "mean_coverage_depth": 11500.0
  }
}
```

**Data Models**: 
- `Mutation` (multiple, from LinkML)
- `MolecularTest` (from LinkML)
- `Biopsy` (for PD-L1)

**Database Query**: 
- Mutation JOIN MolecularTest WHERE patient_id
- Biopsy WHERE patient_id (for PD-L1)
- Filter by is_primary_driver, resistance_mutation flags

---

### 2.4 Disease Timeline

#### GET `/api/patients/{patient_id}/timeline`

**Purpose**: Integrated time-series for visualization (Dashboard View #3)

**Response**: 200 OK
```json
{
  "patient_id": "NGDX-001",
  "diagnosis_date": "2020-03-23",
  "timeline_events": [
    {
      "date": "2020-03-14",
      "event_type": "molecular_test",
      "description": "Tissue NGS - EGFR Ex19del detected (VAF 38.5%)",
      "data": {
        "molecular_test_id": "MOL-NGDX-001-001",
        "panel": "FoundationOne CDx",
        "mutations_detected": 2
      }
    },
    {
      "date": "2020-03-25",
      "event_type": "treatment_start",
      "description": "Surgery - Lobectomy",
      "data": {
        "treatment_id": "TX-NGDX-001-001",
        "treatment_line": 0,
        "treatment_intent": "Curative"
      }
    },
    {
      "date": "2020-04-15",
      "event_type": "treatment_start",
      "description": "Adjuvant Osimertinib 80mg OD",
      "data": {
        "treatment_id": "TX-NGDX-001-002",
        "treatment_line": 1,
        "treatment_intent": "Adjuvant"
      }
    },
    {
      "date": "2020-04-29",
      "event_type": "response_assessment",
      "description": "Post-surgery - Complete Response",
      "data": {
        "assessment_id": "RESP-NGDX-001-001",
        "recist_response": "CR",
        "tumor_diameter_mm": 0.0
      }
    },
    {
      "date": "2022-05-12",
      "event_type": "response_assessment",
      "description": "Progression - Progressive Disease",
      "data": {
        "assessment_id": "RESP-NGDX-001-004",
        "recist_response": "PD",
        "tumor_diameter_mm": 35.0,
        "progression_type": "Systemic_multi_site"
      }
    },
    {
      "date": "2022-05-14",
      "event_type": "molecular_test",
      "description": "ctDNA - T790M + MET amp resistance detected",
      "data": {
        "molecular_test_id": "MOL-NGDX-001-002",
        "panel": "Guardant360",
        "mutations_detected": 4
      }
    }
  ],
  "vaf_series": [
    {
      "date": "2020-03-14",
      "gene_symbol": "EGFR",
      "mutation_type": "Exon 19 deletion",
      "vaf_percent": 38.5,
      "specimen_source": "Tissue"
    },
    {
      "date": "2020-09-01",
      "gene_symbol": "EGFR",
      "mutation_type": "Exon 19 deletion",
      "vaf_percent": 0.08,
      "specimen_source": "ctDNA"
    },
    {
      "date": "2022-05-14",
      "gene_symbol": "EGFR",
      "mutation_type": "Exon 19 deletion",
      "vaf_percent": 12.4,
      "specimen_source": "ctDNA"
    },
    {
      "date": "2022-05-14",
      "gene_symbol": "EGFR",
      "mutation_type": "T790M",
      "vaf_percent": 8.2,
      "specimen_source": "ctDNA"
    }
  ],
  "recist_series": [
    {
      "date": "2020-03-30",
      "tumor_diameter_mm": 15.6,
      "ajcc_stage": "IA1",
      "imaging_modality": "CT",
      "recist_response": null
    },
    {
      "date": "2020-04-29",
      "tumor_diameter_mm": 0.0,
      "ajcc_stage": "CR",
      "imaging_modality": "CT",
      "recist_response": "CR"
    },
    {
      "date": "2020-09-28",
      "tumor_diameter_mm": 0.0,
      "ajcc_stage": "CR",
      "imaging_modality": "CT",
      "recist_response": "CR"
    },
    {
      "date": "2021-03-30",
      "tumor_diameter_mm": 0.0,
      "ajcc_stage": "CR",
      "imaging_modality": "PET",
      "recist_response": "CR"
    },
    {
      "date": "2022-08-05",
      "tumor_diameter_mm": 35.0,
      "ajcc_stage": "IVB",
      "imaging_modality": "PET",
      "recist_response": "PD"
    }
  ],
  "ecog_series": [
    {
      "date": "2020-03-23",
      "ecog_status": 0
    },
    {
      "date": "2020-04-29",
      "ecog_status": 0
    },
    {
      "date": "2022-08-05",
      "ecog_status": 1
    }
  ]
}
```

**Data Models**: All LinkML classes (ImagingStudy, MolecularTest, Mutation, Treatment, ResponseAssessment, ClinicalAssessment)

**Database Query**: 
- Union of events from all fact tables
- Sort by date ascending
- Aggregate VAF by (date, gene, mutation)
- Aggregate RECIST by (date, tumor_diameter)

---

### 2.5 Imaging History

#### GET `/api/patients/{patient_id}/imaging`

**Purpose**: All imaging studies with staging

**Response**: 200 OK (array of `ImagingStudy`)
```json
{
  "patient_id": "NGDX-001",
  "imaging_studies": [
    {
      "imaging_study_id": "IMG-NGDX-001-001",
      "scan_date": "2020-03-30",
      "imaging_modality": "CT",
      "study_description": "Chest CT with contrast",
      "t_stage": "T2a",
      "n_stage": "N0",
      "m_stage": "M0",
      "ajcc_stage": "IA1",
      "primary_tumor_diameter_mm": 15.6,
      "suv_max": 2.3,
      "brain_metastasis_present": false,
      "brain_lesion_count": null,
      "brain_largest_lesion_mm": null,
      "study_uid": "1.2.840.113619.2.xxx",
      "accession_number": "ACC-001",
      "dicom_file_path": "/imaging/NGDX-001/baseline/",
      "thumbnail_image_path": null
    }
  ],
  "total_scans": 5
}
```

**Data Model**: `ImagingStudy` (direct from LinkML)

**Database Query**: SELECT * FROM ImagingStudy WHERE patient_id ORDER BY scan_date

---

### 2.6 Treatment History

#### GET `/api/patients/{patient_id}/treatments`

**Purpose**: All treatment lines

**Response**: 200 OK (array of `Treatment`)
```json
{
  "patient_id": "NGDX-001",
  "treatments": [
    {
      "treatment_id": "TX-NGDX-001-001",
      "treatment_line": 0,
      "treatment_intent": "Curative",
      "drug_name": "Surgery - Lobectomy",
      "drug_dose_mg": null,
      "drug_frequency": null,
      "drug_route": null,
      "treatment_start_date": "2020-03-25",
      "treatment_end_date": "2020-03-25",
      "discontinuation_reason": null,
      "mdt_recommendation": "Surgical resection recommended",
      "mdt_date": "2020-03-23"
    },
    {
      "treatment_id": "TX-NGDX-001-002",
      "treatment_line": 1,
      "treatment_intent": "Adjuvant",
      "drug_name": "Osimertinib",
      "drug_dose_mg": 80.0,
      "drug_frequency": "OD",
      "drug_route": "Oral",
      "treatment_start_date": "2020-04-15",
      "treatment_end_date": "2022-05-08",
      "discontinuation_reason": "Progression",
      "prior_ici_exposure": false,
      "months_since_last_ici": null
    }
  ],
  "current_line": 2,
  "total_lines": 3
}
```

**Data Model**: `Treatment` (direct from LinkML)

**Database Query**: SELECT * FROM Treatment WHERE patient_id ORDER BY treatment_line

---

### 2.7 Response Assessments

#### GET `/api/patients/{patient_id}/response`

**Purpose**: All response assessments with RECIST + ctDNA

**Response**: 200 OK (array of `ResponseAssessment`)
```json
{
  "patient_id": "NGDX-001",
  "assessments": [
    {
      "assessment_id": "RESP-NGDX-001-001",
      "assessment_date": "2020-04-29",
      "assessment_type": "Post_surgery",
      "recist_response": "CR",
      "sum_target_lesions_mm": 0.0,
      "percent_change_from_baseline": -100.0,
      "new_lesions_present": false,
      "ctdna_vaf_percent": null,
      "ctdna_mutation_cleared": null,
      "ctdna_tumor_fraction_percent": null,
      "ecog_status": 0,
      "symptom_improvement": null,
      "progression_detected": false,
      "progression_type": null,
      "time_to_progression_months": null,
      "resistance_mutation_detected": false,
      "resistance_mechanism": null,
      "histologic_transformation": false,
      "treatment_id": "TX-NGDX-001-001",
      "imaging_study_id": "IMG-NGDX-001-002",
      "molecular_test_id": null
    },
    {
      "assessment_id": "RESP-NGDX-001-004",
      "assessment_date": "2022-08-05",
      "assessment_type": "Progression",
      "recist_response": "PD",
      "sum_target_lesions_mm": 35.0,
      "percent_change_from_baseline": 125.0,
      "new_lesions_present": true,
      "ctdna_vaf_percent": 12.4,
      "ctdna_mutation_cleared": false,
      "ctdna_tumor_fraction_percent": 15.0,
      "ecog_status": 1,
      "symptom_improvement": false,
      "progression_detected": true,
      "progression_type": "Systemic_multi_site",
      "time_to_progression_months": 28.0,
      "resistance_mutation_detected": true,
      "resistance_mechanism": "T790M + MET amplification",
      "histologic_transformation": false,
      "treatment_id": "TX-NGDX-001-002",
      "imaging_study_id": "IMG-NGDX-001-005",
      "molecular_test_id": "MOL-NGDX-001-002"
    }
  ],
  "total": 4
}
```

**Data Model**: `ResponseAssessment` (direct from LinkML)

**Database Query**: SELECT * FROM ResponseAssessment WHERE patient_id ORDER BY assessment_date

---

### 2.8 Clinical Assessments

#### GET `/api/patients/{patient_id}/clinical`

**Purpose**: Longitudinal ECOG, labs, symptoms

**Response**: 200 OK (array of `ClinicalAssessment`)
```json
{
  "patient_id": "NGDX-001",
  "assessments": [
    {
      "clinical_assessment_id": "CLIN-NGDX-001-001",
      "assessment_date": "2020-03-23",
      "visit_type": "Baseline",
      "ecog_status": 0,
      "symptoms_coded": null,
      "symptom_severity_grade": null,
      "wbc": 6.8,
      "hemoglobin": 132.0,
      "platelets": 245.0,
      "neutrophils": null,
      "egfr_value": 113.0,
      "alt": 23.0,
      "ast": 28.0
    }
  ],
  "total": 8,
  "latest_ecog": 1,
  "latest_labs": {
    "date": "2022-08-05",
    "wbc": 5.9,
    "hemoglobin": 118.0,
    "platelets": 220.0,
    "egfr_value": 95.0,
    "alt": 45.0,
    "ast": 38.0
  }
}
```

**Data Model**: `ClinicalAssessment` (direct from LinkML)

**Database Query**: SELECT * FROM ClinicalAssessment WHERE patient_id ORDER BY assessment_date

---

### 2.9 Treatment Decision Support

#### GET `/api/patients/{patient_id}/decisions`

**Purpose**: Clinical decision rules with evidence (Dashboard View #4)

**Response**: 200 OK
```json
{
  "patient_id": "NGDX-001",
  "current_treatment_line": 2,
  "current_stage": "IVB",
  "recommendations": [
    {
      "recommendation_id": "REC-MET-AMP",
      "recommendation": "Consider adding MET inhibitor (Tepotinib or Savolitinib) to Osimertinib",
      "rationale": "MET amplification detected as acquired resistance mechanism after progression on osimertinib",
      "evidence_level": "Level II (Phase II trial)",
      "guideline_reference": "GEOMETRY-E1 trial (Wu et al., Lancet Resp Med 2023)",
      "confidence": "Moderate",
      "applicable": true,
      "priority": "High",
      "supporting_data": {
        "mutations_detected": ["T790M", "MET amplification"],
        "current_treatment": "Osimertinib",
        "progression_type": "Systemic_multi_site",
        "pdl1_tps": 3
      }
    },
    {
      "recommendation_id": "REC-T790M",
      "recommendation": "Continue third-generation EGFR TKI with MET inhibitor combination",
      "rationale": "T790M co-exists with MET amplification - dual resistance mechanism requires combination therapy",
      "evidence_level": "Level II (Phase II trial)",
      "guideline_reference": "TATTON trial (Oxnard et al., JTO 2020)",
      "confidence": "Moderate",
      "applicable": true,
      "priority": "High",
      "supporting_data": {
        "t790m_vaf": 8.2,
        "met_amplification": true,
        "progression_confirmed": true
      }
    }
  ],
  "alerts": [
    {
      "alert_id": "ALR-RES-001",
      "alert_type": "resistance_mutation_detected",
      "severity": "High",
      "message": "New resistance mutations detected: T790M (VAF 8.2%), MET amplification",
      "trigger_date": "2022-05-14",
      "requires_action": true,
      "action_recommendation": "Re-biopsy performed. Consider combination MET + EGFR TKI therapy per GEOMETRY-E1/TATTON trials."
    },
    {
      "alert_id": "ALR-PROG-001",
      "alert_type": "progression_detected",
      "severity": "High",
      "message": "Radiographic progression detected (RECIST PD) - systemic multi-site",
      "trigger_date": "2022-08-05",
      "requires_action": true,
      "action_recommendation": "MDT discussion for next-line therapy. Molecular testing confirms dual resistance mechanism."
    }
  ]
}
```

**Data Models**: Custom Pydantic (references LinkML Mutation, Treatment, ResponseAssessment)

**Logic**: Implements clinical rules from system spec Section 6:
- EGFR Ex19del/L858R + Stage IV → Osimertinib (FLAURA)
- T790M on 1st/2nd-gen TKI → Switch to osimertinib (AURA3)
- C797S on osimertinib → No targeted therapy (ORCHARD)
- MET amplification → Add MET inhibitor (GEOMETRY-E1)

---

### 2.10 Active Alerts

#### GET `/api/patients/{patient_id}/alerts`

**Purpose**: Real-time clinical alerts (Dashboard View #5)

**Response**: 200 OK
```json
{
  "patient_id": "NGDX-001",
  "alerts": [
    {
      "alert_id": "ALR-VAF-001",
      "alert_type": "rising_ctdna_vaf",
      "severity": "High",
      "message": "ctDNA VAF increased 155x from nadir (0.08% → 12.4%)",
      "trigger_date": "2022-05-14",
      "requires_action": true,
      "action_recommendation": "Molecular progression detected. Consider repeat imaging (CHRYSALIS-2 precedent: VAF rise precedes radiographic progression by ~4 months).",
      "supporting_data": {
        "nadir_vaf": 0.08,
        "nadir_date": "2020-09-01",
        "current_vaf": 12.4,
        "current_date": "2022-05-14",
        "fold_change": 155.0,
        "threshold": 2.0
      }
    },
    {
      "alert_id": "ALR-RES-002",
      "alert_type": "resistance_mutation",
      "severity": "High",
      "message": "Acquired resistance mutations detected: T790M (EGFR), MET amplification",
      "trigger_date": "2022-05-14",
      "requires_action": true,
      "action_recommendation": "Dual resistance mechanism identified. Consider osimertinib + MET inhibitor combination per GEOMETRY-E1 or TATTON protocols.",
      "supporting_data": {
        "resistance_mutations": [
          {"gene": "EGFR", "mutation": "T790M", "vaf_percent": 8.2},
          {"gene": "MET", "mutation": "Amplification", "vaf_percent": null}
        ],
        "detection_timepoint": "Progression",
        "specimen_source": "ctDNA"
      }
    }
  ],
  "overdue_tests": [],
  "total_active_alerts": 2
}
```

**Data Models**: Custom Pydantic (references LinkML Mutation, MolecularTest)

**Alert Logic**:
- **Rising VAF**: Current VAF ≥ 2x nadir VAF (CHRYSALIS-2 threshold)
- **Resistance mutation**: `resistance_mutation=TRUE` in Mutation table
- **Overdue imaging**: Days since last scan > 84 days (12 weeks)

---

## 3. Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API Framework** | FastAPI 0.115+ | REST API with auto docs |
| **Server** | Uvicorn 0.32+ | ASGI server |
| **Validation** | Pydantic 2.10+ | Auto-generated from LinkML |
| **Database** | SQLite 3.45+ | clinical_data.db |
| **CORS** | FastAPI middleware | Allow localhost:3000 |

---

## 4. Configuration

**Base URL**: `http://localhost:8000`  
**API Prefix**: `/api`  
**Docs**: `http://localhost:8000/docs` (Swagger UI)  
**CORS**: Allow origin `http://localhost:3000`  
**Methods**: GET only (read-only MVP)

---

## 5. Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app, CORS, routes
│   ├── database.py             # SQLite connection
│   ├── schemas.py              # Custom response models
│   ├── api/
│   │   ├── __init__.py
│   │   ├── patients.py         # Patient endpoints
│   │   ├── timeline.py         # Timeline aggregation
│   │   ├── decisions.py        # Clinical decision support
│   │   └── alerts.py           # Alert generation
│   └── utils/
│       ├── __init__.py
│       ├── clinical_rules.py   # Decision rule engine
│       ├── alerts.py           # Alert engine
│       └── queries.py          # Reusable SQL queries
├── clinical_data.db            # SQLite database
└── requirements.txt
```

---

## 6. Error Responses

**404 Not Found**:
```json
{
  "detail": "Patient NGDX-999 not found"
}
```

**500 Internal Server Error**:
```json
{
  "detail": "Database query failed"
}
```

---

## 7. Implementation Phases

### Phase 1: Setup (30 min)
- Create backend/ structure
- requirements.txt: fastapi, uvicorn, pydantic
- Test server starts

### Phase 2: Core Endpoints (3 hours)
- GET /api/patients
- GET /api/patients/{patient_id}/summary
- GET /api/patients/{patient_id}/molecular
- GET /api/patients/{patient_id}/imaging
- GET /api/patients/{patient_id}/treatments
- GET /api/patients/{patient_id}/response
- GET /api/patients/{patient_id}/clinical

### Phase 3: Timeline (2 hours)
- GET /api/patients/{patient_id}/timeline
- Aggregate events from all tables
- Format for charting (VAF series, RECIST series)

### Phase 4: Decision Support (3 hours)
- GET /api/patients/{patient_id}/decisions
- Implement clinical rules from system spec Section 6
- Add evidence levels and references

### Phase 5: Alerts (2 hours)
- GET /api/patients/{patient_id}/alerts
- VAF trending logic
- Resistance mutation detection
- Overdue test checks

**Total**: ~10-11 hours

---

## 8. Success Criteria

✅ All 10 endpoints return valid JSON  
✅ Pydantic validation passes  
✅ Timeline aggregates correctly  
✅ Clinical rules trigger for NGDX-001  
✅ Alerts detect rising VAF + resistance  
✅ Swagger docs complete  
✅ CORS allows React connection  

---

## Next Steps

Create concise implementation checklist → `NEXT_STEPS.md`