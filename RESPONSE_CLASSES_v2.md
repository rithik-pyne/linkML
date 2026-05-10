# Response Classes v2.0 - Documentation

## Overview

The ResponseAssessment table has been refactored into three specialized response classes in LinkML schema v2.0.0. This document describes the new classes and their usage.

---

## ImagingResponse

**Purpose**: Track radiographic treatment response using RECIST criteria.

**Grain**: One row per imaging study with documented radiologist assessment.

### Schema Definition

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `imaging_response_id` | string | Yes | Primary key (format: IR-XXX-XXX) |
| `imaging_study_id` | string | Yes | FK to ImagingStudy (source lineage) |
| `patient_id` | string | Yes | FK to Patient (conformed dimension) |
| `treatment_id` | string | No | FK to Treatment (nullable for baseline) |
| `assessment_date` | date | Yes | Date of radiologist assessment |
| `assessment_type` | enum | Yes | Baseline/Follow_up/Progression |
| `recist_response` | enum | No | CR/PR/SD/PD |
| `sum_target_lesions_mm` | float | No | RECIST sum of target lesion diameters |
| `percent_change_from_baseline` | float | No | Percent change from treatment baseline |
| `new_lesions_present` | boolean | No | Indicator for new lesions (RECIST PD) |

### SQL Schema
```sql
CREATE TABLE "ImagingResponse" (
    imaging_response_id TEXT NOT NULL PRIMARY KEY,
    imaging_study_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    treatment_id TEXT,
    assessment_date DATE NOT NULL,
    assessment_type VARCHAR(11) NOT NULL,
    recist_response VARCHAR(2),
    sum_target_lesions_mm FLOAT,
    percent_change_from_baseline FLOAT,
    new_lesions_present BOOLEAN,
    FOREIGN KEY(imaging_study_id) REFERENCES ImagingStudy(imaging_study_id),
    FOREIGN KEY(patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY(treatment_id) REFERENCES Treatment(treatment_id)
);
```

### Usage Example
```python
from clinical_model_pydantic_v2 import ImagingResponse

imaging_response = ImagingResponse(
    imaging_response_id="IR-001-001",
    imaging_study_id="IMG-001-001",
    patient_id="NGDX-001",
    treatment_id="TRT-001-001",
    assessment_date="2024-06-15",
    assessment_type="Follow_up",
    recist_response="PR",
    sum_target_lesions_mm=28.5,
    percent_change_from_baseline=-35.2,
    new_lesions_present=False
)
```

### Query Pattern
```sql
-- Get RECIST response timeline for a patient
SELECT 
    ir.assessment_date,
    ir.recist_response,
    ir.sum_target_lesions_mm,
    ir.percent_change_from_baseline,
    i.imaging_modality,
    i.ajcc_stage
FROM ImagingResponse ir
JOIN ImagingStudy i ON ir.imaging_study_id = i.imaging_study_id
WHERE ir.patient_id = 'NGDX-001'
ORDER BY ir.assessment_date;
```

---

## MolecularResponse

**Purpose**: Track molecular treatment response via serial ctDNA monitoring and VAF trends.

**Grain**: One row per molecular test with documented ctDNA response assessment.

### Schema Definition

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `molecular_response_id` | string | Yes | Primary key (format: MR-XXX-XXX) |
| `molecular_test_id` | string | Yes | FK to MolecularTest (source lineage) |
| `patient_id` | string | Yes | FK to Patient (conformed dimension) |
| `treatment_id` | string | No | FK to Treatment (nullable for baseline) |
| `assessment_date` | date | Yes | Date of molecular assessment |
| `assessment_type` | enum | Yes | Baseline/Follow_up/Progression |
| `ctdna_vaf_percent` | float | No | Variant allele frequency (%) |
| `ctdna_tumor_fraction_percent` | float | No | Tumor fraction estimate (%) |
| `ctdna_mutation_cleared` | boolean | No | Driver mutation clearance flag |

### SQL Schema
```sql
CREATE TABLE "MolecularResponse" (
    molecular_response_id TEXT NOT NULL PRIMARY KEY,
    molecular_test_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    treatment_id TEXT,
    assessment_date DATE NOT NULL,
    assessment_type VARCHAR(11) NOT NULL,
    ctdna_vaf_percent FLOAT,
    ctdna_tumor_fraction_percent FLOAT,
    ctdna_mutation_cleared BOOLEAN,
    FOREIGN KEY(molecular_test_id) REFERENCES MolecularTest(molecular_test_id),
    FOREIGN KEY(patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY(treatment_id) REFERENCES Treatment(treatment_id)
);
```

### Usage Example
```python
from clinical_model_pydantic_v2 import MolecularResponse

molecular_response = MolecularResponse(
    molecular_response_id="MR-001-001",
    molecular_test_id="MOL-001-002",
    patient_id="NGDX-001",
    treatment_id="TRT-001-001",
    assessment_date="2024-06-20",
    assessment_type="Follow_up",
    ctdna_vaf_percent=0.08,
    ctdna_tumor_fraction_percent=0.15,
    ctdna_mutation_cleared=False
)
```

### Query Pattern
```sql
-- Get ctDNA VAF trend for primary EGFR mutation
SELECT 
    mr.assessment_date,
    mr.ctdna_vaf_percent,
    mr.ctdna_mutation_cleared,
    mt.specimen_source,
    m.mutation_type
FROM MolecularResponse mr
JOIN MolecularTest mt ON mr.molecular_test_id = mt.molecular_test_id
JOIN Mutation m ON m.molecular_test_id = mt.molecular_test_id
WHERE mr.patient_id = 'NGDX-001'
  AND m.is_primary_driver = 1
ORDER BY mr.assessment_date;
```

---

## ClinicalResponse

**Purpose**: Document clinical outcome events (progression, resistance, histologic transformation) as determined by MDT consensus.

**Grain**: One row per clinical outcome event.

### Schema Definition

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `clinical_response_id` | string | Yes | Primary key (format: CR-XXX-XXX) |
| `patient_id` | string | Yes | FK to Patient (conformed dimension) |
| `treatment_id` | string | No | FK to Treatment (may be post-treatment) |
| `event_date` | date | Yes | Date event was documented/detected |
| `event_type` | enum | Yes | Progression/Resistance/Transformation |
| `progression_detected` | boolean | Yes | Progression flag |
| `progression_type` | enum | No | Oligoprogression/Systemic/CNS_only/Asymptomatic |
| `time_to_progression_months` | float | No | TTP from treatment start |
| `resistance_mutation_detected` | boolean | No | Resistance mutation flag |
| `resistance_mechanism` | string | No | Free-text mechanism description |
| `histologic_transformation` | boolean | No | SCLC transformation flag |

### SQL Schema
```sql
CREATE TABLE "ClinicalResponse" (
    clinical_response_id TEXT NOT NULL PRIMARY KEY,
    patient_id TEXT NOT NULL,
    treatment_id TEXT,
    event_date DATE NOT NULL,
    event_type VARCHAR(15) NOT NULL,
    progression_detected BOOLEAN NOT NULL,
    progression_type VARCHAR(19),
    time_to_progression_months FLOAT,
    resistance_mutation_detected BOOLEAN,
    resistance_mechanism TEXT,
    histologic_transformation BOOLEAN,
    FOREIGN KEY(patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY(treatment_id) REFERENCES Treatment(treatment_id)
);
```

### ClinicalEventTypeEnum
- `Progression` - Disease progression event
- `Resistance` - Resistance mechanism detected
- `Transformation` - Histologic transformation (e.g., SCLC)

### Usage Example
```python
from clinical_model_pydantic_v2 import ClinicalResponse

clinical_response = ClinicalResponse(
    clinical_response_id="CR-001-001",
    patient_id="NGDX-001",
    treatment_id="TRT-001-001",
    event_date="2024-12-15",
    event_type="Resistance",
    progression_detected=True,
    progression_type="Systemic_multi_site",
    time_to_progression_months=26.5,
    resistance_mutation_detected=True,
    resistance_mechanism="T790M + MET amplification",
    histologic_transformation=False
)
```

### Query Pattern
```sql
-- Get all clinical events for a patient with treatment context
SELECT 
    cr.event_date,
    cr.event_type,
    cr.progression_type,
    cr.resistance_mechanism,
    cr.time_to_progression_months,
    t.drug_name,
    t.treatment_line
FROM ClinicalResponse cr
LEFT JOIN Treatment t ON cr.treatment_id = t.treatment_id
WHERE cr.patient_id = 'NGDX-001'
ORDER BY cr.event_date;
```

---

## Query Patterns

### Anti-Pattern: Direct Fact-to-Fact JOIN ❌
```sql
-- DON'T DO THIS - fragile if dates don't match exactly
SELECT 
    ir.recist_response,
    mr.ctdna_vaf_percent
FROM ImagingResponse ir
JOIN MolecularResponse mr 
    ON mr.patient_id = ir.patient_id
    AND mr.assessment_date = ir.assessment_date  -- FRAGILE!
WHERE ir.patient_id = 'NGDX-001';
```

### Recommended: Drill-Across via Shared Dimension ✅
```sql
-- Separate queries, merged in application layer
-- Query 1: Imaging responses
SELECT 
    assessment_date AS date,
    recist_response,
    'imaging' AS source
FROM ImagingResponse
WHERE patient_id = 'NGDX-001';

-- Query 2: Molecular responses (separate query)
SELECT 
    assessment_date AS date,
    ctdna_vaf_percent,
    'molecular' AS source
FROM MolecularResponse
WHERE patient_id = 'NGDX-001';

-- Merge in application with fuzzy date matching (±7 days)
```

---

## Migration Notes

- **Old table**: `ResponseAssessment` (deprecated)
- **New tables**: `ImagingResponse`, `MolecularResponse`, `ClinicalResponse`
- **Migration script**: `scripts/migrate_response_tables.py`
- **Migration guide**: `MIGRATION_GUIDE.md`

### Data Splitting Rules

During migration, ResponseAssessment rows are split based on content:

1. Rows with `imaging_study_id` + RECIST data → **ImagingResponse**
2. Rows with `molecular_test_id` + ctDNA data → **MolecularResponse**
3. Rows with progression/resistance flags → **ClinicalResponse**

**Note**: Rows with multiple data types appear in multiple new tables (expected behavior).

---

## References

- **LinkML Schema**: `schemas/clinical_model.yaml` v2.0.0
- **SQL DDL**: `schemas/generated/sql/clinical_model_v2.sql`
- **Python Models**: `schemas/generated/python/clinical_model_pydantic_v2.py`
- **ER Diagram**: `schemas/generated/diagrams/er_diagram_v2.mmd`
- **Changelog**: `LINKML_SCHEMA_CHANGELOG.md`

---

**Generated**: 2026-04-30  
**Schema Version**: 2.0.0  
**Status**: Ready for migration