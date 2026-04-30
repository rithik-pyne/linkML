#!/usr/bin/env python3
"""Analyze simulated_data.csv to select 5 diverse patients for time-series generation"""

import csv
from pathlib import Path

# Read CSV
csv_path = Path(__file__).parent.parent / "example_files" / "simulated_data.csv"

with open(csv_path, 'r', encoding='latin-1') as f:
    reader = csv.reader(f)

    # Read first header row (has Patient_ID in first column)
    first_header = next(reader)

    # Read variable header row (has empty first column, then Var_001, Var_002, ...)
    var_headers = next(reader)

    # Merge headers: use Patient_ID from first_header[0], then var_headers[1:]
    headers = [first_header[0]] + var_headers[1:]

    # Read all patient rows
    patients = []
    for row in reader:
        if row and row[0]:  # Skip empty rows
            patient_dict = dict(zip(headers, row))
            patients.append(patient_dict)

print("=" * 150)
print(f"PATIENT ANALYSIS - Total patients: {len(patients)}")
print("=" * 150)

# Define indices for key columns
cols = {
    'id': 0,
    'age': 2,
    'sex': 3,
    'stage': 30,
    'egfr_tissue': 50,
    'egfr_ctdna': 74,
    'treatment': 86,
    'drug': 87,
    'progression': 95,
    'ttp': 99,
    'resistance': 96
}

# Analyze first 15 patients
for i in range(min(15, len(patients))):
    row = patients[i]

    # Access by header names
    pid = row.get('Patient_ID', '')
    age = row.get('Var_002_Age_at_diagnosis', '')
    sex = row.get('Var_003_Sex', '')
    stage = row.get('Var_030_Overall_AJCC_clinical_stage_Stage_IIV', '')
    egfr_tissue = row.get('Var_050_EGFR_mutation_detected__tissue_HGVS_notation', '')[:60]
    egfr_ctdna = row.get('Var_074_EGFR_mutation_detected__ctDNA_HGVS_notation', '')[:60]
    treatment = row.get('Var_086_Treatment_intent', '')
    drug = row.get('Var_087_Drug_name_dose_and_route_of_administration', '')
    if '|' in drug:
        drug = drug.split('|')[0][:40]
    else:
        drug = drug[:40]
    progression = row.get('Var_095_Progression_type_at_reassessment', '')
    ttp = row.get('Var_099_Time_from_initial_diagnosis_to_progression_months', '')
    resistance = row.get('Var_096_Resistance_mechanism_detected_HGVS_notation', '')[:40]

    print(f"\n{pid}:")
    print(f"  Age: {age}, Sex: {sex}, Stage: {stage}")
    print(f"  EGFR (tissue): {egfr_tissue}")
    print(f"  EGFR (ctDNA):  {egfr_ctdna}")
    print(f"  Treatment: {treatment}")
    print(f"  Drug: {drug}")
    print(f"  Progression: {progression} at {ttp} months")
    print(f"  Resistance: {resistance}")

print("\n" + "=" * 150)
print("RECOMMENDATIONS FOR 5-PATIENT COHORT:")
print("=" * 150)
print("""
Based on diversity of clinical trajectories, select patients with:
1. Early stage (IA/IB) with surgery
2. Advanced stage (IV) with long response duration
3. Patient with T790M resistance
4. Patient with MET amplification resistance
5. Patient with uncommon EGFR mutation

Next step: Manually select 5 patient IDs based on above output.
""")