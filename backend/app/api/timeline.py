"""
Timeline endpoint - aggregates events from all tables for chronological visualization
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.app.database import execute_query, execute_query_one

router = APIRouter()


@router.get("/patients/{patient_id}/timeline")
async def get_patient_timeline(patient_id: str) -> Dict[str, Any]:
    """
    Get integrated disease timeline with all events and time-series data

    Args:
        patient_id: Patient identifier (e.g., NGDX-001)

    Returns:
        Dictionary with timeline_events, vaf_series, recist_series, ecog_series

    Raises:
        HTTPException: 404 if patient not found
    """
    # Check patient exists
    patient_check = execute_query_one("SELECT patient_id, diagnosis_date FROM Patient WHERE patient_id = ?", (patient_id,))
    if not patient_check:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    diagnosis_date = patient_check['diagnosis_date']

    # Collect timeline events from all tables
    timeline_events = []

    # 1. Molecular test events
    molecular_events_sql = """
    SELECT
        mt.test_date as date,
        'molecular_test' as event_type,
        mt.ngs_panel_name as panel,
        mt.specimen_source,
        mt.molecular_test_id,
        COUNT(m.mutation_id) as mutations_detected
    FROM MolecularTest mt
    JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
    LEFT JOIN Mutation m ON m.molecular_test_id = mt.molecular_test_id
    WHERE b.patient_id = ?
    GROUP BY mt.molecular_test_id
    ORDER BY mt.test_date
    """
    molecular_events = execute_query(molecular_events_sql, (patient_id,))
    for event in molecular_events:
        description = f"{event['specimen_source']} NGS - {event['panel']}"
        if event['mutations_detected'] > 0:
            description += f" ({event['mutations_detected']} mutations detected)"

        timeline_events.append({
            "date": event['date'],
            "event_type": "molecular_test",
            "description": description,
            "data": {
                "molecular_test_id": event['molecular_test_id'],
                "panel": event['panel'],
                "mutations_detected": event['mutations_detected']
            }
        })

    # 2. Treatment start events
    treatment_events_sql = """
    SELECT
        treatment_id,
        treatment_start_date as date,
        treatment_line,
        drug_name,
        treatment_intent
    FROM Treatment
    WHERE patient_id = ?
    ORDER BY treatment_start_date
    """
    treatment_events = execute_query(treatment_events_sql, (patient_id,))
    for event in treatment_events:
        description = f"{event['drug_name']}"
        if event['treatment_intent']:
            description += f" ({event['treatment_intent']})"

        timeline_events.append({
            "date": event['date'],
            "event_type": "treatment_start",
            "description": description,
            "data": {
                "treatment_id": event['treatment_id'],
                "treatment_line": event['treatment_line'],
                "treatment_intent": event['treatment_intent']
            }
        })

    # 3. Response assessment events (especially progression)
    response_events_sql = """
    SELECT
        assessment_id,
        assessment_date as date,
        assessment_type,
        recist_response,
        sum_target_lesions_mm,
        progression_detected
    FROM ResponseAssessment
    WHERE patient_id = ?
      AND (progression_detected = 1 OR recist_response IN ('CR', 'PR', 'PD'))
    ORDER BY assessment_date
    """
    response_events = execute_query(response_events_sql, (patient_id,))
    for event in response_events:
        if event['progression_detected']:
            description = f"Progression - {event['recist_response'] or 'Clinical'}"
        else:
            description = f"{event['assessment_type']} - {event['recist_response']}"

        if event['sum_target_lesions_mm'] is not None:
            description += f" (tumor {event['sum_target_lesions_mm']:.1f}mm)"

        timeline_events.append({
            "date": event['date'],
            "event_type": "response_assessment",
            "description": description,
            "data": {
                "assessment_id": event['assessment_id'],
                "recist_response": event['recist_response'],
                "tumor_diameter_mm": event['sum_target_lesions_mm'],
                "progression_detected": bool(event['progression_detected'])
            }
        })

    # 4. Imaging events (major staging changes)
    imaging_events_sql = """
    SELECT
        imaging_study_id,
        scan_date as date,
        imaging_modality,
        ajcc_stage,
        primary_tumor_diameter_mm
    FROM ImagingStudy
    WHERE patient_id = ?
    ORDER BY scan_date
    """
    imaging_events = execute_query(imaging_events_sql, (patient_id,))
    # Only add significant imaging events (baseline and stage changes)
    prev_stage = None
    for i, event in enumerate(imaging_events):
        is_baseline = (i == 0)
        stage_changed = (event['ajcc_stage'] != prev_stage)

        if is_baseline or stage_changed:
            description = f"{event['imaging_modality']} - Stage {event['ajcc_stage']}"
            if event['primary_tumor_diameter_mm']:
                description += f" (tumor {event['primary_tumor_diameter_mm']:.1f}mm)"

            timeline_events.append({
                "date": event['date'],
                "event_type": "imaging_study",
                "description": description,
                "data": {
                    "imaging_study_id": event['imaging_study_id'],
                    "modality": event['imaging_modality'],
                    "ajcc_stage": event['ajcc_stage']
                }
            })

        prev_stage = event['ajcc_stage']

    # Sort all events chronologically
    timeline_events.sort(key=lambda x: x['date'] if x['date'] else '')

    # Create VAF time-series
    vaf_series_sql = """
    SELECT
        mt.test_date as date,
        m.gene_symbol,
        m.mutation_type,
        m.vaf_percent,
        mt.specimen_source
    FROM Mutation m
    JOIN MolecularTest mt ON m.molecular_test_id = mt.molecular_test_id
    JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
    WHERE b.patient_id = ?
      AND m.vaf_percent IS NOT NULL
    ORDER BY mt.test_date, m.gene_symbol
    """
    vaf_series = execute_query(vaf_series_sql, (patient_id,))

    # Create RECIST time-series
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
    recist_series = execute_query(recist_series_sql, (patient_id,))

    # Create ECOG time-series
    ecog_series_sql = """
    SELECT
        assessment_date as date,
        ecog_status
    FROM ClinicalAssessment
    WHERE patient_id = ?
      AND ecog_status IS NOT NULL
    ORDER BY assessment_date
    """
    ecog_series = execute_query(ecog_series_sql, (patient_id,))

    return {
        "patient_id": patient_id,
        "diagnosis_date": diagnosis_date,
        "timeline_events": timeline_events,
        "vaf_series": vaf_series,
        "recist_series": recist_series,
        "ecog_series": ecog_series
    }