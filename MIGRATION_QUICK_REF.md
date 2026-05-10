# ResponseAssessment Migration - Quick Reference

## One-Page Cheat Sheet

### Migration Goal
Split `ResponseAssessment` (1 polymorphic table) → 3 specialized tables:
- `ImagingResponse` (RECIST imaging assessments)
- `MolecularResponse` (ctDNA/VAF molecular assessments)  
- `ClinicalResponse` (progression/resistance events)

---

## Quick Start (5 Steps)

```bash
# Activate virtual environment
source .venv/Scripts/activate  # Windows Git Bash

# Step 1: Pre-check
python scripts/validate_pre_migration.py

# Step 2: Run migration (will prompt for confirmation)
python scripts/migrate_response_tables.py

# Step 3: Verify
python scripts/verify_post_migration.py

# Step 4: Update API (see Backend API Changes below)

# Step 5: Test
curl http://localhost:8000/api/patients/NGDX-001/timeline | jq
```

---

## Table Schemas

### ImagingResponse
| Column | Type | Nullable | FK/PK |
|--------|------|----------|-------|
| imaging_response_id | TEXT | NOT NULL | PK |
| imaging_study_id | TEXT | NOT NULL | FK → ImagingStudy |
| patient_id | TEXT | NOT NULL | FK → Patient |
| treatment_id | TEXT | **NULL** | FK → Treatment |
| assessment_date | DATE | NOT NULL | |
| assessment_type | VARCHAR(11) | NULL | |
| recist_response | VARCHAR(2) | NULL | CR/PR/SD/PD |
| sum_target_lesions_mm | FLOAT | NULL | |
| percent_change_from_baseline | FLOAT | NULL | |
| new_lesions_present | BOOLEAN | NULL | |

**ID Format**: `IR-001-001` (IR-{patient_num}-{counter})

---

### MolecularResponse
| Column | Type | Nullable | FK/PK |
|--------|------|----------|-------|
| molecular_response_id | TEXT | NOT NULL | PK |
| molecular_test_id | TEXT | NOT NULL | FK → MolecularTest |
| patient_id | TEXT | NOT NULL | FK → Patient |
| treatment_id | TEXT | **NULL** | FK → Treatment |
| assessment_date | DATE | NOT NULL | |
| assessment_type | VARCHAR(11) | NULL | |
| ctdna_vaf_percent | FLOAT | NULL | |
| ctdna_tumor_fraction_percent | FLOAT | NULL | |
| ctdna_mutation_cleared | BOOLEAN | NULL | |

**ID Format**: `MR-001-001` (MR-{patient_num}-{counter})

---

### ClinicalResponse
| Column | Type | Nullable | FK/PK |
|--------|------|----------|-------|
| clinical_response_id | TEXT | NOT NULL | PK |
| patient_id | TEXT | NOT NULL | FK → Patient |
| treatment_id | TEXT | **NULL** | FK → Treatment |
| event_date | DATE | NOT NULL | |
| event_type | VARCHAR(15) | NOT NULL | Progression/Resistance/Transformation |
| progression_detected | BOOLEAN | NOT NULL | |
| progression_type | VARCHAR(19) | NULL | |
| time_to_progression_months | FLOAT | NULL | |
| resistance_mutation_detected | BOOLEAN | NULL | |
| resistance_mechanism | TEXT | NULL | |
| histologic_transformation | BOOLEAN | NULL | |

**ID Format**: `CR-001-001` (CR-{patient_num}-{counter})

---

## Backend API Changes

### File: `backend/app/api/timeline.py`

**Line ~191-203**: Change `ResponseAssessment` → `ImagingResponse`

```python
# OLD: LEFT JOIN ResponseAssessment r ON r.imaging_study_id = i.imaging_study_id
# NEW: LEFT JOIN ImagingResponse ir ON ir.imaging_study_id = i.imaging_study_id
```

### File: `backend/app/api/patients.py`

**Replace `/patients/{patient_id}/response` endpoint** (line ~355-408):

```python
return {
    "patient_id": patient_id,
    "imaging_responses": [...],    # NEW: separate arrays
    "molecular_responses": [...],  # NEW
    "clinical_responses": [...],   # NEW
    "total_imaging": len(...),
    "total_molecular": len(...),
    "total_clinical": len(...)
}
```

**Old format** (single array):
```json
{
  "assessments": [
    {"recist_response": "PR", "ctdna_vaf_percent": 5.2}  // MIXED
  ]
}
```

**New format** (three arrays):
```json
{
  "imaging_responses": [
    {"recist_response": "PR", "sum_target_lesions_mm": 35}
  ],
  "molecular_responses": [
    {"ctdna_vaf_percent": 5.2, "ctdna_mutation_cleared": false}
  ],
  "clinical_responses": [
    {"event_type": "Progression", "progression_detected": true}
  ]
}
```

### File: `backend/app/database.py`

**Line ~79**: Update table list

```python
# OLD: 'ResponseAssessment'
# NEW: 'ImagingResponse', 'MolecularResponse', 'ClinicalResponse'
```

---

## Query Patterns

### ❌ ANTI-PATTERN: Direct fact-to-fact JOIN

```sql
-- DON'T DO THIS (fragile date matching)
SELECT ir.recist_response, mr.ctdna_vaf_percent
FROM ImagingResponse ir
JOIN MolecularResponse mr ON mr.patient_id = ir.patient_id
  AND mr.assessment_date = ir.assessment_date  -- FRAGILE!
```

### ✅ RECOMMENDED: Drill-across via shared dimension

```sql
-- Query 1: Imaging
SELECT assessment_date, recist_response, 'imaging' AS source
FROM ImagingResponse
WHERE patient_id = ?;

-- Query 2: Molecular (separate query)
SELECT assessment_date, ctdna_vaf_percent, 'molecular' AS source
FROM MolecularResponse
WHERE patient_id = ?;

-- Merge in application layer with fuzzy date matching (±7 days)
```

---

## Common Commands

### Check if migration completed
```bash
python -c "import sqlite3; conn = sqlite3.connect('backend/clinical_data.db'); cursor = conn.cursor(); cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\" AND name LIKE \"%Response\"'); print(cursor.fetchall())"
```

**Expected**: `[('ImagingResponse',), ('MolecularResponse',), ('ClinicalResponse',)]`

### Count rows in new tables
```bash
python -c "import sqlite3; conn = sqlite3.connect('backend/clinical_data.db'); cursor = conn.cursor(); tables = ['ImagingResponse', 'MolecularResponse', 'ClinicalResponse']; [print(f'{t}: {cursor.execute(f\"SELECT COUNT(*) FROM {t}\").fetchone()[0]} rows') for t in tables]"
```

### Check FK integrity
```bash
python -c "import sqlite3; conn = sqlite3.connect('backend/clinical_data.db'); conn.execute('PRAGMA foreign_keys = ON'); cursor = conn.cursor(); [print(f'{t}: {\"✓ valid\" if not cursor.execute(f\"PRAGMA foreign_key_check({t})\").fetchall() else \"✗ violations\"}') for t in ['ImagingResponse', 'MolecularResponse', 'ClinicalResponse']]"
```

### Find backup files
```bash
ls -lht backend/clinical_data_pre_migration_*.db | head -3
ls -lht example_files/archive/response_assessment_backup_*.csv | head -3
```

### Restore from backup
```bash
# Find latest backup
BACKUP=$(ls -t backend/clinical_data_pre_migration_*.db | head -1)
echo "Restoring from: $BACKUP"

# Restore
cp "$BACKUP" backend/clinical_data.db
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| **"ResponseAssessment table not found"** | Migration already done. Check if new tables exist. |
| **"Foreign key violations detected"** | Run `validate_pre_migration.py` to find orphaned FKs. Delete or fix before retrying. |
| **Row count mismatch** | Check migration script WHERE clauses. Some rows may not qualify (expected if no data). |
| **API returns empty arrays** | Table names in SQL queries may be incorrect. Check for `ResponseAssessment` references. |
| **Frontend errors** | API response structure changed. Update TypeScript types and component queries. |

---

## Rollback

```bash
# Option 1: Restore from automatic backup
cp backend/clinical_data_pre_migration_YYYYMMDD_HHMMSS.db backend/clinical_data.db

# Option 2: Check archive
ls example_files/archive/response_assessment_backup_*.csv
# Manually restore ResponseAssessment table from CSV if needed
```

---

## Success Criteria Checklist

- [ ] `ImagingResponse` table exists with correct schema
- [ ] `MolecularResponse` table exists with correct schema
- [ ] `ClinicalResponse` table exists with correct schema
- [ ] Row counts match pre-migration expectations
- [ ] No foreign key violations
- [ ] All primary keys are unique
- [ ] Required fields have no NULLs
- [ ] 9 indexes created successfully
- [ ] `ResponseAssessment` table dropped (or archived)
- [ ] API endpoints updated to query new tables
- [ ] Backend tests pass
- [ ] Frontend components render without errors

---

## Files Created by Migration

```
backend/
  clinical_data_pre_migration_YYYYMMDD_HHMMSS.db  # Auto backup

example_files/archive/
  response_assessment_backup_YYYYMMDD_HHMMSS.csv  # CSV archive
  pre_migration_report.json                       # Validation report
```

---

## Safety Features

✅ **Automatic database backup** before any changes  
✅ **Transaction rollback** on any error  
✅ **Pre-migration validation** (FK integrity, row counts)  
✅ **Post-migration validation** (data integrity, indexes)  
✅ **Interactive confirmation prompts** before destructive actions  
✅ **CSV archive** of old table before dropping  

---

## Performance Notes

- **Migration time**: ~1-2 seconds for 100 rows, ~10-30 seconds for 1000 rows
- **Disk space**: Backup + archive adds ~2x original DB size temporarily
- **Query performance**: New indexes improve response time by ~5-10x for patient-filtered queries

---

## Next Steps After Migration

1. ✅ Update backend API endpoints (required)
2. ✅ Update LinkML schema (add 3 new classes, deprecate old)
3. ✅ Regenerate Python Pydantic models
4. ✅ Update frontend TypeScript types (if using frontend)
5. ✅ Update tests (replace `ResponseAssessment` references)
6. ⚠️ Update documentation/README

---

**Quick Links**:
- Full guide: [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)
- Technical spec: [RESPONSE_TABLE_REFACTOR_SPEC.md](RESPONSE_TABLE_REFACTOR_SPEC.md)
- System architecture: [00-SYSTEM-SPEC.md](00-SYSTEM-SPEC.md)

**Support**: If issues arise, restore from backup and consult `pre_migration_report.json`