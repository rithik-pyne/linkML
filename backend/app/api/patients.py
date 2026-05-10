"""
Patient endpoints - list, summary, and basic patient data
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.app.database import execute_query, execute_query_one

router = APIRouter()


@router.get("/patients")
async def get_patients() -> Dict[str, Any]:
    """
    Get list of all patients with current status

    Returns:
        Dictionary with patients array and total count
    """
    sql = """
    SELECT
        p.patient_id,
        p.age_at_diagnosis,
        p.sex,
        p.diagnosis_date,
        -- Get current stage from latest imaging study
        (SELECT i.ajcc_stage
         FROM ImagingStudy i
         WHERE i.patient_id = p.patient_id
         ORDER BY i.scan_date DESC
         LIMIT 1) as current_stage,
        -- Get current treatment from latest treatment
        (SELECT t.drug_name
         FROM Treatment t
         WHERE t.patient_id = p.patient_id
         ORDER BY t.treatment_line DESC
         LIMIT 1) as current_treatment,
        -- Get treatment line
        (SELECT MAX(t.treatment_line)
         FROM Treatment t
         WHERE t.patient_id = p.patient_id) as treatment_line
    FROM Patient p
    ORDER BY p.patient_id
    """

    patients = execute_query(sql)

    return {
        "patients": patients,
        "total": len(patients)
    }


@router.get("/patients/{patient_id}/summary")
async def get_patient_summary(patient_id: str) -> Dict[str, Any]:
    """
    Get patient summary with demographics, baseline data, and current status

    Args:
        patient_id: Patient identifier (e.g., NGDX-001)

    Returns:
        Patient summary dictionary

    Raises:
        HTTPException: 404 if patient not found
    """
    # Get patient demographics and baseline data
    patient_sql = """
    SELECT
        patient_id,
        nhs_number,
        age_at_diagnosis,
        sex,
        ethnicity_code,
        diagnosis_date,
        diagnosis_pathway,
        smoking_status,
        pack_years,
        family_history_lung_cancer,
        ecog_baseline,
        baseline_egfr,
        baseline_wbc,
        baseline_hemoglobin,
        baseline_platelets,
        baseline_alt,
        baseline_ast
    FROM Patient
    WHERE patient_id = ?
    """

    patient = execute_query_one(patient_sql, (patient_id,))

    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    # Get latest ECOG from clinical assessments
    latest_ecog_sql = """
    SELECT ecog_status, assessment_date
    FROM ClinicalAssessment
    WHERE patient_id = ?
    ORDER BY assessment_date DESC
    LIMIT 1
    """
    latest_ecog = execute_query_one(latest_ecog_sql, (patient_id,))

    # Get current stage from latest imaging
    current_stage_sql = """
    SELECT ajcc_stage
    FROM ImagingStudy
    WHERE patient_id = ?
    ORDER BY scan_date DESC
    LIMIT 1
    """
    current_stage = execute_query_one(current_stage_sql, (patient_id,))

    # Get current treatment
    current_treatment_sql = """
    SELECT
        treatment_id,
        drug_name,
        treatment_line,
        treatment_start_date,
        treatment_intent,
        drug_dose_mg,
        drug_frequency
    FROM Treatment
    WHERE patient_id = ?
    ORDER BY treatment_line DESC
    LIMIT 1
    """
    current_treatment = execute_query_one(current_treatment_sql, (patient_id,))

    # Build response
    summary = {
        **patient,
        "latest_ecog": latest_ecog.get('ecog_status') if latest_ecog else None,
        "latest_ecog_date": latest_ecog.get('assessment_date') if latest_ecog else None,
        "current_stage": current_stage.get('ajcc_stage') if current_stage else None,
        "current_treatment": current_treatment if current_treatment else None
    }

    return summary


@router.get("/patients/{patient_id}/molecular")
async def get_molecular_profile(patient_id: str) -> Dict[str, Any]:
    """
    Get molecular profile with mutations, PD-L1, and actionable variants

    Args:
        patient_id: Patient identifier (e.g., NGDX-001)

    Returns:
        Molecular profile dictionary with primary driver, co-mutations, resistance mutations

    Raises:
        HTTPException: 404 if patient not found
    """
    # Check patient exists
    patient_check = execute_query_one("SELECT patient_id FROM Patient WHERE patient_id = ?", (patient_id,))
    if not patient_check:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    # Get all mutations with molecular test details
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
        mt.ngs_panel_name,
        mt.ngs_panel_version,
        mt.mean_coverage_depth
    FROM Mutation m
    JOIN MolecularTest mt ON m.molecular_test_id = mt.molecular_test_id
    JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
    WHERE b.patient_id = ?
    ORDER BY mt.test_date, m.gene_symbol
    """
    all_mutations = execute_query(mutations_sql, (patient_id,))

    # Separate mutations by type
    primary_driver = None
    co_mutations = []
    resistance_mutations = []

    for mut in all_mutations:
        if mut.get('is_primary_driver'):
            primary_driver = mut
        elif mut.get('resistance_mutation') or mut.get('is_acquired_resistance'):
            resistance_mutations.append(mut)
        else:
            co_mutations.append(mut)

    # Get PD-L1 status from biopsy (take the first tissue biopsy with PD-L1 data)
    pdl1_sql = """
    SELECT
        pdl1_tps_percent as tps_percent,
        pdl1_antibody_clone as antibody_clone,
        biopsy_date as test_date
    FROM Biopsy
    WHERE patient_id = ?
      AND specimen_type = 'Tissue'
      AND pdl1_tps_percent IS NOT NULL
    ORDER BY biopsy_date
    LIMIT 1
    """
    pdl1_status = execute_query_one(pdl1_sql, (patient_id,))

    # Count actionable mutations
    actionable_count = sum(1 for m in all_mutations if m.get('actionable_mutation'))

    # Get latest NGS test
    latest_ngs_sql = """
    SELECT
        mt.molecular_test_id,
        mt.test_date,
        mt.specimen_source,
        mt.ngs_panel_name,
        mt.ngs_panel_version,
        mt.mean_coverage_depth
    FROM MolecularTest mt
    JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
    WHERE b.patient_id = ?
    ORDER BY mt.test_date DESC
    LIMIT 1
    """
    latest_ngs_test = execute_query_one(latest_ngs_sql, (patient_id,))

    return {
        "patient_id": patient_id,
        "primary_driver_mutation": primary_driver,
        "co_mutations": co_mutations,
        "resistance_mutations": resistance_mutations,
        "pdl1_status": pdl1_status,
        "actionable_mutations_count": actionable_count,
        "latest_ngs_test": latest_ngs_test
    }


@router.get("/patients/{patient_id}/imaging")
async def get_imaging_history(patient_id: str) -> Dict[str, Any]:
    """
    Get all imaging studies for a patient

    Args:
        patient_id: Patient identifier (e.g., NGDX-001)

    Returns:
        Dictionary with imaging_studies array and total count

    Raises:
        HTTPException: 404 if patient not found
    """
    # Check patient exists
    patient_check = execute_query_one("SELECT patient_id FROM Patient WHERE patient_id = ?", (patient_id,))
    if not patient_check:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    imaging_sql = """
    SELECT
        imaging_study_id,
        patient_id,
        scan_date,
        imaging_modality,
        study_description,
        t_stage,
        n_stage,
        m_stage,
        ajcc_stage,
        primary_tumor_diameter_mm,
        suv_max,
        brain_metastasis_present,
        brain_lesion_count,
        brain_largest_lesion_mm,
        study_uid,
        accession_number,
        dicom_file_path,
        thumbnail_image_path
    FROM ImagingStudy
    WHERE patient_id = ?
    ORDER BY scan_date
    """
    imaging_studies = execute_query(imaging_sql, (patient_id,))

    return {
        "patient_id": patient_id,
        "imaging_studies": imaging_studies,
        "total_scans": len(imaging_studies)
    }


@router.get("/patients/{patient_id}/treatments")
async def get_treatment_history(patient_id: str) -> Dict[str, Any]:
    """
    Get all treatment lines for a patient

    Args:
        patient_id: Patient identifier (e.g., NGDX-001)

    Returns:
        Dictionary with treatments array and summary

    Raises:
        HTTPException: 404 if patient not found
    """
    # Check patient exists
    patient_check = execute_query_one("SELECT patient_id FROM Patient WHERE patient_id = ?", (patient_id,))
    if not patient_check:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    treatments_sql = """
    SELECT
        treatment_id,
        patient_id,
        treatment_line,
        treatment_intent,
        drug_name,
        drug_dose_mg,
        drug_frequency,
        drug_route,
        treatment_start_date,
        treatment_end_date,
        discontinuation_reason,
        mdt_recommendation,
        mdt_date,
        prior_ici_exposure,
        months_since_last_ici
    FROM Treatment
    WHERE patient_id = ?
    ORDER BY treatment_line
    """
    treatments = execute_query(treatments_sql, (patient_id,))

    # Get current line (max treatment_line)
    current_line = max([t['treatment_line'] for t in treatments]) if treatments else 0

    return {
        "patient_id": patient_id,
        "treatments": treatments,
        "current_line": current_line,
        "total_lines": len(treatments)
    }


@router.get("/patients/{patient_id}/response")
async def get_response_assessments(patient_id: str) -> Dict[str, Any]:
    """
    Get all response assessments for a patient (imaging, molecular, clinical)

    Args:
        patient_id: Patient identifier (e.g., NGDX-001)

    Returns:
        Dictionary with imaging_responses, molecular_responses, clinical_responses arrays

    Raises:
        HTTPException: 404 if patient not found
    """
    # Check patient exists
    patient_check = execute_query_one("SELECT patient_id FROM Patient WHERE patient_id = ?", (patient_id,))
    if not patient_check:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    # Get imaging responses
    imaging_response_sql = """
    SELECT
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
    FROM ImagingResponse
    WHERE patient_id = ?
    ORDER BY assessment_date
    """
    imaging_responses = execute_query(imaging_response_sql, (patient_id,))

    # Get molecular responses
    molecular_response_sql = """
    SELECT
        molecular_response_id,
        molecular_test_id,
        patient_id,
        treatment_id,
        assessment_date,
        assessment_type,
        ctdna_vaf_percent,
        ctdna_tumor_fraction_percent,
        ctdna_mutation_cleared
    FROM MolecularResponse
    WHERE patient_id = ?
    ORDER BY assessment_date
    """
    molecular_responses = execute_query(molecular_response_sql, (patient_id,))

    # Get clinical responses
    clinical_response_sql = """
    SELECT
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
    FROM ClinicalResponse
    WHERE patient_id = ?
    ORDER BY event_date
    """
    clinical_responses = execute_query(clinical_response_sql, (patient_id,))

    return {
        "patient_id": patient_id,
        "imaging_responses": imaging_responses,
        "molecular_responses": molecular_responses,
        "clinical_responses": clinical_responses,
        "total_imaging": len(imaging_responses),
        "total_molecular": len(molecular_responses),
        "total_clinical": len(clinical_responses)
    }


@router.get("/patients/{patient_id}/clinical")
async def get_clinical_assessments(patient_id: str) -> Dict[str, Any]:
    """
    Get all clinical assessments (ECOG, labs, symptoms) for a patient

    Args:
        patient_id: Patient identifier (e.g., NGDX-001)

    Returns:
        Dictionary with assessments array and latest values

    Raises:
        HTTPException: 404 if patient not found
    """
    # Check patient exists
    patient_check = execute_query_one("SELECT patient_id FROM Patient WHERE patient_id = ?", (patient_id,))
    if not patient_check:
        raise HTTPException(status_code=404, detail=f"Patient {patient_id} not found")

    clinical_sql = """
    SELECT
        clinical_assessment_id,
        patient_id,
        assessment_date,
        visit_type,
        ecog_status,
        symptoms_coded,
        symptom_severity_grade,
        wbc,
        hemoglobin,
        platelets,
        neutrophils,
        egfr_value,
        alt,
        ast
    FROM ClinicalAssessment
    WHERE patient_id = ?
    ORDER BY assessment_date
    """
    assessments = execute_query(clinical_sql, (patient_id,))

    # Get latest values
    latest_ecog = None
    latest_labs = None

    if assessments:
        latest = assessments[-1]  # Last item (most recent)
        latest_ecog = latest.get('ecog_status')
        latest_labs = {
            "date": latest.get('assessment_date'),
            "wbc": latest.get('wbc'),
            "hemoglobin": latest.get('hemoglobin'),
            "platelets": latest.get('platelets'),
            "egfr_value": latest.get('egfr_value'),
            "alt": latest.get('alt'),
            "ast": latest.get('ast')
        }

    return {
        "patient_id": patient_id,
        "assessments": assessments,
        "total": len(assessments),
        "latest_ecog": latest_ecog,
        "latest_labs": latest_labs
    }