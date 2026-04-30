#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete data extraction and mapping analysis for top 5 patients.
Shows what data EXISTS in simulated_data.csv vs what needs to be GENERATED.
"""

import csv
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Set UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

# Excel date conversion
def excel_serial_to_date(serial):
    """Convert Excel serial date to YYYY-MM-DD"""
    if not serial or serial == '':
        return None
    try:
        base_date = datetime(1899, 12, 30)
        date = base_date + timedelta(days=int(serial))
        return date.strftime("%Y-%m-%d")
    except:
        return None

# Parsing functions
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

def parse_mutation_string(mutation_str):
    """Parse EGFR mutation string"""
    if not mutation_str or mutation_str == '':
        return None

    # "EGFR Ex19del | HGVS: p.Glu746_Ala750del (c.2235_2249del15)"
    parts = mutation_str.split('|')

    gene_and_type = parts[0].strip()
    tokens = gene_and_type.split()
    gene = tokens[0] if tokens else ""
    mutation_type = ' '.join(tokens[1:]) if len(tokens) > 1 else ""

    hgvs_p = ""
    hgvs_c = ""
    if len(parts) > 1:
        hgvs_part = parts[1].strip()
        if 'HGVS:' in hgvs_part:
            hgvs_full = hgvs_part.replace('HGVS:', '').strip()
            # Extract p. and c. notation
            if '(' in hgvs_full:
                hgvs_p = hgvs_full.split('(')[0].strip()
                hgvs_c = hgvs_full.split('(')[1].replace(')', '').strip()
            else:
                hgvs_p = hgvs_full

    return {
        'gene': gene,
        'type': mutation_type,
        'hgvs_p': hgvs_p,
        'hgvs_c': hgvs_c
    }

def parse_response_assessments(var_092_value):
    """Parse multiple response assessments from Var_092"""
    if not var_092_value or var_092_value == '':
        return []

    # "Baseline: 40.7 mm | Assessment 1: 31.6 mm"
    assessments = []
    parts = var_092_value.split('|')
    for part in parts:
        part = part.strip()
        if ':' in part:
            timepoint, value_str = part.split(':', 1)
            value_str = value_str.strip().replace(' mm', '')
            try:
                value = float(value_str)
                assessments.append({
                    'timepoint': timepoint.strip(),
                    'sum_target_lesions_mm': value
                })
            except:
                pass
    return assessments

# Read CSV
csv_path = Path(__file__).parent.parent / "example_files" / "simulated_data.csv"

with open(csv_path, 'r', encoding='latin-1') as f:
    reader = csv.reader(f)
    first_header = next(reader)
    var_headers = next(reader)
    headers = [first_header[0]] + var_headers[1:]

    patients = []
    for row in reader:
        if row and row[0]:
            patient_dict = dict(zip(headers, row))
            patients.append(patient_dict)

# Select top 5 patients
top5 = patients[:5]

print("=" * 150)
print("COMPLETE DATA EXTRACTION FOR TOP 5 PATIENTS")
print("=" * 150)

for patient in top5:
    pid = patient.get('Patient_ID', '')

    print(f"\n{'='*150}")
    print(f"PATIENT: {pid}")
    print(f"{'='*150}")

    # ===== PATIENT (Dimension Table) =====
    print("\n[Patient] - 1 row")
    print(f"  patient_id: {pid}")
    print(f"  nhs_number: {patient.get('Var_001_Patient_identifier_NHS_number___MRN', '')}")
    print(f"  age_at_diagnosis: {patient.get('Var_002_Age_at_diagnosis', '')}")
    print(f"  sex: {patient.get('Var_003_Sex', '')}")

    ethnicity_raw = patient.get('Var_004_Ethnicity___race', '')
    ethnicity_code = ethnicity_raw.split('=')[0] if '=' in ethnicity_raw else ethnicity_raw
    print(f"  ethnicity_code: {ethnicity_code}")

    smoking_raw = patient.get('Var_006_Smoking_status', '')
    print(f"  smoking_status: {smoking_raw}")

    print(f"  pack_years: {patient.get('Var_007_Packyear_history', '')}")

    family_history_raw = patient.get('Var_008_Family_history_cancer___lung_cancer', '')
    print(f"  family_history_lung_cancer: {family_history_raw}")

    print(f"  ecog_baseline: {patient.get('Var_009_ECOG_performance_status', '')}")
    print(f"  baseline_egfr: {patient.get('Var_012_Baseline_renal_function_eGFR', '')}")

    # Parse labs
    labs = parse_pipe_delimited(patient.get('Var_011_Baseline_full_blood_count___haematology_results', ''))
    print(f"  baseline_wbc: {labs.get('WBC', '').split()[0] if 'WBC' in labs else ''}")
    print(f"  baseline_hemoglobin: {labs.get('HGB', '').split()[0] if 'HGB' in labs else ''}")
    print(f"  baseline_platelets: {labs.get('PLT', '').split()[0] if 'PLT' in labs else ''}")

    lfts = parse_pipe_delimited(patient.get('Var_014_Baseline_liver_function_tests_LFTs', ''))
    print(f"  baseline_alt: {lfts.get('ALT', '').split()[0] if 'ALT' in lfts else ''}")
    print(f"  baseline_ast: {lfts.get('AST', '').split()[0] if 'AST' in lfts else ''}")

    diagnosis_date_serial = patient.get('Var_017_Date_of_first_clinical_presentation___diagnosis_date', '')
    diagnosis_date = excel_serial_to_date(diagnosis_date_serial)
    print(f"  diagnosis_date: {diagnosis_date} (from Excel serial: {diagnosis_date_serial})")

    print(f"  diagnosis_pathway: {patient.get('Var_015_NICE_NG12___urgent_suspected_cancer_referral_pathway_tri', '')}")

    # ===== BIOPSY (Fact Table) - 2 rows expected =====
    print("\n[Biopsy] - Expected 2 rows (tissue + ctDNA)")

    print("\n  Biopsy 1 (Tissue):")
    print(f"    biopsy_id: BX-{pid}-001 (GENERATED)")
    scan_date_serial = patient.get('Var_020_Scan_acquisition_date', '')
    scan_date = excel_serial_to_date(scan_date_serial)
    print(f"    biopsy_date: {scan_date} (proxy from Var_020)")
    print(f"    specimen_type: Tissue")
    print(f"    biopsy_technique: {patient.get('Var_032_Biopsy_procedure_technique', '')}")

    biopsy_site = patient.get('Var_029_Biopsy_target_anatomical_location_SNOMED_CT_coded', '')
    snomed_code = biopsy_site.split()[0] if biopsy_site else ''
    snomed_desc = biopsy_site.replace(snomed_code, '').strip('()') if biopsy_site else ''
    print(f"    biopsy_site_snomed: {snomed_code}")
    print(f"    biopsy_site_description: {snomed_desc}")

    print(f"    tissue_specimen_category: {patient.get('Var_035_Specimen_category', '')}")
    print(f"    tissue_preparation_format: {patient.get('Var_036_Preparation_format', '')}")
    print(f"    tissue_fixation_hours: {patient.get('Var_037_Fixation_duration_hours_in_fixative', '')}")
    print(f"    tumor_cellularity_percent: {patient.get('Var_039_Tumour_cellularity__tumour_nuclei', '')}")
    print(f"    necrosis_percent: {patient.get('Var_043_Necrosis__of_specimen_showing_necrosis', '')}")
    print(f"    histologic_subtype: {patient.get('Var_041_Tumour_subtype_WHO_2021___ICDO3_coded', '')}")
    print(f"    pdl1_tps_percent: {patient.get('Var_045_PDL1_TPS_tumour_proportion_score_', '')}")

    pdl1_antibody = parse_pipe_delimited(patient.get('Var_044_IHC_antibody_clone_and_staining_platform', ''))
    print(f"    pdl1_antibody_clone: {list(pdl1_antibody.keys())[0] if pdl1_antibody else ''}")

    print(f"    specimen_adequacy: {patient.get('Var_034_ROSE_result_Rapid_OnSite_Evaluation', '')}")
    print(f"    tissue_sufficiency: {patient.get('Var_052_Tissue_sufficiency_status', '')}")

    print("\n  Biopsy 2 (ctDNA):")
    print(f"    biopsy_id: BX-{pid}-002 (GENERATED)")

    blood_timestamp = patient.get('Var_057_Time_of_blood_draw_timestamp', '')
    print(f"    biopsy_date: {blood_timestamp}")
    print(f"    specimen_type: ctDNA")
    print(f"    blood_tube_type: {patient.get('Var_054_Tube_type_BLOODPAC_MTDE_1', '')}")
    print(f"    blood_collection_volume_ml: {patient.get('Var_056_Collection_volume_mL_BLOODPAC_MTDE_3', '')}")
    print(f"    blood_draw_timestamp: {blood_timestamp}")
    print(f"    time_to_fractionation_hours: {patient.get('Var_059_Time_from_collection_to_fractionation_hours_BLOODPAC_MTD', '')}")
    print(f"    plasma_volume_ml: {patient.get('Var_062_Plasma_volume_recovered_mL', '')}")
    print(f"    cfdna_concentration_ng_ul: {patient.get('Var_067_cfDNA_concentration_ng_?L_BLOODPAC_MTDE_10', '')}")
    print(f"    cfdna_total_yield_ng: {patient.get('Var_068_cfDNA_total_yield_ng', '')}")

    # ===== IMAGING STUDY (Fact Table) - 1 row from CSV, need 4-6 more =====
    print("\n[ImagingStudy] - CSV has 1 (baseline), NEED 4-6 total")
    print("\n  ImagingStudy 1 (Baseline - FROM CSV):")
    print(f"    imaging_study_id: IMG-{pid}-001 (GENERATED)")
    print(f"    scan_date: {scan_date}")
    print(f"    imaging_modality: {patient.get('Var_018_Imaging_modality', '')}")
    print(f"    study_uid: {patient.get('Var_019_DICOM_series_UID___study_UID', '')}")
    print(f"    accession_number: {patient.get('Var_016_Imaging_order__accession_number', '')}")

    ct_params = parse_pipe_delimited(patient.get('Var_021_CT_acquisition_parameters_kVp_mAs_slice_thickness', ''))
    print(f"    ct_kvp: {ct_params.get('kVp', '')}")
    print(f"    ct_mas: {ct_params.get('mAs', '')}")
    print(f"    ct_slice_thickness_mm: {ct_params.get('Slice', '').replace(' mm', '') if 'Slice' in ct_params else ''}")

    pet_params = parse_pipe_delimited(patient.get('Var_022_PET_radiopharmaceutical_injected_dose_MBq_and_uptake_tim', ''))
    print(f"    pet_tracer: {pet_params.get('Radiopharmaceutical', '')}")
    print(f"    pet_injected_dose_mbq: {pet_params.get('Dose', '').replace(' MBq', '') if 'Dose' in pet_params else ''}")
    print(f"    pet_uptake_time_min: {pet_params.get('Uptake', '').replace(' min', '') if 'Uptake' in pet_params else ''}")

    print(f"    t_stage: {patient.get('Var_023_Clinical_Tstage_TNM_8th_edition', '')}")
    print(f"    n_stage: {patient.get('Var_024_Clinical_Nstage_TNM_8th_edition', '')}")

    m_stage_raw = patient.get('Var_025_Clinical_Mstage_and_metastatic_sites_TNM_8th_edition', '')
    m_stage = m_stage_raw.split('|')[0].strip() if '|' in m_stage_raw else m_stage_raw
    m_sites = m_stage_raw.split('Sites:')[1].strip() if 'Sites:' in m_stage_raw else ''
    print(f"    m_stage: {m_stage}")
    print(f"    m_sites: {m_sites}")

    print(f"    ajcc_stage: {patient.get('Var_030_Overall_AJCC_clinical_stage_Stage_IIV', '')}")
    print(f"    primary_tumor_diameter_mm: {patient.get('Var_026_Primary_tumour_diameter__RECIST_11_target_lesion_mm', '')}")
    print(f"    suv_max: {patient.get('Var_027_SUV_max_standardised_uptake_value_maximum__PETCT', '')}")

    brain_imaging = parse_pipe_delimited(patient.get('Var_028_Brain_imaging_findings_MRI___CT', ''))
    print(f"    brain_metastasis_present: {brain_imaging.get('brain_mets_detected', '')}")
    print(f"    brain_lesion_count: {brain_imaging.get('n_lesions', '')}")

    print("\n  ImagingStudy 2-6: *** NEED TO GENERATE (follow-up scans over time) ***")

    # ===== MOLECULAR TEST (Fact Table) - 2 rows expected =====
    print("\n[MolecularTest] - Expected 2 rows (tissue NGS + ctDNA NGS)")

    print("\n  MolecularTest 1 (Tissue NGS):")
    print(f"    molecular_test_id: NGS-{pid}-001 (GENERATED)")
    print(f"    biopsy_id: BX-{pid}-001 (links to tissue biopsy)")
    print(f"    test_date: {scan_date} (proxy from scan date)")
    print(f"    specimen_source: Tissue")

    ngs_panel = patient.get('Var_046_Tissue_NGS_panel_name_and_version', '')
    print(f"    ngs_panel_name: {ngs_panel}")
    print(f"    ngs_panel_version: (parse from above if contains version)")

    print(f"    ngs_assay_type: {patient.get('Var_047_NGS_assay_type_DNA___RNA___concurrent_DNARNA', '')}")
    print(f"    dna_input_mass_ng: {patient.get('Var_048_DNA_input_mass__tissue_NGS_ng', '')}")
    print(f"    mean_coverage_depth: {patient.get('Var_049_Mean_ontarget_coverage_depth__tissue_NGS_', '')}")
    print(f"    assay_lod_percent: {patient.get('Var_080_Assay_limit_of_detection_LOD_', '')}")

    print("\n  MolecularTest 2 (ctDNA NGS):")
    print(f"    molecular_test_id: NGS-{pid}-002 (GENERATED)")
    print(f"    biopsy_id: BX-{pid}-002 (links to ctDNA biopsy)")
    print(f"    test_date: {blood_timestamp}")
    print(f"    specimen_source: ctDNA")

    print(f"    ngs_panel_name: (inferred from Var_070 or use common ctDNA panel)")
    print(f"    mean_coverage_depth: {patient.get('Var_073_Mean_ontarget_coverage_depth__ctDNA_NGS_', '')}")

    # ===== MUTATION (Fact Table) - 2+ rows expected =====
    print("\n[Mutation] - Expected 2+ rows (EGFR from tissue + EGFR from ctDNA + co-mutations)")

    print("\n  Mutation 1 (Tissue NGS - EGFR):")
    tissue_mutation = parse_mutation_string(patient.get('Var_050_EGFR_mutation_detected__tissue_HGVS_notation', ''))
    if tissue_mutation:
        print(f"    mutation_id: MUT-{pid}-001 (GENERATED)")
        print(f"    molecular_test_id: NGS-{pid}-001")
        print(f"    gene_symbol: {tissue_mutation['gene']}")
        print(f"    mutation_type: {tissue_mutation['type']}")
        print(f"    mutation_hgvs: {tissue_mutation['hgvs_p']} ({tissue_mutation['hgvs_c']})")
        print(f"    vaf_percent: {patient.get('Var_051_VAF__tissue_NGS_', '')}")
        print(f"    mutation_classification: {patient.get('Var_078_Variant_tier_classification_Tier_IIV_AMP_ASCO_CAP', '')}")
        print(f"    actionable_mutation: TRUE (if Tier_I)")
        print(f"    is_primary_driver: TRUE")
        print(f"    detection_timepoint: Baseline")

    print("\n  Mutation 2 (ctDNA NGS - EGFR):")
    ctdna_mutation = parse_mutation_string(patient.get('Var_074_EGFR_mutation_detected__ctDNA_HGVS_notation', ''))
    if ctdna_mutation:
        print(f"    mutation_id: MUT-{pid}-002 (GENERATED)")
        print(f"    molecular_test_id: NGS-{pid}-002")
        print(f"    gene_symbol: {ctdna_mutation['gene']}")
        print(f"    mutation_type: {ctdna_mutation['type']}")
        print(f"    mutation_hgvs: {ctdna_mutation['hgvs_p']} ({ctdna_mutation['hgvs_c']})")
        print(f"    vaf_percent: {patient.get('Var_075_ctDNA_VAF_at_timepoint_', '')}")

        tumor_fraction = parse_pipe_delimited(patient.get('Var_076_Tumour_fraction_estimate_ppm___', ''))
        print(f"    tumor_fraction_percent: {tumor_fraction.get('tumour_fraction_%', '')}")

        print(f"    chip_status: {patient.get('Var_077_CHIP_status_per_variant_yes___no___unknown', '')}")
        print(f"    is_primary_driver: TRUE")
        print(f"    detection_timepoint: Baseline")

    print("\n  Mutation 3+: *** CHECK IF CO-MUTATIONS (TP53, MET, etc.) present in CSV ***")

    # ===== TREATMENT (Fact Table) - 1-2 rows expected =====
    print("\n[Treatment] - CSV has 1, may need 1-2 more for progression")

    print("\n  Treatment 1 (FROM CSV):")
    print(f"    treatment_id: TX-{pid}-001 (GENERATED)")
    print(f"    treatment_line: 0 (surgery) or 1 (systemic)")
    print(f"    treatment_intent: {patient.get('Var_086_Treatment_intent', '')}")

    drug_info = parse_pipe_delimited(patient.get('Var_087_Drug_name_dose_and_route_of_administration', ''))
    print(f"    drug_name: {drug_info.get('drug_name', '')}")
    print(f"    drug_dose_mg: {drug_info.get('dose_mg', '')}")
    print(f"    drug_frequency: {drug_info.get('frequency', '')}")
    print(f"    drug_route: {drug_info.get('route', '')}")

    print(f"    treatment_start_date: {diagnosis_date} (proxy)")

    ttp = patient.get('Var_099_Time_from_initial_diagnosis_to_progression_months', '')
    if ttp and ttp != '':
        print(f"    treatment_end_date: (calculate: {diagnosis_date} + {ttp} months)")

    mdt = parse_pipe_delimited(patient.get('Var_084_MDT_treatment_recommendation', ''))
    print(f"    mdt_recommendation: {mdt}")

    ici_exposure = parse_pipe_delimited(patient.get('Var_089_ICI_exposure_history_time_since_last_ICI_months', ''))
    print(f"    prior_ici_exposure: {ici_exposure.get('recent_ICI_exposure_le3months', '')}")
    print(f"    months_since_last_ici: {ici_exposure.get('months_since_last_ICI', '')}")

    print("\n  Treatment 2-3: *** NEED TO GENERATE (if progression occurred) ***")

    # ===== RESPONSE ASSESSMENT (Fact Table) - Parse Var_092 =====
    print("\n[ResponseAssessment] - Parse Var_092 for multiple timepoints")

    var_092 = patient.get('Var_092_Sum_of_target_lesion_diameters_mm_at_each_monitoring_tim', '')
    assessments = parse_response_assessments(var_092)

    print(f"\n  Var_092 raw: {var_092}")
    print(f"  Parsed {len(assessments)} assessment(s):")

    for i, assessment in enumerate(assessments, 1):
        print(f"\n  ResponseAssessment {i}:")
        print(f"    assessment_id: ASSESS-{pid}-{i:03d} (GENERATED)")
        print(f"    assessment_date: *** NEED TO CALCULATE from baseline + interval ***")
        print(f"    assessment_type: {assessment['timepoint']}")
        print(f"    sum_target_lesions_mm: {assessment['sum_target_lesions_mm']}")
        print(f"    recist_response: {patient.get('Var_091_RECIST_11_response_assessment_category', '') if i == 1 else 'CALCULATE'}")

        if i == 1:
            print(f"    ctdna_vaf_percent: {patient.get('Var_075_ctDNA_VAF_at_timepoint_', '')}")
            clearance = parse_pipe_delimited(patient.get('Var_093_Clearance_of_primary_EGFR_mutation_from_ctDNA_boolean', ''))
            print(f"    ctdna_mutation_cleared: {clearance.get('mutation_cleared', '')}")

    print("\n  ResponseAssessment (additional): *** NEED TO GENERATE (3-5 more timepoints) ***")

    # ===== CLINICAL ASSESSMENT (Fact Table) =====
    print("\n[ClinicalAssessment] - CSV has baseline data, NEED 5-8 total")

    print("\n  ClinicalAssessment 1 (Baseline - FROM CSV):")
    print(f"    clinical_assessment_id: CLIN-{pid}-001 (GENERATED)")
    print(f"    assessment_date: {diagnosis_date}")
    print(f"    visit_type: Baseline")
    print(f"    ecog_status: {patient.get('Var_009_ECOG_performance_status', '')}")
    print(f"    symptoms_coded: {patient.get('Var_005_Presenting_symptoms_coded', '')}")
    print(f"    wbc: {labs.get('WBC', '').split()[0] if 'WBC' in labs else ''}")
    print(f"    hemoglobin: {labs.get('HGB', '').split()[0] if 'HGB' in labs else ''}")
    print(f"    platelets: {labs.get('PLT', '').split()[0] if 'PLT' in labs else ''}")
    print(f"    egfr_value: {patient.get('Var_012_Baseline_renal_function_eGFR', '')}")
    print(f"    alt: {lfts.get('ALT', '').split()[0] if 'ALT' in lfts else ''}")
    print(f"    ast: {lfts.get('AST', '').split()[0] if 'AST' in lfts else ''}")

    print("\n  ClinicalAssessment 2-8: *** NEED TO GENERATE (follow-up visits) ***")

    # ===== SUMMARY =====
    print(f"\n{'='*150}")
    print(f"SUMMARY FOR {pid}:")
    print(f"{'='*150}")
    print(f"  ✓ Patient: 1 row complete from CSV")
    print(f"  ✓ Biopsy: 2 rows parseable from CSV")
    print(f"  ✗ ImagingStudy: 1 row from CSV, NEED 4-6 total (GENERATE 3-5 more)")
    print(f"  ✓ MolecularTest: 2 rows parseable from CSV")
    print(f"  ✓ Mutation: 2+ rows parseable from CSV")
    print(f"  ✗ Treatment: 1 row from CSV, NEED 1-3 more if progression (GENERATE)")
    print(f"  ~ ResponseAssessment: {len(assessments)} from Var_092, NEED 5-7 total (GENERATE more)")
    print(f"  ✗ ClinicalAssessment: 1 row from CSV, NEED 6-8 total (GENERATE 5-7 more)")

    print("\n")

# ===== FINAL SUMMARY =====
print("\n" + "=" * 150)
print("FINAL DATA GENERATION REQUIREMENTS")
print("=" * 150)

print("""
FROM simulated_data.csv (can be PARSED and used directly):
  ✓ Patient dimension table - complete
  ✓ Biopsy (2 rows per patient: tissue + ctDNA)
  ✓ MolecularTest (2 rows per patient: tissue NGS + ctDNA NGS)
  ✓ Mutation (2+ rows per patient: EGFR from tissue + EGFR from ctDNA)
  ✓ ImagingStudy (1 baseline row per patient)
  ✓ Treatment (1 row per patient - first line)
  ~ ResponseAssessment (1-2 rows per patient from Var_092)
  ✓ ClinicalAssessment (1 baseline row per patient)

NEED TO GENERATE (time-series mock data):
  ✗ ImagingStudy: 3-5 additional scans per patient (follow-up, progression)
  ✗ Treatment: 1-2 additional treatment lines per patient (post-progression)
  ✗ ResponseAssessment: 3-5 additional assessments per patient (serial monitoring)
  ✗ ClinicalAssessment: 5-7 additional visits per patient (follow-up labs/ECOG)
  ✗ Mutation (optional): Acquired resistance mutations at progression timepoints

RECOMMENDATION:
Create 4 time-series CSV files:
  1. imaging_studies_timeseries.csv (3-5 rows per patient × 5 patients = 15-25 rows)
  2. treatments_timeseries.csv (1-2 rows per patient × 5 patients = 5-10 rows)
  3. response_assessments_timeseries.csv (3-5 rows per patient × 5 patients = 15-25 rows)
  4. clinical_assessments_timeseries.csv (5-7 rows per patient × 5 patients = 25-35 rows)

Total mock rows to generate: ~60-95 rows across 4 files
""")