-- # Class: Patient Description: Core patient entity with demographics and baseline clinical data
--     * Slot: patient_id
--     * Slot: nhs_number
--     * Slot: age_at_diagnosis
--     * Slot: sex
--     * Slot: ethnicity_code
--     * Slot: smoking_status
--     * Slot: pack_years
--     * Slot: family_history_lung_cancer
--     * Slot: ecog_baseline
--     * Slot: baseline_egfr
--     * Slot: baseline_wbc
--     * Slot: baseline_hemoglobin
--     * Slot: baseline_platelets
--     * Slot: baseline_alt
--     * Slot: baseline_ast
--     * Slot: diagnosis_date
--     * Slot: diagnosis_pathway
-- # Class: Biopsy Description: Tissue or liquid biopsy procedure - multiple rows per patient
--     * Slot: biopsy_id
--     * Slot: patient_id
--     * Slot: biopsy_date
--     * Slot: specimen_type
--     * Slot: biopsy_technique
--     * Slot: biopsy_site_snomed
--     * Slot: biopsy_site_description
--     * Slot: tissue_specimen_category
--     * Slot: tissue_preparation_format
--     * Slot: tissue_fixation_hours
--     * Slot: tumor_cellularity_percent
--     * Slot: necrosis_percent
--     * Slot: pathology_slide_image_path
--     * Slot: pathology_report_pdf_path
--     * Slot: blood_tube_type
--     * Slot: blood_collection_volume_ml
--     * Slot: blood_draw_timestamp
--     * Slot: time_to_fractionation_hours
--     * Slot: plasma_volume_ml
--     * Slot: cfdna_concentration_ng_ul
--     * Slot: cfdna_total_yield_ng
--     * Slot: histologic_subtype
--     * Slot: pdl1_tps_percent
--     * Slot: pdl1_antibody_clone
--     * Slot: specimen_adequacy
--     * Slot: tissue_sufficiency
-- # Class: MolecularTest Description: NGS test from tissue or ctDNA - multiple rows per patient
--     * Slot: molecular_test_id
--     * Slot: biopsy_id
--     * Slot: test_date
--     * Slot: specimen_source
--     * Slot: ngs_panel_name
--     * Slot: ngs_panel_version
--     * Slot: ngs_assay_type
--     * Slot: dna_input_mass_ng
--     * Slot: mean_coverage_depth
--     * Slot: assay_lod_percent
--     * Slot: ngs_report_pdf_path
--     * Slot: vcf_file_path
-- # Class: Mutation Description: Individual genomic variant detected in NGS test - normalized to enable time-series tracking
--     * Slot: mutation_id
--     * Slot: molecular_test_id
--     * Slot: gene_symbol
--     * Slot: mutation_hgvs
--     * Slot: mutation_type
--     * Slot: mutation_classification
--     * Slot: vaf_percent
--     * Slot: tumor_fraction_percent
--     * Slot: actionable_mutation
--     * Slot: resistance_mutation
--     * Slot: chip_status
--     * Slot: is_primary_driver
--     * Slot: is_acquired_resistance
--     * Slot: detection_timepoint
-- # Class: Treatment Description: Treatment line with drug regimen and duration - multiple rows per patient
--     * Slot: treatment_id
--     * Slot: patient_id
--     * Slot: treatment_line
--     * Slot: treatment_intent
--     * Slot: drug_name
--     * Slot: drug_dose_mg
--     * Slot: drug_frequency
--     * Slot: drug_route
--     * Slot: treatment_start_date
--     * Slot: treatment_end_date
--     * Slot: mdt_recommendation
--     * Slot: mdt_date
--     * Slot: prior_ici_exposure
--     * Slot: months_since_last_ici
--     * Slot: discontinuation_reason
-- # Class: ImagingResponse Description: Treatment response assessment based on imaging studies (RECIST criteria). Grain - one row per imaging study with documented radiologist assessment.
--     * Slot: imaging_response_id Description: Primary key for ImagingResponse. Format - IR-{patient_num}-{counter} e.g. IR-001-001
--     * Slot: imaging_study_id Description: Source imaging study (REQUIRED - establishes lineage)
--     * Slot: patient_id Description: Conformed dimension for drill-across queries
--     * Slot: treatment_id Description: Treatment context (NULL for pre-treatment baseline)
--     * Slot: assessment_date
--     * Slot: assessment_type
--     * Slot: recist_response
--     * Slot: sum_target_lesions_mm
--     * Slot: percent_change_from_baseline
--     * Slot: new_lesions_present
-- # Class: MolecularResponse Description: Treatment response assessment based on molecular testing (ctDNA/VAF tracking). Grain - one row per molecular test with documented ctDNA response.
--     * Slot: molecular_response_id Description: Primary key for MolecularResponse. Format - MR-{patient_num}-{counter} e.g. MR-001-001
--     * Slot: molecular_test_id Description: Source molecular test (REQUIRED - establishes lineage)
--     * Slot: patient_id Description: Conformed dimension for drill-across queries
--     * Slot: treatment_id Description: Treatment context (NULL for pre-treatment baseline)
--     * Slot: assessment_date
--     * Slot: assessment_type
--     * Slot: ctdna_vaf_percent
--     * Slot: ctdna_tumor_fraction_percent
--     * Slot: ctdna_mutation_cleared
-- # Class: ClinicalResponse Description: Clinical outcome events (progression, resistance, histologic transformation). Grain - one row per documented clinical outcome event. Does NOT link to specific imaging/molecular tests - represents MDT consensus.
--     * Slot: clinical_response_id Description: Primary key for ClinicalResponse. Format - CR-{patient_num}-{counter} e.g. CR-001-001
--     * Slot: patient_id Description: Conformed dimension for drill-across queries
--     * Slot: treatment_id Description: Treatment context (may be post-treatment)
--     * Slot: event_date Description: Date event was documented (may differ from test date)
--     * Slot: event_type Description: Type of clinical event (Progression, Resistance, Transformation)
--     * Slot: progression_detected
--     * Slot: progression_type
--     * Slot: time_to_progression_months
--     * Slot: resistance_mutation_detected
--     * Slot: resistance_mechanism
--     * Slot: histologic_transformation
-- # Class: ClinicalAssessment Description: Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patient
--     * Slot: clinical_assessment_id
--     * Slot: patient_id
--     * Slot: assessment_date
--     * Slot: visit_type
--     * Slot: ecog_status
--     * Slot: symptoms_coded
--     * Slot: symptom_severity_grade
--     * Slot: wbc
--     * Slot: hemoglobin
--     * Slot: platelets
--     * Slot: neutrophils
--     * Slot: egfr_value
--     * Slot: alt
--     * Slot: ast
-- # Class: ImagingStudy Description: Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient
--     * Slot: imaging_study_id
--     * Slot: patient_id
--     * Slot: study_uid
--     * Slot: series_uid
--     * Slot: accession_number
--     * Slot: scan_date
--     * Slot: imaging_modality
--     * Slot: study_description
--     * Slot: dicom_file_path
--     * Slot: thumbnail_image_path
--     * Slot: ct_kvp
--     * Slot: ct_mas
--     * Slot: ct_slice_thickness_mm
--     * Slot: pet_tracer
--     * Slot: pet_injected_dose_mbq
--     * Slot: pet_uptake_time_min
--     * Slot: t_stage
--     * Slot: n_stage
--     * Slot: m_stage
--     * Slot: m_sites
--     * Slot: ajcc_stage
--     * Slot: primary_tumor_diameter_mm
--     * Slot: suv_max
--     * Slot: brain_metastasis_present
--     * Slot: brain_lesion_count
--     * Slot: brain_largest_lesion_mm

CREATE TABLE "Patient" (
	patient_id TEXT NOT NULL,
	nhs_number TEXT NOT NULL,
	age_at_diagnosis INTEGER,
	sex VARCHAR(13),
	ethnicity_code TEXT,
	smoking_status VARCHAR(26),
	pack_years FLOAT,
	family_history_lung_cancer BOOLEAN,
	ecog_baseline INTEGER,
	baseline_egfr FLOAT,
	baseline_wbc FLOAT,
	baseline_hemoglobin FLOAT,
	baseline_platelets FLOAT,
	baseline_alt FLOAT,
	baseline_ast FLOAT,
	diagnosis_date DATE NOT NULL,
	diagnosis_pathway TEXT,
	PRIMARY KEY (patient_id)
);
CREATE INDEX "ix_Patient_patient_id" ON "Patient" (patient_id);

CREATE TABLE "Biopsy" (
	biopsy_id TEXT NOT NULL,
	patient_id TEXT NOT NULL,
	biopsy_date DATE NOT NULL,
	specimen_type VARCHAR(6),
	biopsy_technique TEXT,
	biopsy_site_snomed TEXT,
	biopsy_site_description TEXT,
	tissue_specimen_category TEXT,
	tissue_preparation_format TEXT,
	tissue_fixation_hours FLOAT,
	tumor_cellularity_percent FLOAT,
	necrosis_percent FLOAT,
	pathology_slide_image_path TEXT,
	pathology_report_pdf_path TEXT,
	blood_tube_type TEXT,
	blood_collection_volume_ml FLOAT,
	blood_draw_timestamp DATETIME,
	time_to_fractionation_hours FLOAT,
	plasma_volume_ml FLOAT,
	cfdna_concentration_ng_ul FLOAT,
	cfdna_total_yield_ng FLOAT,
	histologic_subtype TEXT,
	pdl1_tps_percent INTEGER,
	pdl1_antibody_clone TEXT,
	specimen_adequacy TEXT,
	tissue_sufficiency TEXT,
	PRIMARY KEY (biopsy_id),
	FOREIGN KEY(patient_id) REFERENCES "Patient" (patient_id)
);
CREATE INDEX "ix_Biopsy_biopsy_id" ON "Biopsy" (biopsy_id);

CREATE TABLE "Treatment" (
	treatment_id TEXT NOT NULL,
	patient_id TEXT NOT NULL,
	treatment_line INTEGER,
	treatment_intent VARCHAR(19),
	drug_name TEXT,
	drug_dose_mg FLOAT,
	drug_frequency VARCHAR(6),
	drug_route TEXT,
	treatment_start_date DATE NOT NULL,
	treatment_end_date DATE,
	mdt_recommendation TEXT,
	mdt_date DATE,
	prior_ici_exposure BOOLEAN,
	months_since_last_ici FLOAT,
	discontinuation_reason VARCHAR(20),
	PRIMARY KEY (treatment_id),
	FOREIGN KEY(patient_id) REFERENCES "Patient" (patient_id)
);
CREATE INDEX "ix_Treatment_treatment_id" ON "Treatment" (treatment_id);

CREATE TABLE "ClinicalAssessment" (
	clinical_assessment_id TEXT NOT NULL,
	patient_id TEXT NOT NULL,
	assessment_date DATE NOT NULL,
	visit_type TEXT,
	ecog_status INTEGER,
	symptoms_coded TEXT,
	symptom_severity_grade INTEGER,
	wbc FLOAT,
	hemoglobin FLOAT,
	platelets FLOAT,
	neutrophils FLOAT,
	egfr_value FLOAT,
	alt FLOAT,
	ast FLOAT,
	PRIMARY KEY (clinical_assessment_id),
	FOREIGN KEY(patient_id) REFERENCES "Patient" (patient_id)
);
CREATE INDEX "ix_ClinicalAssessment_clinical_assessment_id" ON "ClinicalAssessment" (clinical_assessment_id);

CREATE TABLE "ImagingStudy" (
	imaging_study_id TEXT NOT NULL,
	patient_id TEXT NOT NULL,
	study_uid TEXT,
	series_uid TEXT,
	accession_number TEXT,
	scan_date DATE NOT NULL,
	imaging_modality VARCHAR(2),
	study_description TEXT,
	dicom_file_path TEXT,
	thumbnail_image_path TEXT,
	ct_kvp INTEGER,
	ct_mas FLOAT,
	ct_slice_thickness_mm FLOAT,
	pet_tracer TEXT,
	pet_injected_dose_mbq FLOAT,
	pet_uptake_time_min FLOAT,
	t_stage VARCHAR(3),
	n_stage VARCHAR(2),
	m_stage VARCHAR(3),
	m_sites TEXT,
	ajcc_stage VARCHAR(7),
	primary_tumor_diameter_mm FLOAT,
	suv_max FLOAT,
	brain_metastasis_present BOOLEAN,
	brain_lesion_count INTEGER,
	brain_largest_lesion_mm FLOAT,
	PRIMARY KEY (imaging_study_id),
	FOREIGN KEY(patient_id) REFERENCES "Patient" (patient_id)
);
CREATE INDEX "ix_ImagingStudy_imaging_study_id" ON "ImagingStudy" (imaging_study_id);

CREATE TABLE "MolecularTest" (
	molecular_test_id TEXT NOT NULL,
	biopsy_id TEXT NOT NULL,
	test_date DATE NOT NULL,
	specimen_source VARCHAR(6),
	ngs_panel_name TEXT,
	ngs_panel_version TEXT,
	ngs_assay_type VARCHAR(22),
	dna_input_mass_ng FLOAT,
	mean_coverage_depth FLOAT,
	assay_lod_percent FLOAT,
	ngs_report_pdf_path TEXT,
	vcf_file_path TEXT,
	PRIMARY KEY (molecular_test_id),
	FOREIGN KEY(biopsy_id) REFERENCES "Biopsy" (biopsy_id)
);
CREATE INDEX "ix_MolecularTest_molecular_test_id" ON "MolecularTest" (molecular_test_id);

CREATE TABLE "ImagingResponse" (
	imaging_response_id TEXT NOT NULL,
	imaging_study_id TEXT NOT NULL,
	patient_id TEXT NOT NULL,
	treatment_id TEXT,
	assessment_date DATE NOT NULL,
	assessment_type VARCHAR(11) NOT NULL,
	recist_response VARCHAR(2),
	sum_target_lesions_mm FLOAT,
	percent_change_from_baseline FLOAT,
	new_lesions_present BOOLEAN,
	PRIMARY KEY (imaging_response_id),
	FOREIGN KEY(imaging_study_id) REFERENCES "ImagingStudy" (imaging_study_id),
	FOREIGN KEY(patient_id) REFERENCES "Patient" (patient_id),
	FOREIGN KEY(treatment_id) REFERENCES "Treatment" (treatment_id)
);
CREATE INDEX "ix_ImagingResponse_imaging_response_id" ON "ImagingResponse" (imaging_response_id);

CREATE TABLE "ClinicalResponse" (
	clinical_response_id TEXT NOT NULL,
	patient_id TEXT NOT NULL,
	treatment_id TEXT,
	event_date DATE NOT NULL,
	event_type VARCHAR(14) NOT NULL,
	progression_detected BOOLEAN NOT NULL,
	progression_type VARCHAR(19),
	time_to_progression_months FLOAT,
	resistance_mutation_detected BOOLEAN,
	resistance_mechanism TEXT,
	histologic_transformation BOOLEAN,
	PRIMARY KEY (clinical_response_id),
	FOREIGN KEY(patient_id) REFERENCES "Patient" (patient_id),
	FOREIGN KEY(treatment_id) REFERENCES "Treatment" (treatment_id)
);
CREATE INDEX "ix_ClinicalResponse_clinical_response_id" ON "ClinicalResponse" (clinical_response_id);

CREATE TABLE "Mutation" (
	mutation_id TEXT NOT NULL,
	molecular_test_id TEXT NOT NULL,
	gene_symbol TEXT NOT NULL,
	mutation_hgvs TEXT,
	mutation_type TEXT,
	mutation_classification VARCHAR(8),
	vaf_percent FLOAT,
	tumor_fraction_percent FLOAT,
	actionable_mutation BOOLEAN,
	resistance_mutation BOOLEAN,
	chip_status TEXT,
	is_primary_driver BOOLEAN,
	is_acquired_resistance BOOLEAN,
	detection_timepoint VARCHAR(14),
	PRIMARY KEY (mutation_id),
	FOREIGN KEY(molecular_test_id) REFERENCES "MolecularTest" (molecular_test_id)
);
CREATE INDEX "ix_Mutation_mutation_id" ON "Mutation" (mutation_id);

CREATE TABLE "MolecularResponse" (
	molecular_response_id TEXT NOT NULL,
	molecular_test_id TEXT NOT NULL,
	patient_id TEXT NOT NULL,
	treatment_id TEXT,
	assessment_date DATE NOT NULL,
	assessment_type VARCHAR(11) NOT NULL,
	ctdna_vaf_percent FLOAT,
	ctdna_tumor_fraction_percent FLOAT,
	ctdna_mutation_cleared BOOLEAN,
	PRIMARY KEY (molecular_response_id),
	FOREIGN KEY(molecular_test_id) REFERENCES "MolecularTest" (molecular_test_id),
	FOREIGN KEY(patient_id) REFERENCES "Patient" (patient_id),
	FOREIGN KEY(treatment_id) REFERENCES "Treatment" (treatment_id)
);
CREATE INDEX "ix_MolecularResponse_molecular_response_id" ON "MolecularResponse" (molecular_response_id);

