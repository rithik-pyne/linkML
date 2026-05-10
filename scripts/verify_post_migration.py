#!/usr/bin/env python3
"""
Post-migration verification script

Comprehensive validation of the ResponseAssessment → 3 tables migration.
Run this AFTER migrating to ensure data integrity and correctness.

Checks:
1. New tables exist with expected schema
2. Row counts match pre-migration expectations
3. No orphaned foreign keys
4. Primary keys are unique
5. Required fields are not NULL
6. Date alignment with source tables
7. Sample data spot checks

Author: Migration validation
Date: 2026-04-30
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
import json

DB_PATH = Path(__file__).parent.parent / "backend" / "clinical_data.db"
REPORT_PATH = Path(__file__).parent.parent / "example_files" / "archive" / "pre_migration_report.json"


def load_pre_migration_stats() -> Dict:
    """Load pre-migration statistics if available"""
    if REPORT_PATH.exists():
        with open(REPORT_PATH, 'r') as f:
            return json.load(f)
    return {}


def check_tables_exist(conn: sqlite3.Connection) -> bool:
    """Verify all 3 new tables exist"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("TABLE EXISTENCE CHECK")
    print("="*70)

    expected_tables = ['ImagingResponse', 'MolecularResponse', 'ClinicalResponse']
    all_exist = True

    for table in expected_tables:
        cursor.execute(f"""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='{table}'
        """)
        exists = cursor.fetchone()[0] > 0

        if exists:
            print(f"  ✓ {table} exists")
        else:
            print(f"  ✗ {table} NOT FOUND")
            all_exist = False

    # Check if old table still exists
    cursor.execute("""
        SELECT COUNT(*) FROM sqlite_master
        WHERE type='table' AND name='ResponseAssessment'
    """)
    old_exists = cursor.fetchone()[0] > 0

    if old_exists:
        print(f"  ⚠ ResponseAssessment still exists (was not dropped)")
    else:
        print(f"  ✓ ResponseAssessment successfully dropped")

    return all_exist


def check_row_counts(conn: sqlite3.Connection, pre_stats: Dict) -> bool:
    """Verify row counts match expectations"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("ROW COUNT VERIFICATION")
    print("="*70)

    tables = {
        'ImagingResponse': 'to_imaging',
        'MolecularResponse': 'to_molecular',
        'ClinicalResponse': 'to_clinical'
    }

    all_match = True

    for table, stat_key in tables.items():
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        actual_count = cursor.fetchone()[0]

        expected_count = pre_stats.get('stats', {}).get(stat_key, '?')

        if expected_count != '?':
            match = actual_count == expected_count
            status = "✓" if match else "✗"
            print(f"  {status} {table}: {actual_count} rows (expected: {expected_count})")

            if not match:
                all_match = False
                diff = actual_count - expected_count
                print(f"      ⚠ Difference: {diff:+d} rows")
        else:
            print(f"  ? {table}: {actual_count} rows (no pre-migration data to compare)")

    return all_match


def check_foreign_key_integrity(conn: sqlite3.Connection) -> bool:
    """Check all foreign keys are valid"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("FOREIGN KEY INTEGRITY CHECK")
    print("="*70)

    tables = ['ImagingResponse', 'MolecularResponse', 'ClinicalResponse']
    all_valid = True

    for table in tables:
        cursor.execute(f"PRAGMA foreign_key_check({table})")
        violations = cursor.fetchall()

        if violations:
            print(f"  ✗ {table}: {len(violations)} FK violations!")
            all_valid = False

            # Show first 3 violations
            for i, violation in enumerate(violations[:3]):
                print(f"      - Row: {violation}")
        else:
            print(f"  ✓ {table}: No FK violations")

    return all_valid


def check_primary_key_uniqueness(conn: sqlite3.Connection) -> bool:
    """Verify all primary keys are unique (no duplicates)"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("PRIMARY KEY UNIQUENESS CHECK")
    print("="*70)

    checks = [
        ('ImagingResponse', 'imaging_response_id'),
        ('MolecularResponse', 'molecular_response_id'),
        ('ClinicalResponse', 'clinical_response_id')
    ]

    all_unique = True

    for table, pk_col in checks:
        # Check for duplicates
        cursor.execute(f"""
            SELECT {pk_col}, COUNT(*) as dup_count
            FROM {table}
            GROUP BY {pk_col}
            HAVING COUNT(*) > 1
        """)

        duplicates = cursor.fetchall()

        if duplicates:
            print(f"  ✗ {table}.{pk_col}: {len(duplicates)} duplicate IDs!")
            all_unique = False

            for dup in duplicates[:3]:
                print(f"      - ID '{dup[0]}' appears {dup[1]} times")
        else:
            print(f"  ✓ {table}.{pk_col}: All unique")

    return all_unique


def check_required_fields(conn: sqlite3.Connection) -> bool:
    """Check that required fields are not NULL"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("REQUIRED FIELDS CHECK (NOT NULL)")
    print("="*70)

    checks = [
        ('ImagingResponse', [
            'imaging_response_id',
            'imaging_study_id',
            'patient_id',
            'assessment_date'
        ]),
        ('MolecularResponse', [
            'molecular_response_id',
            'molecular_test_id',
            'patient_id',
            'assessment_date'
        ]),
        ('ClinicalResponse', [
            'clinical_response_id',
            'patient_id',
            'event_date',
            'event_type',
            'progression_detected'
        ])
    ]

    all_valid = True

    for table, required_cols in checks:
        print(f"\n{table}:")

        for col in required_cols:
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE {col} IS NULL")
            null_count = cursor.fetchone()[0]

            if null_count > 0:
                print(f"  ✗ {col}: {null_count} NULL values (should be 0)")
                all_valid = False
            else:
                print(f"  ✓ {col}: No NULL values")

    return all_valid


def check_source_fk_links(conn: sqlite3.Connection) -> bool:
    """Verify all response records link to valid source records"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("SOURCE TABLE LINKAGE CHECK")
    print("="*70)

    # Check ImagingResponse → ImagingStudy
    cursor.execute("""
        SELECT COUNT(*) FROM ImagingResponse ir
        WHERE NOT EXISTS (
            SELECT 1 FROM ImagingStudy i
            WHERE i.imaging_study_id = ir.imaging_study_id
        )
    """)
    orphaned_imaging = cursor.fetchone()[0]

    # Check MolecularResponse → MolecularTest
    cursor.execute("""
        SELECT COUNT(*) FROM MolecularResponse mr
        WHERE NOT EXISTS (
            SELECT 1 FROM MolecularTest mt
            WHERE mt.molecular_test_id = mr.molecular_test_id
        )
    """)
    orphaned_molecular = cursor.fetchone()[0]

    all_valid = True

    if orphaned_imaging > 0:
        print(f"  ✗ ImagingResponse: {orphaned_imaging} orphaned records (no matching ImagingStudy)")
        all_valid = False
    else:
        print(f"  ✓ ImagingResponse: All records link to valid ImagingStudy")

    if orphaned_molecular > 0:
        print(f"  ✗ MolecularResponse: {orphaned_molecular} orphaned records (no matching MolecularTest)")
        all_valid = False
    else:
        print(f"  ✓ MolecularResponse: All records link to valid MolecularTest")

    # Clinical responses don't link to a specific source, so no check needed
    print(f"  ℹ ClinicalResponse: No source FK (by design)")

    return all_valid


def check_date_alignment(conn: sqlite3.Connection):
    """Check that response dates align with source test dates"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("DATE ALIGNMENT CHECK")
    print("="*70)

    # Check ImagingResponse assessment_date vs ImagingStudy scan_date
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN ABS(julianday(ir.assessment_date) - julianday(i.scan_date)) <= 7 THEN 1 ELSE 0 END) as within_7_days,
            SUM(CASE WHEN ABS(julianday(ir.assessment_date) - julianday(i.scan_date)) > 7 THEN 1 ELSE 0 END) as beyond_7_days
        FROM ImagingResponse ir
        JOIN ImagingStudy i ON ir.imaging_study_id = i.imaging_study_id
    """)

    row = cursor.fetchone()
    total, within_7, beyond_7 = row

    print(f"\nImagingResponse assessment_date vs ImagingStudy scan_date:")
    print(f"  - Total imaging responses: {total}")
    print(f"  - Within ±7 days: {within_7} ({within_7/total*100:.1f}%)")
    print(f"  - Beyond ±7 days: {beyond_7} ({beyond_7/total*100:.1f}%)")

    if beyond_7 > 0:
        print(f"  ℹ {beyond_7} responses have delayed assessment dates (>7 days after scan)")
        print(f"    This may indicate delayed radiology reads (expected in some cases)")

    # Check MolecularResponse assessment_date vs MolecularTest test_date
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN ABS(julianday(mr.assessment_date) - julianday(mt.test_date)) <= 7 THEN 1 ELSE 0 END) as within_7_days,
            SUM(CASE WHEN ABS(julianday(mr.assessment_date) - julianday(mt.test_date)) > 7 THEN 1 ELSE 0 END) as beyond_7_days
        FROM MolecularResponse mr
        JOIN MolecularTest mt ON mr.molecular_test_id = mt.molecular_test_id
    """)

    row = cursor.fetchone()
    total, within_7, beyond_7 = row

    print(f"\nMolecularResponse assessment_date vs MolecularTest test_date:")
    print(f"  - Total molecular responses: {total}")
    print(f"  - Within ±7 days: {within_7} ({within_7/total*100:.1f}%)")
    print(f"  - Beyond ±7 days: {beyond_7} ({beyond_7/total*100:.1f}%)")


def check_id_format(conn: sqlite3.Connection) -> bool:
    """Verify ID format matches expected pattern"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("ID FORMAT CHECK")
    print("="*70)

    # Expected patterns: IR-XXX-YYY, MR-XXX-YYY, CR-XXX-YYY
    checks = [
        ('ImagingResponse', 'imaging_response_id', r'^IR-[0-9]{3}-[0-9]{3}$'),
        ('MolecularResponse', 'molecular_response_id', r'^MR-[0-9]{3}-[0-9]{3}$'),
        ('ClinicalResponse', 'clinical_response_id', r'^CR-[0-9]{3}-[0-9]{3}$')
    ]

    all_valid = True

    for table, id_col, pattern in checks:
        # SQLite doesn't have REGEXP by default, so check format manually
        cursor.execute(f"""
            SELECT COUNT(*) FROM {table}
            WHERE length({id_col}) != 11
               OR substr({id_col}, 1, 3) NOT IN ('IR-', 'MR-', 'CR-')
               OR substr({id_col}, 4, 3) NOT GLOB '[0-9][0-9][0-9]'
               OR substr({id_col}, 7, 1) != '-'
               OR substr({id_col}, 8, 3) NOT GLOB '[0-9][0-9][0-9]'
        """)

        invalid_count = cursor.fetchone()[0]

        if invalid_count > 0:
            print(f"  ✗ {table}.{id_col}: {invalid_count} IDs with invalid format")
            all_valid = False
        else:
            print(f"  ✓ {table}.{id_col}: All IDs match expected format")

    return all_valid


def sample_data_spot_check(conn: sqlite3.Connection):
    """Show sample records from each table"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("SAMPLE DATA SPOT CHECK")
    print("="*70)

    # Sample ImagingResponse
    cursor.execute("""
        SELECT
            ir.imaging_response_id,
            ir.patient_id,
            ir.assessment_date,
            ir.recist_response,
            ir.sum_target_lesions_mm
        FROM ImagingResponse ir
        ORDER BY ir.assessment_date DESC
        LIMIT 3
    """)

    print("\nImagingResponse (3 most recent):")
    print("-" * 70)
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Patient: {row[1]}, Date: {row[2]}, RECIST: {row[3]}, Sum: {row[4]}mm")

    # Sample MolecularResponse
    cursor.execute("""
        SELECT
            mr.molecular_response_id,
            mr.patient_id,
            mr.assessment_date,
            mr.ctdna_vaf_percent,
            mr.ctdna_mutation_cleared
        FROM MolecularResponse mr
        ORDER BY mr.assessment_date DESC
        LIMIT 3
    """)

    print("\nMolecularResponse (3 most recent):")
    print("-" * 70)
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Patient: {row[1]}, Date: {row[2]}, VAF: {row[3]}%, Cleared: {row[4]}")

    # Sample ClinicalResponse
    cursor.execute("""
        SELECT
            cr.clinical_response_id,
            cr.patient_id,
            cr.event_date,
            cr.event_type,
            cr.progression_detected,
            cr.resistance_mechanism
        FROM ClinicalResponse cr
        ORDER BY cr.event_date DESC
        LIMIT 3
    """)

    print("\nClinicalResponse (3 most recent):")
    print("-" * 70)
    for row in cursor.fetchall():
        print(f"  ID: {row[0]}, Patient: {row[1]}, Date: {row[2]}, Type: {row[3]}, Prog: {row[4]}, Mech: {row[5]}")


def check_indexes(conn: sqlite3.Connection) -> bool:
    """Verify indexes were created"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("INDEX CHECK")
    print("="*70)

    expected_indexes = [
        'idx_imaging_response_patient',
        'idx_imaging_response_treatment',
        'idx_imaging_response_date',
        'idx_molecular_response_patient',
        'idx_molecular_response_treatment',
        'idx_molecular_response_date',
        'idx_clinical_response_patient',
        'idx_clinical_response_treatment',
        'idx_clinical_response_date'
    ]

    all_exist = True

    for idx_name in expected_indexes:
        cursor.execute(f"""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='index' AND name='{idx_name}'
        """)
        exists = cursor.fetchone()[0] > 0

        if exists:
            print(f"  ✓ {idx_name}")
        else:
            print(f"  ✗ {idx_name} NOT FOUND")
            all_exist = False

    return all_exist


def main():
    """Run all post-migration verification checks"""
    print("="*70)
    print("POST-MIGRATION VERIFICATION")
    print("ResponseAssessment → 3 Specialized Tables")
    print("="*70)

    if not DB_PATH.exists():
        print(f"\n✗ Database not found at {DB_PATH}")
        return

    # Load pre-migration stats if available
    pre_stats = load_pre_migration_stats()

    if pre_stats:
        print(f"\nℹ Loaded pre-migration statistics from {REPORT_PATH}")
    else:
        print(f"\n⚠ No pre-migration report found - some checks will be skipped")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        # Run all checks
        checks_passed = []
        checks_failed = []

        # Check 1: Tables exist
        result = check_tables_exist(conn)
        if result:
            checks_passed.append("Table existence")
        else:
            checks_failed.append("Table existence")
            print("\n✗ Migration appears incomplete - new tables not found")
            return

        # Check 2: Row counts
        if pre_stats:
            result = check_row_counts(conn, pre_stats)
            if result:
                checks_passed.append("Row counts")
            else:
                checks_failed.append("Row counts")

        # Check 3: FK integrity
        result = check_foreign_key_integrity(conn)
        if result:
            checks_passed.append("Foreign key integrity")
        else:
            checks_failed.append("Foreign key integrity")

        # Check 4: PK uniqueness
        result = check_primary_key_uniqueness(conn)
        if result:
            checks_passed.append("Primary key uniqueness")
        else:
            checks_failed.append("Primary key uniqueness")

        # Check 5: Required fields
        result = check_required_fields(conn)
        if result:
            checks_passed.append("Required fields")
        else:
            checks_failed.append("Required fields")

        # Check 6: Source linkage
        result = check_source_fk_links(conn)
        if result:
            checks_passed.append("Source table linkage")
        else:
            checks_failed.append("Source table linkage")

        # Check 7: Date alignment (informational only)
        check_date_alignment(conn)

        # Check 8: ID format
        result = check_id_format(conn)
        if result:
            checks_passed.append("ID format")
        else:
            checks_failed.append("ID format")

        # Check 9: Indexes
        result = check_indexes(conn)
        if result:
            checks_passed.append("Indexes")
        else:
            checks_failed.append("Indexes")

        # Check 10: Sample data
        sample_data_spot_check(conn)

        # Summary
        print("\n" + "="*70)
        print("VERIFICATION SUMMARY")
        print("="*70)

        print(f"\n✓ Passed: {len(checks_passed)} checks")
        for check in checks_passed:
            print(f"    - {check}")

        if checks_failed:
            print(f"\n✗ Failed: {len(checks_failed)} checks")
            for check in checks_failed:
                print(f"    - {check}")

            print("\n⚠ MIGRATION VERIFICATION FAILED")
            print("Review the failures above and consider restoring from backup.")
        else:
            print("\n" + "="*70)
            print("✓ ALL CHECKS PASSED - MIGRATION SUCCESSFUL")
            print("="*70)
            print("\nNext steps:")
            print("  1. Update backend API endpoints (see MIGRATION_GUIDE.md)")
            print("  2. Update LinkML schema")
            print("  3. Regenerate Python/TypeScript models")
            print("  4. Update tests")

    except sqlite3.OperationalError as e:
        print(f"\n✗ Database error: {e}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()