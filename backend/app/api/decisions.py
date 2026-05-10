"""
Treatment decision support endpoint - clinical recommendations based on evidence
"""
from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from backend.app.database import execute_query, execute_query_one
from backend.app.utils.clinical_rules import get_recommendations, generate_alerts_from_mutations

router = APIRouter()


@router.get("/patients/{patient_id}/decisions")
async def get_treatment_decisions(patient_id: str) -> Dict[str, Any]:
    """
    Get clinical decision support with treatment recommendations and alerts

    Args:
        patient_id: Patient identifier (e.g., NGDX-001)

    Returns:
        Dictionary with recommendations and alerts based on clinical guidelines

    Raises:
        HTTPException: 404 if patient not found
    """
    # Check patient exists and get basic data
    patient_sql = """
    SELECT
        patient_id,
        age_at_diagnosis,
        sex,
        diagnosis_date,
        ecog_baseline
    FROM Patient
    WHERE patient_id = ?
    """
    patient_data = execute_query_one(patient_sql, (patient_id,))

    if not patient_data:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    # Get current stage from latest imaging
    current_stage_sql = """
    SELECT ajcc_stage
    FROM ImagingStudy
    WHERE patient_id = ?
    ORDER BY scan_date DESC
    LIMIT 1
    """
    stage_result = execute_query_one(current_stage_sql, (patient_id,))
    current_stage = stage_result.get('ajcc_stage') if stage_result else None

    # Get current treatment line
    treatment_line_sql = """
    SELECT MAX(treatment_line) as current_line
    FROM Treatment
    WHERE patient_id = ?
    """
    line_result = execute_query_one(treatment_line_sql, (patient_id,))
    current_treatment_line = line_result.get('current_line') if line_result else 0

    # Get all mutations
    mutations_sql = """
    SELECT
        m.mutation_id,
        m.gene_symbol,
        m.mutation_type,
        m.mutation_hgvs,
        m.vaf_percent,
        m.actionable_mutation,
        m.resistance_mutation,
        m.is_primary_driver,
        m.is_acquired_resistance,
        m.detection_timepoint,
        mt.test_date,
        mt.specimen_source
    FROM Mutation m
    JOIN MolecularTest mt ON m.molecular_test_id = mt.molecular_test_id
    JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
    WHERE b.patient_id = ?
    ORDER BY mt.test_date
    """
    mutations = execute_query(mutations_sql, (patient_id,))

    # Get treatment history
    treatments_sql = """
    SELECT
        treatment_id,
        treatment_line,
        drug_name,
        treatment_intent,
        treatment_start_date,
        treatment_end_date,
        discontinuation_reason
    FROM Treatment
    WHERE patient_id = ?
    ORDER BY treatment_line
    """
    treatments = execute_query(treatments_sql, (patient_id,))

    # Get PD-L1 status
    pdl1_sql = """
    SELECT pdl1_tps_percent as tps_percent
    FROM Biopsy
    WHERE patient_id = ?
      AND specimen_type = 'Tissue'
      AND pdl1_tps_percent IS NOT NULL
    ORDER BY biopsy_date
    LIMIT 1
    """
    pdl1_result = execute_query_one(pdl1_sql, (patient_id,))
    pdl1_tps = pdl1_result.get('tps_percent') if pdl1_result else None

    # Get progression status from ClinicalResponse
    progression_sql = """
    SELECT
        progression_detected,
        progression_type,
        resistance_mutation_detected,
        resistance_mechanism,
        event_date
    FROM ClinicalResponse
    WHERE patient_id = ?
      AND progression_detected = 1
    ORDER BY event_date DESC
    LIMIT 1
    """
    progression = execute_query_one(progression_sql, (patient_id,))

    # Generate recommendations using clinical rules engine
    recommendations = get_recommendations(
        patient_data=patient_data,
        mutations=mutations,
        treatments=treatments,
        current_stage=current_stage
    )

    # Generate alerts from mutations
    mutation_alerts = generate_alerts_from_mutations(mutations, treatments)

    # Additional progression alerts
    additional_alerts = []
    if progression and progression.get('progression_detected'):
        additional_alerts.append({
            "alert_id": "ALR-PROG-001",
            "alert_type": "progression_detected",
            "severity": "High",
            "message": f"Radiographic progression detected - {progression.get('progression_type', 'Clinical progression')}",
            "trigger_date": progression.get('event_date'),
            "requires_action": True,
            "action_recommendation": "MDT discussion for next-line therapy. Consider molecular testing for resistance mechanisms.",
            "supporting_data": {
                "progression_type": progression.get('progression_type'),
                "resistance_mechanism": progression.get('resistance_mechanism')
            }
        })

    all_alerts = mutation_alerts + additional_alerts

    # Extract mutations detected for supporting data
    mutations_detected = [
        f"{m['gene_symbol']} {m['mutation_type']}"
        for m in mutations
        if m.get('actionable_mutation') or m.get('resistance_mutation')
    ]

    return {
        "patient_id": patient_id,
        "current_treatment_line": current_treatment_line,
        "current_stage": current_stage,
        "recommendations": recommendations,
        "alerts": all_alerts,
        "supporting_data": {
            "mutations_detected": mutations_detected,
            "pdl1_tps": pdl1_tps,
            "progression_detected": bool(progression) if progression else False
        }
    }