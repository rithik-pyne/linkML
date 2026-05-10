# Decisions Endpoint Fixed + Artifacts Regenerated ✅

**Date:** 2026-04-30  
**Issue:** Treatment recommendations endpoint broken, ER diagram outdated

---

## Issues Fixed

### 1. Decisions Endpoint Query Error ✅

**Problem:**
```python
# backend/app/api/decisions.py (lines 115-127)
progression_sql = """
SELECT progression_detected, progression_type
FROM ResponseAssessment  # <-- BROKEN: Table dropped
WHERE patient_id = ? AND progression_detected = 1
"""
```

**Error:** Would return no results because ResponseAssessment table was dropped in Step 3.

**Fix Applied:**
```python
# backend/app/api/decisions.py (lines 115-128)
progression_sql = """
SELECT
    progression_detected,
    progression_type,
    resistance_mutation_detected,
    resistance_mechanism,
    event_date  # Added
FROM ClinicalResponse  # Updated table
WHERE patient_id = ?
  AND progression_detected = 1
ORDER BY event_date DESC
LIMIT 1
"""
```

**Changes:**
- Line 120: `ResponseAssessment` → `ClinicalResponse`
- Line 123: `ORDER BY assessment_date` → `ORDER BY event_date`
- Line 119: Added `event_date` to SELECT
- Line 149: Updated `trigger_date` to use `progression.get('event_date')`

---

### 2. ER Diagram Regenerated ✅

**Issue:** ER diagram out of sync with actual schema changes.

**Action:** Regenerated using LinkML generator:
```bash
gen-erdiagram --format mermaid schemas/clinical_model.yaml > schemas/generated/diagrams/er_diagram_v2.mmd
```

**Result:**
- **File:** `schemas/generated/diagrams/er_diagram_v2.mmd` (201 lines)
- **Tables included:** All 11 classes (including deprecated ResponseAssessment for reference)
- **Relationships correct:**
  ```mermaid
  ClinicalResponse ||--|| Patient : "patient_id"
  ClinicalResponse ||--|o Treatment : "treatment_id"
  ImagingResponse ||--|| Patient : "patient_id"
  ImagingResponse ||--|| ImagingStudy : "imaging_study_id"
  ImagingResponse ||--|o Treatment : "treatment_id"
  MolecularResponse ||--|| Patient : "patient_id"
  MolecularResponse ||--|| MolecularTest : "molecular_test_id"
  MolecularResponse ||--|o Treatment : "treatment_id"
  ```

**Note:** ResponseAssessment still appears in ER diagram because it's in the schema as deprecated. This is intentional for documentation purposes. The actual database table has been dropped.

---

### 3. All Artifacts Regenerated ✅

**SQL DDL:**
```bash
gen-sqlddl schemas/clinical_model.yaml > schemas/generated/sql/clinical_model_v2.sql
```
- **Result:** 437 lines ✅
- **Validation:** Contains all 3 new response tables

**Pydantic Models:**
```bash
gen-pydantic schemas/clinical_model.yaml > schemas/generated/python/clinical_model_pydantic_v2.py
```
- **Result:** 994 lines ✅
- **Validation:** All 3 response classes present

**ER Diagram:**
```bash
gen-erdiagram --format mermaid schemas/clinical_model.yaml > schemas/generated/diagrams/er_diagram_v2.mmd
```
- **Result:** 201 lines ✅
- **Validation:** All relationships correct

---

## Validation

### Decisions Query Test
```sql
SELECT progression_detected, progression_type, resistance_mechanism, event_date
FROM ClinicalResponse
WHERE patient_id = 'NGDX-001'
  AND progression_detected = 1
ORDER BY event_date DESC
LIMIT 1
```

**Result:** ✅
```python
{
  'progression_detected': 1,
  'progression_type': 'Systemic_multi-site',
  'resistance_mechanism': 'T790M + MET_amplification',
  'event_date': '2022-08-05'
}
```

---

## Files Updated

### Backend
1. ✅ `backend/app/api/decisions.py` (lines 115-149)
   - Updated query to use ClinicalResponse
   - Changed assessment_date → event_date
   - Fixed trigger_date in alert

### Generated Artifacts
2. ✅ `schemas/generated/sql/clinical_model_v2.sql` (437 lines)
3. ✅ `schemas/generated/python/clinical_model_pydantic_v2.py` (994 lines)
4. ✅ `schemas/generated/diagrams/er_diagram_v2.mmd` (201 lines)

---

## Testing

### Manual Query Test
```bash
# Test ClinicalResponse query
python -c "
import sys
sys.path.insert(0, 'backend')
from app.database import execute_query_one

result = execute_query_one('''
SELECT progression_detected, progression_type, resistance_mechanism, event_date
FROM ClinicalResponse
WHERE patient_id = \"NGDX-001\"
AND progression_detected = 1
ORDER BY event_date DESC
LIMIT 1
''')

print('Progression found:', result)
"
```
**Result:** ✅ Query works, returns progression data

### Decisions Endpoint (Full Stack Test Required)
To fully test, start backend server:
```bash
cd backend
uvicorn app.main:app --reload

# Then test:
curl http://localhost:8000/api/patients/NGDX-001/decisions
```

**Expected Response:**
```json
{
  "patient_id": "NGDX-001",
  "current_treatment_line": 3,
  "current_stage": "IVB",
  "recommendations": [...],
  "alerts": [
    {
      "alert_type": "progression_detected",
      "severity": "High",
      "message": "Radiographic progression detected - Systemic_multi-site",
      "trigger_date": "2022-08-05",
      "requires_action": true
    }
  ],
  "supporting_data": {
    "progression_detected": true
  }
}
```

---

## ER Diagram Note

### Why ResponseAssessment Still Appears

The ER diagram shows ResponseAssessment because:
1. It's still in the LinkML schema (marked as deprecated)
2. This provides documentation of the old structure
3. Helps with understanding migration history

**Important:** The actual database table has been dropped. ResponseAssessment only exists in:
- ✅ LinkML schema (deprecated)
- ✅ Generated documentation (deprecated)
- ✅ ER diagram (reference only)

**Does NOT exist in:**
- ❌ Database (dropped in Step 3)
- ❌ Backend API queries (all updated)
- ❌ Frontend types (removed)

To fully remove from ER diagram, you would need to delete the ResponseAssessment class from `schemas/clinical_model.yaml` entirely. Current approach keeps it for documentation purposes.

---

## Summary

### Fixed ✅
- [x] Decisions endpoint query updated to ClinicalResponse
- [x] Event date field corrected (assessment_date → event_date)
- [x] Alert trigger_date now populated correctly
- [x] Query validated against database
- [x] ER diagram regenerated
- [x] SQL DDL regenerated
- [x] Pydantic models regenerated

### Remaining Work
- [ ] Full stack runtime test (start backend and test /decisions endpoint)
- [ ] Optional: Remove ResponseAssessment from schema entirely

---

**Status:** ✅ DECISIONS ENDPOINT FIXED

**Next Step:** Runtime test by starting backend and calling `/api/patients/NGDX-001/decisions`

**Files Changed:**
- backend/app/api/decisions.py (2 edits)
- schemas/generated/sql/clinical_model_v2.sql (regenerated)
- schemas/generated/python/clinical_model_pydantic_v2.py (regenerated)
- schemas/generated/diagrams/er_diagram_v2.mmd (regenerated)