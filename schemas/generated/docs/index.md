# NG-DX EGFR-NSCLC Clinical Data Model

Clinical data model for EGFR-mutant NSCLC diagnostic pathway

URI: https://ngdx.org/clinical_model

Name: clinical_model



## Classes

| Class | Description |
| --- | --- |
| [Biopsy](Biopsy.md) | Tissue or liquid biopsy procedure - multiple rows per patient |
| [ClinicalAssessment](ClinicalAssessment.md) | Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patie... |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |
| [MolecularTest](MolecularTest.md) | NGS test from tissue or ctDNA - multiple rows per patient |
| [Mutation](Mutation.md) | Individual genomic variant detected in NGS test - normalized to enable time-s... |
| [Patient](Patient.md) | Core patient entity with demographics and baseline clinical data |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |



## Slots

| Slot | Description |
| --- | --- |
| [accession_number](accession_number.md) |  |
| [actionable_mutation](actionable_mutation.md) |  |
| [age_at_diagnosis](age_at_diagnosis.md) |  |
| [ajcc_stage](ajcc_stage.md) |  |
| [alt](alt.md) |  |
| [assay_lod_percent](assay_lod_percent.md) |  |
| [assessment_date](assessment_date.md) |  |
| [assessment_id](assessment_id.md) |  |
| [assessment_type](assessment_type.md) |  |
| [ast](ast.md) |  |
| [baseline_alt](baseline_alt.md) |  |
| [baseline_ast](baseline_ast.md) |  |
| [baseline_egfr](baseline_egfr.md) |  |
| [baseline_hemoglobin](baseline_hemoglobin.md) |  |
| [baseline_platelets](baseline_platelets.md) |  |
| [baseline_wbc](baseline_wbc.md) |  |
| [biopsy_date](biopsy_date.md) |  |
| [biopsy_id](biopsy_id.md) |  |
| [biopsy_site_description](biopsy_site_description.md) |  |
| [biopsy_site_snomed](biopsy_site_snomed.md) |  |
| [biopsy_technique](biopsy_technique.md) |  |
| [blood_collection_volume_ml](blood_collection_volume_ml.md) |  |
| [blood_draw_timestamp](blood_draw_timestamp.md) |  |
| [blood_tube_type](blood_tube_type.md) |  |
| [brain_largest_lesion_mm](brain_largest_lesion_mm.md) |  |
| [brain_lesion_count](brain_lesion_count.md) |  |
| [brain_metastasis_present](brain_metastasis_present.md) |  |
| [cfdna_concentration_ng_ul](cfdna_concentration_ng_ul.md) |  |
| [cfdna_total_yield_ng](cfdna_total_yield_ng.md) |  |
| [chip_status](chip_status.md) |  |
| [clinical_assessment_id](clinical_assessment_id.md) |  |
| [ct_kvp](ct_kvp.md) |  |
| [ct_mas](ct_mas.md) |  |
| [ct_slice_thickness_mm](ct_slice_thickness_mm.md) |  |
| [ctdna_mutation_cleared](ctdna_mutation_cleared.md) |  |
| [ctdna_tumor_fraction_percent](ctdna_tumor_fraction_percent.md) |  |
| [ctdna_vaf_percent](ctdna_vaf_percent.md) |  |
| [detection_timepoint](detection_timepoint.md) |  |
| [diagnosis_date](diagnosis_date.md) |  |
| [diagnosis_pathway](diagnosis_pathway.md) |  |
| [dicom_file_path](dicom_file_path.md) |  |
| [discontinuation_reason](discontinuation_reason.md) |  |
| [dna_input_mass_ng](dna_input_mass_ng.md) |  |
| [drug_dose_mg](drug_dose_mg.md) |  |
| [drug_frequency](drug_frequency.md) |  |
| [drug_name](drug_name.md) |  |
| [drug_route](drug_route.md) |  |
| [ecog_baseline](ecog_baseline.md) |  |
| [ecog_status](ecog_status.md) |  |
| [egfr_value](egfr_value.md) |  |
| [ethnicity_code](ethnicity_code.md) |  |
| [family_history_lung_cancer](family_history_lung_cancer.md) |  |
| [gene_symbol](gene_symbol.md) |  |
| [hemoglobin](hemoglobin.md) |  |
| [histologic_subtype](histologic_subtype.md) |  |
| [histologic_transformation](histologic_transformation.md) |  |
| [imaging_modality](imaging_modality.md) |  |
| [imaging_study_id](imaging_study_id.md) |  |
| [is_acquired_resistance](is_acquired_resistance.md) |  |
| [is_primary_driver](is_primary_driver.md) |  |
| [m_sites](m_sites.md) |  |
| [m_stage](m_stage.md) |  |
| [mdt_date](mdt_date.md) |  |
| [mdt_recommendation](mdt_recommendation.md) |  |
| [mean_coverage_depth](mean_coverage_depth.md) |  |
| [molecular_test_id](molecular_test_id.md) |  |
| [months_since_last_ici](months_since_last_ici.md) |  |
| [mutation_classification](mutation_classification.md) |  |
| [mutation_hgvs](mutation_hgvs.md) |  |
| [mutation_id](mutation_id.md) |  |
| [mutation_type](mutation_type.md) |  |
| [n_stage](n_stage.md) |  |
| [necrosis_percent](necrosis_percent.md) |  |
| [neutrophils](neutrophils.md) |  |
| [new_lesions_present](new_lesions_present.md) |  |
| [ngs_assay_type](ngs_assay_type.md) |  |
| [ngs_panel_name](ngs_panel_name.md) |  |
| [ngs_panel_version](ngs_panel_version.md) |  |
| [ngs_report_pdf_path](ngs_report_pdf_path.md) |  |
| [nhs_number](nhs_number.md) |  |
| [pack_years](pack_years.md) |  |
| [pathology_report_pdf_path](pathology_report_pdf_path.md) |  |
| [pathology_slide_image_path](pathology_slide_image_path.md) |  |
| [patient_id](patient_id.md) |  |
| [pdl1_antibody_clone](pdl1_antibody_clone.md) |  |
| [pdl1_tps_percent](pdl1_tps_percent.md) |  |
| [percent_change_from_baseline](percent_change_from_baseline.md) |  |
| [pet_injected_dose_mbq](pet_injected_dose_mbq.md) |  |
| [pet_tracer](pet_tracer.md) |  |
| [pet_uptake_time_min](pet_uptake_time_min.md) |  |
| [plasma_volume_ml](plasma_volume_ml.md) |  |
| [platelets](platelets.md) |  |
| [primary_tumor_diameter_mm](primary_tumor_diameter_mm.md) |  |
| [prior_ici_exposure](prior_ici_exposure.md) |  |
| [progression_detected](progression_detected.md) |  |
| [progression_type](progression_type.md) |  |
| [recist_response](recist_response.md) |  |
| [resistance_mechanism](resistance_mechanism.md) |  |
| [resistance_mutation](resistance_mutation.md) |  |
| [resistance_mutation_detected](resistance_mutation_detected.md) |  |
| [scan_date](scan_date.md) |  |
| [series_uid](series_uid.md) |  |
| [sex](sex.md) |  |
| [smoking_status](smoking_status.md) |  |
| [specimen_adequacy](specimen_adequacy.md) |  |
| [specimen_source](specimen_source.md) |  |
| [specimen_type](specimen_type.md) |  |
| [study_description](study_description.md) |  |
| [study_uid](study_uid.md) |  |
| [sum_target_lesions_mm](sum_target_lesions_mm.md) |  |
| [suv_max](suv_max.md) |  |
| [symptom_improvement](symptom_improvement.md) |  |
| [symptom_severity_grade](symptom_severity_grade.md) |  |
| [symptoms_coded](symptoms_coded.md) |  |
| [t_stage](t_stage.md) |  |
| [test_date](test_date.md) |  |
| [thumbnail_image_path](thumbnail_image_path.md) |  |
| [time_to_fractionation_hours](time_to_fractionation_hours.md) |  |
| [time_to_progression_months](time_to_progression_months.md) |  |
| [tissue_fixation_hours](tissue_fixation_hours.md) |  |
| [tissue_preparation_format](tissue_preparation_format.md) |  |
| [tissue_specimen_category](tissue_specimen_category.md) |  |
| [tissue_sufficiency](tissue_sufficiency.md) |  |
| [treatment_end_date](treatment_end_date.md) |  |
| [treatment_id](treatment_id.md) |  |
| [treatment_intent](treatment_intent.md) |  |
| [treatment_line](treatment_line.md) |  |
| [treatment_start_date](treatment_start_date.md) |  |
| [tumor_cellularity_percent](tumor_cellularity_percent.md) |  |
| [tumor_fraction_percent](tumor_fraction_percent.md) |  |
| [vaf_percent](vaf_percent.md) |  |
| [vcf_file_path](vcf_file_path.md) |  |
| [visit_type](visit_type.md) |  |
| [wbc](wbc.md) |  |


## Enumerations

| Enumeration | Description |
| --- | --- |
| [AJCCStageEnum](AJCCStageEnum.md) |  |
| [AssessmentTypeEnum](AssessmentTypeEnum.md) |  |
| [DetectionTimepointEnum](DetectionTimepointEnum.md) |  |
| [DiscontinuationReasonEnum](DiscontinuationReasonEnum.md) |  |
| [DoseFrequencyEnum](DoseFrequencyEnum.md) |  |
| [ImagingModalityEnum](ImagingModalityEnum.md) |  |
| [MStageEnum](MStageEnum.md) |  |
| [NGSAssayTypeEnum](NGSAssayTypeEnum.md) |  |
| [NStageEnum](NStageEnum.md) |  |
| [ProgressionTypeEnum](ProgressionTypeEnum.md) |  |
| [RECISTResponseEnum](RECISTResponseEnum.md) |  |
| [SexEnum](SexEnum.md) |  |
| [SmokingStatusEnum](SmokingStatusEnum.md) |  |
| [SpecimenSourceEnum](SpecimenSourceEnum.md) |  |
| [SpecimenTypeEnum](SpecimenTypeEnum.md) |  |
| [TreatmentIntentEnum](TreatmentIntentEnum.md) |  |
| [TStageEnum](TStageEnum.md) |  |
| [VariantTierEnum](VariantTierEnum.md) |  |


## Types

| Type | Description |
| --- | --- |
| [Boolean](Boolean.md) | A binary (true or false) value |
| [Curie](Curie.md) | a compact URI |
| [Date](Date.md) | a date (year, month and day) in an idealized calendar |
| [DateOrDatetime](DateOrDatetime.md) | Either a date or a datetime |
| [Datetime](Datetime.md) | The combination of a date and time |
| [Decimal](Decimal.md) | A real number with arbitrary precision that conforms to the xsd:decimal speci... |
| [Double](Double.md) | A real number that conforms to the xsd:double specification |
| [Float](Float.md) | A real number that conforms to the xsd:float specification |
| [Integer](Integer.md) | An integer |
| [Jsonpath](Jsonpath.md) | A string encoding a JSON Path |
| [Jsonpointer](Jsonpointer.md) | A string encoding a JSON Pointer |
| [Ncname](Ncname.md) | Prefix part of CURIE |
| [Nodeidentifier](Nodeidentifier.md) | A URI, CURIE or BNODE that represents a node in a model |
| [Objectidentifier](Objectidentifier.md) | A URI or CURIE that represents an object in the model |
| [Sparqlpath](Sparqlpath.md) | A string encoding a SPARQL Property Path |
| [String](String.md) | A character string |
| [Time](Time.md) | A time object represents a (local) time of day, independent of any particular... |
| [Uri](Uri.md) | a complete URI |
| [Uriorcurie](Uriorcurie.md) | a URI or a CURIE |


## Subsets

| Subset | Description |
| --- | --- |
