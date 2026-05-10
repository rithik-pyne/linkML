#!/usr/bin/env python3
"""
Database migration script: ResponseAssessment → 3 new fact tables

Migrates data from the polymorphic ResponseAssessment table into:
  - ImagingResponse (RECIST-based imaging assessments)
  - MolecularResponse (ctDNA/VAF molecular assessments)
  - ClinicalResponse (progression/resistance clinical events)

Author: Migration refactor
Date: 2026-04-30
Version: 1.0
"""

import sqlite3
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Path configuration
DB_PATH = Path(__file__).parent.parent / "backend" / "clinical_data.db"
BACKUP_DIR = Path(__file__).parent.parent / "example_files" / "archive"

# Ensure backup directory exists
BACKUP_DIR.mkdir(parents=True, exist_ok=True)


def check_sqlite_version(conn: sqlite3.Connection) -> Tuple[int, int, int]:
    """Check SQLite version and return as tuple (major, minor, patch)"""
    cursor = conn.cursor()
    cursor.execute("SELECT sqlite_version()")
    version_str = cursor.fetchone()[0]
    major, minor, patch = map(int, version_str.split('.'))
    print(f"[INFO] SQLite version: {version_str}")
    return (major, minor, patch)


def validate_preconditions(conn: sqlite3.Connection) -> Dict[str, int]:
    """Validate database state before migration"""
    cursor = conn.cursor()

    print("\n[STEP] Validating preconditions...")

    # Check if ResponseAssessment exists
    cursor.execute("""
        SELECT COUNT(*) FROM sqlite_master
        WHERE type='table' AND name='ResponseAssessment'
    """)
    if cursor.fetchone()[0] == 0:
        raise ValueError("ResponseAssessment table not found - migration already completed?")

    # Check if new tables already exist
    for table in ['ImagingResponse', 'MolecularResponse', 'ClinicalResponse']:
        cursor.execute(f"""
            SELECT COUNT(*) FROM sqlite_master
            WHERE type='table' AND name='{table}'
        """)
        if cursor.fetchone()[0] > 0:
            raise ValueError(f"{table} table already exists - migration already completed?")

    # Count rows by type
    cursor.execute("SELECT COUNT(*) FROM ResponseAssessment")
    total_rows = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE imaging_study_id IS NOT NULL
          AND (recist_response IS NOT NULL OR sum_target_lesions_mm IS NOT NULL)
    """)
    imaging_rows = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE molecular_test_id IS NOT NULL
          AND (ctdna_vaf_percent IS NOT NULL OR ctdna_mutation_cleared IS NOT NULL)
    """)
    molecular_rows = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE progression_detected = 1
           OR resistance_mutation_detected = 1
           OR histologic_transformation = 1
    """)
    clinical_rows = cursor.fetchone()[0]

    stats = {
        'total': total_rows,
        'imaging': imaging_rows,
        'molecular': molecular_rows,
        'clinical': clinical_rows
    }

    print(f"  [OK] Total ResponseAssessment rows: {total_rows}")
    print(f"  [OK] Rows with imaging data: {imaging_rows}")
    print(f"  [OK] Rows with molecular data: {molecular_rows}")
    print(f"  [OK] Rows with clinical events: {clinical_rows}")

    # Check for orphaned foreign keys
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment ra
        WHERE ra.imaging_study_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1 FROM ImagingStudy i
              WHERE i.imaging_study_id = ra.imaging_study_id
          )
    """)
    orphaned_imaging = cursor.fetchone()[0]
    if orphaned_imaging > 0:
        raise ValueError(f"Found {orphaned_imaging} orphaned imaging_study_id references")

    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment ra
        WHERE ra.molecular_test_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1 FROM MolecularTest mt
              WHERE mt.molecular_test_id = ra.molecular_test_id
          )
    """)
    orphaned_molecular = cursor.fetchone()[0]
    if orphaned_molecular > 0:
        raise ValueError(f"Found {orphaned_molecular} orphaned molecular_test_id references")

    print("  [OK] No orphaned foreign keys found")

    return stats


def create_new_tables(conn: sqlite3.Connection):
    """Create the three new response tables"""
    cursor = conn.cursor()

    print("\n[STEP] Creating new tables...")

    # Table 1: ImagingResponse
    cursor.execute("""
        CREATE TABLE ImagingResponse (
            imaging_response_id TEXT NOT NULL PRIMARY KEY,
            imaging_study_id TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            treatment_id TEXT,
            assessment_date DATE NOT NULL,
            assessment_type VARCHAR(11),
            recist_response VARCHAR(2),
            sum_target_lesions_mm FLOAT,
            percent_change_from_baseline FLOAT,
            new_lesions_present BOOLEAN,

            FOREIGN KEY (imaging_study_id) REFERENCES ImagingStudy(imaging_study_id),
            FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
            FOREIGN KEY (treatment_id) REFERENCES Treatment(treatment_id)
        )
    """)
    print("  [OK] Created ImagingResponse table")

    # Table 2: MolecularResponse
    cursor.execute("""
        CREATE TABLE MolecularResponse (
            molecular_response_id TEXT NOT NULL PRIMARY KEY,
            molecular_test_id TEXT NOT NULL,
            patient_id TEXT NOT NULL,
            treatment_id TEXT,
            assessment_date DATE NOT NULL,
            assessment_type VARCHAR(11),
            ctdna_vaf_percent FLOAT,
            ctdna_tumor_fraction_percent FLOAT,
            ctdna_mutation_cleared BOOLEAN,

            FOREIGN KEY (molecular_test_id) REFERENCES MolecularTest(molecular_test_id),
            FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
            FOREIGN KEY (treatment_id) REFERENCES Treatment(treatment_id)
        )
    """)
    print("  [OK] Created MolecularResponse table")

    # Table 3: ClinicalResponse
    cursor.execute("""
        CREATE TABLE ClinicalResponse (
            clinical_response_id TEXT NOT NULL PRIMARY KEY,
            patient_id TEXT NOT NULL,
            treatment_id TEXT,
            event_date DATE NOT NULL,
            event_type VARCHAR(15),
            progression_detected BOOLEAN NOT NULL,
            progression_type VARCHAR(19),
            time_to_progression_months FLOAT,
            resistance_mutation_detected BOOLEAN,
            resistance_mechanism TEXT,
            histologic_transformation BOOLEAN,

            FOREIGN KEY (patient_id) REFERENCES Patient(patient_id),
            FOREIGN KEY (treatment_id) REFERENCES Treatment(treatment_id),
            CHECK (event_type IN ('Progression', 'Resistance', 'Transformation'))
        )
    """)
    print("  [OK] Created ClinicalResponse table")

    # Create indexes
    print("\n[STEP] Creating indexes...")

    indexes = [
        "CREATE INDEX idx_imaging_response_patient ON ImagingResponse(patient_id)",
        "CREATE INDEX idx_imaging_response_treatment ON ImagingResponse(treatment_id)",
        "CREATE INDEX idx_imaging_response_date ON ImagingResponse(assessment_date)",
        "CREATE INDEX idx_molecular_response_patient ON MolecularResponse(patient_id)",
        "CREATE INDEX idx_molecular_response_treatment ON MolecularResponse(treatment_id)",
        "CREATE INDEX idx_molecular_response_date ON MolecularResponse(assessment_date)",
        "CREATE INDEX idx_clinical_response_patient ON ClinicalResponse(patient_id)",
        "CREATE INDEX idx_clinical_response_treatment ON ClinicalResponse(treatment_id)",
        "CREATE INDEX idx_clinical_response_date ON ClinicalResponse(event_date)",
    ]

    for idx_sql in indexes:
        cursor.execute(idx_sql)

    print(f"  [OK] Created {len(indexes)} indexes")


def migrate_imaging_responses(conn: sqlite3.Connection) -> int:
    """Migrate imaging-related assessments"""
    cursor = conn.cursor()

    print("\n[STEP] Migrating imaging responses...")

    # Fetch all imaging assessments
    cursor.execute("""
        SELECT
            assessment_id,
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
        ORDER BY patient_id, assessment_date
    """)

    rows = cursor.fetchall()

    # Generate new IDs using Python-based counter (avoids window function)
    patient_counters = {}
    imaging_data = []

    for row in rows:
        (assessment_id, imaging_study_id, patient_id, treatment_id,
         assessment_date, assessment_type, recist_response,
         sum_target_lesions_mm, percent_change_from_baseline,
         new_lesions_present) = row

        # Extract patient number from patient_id (e.g., NGDX-001 -> 001)
        patient_num = patient_id.split('-')[-1]

        # Increment counter for this patient
        if patient_id not in patient_counters:
            patient_counters[patient_id] = 1
        else:
            patient_counters[patient_id] += 1

        # Generate new ID: IR-{patient_num}-{counter:03d}
        new_id = f"IR-{patient_num}-{patient_counters[patient_id]:03d}"

        imaging_data.append((
            new_id,
            imaging_study_id,
            patient_id,
            treatment_id,
            assessment_date,
            assessment_type,
            recist_response,
            sum_target_lesions_mm,
            percent_change_from_baseline,
            new_lesions_present
        ))

    # Bulk insert
    cursor.executemany("""
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
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, imaging_data)

    print(f"  [OK] Migrated {len(imaging_data)} imaging response records")
    return len(imaging_data)


def migrate_molecular_responses(conn: sqlite3.Connection) -> int:
    """Migrate molecular/ctDNA assessments"""
    cursor = conn.cursor()

    print("\n[STEP] Migrating molecular responses...")

    # Fetch all molecular assessments
    cursor.execute("""
        SELECT
            assessment_id,
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
        ORDER BY patient_id, assessment_date
    """)

    rows = cursor.fetchall()

    # Generate new IDs
    patient_counters = {}
    molecular_data = []

    for row in rows:
        (assessment_id, molecular_test_id, patient_id, treatment_id,
         assessment_date, assessment_type, ctdna_vaf_percent,
         ctdna_tumor_fraction_percent, ctdna_mutation_cleared) = row

        patient_num = patient_id.split('-')[-1]

        if patient_id not in patient_counters:
            patient_counters[patient_id] = 1
        else:
            patient_counters[patient_id] += 1

        # Generate new ID: MR-{patient_num}-{counter:03d}
        new_id = f"MR-{patient_num}-{patient_counters[patient_id]:03d}"

        molecular_data.append((
            new_id,
            molecular_test_id,
            patient_id,
            treatment_id,
            assessment_date,
            assessment_type,
            ctdna_vaf_percent,
            ctdna_tumor_fraction_percent,
            ctdna_mutation_cleared
        ))

    # Bulk insert
    cursor.executemany("""
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
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, molecular_data)

    print(f"  [OK] Migrated {len(molecular_data)} molecular response records")
    return len(molecular_data)


def migrate_clinical_responses(conn: sqlite3.Connection) -> int:
    """Migrate clinical outcome events (progression, resistance, transformation)"""
    cursor = conn.cursor()

    print("\n[STEP] Migrating clinical responses...")

    # Fetch all clinical events
    cursor.execute("""
        SELECT
            assessment_id,
            patient_id,
            treatment_id,
            assessment_date,
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
        ORDER BY patient_id, assessment_date
    """)

    rows = cursor.fetchall()

    # Generate new IDs
    patient_counters = {}
    clinical_data = []

    for row in rows:
        (assessment_id, patient_id, treatment_id, assessment_date,
         progression_detected, progression_type, time_to_progression_months,
         resistance_mutation_detected, resistance_mechanism,
         histologic_transformation) = row

        patient_num = patient_id.split('-')[-1]

        if patient_id not in patient_counters:
            patient_counters[patient_id] = 1
        else:
            patient_counters[patient_id] += 1

        # Generate new ID: CR-{patient_num}-{counter:03d}
        new_id = f"CR-{patient_num}-{patient_counters[patient_id]:03d}"

        # Determine event type
        if histologic_transformation == 1:
            event_type = 'Transformation'
        elif resistance_mutation_detected == 1:
            event_type = 'Resistance'
        else:
            event_type = 'Progression'

        clinical_data.append((
            new_id,
            patient_id,
            treatment_id,
            assessment_date,  # event_date
            event_type,
            progression_detected if progression_detected is not None else 0,
            progression_type,
            time_to_progression_months,
            resistance_mutation_detected,
            resistance_mechanism,
            histologic_transformation
        ))

    # Bulk insert
    cursor.executemany("""
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
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, clinical_data)

    print(f"  [OK] Migrated {len(clinical_data)} clinical response records")
    return len(clinical_data)


def validate_migration(conn: sqlite3.Connection, pre_stats: Dict[str, int]) -> bool:
    """Validate migration results"""
    cursor = conn.cursor()

    print("\n[STEP] Validating migration...")

    # Count rows in new tables
    cursor.execute("SELECT COUNT(*) FROM ImagingResponse")
    imaging_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM MolecularResponse")
    molecular_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ClinicalResponse")
    clinical_count = cursor.fetchone()[0]

    print(f"  ImagingResponse: {imaging_count} rows (expected: {pre_stats['imaging']})")
    print(f"  MolecularResponse: {molecular_count} rows (expected: {pre_stats['molecular']})")
    print(f"  ClinicalResponse: {clinical_count} rows (expected: {pre_stats['clinical']})")

    # Check if counts match
    if imaging_count != pre_stats['imaging']:
        print(f"  [FAIL] ImagingResponse count mismatch!")
        return False

    if molecular_count != pre_stats['molecular']:
        print(f"  [FAIL] MolecularResponse count mismatch!")
        return False

    if clinical_count != pre_stats['clinical']:
        print(f"  [FAIL] ClinicalResponse count mismatch!")
        return False

    # Check foreign key integrity
    cursor.execute("PRAGMA foreign_key_check(ImagingResponse)")
    fk_violations = cursor.fetchall()
    if fk_violations:
        print(f"  [FAIL] ImagingResponse has {len(fk_violations)} FK violations!")
        return False

    cursor.execute("PRAGMA foreign_key_check(MolecularResponse)")
    fk_violations = cursor.fetchall()
    if fk_violations:
        print(f"  [FAIL] MolecularResponse has {len(fk_violations)} FK violations!")
        return False

    cursor.execute("PRAGMA foreign_key_check(ClinicalResponse)")
    fk_violations = cursor.fetchall()
    if fk_violations:
        print(f"  [FAIL] ClinicalResponse has {len(fk_violations)} FK violations!")
        return False

    print("  [OK] All foreign key constraints valid")
    print("  [OK] Row counts match expected values")

    return True


def archive_old_table(conn: sqlite3.Connection):
    """Archive ResponseAssessment to CSV before dropping"""
    import csv

    cursor = conn.cursor()

    print("\n[STEP] Archiving old ResponseAssessment table...")

    # Set row factory to get column names
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ResponseAssessment ORDER BY patient_id, assessment_date")
    rows = cursor.fetchall()

    if rows:
        # Create archive file
        archive_path = BACKUP_DIR / f"response_assessment_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        with open(archive_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows([dict(row) for row in rows])

        print(f"  [OK] Archived {len(rows)} rows to {archive_path}")
    else:
        print("  [OK] No rows to archive (table was empty)")

    # Reset row factory
    conn.row_factory = None


def drop_old_table(conn: sqlite3.Connection):
    """Drop the old ResponseAssessment table"""
    cursor = conn.cursor()

    print("\n[STEP] Dropping old ResponseAssessment table...")

    cursor.execute("DROP TABLE IF EXISTS ResponseAssessment")

    print("  [OK] ResponseAssessment table dropped")


def main():
    """Execute migration"""
    print("="*70)
    print("ResponseAssessment Table Migration")
    print("="*70)

    # Check if database exists
    if not DB_PATH.exists():
        print(f"[ERROR] Database not found at {DB_PATH}")
        sys.exit(1)

    # Create backup
    backup_path = DB_PATH.parent / f"{DB_PATH.stem}_pre_migration_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    print(f"\n[BACKUP] Creating database backup at {backup_path}")

    import shutil
    shutil.copy2(DB_PATH, backup_path)
    print(f"  [OK] Backup created")

    # Connect to database
    conn = sqlite3.connect(DB_PATH)

    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON")

    try:
        # Check SQLite version
        version = check_sqlite_version(conn)

        # Validate preconditions
        pre_stats = validate_preconditions(conn)

        # Ask for confirmation
        print("\n" + "="*70)
        print("READY TO MIGRATE")
        print("="*70)
        print(f"This will create 3 new tables and eventually drop ResponseAssessment.")
        print(f"Backup created at: {backup_path}")
        response = input("\nProceed with migration? (yes/no): ")

        if response.lower() != 'yes':
            print("\n[CANCELLED] Migration cancelled by user")
            conn.close()
            sys.exit(0)

        # Begin transaction
        conn.execute("BEGIN TRANSACTION")

        # Execute migration steps
        create_new_tables(conn)

        imaging_migrated = migrate_imaging_responses(conn)
        molecular_migrated = migrate_molecular_responses(conn)
        clinical_migrated = migrate_clinical_responses(conn)

        # Validate
        if not validate_migration(conn, pre_stats):
            print("\n[ERROR] Validation failed - rolling back")
            conn.rollback()
            conn.close()
            sys.exit(1)

        # Archive old table
        archive_old_table(conn)

        # Ask before dropping
        print("\n" + "="*70)
        print("VALIDATION PASSED - READY TO DROP OLD TABLE")
        print("="*70)
        response = input("\nDrop ResponseAssessment table? (yes/no): ")

        if response.lower() == 'yes':
            drop_old_table(conn)
        else:
            print("  [WARN] ResponseAssessment table kept (you can drop it manually later)")

        # Commit transaction
        conn.commit()

        print("\n" + "="*70)
        print("MIGRATION COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"  [OK] ImagingResponse: {imaging_migrated} rows")
        print(f"  [OK] MolecularResponse: {molecular_migrated} rows")
        print(f"  [OK] ClinicalResponse: {clinical_migrated} rows")
        print(f"  [OK] Backup: {backup_path}")
        print("\n")

    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        print("[ROLLBACK] Rolling back changes...")
        conn.rollback()
        print(f"[RESTORE] Database unchanged - backup available at {backup_path}")
        conn.close()
        sys.exit(1)

    finally:
        conn.close()


if __name__ == "__main__":
    main()