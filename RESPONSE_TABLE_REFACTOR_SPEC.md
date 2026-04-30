# Technical Specification: ResponseAssessment Table Refactoring
## EGFR-NSCLC Clinical Decision Support System Data Model v2.0

---

## Executive Summary

### Problem Statement
The current `ResponseAssessment` table is a **polymorphic fact table** that conflates three distinct clinical processes:
1. **Imaging-based response** (RECIST measurements from ImagingStudy)
2. **Molecular response** (ctDNA/VAF tracking from MolecularTest)  
3. **Clinical outcomes** (progression events, resistance mechanisms)

This design creates:
- **Ambiguous grain**: A single row may represent imaging data, molecular data, or both
- **Sparse columns**: Most rows have NULL values in 50%+ of columns
- **Fragile FKs**: Optional links to imaging_study_id, molecular_test_id, and treatment_id make lineage unclear
- **Complex queries**: Extracting time-series for a single modality requires filtering NULLs

### Solution
Refactor into **three purpose-built fact tables** with explicit grain and lineage:
- `fact_imaging_response` (grain: one row per imaging study assessment)
- `fact_molecular_response` (grain: one row per molecular test assessment)
- `fact_clinical_response` (grain: one row per clinical outcome event)

**Benefits:**
- Clear source lineage (required FKs to source tables)
- Dense columns (no NULL-heavy polymorphism)
- Simpler queries (direct JOINs to source facts)
- Better LinkML semantics (explicit relationships vs optional fields)

---

## 1. Assumptions

### Data Characteristics
1. **Append-only ingestion** from flat CSV files - no updates or deletes
2. **Sparse cross-modality assessments**: Not every treatment cycle has both imaging AND molecular tests
3. **Progression events** may occur without a same-day imaging/molecular test
4. **Treatment context is optional**: Some assessments (e.g., baseline scans) occur before treatment starts
5. **Data volume**: 5-50 patients, ~200-500 rows per fact table (SQLite-scale, not enterprise)

### Workflow Assumptions
1. **Imaging response** workflow: ImagingStudy → radiologist reads → ResponseAssessment with RECIST
2. **Molecular response** workflow: MolecularTest → bioinformatics pipeline → ctDNA VAF trends
3. **Clinical response** workflow: MDT meeting → progression declared → resistance mechanism documented

### Technical Constraints
1. SQLite 3.x (no window functions pre-3.25, limited optimizer)
2. LinkML 1.x with SQL DDL generator
3. Python 3.10+ for ETL scripts
4. No ORMs - direct SQL queries in FastAPI backend

---

## 2. Design Principles

### Dimensional Modeling Principles (Kimball-style)
1. **Explicit grain**: Every fact table has ONE clearly defined grain statement
2. **Conformed dimensions**: Patient, Treatment, and Date dimensions shared across all facts
3. **Source lineage**: Every response fact links to its originating source fact (imaging_study_id, molecular_test_id)
4. **Denormalized for queries**: Include patient_id directly in fact tables (even though derivable)
5. **Drill-across, not fact-joins**: Compare imaging vs molecular response via shared Patient/Treatment dimensions, NOT direct fact-to-fact joins

### LinkML Modeling Principles
1. **Identifier as scalar slot**: `patient_id: string` with `identifier: true`
2. **Relationships as class-valued slots**: `patient: Patient` (range: Patient)
3. **Required FKs for source lineage**: `imaging_study_id` required in `fact_imaging_response`
4. **Optional FKs for context**: `treatment_id` nullable (baseline assessments pre-date treatment)
5. **No parent-side multivalued collections**: Avoid `Patient.treatments: list[Treatment]` in SQL schema generation

### SQL Anti-Patterns to Avoid
❌ **No fact-to-fact JOINs in production queries** (e.g., `fact_imaging_response JOIN fact_molecular_response ON date`)  
❌ **No deeply nested subqueries** for time-series (pre-aggregate in ETL if needed)  
❌ **No UNION ALL of fact tables** to reconstruct old ResponseAssessment (breaks grain semantics)

---

## 3. Target Logical Model

### 3.1 Conformed Dimensions

#### **dim_patient** (unchanged)
- **Grain**: One row per patient
- **PK**: `patient_id` (e.g., NGDX-001)
- **Attributes**: Demographics, baseline labs, diagnosis date

#### **dim_treatment** (unchanged, promoted to dimension)
- **Grain**: One row per treatment line per patient
- **PK**: `treatment_id`
- **FK**: `patient_id` → dim_patient
- **Attributes**: Drug name, start/end dates, line number, discontinuation reason

### 3.2 Source Fact Tables (unchanged)

#### **fact_imaging_study**
- **Grain**: One row per imaging scan
- **PK**: `imaging_study_id`
- **FK**: `patient_id` → dim_patient
- **Measures**: TNM staging, tumor diameter, DICOM paths

#### **fact_biopsy** → **fact_molecular_test** → **fact_mutation**
- **Grain (Biopsy)**: One row per biopsy procedure
- **Grain (MolecularTest)**: One row per NGS panel run
- **Grain (Mutation)**: One row per detected variant
- **Lineage**: fact_mutation → fact_molecular_test → fact_biopsy → dim_patient

### 3.3 New Response Fact Tables

#### **fact_imaging_response**
**Grain**: One row per imaging study with documented treatment response assessment

| Attribute | Type | Nullable | Description |
|-----------|------|----------|-------------|
| `imaging_response_id` | TEXT | PK, NOT NULL | Surrogate key |
| `imaging_study_id` | TEXT | FK, NOT NULL | Source imaging study (REQUIRED) |
| `patient_id` | TEXT | FK, NOT NULL | Conformed dimension |
| `treatment_id` | TEXT | FK, NULLABLE | Treatment context (NULL for baseline) |
| `assessment_date` | DATE | NOT NULL | Date of radiologist assessment |
| `assessment_type` | ENUM | NOT NULL | Baseline / Follow_up / Progression |
| `recist_response` | ENUM | NULLABLE | CR / PR / SD / PD |
| `sum_target_lesions_mm` | FLOAT | NULLABLE | RECIST sum of diameters |
| `percent_change_from_baseline` | FLOAT | NULLABLE | % change from treatment baseline |
| `new_lesions_present` | BOOLEAN | NULLABLE | New lesions indicator |

**Business Rules:**
- `imaging_study_id` MUST exist in fact_imaging_study
- `assessment_date` typically matches `scan_date` from fact_imaging_study (but allows delayed reads)
- `treatment_id` NULL allowed for pre-treatment baseline scans

---

#### **fact_molecular_response**
**Grain**: One row per molecular test with documented ctDNA/VAF response assessment

| Attribute | Type | Nullable | Description |
|-----------|------|----------|-------------|
| `molecular_response_id` | TEXT | PK, NOT NULL | Surrogate key |
| `molecular_test_id` | TEXT | FK, NOT NULL | Source molecular test (REQUIRED) |
| `patient_id` | TEXT | FK, NOT NULL | Conformed dimension |
| `treatment_id` | TEXT | FK, NULLABLE | Treatment context (NULL for baseline) |
| `assessment_date` | DATE | NOT NULL | Date of molecular assessment |
| `assessment_type` | ENUM | NOT NULL | Baseline / Follow_up / Progression |
| `ctdna_vaf_percent` | FLOAT | NULLABLE | Primary driver VAF |
| `ctdna_tumor_fraction_percent` | FLOAT | NULLABLE | Overall tumor fraction |
| `ctdna_mutation_cleared` | BOOLEAN | NULLABLE | Driver mutation clearance flag |

**Business Rules:**
- `molecular_test_id` MUST exist in fact_molecular_test
- `assessment_date` typically matches `test_date` from fact_molecular_test
- Used for serial ctDNA monitoring (VAF trends over time)

---

#### **fact_clinical_response**
**Grain**: One row per documented clinical outcome event (progression, resistance, transformation)

| Attribute | Type | Nullable | Description |
|-----------|------|----------|-------------|
| `clinical_response_id` | TEXT | PK, NOT NULL | Surrogate key |
| `patient_id` | TEXT | FK, NOT NULL | Conformed dimension |
| `treatment_id` | TEXT | FK, NULLABLE | Treatment context (may be post-treatment) |
| `event_date` | DATE | NOT NULL | Date event was documented/detected |
| `event_type` | ENUM | NOT NULL | Progression / Resistance / Transformation |
| `progression_detected` | BOOLEAN | NOT NULL | Progression flag |
| `progression_type` | ENUM | NULLABLE | Oligoprogression / Systemic / CNS_only / Asymptomatic |
| `time_to_progression_months` | FLOAT | NULLABLE | TTP from treatment start |
| `resistance_mutation_detected` | BOOLEAN | NULLABLE | Resistance mutation flag |
| `resistance_mechanism` | TEXT | NULLABLE | Free-text mechanism (e.g., "T790M", "MET amplification") |
| `histologic_transformation` | BOOLEAN | NULLABLE | SCLC transformation flag |

**Business Rules:**
- Does NOT link to a specific imaging_study or molecular_test (independent clinical event)
- May be informed by imaging/molecular data, but grain is the MDT decision/documentation
- `event_date` is the date progression was declared (may differ from scan date)

---

### 3.4 Deprecated Table

#### **ResponseAssessment** (removed)
- All functionality decomposed into three specialized fact tables above
- Old data migrated via SQL backfill script (see Section 6)

---

## 4. Target Physical Model (SQLite DDL)

### 4.1 fact_imaging_response

```sql
CREATE TABLE fact_imaging_response (
    imaging_response_id TEXT PRIMARY KEY,
    imaging_study_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    treatment_id TEXT,  -- NULLABLE
    assessment_date DATE NOT NULL,
    assessment_type TEXT CHECK(assessment_type IN ('Baseline', 'Follow_up', 'Progression')),
    recist_response TEXT CHECK(recist_response IN ('CR', 'PR', 'SD', 'PD')),
    sum_target_lesions_mm REAL,
    percent_change_from_baseline REAL,
    new_lesions_present INTEGER,  -- SQLite BOOLEAN as 0/1
    
    FOREIGN KEY (imaging_study_id) REFERENCES ImagingStudy(imaging_study_id),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (treatment_id) REFERENCES Treatment(treatment_id)
);

CREATE INDEX idx_imaging_response_patient ON fact_imaging_response(patient_id);
CREATE INDEX idx_imaging_response_treatment ON fact_imaging_response(treatment_id);
CREATE INDEX idx_imaging_response_date ON fact_imaging_response(assessment_date);
```

---

### 4.2 fact_molecular_response

```sql
CREATE TABLE fact_molecular_response (
    molecular_response_id TEXT PRIMARY KEY,
    molecular_test_id TEXT NOT NULL,
    patient_id TEXT NOT NULL,
    treatment_id TEXT,  -- NULLABLE
    assessment_date DATE NOT NULL,
    assessment_type TEXT CHECK(assessment_type IN ('Baseline', 'Follow_up', 'Progression')),
    ctdna_vaf_percent REAL,
    ctdna_tumor_fraction_percent REAL,
    ctdna_mutation_cleared INTEGER,  -- SQLite BOOLEAN as 0/1
    
    FOREIGN KEY (molecular_test_id) REFERENCES MolecularTest(molecular_test_id),
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (treatment_id) REFERENCES Treatment(treatment_id)
);

CREATE INDEX idx_molecular_response_patient ON fact_molecular_response(patient_id);
CREATE INDEX idx_molecular_response_treatment ON fact_molecular_response(treatment_id);
CREATE INDEX idx_molecular_response_date ON fact_molecular_response(assessment_date);
```

---

### 4.3 fact_clinical_response

```sql
CREATE TABLE fact_clinical_response (
    clinical_response_id TEXT PRIMARY KEY,
    patient_id TEXT NOT NULL,
    treatment_id TEXT,  -- NULLABLE
    event_date DATE NOT NULL,
    event_type TEXT CHECK(event_type IN ('Progression', 'Resistance', 'Transformation')),
    progression_detected INTEGER NOT NULL,  -- SQLite BOOLEAN
    progression_type TEXT CHECK(progression_type IN ('Oligoprogression', 'Systemic_multi_site', 'CNS_only', 'Asymptomatic_slow')),
    time_to_progression_months REAL,
    resistance_mutation_detected INTEGER,
    resistance_mechanism TEXT,
    histologic_transformation INTEGER,
    
    FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
    FOREIGN KEY (treatment_id) REFERENCES Treatment(treatment_id)
);

CREATE INDEX idx_clinical_response_patient ON fact_clinical_response(patient_id);
CREATE INDEX idx_clinical_response_treatment ON fact_clinical_response(treatment_id);
CREATE INDEX idx_clinical_response_date ON fact_clinical_response(event_date);
```

---

## 5. LinkML Refactor Specification

### 5.1 Core Modeling Pattern

**BEFORE (anti-pattern):**
```yaml
classes:
  Patient:
    slots:
      - patient_id  # identifier: true
      # NO relationship slot here
  
  ResponseAssessment:
    slots:
      - patient_id  # FK as scalar, but confusing (is this identifier or FK?)
      - imaging_study_id  # optional FK
      - molecular_test_id  # optional FK
```

**AFTER (recommended pattern):**
```yaml
classes:
  Patient:
    slots:
      - patient_id  # identifier: true, range: string
      # NO collection slots like treatments[] here (avoid parent-side lists)
  
  ImagingResponse:
    slots:
      - imaging_response_id  # identifier: true
      - imaging_study  # relationship slot (range: ImagingStudy)
      - patient  # relationship slot (range: Patient)
      - treatment  # relationship slot (range: Treatment), required: false
      - assessment_date
      - recist_response
      # ... measures
    slot_usage:
      imaging_study:
        required: true
        range: ImagingStudy
      patient:
        required: true
        range: Patient
      treatment:
        required: false  # nullable for baseline assessments
        range: Treatment
```

### 5.2 Full LinkML Schema Changes

#### **Step 5.2.1: Add New Classes**

```yaml
classes:
  ImagingResponse:
    description: >
      Treatment response assessment based on imaging studies (RECIST criteria).
      Grain: one row per imaging study with documented radiologist assessment.
    slots:
      - imaging_response_id
      - imaging_study
      - patient
      - treatment
      - assessment_date
      - assessment_type
      - recist_response
      - sum_target_lesions_mm
      - percent_change_from_baseline
      - new_lesions_present
    slot_usage:
      imaging_response_id:
        identifier: true
        required: true
        range: string
      imaging_study:
        required: true
        range: ImagingStudy
        description: Source imaging study (REQUIRED - establishes lineage)
      patient:
        required: true
        range: Patient
        description: Conformed dimension for drill-across queries
      treatment:
        required: false
        range: Treatment
        description: Treatment context (NULL for pre-treatment baseline)
      assessment_date:
        required: true
        range: date
      assessment_type:
        required: true
        range: AssessmentTypeEnum
      recist_response:
        range: RECISTResponseEnum
      sum_target_lesions_mm:
        range: float
        minimum_value: 0
        maximum_value: 500
      percent_change_from_baseline:
        range: float
      new_lesions_present:
        range: boolean

  MolecularResponse:
    description: >
      Treatment response assessment based on molecular testing (ctDNA/VAF tracking).
      Grain: one row per molecular test with documented ctDNA response.
    slots:
      - molecular_response_id
      - molecular_test
      - patient
      - treatment
      - assessment_date
      - assessment_type
      - ctdna_vaf_percent
      - ctdna_tumor_fraction_percent
      - ctdna_mutation_cleared
    slot_usage:
      molecular_response_id:
        identifier: true
        required: true
        range: string
      molecular_test:
        required: true
        range: MolecularTest
        description: Source molecular test (REQUIRED - establishes lineage)
      patient:
        required: true
        range: Patient
      treatment:
        required: false
        range: Treatment
      assessment_date:
        required: true
        range: date
      assessment_type:
        required: true
        range: AssessmentTypeEnum
      ctdna_vaf_percent:
        range: float
        minimum_value: 0.0
        maximum_value: 100.0
      ctdna_tumor_fraction_percent:
        range: float
        minimum_value: 0.0
        maximum_value: 100.0
      ctdna_mutation_cleared:
        range: boolean

  ClinicalResponse:
    description: >
      Clinical outcome events (progression, resistance, histologic transformation).
      Grain: one row per documented clinical outcome event.
      Does NOT link to specific imaging/molecular tests - represents MDT consensus.
    slots:
      - clinical_response_id
      - patient
      - treatment
      - event_date
      - event_type
      - progression_detected
      - progression_type
      - time_to_progression_months
      - resistance_mutation_detected
      - resistance_mechanism
      - histologic_transformation
    slot_usage:
      clinical_response_id:
        identifier: true
        required: true
        range: string
      patient:
        required: true
        range: Patient
      treatment:
        required: false
        range: Treatment
      event_date:
        required: true
        range: date
        description: Date event was documented (may differ from test date)
      event_type:
        required: true
        range: ClinicalEventTypeEnum
      progression_detected:
        required: true
        range: boolean
      progression_type:
        range: ProgressionTypeEnum
      time_to_progression_months:
        range: float
        minimum_value: 0
      resistance_mutation_detected:
        range: boolean
      resistance_mechanism:
        range: string
      histologic_transformation:
        range: boolean
```

#### **Step 5.2.2: Add New Slots (relationship slots)**

```yaml
slots:
  # ============================================
  # ImagingResponse slots
  # ============================================
  imaging_response_id:
    identifier: true
    required: true
    range: string
    pattern: "^IR-[0-9]{3}-[0-9]{3}$"  # e.g., IR-001-001
  
  imaging_study:
    description: Relationship to source ImagingStudy
    range: ImagingStudy
    required: true
  
  # ============================================
  # MolecularResponse slots
  # ============================================
  molecular_response_id:
    identifier: true
    required: true
    range: string
    pattern: "^MR-[0-9]{3}-[0-9]{3}$"  # e.g., MR-001-001
  
  molecular_test:
    description: Relationship to source MolecularTest
    range: MolecularTest
    required: true
  
  # ============================================
  # ClinicalResponse slots
  # ============================================
  clinical_response_id:
    identifier: true
    required: true
    range: string
    pattern: "^CR-[0-9]{3}-[0-9]{3}$"  # e.g., CR-001-001
  
  event_date:
    range: date
    required: true
  
  event_type:
    range: ClinicalEventTypeEnum
    required: true
  
  # ============================================
  # Shared relationship slots
  # ============================================
  patient:
    description: Relationship to Patient dimension
    range: Patient
    required: true
  
  treatment:
    description: Relationship to Treatment dimension (nullable)
    range: Treatment
    required: false
```

#### **Step 5.2.3: Add New Enums**

```yaml
enums:
  ClinicalEventTypeEnum:
    permissible_values:
      Progression:
      Resistance:
      Transformation:
  
  # Keep existing AssessmentTypeEnum, RECISTResponseEnum, ProgressionTypeEnum
```

#### **Step 5.2.4: Deprecate ResponseAssessment Class**

```yaml
classes:
  ResponseAssessment:
    deprecated: "Replaced by ImagingResponse, MolecularResponse, ClinicalResponse"
    description: "[DEPRECATED] Use specialized response classes instead"
    # Keep class definition for backward compatibility, but mark deprecated
```

---

## 6. Migration Plan

### Overview
8-step migration with **mandatory validation checkpoints** after each step. You MUST confirm validation before proceeding to next step.

---

### **STEP 1: Update LinkML Schema**

#### Tasks
1. Open `schemas/clinical_model.yaml`
2. Add three new classes: `ImagingResponse`, `MolecularResponse`, `ClinicalResponse` (see Section 5.2.1)
3. Add new slots: `imaging_response_id`, `molecular_response_id`, `clinical_response_id`, relationship slots (see Section 5.2.2)
4. Add new enum: `ClinicalEventTypeEnum` (see Section 5.2.3)
5. Mark `ResponseAssessment` as deprecated (see Section 5.2.4)
6. Save file

#### Validation Checklist
```bash
# 1. Lint YAML syntax
linkml-lint schemas/clinical_model.yaml

# 2. Validate schema semantics
linkml-validate schemas/clinical_model.yaml

# 3. Check for undefined slot references
gen-linkml-jsonschema schemas/clinical_model.yaml > /tmp/test_schema.json
# Should complete without errors

# 4. Visual inspection
cat schemas/clinical_model.yaml | grep -A 20 "ImagingResponse:"
cat schemas/clinical_model.yaml | grep -A 20 "MolecularResponse:"
cat schemas/clinical_model.yaml | grep -A 20 "ClinicalResponse:"
```

#### Expected Output
- ✅ No YAML syntax errors
- ✅ All slot references resolve (no undefined slots)
- ✅ Three new classes visible in schema
- ✅ ResponseAssessment marked deprecated

#### Pause Point
🛑 **DO NOT PROCEED** until user confirms: "STEP 1 validated - proceed to STEP 2"

---

### **STEP 2: Regenerate LinkML Artifacts**

#### Tasks
```bash
# 2.1 Generate SQL DDL
gen-linkml-sql schemas/clinical_model.yaml > schemas/generated/sql/clinical_model_v2.sql

# 2.2 Generate Python Pydantic models
gen-pydantic schemas/clinical_model.yaml > schemas/generated/python/clinical_model_pydantic_v2.py

# 2.3 Generate ER diagram
gen-erdiagram schemas/clinical_model.yaml > schemas/generated/diagrams/er_diagram_v2.mmd

# 2.4 Generate documentation
gen-markdown schemas/clinical_model.yaml --directory schemas/generated/docs/
```

#### Validation Checklist
```bash
# 1. Check SQL DDL contains new tables
grep "CREATE TABLE.*ImagingResponse" schemas/generated/sql/clinical_model_v2.sql
grep "CREATE TABLE.*MolecularResponse" schemas/generated/sql/clinical_model_v2.sql
grep "CREATE TABLE.*ClinicalResponse" schemas/generated/sql/clinical_model_v2.sql

# 2. Check foreign key constraints
grep "FOREIGN KEY.*imaging_study" schemas/generated/sql/clinical_model_v2.sql
grep "FOREIGN KEY.*molecular_test" schemas/generated/sql/clinical_model_v2.sql

# 3. Validate Python models compile
python3 -m py_compile schemas/generated/python/clinical_model_pydantic_v2.py

# 4. Check Pydantic classes exist
grep "class ImagingResponse" schemas/generated/python/clinical_model_pydantic_v2.py
grep "class MolecularResponse" schemas/generated/python/clinical_model_pydantic_v2.py
grep "class ClinicalResponse" schemas/generated/python/clinical_model_pydantic_v2.py

# 5. Verify ER diagram relationships
grep "ImagingResponse ||--|| ImagingStudy" schemas/generated/diagrams/er_diagram_v2.mmd
grep "MolecularResponse ||--|| MolecularTest" schemas/generated/diagrams/er_diagram_v2.mmd
```

#### Expected Output
- ✅ `clinical_model_v2.sql` contains 3 new CREATE TABLE statements
- ✅ Foreign key constraints present for imaging_study_id, molecular_test_id, patient_id, treatment_id
- ✅ Python file compiles without syntax errors
- ✅ Three new Pydantic classes defined
- ✅ ER diagram shows relationships

#### Pause Point
🛑 **DO NOT PROCEED** until user confirms: "STEP 2 validated - proceed to STEP 3"

---

### **STEP 3: Create Database Migration Script**

#### Tasks
1. Create `scripts/migrate_response_tables.py`
2. Implement backfill logic to split old `ResponseAssessment` into three new tables

#### Migration Script Logic

```python
#!/usr/bin/env python3
"""
Database migration script: ResponseAssessment → 3 new fact tables
Backfills data from old ResponseAssessment table into:
  - fact_imaging_response
  - fact_molecular_response  
  - fact_clinical_response
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "backend" / "clinical_data.db"

def migrate_response_tables(conn: sqlite3.Connection):
    """Execute migration with transaction safety"""
    cursor = conn.cursor()
    
    # Step 3.1: Create new tables from v2 schema
    with open("schemas/generated/sql/clinical_model_v2.sql") as f:
        schema_sql = f.read()
        # Extract only the 3 new table definitions
        cursor.executescript(schema_sql)  # Simplified - manual extraction needed
    
    # Step 3.2: Backfill fact_imaging_response
    cursor.execute("""
        INSERT INTO ImagingResponse (
            imaging_response_id,
            imaging_study_id,
            patient_id,
            treatment_id,
            assessment_date,
            assessment_type,
            recist_response,
            sum_target_lesions_mm,
            percent_change_from_baseline,
            new_lesions_present
        )
        SELECT
            'IR-' || SUBSTR(patient_id, 6, 3) || '-' || 
                ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY assessment_date) AS imaging_response_id,
            imaging_study_id,
            patient_id,
            treatment_id,
            assessment_date,
            assessment_type,
            recist_response,
            sum_target_lesions_mm,
            percent_change_from_baseline,
            new_lesions_present
        FROM ResponseAssessment
        WHERE imaging_study_id IS NOT NULL
          AND (recist_response IS NOT NULL OR sum_target_lesions_mm IS NOT NULL)
    """)
    
    # Step 3.3: Backfill fact_molecular_response
    cursor.execute("""
        INSERT INTO MolecularResponse (
            molecular_response_id,
            molecular_test_id,
            patient_id,
            treatment_id,
            assessment_date,
            assessment_type,
            ctdna_vaf_percent,
            ctdna_tumor_fraction_percent,
            ctdna_mutation_cleared
        )
        SELECT
            'MR-' || SUBSTR(patient_id, 6, 3) || '-' || 
                ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY assessment_date) AS molecular_response_id,
            molecular_test_id,
            patient_id,
            treatment_id,
            assessment_date,
            assessment_type,
            ctdna_vaf_percent,
            ctdna_tumor_fraction_percent,
            ctdna_mutation_cleared
        FROM ResponseAssessment
        WHERE molecular_test_id IS NOT NULL
          AND (ctdna_vaf_percent IS NOT NULL OR ctdna_mutation_cleared IS NOT NULL)
    """)
    
    # Step 3.4: Backfill fact_clinical_response
    cursor.execute("""
        INSERT INTO ClinicalResponse (
            clinical_response_id,
            patient_id,
            treatment_id,
            event_date,
            event_type,
            progression_detected,
            progression_type,
            time_to_progression_months,
            resistance_mutation_detected,
            resistance_mechanism,
            histologic_transformation
        )
        SELECT
            'CR-' || SUBSTR(patient_id, 6, 3) || '-' || 
                ROW_NUMBER() OVER (PARTITION BY patient_id ORDER BY assessment_date) AS clinical_response_id,
            patient_id,
            treatment_id,
            assessment_date AS event_date,
            CASE
                WHEN progression_detected = 1 THEN 'Progression'
                WHEN resistance_mutation_detected = 1 THEN 'Resistance'
                WHEN histologic_transformation = 1 THEN 'Transformation'
                ELSE 'Progression'
            END AS event_type,
            progression_detected,
            progression_type,
            time_to_progression_months,
            resistance_mutation_detected,
            resistance_mechanism,
            histologic_transformation
        FROM ResponseAssessment
        WHERE progression_detected = 1
           OR resistance_mutation_detected = 1
           OR histologic_transformation = 1
    """)
    
    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    try:
        migrate_response_tables(conn)
        print("[OK] Migration completed successfully")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Migration failed: {e}")
        raise
    finally:
        conn.close()
```

#### Validation Checklist
```bash
# 1. Dry-run mode (read-only query test)
sqlite3 backend/clinical_data.db << EOF
SELECT COUNT(*) FROM ResponseAssessment WHERE imaging_study_id IS NOT NULL;
SELECT COUNT(*) FROM ResponseAssessment WHERE molecular_test_id IS NOT NULL;
SELECT COUNT(*) FROM ResponseAssessment WHERE progression_detected = 1;
EOF

# 2. Backup existing database
cp backend/clinical_data.db backend/clinical_data.db.backup

# 3. Run migration script
python3 scripts/migrate_response_tables.py

# 4. Verify row counts
sqlite3 backend/clinical_data.db << EOF
SELECT 'ImagingResponse', COUNT(*) FROM ImagingResponse;
SELECT 'MolecularResponse', COUNT(*) FROM MolecularResponse;
SELECT 'ClinicalResponse', COUNT(*) FROM ClinicalResponse;
SELECT 'Old ResponseAssessment', COUNT(*) FROM ResponseAssessment;
EOF

# 5. Spot-check data integrity
sqlite3 backend/clinical_data.db << EOF
-- Check FK integrity
SELECT COUNT(*) FROM ImagingResponse ir
WHERE NOT EXISTS (SELECT 1 FROM ImagingStudy i WHERE i.imaging_study_id = ir.imaging_study_id);

SELECT COUNT(*) FROM MolecularResponse mr
WHERE NOT EXISTS (SELECT 1 FROM MolecularTest m WHERE m.molecular_test_id = mr.molecular_test_id);

-- Check no orphaned records (should return 0)
EOF
```

#### Expected Output
- ✅ Migration script executes without errors
- ✅ Row counts: ImagingResponse ~= rows with imaging_study_id, MolecularResponse ~= rows with molecular_test_id
- ✅ All foreign keys resolve (0 orphaned records)
- ✅ Backup database exists

#### Pause Point
🛑 **DO NOT PROCEED** until user confirms: "STEP 3 validated - proceed to STEP 4"

---

### **STEP 4: Update Database Loader (populate_db.py)**

#### Tasks
1. Modify `scripts/populate_db.py` to load three new CSV files:
   - `example_files/mock_simulated/imaging_responses_timeseries.csv`
   - `example_files/mock_simulated/molecular_responses_timeseries.csv`
   - `example_files/mock_simulated/clinical_responses_timeseries.csv`
2. Update table list in `backend/app/database.py`

#### Code Changes

**File: `scripts/populate_db.py`** (modify existing file, add after ResponseAssessment section)

```python
# ============================================================================
# STEP 9: Load ImagingResponse (NEW)
# ============================================================================
print("\n[9/11] Loading ImagingResponse...")
imaging_response_file = mock_dir / "imaging_responses_timeseries.csv"

with open(imaging_response_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    imaging_responses = []
    
    for row in reader:
        if row['patient_id'] not in PATIENT_IDS:
            continue
        
        imaging_responses.append((
            row['imaging_response_id'],
            row['imaging_study_id'],
            row['patient_id'],
            row.get('treatment_id') or None,
            row['assessment_date'],
            row['assessment_type'],
            row.get('recist_response') or None,
            safe_float(row.get('sum_target_lesions_mm')),
            safe_float(row.get('percent_change_from_baseline')),
            parse_boolean(row.get('new_lesions_present'))
        ))
    
    cursor.executemany("""
        INSERT INTO ImagingResponse (
            imaging_response_id, imaging_study_id, patient_id, treatment_id,
            assessment_date, assessment_type, recist_response,
            sum_target_lesions_mm, percent_change_from_baseline, new_lesions_present
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, imaging_responses)
    
    print(f"  ✓ Loaded {len(imaging_responses)} imaging response records")

# Similar sections for MolecularResponse and ClinicalResponse...
```

**File: `backend/app/database.py`** (line 79-82)

```python
# OLD
tables = [
    'Patient', 'ImagingStudy', 'Biopsy', 'MolecularTest',
    'Mutation', 'Treatment', 'ResponseAssessment', 'ClinicalAssessment'
]

# NEW
tables = [
    'Patient', 'ImagingStudy', 'Biopsy', 'MolecularTest',
    'Mutation', 'Treatment', 'ImagingResponse', 'MolecularResponse',
    'ClinicalResponse', 'ClinicalAssessment'
]
```

#### Validation Checklist
```bash
# 1. Check CSV files exist
ls -lh example_files/mock_simulated/imaging_responses_timeseries.csv
ls -lh example_files/mock_simulated/molecular_responses_timeseries.csv
ls -lh example_files/mock_simulated/clinical_responses_timeseries.csv

# 2. Validate CSV headers
head -1 example_files/mock_simulated/imaging_responses_timeseries.csv

# 3. Drop and recreate database with new loader
rm backend/clinical_data.db
python3 scripts/populate_db.py

# 4. Verify all tables loaded
sqlite3 backend/clinical_data.db << EOF
SELECT name, COUNT(*) as row_count 
FROM (
  SELECT 'ImagingResponse' as name, COUNT(*) FROM ImagingResponse
  UNION ALL SELECT 'MolecularResponse', COUNT(*) FROM MolecularResponse
  UNION ALL SELECT 'ClinicalResponse', COUNT(*) FROM ClinicalResponse
);
EOF

# 5. Check foreign key integrity
sqlite3 backend/clinical_data.db << EOF
PRAGMA foreign_key_check;
EOF
# Should return empty (no FK violations)
```

#### Expected Output
- ✅ populate_db.py runs without errors
- ✅ All three new tables have > 0 rows
- ✅ No foreign key violations
- ✅ Row counts match CSV line counts (minus header)

#### Pause Point
🛑 **DO NOT PROCEED** until user confirms: "STEP 4 validated - proceed to STEP 5"

---

### **STEP 5: Update Backend API Endpoints**

#### Tasks
1. Modify `backend/app/api/timeline.py` - update RECIST series query
2. Modify `backend/app/api/patients.py` - update `/patients/{id}/response` endpoint
3. Modify `backend/app/api/decisions.py` (if exists) - update resistance detection logic

#### Code Changes

**File: `backend/app/api/timeline.py`** (lines 191-203)

```python
# OLD QUERY (lines 191-203)
recist_series_sql = """
SELECT
    i.scan_date as date,
    i.primary_tumor_diameter_mm as tumor_diameter_mm,
    i.ajcc_stage,
    i.imaging_modality,
    r.recist_response
FROM ImagingStudy i
LEFT JOIN ResponseAssessment r ON r.imaging_study_id = i.imaging_study_id
WHERE i.patient_id = ?
ORDER BY i.scan_date
"""

# NEW QUERY
recist_series_sql = """
SELECT
    i.scan_date as date,
    i.primary_tumor_diameter_mm as tumor_diameter_mm,
    i.ajcc_stage,
    i.imaging_modality,
    ir.recist_response
FROM ImagingStudy i
LEFT JOIN ImagingResponse ir ON ir.imaging_study_id = i.imaging_study_id
WHERE i.patient_id = ?
ORDER BY i.scan_date
"""
```

**File: `backend/app/api/patients.py`** (lines 355-408 - complete rewrite)

```python
@router.get("/patients/{patient_id}/response")
async def get_response_assessments(patient_id: str) -> Dict[str, Any]:
    """
    Get all response assessments for a patient (aggregated from 3 fact tables)
    
    Returns:
        Dictionary with imaging_responses, molecular_responses, clinical_responses
    """
    # Check patient exists
    patient_check = execute_query_one("SELECT patient_id FROM Patient WHERE patient_id = ?", (patient_id,))
    if not patient_check:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")
    
    # Get imaging responses
    imaging_sql = """
    SELECT
        ir.imaging_response_id,
        ir.imaging_study_id,
        ir.assessment_date,
        ir.assessment_type,
        ir.recist_response,
        ir.sum_target_lesions_mm,
        ir.percent_change_from_baseline,
        ir.new_lesions_present,
        ir.treatment_id,
        i.imaging_modality,
        i.ajcc_stage
    FROM ImagingResponse ir
    JOIN ImagingStudy i ON ir.imaging_study_id = i.imaging_study_id
    WHERE ir.patient_id = ?
    ORDER BY ir.assessment_date
    """
    imaging_responses = execute_query(imaging_sql, (patient_id,))
    
    # Get molecular responses
    molecular_sql = """
    SELECT
        mr.molecular_response_id,
        mr.molecular_test_id,
        mr.assessment_date,
        mr.assessment_type,
        mr.ctdna_vaf_percent,
        mr.ctdna_tumor_fraction_percent,
        mr.ctdna_mutation_cleared,
        mr.treatment_id,
        mt.specimen_source,
        mt.ngs_panel_name
    FROM MolecularResponse mr
    JOIN MolecularTest mt ON mr.molecular_test_id = mt.molecular_test_id
    WHERE mr.patient_id = ?
    ORDER BY mr.assessment_date
    """
    molecular_responses = execute_query(molecular_sql, (patient_id,))
    
    # Get clinical responses (progression events)
    clinical_sql = """
    SELECT
        cr.clinical_response_id,
        cr.event_date,
        cr.event_type,
        cr.progression_detected,
        cr.progression_type,
        cr.time_to_progression_months,
        cr.resistance_mutation_detected,
        cr.resistance_mechanism,
        cr.histologic_transformation,
        cr.treatment_id
    FROM ClinicalResponse cr
    WHERE cr.patient_id = ?
    ORDER BY cr.event_date
    """
    clinical_responses = execute_query(clinical_sql, (patient_id,))
    
    return {
        "patient_id": patient_id,
        "imaging_responses": imaging_responses,
        "molecular_responses": molecular_responses,
        "clinical_responses": clinical_responses,
        "total_imaging": len(imaging_responses),
        "total_molecular": len(molecular_responses),
        "total_clinical": len(clinical_responses)
    }
```

#### Validation Checklist
```bash
# 1. Start FastAPI server
cd backend
uvicorn app.main:app --reload

# 2. Test timeline endpoint
curl http://localhost:8000/api/patients/NGDX-001/timeline | jq '.recist_series'
# Should return RECIST series with recist_response populated

# 3. Test response endpoint
curl http://localhost:8000/api/patients/NGDX-001/response | jq '.imaging_responses | length'
curl http://localhost:8000/api/patients/NGDX-001/response | jq '.molecular_responses | length'
curl http://localhost:8000/api/patients/NGDX-001/response | jq '.clinical_responses | length'
# Should return counts > 0

# 4. Check for errors in API logs
# No 500 errors or SQL exceptions

# 5. Verify data structure
curl http://localhost:8000/api/patients/NGDX-001/response | jq '.imaging_responses[0]'
# Should show imaging_response_id, imaging_study_id, recist_response, etc.
```

#### Expected Output
- ✅ FastAPI starts without import errors
- ✅ Timeline endpoint returns RECIST series with response data
- ✅ Response endpoint returns three separate arrays
- ✅ No SQL errors in logs
- ✅ Data structure matches new schema

#### Pause Point
🛑 **DO NOT PROCEED** until user confirms: "STEP 5 validated - proceed to STEP 6"

---

### **STEP 6: Update Frontend Types (Optional - No UI Changes)**

#### Tasks
1. Add new TypeScript interfaces in `frontend/src/types/timeline.ts`
2. Verify existing components still work (no changes needed if backend response structure unchanged)

#### Code Changes

**File: `frontend/src/types/timeline.ts`** (add at end)

```typescript
// New response types (for future use)
export interface ImagingResponse {
  imaging_response_id: string;
  imaging_study_id: string;
  assessment_date: string;
  assessment_type: string;
  recist_response: string | null;
  sum_target_lesions_mm: number | null;
  percent_change_from_baseline: number | null;
  new_lesions_present: boolean | null;
  treatment_id: string | null;
}

export interface MolecularResponse {
  molecular_response_id: string;
  molecular_test_id: string;
  assessment_date: string;
  assessment_type: string;
  ctdna_vaf_percent: number | null;
  ctdna_tumor_fraction_percent: number | null;
  ctdna_mutation_cleared: boolean | null;
  treatment_id: string | null;
}

export interface ClinicalResponse {
  clinical_response_id: string;
  event_date: string;
  event_type: 'Progression' | 'Resistance' | 'Transformation';
  progression_detected: boolean;
  progression_type: string | null;
  time_to_progression_months: number | null;
  resistance_mutation_detected: boolean | null;
  resistance_mechanism: string | null;
  histologic_transformation: boolean | null;
  treatment_id: string | null;
}
```

#### Validation Checklist
```bash
# 1. Check TypeScript compiles
cd frontend
npm run build

# 2. Check for type errors
npm run type-check

# 3. Start dev server
npm run dev

# 4. Open browser to http://localhost:3000
# Navigate to patient detail page

# 5. Check browser console for errors
# Should see no runtime errors

# 6. Verify timeline renders correctly
# VAF chart, RECIST chart, ECOG chart should all display
```

#### Expected Output
- ✅ TypeScript compiles without errors
- ✅ No type checking errors
- ✅ Frontend dev server starts
- ✅ Timeline components render correctly
- ✅ No console errors

#### Pause Point
🛑 **DO NOT PROCEED** until user confirms: "STEP 6 validated - proceed to STEP 7"

---

### **STEP 7: Update Tests (Modify Existing, No New Files)**

#### Tasks
1. Check if tests exist in `tests/` or `backend/tests/`
2. Update existing API tests to use new table names
3. Update any integration tests that query ResponseAssessment

#### Test Update Strategy

```python
# Example test file: tests/test_api_patients.py

# OLD TEST
def test_get_response_assessments():
    response = client.get("/api/patients/NGDX-001/response")
    assert response.status_code == 200
    data = response.json()
    assert "assessments" in data
    assert len(data["assessments"]) > 0
    assert "recist_response" in data["assessments"][0]
    assert "ctdna_vaf_percent" in data["assessments"][0]  # Mixed data!

# NEW TEST
def test_get_response_assessments():
    response = client.get("/api/patients/NGDX-001/response")
    assert response.status_code == 200
    data = response.json()
    
    # Check structure has three separate arrays
    assert "imaging_responses" in data
    assert "molecular_responses" in data
    assert "clinical_responses" in data
    
    # Check imaging responses have RECIST data only
    if len(data["imaging_responses"]) > 0:
        img_resp = data["imaging_responses"][0]
        assert "recist_response" in img_resp
        assert "imaging_study_id" in img_resp
        assert "ctdna_vaf_percent" not in img_resp  # Should NOT have molecular fields
    
    # Check molecular responses have ctDNA data only
    if len(data["molecular_responses"]) > 0:
        mol_resp = data["molecular_responses"][0]
        assert "ctdna_vaf_percent" in mol_resp
        assert "molecular_test_id" in mol_resp
        assert "recist_response" not in mol_resp  # Should NOT have imaging fields
```

#### Validation Checklist
```bash
# 1. Find existing tests
find . -name "test_*.py" -o -name "*_test.py"

# 2. Run tests BEFORE changes (baseline)
pytest -v tests/

# 3. Update tests to match new schema

# 4. Run tests AFTER changes
pytest -v tests/

# 5. Check test coverage
pytest --cov=backend/app tests/

# 6. All tests should pass (or be updated to pass)
```

#### Expected Output
- ✅ All existing tests identified
- ✅ Tests updated to use new table structure
- ✅ All tests pass
- ✅ No decrease in test coverage percentage

#### Pause Point
🛑 **DO NOT PROCEED** until user confirms: "STEP 7 validated - proceed to STEP 8"

---

### **STEP 8: Drop Old ResponseAssessment Table (Final Cutover)**

#### Tasks
1. Archive old ResponseAssessment data to CSV backup
2. Drop ResponseAssessment table from SQLite
3. Update populate_db.py to remove ResponseAssessment loading
4. Update any remaining documentation

#### Archival Script

```python
#!/usr/bin/env python3
"""Archive ResponseAssessment table before dropping"""
import sqlite3
import csv
from pathlib import Path

DB_PATH = Path("backend/clinical_data.db")
ARCHIVE_PATH = Path("example_files/archive/response_assessment_backup.csv")

ARCHIVE_PATH.parent.mkdir(exist_ok=True)

conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row

cursor = conn.cursor()
cursor.execute("SELECT * FROM ResponseAssessment ORDER BY patient_id, assessment_date")
rows = cursor.fetchall()

# Write to CSV
with open(ARCHIVE_PATH, 'w', newline='') as f:
    if rows:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows([dict(row) for row in rows])

print(f"[OK] Archived {len(rows)} rows to {ARCHIVE_PATH}")

# Drop table
cursor.execute("DROP TABLE IF EXISTS ResponseAssessment")
conn.commit()
conn.close()

print("[OK] Dropped ResponseAssessment table")
```

#### Validation Checklist
```bash
# 1. Archive old data
python3 scripts/archive_response_assessment.py

# 2. Verify archive exists
ls -lh example_files/archive/response_assessment_backup.csv
wc -l example_files/archive/response_assessment_backup.csv

# 3. Verify table dropped
sqlite3 backend/clinical_data.db "SELECT name FROM sqlite_master WHERE type='table' AND name='ResponseAssessment';"
# Should return empty

# 4. Check all API endpoints still work
curl http://localhost:8000/api/patients/NGDX-001/timeline | jq '.recist_series | length'
curl http://localhost:8000/api/patients/NGDX-001/response | jq '.imaging_responses | length'

# 5. No SQL errors referencing ResponseAssessment
grep -r "ResponseAssessment" backend/app/api/*.py
# Should only find comments/docstrings, no active queries

# 6. Update documentation
grep -r "ResponseAssessment" *.md
# Update any references in README, docs, etc.
```

#### Expected Output
- ✅ Archive CSV created with all old data
- ✅ ResponseAssessment table no longer in database
- ✅ All API endpoints work without ResponseAssessment
- ✅ No code references to old table (except deprecated LinkML class)
- ✅ Documentation updated

#### Final Validation
🛑 **DO NOT MARK COMPLETE** until user confirms: "STEP 8 validated - migration complete"

---

## 7. Query Impact & Example SQL Patterns

### 7.1 VAF Trends Over Time (No Change)

**Use Case**: Plot EGFR exon19del VAF across treatment lines

**Query Pattern**:
```sql
-- BEFORE (works on ResponseAssessment)
SELECT
    mt.test_date,
    m.vaf_percent,
    r.treatment_id
FROM Mutation m
JOIN MolecularTest mt ON m.molecular_test_id = mt.molecular_test_id
JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
LEFT JOIN ResponseAssessment r ON r.molecular_test_id = mt.molecular_test_id
WHERE b.patient_id = 'NGDX-001'
  AND m.gene_symbol = 'EGFR'
ORDER BY mt.test_date;

-- AFTER (cleaner with new table)
SELECT
    mt.test_date,
    m.vaf_percent,
    mr.treatment_id
FROM Mutation m
JOIN MolecularTest mt ON m.molecular_test_id = mt.molecular_test_id
JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
LEFT JOIN MolecularResponse mr ON mr.molecular_test_id = mt.molecular_test_id
WHERE b.patient_id = 'NGDX-001'
  AND m.gene_symbol = 'EGFR'
ORDER BY mt.test_date;
```

**Impact**: ✅ Minimal - just table name change

---

### 7.2 Imaging + Molecular Response Comparison (Drill-Across)

**Use Case**: For treatment line 1, show RECIST response AND ctDNA clearance over time

**❌ ANTI-PATTERN (fact-to-fact JOIN):**
```sql
-- DON'T DO THIS - fragile if dates don't match exactly
SELECT
    ir.assessment_date,
    ir.recist_response,
    mr.ctdna_mutation_cleared
FROM ImagingResponse ir
JOIN MolecularResponse mr ON mr.patient_id = ir.patient_id
    AND mr.assessment_date = ir.assessment_date  -- FRAGILE!
WHERE ir.patient_id = 'NGDX-001';
```

**✅ RECOMMENDED PATTERN (drill-across via shared dimensions):**
```sql
-- Separate queries, merged in application layer
-- Query 1: Imaging responses
SELECT
    ir.assessment_date AS date,
    ir.recist_response,
    'imaging' AS source
FROM ImagingResponse ir
WHERE ir.patient_id = 'NGDX-001'
  AND ir.treatment_id = 'TRT-001-001';

-- Query 2: Molecular responses
SELECT
    mr.assessment_date AS date,
    mr.ctdna_mutation_cleared,
    'molecular' AS source
FROM MolecularResponse mr
WHERE mr.patient_id = 'NGDX-001'
  AND mr.treatment_id = 'TRT-001-001';

-- Merge in Python/TypeScript by date (allows fuzzy date matching ±7 days)
```

**Impact**: ✅ More flexible - handles different assessment schedules

---

### 7.3 Progression with Resistance Mechanism

**Use Case**: Find patients who progressed with T790M resistance mutation

**Query Pattern**:
```sql
-- BEFORE (single table, confusing columns)
SELECT
    patient_id,
    assessment_date,
    progression_type,
    resistance_mechanism
FROM ResponseAssessment
WHERE progression_detected = 1
  AND resistance_mutation_detected = 1
  AND resistance_mechanism LIKE '%T790M%';

-- AFTER (explicit clinical response table)
SELECT
    cr.patient_id,
    cr.event_date,
    cr.progression_type,
    cr.resistance_mechanism,
    t.drug_name AS prior_treatment
FROM ClinicalResponse cr
LEFT JOIN Treatment t ON cr.treatment_id = t.treatment_id
WHERE cr.event_type = 'Progression'
  AND cr.resistance_mutation_detected = 1
  AND cr.resistance_mechanism LIKE '%T790M%';
```

**Impact**: ✅ Clearer semantics - ClinicalResponse is explicitly for outcomes

---

### 7.4 Time to Progression (TTP) Calculation

**Use Case**: Calculate median TTP for patients on osimertinib

**Query Pattern**:
```sql
-- AFTER (clean join to treatment dimension)
SELECT
    t.drug_name,
    AVG(cr.time_to_progression_months) AS median_ttp_months,
    COUNT(*) AS n_progressions
FROM ClinicalResponse cr
JOIN Treatment t ON cr.treatment_id = t.treatment_id
WHERE t.drug_name = 'Osimertinib'
  AND cr.progression_detected = 1
GROUP BY t.drug_name;
```

**Impact**: ✅ Direct join to Treatment dimension (no need to backtrack through patient)

---

### 7.5 Dashboard Aggregate (Patient Summary)

**Use Case**: Show latest response status across all modalities

**Query Pattern**:
```sql
-- Get latest imaging response
SELECT
    'Imaging' AS modality,
    ir.assessment_date AS last_assessed,
    ir.recist_response AS status
FROM ImagingResponse ir
WHERE ir.patient_id = 'NGDX-001'
ORDER BY ir.assessment_date DESC
LIMIT 1

UNION ALL

-- Get latest molecular response
SELECT
    'Molecular' AS modality,
    mr.assessment_date AS last_assessed,
    CASE WHEN mr.ctdna_mutation_cleared = 1 THEN 'Cleared' ELSE 'Detected' END AS status
FROM MolecularResponse mr
WHERE mr.patient_id = 'NGDX-001'
ORDER BY mr.assessment_date DESC
LIMIT 1

UNION ALL

-- Get latest clinical outcome
SELECT
    'Clinical' AS modality,
    cr.event_date AS last_assessed,
    cr.event_type AS status
FROM ClinicalResponse cr
WHERE cr.patient_id = 'NGDX-001'
ORDER BY cr.event_date DESC
LIMIT 1;
```

**Impact**: ✅ UNION query across specialized tables (each optimized for its domain)

---

## 8. Risks & Anti-Patterns to Avoid

### Risk 1: Fact-to-Fact JOINs in Production
**Problem**: Directly joining `ImagingResponse` to `MolecularResponse` assumes assessment dates align perfectly (they often don't)

**Mitigation**:
- Use drill-across pattern (join through shared Patient/Treatment dimensions)
- Merge time-series in application layer with fuzzy date matching (±7 days)
- Create a denormalized view if needed: `vw_integrated_response_timeline`

---

### Risk 2: Orphaned Response Records
**Problem**: Deleting a MolecularTest should invalidate related MolecularResponse rows

**Mitigation**:
- Enable foreign key constraints: `PRAGMA foreign_keys = ON`
- Use `ON DELETE RESTRICT` (prevent test deletion if responses exist)
- Validate FK integrity in ETL: `PRAGMA foreign_key_check`

---

### Risk 3: Confusing Grain (e.g., multiple responses per test)
**Problem**: User creates 2 MolecularResponse rows for same molecular_test_id (violates 1:1 grain)

**Mitigation**:
- Add UNIQUE constraint: `UNIQUE(molecular_test_id)` on MolecularResponse
- Document grain explicitly in schema description
- ETL validation: detect duplicate molecular_test_id before INSERT

---

### Risk 4: Treatment FK Nullability Confusion
**Problem**: Analyst expects all responses have treatment_id, but baseline assessments are NULL

**Mitigation**:
- Document in schema: "treatment_id nullable for pre-treatment baseline assessments"
- Add check constraint: `assessment_type = 'Baseline' OR treatment_id IS NOT NULL`
- Dashboard UI: label baseline rows clearly ("Pre-treatment")

---

### Risk 5: Lost Historical Context After Migration
**Problem**: Old ResponseAssessment table dropped before validating backfill quality

**Mitigation**:
- Archive ResponseAssessment to CSV before dropping (see STEP 8)
- Run reconciliation query: compare row counts, check for missing FKs
- Keep backup database for 30 days: `clinical_data.db.backup`

---

## 9. Acceptance Criteria

### 9.1 Schema Validation
- [ ] LinkML schema validates with `linkml-validate`
- [ ] Three new classes defined: ImagingResponse, MolecularResponse, ClinicalResponse
- [ ] ResponseAssessment class marked deprecated
- [ ] All slot references resolve (no undefined slots)

### 9.2 Database Validation
- [ ] Three new tables exist: ImagingResponse, MolecularResponse, ClinicalResponse
- [ ] Foreign key constraints enforced (`PRAGMA foreign_key_check` returns empty)
- [ ] Indexes created on patient_id, treatment_id, date columns
- [ ] Row counts: ImagingResponse ≥ 5, MolecularResponse ≥ 5, ClinicalResponse ≥ 3
- [ ] Old ResponseAssessment table dropped (or archived and marked deprecated)

### 9.3 Code Validation
- [ ] Backend API endpoints updated to query new tables
- [ ] No SQL queries reference ResponseAssessment (except in deprecation comments)
- [ ] Python Pydantic models generated and compile without errors
- [ ] TypeScript types defined for new response structures

### 9.4 Functional Validation
- [ ] Timeline endpoint `/patients/{id}/timeline` returns RECIST series with response data
- [ ] Response endpoint `/patients/{id}/response` returns three separate arrays
- [ ] VAF trend queries work (no regression)
- [ ] Imaging + molecular drill-across queries return expected results
- [ ] Progression detection queries return clinical response events

### 9.5 Data Quality Validation
- [ ] No orphaned response records (all FKs resolve)
- [ ] No duplicate responses for same source test (grain validation)
- [ ] Baseline assessments have NULL treatment_id (expected)
- [ ] Response dates align with source test dates (±7 days tolerance)
- [ ] All archived ResponseAssessment rows accounted for in new tables

### 9.6 Testing Validation
- [ ] All existing tests pass (or updated to pass)
- [ ] No decrease in test coverage percentage
- [ ] Integration tests verify new table structure
- [ ] No runtime SQL errors in API logs

### 9.7 Documentation Validation
- [ ] ER diagram updated to show new relationships
- [ ] README/docs updated to remove ResponseAssessment references
- [ ] Migration script documented with usage instructions
- [ ] Grain statements documented in LinkML descriptions

---

## 10. Rollback Plan

**If migration fails at any step:**

1. **Restore database backup**:
   ```bash
   cp backend/clinical_data.db.backup backend/clinical_data.db
   ```

2. **Revert LinkML schema**:
   ```bash
   git checkout HEAD -- schemas/clinical_model.yaml
   ```

3. **Regenerate old artifacts**:
   ```bash
   gen-linkml-sql schemas/clinical_model.yaml > schemas/generated/sql/clinical_model.sql
   ```

4. **Restart backend** (will load old schema)

5. **Investigate failure**, fix issue, retry from failed step

---

## Summary

This specification provides a **complete, step-by-step migration plan** to refactor the ResponseAssessment table into three specialized fact tables with clear grain and lineage. Each step includes:

✅ **Explicit tasks**  
✅ **Validation checklists**  
✅ **Expected outputs**  
✅ **Mandatory pause points for user confirmation**

**Key principles:**
- OLAP-oriented dimensional design (drill-across, not fact-to-fact joins)
- Clear grain statements for every fact table
- Required FKs for source lineage, optional FKs for context
- LinkML best practices (scalar IDs, relationship slots)
- Modify existing files, no new test files
- Validate at every step before proceeding

**Total steps**: 8 sequential steps with validation gates  
**Estimated time**: 4-6 hours with validation pauses  
**Risk level**: Medium (requires database migration + API changes)

---

**READY TO BEGIN:** User should confirm "START STEP 1" to begin execution.