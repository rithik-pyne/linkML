# ResponseAssessment Table Migration Guide

## Overview

This guide walks you through migrating the `ResponseAssessment` table from a polymorphic design to three specialized fact tables:

- **Before**: 1 table with mixed imaging, molecular, and clinical data (sparse columns, ambiguous grain)
- **After**: 3 specialized tables with clear purpose and dense columns

## Target Schema

### ImagingResponse
**Grain**: One row per imaging study with RECIST assessment  
**FK**: imaging_study_id (REQUIRED), patient_id, treatment_id (nullable)  
**Measures**: recist_response, sum_target_lesions_mm, percent_change_from_baseline

### MolecularResponse
**Grain**: One row per molecular test with ctDNA assessment  
**FK**: molecular_test_id (REQUIRED), patient_id, treatment_id (nullable)  
**Measures**: ctdna_vaf_percent, ctdna_tumor_fraction_percent, ctdna_mutation_cleared

### ClinicalResponse
**Grain**: One row per clinical outcome event  
**FK**: patient_id, treatment_id (nullable)  
**Measures**: progression_detected, progression_type, resistance_mechanism, histologic_transformation

---

## Prerequisites

1. **Python 3.10+** with SQLite3 support
2. **Virtual environment activated**:
   ```bash
   source .venv/Scripts/activate  # Windows Git Bash
   # or
   .venv\Scripts\activate  # Windows CMD
   ```
3. **Database backup** (done automatically by migration script)
4. **No active database connections** (close any DB browsers)

---

## Migration Steps

### Step 1: Pre-Migration Validation

**Run the validation script to understand your current data:**

```bash
python scripts/validate_pre_migration.py
```

**What it does:**
- Counts rows by data type (imaging, molecular, clinical)
- Identifies polymorphic rows (rows with multiple data types)
- Checks NULL sparsity (why polymorphism is bad)
- Validates foreign key integrity
- Shows sample rows that will be split
- Generates a JSON report

**Expected Output:**
```
======================================================================
DATA DISTRIBUTION ANALYSIS
======================================================================

Total ResponseAssessment rows: 25

By Foreign Key Presence:
  - With imaging_study_id: 20 (80.0%)
  - With molecular_test_id: 15 (60.0%)

By Data Content:
  - Has imaging data (RECIST): 18 (72.0%)
  - Has molecular data (ctDNA): 12 (48.0%)
  - Has clinical event: 5 (20.0%)

----------------------------------------------------------------------
MIGRATION TARGET (rows that meet criteria):
----------------------------------------------------------------------
  → ImagingResponse: 18 rows
  → MolecularResponse: 12 rows
  → ClinicalResponse: 5 rows
```

**Review the report:**
- Check that foreign key integrity is valid (✓ All foreign keys valid)
- Note how many rows will migrate to each table
- Understand overlaps (rows appearing in multiple new tables)

**⚠️ DO NOT PROCEED if foreign key violations are found!**

---

### Step 2: Run Migration

**Execute the migration script:**

```bash
python scripts/migrate_response_tables.py
```

**What it does:**
1. **Checks database exists** and validates preconditions
2. **Creates automatic backup**: `clinical_data_pre_migration_YYYYMMDD_HHMMSS.db`
3. **Creates 3 new tables**: ImagingResponse, MolecularResponse, ClinicalResponse
4. **Creates 9 indexes** for query performance
5. **Migrates data** from ResponseAssessment to new tables
6. **Validates migration** (row counts, FK integrity)
7. **Archives old table** to CSV
8. **Asks for confirmation** before dropping ResponseAssessment

**Interactive Prompts:**

```
======================================================================
READY TO MIGRATE
======================================================================
This will create 3 new tables and eventually drop ResponseAssessment.
Backup created at: backend/clinical_data_pre_migration_20260430_143022.db

Proceed with migration? (yes/no):
```

Type `yes` and press Enter.

After validation passes:

```
======================================================================
VALIDATION PASSED - READY TO DROP OLD TABLE
======================================================================

Drop ResponseAssessment table? (yes/no):
```

Type `yes` to drop, or `no` to keep for manual inspection.

**Expected Output:**
```
======================================================================
MIGRATION COMPLETED SUCCESSFULLY
======================================================================
  ✓ ImagingResponse: 18 rows
  ✓ MolecularResponse: 12 rows
  ✓ ClinicalResponse: 5 rows
  ✓ Backup: backend/clinical_data_pre_migration_20260430_143022.db
```

---

### Step 3: Verify Migration

**Check the new tables exist and have data:**

```bash
python -c "
import sqlite3
conn = sqlite3.connect('backend/clinical_data.db')
cursor = conn.cursor()

tables = ['ImagingResponse', 'MolecularResponse', 'ClinicalResponse']
for table in tables:
    cursor.execute(f'SELECT COUNT(*) FROM {table}')
    count = cursor.fetchone()[0]
    print(f'{table}: {count} rows')

conn.close()
"
```

**Expected Output:**
```
ImagingResponse: 18 rows
MolecularResponse: 12 rows
ClinicalResponse: 5 rows
```

**Check foreign key integrity:**

```bash
python -c "
import sqlite3
conn = sqlite3.connect('backend/clinical_data.db')
conn.execute('PRAGMA foreign_keys = ON')
cursor = conn.cursor()

for table in ['ImagingResponse', 'MolecularResponse', 'ClinicalResponse']:
    cursor.execute(f'PRAGMA foreign_key_check({table})')
    violations = cursor.fetchall()
    if violations:
        print(f'{table}: {len(violations)} FK violations!')
    else:
        print(f'{table}: ✓ FK integrity valid')

conn.close()
"
```

**Expected Output:**
```
ImagingResponse: ✓ FK integrity valid
MolecularResponse: ✓ FK integrity valid
ClinicalResponse: ✓ FK integrity valid
```

---

### Step 4: Test Backend API (If Running)

**If your FastAPI backend is running, test the endpoints:**

```bash
# Start backend (if not already running)
cd backend
uvicorn app.main:app --reload
```

In another terminal:

```bash
# Test timeline endpoint (uses ImagingResponse)
curl http://localhost:8000/api/patients/NGDX-001/timeline | jq '.recist_series | length'

# Expected: Number of imaging timepoints for patient NGDX-001
```

**⚠️ Note**: The API endpoints in `backend/app/api/` may need updates to query the new tables. This is covered in the next section.

---

## Post-Migration Tasks

### Update Backend API Endpoints

The following files need updates to use the new tables:

#### 1. `backend/app/api/timeline.py`

**Change** (around line 191-203):

```python
# OLD
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

# NEW
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

#### 2. `backend/app/api/patients.py`

**Replace the `/patients/{patient_id}/response` endpoint** (around line 355-408) with:

```python
@router.get("/patients/{patient_id}/response")
async def get_response_assessments(patient_id: str) -> Dict[str, Any]:
    """
    Get all response assessments for a patient (aggregated from 3 fact tables)
    """
    from app.database import execute_query, execute_query_one

    # Check patient exists
    patient_check = execute_query_one(
        "SELECT patient_id FROM Patient WHERE patient_id = ?",
        (patient_id,)
    )
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

    # Get clinical responses
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

#### 3. `backend/app/database.py`

**Update the table list** (around line 79):

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

---

## Rollback Procedure

If migration fails or produces incorrect results:

### Option 1: Restore from Automatic Backup

```bash
# Find the backup file
ls -lh backend/clinical_data_pre_migration_*.db

# Restore (replace TIMESTAMP with actual timestamp)
cp backend/clinical_data_pre_migration_YYYYMMDD_HHMMSS.db backend/clinical_data.db
```

### Option 2: Restore from Archive

```bash
# The migration script archives ResponseAssessment to CSV before dropping
ls -lh example_files/archive/response_assessment_backup_*.csv

# To restore, you'll need to:
# 1. Restore database from backup (Option 1)
# 2. Or manually recreate ResponseAssessment and import CSV
```

---

## Troubleshooting

### Issue: "ResponseAssessment table not found"

**Cause**: Migration already completed or table was manually dropped.

**Solution**: Check if new tables exist:
```bash
python -c "import sqlite3; conn = sqlite3.connect('backend/clinical_data.db'); 
cursor = conn.cursor(); 
cursor.execute(\"SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%Response'\"); 
print(cursor.fetchall())"
```

If new tables exist, migration is already done.

---

### Issue: "Foreign key violations detected"

**Cause**: Orphaned foreign keys in ResponseAssessment.

**Solution**:
1. Run `validate_pre_migration.py` to identify which FKs are orphaned
2. Fix orphaned references manually or delete invalid rows
3. Re-run migration

**Example fix** (delete rows with invalid imaging_study_id):
```bash
python -c "
import sqlite3
conn = sqlite3.connect('backend/clinical_data.db')
cursor = conn.cursor()

# Find orphaned rows
cursor.execute('''
    SELECT assessment_id, imaging_study_id 
    FROM ResponseAssessment ra
    WHERE ra.imaging_study_id IS NOT NULL
      AND NOT EXISTS (
          SELECT 1 FROM ImagingStudy i
          WHERE i.imaging_study_id = ra.imaging_study_id
      )
''')
orphans = cursor.fetchall()
print(f'Found {len(orphans)} orphaned rows')

# Delete them (CAREFUL!)
if len(orphans) > 0:
    response = input('Delete these rows? (yes/no): ')
    if response == 'yes':
        cursor.execute('''
            DELETE FROM ResponseAssessment
            WHERE imaging_study_id IS NOT NULL
              AND NOT EXISTS (
                  SELECT 1 FROM ImagingStudy i
                  WHERE i.imaging_study_id = imaging_study_id
              )
        ''')
        conn.commit()
        print(f'Deleted {len(orphans)} rows')

conn.close()
"
```

---

### Issue: "Row count mismatch after migration"

**Cause**: Migration script filtering criteria may be too strict.

**Solution**:
1. Check the validation output to see expected vs actual counts
2. Review the migration script's WHERE clauses
3. If intentional (some rows don't qualify), this is expected
4. If unintentional, restore from backup and report the issue

---

## Data Quality Checks

After migration, run these checks:

### Check 1: No Orphaned ImagingResponse Records

```bash
python -c "
import sqlite3
conn = sqlite3.connect('backend/clinical_data.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT COUNT(*) FROM ImagingResponse ir
    WHERE NOT EXISTS (
        SELECT 1 FROM ImagingStudy i
        WHERE i.imaging_study_id = ir.imaging_study_id
    )
''')
print(f'Orphaned ImagingResponse rows: {cursor.fetchone()[0]} (should be 0)')
conn.close()
"
```

### Check 2: No Orphaned MolecularResponse Records

```bash
python -c "
import sqlite3
conn = sqlite3.connect('backend/clinical_data.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT COUNT(*) FROM MolecularResponse mr
    WHERE NOT EXISTS (
        SELECT 1 FROM MolecularTest mt
        WHERE mt.molecular_test_id = mr.molecular_test_id
    )
''')
print(f'Orphaned MolecularResponse rows: {cursor.fetchone()[0]} (should be 0)')
conn.close()
"
```

### Check 3: Date Alignment (Imaging)

```bash
python -c "
import sqlite3
conn = sqlite3.connect('backend/clinical_data.db')
cursor = conn.cursor()

cursor.execute('''
    SELECT 
        ir.imaging_response_id,
        ir.assessment_date,
        i.scan_date,
        julianday(ir.assessment_date) - julianday(i.scan_date) as day_diff
    FROM ImagingResponse ir
    JOIN ImagingStudy i ON ir.imaging_study_id = i.imaging_study_id
    WHERE ABS(julianday(ir.assessment_date) - julianday(i.scan_date)) > 7
''')

rows = cursor.fetchall()
if rows:
    print(f'⚠ {len(rows)} imaging responses with assessment_date > 7 days from scan_date')
    print('This may indicate delayed radiology reads (expected for some cases)')
else:
    print('✓ All imaging response dates align with scan dates (±7 days)')

conn.close()
"
```

---

## Next Steps After Migration

1. **Update LinkML Schema**: Add the 3 new classes (ImagingResponse, MolecularResponse, ClinicalResponse) and deprecate ResponseAssessment
2. **Regenerate Python Models**: Run LinkML generators to create new Pydantic models
3. **Update Frontend Types**: Add TypeScript interfaces for the new response types
4. **Update Tests**: Modify any tests that query ResponseAssessment
5. **Update Documentation**: Update any README or docs mentioning ResponseAssessment

See `RESPONSE_TABLE_REFACTOR_SPEC.md` for detailed steps 1-8.

---

## Summary

✅ **What the migration does:**
- Splits 1 polymorphic table into 3 specialized tables
- Preserves all data (rows may appear in multiple tables if they have multiple data types)
- Creates automatic backup before changes
- Validates foreign key integrity before and after
- Archives old table to CSV before dropping

✅ **What you need to do:**
1. Run `validate_pre_migration.py` to understand your data
2. Run `migrate_response_tables.py` and confirm prompts
3. Verify migration with the checks above
4. Update backend API endpoints
5. Test your application

✅ **Safety features:**
- Automatic database backup
- Pre-migration validation
- Post-migration validation
- Interactive confirmation prompts
- Transaction rollback on any error
- CSV archive of old table

---

## Support

If you encounter issues not covered in this guide:

1. Check the backup files in `backend/` (pre_migration backups)
2. Check the archive in `example_files/archive/` (CSV backups)
3. Review the validation report at `example_files/archive/pre_migration_report.json`
4. Restore from backup if needed
5. Report the issue with the validation report attached

---

**Migration Version**: 1.0  
**Last Updated**: 2026-04-30  
**Tested With**: SQLite 3.43+, Python 3.10+