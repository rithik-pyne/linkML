"""
Active alerts endpoint - real-time clinical monitoring alerts
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from backend.app.database import execute_query, execute_query_one
from backend.app.utils.alerts import generate_all_alerts

router = APIRouter()


@router.get("/patients/{patient_id}/alerts")
async def get_patient_alerts(patient_id: str) -> Dict[str, Any]:
    """
    Get active clinical alerts for a patient

    Generates alerts for:
    - Rising ctDNA VAF (≥2x from nadir)
    - Resistance mutations (acquired at progression)
    - Overdue imaging (>84 days since last scan)

    Args:
        patient_id: Patient identifier (e.g., NGDX-001)

    Returns:
        Dictionary with active alerts and overdue tests

    Raises:
        HTTPException: 404 if patient not found
    """
    # Check patient exists
    patient_check = execute_query_one("SELECT patient_id FROM Patient WHERE patient_id = ?", (patient_id,))
    if not patient_check:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    # Get current stage
    current_stage_sql = """
    SELECT ajcc_stage
    FROM ImagingStudy
    WHERE patient_id = ?
    ORDER BY scan_date DESC
    LIMIT 1
    """
    stage_result = execute_query_one(current_stage_sql, (patient_id,))
    current_stage = stage_result.get('ajcc_stage') if stage_result else None

    # Get all mutations with test dates for VAF trending
    mutations_sql = """
    SELECT
        m.mutation_id,
        m.gene_symbol,
        m.mutation_type,
        m.mutation_hgvs,
        m.vaf_percent,
        m.tumor_fraction_percent,
        m.actionable_mutation,
        m.resistance_mutation,
        m.is_primary_driver,
        m.is_acquired_resistance,
        m.detection_timepoint,
        mt.test_date,
        mt.specimen_source,
        mt.molecular_test_id
    FROM Mutation m
    JOIN MolecularTest mt ON m.molecular_test_id = mt.molecular_test_id
    JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
    WHERE b.patient_id = ?
    ORDER BY mt.test_date
    """
    mutations = execute_query(mutations_sql, (patient_id,))

    # Get molecular tests
    molecular_tests_sql = """
    SELECT
        mt.molecular_test_id,
        mt.test_date,
        mt.specimen_source,
        mt.ngs_panel_name
    FROM MolecularTest mt
    JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
    WHERE b.patient_id = ?
    ORDER BY mt.test_date
    """
    molecular_tests = execute_query(molecular_tests_sql, (patient_id,))

    # Get imaging studies for overdue checks
    imaging_studies_sql = """
    SELECT
        imaging_study_id,
        scan_date,
        imaging_modality,
        ajcc_stage
    FROM ImagingStudy
    WHERE patient_id = ?
    ORDER BY scan_date
    """
    imaging_studies = execute_query(imaging_studies_sql, (patient_id,))

    # Generate all alerts using the alert engine
    alerts = generate_all_alerts(
        mutations=mutations,
        molecular_tests=molecular_tests,
        imaging_studies=imaging_studies,
        current_stage=current_stage
    )

    # Check for overdue tests (separate from imaging alerts)
    overdue_tests = []

    # Check if molecular testing is overdue (>6 months for stable disease, >3 months for progression)
    if molecular_tests:
        latest_molecular = molecular_tests[-1]
        # This would require date calculation - simplified for now
        # In production, calculate days since last molecular test

    return {
        "patient_id": patient_id,
        "alerts": alerts,
        "overdue_tests": overdue_tests,
        "total_active_alerts": len(alerts)
    }