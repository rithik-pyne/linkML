#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database population script for clinical_model.yaml
Uses generated SQL schema file and loads 5 patients with baseline + time-series data
"""

import sqlite3
import csv
from pathlib import Path
from datetime import datetime, timedelta
import sys

# Paths
base_dir = Path(__file__).parent.parent
db_path = base_dir / "backend" / "clinical_data.db"
schema_sql_path = base_dir / "schemas" / "generated" / "sql" / "clinical_model.sql"
csv_path = base_dir / "example_files" / "simulated_data.csv"
mock_dir = base_dir / "example_files" / "mock_simulated"

# Patient IDs to load
PATIENT_IDS = ['NGDX-001', 'NGDX-002', 'NGDX-003', 'NGDX-004', 'NGDX-005']

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def excel_serial_to_date(serial):
    """Convert Excel date serial to YYYY-MM-DD"""
    if not serial or serial == '':
        return None
    try:
        base_date = datetime(1899, 12, 30)
        date = base_date + timedelta(days=int(serial))
        return date.strftime("%Y-%m-%d")
    except:
        return None

def parse_pipe_delimited(value):
    """Parse 'Key: Value | Key: Value' format"""
    if not value or value == '':
        return {}
    result = {}
    parts = value.split('|')
    for part in parts:
        part = part.strip()
        if ':' in part:
            key, val = part.split(':', 1)
            result[key.strip()] = val.strip()
    return result

def safe_float(value, default=None):
    """Safely convert to float"""
    if value == '' or value is None:
        return default
    try:
        return float(value)
    except:
        return default

def safe_int(value, default=None):
    """Safely convert to integer"""
    if value == '' or value is None:
        return default
    try:
        return int(value)
    except:
        return default

def extract_code_before_equals(value):
    """Extract code before '=' sign"""
    if not value or '=' not in value:
        return value
    return value.split('=')[0].strip()

def parse_boolean_field(value, key):
    """Parse boolean from 'key: True' format"""
    if not value:
        return False
    parsed = parse_pipe_delimited(value)
    val = parsed.get(key, 'False')
    return val.lower() in ['true', '1', 'yes']

# ============================================================================
# STEP 1: DROP AND CREATE DATABASE FROM SCHEMA
# ============================================================================

print("=" * 80)
print("DATABASE POPULATION SCRIPT")
print("=" * 80)

# Create backend directory if needed
db_path.parent.mkdir(exist_ok=True, parents=True)

# Drop existing database
if db_path.exists():
    db_path.unlink()
    print(f"[OK] Dropped existing database: {db_path}")

# Create new database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
print(f"[OK] Created new database: {db_path}")

# Read and execute schema SQL
print(f"\nLoading schema from: {schema_sql_path}")
with open(schema_sql_path, 'r', encoding='utf-8') as f:
    schema_sql = f.read()
    cursor.executescript(schema_sql)

conn.commit()
print("[OK] Schema created from clinical_model.sql")

# ============================================================================
# STEP 2: LOAD BASELINE DATA FROM simulated_data.csv
# ============================================================================

print("\n" + "=" * 80)
print("LOADING BASELINE DATA FROM simulated_data.csv")
print("=" * 80)

# Read CSV
with open(csv_path, 'r', encoding='latin-1') as f:
    reader = csv.reader(f)
    first_header = next(reader)
    var_headers = next(reader)
    headers = [first_header[0]] + var_headers[1:]

    patients_data = []
    for row in reader:
        if row and row[0] and row[0] in PATIENT_IDS:
            patient_dict = dict(zip(headers, row))
            patients_data.append(patient_dict)

print(f"[OK] Read {len(patients_data)} patients from CSV")

# Process each patient
for patient in patients_data:
    pid = patient.get('Patient_ID', '')
    print(f"\nProcessing {pid}...")

    # ========================================================================
    # PATIENT
    # ========================================================================
    diagnosis_date = excel_serial_to_date(patient.get('Var_017_Date_of_first_clinical_presentation___diagnosis_date', ''))

    ethnicity_raw = patient.get('Var_004_Ethnicity___race', '')
    ethnicity_code = extract_code_before_equals(ethnicity_raw)

    smoking_raw = patient.get('Var_006_Smoking_status', '')
    # Extract smoking status enum value (e.g., "4=Non-smoker" -> "Never_smoked")
    if '=' in smoking_raw:
        smoking_status = smoking_raw.split('=')[1].strip().replace(' ', '_').replace('', '-')
    else:
        smoking_status = smoking_raw

    family_history = parse_boolean_field(patient.get('Var_008_Family_history_cancer___lung_cancer', ''),
                                         'relative_with_cancer_history')

    labs = parse_pipe_delimited(patient.get('Var_011_Baseline_full_blood_count___haematology_results', ''))
    wbc = safe_float(labs.get('WBC', '').split()[0] if 'WBC' in labs else '')
    hgb = safe_float(labs.get('HGB', '').split()[0] if 'HGB' in labs else '')
    plt = safe_float(labs.get('PLT', '').split()[0] if 'PLT' in labs else '')

    lfts = parse_pipe_delimited(patient.get('Var_014_Baseline_liver_function_tests_LFTs', ''))
    alt = safe_float(lfts.get('ALT', '').split()[0] if 'ALT' in lfts else '')
    ast = safe_float(lfts.get('AST', '').split()[0] if 'AST' in lfts else '')

    cursor.execute("""
        INSERT INTO Patient VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        pid,
        patient.get('Var_001_Patient_identifier_NHS_number___MRN', ''),
        safe_int(patient.get('Var_002_Age_at_diagnosis', '')),
        patient.get('Var_003_Sex', ''),
        ethnicity_code,
        smoking_status,
        safe_float(patient.get('Var_007_Packyear_history', '')),
        1 if family_history else 0,
        safe_int(patient.get('Var_009_ECOG_performance_status', '')),
        safe_float(patient.get('Var_012_Baseline_renal_function_eGFR', '')),
        wbc, hgb, plt, alt, ast,
        diagnosis_date,
        patient.get('Var_015_NICE_NG12___urgent_suspected_cancer_referral_pathway_tri', '')
    ))
    print(f"  [OK] Patient")

    # ========================================================================
    # BIOPSY (2 rows: tissue + ctDNA)
    # ========================================================================
    scan_date = excel_serial_to_date(patient.get('Var_020_Scan_acquisition_date', ''))

    # Biopsy 1: Tissue
    biopsy_site = patient.get('Var_029_Biopsy_target_anatomical_location_SNOMED_CT_coded', '')
    snomed_code = biopsy_site.split()[0] if biopsy_site else ''
    snomed_desc = biopsy_site.replace(snomed_code, '').strip('()') if biopsy_site else ''

    pdl1_antibody_raw = patient.get('Var_044_IHC_antibody_clone_and_staining_platform', '')
    pdl1_antibody = pdl1_antibody_raw.split('|')[0].strip() if '|' in pdl1_antibody_raw else pdl1_antibody_raw

    cursor.execute("""
        INSERT INTO Biopsy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f'BX-{pid}-001',  # biopsy_id
        pid,  # patient_id
        scan_date,  # biopsy_date (proxy)
        'Tissue',  # specimen_type
        patient.get('Var_032_Biopsy_procedure_technique', ''),
        snomed_code,
        snomed_desc,
        patient.get('Var_035_Specimen_category', ''),
        patient.get('Var_036_Preparation_format', ''),
        safe_float(patient.get('Var_037_Fixation_duration_hours_in_fixative', '')),
        safe_float(patient.get('Var_039_Tumour_cellularity__tumour_nuclei', '')),
        safe_float(patient.get('Var_043_Necrosis__of_specimen_showing_necrosis', '')),
        None,  # pathology_slide_image_path
        None,  # pathology_report_pdf_path
        None, None, None, None, None, None, None,  # ctDNA fields (null for tissue)
        patient.get('Var_041_Tumour_subtype_WHO_2021___ICDO3_coded', ''),
        safe_int(patient.get('Var_045_PDL1_TPS_tumour_proportion_score_', '')),
        pdl1_antibody,
        patient.get('Var_034_ROSE_result_Rapid_OnSite_Evaluation', ''),
        patient.get('Var_052_Tissue_sufficiency_status', '')
    ))

    # Biopsy 2: ctDNA
    blood_timestamp = patient.get('Var_057_Time_of_blood_draw_timestamp', '')

    cursor.execute("""
        INSERT INTO Biopsy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f'BX-{pid}-002',  # biopsy_id
        pid,  # patient_id
        blood_timestamp,  # biopsy_date
        'ctDNA',  # specimen_type
        'Venipuncture',  # biopsy_technique
        None, None, None, None, None, None, None, None, None,  # tissue fields (null for ctDNA)
        patient.get('Var_054_Tube_type_BLOODPAC_MTDE_1', ''),
        safe_float(patient.get('Var_056_Collection_volume_mL_BLOODPAC_MTDE_3', '')),
        blood_timestamp,
        safe_float(patient.get('Var_059_Time_from_collection_to_fractionation_hours_BLOODPAC_MTD', '')),
        safe_float(patient.get('Var_062_Plasma_volume_recovered_mL', '')),
        safe_float(patient.get('Var_067_cfDNA_concentration_ng_?L_BLOODPAC_MTDE_10', '')),
        safe_float(patient.get('Var_068_cfDNA_total_yield_ng', '')),
        None, None, None, None, None  # histology fields (null for ctDNA)
    ))
    print(f"  [OK] Biopsy (2 rows)")

    # ========================================================================
    # IMAGING STUDY (1 baseline row)
    # ========================================================================
    ct_params = parse_pipe_delimited(patient.get('Var_021_CT_acquisition_parameters_kVp_mAs_slice_thickness', ''))
    pet_params = parse_pipe_delimited(patient.get('Var_022_PET_radiopharmaceutical_injected_dose_MBq_and_uptake_tim', ''))

    m_stage_raw = patient.get('Var_025_Clinical_Mstage_and_metastatic_sites_TNM_8th_edition', '')
    m_stage = m_stage_raw.split('|')[0].strip() if '|' in m_stage_raw else m_stage_raw
    m_sites = m_stage_raw.split('Sites:')[1].strip() if 'Sites:' in m_stage_raw else ''

    brain_imaging = parse_pipe_delimited(patient.get('Var_028_Brain_imaging_findings_MRI___CT', ''))
    brain_mets = parse_boolean_field(patient.get('Var_028_Brain_imaging_findings_MRI___CT', ''), 'brain_mets_detected')
    brain_lesions = safe_int(brain_imaging.get('n_lesions', '0'))

    cursor.execute("""
        INSERT INTO ImagingStudy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f'IMG-{pid}-001',  # imaging_study_id
        pid,  # patient_id
        patient.get('Var_019_DICOM_series_UID___study_UID', ''),
        None,  # series_uid
        patient.get('Var_016_Imaging_order__accession_number', ''),
        scan_date,
        patient.get('Var_018_Imaging_modality', ''),
        None,  # study_description
        None,  # dicom_file_path
        None,  # thumbnail_image_path
        safe_int(ct_params.get('kVp', '')),
        safe_float(ct_params.get('mAs', '')),
        safe_float(ct_params.get('Slice', '').replace(' mm', '') if 'Slice' in ct_params else ''),
        pet_params.get('Radiopharmaceutical', ''),
        safe_float(pet_params.get('Dose', '').replace(' MBq', '') if 'Dose' in pet_params else ''),
        safe_float(pet_params.get('Uptake', '').replace(' min', '') if 'Uptake' in pet_params else ''),
        patient.get('Var_023_Clinical_Tstage_TNM_8th_edition', ''),
        patient.get('Var_024_Clinical_Nstage_TNM_8th_edition', ''),
        m_stage,
        m_sites,
        patient.get('Var_030_Overall_AJCC_clinical_stage_Stage_IIV', ''),
        safe_float(patient.get('Var_026_Primary_tumour_diameter__RECIST_11_target_lesion_mm', '')),
        safe_float(patient.get('Var_027_SUV_max_standardised_uptake_value_maximum__PETCT', '')),
        1 if brain_mets else 0,
        brain_lesions,
        None  # brain_largest_lesion_mm
    ))
    print(f"  [OK] ImagingStudy (1 baseline)")

    # ========================================================================
    # MOLECULAR TEST (2 rows: tissue NGS + ctDNA NGS)
    # ========================================================================
    # Test 1: Tissue NGS
    cursor.execute("""
        INSERT INTO MolecularTest VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f'NGS-{pid}-001',  # molecular_test_id
        f'BX-{pid}-001',  # biopsy_id (tissue)
        scan_date,  # test_date (proxy)
        'Tissue',  # specimen_source
        patient.get('Var_046_Tissue_NGS_panel_name_and_version', ''),
        None,  # ngs_panel_version
        patient.get('Var_047_NGS_assay_type_DNA___RNA___concurrent_DNARNA', ''),
        safe_float(patient.get('Var_048_DNA_input_mass__tissue_NGS_ng', '')),
        safe_float(patient.get('Var_049_Mean_ontarget_coverage_depth__tissue_NGS_', '')),
        safe_float(patient.get('Var_080_Assay_limit_of_detection_LOD_', '')),
        None,  # ngs_report_pdf_path
        None   # vcf_file_path
    ))

    # Test 2: ctDNA NGS
    cursor.execute("""
        INSERT INTO MolecularTest VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f'NGS-{pid}-002',  # molecular_test_id
        f'BX-{pid}-002',  # biopsy_id (ctDNA)
        blood_timestamp,  # test_date
        'ctDNA',  # specimen_source
        'Guardant360',  # ngs_panel_name (common ctDNA panel)
        None,  # ngs_panel_version
        'DNA_only',  # ngs_assay_type
        None,  # dna_input_mass_ng (not typical for ctDNA)
        safe_float(patient.get('Var_073_Mean_ontarget_coverage_depth__ctDNA_NGS_', '')),
        safe_float(patient.get('Var_080_Assay_limit_of_detection_LOD_', '')),
        None,  # ngs_report_pdf_path
        None   # vcf_file_path
    ))
    print(f"  [OK] MolecularTest (2 rows)")

    # ========================================================================
    # MUTATION (2+ rows: EGFR from tissue + EGFR from ctDNA)
    # ========================================================================
    # Mutation 1: Tissue EGFR
    tissue_mutation_raw = patient.get('Var_050_EGFR_mutation_detected__tissue_HGVS_notation', '')
    if tissue_mutation_raw:
        # Parse: "EGFR Ex19del | HGVS: p.Glu746_Ala750del (c.2235_2249del15)"
        parts = tissue_mutation_raw.split('|')
        gene_and_type = parts[0].strip()
        tokens = gene_and_type.split()
        gene = tokens[0] if tokens else ""
        mutation_type = ' '.join(tokens[1:]) if len(tokens) > 1 else ""

        hgvs = ""
        if len(parts) > 1 and 'HGVS:' in parts[1]:
            hgvs = parts[1].replace('HGVS:', '').strip()

        cursor.execute("""
            INSERT INTO Mutation VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f'MUT-{pid}-001',  # mutation_id
            f'NGS-{pid}-001',  # molecular_test_id
            gene,
            hgvs,
            mutation_type,
            patient.get('Var_078_Variant_tier_classification_Tier_IIV_AMP_ASCO_CAP', ''),
            safe_float(patient.get('Var_051_VAF__tissue_NGS_', '')),
            None,  # tumor_fraction_percent
            1,  # actionable_mutation
            0,  # resistance_mutation
            None,  # chip_status
            1,  # is_primary_driver
            0,  # is_acquired_resistance
            'Baseline'  # detection_timepoint
        ))

    # Mutation 2: ctDNA EGFR
    ctdna_mutation_raw = patient.get('Var_074_EGFR_mutation_detected__ctDNA_HGVS_notation', '')
    if ctdna_mutation_raw:
        parts = ctdna_mutation_raw.split('|')
        gene_and_type = parts[0].strip()
        tokens = gene_and_type.split()
        gene = tokens[0] if tokens else ""
        mutation_type = ' '.join(tokens[1:]) if len(tokens) > 1 else ""
        if '(ctDNA)' in mutation_type:
            mutation_type = mutation_type.replace('(ctDNA)', '').strip()

        hgvs = ""
        if len(parts) > 1 and 'HGVS:' in parts[1]:
            hgvs = parts[1].replace('HGVS:', '').strip()
            if '(ctDNA)' in hgvs:
                hgvs = hgvs.split('(ctDNA)')[0].strip()

        tumor_fraction_raw = patient.get('Var_076_Tumour_fraction_estimate_ppm___', '')
        tumor_fraction_parsed = parse_pipe_delimited(tumor_fraction_raw)
        tumor_fraction_pct = safe_float(tumor_fraction_parsed.get('tumour_fraction_%', ''))

        cursor.execute("""
            INSERT INTO Mutation VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            f'MUT-{pid}-002',  # mutation_id
            f'NGS-{pid}-002',  # molecular_test_id
            gene,
            hgvs,
            mutation_type,
            patient.get('Var_078_Variant_tier_classification_Tier_IIV_AMP_ASCO_CAP', ''),
            safe_float(patient.get('Var_075_ctDNA_VAF_at_timepoint_', '')),
            tumor_fraction_pct,
            1,  # actionable_mutation
            0,  # resistance_mutation
            patient.get('Var_077_CHIP_status_per_variant_yes___no___unknown', ''),
            1,  # is_primary_driver
            0,  # is_acquired_resistance
            'Baseline'  # detection_timepoint
        ))
    print(f"  [OK] Mutation (2 rows)")

    # ========================================================================
    # TREATMENT (1 row from CSV)
    # ========================================================================
    drug_info = parse_pipe_delimited(patient.get('Var_087_Drug_name_dose_and_route_of_administration', ''))
    mdt_info = parse_pipe_delimited(patient.get('Var_084_MDT_treatment_recommendation', ''))
    ici_info = parse_pipe_delimited(patient.get('Var_089_ICI_exposure_history_time_since_last_ICI_months', ''))

    prior_ici = parse_boolean_field(patient.get('Var_089_ICI_exposure_history_time_since_last_ICI_months', ''),
                                    'recent_ICI_exposure_le3months')

    cursor.execute("""
        INSERT INTO Treatment VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f'TX-{pid}-001',  # treatment_id
        pid,  # patient_id
        0,  # treatment_line (surgery is line 0)
        patient.get('Var_086_Treatment_intent', ''),
        drug_info.get('drug_name', ''),
        safe_float(drug_info.get('dose_mg', '')),
        drug_info.get('frequency', ''),
        drug_info.get('route', ''),
        diagnosis_date,  # treatment_start_date (proxy)
        diagnosis_date,  # treatment_end_date (same day for surgery)
        str(mdt_info),  # mdt_recommendation
        diagnosis_date,  # mdt_date (proxy)
        1 if prior_ici else 0,
        safe_float(ici_info.get('months_since_last_ICI', '')),
        None  # discontinuation_reason
    ))
    print(f"  [OK] Treatment (1 baseline)")

    # ========================================================================
    # RESPONSE ASSESSMENT (2 rows from Var_092) - SKIPPING FOR NOW
    # Schema requires NOT NULL for foreign keys, will add from time-series CSV
    # ========================================================================
    print(f"  [SKIP] ResponseAssessment (will load from time-series CSV)")

    # ========================================================================
    # CLINICAL ASSESSMENT (1 baseline row)
    # ========================================================================
    cursor.execute("""
        INSERT INTO ClinicalAssessment VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        f'CLIN-{pid}-001',  # clinical_assessment_id
        pid,  # patient_id
        diagnosis_date,  # assessment_date
        'Baseline',  # visit_type
        safe_int(patient.get('Var_009_ECOG_performance_status', '')),
        patient.get('Var_005_Presenting_symptoms_coded', ''),
        None,  # symptom_severity_grade
        wbc,
        hgb,
        plt,
        None,  # neutrophils
        safe_float(patient.get('Var_012_Baseline_renal_function_eGFR', '')),
        alt,
        ast
    ))
    print(f"  [OK] ClinicalAssessment (1 baseline)")

conn.commit()
print(f"\n[OK] Loaded baseline data for {len(patients_data)} patients")

# ============================================================================
# STEP 3: LOAD TIME-SERIES DATA FROM CSVs
# ============================================================================

print("\n" + "=" * 80)
print("LOADING TIME-SERIES DATA FROM mock_simulated/")
print("=" * 80)

# Load imaging studies
imaging_csv = mock_dir / 'imaging_studies_timeseries.csv'
with open(imaging_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    imaging_rows = list(reader)

    for row in imaging_rows:
        cursor.execute("""
            INSERT INTO ImagingStudy VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['imaging_study_id'],
            row['patient_id'],
            row['study_uid'],
            None,  # series_uid
            row['accession_number'],
            row['scan_date'],
            row['imaging_modality'],
            None,  # study_description
            None,  # dicom_file_path
            None,  # thumbnail_image_path
            None,  # ct_kvp
            None,  # ct_mas
            None,  # ct_slice_thickness_mm
            None,  # pet_tracer
            None,  # pet_injected_dose_mbq
            safe_float(row['suv_max']) if row['suv_max'] else None,
            row['t_stage'],
            row['n_stage'],
            row['m_stage'],
            None,  # m_sites
            row['ajcc_stage'],
            safe_float(row['primary_tumor_diameter_mm']),
            safe_float(row['suv_max']) if row['suv_max'] else None,
            1 if row['brain_metastasis_present'] == 'TRUE' else 0,
            safe_int(row['brain_lesion_count']),
            None  # brain_largest_lesion_mm
        ))

print(f"[OK] Loaded {len(imaging_rows)} imaging studies")

# Load treatments
treatments_csv = mock_dir / 'treatments_timeseries.csv'
with open(treatments_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    treatment_rows = list(reader)

    for row in treatment_rows:
        cursor.execute("""
            INSERT INTO Treatment VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['treatment_id'],
            row['patient_id'],
            safe_int(row['treatment_line']),
            row['treatment_intent'],
            row['drug_name'],
            safe_float(row['drug_dose_mg']),
            row['drug_frequency'],
            row['drug_route'],
            row['treatment_start_date'],
            row['treatment_end_date'] if row['treatment_end_date'] else None,
            row['mdt_recommendation'],
            None,  # mdt_date
            None,  # prior_ici_exposure
            None,  # months_since_last_ici
            row['discontinuation_reason'] if row['discontinuation_reason'] else None
        ))

print(f"[OK] Loaded {len(treatment_rows)} treatments")

# Load response assessments
response_csv = mock_dir / 'response_assessments_timeseries.csv'
with open(response_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    response_rows = list(reader)

    for row in response_rows:
        # Foreign keys are now nullable in the updated schema
        treatment_id = row['treatment_id'] if row['treatment_id'] else None
        imaging_study_id = row['imaging_study_id'] if row['imaging_study_id'] else None
        molecular_test_id = row['molecular_test_id'] if row['molecular_test_id'] else None

        cursor.execute("""
            INSERT INTO ResponseAssessment VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['assessment_id'],
            row['patient_id'],
            treatment_id,
            imaging_study_id,
            molecular_test_id,
            row['assessment_date'],
            row['assessment_type'],
            row['recist_response'],
            safe_float(row['sum_target_lesions_mm']),
            safe_float(row['percent_change_from_baseline']),
            1 if row['new_lesions_present'] == 'TRUE' else 0,
            safe_float(row['ctdna_vaf_percent']),
            1 if row['ctdna_mutation_cleared'] == 'TRUE' else 0,
            None,  # ctdna_tumor_fraction_percent
            safe_int(row['ecog_status']),
            None,  # symptom_improvement
            1 if row['progression_detected'] == 'TRUE' else 0,
            row['progression_type'] if row['progression_type'] else None,
            None,  # time_to_progression_months
            1 if row['resistance_mutation_detected'] == 'TRUE' else 0,
            row['resistance_mechanism'] if row['resistance_mechanism'] else None,
            0  # histologic_transformation
        ))

print(f"[OK] Loaded response assessments (filtered for NOT NULL constraints)")

# Load clinical assessments
clinical_csv = mock_dir / 'clinical_assessments_timeseries.csv'
with open(clinical_csv, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    clinical_rows = list(reader)

    for row in clinical_rows:
        cursor.execute("""
            INSERT INTO ClinicalAssessment VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row['clinical_assessment_id'],
            row['patient_id'],
            row['assessment_date'],
            row['visit_type'],
            safe_int(row['ecog_status']),
            None,  # symptoms_coded
            None,  # symptom_severity_grade
            safe_float(row['wbc']),
            safe_float(row['hemoglobin']),
            safe_float(row['platelets']),
            None,  # neutrophils
            safe_float(row['egfr_value']),
            safe_float(row['alt']),
            safe_float(row['ast'])
        ))

print(f"[OK] Loaded {len(clinical_rows)} clinical assessments")

conn.commit()

# ============================================================================
# STEP 4: VERIFY DATA
# ============================================================================

print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

# Count rows per table
tables = ['Patient', 'Biopsy', 'ImagingStudy', 'MolecularTest', 'Mutation',
          'Treatment', 'ResponseAssessment', 'ClinicalAssessment']

total_rows = 0
for table in tables:
    count = cursor.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0]
    print(f"  {table:25s}: {count:4d} rows")
    total_rows += count

print(f"  {'TOTAL':25s}: {total_rows:4d} rows")

# Verify foreign keys
print("\nForeign key checks:")

orphan_biopsies = cursor.execute("""
    SELECT COUNT(*) FROM Biopsy b
    LEFT JOIN Patient p ON b.patient_id = p.patient_id
    WHERE p.patient_id IS NULL
""").fetchone()[0]
print(f"  Orphan biopsies: {orphan_biopsies}")

orphan_molecular = cursor.execute("""
    SELECT COUNT(*) FROM MolecularTest mt
    LEFT JOIN Biopsy b ON mt.biopsy_id = b.biopsy_id
    WHERE b.biopsy_id IS NULL
""").fetchone()[0]
print(f"  Orphan molecular tests: {orphan_molecular}")

orphan_mutations = cursor.execute("""
    SELECT COUNT(*) FROM Mutation m
    LEFT JOIN MolecularTest mt ON m.molecular_test_id = mt.molecular_test_id
    WHERE mt.molecular_test_id IS NULL
""").fetchone()[0]
print(f"  Orphan mutations: {orphan_mutations}")

# Verify time-series continuity for NGDX-001
print("\nTime-series check for NGDX-001:")
ngdx001_imaging = cursor.execute("""
    SELECT COUNT(*) FROM ImagingStudy WHERE patient_id = 'NGDX-001'
""").fetchone()[0]
print(f"  Imaging studies: {ngdx001_imaging}")

ngdx001_response = cursor.execute("""
    SELECT COUNT(*) FROM ResponseAssessment WHERE patient_id = 'NGDX-001'
""").fetchone()[0]
print(f"  Response assessments: {ngdx001_response}")

ngdx001_clinical = cursor.execute("""
    SELECT COUNT(*) FROM ClinicalAssessment WHERE patient_id = 'NGDX-001'
""").fetchone()[0]
print(f"  Clinical assessments: {ngdx001_clinical}")

conn.commit()
conn.close()

print("\n" + "=" * 80)
print("DATABASE POPULATION COMPLETE")
print("=" * 80)
print(f"Database: {db_path}")
print(f"Total rows: {total_rows}")
print(f"Patients: {len(PATIENT_IDS)}")
print("\nReady for dashboard integration!")