#!/usr/bin/env python3
"""
Pre-migration validation script for ResponseAssessment refactor

Analyzes current ResponseAssessment data to understand:
1. Data distribution across imaging/molecular/clinical dimensions
2. Overlaps (rows with multiple data types)
3. Potential data quality issues
4. Foreign key integrity

Run this BEFORE migrating to understand what will be split.

Author: Migration validation
Date: 2026-04-30
"""

import sqlite3
from pathlib import Path
from typing import Dict, List, Tuple
import json

DB_PATH = Path(__file__).parent.parent / "backend" / "clinical_data.db"


def analyze_data_distribution(conn: sqlite3.Connection) -> Dict:
    """Analyze how ResponseAssessment data is distributed"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("DATA DISTRIBUTION ANALYSIS")
    print("="*70)

    # Total rows
    cursor.execute("SELECT COUNT(*) FROM ResponseAssessment")
    total_rows = cursor.fetchone()[0]
    print(f"\nTotal ResponseAssessment rows: {total_rows}")

    if total_rows == 0:
        print("⚠ No data to migrate!")
        return {}

    # Rows by type
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN imaging_study_id IS NOT NULL THEN 1 ELSE 0 END) as has_imaging_fk,
            SUM(CASE WHEN molecular_test_id IS NOT NULL THEN 1 ELSE 0 END) as has_molecular_fk,
            SUM(CASE WHEN recist_response IS NOT NULL OR sum_target_lesions_mm IS NOT NULL THEN 1 ELSE 0 END) as has_imaging_data,
            SUM(CASE WHEN ctdna_vaf_percent IS NOT NULL OR ctdna_mutation_cleared IS NOT NULL THEN 1 ELSE 0 END) as has_molecular_data,
            SUM(CASE WHEN progression_detected = 1 OR resistance_mutation_detected = 1 OR histologic_transformation = 1 THEN 1 ELSE 0 END) as has_clinical_event
        FROM ResponseAssessment
    """)

    row = cursor.fetchone()
    stats = {
        'total': row[0],
        'has_imaging_fk': row[1],
        'has_molecular_fk': row[2],
        'has_imaging_data': row[3],
        'has_molecular_data': row[4],
        'has_clinical_event': row[5]
    }

    print("\nBy Foreign Key Presence:")
    print(f"  - With imaging_study_id: {stats['has_imaging_fk']} ({stats['has_imaging_fk']/total_rows*100:.1f}%)")
    print(f"  - With molecular_test_id: {stats['has_molecular_fk']} ({stats['has_molecular_fk']/total_rows*100:.1f}%)")

    print("\nBy Data Content:")
    print(f"  - Has imaging data (RECIST): {stats['has_imaging_data']} ({stats['has_imaging_data']/total_rows*100:.1f}%)")
    print(f"  - Has molecular data (ctDNA): {stats['has_molecular_data']} ({stats['has_molecular_data']/total_rows*100:.1f}%)")
    print(f"  - Has clinical event: {stats['has_clinical_event']} ({stats['has_clinical_event']/total_rows*100:.1f}%)")

    # Rows that will be migrated
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE imaging_study_id IS NOT NULL
          AND (recist_response IS NOT NULL OR sum_target_lesions_mm IS NOT NULL)
    """)
    to_imaging = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE molecular_test_id IS NOT NULL
          AND (ctdna_vaf_percent IS NOT NULL OR ctdna_mutation_cleared IS NOT NULL)
    """)
    to_molecular = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE progression_detected = 1
           OR resistance_mutation_detected = 1
           OR histologic_transformation = 1
    """)
    to_clinical = cursor.fetchone()[0]

    print("\n" + "-"*70)
    print("MIGRATION TARGET (rows that meet criteria):")
    print("-"*70)
    print(f"  → ImagingResponse: {to_imaging} rows")
    print(f"  → MolecularResponse: {to_molecular} rows")
    print(f"  → ClinicalResponse: {to_clinical} rows")

    stats['to_imaging'] = to_imaging
    stats['to_molecular'] = to_molecular
    stats['to_clinical'] = to_clinical

    return stats


def analyze_overlaps(conn: sqlite3.Connection):
    """Analyze rows with multiple data types (polymorphic rows)"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("DATA OVERLAP ANALYSIS (Polymorphic Rows)")
    print("="*70)

    # Rows with both imaging and molecular data
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE imaging_study_id IS NOT NULL
          AND molecular_test_id IS NOT NULL
    """)
    both_imaging_molecular = cursor.fetchone()[0]

    # Rows with imaging + clinical event
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE imaging_study_id IS NOT NULL
          AND (progression_detected = 1 OR resistance_mutation_detected = 1)
    """)
    imaging_plus_clinical = cursor.fetchone()[0]

    # Rows with molecular + clinical event
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE molecular_test_id IS NOT NULL
          AND (progression_detected = 1 OR resistance_mutation_detected = 1)
    """)
    molecular_plus_clinical = cursor.fetchone()[0]

    # Rows with all three
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment
        WHERE imaging_study_id IS NOT NULL
          AND molecular_test_id IS NOT NULL
          AND progression_detected = 1
    """)
    all_three = cursor.fetchone()[0]

    print(f"\nRows with multiple data types:")
    print(f"  - Imaging + Molecular: {both_imaging_molecular}")
    print(f"  - Imaging + Clinical event: {imaging_plus_clinical}")
    print(f"  - Molecular + Clinical event: {molecular_plus_clinical}")
    print(f"  - All three types: {all_three}")

    if both_imaging_molecular > 0 or imaging_plus_clinical > 0 or molecular_plus_clinical > 0:
        print("\n⚠ NOTE: These rows will be DUPLICATED across multiple new tables.")
        print("  This is EXPECTED behavior - same assessment captured in multiple dimensions.")


def analyze_null_sparsity(conn: sqlite3.Connection):
    """Analyze NULL value sparsity (the polymorphism problem)"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("NULL SPARSITY ANALYSIS (Why Polymorphism is Bad)")
    print("="*70)

    cursor.execute("SELECT COUNT(*) FROM ResponseAssessment")
    total = cursor.fetchone()[0]

    if total == 0:
        return

    # Imaging columns
    imaging_cols = [
        'imaging_study_id', 'recist_response', 'sum_target_lesions_mm',
        'percent_change_from_baseline', 'new_lesions_present'
    ]

    # Molecular columns
    molecular_cols = [
        'molecular_test_id', 'ctdna_vaf_percent', 'ctdna_mutation_cleared',
        'ctdna_tumor_fraction_percent'
    ]

    # Clinical columns
    clinical_cols = [
        'progression_detected', 'progression_type', 'time_to_progression_months',
        'resistance_mutation_detected', 'resistance_mechanism', 'histologic_transformation'
    ]

    print("\nImaging columns NULL rates:")
    for col in imaging_cols:
        cursor.execute(f"SELECT COUNT(*) FROM ResponseAssessment WHERE {col} IS NULL")
        null_count = cursor.fetchone()[0]
        print(f"  - {col}: {null_count}/{total} NULL ({null_count/total*100:.1f}%)")

    print("\nMolecular columns NULL rates:")
    for col in molecular_cols:
        cursor.execute(f"SELECT COUNT(*) FROM ResponseAssessment WHERE {col} IS NULL")
        null_count = cursor.fetchone()[0]
        print(f"  - {col}: {null_count}/{total} NULL ({null_count/total*100:.1f}%)")

    print("\nClinical columns NULL rates:")
    for col in clinical_cols:
        cursor.execute(f"SELECT COUNT(*) FROM ResponseAssessment WHERE {col} IS NULL")
        null_count = cursor.fetchone()[0]
        print(f"  - {col}: {null_count}/{total} NULL ({null_count/total*100:.1f}%)")

    print("\n💡 After migration, each specialized table will have much lower NULL rates.")


def check_foreign_key_integrity(conn: sqlite3.Connection):
    """Check for orphaned foreign keys"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("FOREIGN KEY INTEGRITY CHECK")
    print("="*70)

    # Check imaging_study_id
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment ra
        WHERE ra.imaging_study_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1 FROM ImagingStudy i
              WHERE i.imaging_study_id = ra.imaging_study_id
          )
    """)
    orphaned_imaging = cursor.fetchone()[0]

    # Check molecular_test_id
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment ra
        WHERE ra.molecular_test_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1 FROM MolecularTest mt
              WHERE mt.molecular_test_id = ra.molecular_test_id
          )
    """)
    orphaned_molecular = cursor.fetchone()[0]

    # Check treatment_id
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment ra
        WHERE ra.treatment_id IS NOT NULL
          AND NOT EXISTS (
              SELECT 1 FROM Treatment t
              WHERE t.treatment_id = ra.treatment_id
          )
    """)
    orphaned_treatment = cursor.fetchone()[0]

    # Check patient_id
    cursor.execute("""
        SELECT COUNT(*) FROM ResponseAssessment ra
        WHERE NOT EXISTS (
            SELECT 1 FROM Patient p
            WHERE p.patient_id = ra.patient_id
        )
    """)
    orphaned_patient = cursor.fetchone()[0]

    print(f"\nOrphaned foreign keys (MUST be 0 to proceed):")
    print(f"  - imaging_study_id: {orphaned_imaging}")
    print(f"  - molecular_test_id: {orphaned_molecular}")
    print(f"  - treatment_id: {orphaned_treatment}")
    print(f"  - patient_id: {orphaned_patient}")

    all_valid = (orphaned_imaging == 0 and orphaned_molecular == 0 and
                 orphaned_treatment == 0 and orphaned_patient == 0)

    if all_valid:
        print("\n✓ All foreign keys valid - safe to migrate")
    else:
        print("\n✗ FOREIGN KEY VIOLATIONS DETECTED!")
        print("  You must fix these before running migration.")

    return all_valid


def sample_polymorphic_rows(conn: sqlite3.Connection):
    """Show sample rows that will be split across tables"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("SAMPLE POLYMORPHIC ROWS (Before Split)")
    print("="*70)

    # Find a row with both imaging and molecular data
    cursor.execute("""
        SELECT
            assessment_id,
            patient_id,
            assessment_date,
            imaging_study_id,
            recist_response,
            molecular_test_id,
            ctdna_vaf_percent,
            progression_detected
        FROM ResponseAssessment
        WHERE imaging_study_id IS NOT NULL
          AND molecular_test_id IS NOT NULL
        LIMIT 1
    """)

    row = cursor.fetchone()
    if row:
        print("\nExample: Row with BOTH imaging + molecular data")
        print("-" * 70)
        print(f"  assessment_id: {row[0]}")
        print(f"  patient_id: {row[1]}")
        print(f"  assessment_date: {row[2]}")
        print(f"  imaging_study_id: {row[3]}")
        print(f"  recist_response: {row[4]}")
        print(f"  molecular_test_id: {row[5]}")
        print(f"  ctdna_vaf_percent: {row[6]}")
        print(f"  progression_detected: {row[7]}")
        print("\nAfter migration, this will become:")
        print(f"  → 1 row in ImagingResponse (imaging_study_id + recist_response)")
        print(f"  → 1 row in MolecularResponse (molecular_test_id + ctdna_vaf_percent)")
        if row[7]:
            print(f"  → 1 row in ClinicalResponse (progression event)")


def check_patient_distribution(conn: sqlite3.Connection):
    """Check how assessments are distributed across patients"""
    cursor = conn.cursor()

    print("\n" + "="*70)
    print("PATIENT DISTRIBUTION")
    print("="*70)

    # Count patients with assessments
    cursor.execute("SELECT COUNT(DISTINCT patient_id) FROM ResponseAssessment")
    total_patients = cursor.fetchone()[0]

    # Assessments per patient
    cursor.execute("""
        SELECT
            patient_id,
            COUNT(*) as assessment_count,
            SUM(CASE WHEN imaging_study_id IS NOT NULL THEN 1 ELSE 0 END) as imaging_count,
            SUM(CASE WHEN molecular_test_id IS NOT NULL THEN 1 ELSE 0 END) as molecular_count
        FROM ResponseAssessment
        GROUP BY patient_id
        ORDER BY assessment_count DESC
        LIMIT 10
    """)

    rows = cursor.fetchall()

    print(f"\nTotal patients with assessments: {total_patients}")
    print(f"\nTop 10 patients by assessment count:")
    print("-" * 70)
    print(f"{'Patient ID':<15} {'Total':<10} {'Imaging':<10} {'Molecular':<10}")
    print("-" * 70)

    for row in rows:
        print(f"{row[0]:<15} {row[1]:<10} {row[2]:<10} {row[3]:<10}")


def generate_summary_report(stats: Dict) -> str:
    """Generate JSON summary report"""
    report = {
        "migration_type": "ResponseAssessment → 3 specialized tables",
        "source_table": "ResponseAssessment",
        "target_tables": ["ImagingResponse", "MolecularResponse", "ClinicalResponse"],
        "stats": stats,
        "recommendations": []
    }

    # Add recommendations
    if stats.get('to_imaging', 0) == 0:
        report['recommendations'].append("⚠ No imaging responses to migrate - table will be empty")

    if stats.get('to_molecular', 0) == 0:
        report['recommendations'].append("⚠ No molecular responses to migrate - table will be empty")

    if stats.get('to_clinical', 0) == 0:
        report['recommendations'].append("⚠ No clinical events to migrate - table will be empty")

    total = stats.get('total', 0)
    migrated = stats.get('to_imaging', 0) + stats.get('to_molecular', 0) + stats.get('to_clinical', 0)

    if total > 0 and migrated < total:
        unmigrated = total - migrated
        report['recommendations'].append(
            f"ℹ {unmigrated} rows will not be migrated (no qualifying data)"
        )

    return json.dumps(report, indent=2)


def main():
    """Run pre-migration validation"""
    print("="*70)
    print("PRE-MIGRATION VALIDATION")
    print("ResponseAssessment Table Refactor")
    print("="*70)

    if not DB_PATH.exists():
        print(f"\n✗ Database not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)

    try:
        # Run all analyses
        stats = analyze_data_distribution(conn)

        if stats.get('total', 0) > 0:
            analyze_overlaps(conn)
            analyze_null_sparsity(conn)
            fk_valid = check_foreign_key_integrity(conn)
            sample_polymorphic_rows(conn)
            check_patient_distribution(conn)

            # Generate summary
            print("\n" + "="*70)
            print("SUMMARY REPORT")
            print("="*70)

            report = generate_summary_report(stats)
            print(report)

            # Save report
            report_path = Path(__file__).parent.parent / "example_files" / "archive" / "pre_migration_report.json"
            report_path.parent.mkdir(parents=True, exist_ok=True)

            with open(report_path, 'w') as f:
                f.write(report)

            print(f"\n📄 Full report saved to: {report_path}")

            # Final recommendation
            print("\n" + "="*70)
            print("RECOMMENDATION")
            print("="*70)

            if fk_valid and stats.get('total', 0) > 0:
                print("\n✓ Database is READY for migration")
                print("\nNext steps:")
                print("  1. Review this report carefully")
                print("  2. Run: python scripts/migrate_response_tables.py")
                print("  3. The migration script will create a backup automatically")
            else:
                print("\n✗ Database is NOT ready for migration")
                print("\nFix the issues above before proceeding.")

        else:
            print("\n⚠ No data in ResponseAssessment table")

    except sqlite3.OperationalError as e:
        print(f"\n✗ Database error: {e}")
        print("\nIs the ResponseAssessment table present?")

    finally:
        conn.close()


if __name__ == "__main__":
    main()