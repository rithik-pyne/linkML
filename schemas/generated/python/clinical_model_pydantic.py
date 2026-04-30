from __future__ import annotations

import re
import sys
from datetime import (
    date,
    datetime,
    time
)
from decimal import Decimal
from enum import Enum
from typing import (
    Any,
    ClassVar,
    Literal,
    Optional,
    Union
)

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    RootModel,
    SerializationInfo,
    SerializerFunctionWrapHandler,
    field_validator,
    model_serializer
)


metamodel_version = "1.7.0"
version = "1.0.0"


class ConfiguredBaseModel(BaseModel):
    model_config = ConfigDict(
        serialize_by_alias = True,
        validate_by_name = True,
        validate_assignment = True,
        validate_default = True,
        extra = "forbid",
        arbitrary_types_allowed = True,
        use_enum_values = True,
        strict = False,
    )





class LinkMLMeta(RootModel):
    root: dict[str, Any] = {}
    model_config = ConfigDict(frozen=True)

    def __getattr__(self, key:str):
        return getattr(self.root, key)

    def __getitem__(self, key:str):
        return self.root[key]

    def __setitem__(self, key:str, value):
        self.root[key] = value

    def __contains__(self, key:str) -> bool:
        return key in self.root


linkml_meta = LinkMLMeta({'default_prefix': 'clinical_model',
     'default_range': 'string',
     'description': 'Clinical data model for EGFR-mutant NSCLC diagnostic pathway',
     'id': 'https://ngdx.org/clinical_model',
     'imports': ['linkml:types'],
     'license': 'MIT',
     'name': 'clinical_model',
     'prefixes': {'clinical_model': {'prefix_prefix': 'clinical_model',
                                     'prefix_reference': 'https://uk-cpi.com/clinical_model/'},
                  'linkml': {'prefix_prefix': 'linkml',
                             'prefix_reference': 'https://w3id.org/linkml/'},
                  'loinc': {'prefix_prefix': 'loinc',
                            'prefix_reference': 'http://loinc.org/rdf/'},
                  'snomed': {'prefix_prefix': 'snomed',
                             'prefix_reference': 'http://snomed.info/id/'}},
     'source_file': 'schemas/clinical_model.yaml',
     'title': 'NG-DX EGFR-NSCLC Clinical Data Model'} )

class SexEnum(str, Enum):
    Male = "Male"
    Female = "Female"
    Indeterminate = "Indeterminate"
    Not_Known = "Not_Known"


class ImagingModalityEnum(str, Enum):
    CT = "CT"
    PT = "PT"
    MR = "MR"
    CR = "CR"
    US = "US"


class TStageEnum(str, Enum):
    TX = "TX"
    T0 = "T0"
    Tis = "Tis"
    T1a = "T1a"
    T1b = "T1b"
    T1c = "T1c"
    T2a = "T2a"
    T2b = "T2b"
    T3 = "T3"
    T4 = "T4"


class NStageEnum(str, Enum):
    NX = "NX"
    N0 = "N0"
    N1 = "N1"
    N2 = "N2"
    N3 = "N3"


class MStageEnum(str, Enum):
    M0 = "M0"
    M1a = "M1a"
    M1b = "M1b"
    M1c = "M1c"


class SmokingStatusEnum(str, Enum):
    Current_smoker = "Current_smoker"
    Former_smoker = "Former_smoker"
    Never_smoked = "Never_smoked"
    Non_smoker_unknown_history = "Non_smoker_unknown_history"
    Not_stated = "Not_stated"
    Unknown = "Unknown"


class AJCCStageEnum(str, Enum):
    Stage_0 = "Stage_0"
    IA1 = "IA1"
    IA2 = "IA2"
    IA3 = "IA3"
    IB = "IB"
    IIA = "IIA"
    IIB = "IIB"
    IIIA = "IIIA"
    IIIB = "IIIB"
    IIIC = "IIIC"
    IVA = "IVA"
    IVB = "IVB"


class SpecimenTypeEnum(str, Enum):
    Tissue = "Tissue"
    ctDNA = "ctDNA"


class SpecimenSourceEnum(str, Enum):
    Tissue = "Tissue"
    ctDNA = "ctDNA"


class NGSAssayTypeEnum(str, Enum):
    DNA_only = "DNA_only"
    RNA_only = "RNA_only"
    Concurrent_DNA_and_RNA = "Concurrent_DNA_and_RNA"


class VariantTierEnum(str, Enum):
    Tier_I = "Tier_I"
    Tier_II = "Tier_II"
    Tier_III = "Tier_III"
    Tier_IV = "Tier_IV"


class DetectionTimepointEnum(str, Enum):
    Baseline = "Baseline"
    Progression = "Progression"
    MRD = "MRD"
    Post_treatment = "Post_treatment"


class TreatmentIntentEnum(str, Enum):
    Curative_definitive = "Curative_definitive"
    Palliative = "Palliative"
    Adjuvant = "Adjuvant"
    Neoadjuvant = "Neoadjuvant"


class DoseFrequencyEnum(str, Enum):
    OD = "OD"
    BD = "BD"
    TID = "TID"
    q3w = "q3w"
    weekly = "weekly"


class DiscontinuationReasonEnum(str, Enum):
    Progression = "Progression"
    Toxicity = "Toxicity"
    Patient_choice = "Patient_choice"
    Death = "Death"
    Treatment_completion = "Treatment_completion"


class AssessmentTypeEnum(str, Enum):
    Baseline = "Baseline"
    Follow_up = "Follow_up"
    Progression = "Progression"


class RECISTResponseEnum(str, Enum):
    CR = "CR"
    PR = "PR"
    SD = "SD"
    PD = "PD"


class ProgressionTypeEnum(str, Enum):
    Oligoprogression = "Oligoprogression"
    Systemic_multi_site = "Systemic_multi_site"
    CNS_only = "CNS_only"
    Asymptomatic_slow = "Asymptomatic_slow"



class Patient(ConfiguredBaseModel):
    """
    Core patient entity with demographics and baseline clinical data
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://ngdx.org/clinical_model',
         'slot_usage': {'patient_id': {'name': 'patient_id', 'range': 'string'}}})

    patient_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Patient',
                       'Biopsy',
                       'Treatment',
                       'ResponseAssessment',
                       'ClinicalAssessment',
                       'ImagingStudy']} })
    nhs_number: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    age_at_diagnosis: Optional[int] = Field(default=None, ge=0, le=130, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    sex: Optional[SexEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    ethnicity_code: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    smoking_status: Optional[SmokingStatusEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    pack_years: Optional[float] = Field(default=None, ge=0, le=200, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    family_history_lung_cancer: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    ecog_baseline: Optional[int] = Field(default=None, ge=0, le=5, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    baseline_egfr: Optional[float] = Field(default=None, ge=0, le=200, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    baseline_wbc: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    baseline_hemoglobin: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    baseline_platelets: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    baseline_alt: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    baseline_ast: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    diagnosis_date: date = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })
    diagnosis_pathway: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Patient']} })

    @field_validator('patient_id')
    def pattern_patient_id(cls, v):
        pattern=re.compile(r"^NGDX-[0-9]{3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid patient_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid patient_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('nhs_number')
    def pattern_nhs_number(cls, v):
        pattern=re.compile(r"^[0-9]{10}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid nhs_number format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid nhs_number format: {v}"
            raise ValueError(err_msg)
        return v


class Biopsy(ConfiguredBaseModel):
    """
    Tissue or liquid biopsy procedure - multiple rows per patient
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://ngdx.org/clinical_model',
         'slot_usage': {'biopsy_id': {'name': 'biopsy_id', 'range': 'string'},
                        'patient_id': {'identifier': False, 'name': 'patient_id'}}})

    biopsy_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy', 'MolecularTest']} })
    patient_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Patient',
                       'Biopsy',
                       'Treatment',
                       'ResponseAssessment',
                       'ClinicalAssessment',
                       'ImagingStudy']} })
    biopsy_date: date = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    specimen_type: Optional[SpecimenTypeEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    biopsy_technique: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    biopsy_site_snomed: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    biopsy_site_description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    tissue_specimen_category: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    tissue_preparation_format: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    tissue_fixation_hours: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    tumor_cellularity_percent: Optional[float] = Field(default=None, ge=0, le=100, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    necrosis_percent: Optional[float] = Field(default=None, ge=0, le=100, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    pathology_slide_image_path: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    pathology_report_pdf_path: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    blood_tube_type: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    blood_collection_volume_ml: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    blood_draw_timestamp: Optional[datetime ] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    time_to_fractionation_hours: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    plasma_volume_ml: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    cfdna_concentration_ng_ul: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    cfdna_total_yield_ng: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    histologic_subtype: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    pdl1_tps_percent: Optional[int] = Field(default=None, ge=0, le=100, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    pdl1_antibody_clone: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    specimen_adequacy: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })
    tissue_sufficiency: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy']} })

    @field_validator('patient_id')
    def pattern_patient_id(cls, v):
        pattern=re.compile(r"^NGDX-[0-9]{3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid patient_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid patient_id format: {v}"
            raise ValueError(err_msg)
        return v


class MolecularTest(ConfiguredBaseModel):
    """
    NGS test from tissue or ctDNA - multiple rows per patient
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://ngdx.org/clinical_model',
         'slot_usage': {'biopsy_id': {'identifier': False, 'name': 'biopsy_id'},
                        'molecular_test_id': {'name': 'molecular_test_id',
                                              'range': 'string'}}})

    molecular_test_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest', 'Mutation', 'ResponseAssessment']} })
    biopsy_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Biopsy', 'MolecularTest']} })
    test_date: date = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })
    specimen_source: Optional[SpecimenSourceEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })
    ngs_panel_name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })
    ngs_panel_version: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })
    ngs_assay_type: Optional[NGSAssayTypeEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })
    dna_input_mass_ng: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })
    mean_coverage_depth: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })
    assay_lod_percent: Optional[float] = Field(default=None, ge=0, le=100, json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })
    ngs_report_pdf_path: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })
    vcf_file_path: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest']} })


class Mutation(ConfiguredBaseModel):
    """
    Individual genomic variant detected in NGS test - normalized to enable time-series tracking
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://ngdx.org/clinical_model',
         'slot_usage': {'molecular_test_id': {'identifier': False,
                                              'name': 'molecular_test_id',
                                              'required': True},
                        'mutation_id': {'name': 'mutation_id', 'range': 'string'}}})

    mutation_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    molecular_test_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest', 'Mutation', 'ResponseAssessment']} })
    gene_symbol: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    mutation_hgvs: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    mutation_type: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    mutation_classification: Optional[VariantTierEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    vaf_percent: Optional[float] = Field(default=None, ge=0.0, le=100.0, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    tumor_fraction_percent: Optional[float] = Field(default=None, ge=0.0, le=100.0, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    actionable_mutation: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    resistance_mutation: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    chip_status: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    is_primary_driver: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    is_acquired_resistance: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })
    detection_timepoint: Optional[DetectionTimepointEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Mutation']} })

    @field_validator('gene_symbol')
    def pattern_gene_symbol(cls, v):
        pattern=re.compile(r"^[A-Z0-9-]+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid gene_symbol format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid gene_symbol format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('mutation_hgvs')
    def pattern_mutation_hgvs(cls, v):
        pattern=re.compile(r"^[cp]\..+$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid mutation_hgvs format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid mutation_hgvs format: {v}"
            raise ValueError(err_msg)
        return v


class Treatment(ConfiguredBaseModel):
    """
    Treatment line with drug regimen and duration - multiple rows per patient
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://ngdx.org/clinical_model',
         'slot_usage': {'patient_id': {'identifier': False, 'name': 'patient_id'},
                        'treatment_id': {'name': 'treatment_id', 'range': 'string'}}})

    treatment_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment', 'ResponseAssessment']} })
    patient_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Patient',
                       'Biopsy',
                       'Treatment',
                       'ResponseAssessment',
                       'ClinicalAssessment',
                       'ImagingStudy']} })
    treatment_line: Optional[int] = Field(default=None, ge=0, le=10, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    treatment_intent: Optional[TreatmentIntentEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    drug_name: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    drug_dose_mg: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    drug_frequency: Optional[DoseFrequencyEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    drug_route: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    treatment_start_date: date = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    treatment_end_date: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    mdt_recommendation: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    mdt_date: Optional[date] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    prior_ici_exposure: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    months_since_last_ici: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })
    discontinuation_reason: Optional[DiscontinuationReasonEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment']} })

    @field_validator('patient_id')
    def pattern_patient_id(cls, v):
        pattern=re.compile(r"^NGDX-[0-9]{3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid patient_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid patient_id format: {v}"
            raise ValueError(err_msg)
        return v


class ResponseAssessment(ConfiguredBaseModel):
    """
    Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per patient
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://ngdx.org/clinical_model',
         'slot_usage': {'assessment_id': {'name': 'assessment_id', 'range': 'string'},
                        'imaging_study_id': {'identifier': False,
                                             'name': 'imaging_study_id'},
                        'molecular_test_id': {'identifier': False,
                                              'name': 'molecular_test_id'},
                        'patient_id': {'identifier': False, 'name': 'patient_id'},
                        'treatment_id': {'identifier': False, 'name': 'treatment_id'}}})

    assessment_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    patient_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Patient',
                       'Biopsy',
                       'Treatment',
                       'ResponseAssessment',
                       'ClinicalAssessment',
                       'ImagingStudy']} })
    treatment_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Treatment', 'ResponseAssessment']} })
    imaging_study_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment', 'ImagingStudy']} })
    molecular_test_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['MolecularTest', 'Mutation', 'ResponseAssessment']} })
    assessment_date: date = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment', 'ClinicalAssessment']} })
    assessment_type: Optional[AssessmentTypeEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    recist_response: Optional[RECISTResponseEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    sum_target_lesions_mm: Optional[float] = Field(default=None, ge=0, le=500, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    percent_change_from_baseline: Optional[float] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    new_lesions_present: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    ctdna_vaf_percent: Optional[float] = Field(default=None, ge=0.0, le=100.0, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    ctdna_mutation_cleared: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    ctdna_tumor_fraction_percent: Optional[float] = Field(default=None, ge=0.0, le=100.0, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    ecog_status: Optional[int] = Field(default=None, ge=0, le=5, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment', 'ClinicalAssessment']} })
    symptom_improvement: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    progression_detected: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    progression_type: Optional[ProgressionTypeEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    time_to_progression_months: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    resistance_mutation_detected: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    resistance_mechanism: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })
    histologic_transformation: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment']} })

    @field_validator('patient_id')
    def pattern_patient_id(cls, v):
        pattern=re.compile(r"^NGDX-[0-9]{3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid patient_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid patient_id format: {v}"
            raise ValueError(err_msg)
        return v


class ClinicalAssessment(ConfiguredBaseModel):
    """
    Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patient
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://ngdx.org/clinical_model',
         'slot_usage': {'clinical_assessment_id': {'name': 'clinical_assessment_id',
                                                   'range': 'string'},
                        'ecog_status': {'identifier': False, 'name': 'ecog_status'},
                        'patient_id': {'identifier': False, 'name': 'patient_id'}}})

    clinical_assessment_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    patient_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Patient',
                       'Biopsy',
                       'Treatment',
                       'ResponseAssessment',
                       'ClinicalAssessment',
                       'ImagingStudy']} })
    assessment_date: date = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment', 'ClinicalAssessment']} })
    visit_type: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    ecog_status: Optional[int] = Field(default=None, ge=0, le=5, json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment', 'ClinicalAssessment']} })
    symptoms_coded: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    symptom_severity_grade: Optional[int] = Field(default=None, ge=0, le=5, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    wbc: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    hemoglobin: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    platelets: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    neutrophils: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    egfr_value: Optional[float] = Field(default=None, ge=0, le=200, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    alt: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })
    ast: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ClinicalAssessment']} })

    @field_validator('patient_id')
    def pattern_patient_id(cls, v):
        pattern=re.compile(r"^NGDX-[0-9]{3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid patient_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid patient_id format: {v}"
            raise ValueError(err_msg)
        return v


class ImagingStudy(ConfiguredBaseModel):
    """
    Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient
    """
    linkml_meta: ClassVar[LinkMLMeta] = LinkMLMeta({'from_schema': 'https://ngdx.org/clinical_model',
         'slot_usage': {'imaging_study_id': {'name': 'imaging_study_id',
                                             'range': 'string'},
                        'patient_id': {'identifier': False, 'name': 'patient_id'}}})

    imaging_study_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ResponseAssessment', 'ImagingStudy']} })
    patient_id: str = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['Patient',
                       'Biopsy',
                       'Treatment',
                       'ResponseAssessment',
                       'ClinicalAssessment',
                       'ImagingStudy']} })
    study_uid: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    series_uid: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    accession_number: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    scan_date: date = Field(default=..., json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    imaging_modality: Optional[ImagingModalityEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    study_description: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    dicom_file_path: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    thumbnail_image_path: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    ct_kvp: Optional[int] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    ct_mas: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    ct_slice_thickness_mm: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    pet_tracer: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    pet_injected_dose_mbq: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    pet_uptake_time_min: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    t_stage: Optional[TStageEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    n_stage: Optional[NStageEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    m_stage: Optional[MStageEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    m_sites: Optional[str] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    ajcc_stage: Optional[AJCCStageEnum] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    primary_tumor_diameter_mm: Optional[float] = Field(default=None, ge=0, le=300, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    suv_max: Optional[float] = Field(default=None, ge=0, le=50, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    brain_metastasis_present: Optional[bool] = Field(default=None, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    brain_lesion_count: Optional[int] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })
    brain_largest_lesion_mm: Optional[float] = Field(default=None, ge=0, json_schema_extra = { "linkml_meta": {'domain_of': ['ImagingStudy']} })

    @field_validator('patient_id')
    def pattern_patient_id(cls, v):
        pattern=re.compile(r"^NGDX-[0-9]{3}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid patient_id format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid patient_id format: {v}"
            raise ValueError(err_msg)
        return v

    @field_validator('study_uid')
    def pattern_study_uid(cls, v):
        pattern=re.compile(r"^[0-9.]{1,64}$")
        if isinstance(v, list):
            for element in v:
                if isinstance(element, str) and not pattern.match(element):
                    err_msg = f"Invalid study_uid format: {element}"
                    raise ValueError(err_msg)
        elif isinstance(v, str) and not pattern.match(v):
            err_msg = f"Invalid study_uid format: {v}"
            raise ValueError(err_msg)
        return v


# Model rebuild
# see https://pydantic-docs.helpmanual.io/usage/models/#rebuilding-a-model
Patient.model_rebuild()
Biopsy.model_rebuild()
MolecularTest.model_rebuild()
Mutation.model_rebuild()
Treatment.model_rebuild()
ResponseAssessment.model_rebuild()
ClinicalAssessment.model_rebuild()
ImagingStudy.model_rebuild()
