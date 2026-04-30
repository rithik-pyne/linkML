#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate time-series mock data for 5 patients.
Creates 4 CSV files with realistic clinical trajectories.
"""

import csv
from datetime import datetime, timedelta
from pathlib import Path

# Output directory
output_dir = Path(__file__).parent.parent / "example_files" / "mock_simulated"
output_dir.mkdir(exist_ok=True, parents=True)

# Patient baseline data (from mapping analysis)
patients_baseline = {
    'NGDX-001': {
        'diagnosis_date': '2020-03-23',
        'baseline_scan_date': '2020-03-30',
        'ttp_months': 28.2,
        'has_progression': True,
        'progression_type': 'Systemic_multi-site',
        'stage': 'IA1',
        'baseline_tumor_mm': 15.6,
        'baseline_recist_mm': 40.7,
        'adjuvant_therapy': 'Osimertinib_80mg_OD',
        'baseline_ecog': 0,
        'baseline_wbc': 4.5,
        'baseline_hgb': 157,
        'baseline_plt': 285,
        'baseline_egfr': 113,
        'baseline_alt': 46,
        'baseline_ast': 25,
    },
    'NGDX-002': {
        'diagnosis_date': '2023-04-04',
        'baseline_scan_date': '2023-04-16',
        'ttp_months': 16.2,
        'has_progression': False,
        'progression_type': 'Not_applicable',
        'stage': 'IA3',
        'baseline_tumor_mm': 17.8,
        'baseline_recist_mm': 102.6,
        'adjuvant_therapy': 'Platinum_doublet_chemotherapy',
        'baseline_ecog': 1,
        'baseline_wbc': 6.5,
        'baseline_hgb': 134,
        'baseline_plt': 173,
        'baseline_egfr': 49,
        'baseline_alt': 53,
        'baseline_ast': 37,
    },
    'NGDX-003': {
        'diagnosis_date': '2020-06-25',
        'baseline_scan_date': '2020-06-26',
        'ttp_months': 18.9,
        'has_progression': False,
        'progression_type': 'Not_applicable',
        'stage': 'IA1',
        'baseline_tumor_mm': 21,
        'baseline_recist_mm': 57.7,
        'adjuvant_therapy': None,
        'baseline_ecog': 1,
        'baseline_wbc': 10.7,
        'baseline_hgb': 126,
        'baseline_plt': 220,
        'baseline_egfr': 93,
        'baseline_alt': 37,
        'baseline_ast': 28,
    },
    'NGDX-004': {
        'diagnosis_date': '2020-03-05',
        'baseline_scan_date': '2020-03-12',
        'ttp_months': 10.2,
        'has_progression': False,
        'progression_type': 'Not_applicable',
        'stage': 'IB',
        'baseline_tumor_mm': 27,
        'baseline_recist_mm': 89.4,
        'adjuvant_therapy': None,
        'baseline_ecog': 0,
        'baseline_wbc': 6.1,
        'baseline_hgb': 142,
        'baseline_plt': 266,
        'baseline_egfr': 98,
        'baseline_alt': 34,
        'baseline_ast': 29,
    },
    'NGDX-005': {
        'diagnosis_date': '2020-03-05',
        'baseline_scan_date': '2020-03-12',
        'ttp_months': 25.7,
        'has_progression': False,
        'progression_type': 'Not_applicable',
        'stage': 'IA3',
        'baseline_tumor_mm': 21.6,
        'baseline_recist_mm': 70.8,
        'adjuvant_therapy': 'Platinum_doublet_chemotherapy',
        'baseline_ecog': 0,
        'baseline_wbc': 5.7,
        'baseline_hgb': 117,
        'baseline_plt': 238,
        'baseline_egfr': 84,
        'baseline_alt': 19,
        'baseline_ast': 24,
    }
}

# Helper function to add months to date
def add_months(date_str, months):
    dt = datetime.strptime(date_str, '%Y-%m-%d')
    # Approximate: 30.44 days per month
    new_dt = dt + timedelta(days=int(months * 30.44))
    return new_dt.strftime('%Y-%m-%d')

# =============================================================================
# 1. IMAGING STUDIES TIME-SERIES
# =============================================================================
print("Generating imaging_studies_timeseries.csv...")

imaging_data = []
for pid, data in patients_baseline.items():
    baseline_date = datetime.strptime(data['baseline_scan_date'], '%Y-%m-%d')

    # Scan 1: Baseline (already in main CSV, but include for completeness)
    # imaging_data.append({
    #     'patient_id': pid,
    #     'imaging_study_id': f'IMG-{pid}-001',
    #     'scan_date': data['baseline_scan_date'],
    #     'imaging_modality': 'CT',
    #     't_stage': 'T2a' if pid in ['NGDX-001', 'NGDX-002'] else 'T1a',
    #     'n_stage': 'N0',
    #     'm_stage': 'M0',
    #     'ajcc_stage': data['stage'],
    #     'primary_tumor_diameter_mm': data['baseline_tumor_mm'],
    #     'suv_max': 2.3 if pid == 'NGDX-001' else 5.0,
    #     'brain_metastasis_present': 'FALSE',
    #     'brain_lesion_count': 0,
    #     'study_uid': f'1.3.6.1.4.1.14519.5.2.1.{hash(pid) % 10000}.{hash(data["baseline_scan_date"]) % 10000}',
    #     'accession_number': f'ACC{data["baseline_scan_date"].replace("-", "")}',
    # })

    # Scan 2: Post-surgery (1 month) - Complete resection
    scan2_date = add_months(data['baseline_scan_date'], 1)
    imaging_data.append({
        'patient_id': pid,
        'imaging_study_id': f'IMG-{pid}-002',
        'scan_date': scan2_date,
        'imaging_modality': 'CT',
        't_stage': 'T0',
        'n_stage': 'N0',
        'm_stage': 'M0',
        'ajcc_stage': 'CR',
        'primary_tumor_diameter_mm': 0,
        'suv_max': '',
        'brain_metastasis_present': 'FALSE',
        'brain_lesion_count': 0,
        'study_uid': f'1.3.6.1.4.1.14519.5.2.1.{hash(pid) % 10000}.{hash(scan2_date) % 10000}',
        'accession_number': f'ACC{scan2_date.replace("-", "")}',
    })

    # Scan 3: 6-month follow-up - Remission
    scan3_date = add_months(data['baseline_scan_date'], 6)
    imaging_data.append({
        'patient_id': pid,
        'imaging_study_id': f'IMG-{pid}-003',
        'scan_date': scan3_date,
        'imaging_modality': 'CT',
        't_stage': 'T0',
        'n_stage': 'N0',
        'm_stage': 'M0',
        'ajcc_stage': 'CR',
        'primary_tumor_diameter_mm': 0,
        'suv_max': '',
        'brain_metastasis_present': 'FALSE',
        'brain_lesion_count': 0,
        'study_uid': f'1.3.6.1.4.1.14519.5.2.1.{hash(pid) % 10000}.{hash(scan3_date) % 10000}',
        'accession_number': f'ACC{scan3_date.replace("-", "")}',
    })

    # Scan 4: 12-month follow-up - Remission
    scan4_date = add_months(data['baseline_scan_date'], 12)
    imaging_data.append({
        'patient_id': pid,
        'imaging_study_id': f'IMG-{pid}-004',
        'scan_date': scan4_date,
        'imaging_modality': 'PET',
        't_stage': 'T0',
        'n_stage': 'N0',
        'm_stage': 'M0',
        'ajcc_stage': 'CR',
        'primary_tumor_diameter_mm': 0,
        'suv_max': 1.2,
        'brain_metastasis_present': 'FALSE',
        'brain_lesion_count': 0,
        'study_uid': f'1.3.6.1.4.1.14519.5.2.1.{hash(pid) % 10000}.{hash(scan4_date) % 10000}',
        'accession_number': f'ACC{scan4_date.replace("-", "")}',
    })

    # Scan 5: Progression scan (if applicable)
    if data['has_progression']:
        scan5_date = add_months(data['baseline_scan_date'], data['ttp_months'])
        imaging_data.append({
            'patient_id': pid,
            'imaging_study_id': f'IMG-{pid}-005',
            'scan_date': scan5_date,
            'imaging_modality': 'PET',
            't_stage': 'T2b',
            'n_stage': 'N2',
            'm_stage': 'M1b',
            'ajcc_stage': 'IVB',
            'primary_tumor_diameter_mm': 35.0,
            'suv_max': 8.9,
            'brain_metastasis_present': 'TRUE',
            'brain_lesion_count': 3,
            'study_uid': f'1.3.6.1.4.1.14519.5.2.1.{hash(pid) % 10000}.{hash(scan5_date) % 10000}',
            'accession_number': f'ACC{scan5_date.replace("-", "")}',
        })
    else:
        # Final follow-up scan at TTP (still in remission)
        scan5_date = add_months(data['baseline_scan_date'], min(data['ttp_months'], 18))
        imaging_data.append({
            'patient_id': pid,
            'imaging_study_id': f'IMG-{pid}-005',
            'scan_date': scan5_date,
            'imaging_modality': 'CT',
            't_stage': 'T0',
            'n_stage': 'N0',
            'm_stage': 'M0',
            'ajcc_stage': 'CR',
            'primary_tumor_diameter_mm': 0,
            'suv_max': '',
            'brain_metastasis_present': 'FALSE',
            'brain_lesion_count': 0,
            'study_uid': f'1.3.6.1.4.1.14519.5.2.1.{hash(pid) % 10000}.{hash(scan5_date) % 10000}',
            'accession_number': f'ACC{scan5_date.replace("-", "")}',
        })

# Write imaging CSV
imaging_csv_path = output_dir / 'imaging_studies_timeseries.csv'
with open(imaging_csv_path, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['patient_id', 'imaging_study_id', 'scan_date', 'imaging_modality',
                  't_stage', 'n_stage', 'm_stage', 'ajcc_stage', 'primary_tumor_diameter_mm',
                  'suv_max', 'brain_metastasis_present', 'brain_lesion_count',
                  'study_uid', 'accession_number']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(imaging_data)

print(f"[OK] Created {imaging_csv_path} ({len(imaging_data)} rows)")

# =============================================================================
# 2. TREATMENTS TIME-SERIES
# =============================================================================
print("Generating treatments_timeseries.csv...")

treatments_data = []
for pid, data in patients_baseline.items():
    surgery_date = add_months(data['diagnosis_date'], 0.5)  # Surgery ~2 weeks after diagnosis

    # Treatment 1: Surgery (already in main CSV, but include for reference)
    # treatments_data.append({
    #     'patient_id': pid,
    #     'treatment_id': f'TX-{pid}-001',
    #     'treatment_line': 0,
    #     'treatment_intent': 'Curative_definitive',
    #     'drug_name': 'Surgical_resection',
    #     'drug_dose_mg': '',
    #     'drug_frequency': '',
    #     'drug_route': 'Surgical',
    #     'treatment_start_date': surgery_date,
    #     'treatment_end_date': surgery_date,
    #     'discontinuation_reason': '',
    #     'mdt_recommendation': f'Surgery followed by {data["adjuvant_therapy"]}' if data['adjuvant_therapy'] else 'Surgery only',
    # })

    # Treatment 2: Adjuvant therapy (if applicable)
    if data['adjuvant_therapy']:
        adjuvant_start = add_months(surgery_date, 1)  # Start 1 month post-surgery

        if 'Osimertinib' in data['adjuvant_therapy']:
            drug = 'Osimertinib'
            dose = 80
            freq = 'OD'
        elif 'Platinum' in data['adjuvant_therapy']:
            drug = 'Carboplatin_Pemetrexed'
            dose = ''
            freq = 'q3w'
        else:
            drug = data['adjuvant_therapy']
            dose = ''
            freq = ''

        # If progression, adjuvant ends at progression; otherwise ongoing or completed
        if data['has_progression']:
            adjuvant_end = add_months(data['baseline_scan_date'], data['ttp_months'])
            disc_reason = 'Progression'
        else:
            adjuvant_end = add_months(adjuvant_start, 12)  # Standard 1-year adjuvant
            disc_reason = 'Treatment_completion'

        treatments_data.append({
            'patient_id': pid,
            'treatment_id': f'TX-{pid}-002',
            'treatment_line': 1,
            'treatment_intent': 'Adjuvant',
            'drug_name': drug,
            'drug_dose_mg': dose,
            'drug_frequency': freq,
            'drug_route': 'Oral' if 'Osimertinib' in drug else 'IV',
            'treatment_start_date': adjuvant_start,
            'treatment_end_date': adjuvant_end,
            'discontinuation_reason': disc_reason,
            'mdt_recommendation': f'Continue {drug} as adjuvant therapy',
        })

    # Treatment 3: Second-line therapy (if progression occurred)
    if data['has_progression']:
        second_line_start = add_months(data['baseline_scan_date'], data['ttp_months'] + 0.5)
        second_line_end = add_months(second_line_start, 6)  # Assume 6-month second-line

        treatments_data.append({
            'patient_id': pid,
            'treatment_id': f'TX-{pid}-003',
            'treatment_line': 2,
            'treatment_intent': 'Palliative',
            'drug_name': 'Osimertinib_plus_Savolitinib',  # MET inhibitor combo
            'drug_dose_mg': '80 + 600',
            'drug_frequency': 'OD',
            'drug_route': 'Oral',
            'treatment_start_date': second_line_start,
            'treatment_end_date': second_line_end,
            'discontinuation_reason': 'Ongoing',
            'mdt_recommendation': 'Clinical trial: Osimertinib + MET inhibitor for T790M + MET amp resistance',
        })

# Write treatments CSV
treatments_csv_path = output_dir / 'treatments_timeseries.csv'
with open(treatments_csv_path, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['patient_id', 'treatment_id', 'treatment_line', 'treatment_intent',
                  'drug_name', 'drug_dose_mg', 'drug_frequency', 'drug_route',
                  'treatment_start_date', 'treatment_end_date', 'discontinuation_reason',
                  'mdt_recommendation']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(treatments_data)

print(f"[OK] Created {treatments_csv_path} ({len(treatments_data)} rows)")

# =============================================================================
# 3. RESPONSE ASSESSMENTS TIME-SERIES
# =============================================================================
print("Generating response_assessments_timeseries.csv...")

response_data = []
for pid, data in patients_baseline.items():
    # Assessment 1: Baseline (from Var_092)
    # response_data.append({
    #     'patient_id': pid,
    #     'assessment_id': f'ASSESS-{pid}-001',
    #     'treatment_id': f'TX-{pid}-001',
    #     'imaging_study_id': f'IMG-{pid}-001',
    #     'molecular_test_id': f'NGS-{pid}-002',  # Baseline ctDNA
    #     'assessment_date': data['baseline_scan_date'],
    #     'assessment_type': 'Baseline',
    #     'recist_response': 'Not_assessed',
    #     'sum_target_lesions_mm': data['baseline_recist_mm'],
    #     'percent_change_from_baseline': 0,
    #     'new_lesions_present': 'FALSE',
    #     'ctdna_vaf_percent': 2.17 if pid == 'NGDX-001' else 4.0,
    #     'ctdna_mutation_cleared': 'FALSE',
    #     'ecog_status': data['baseline_ecog'],
    #     'progression_detected': 'FALSE',
    # })

    # Assessment 2: Post-surgery (1 month)
    assess2_date = add_months(data['baseline_scan_date'], 1)
    response_data.append({
        'patient_id': pid,
        'assessment_id': f'ASSESS-{pid}-002',
        'treatment_id': f'TX-{pid}-002' if data['adjuvant_therapy'] else f'TX-{pid}-001',
        'imaging_study_id': f'IMG-{pid}-002',
        'molecular_test_id': '',
        'assessment_date': assess2_date,
        'assessment_type': 'Post_surgery',
        'recist_response': 'CR',
        'sum_target_lesions_mm': 0,
        'percent_change_from_baseline': -100,
        'new_lesions_present': 'FALSE',
        'ctdna_vaf_percent': 0.08,  # MRD level
        'ctdna_mutation_cleared': 'FALSE',
        'ecog_status': data['baseline_ecog'],
        'progression_detected': 'FALSE',
        'progression_type': '',
        'resistance_mutation_detected': 'FALSE',
    })

    # Assessment 3: 6-month follow-up
    assess3_date = add_months(data['baseline_scan_date'], 6)
    response_data.append({
        'patient_id': pid,
        'assessment_id': f'ASSESS-{pid}-003',
        'treatment_id': f'TX-{pid}-002' if data['adjuvant_therapy'] else f'TX-{pid}-001',
        'imaging_study_id': f'IMG-{pid}-003',
        'molecular_test_id': '',
        'assessment_date': assess3_date,
        'assessment_type': 'Follow_up',
        'recist_response': 'CR',
        'sum_target_lesions_mm': 0,
        'percent_change_from_baseline': -100,
        'new_lesions_present': 'FALSE',
        'ctdna_vaf_percent': 0.02,  # Decreasing MRD
        'ctdna_mutation_cleared': 'FALSE',
        'ecog_status': 0,
        'progression_detected': 'FALSE',
        'progression_type': '',
        'resistance_mutation_detected': 'FALSE',
    })

    # Assessment 4: 12-month follow-up
    assess4_date = add_months(data['baseline_scan_date'], 12)
    response_data.append({
        'patient_id': pid,
        'assessment_id': f'ASSESS-{pid}-004',
        'treatment_id': f'TX-{pid}-002' if data['adjuvant_therapy'] else f'TX-{pid}-001',
        'imaging_study_id': f'IMG-{pid}-004',
        'molecular_test_id': '',
        'assessment_date': assess4_date,
        'assessment_type': 'Follow_up',
        'recist_response': 'CR',
        'sum_target_lesions_mm': 0,
        'percent_change_from_baseline': -100,
        'new_lesions_present': 'FALSE',
        'ctdna_vaf_percent': 0.0,  # Cleared
        'ctdna_mutation_cleared': 'TRUE',
        'ecog_status': 0,
        'progression_detected': 'FALSE',
        'progression_type': '',
        'resistance_mutation_detected': 'FALSE',
    })

    # Assessment 5: Progression (if applicable)
    if data['has_progression']:
        assess5_date = add_months(data['baseline_scan_date'], data['ttp_months'])
        response_data.append({
            'patient_id': pid,
            'assessment_id': f'ASSESS-{pid}-005',
            'treatment_id': f'TX-{pid}-002' if data['adjuvant_therapy'] else f'TX-{pid}-001',
            'imaging_study_id': f'IMG-{pid}-005',
            'molecular_test_id': f'NGS-{pid}-003',  # Progression ctDNA test
            'assessment_date': assess5_date,
            'assessment_type': 'Progression',
            'recist_response': 'PD',
            'sum_target_lesions_mm': 35.0,
            'percent_change_from_baseline': -13.7,  # Still below baseline but progressing
            'new_lesions_present': 'TRUE',
            'ctdna_vaf_percent': 12.4,  # Rising VAF
            'ctdna_mutation_cleared': 'FALSE',
            'ecog_status': 1,
            'progression_detected': 'TRUE',
            'progression_type': data['progression_type'],
            'resistance_mutation_detected': 'TRUE',
            'resistance_mechanism': 'T790M + MET_amplification',
        })
    else:
        # Final assessment at TTP (still in remission)
        assess5_date = add_months(data['baseline_scan_date'], min(data['ttp_months'], 18))
        response_data.append({
            'patient_id': pid,
            'assessment_id': f'ASSESS-{pid}-005',
            'treatment_id': f'TX-{pid}-002' if data['adjuvant_therapy'] else f'TX-{pid}-001',
            'imaging_study_id': f'IMG-{pid}-005',
            'molecular_test_id': '',
            'assessment_date': assess5_date,
            'assessment_type': 'Follow_up',
            'recist_response': 'CR',
            'sum_target_lesions_mm': 0,
            'percent_change_from_baseline': -100,
            'new_lesions_present': 'FALSE',
            'ctdna_vaf_percent': 0.0,
            'ctdna_mutation_cleared': 'TRUE',
            'ecog_status': 0,
            'progression_detected': 'FALSE',
            'progression_type': '',
            'resistance_mutation_detected': 'FALSE',
        })

# Write response assessments CSV
response_csv_path = output_dir / 'response_assessments_timeseries.csv'
with open(response_csv_path, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['patient_id', 'assessment_id', 'treatment_id', 'imaging_study_id',
                  'molecular_test_id', 'assessment_date', 'assessment_type', 'recist_response',
                  'sum_target_lesions_mm', 'percent_change_from_baseline', 'new_lesions_present',
                  'ctdna_vaf_percent', 'ctdna_mutation_cleared', 'ecog_status',
                  'progression_detected', 'progression_type', 'resistance_mutation_detected',
                  'resistance_mechanism']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(response_data)

print(f"[OK] Created {response_csv_path} ({len(response_data)} rows)")

# =============================================================================
# 4. CLINICAL ASSESSMENTS TIME-SERIES
# =============================================================================
print("Generating clinical_assessments_timeseries.csv...")

clinical_data = []
for pid, data in patients_baseline.items():
    # Assessment 1: Baseline (from main CSV)
    # clinical_data.append({
    #     'patient_id': pid,
    #     'clinical_assessment_id': f'CLIN-{pid}-001',
    #     'assessment_date': data['diagnosis_date'],
    #     'visit_type': 'Baseline',
    #     'ecog_status': data['baseline_ecog'],
    #     'wbc': data['baseline_wbc'],
    #     'hemoglobin': data['baseline_hgb'],
    #     'platelets': data['baseline_plt'],
    #     'egfr_value': data['baseline_egfr'],
    #     'alt': data['baseline_alt'],
    #     'ast': data['baseline_ast'],
    # })

    # Assessment 2: Post-surgery (1 month)
    clin2_date = add_months(data['diagnosis_date'], 1)
    clinical_data.append({
        'patient_id': pid,
        'clinical_assessment_id': f'CLIN-{pid}-002',
        'assessment_date': clin2_date,
        'visit_type': 'Post_surgery',
        'ecog_status': data['baseline_ecog'],
        'wbc': round(data['baseline_wbc'] * 0.9, 1),  # Slight decrease post-surgery
        'hemoglobin': round(data['baseline_hgb'] * 0.95, 0),
        'platelets': round(data['baseline_plt'] * 0.9, 0),
        'egfr_value': data['baseline_egfr'],
        'alt': data['baseline_alt'],
        'ast': data['baseline_ast'],
    })

    # Assessment 3: 3-month follow-up
    clin3_date = add_months(data['diagnosis_date'], 3)
    clinical_data.append({
        'patient_id': pid,
        'clinical_assessment_id': f'CLIN-{pid}-003',
        'assessment_date': clin3_date,
        'visit_type': 'Follow_up',
        'ecog_status': 0,
        'wbc': data['baseline_wbc'],
        'hemoglobin': data['baseline_hgb'],
        'platelets': data['baseline_plt'],
        'egfr_value': data['baseline_egfr'],
        'alt': data['baseline_alt'],
        'ast': data['baseline_ast'],
    })

    # Assessment 4: 6-month follow-up
    clin4_date = add_months(data['diagnosis_date'], 6)
    clinical_data.append({
        'patient_id': pid,
        'clinical_assessment_id': f'CLIN-{pid}-004',
        'assessment_date': clin4_date,
        'visit_type': 'Follow_up',
        'ecog_status': 0,
        'wbc': data['baseline_wbc'],
        'hemoglobin': data['baseline_hgb'],
        'platelets': data['baseline_plt'],
        'egfr_value': data['baseline_egfr'],
        'alt': data['baseline_alt'],
        'ast': data['baseline_ast'],
    })

    # Assessment 5: 9-month follow-up
    clin5_date = add_months(data['diagnosis_date'], 9)
    clinical_data.append({
        'patient_id': pid,
        'clinical_assessment_id': f'CLIN-{pid}-005',
        'assessment_date': clin5_date,
        'visit_type': 'Follow_up',
        'ecog_status': 0,
        'wbc': data['baseline_wbc'],
        'hemoglobin': data['baseline_hgb'],
        'platelets': data['baseline_plt'],
        'egfr_value': data['baseline_egfr'],
        'alt': round(data['baseline_alt'] * 1.1, 0),  # Slight ALT increase on TKI
        'ast': data['baseline_ast'],
    })

    # Assessment 6: 12-month follow-up
    clin6_date = add_months(data['diagnosis_date'], 12)
    clinical_data.append({
        'patient_id': pid,
        'clinical_assessment_id': f'CLIN-{pid}-006',
        'assessment_date': clin6_date,
        'visit_type': 'Follow_up',
        'ecog_status': 0,
        'wbc': data['baseline_wbc'],
        'hemoglobin': data['baseline_hgb'],
        'platelets': data['baseline_plt'],
        'egfr_value': data['baseline_egfr'],
        'alt': round(data['baseline_alt'] * 1.15, 0),
        'ast': data['baseline_ast'],
    })

    # Assessment 7: 18-month follow-up (if TTP > 18 months)
    if data['ttp_months'] > 18:
        clin7_date = add_months(data['diagnosis_date'], 18)
        clinical_data.append({
            'patient_id': pid,
            'clinical_assessment_id': f'CLIN-{pid}-007',
            'assessment_date': clin7_date,
            'visit_type': 'Follow_up',
            'ecog_status': 0,
            'wbc': data['baseline_wbc'],
            'hemoglobin': data['baseline_hgb'],
            'platelets': data['baseline_plt'],
            'egfr_value': data['baseline_egfr'],
            'alt': round(data['baseline_alt'] * 1.2, 0),
            'ast': data['baseline_ast'],
        })

    # Assessment 8: Progression visit (if applicable)
    if data['has_progression']:
        clin8_date = add_months(data['diagnosis_date'], data['ttp_months'])
        clinical_data.append({
            'patient_id': pid,
            'clinical_assessment_id': f'CLIN-{pid}-008',
            'assessment_date': clin8_date,
            'visit_type': 'Progression',
            'ecog_status': 1,
            'wbc': round(data['baseline_wbc'] * 1.2, 1),
            'hemoglobin': round(data['baseline_hgb'] * 0.9, 0),
            'platelets': round(data['baseline_plt'] * 1.1, 0),
            'egfr_value': data['baseline_egfr'],
            'alt': round(data['baseline_alt'] * 1.3, 0),
            'ast': round(data['baseline_ast'] * 1.2, 0),
        })

# Write clinical assessments CSV
clinical_csv_path = output_dir / 'clinical_assessments_timeseries.csv'
with open(clinical_csv_path, 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['patient_id', 'clinical_assessment_id', 'assessment_date', 'visit_type',
                  'ecog_status', 'wbc', 'hemoglobin', 'platelets', 'egfr_value', 'alt', 'ast']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(clinical_data)

print(f"[OK] Created {clinical_csv_path} ({len(clinical_data)} rows)")

# =============================================================================
# SUMMARY
# =============================================================================
print("\n" + "=" * 80)
print("TIME-SERIES DATA GENERATION COMPLETE")
print("=" * 80)
print(f"Total files created: 4")
print(f"  - imaging_studies_timeseries.csv: {len(imaging_data)} rows")
print(f"  - treatments_timeseries.csv: {len(treatments_data)} rows")
print(f"  - response_assessments_timeseries.csv: {len(response_data)} rows")
print(f"  - clinical_assessments_timeseries.csv: {len(clinical_data)} rows")
print(f"\nTotal rows generated: {len(imaging_data) + len(treatments_data) + len(response_data) + len(clinical_data)}")
print(f"\nAll files saved to: {output_dir}")
print("\nNext step: Create database population script to load all data into SQLite")