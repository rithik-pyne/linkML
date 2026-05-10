# LinkML Schema Changelog

## Version 2.0.0 (2026-04-30) - ResponseAssessment Refactor

### Breaking Changes

**ResponseAssessment class deprecated** and replaced with three specialized response classes:

1. **ImagingResponse** - RECIST-based imaging assessments
2. **MolecularResponse** - ctDNA/VAF molecular tracking
3. **ClinicalResponse** - Clinical outcome events (progression, resistance, transformation)

### Added Classes

#### ImagingResponse
- **Grain**: One row per imaging study with RECIST assessment
- **Primary Key**: `imaging_response_id` (format: `IR-XXX-XXX`)
- **Required FKs**: `imaging_study_id`, `patient_id`
- **Optional FK**: `treatment_id` (nullable for baseline scans)
- **Measures**: `recist_response`, `sum_target_lesions_mm`, `percent_change_from_baseline`, `new_lesions_present`

**Purpose**: Tracks radiographic response to treatment using RECIST criteria over time.

#### MolecularResponse
- **Grain**: One row per molecular test with ctDNA assessment
- **Primary Key**: `molecular_response_id` (format: `MR-XXX-XXX`)
- **Required FKs**: `molecular_test_id`, `patient_id`
- **Optional FK**: `treatment_id` (nullable for baseline tests)
- **Measures**: `ctdna_vaf_percent`, `ctdna_tumor_fraction_percent`, `ctdna_mutation_cleared`

**Purpose**: Tracks molecular response via serial ctDNA monitoring and VAF trend analysis.

#### ClinicalResponse
- **Grain**: One row per clinical outcome event
- **Primary Key**: `clinical_response_id` (format: `CR-XXX-XXX`)
- **Required FK**: `patient_id`
- **Optional FK**: `treatment_id` (nullable for post-treatment events)
- **Event Data**: `event_type`, `progression_detected`, `progression_type`, `time_to_progression_months`, `resistance_mutation_detected`, `resistance_mechanism`, `histologic_transformation`

**Purpose**: Documents clinical outcome events (progression, resistance, transformation) as determined by MDT consensus.

### Added Slots

| Slot | Type | Pattern | Description |
|------|------|---------|-------------|
| `imaging_response_id` | string | `^IR-[0-9]{3}-[0-9]{3}$` | Primary key for ImagingResponse |
| `molecular_response_id` | string | `^MR-[0-9]{3}-[0-9]{3}$` | Primary key for MolecularResponse |
| `clinical_response_id` | string | `^CR-[0-9]{3}-[0-9]{3}$` | Primary key for ClinicalResponse |
| `event_date` | date | - | Date clinical event was documented |
| `event_type` | ClinicalEventTypeEnum | - | Type of clinical event |

### Added Enums

#### ClinicalEventTypeEnum
Defines the type of clinical outcome event documented in ClinicalResponse.

**Values**:
- `Progression` - Disease progression event
- `Resistance` - Resistance mechanism detected
- `Transformation` - Histologic transformation (e.g., SCLC transformation)

### Deprecated Elements

#### ResponseAssessment (class)
- **Status**: DEPRECATED v2.0
- **Replacement**: Use `ImagingResponse`, `MolecularResponse`, or `ClinicalResponse`
- **Reason**: Polymorphic design with mixed imaging/molecular/clinical data caused:
  - Ambiguous grain (unclear what each row represents)
  - Sparse columns (50%+ NULL values in most rows)
  - Fragile FKs (optional links made lineage unclear)
  - Complex queries (filtering NULLs required for time-series)

**Migration**: See `RESPONSE_TABLE_REFACTOR_SPEC.md` and `MIGRATION_GUIDE.md`

### Design Rationale

The refactor follows **dimensional modeling best practices**:

1. **Explicit Grain**: Each new table has ONE clearly defined grain statement
2. **Conformed Dimensions**: Patient and Treatment dimensions shared across all response facts
3. **Source Lineage**: Every response links to its originating source fact (imaging_study_id, molecular_test_id)
4. **Dense Columns**: Specialized tables eliminate NULL-heavy polymorphism
5. **Drill-Across Queries**: Compare imaging vs molecular response via shared Patient dimension, not direct fact-to-fact joins

### Query Pattern Changes

#### ❌ Old Pattern (Mixed Data)
```sql
SELECT 
    recist_response,
    ctdna_vaf_percent,
    progression_detected
FROM ResponseAssessment
WHERE patient_id = 'NGDX-001'
-- Problem: Mixed data types in single row
-- Problem: Many NULLs (sparse columns)
```

#### ✅ New Pattern (Drill-Across)
```sql
-- Query 1: Imaging
SELECT assessment_date, recist_response
FROM ImagingResponse
WHERE patient_id = 'NGDX-001';

-- Query 2: Molecular
SELECT assessment_date, ctdna_vaf_percent
FROM MolecularResponse
WHERE patient_id = 'NGDX-001';

-- Query 3: Clinical events
SELECT event_date, event_type, progression_detected
FROM ClinicalResponse
WHERE patient_id = 'NGDX-001';

-- Merge in application layer with fuzzy date matching (±7 days)
```

### Backward Compatibility

**Breaking Change**: Applications querying `ResponseAssessment` must be updated.

**Migration Path**:
1. Run `scripts/migrate_response_tables.py` to split existing data
2. Update application queries to use new tables
3. Update LinkML-generated models (Pydantic, TypeScript, etc.)
4. ResponseAssessment can be dropped after validation

**Rollback**: Restore from automatic backup created by migration script.

### Data Migration

**Migration Script**: `scripts/migrate_response_tables.py`

**What it does**:
- Splits ResponseAssessment rows based on data content:
  - Rows with `imaging_study_id` + RECIST data → ImagingResponse
  - Rows with `molecular_test_id` + ctDNA data → MolecularResponse
  - Rows with progression/resistance events → ClinicalResponse
- Rows with multiple data types appear in multiple new tables (expected behavior)
- Preserves all data with foreign key validation
- Creates automatic backup before changes

**Expected Results**:
- ~18-20 ImagingResponse rows per 25 ResponseAssessment rows
- ~12-15 MolecularResponse rows per 25 ResponseAssessment rows
- ~5 ClinicalResponse rows per 25 ResponseAssessment rows
- Total > original due to splitting polymorphic rows

### Impact on Generated Artifacts

The following artifacts need regeneration:

1. **SQL DDL**: Run `gen-pydantic` or equivalent SQL generator
2. **Python Models**: Run `gen-pydantic schemas/clinical_model.yaml`
3. **TypeScript Types**: Update frontend type definitions
4. **ER Diagrams**: Regenerate to show new relationships
5. **Documentation**: Run `gen-markdown` for updated docs

### Testing Recommendations

After schema update:

1. ✅ Validate schema: `linkml-lint schemas/clinical_model.yaml`
2. ✅ Load schema in Python: `SchemaView('schemas/clinical_model.yaml')`
3. ✅ Verify new classes present: Check `all_classes()` contains new response classes
4. ✅ Verify enum present: Check `ClinicalEventTypeEnum` exists
5. ✅ Run migration script: `python scripts/migrate_response_tables.py`
6. ✅ Verify migration: `python scripts/verify_post_migration.py`
7. ✅ Update API endpoints: See `MIGRATION_GUIDE.md`
8. ✅ Test API: Verify `/patients/{id}/timeline` and `/patients/{id}/response` work

### References

- **Technical Spec**: `RESPONSE_TABLE_REFACTOR_SPEC.md`
- **Migration Guide**: `MIGRATION_GUIDE.md`
- **Quick Reference**: `MIGRATION_QUICK_REF.md`
- **System Architecture**: `00-SYSTEM-SPEC.md`

---

## Version 1.0.0 (Initial Release)

Initial release with galaxy schema design:
- Patient (dimension)
- ImagingStudy, Biopsy, MolecularTest, Mutation, Treatment, ResponseAssessment, ClinicalAssessment (facts)
- 18 enums for controlled vocabularies
- 130+ slots for clinical data capture