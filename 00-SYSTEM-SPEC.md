# Clinical Decision Support System - Detailed Specification v2
**Domain**: EGFR-mutant Non-Small Cell Lung Cancer (NSCLC) Diagnostic & Treatment Pathway  
**Version**: 0.2  
**Date**: 2026-04-24

---

## 1. Problem Statement & Scope

**Current State**: Clinicians spend 20-30 minutes per patient manually extracting relevant information from unstructured PDF reports (health records, clinical observations, imaging, pathology, molecular testing).

**Target State**: Structured patient-level dashboard powered by standardized data conforming to NG-DX WP3 Data Dictionary (142 variables across 7 buckets).

**MVP Focus**: 
- ✅ Data modeling (galaxy schema - multiple facts + shared Patient dimension)
- ✅ Database implementation (SQLite)
- ✅ Sample data loading from simulated_data.csv (100 patients)
- ✅ Dashboard prototype for individual patient diagnostics
- ❌ PDF ETL pipeline (deferred to Phase 2)

---

## 2. Data Model Design

### 2.1 Schema Approach: **Galaxy Schema** (Analytical)

**Rationale for Galaxy Schema**:

1. **Multiple business processes**: Patients undergo different types of clinical events (imaging, biopsies, treatments, clinical assessments) → separate fact tables per process type
2. **Shared dimension**: All fact tables share the Patient dimension - 1 patient can have N rows in each fact table
3. **Time-series on multiple measurement types**: Each fact table captures time-stamped events independently (multiple imaging studies over time, multiple biopsies, multiple ctDNA tests)
4. **Flexible querying**: Enables both within-process queries (e.g., "Show VAF trend over time") and cross-process queries (e.g., "Compare imaging findings with molecular results")
5. **Snowflake features where needed**: Some fact tables have normalized children (Biopsy → MolecularTest → Mutation), adding hierarchical normalization

**Galaxy Schema = Multiple Facts + Shared Dimension**:
- **1 Dimension Table**: Patient (1 row per patient)
- **6 Fact Tables**: ImagingStudy, Biopsy, MolecularTest, Treatment, ResponseAssessment, ClinicalAssessment (N rows per patient)
- **Normalized sub-facts**: Mutation (child of MolecularTest)

**Schema Structure**:
```
               Patient (Dimension)
          1 row per patient - Demographics & Baseline
                        ↓  ↓  ↓  ↓  ↓  ↓
      ┌─────────────────┴──┴──┴──┴──┴──┴─────────────┐
      ↓                 ↓           ↓                 ↓
  ImagingStudy      Biopsy     Treatment    ClinicalAssessment
   (N rows)        (N rows)    (N rows)         (N rows)
  CT/PET/MRI          ↓         Drug            ECOG, Labs
                      ↓         Regimens
                 MolecularTest                       ↓
                  (N rows)                   ResponseAssessment
                  NGS Tests                      (N rows)
                      ↓                    Links: Treatment +
                  Mutation                 Imaging + Molecular
                  (N rows)
              Individual Variants
```

**Why This is a Galaxy Schema**:
- ✅ Multiple independent fact tables (not just one central fact)
- ✅ All fact tables share the Patient dimension
- ✅ Each fact table measures a different business process
- ✅ Enables flexible cross-process analysis

**Not a Pure Snowflake** (which would have 1 fact + normalized dimensions)

### 2.2 Detailed Table Schemas

---

#### **DIM_PATIENT** (Dimension - 1 row per patient)
*Contains static/slowly-changing demographic and baseline clinical context*

```sql
CREATE TABLE dim_patient (
    -- Primary Key
    patient_sk INTEGER PRIMARY KEY AUTOINCREMENT,  -- Surrogate key
    
    -- Business Key
    nhs_number VARCHAR(10) UNIQUE NOT NULL,        -- Var_001
    patient_id VARCHAR(20) UNIQUE NOT NULL,        -- e.g., NGDX-001
    
    -- Demographics (Bucket 1)
    age_at_diagnosis INTEGER,                       -- Var_002
    sex VARCHAR(20),                                -- Var_003: Male/Female/Indeterminate
    ethnicity_code VARCHAR(2),                      -- Var_004: A=White British, etc.
    
    -- Risk Factors (Bucket 1)
    smoking_status VARCHAR(50),                     -- Var_006: Current/Former/Never
    pack_years REAL,                                -- Var_007
    family_history_lung_cancer BOOLEAN,             -- Var_008
    
    -- Baseline Performance & Labs (Bucket 1)
    ecog_baseline INTEGER CHECK(ecog_baseline BETWEEN 0 AND 5), -- Var_009
    baseline_egfr REAL,                             -- Var_012: eGFR (mL/min/1.73m²)
    baseline_wbc REAL,                              -- Var_011: White blood cell count
    baseline_hemoglobin REAL,                       -- Var_011
    baseline_platelets REAL,                        -- Var_011
    baseline_alt REAL,                              -- Var_014: Liver function
    baseline_ast REAL,                              -- Var_014
    
    -- Diagnosis Metadata
    diagnosis_date DATE,                            -- Var_017
    diagnosis_pathway VARCHAR(50),                  -- Var_015: NG12 referral pathway
    
    -- Audit Columns
    record_created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    record_updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Why 1 row per patient?** Demographics and baseline labs are measured once at diagnosis. Longitudinal changes (e.g., ECOG status over time) go into `fact_clinical_assessments`.

---

#### **FACT_IMAGING_STUDIES** (Fact - N rows per patient)
*Time-series of imaging studies (CT, PET-CT, MRI)*

```sql
CREATE TABLE fact_imaging_studies (
    -- Primary Key
    imaging_study_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Keys
    patient_sk INTEGER NOT NULL,
    date_sk INTEGER NOT NULL,                       -- Links to dim_date
    
    -- Business Keys
    study_uid VARCHAR(64) UNIQUE,                   -- Var_019: DICOM Study Instance UID
    series_uid VARCHAR(64),                         -- Var_019: DICOM Series Instance UID
    accession_number VARCHAR(16),                   -- Var_016
    
    -- Study Metadata (Bucket 2)
    scan_date DATE NOT NULL,                        -- Var_020
    imaging_modality VARCHAR(10),                   -- Var_018: CT/PT/MR/CR
    imaging_modality_sk INTEGER,                    -- FK to dim_imaging_modality
    
    -- Image File References (for dashboard display)
    dicom_file_path TEXT,                           -- Path to DICOM files
    thumbnail_image_path TEXT,                      -- Path to thumbnail PNG/JPG
    study_description TEXT,                         -- e.g., "Chest CT with contrast"
    
    -- CT Acquisition Parameters (Bucket 2)
    ct_kvp INTEGER,                                 -- Var_021: Kilovolt peak
    ct_mas REAL,                                    -- Var_021: Tube current
    ct_slice_thickness_mm REAL,                     -- Var_021
    
    -- PET Parameters (Bucket 2)
    pet_tracer VARCHAR(20),                         -- e.g., F18-FDG
    pet_injected_dose_mbq REAL,                     -- Var_022
    pet_uptake_time_min REAL,                       -- Var_022
    
    -- TNM Staging (Bucket 2)
    t_stage VARCHAR(10),                            -- Var_023: TX/T0/T1a/T1b/T2a/etc.
    n_stage VARCHAR(10),                            -- Var_024: NX/N0/N1/N2/N3
    m_stage VARCHAR(10),                            -- Var_025: M0/M1a/M1b/M1c
    m_sites TEXT,                                   -- Var_025: Metastatic sites (multi-value)
    ajcc_stage VARCHAR(10),                         -- Var_030: IA1/IA2/.../IVB
    tnm_stage_sk INTEGER,                           -- FK to dim_tnm_stage
    
    -- Tumor Measurements (Bucket 2)
    primary_tumor_diameter_mm REAL,                 -- Var_026: RECIST target lesion
    suv_max REAL,                                   -- Var_027: PET SUV max
    
    -- Brain Imaging (Bucket 2)
    brain_metastasis_present BOOLEAN,               -- Var_028
    brain_lesion_count INTEGER,                     -- Var_028
    brain_largest_lesion_mm REAL,                   -- Var_028
    
    -- Audit
    FOREIGN KEY (patient_sk) REFERENCES dim_patient(patient_sk),
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk),
    FOREIGN KEY (imaging_modality_sk) REFERENCES dim_imaging_modality(modality_sk),
    FOREIGN KEY (tnm_stage_sk) REFERENCES dim_tnm_stage(stage_sk)
);
```

**Multiple rows per patient**: A patient gets baseline CT, 3-month follow-up PET-CT, progression imaging, etc. Each scan = 1 row.

**Image file references**: 
- `dicom_file_path`: Store path to original DICOM files (e.g., `/data/imaging/NGDX-001/study_2024-03-15/`)
- `thumbnail_image_path`: Pre-rendered PNG thumbnails for dashboard quick view
- Dashboard can link to full DICOM viewer (e.g., OHIF Viewer, Orthanc)

---

#### **FACT_BIOPSIES** (Fact - N rows per patient)
*Tissue and liquid biopsy procedures*

```sql
CREATE TABLE fact_biopsies (
    -- Primary Key
    biopsy_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Keys
    patient_sk INTEGER NOT NULL,
    date_sk INTEGER NOT NULL,
    
    -- Business Key
    biopsy_id VARCHAR(20) UNIQUE NOT NULL,          -- Internal tracking ID
    
    -- Procedure Metadata (Bucket 3 & 4)
    biopsy_date DATE NOT NULL,
    specimen_type VARCHAR(20),                      -- Tissue / Liquid (ctDNA)
    biopsy_technique VARCHAR(50),                   -- Var_032: EBUS-TBNA/CT-guided/VATS/etc.
    biopsy_procedure_sk INTEGER,                    -- FK to dim_biopsy_procedures
    
    -- Anatomical Location (Bucket 3)
    biopsy_site_snomed VARCHAR(20),                 -- Var_029: SNOMED CT code
    biopsy_site_description TEXT,                   -- Human-readable: "Left lower lobe"
    
    -- Tissue Biopsy Specifics (Bucket 3)
    tissue_specimen_category VARCHAR(50),           -- Var_035: Histology core/Cytology FNA/Cell block
    tissue_preparation_format VARCHAR(50),          -- Var_036: FFPE block/Fresh frozen
    tissue_fixation_hours REAL,                     -- Var_037: Hours in fixative
    tumor_cellularity_percent REAL,                 -- Var_039: % tumor nuclei
    necrosis_percent REAL,                          -- Var_043
    
    -- Image References (Pathology)
    pathology_slide_image_path TEXT,                -- Path to whole-slide image (WSI)
    pathology_report_pdf_path TEXT,                 -- Path to original PDF report
    
    -- Liquid Biopsy Specifics (Bucket 4)
    blood_tube_type VARCHAR(50),                    -- Var_054: K2EDTA/Streck BCT
    blood_collection_volume_ml REAL,                -- Var_056
    blood_draw_timestamp TIMESTAMP,                 -- Var_057
    time_to_fractionation_hours REAL,               -- Var_059
    plasma_volume_ml REAL,                          -- Var_062
    cfdna_concentration_ng_ul REAL,                 -- Var_067
    cfdna_total_yield_ng REAL,                      -- Var_068
    
    -- Histology (Bucket 3)
    histologic_subtype VARCHAR(100),                -- Var_041: Adenocarcinoma/Squamous/etc.
    histology_sk INTEGER,                           -- FK to dim_histology
    pdl1_tps_percent REAL,                          -- Var_045: PD-L1 tumor proportion score
    pdl1_antibody_clone VARCHAR(50),                -- Var_044: 22C3/SP263/etc.
    
    -- Quality Flags
    specimen_adequacy VARCHAR(20),                  -- Var_034: ROSE result
    tissue_sufficiency VARCHAR(50),                 -- Var_083: Sufficient/Insufficient
    
    -- Audit
    FOREIGN KEY (patient_sk) REFERENCES dim_patient(patient_sk),
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk),
    FOREIGN KEY (biopsy_procedure_sk) REFERENCES dim_biopsy_procedures(procedure_sk),
    FOREIGN KEY (histology_sk) REFERENCES dim_histology(histology_sk)
);
```

**Multiple rows per patient**: Initial tissue biopsy → progression liquid biopsy → repeat biopsy at resistance. Each procedure = 1 row.

**Image references for pathology**:
- `pathology_slide_image_path`: Whole-slide imaging (WSI) files in formats like `.svs`, `.ndpi`
- Dashboard can embed QuPath or OpenSeadragon viewer for zoomable pathology images

---

#### **FACT_MOLECULAR_RESULTS** (Fact - N rows per patient)
*NGS results from tissue or ctDNA testing*

```sql
CREATE TABLE fact_molecular_results (
    -- Primary Key
    molecular_result_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Keys
    patient_sk INTEGER NOT NULL,
    biopsy_sk INTEGER,                              -- Links to source biopsy
    date_sk INTEGER NOT NULL,
    
    -- Test Metadata (Bucket 5)
    test_date DATE NOT NULL,
    specimen_source VARCHAR(20),                    -- Tissue / ctDNA
    ngs_panel_name VARCHAR(100),                    -- Var_046: FoundationOne CDx/Guardant360/etc.
    ngs_panel_version VARCHAR(20),                  -- Var_046
    ngs_assay_type VARCHAR(30),                     -- Var_047: DNA_only/RNA_only/Concurrent
    
    -- Sequencing QC (Bucket 5)
    dna_input_mass_ng REAL,                         -- Var_048
    mean_coverage_depth REAL,                       -- Var_049/Var_073
    assay_lod_percent REAL,                         -- Var_080: Limit of detection
    
    -- NGS Report References
    ngs_report_pdf_path TEXT,                       -- Path to original NGS report PDF
    vcf_file_path TEXT,                             -- Path to VCF file (variants)
    
    -- Audit
    FOREIGN KEY (patient_sk) REFERENCES dim_patient(patient_sk),
    FOREIGN KEY (biopsy_sk) REFERENCES fact_biopsies(biopsy_sk),
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk)
);
```

---

#### **FACT_MUTATIONS** (Fact - N rows per molecular result)
*Individual mutations detected in NGS tests (normalized to avoid multi-value fields)*

```sql
CREATE TABLE fact_mutations (
    -- Primary Key
    mutation_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Keys
    molecular_result_sk INTEGER NOT NULL,
    patient_sk INTEGER NOT NULL,
    mutation_sk_dim INTEGER,                        -- FK to dim_mutations (lookup)
    
    -- Mutation Details (Bucket 5)
    gene_symbol VARCHAR(20) NOT NULL,               -- EGFR, TP53, MET, KRAS, etc.
    mutation_hgvs TEXT,                             -- Var_050/Var_074: HGVS notation
    mutation_type VARCHAR(50),                      -- Exon 19 deletion/L858R/T790M/etc.
    mutation_classification VARCHAR(20),            -- Var_078: Tier I/II/III/IV
    
    -- Quantitative Measures (Bucket 5)
    vaf_percent REAL,                               -- Var_075: Variant allele frequency
    tumor_fraction_percent REAL,                    -- Var_076: Tumor fraction estimate
    
    -- Clinical Significance
    actionable_mutation BOOLEAN,                    -- True if guides therapy choice
    resistance_mutation BOOLEAN,                    -- Var_096: True for T790M, C797S, etc.
    chip_status VARCHAR(20),                        -- Var_077: Clonal hematopoiesis filter
    
    -- Context Flags
    is_primary_driver BOOLEAN,                      -- True for initial EGFR sensitizing
    is_acquired_resistance BOOLEAN,                 -- True for post-treatment resistance
    detection_timepoint VARCHAR(20),                -- Baseline / Progression / MRD
    
    -- Audit
    FOREIGN KEY (molecular_result_sk) REFERENCES fact_molecular_results(molecular_result_sk),
    FOREIGN KEY (patient_sk) REFERENCES dim_patient(patient_sk),
    FOREIGN KEY (mutation_sk_dim) REFERENCES dim_mutations(mutation_sk)
);
```

**Why separate mutations table?** A single NGS test detects multiple mutations (EGFR + TP53 + MET). Normalizing into separate rows enables:
1. Time-series queries per mutation (e.g., "Track EGFR Ex19del VAF over time")
2. Resistance mutation detection (e.g., "Flag when T790M appears")
3. Co-mutation analysis (e.g., "Patients with EGFR + TP53")

---

#### **FACT_TREATMENTS** (Fact - N rows per patient)
*Treatment lines and regimens*

```sql
CREATE TABLE fact_treatments (
    -- Primary Key
    treatment_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Keys
    patient_sk INTEGER NOT NULL,
    start_date_sk INTEGER NOT NULL,
    end_date_sk INTEGER,                            -- NULL if ongoing
    drug_sk INTEGER,                                -- FK to dim_drugs
    
    -- Treatment Details (Bucket 6)
    treatment_line INTEGER,                         -- 1st-line, 2nd-line, etc.
    treatment_intent VARCHAR(30),                   -- Var_086: Curative/Palliative/Adjuvant
    drug_name VARCHAR(100),                         -- Var_087: Osimertinib, etc.
    drug_dose_mg REAL,                              -- Var_087
    drug_frequency VARCHAR(20),                     -- Var_087: OD/BD/q3w
    drug_route VARCHAR(20),                         -- Var_087: Oral/IV
    
    -- Treatment Period
    treatment_start_date DATE NOT NULL,             -- Var_089
    treatment_end_date DATE,                        -- NULL if ongoing
    
    -- Treatment Context
    mdt_recommendation TEXT,                        -- Var_084: MDT decision
    mdt_date DATE,                                  -- Var_084
    
    -- Prior Therapy Context
    prior_ici_exposure BOOLEAN,                     -- Var_089: Recent ICI flag
    months_since_last_ici REAL,                     -- Var_089
    
    -- Discontinuation
    discontinuation_reason VARCHAR(100),            -- Progression/Toxicity/Patient choice
    
    -- Audit
    FOREIGN KEY (patient_sk) REFERENCES dim_patient(patient_sk),
    FOREIGN KEY (start_date_sk) REFERENCES dim_date(date_sk),
    FOREIGN KEY (end_date_sk) REFERENCES dim_date(date_sk),
    FOREIGN KEY (drug_sk) REFERENCES dim_drugs(drug_sk)
);
```

**Multiple rows per patient**: 1st-line osimertinib → progression → 2nd-line chemotherapy. Each treatment line = 1 row.

---

#### **FACT_RESPONSE_ASSESSMENTS** (Fact - N rows per patient)
*Serial monitoring of treatment response*

```sql
CREATE TABLE fact_response_assessments (
    -- Primary Key
    assessment_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Keys
    patient_sk INTEGER NOT NULL,
    treatment_sk INTEGER,                           -- Links to active treatment
    date_sk INTEGER NOT NULL,
    imaging_study_sk INTEGER,                       -- Links to concurrent imaging
    molecular_result_sk INTEGER,                    -- Links to concurrent ctDNA test
    
    -- Assessment Metadata (Bucket 6)
    assessment_date DATE NOT NULL,
    assessment_type VARCHAR(30),                    -- Baseline/Follow-up/Progression
    
    -- RECIST Response (Bucket 6)
    recist_response VARCHAR(10),                    -- Var_091: CR/PR/SD/PD
    sum_target_lesions_mm REAL,                     -- Var_092: Sum of diameters
    percent_change_from_baseline REAL,              -- Var_092: Calculated
    new_lesions_present BOOLEAN,                    -- RECIST PD criteria
    
    -- ctDNA Monitoring (Bucket 6)
    ctdna_vaf_percent REAL,                         -- From linked molecular_result
    ctdna_mutation_cleared BOOLEAN,                 -- Var_093: Primary mutation undetectable
    ctdna_tumor_fraction_percent REAL,              -- Tumor burden estimate
    
    -- Clinical Assessment
    ecog_status INTEGER,                            -- ECOG at this timepoint
    symptom_improvement BOOLEAN,                    -- Patient-reported
    
    -- Progression Flags (Bucket 6)
    progression_detected BOOLEAN,
    progression_type VARCHAR(50),                   -- Var_095: Oligoprogression/Systemic/CNS-only
    time_to_progression_months REAL,                -- Var_099: Calculated from treatment start
    
    -- Resistance Mechanism (Bucket 6)
    resistance_mutation_detected BOOLEAN,           -- Var_096: T790M/C797S/MET amp
    resistance_mechanism VARCHAR(100),              -- Var_096
    histologic_transformation BOOLEAN,              -- Var_097: SCLC transformation
    
    -- Audit
    FOREIGN KEY (patient_sk) REFERENCES dim_patient(patient_sk),
    FOREIGN KEY (treatment_sk) REFERENCES fact_treatments(treatment_sk),
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk),
    FOREIGN KEY (imaging_study_sk) REFERENCES fact_imaging_studies(imaging_study_sk),
    FOREIGN KEY (molecular_result_sk) REFERENCES fact_molecular_results(molecular_result_sk)
);
```

**Multiple rows per patient**: Baseline → 6-week → 12-week → progression assessments. Each timepoint = 1 row.

**Linked imaging + ctDNA**: Each response assessment can link to concurrent imaging scan AND ctDNA test for integrated assessment.

---

#### **FACT_CLINICAL_ASSESSMENTS** (Fact - N rows per patient)
*Longitudinal clinical status (ECOG, symptoms, labs)*

```sql
CREATE TABLE fact_clinical_assessments (
    -- Primary Key
    assessment_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Foreign Keys
    patient_sk INTEGER NOT NULL,
    date_sk INTEGER NOT NULL,
    
    -- Assessment Metadata
    assessment_date DATE NOT NULL,
    visit_type VARCHAR(30),                         -- Clinic visit/Phone call/Hospitalization
    
    -- Performance Status
    ecog_status INTEGER CHECK(ecog_status BETWEEN 0 AND 5),
    
    -- Symptoms (Bucket 1)
    symptoms_coded TEXT,                            -- Var_005: Multi-value SNOMED codes
    symptom_severity_grade INTEGER,                 -- CTCAE grade
    
    -- Laboratory Results
    wbc REAL,
    hemoglobin REAL,
    platelets REAL,
    neutrophils REAL,
    egfr_value REAL,
    alt REAL,
    ast REAL,
    
    -- Audit
    FOREIGN KEY (patient_sk) REFERENCES dim_patient(patient_sk),
    FOREIGN KEY (date_sk) REFERENCES dim_date(date_sk)
);
```

---

### 2.3 Dimension Tables (Lookups)

#### **DIM_DATE** (Standard date dimension)
```sql
CREATE TABLE dim_date (
    date_sk INTEGER PRIMARY KEY,                    -- Format: YYYYMMDD (e.g., 20260315)
    full_date DATE UNIQUE NOT NULL,
    year INTEGER,
    quarter INTEGER,
    month INTEGER,
    month_name VARCHAR(10),
    week_of_year INTEGER,
    day_of_month INTEGER,
    day_of_week INTEGER,
    day_name VARCHAR(10),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN                              -- UK bank holidays
);
```

#### **DIM_IMAGING_MODALITY**
```sql
CREATE TABLE dim_imaging_modality (
    modality_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    modality_code VARCHAR(10) UNIQUE NOT NULL,      -- CT/PT/MR/CR/DX/US
    modality_name VARCHAR(50),                      -- Computed Tomography/PET-CT/etc.
    modality_description TEXT
);
```

#### **DIM_TNM_STAGE**
```sql
CREATE TABLE dim_tnm_stage (
    stage_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    t_stage VARCHAR(10),
    n_stage VARCHAR(10),
    m_stage VARCHAR(10),
    ajcc_stage VARCHAR(10),
    tnm_edition VARCHAR(10) DEFAULT '8th',
    stage_group_ordinal INTEGER,                    -- For sorting: IA1=1, IA2=2, ..., IVB=14
    UNIQUE(t_stage, n_stage, m_stage)
);
```

#### **DIM_HISTOLOGY**
```sql
CREATE TABLE dim_histology (
    histology_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    histology_code VARCHAR(20) UNIQUE,              -- ICD-O-3 morphology code
    histology_name VARCHAR(100),                    -- Adenocarcinoma NOS/Squamous cell/etc.
    histology_category VARCHAR(50),                 -- NSCLC/SCLC/Carcinoid
    icd_o_3_code VARCHAR(10)                        -- 8140/3, 8070/3, etc.
);
```

#### **DIM_MUTATIONS**
```sql
CREATE TABLE dim_mutations (
    mutation_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    gene_symbol VARCHAR(20) NOT NULL,
    mutation_type VARCHAR(100) UNIQUE NOT NULL,     -- Ex19del, L858R, T790M, etc.
    mutation_class VARCHAR(30),                     -- Sensitizing/Resistance/Co-mutation
    actionable BOOLEAN,
    tier_classification VARCHAR(20),                -- Tier I/II/III/IV (AMP/ASCO/CAP)
    clinical_significance TEXT
);
```

#### **DIM_DRUGS**
```sql
CREATE TABLE dim_drugs (
    drug_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    drug_inn VARCHAR(100) UNIQUE NOT NULL,          -- International Nonproprietary Name
    drug_brand_names TEXT,                          -- Tagrisso/Iressa/Tarceva/etc.
    drug_class VARCHAR(50),                         -- EGFR TKI/Chemotherapy/ICI
    drug_generation VARCHAR(20),                    -- 1st-gen/2nd-gen/3rd-gen TKI
    standard_dose_mg REAL,
    standard_frequency VARCHAR(20),
    route VARCHAR(20)                               -- Oral/IV
);
```

#### **DIM_BIOPSY_PROCEDURES**
```sql
CREATE TABLE dim_biopsy_procedures (
    procedure_sk INTEGER PRIMARY KEY AUTOINCREMENT,
    procedure_code VARCHAR(20) UNIQUE NOT NULL,
    procedure_name VARCHAR(100),                    -- EBUS-TBNA/CT-guided biopsy/etc.
    procedure_category VARCHAR(30),                 -- Bronchoscopy/Image-guided/Surgical
    invasiveness_level VARCHAR(20)                  -- Minimally invasive/Invasive/Surgical
);
```

---

## 3. Example: Complete Patient Record (NGDX-001)

### Patient: NGDX-001 (73-year-old female, Stage IA1, EGFR Ex19del)

#### **DIM_PATIENT** (1 row)
```
patient_sk: 1
nhs_number: 4000007963
patient_id: NGDX-001
age_at_diagnosis: 73
sex: Female
ethnicity_code: A
smoking_status: Never smoked
pack_years: 0
ecog_baseline: 0
diagnosis_date: 2020-03-15
ajcc_stage_baseline: IA1
```

#### **FACT_IMAGING_STUDIES** (4 rows over 2 years)
| imaging_study_sk | scan_date  | modality | t_stage | n_stage | m_stage | ajcc_stage | primary_tumor_mm | suv_max | dicom_file_path             |
|------------------|------------|----------|---------|---------|---------|------------|------------------|---------|------------------------------|
| 1001             | 2020-03-10 | CT       | T2a     | N0      | M0      | IA1        | 18.5             | NULL    | /imaging/NGDX-001/baseline   |
| 1002             | 2020-06-15 | PET      | T1a     | N0      | M0      | IA1        | 12.0             | 4.2     | /imaging/NGDX-001/post-surg  |
| 1003             | 2021-03-20 | CT       | NULL    | N0      | M0      | NULL       | 0                | NULL    | /imaging/NGDX-001/fu-12mo    |
| 1004             | 2022-05-10 | PET      | NULL    | N2      | M1b     | IVB        | 35.0             | 8.9     | /imaging/NGDX-001/progression|

*Interpretation*: Baseline CT shows T2a lesion → Post-surgery downsized → 12-month follow-up clear → Progression at 26 months with mediastinal nodes + brain met.

#### **FACT_BIOPSIES** (2 rows)
| biopsy_sk | biopsy_date | specimen_type | technique      | histology              | tumor_cellularity | pdl1_tps | pathology_slide_path          |
|-----------|-------------|---------------|----------------|------------------------|-------------------|----------|-------------------------------|
| 2001      | 2020-03-12  | Tissue        | EBUS-TBNA      | Adenocarcinoma 8140/3  | 60%               | 3%       | /pathology/NGDX-001/biopsy-01 |
| 2002      | 2022-05-12  | Liquid (ctDNA)| Venipuncture   | N/A                    | N/A               | N/A      | NULL                          |

#### **FACT_MOLECULAR_RESULTS** (3 rows)
| molecular_result_sk | test_date  | specimen_source | ngs_panel           | mean_coverage | ngs_report_pdf_path               |
|---------------------|------------|-----------------|---------------------|---------------|-----------------------------------|
| 3001                | 2020-03-14 | Tissue          | FoundationOne CDx   | 850x          | /reports/NGDX-001/tissue-ngs.pdf  |
| 3002                | 2020-09-01 | ctDNA           | Guardant360         | 12000x        | /reports/NGDX-001/ctdna-baseline.pdf |
| 3003                | 2022-05-14 | ctDNA           | Guardant360         | 11500x        | /reports/NGDX-001/ctdna-prog.pdf  |

#### **FACT_MUTATIONS** (7 rows across 3 tests)
| mutation_sk | molecular_result_sk | gene_symbol | mutation_type        | vaf_percent | actionable | resistance | is_primary_driver | detection_timepoint |
|-------------|---------------------|-------------|----------------------|-------------|------------|------------|-------------------|---------------------|
| 4001        | 3001                | EGFR        | Exon 19 deletion     | 38.5        | TRUE       | FALSE      | TRUE              | Baseline            |
| 4002        | 3001                | TP53        | R273H                | 42.0        | FALSE      | FALSE      | FALSE             | Baseline            |
| 4003        | 3002                | EGFR        | Exon 19 deletion     | 0.08        | TRUE       | FALSE      | TRUE              | Post-surgery MRD    |
| 4004        | 3003                | EGFR        | Exon 19 deletion     | 12.4        | TRUE       | FALSE      | TRUE              | Progression         |
| 4005        | 3003                | EGFR        | T790M                | 8.2         | TRUE       | TRUE       | FALSE             | Progression         |
| 4006        | 3003                | MET         | Amplification        | N/A         | TRUE       | TRUE       | FALSE             | Progression         |
| 4007        | 3003                | TP53        | R273H                | 14.0        | FALSE      | FALSE      | FALSE             | Progression         |

*Interpretation*: 
- Baseline tissue: EGFR Ex19del (primary driver) + TP53 mutation
- Post-surgery ctDNA: Minimal residual disease (0.08% VAF)
- Progression ctDNA: Rising EGFR Ex19del + acquired T790M + MET amplification (dual resistance)

#### **FACT_TREATMENTS** (2 rows)
| treatment_sk | treatment_line | treatment_intent | drug_name   | drug_dose | start_date | end_date   | discontinuation_reason |
|--------------|----------------|------------------|-------------|-----------|------------|------------|------------------------|
| 5001         | 0              | Curative         | Surgery     | N/A       | 2020-03-25 | 2020-03-25 | N/A                    |
| 5002         | 1              | Adjuvant         | Osimertinib | 80mg OD   | 2020-04-15 | 2022-05-08 | Disease progression    |

#### **FACT_RESPONSE_ASSESSMENTS** (5 rows)
| assessment_sk | assessment_date | assessment_type | recist_response | sum_target_lesions_mm | ctdna_vaf | progression_detected | resistance_mutation_detected | imaging_study_sk | molecular_result_sk |
|---------------|-----------------|-----------------|-----------------|-----------------------|-----------|----------------------|------------------------------|------------------|---------------------|
| 6001          | 2020-04-10      | Baseline        | N/A             | 18.5                  | NULL      | FALSE                | FALSE                        | 1001             | NULL                |
| 6002          | 2020-06-15      | Post-surgery    | CR              | 0                     | NULL      | FALSE                | FALSE                        | 1002             | NULL                |
| 6003          | 2020-09-01      | Follow-up       | CR              | 0                     | 0.08      | FALSE                | FALSE                        | NULL             | 3002                |
| 6004          | 2021-03-20      | Follow-up       | CR              | 0                     | NULL      | FALSE                | FALSE                        | 1003             | NULL                |
| 6005          | 2022-05-12      | Progression     | PD              | 35.0                  | 12.4      | TRUE                 | TRUE (T790M + MET amp)       | 1004             | 3003                |

---

### 3.1 Why This Table Structure?

#### **Galaxy schema advantages for this case**:

1. **Time-series on multiple dimensions**: Patient NGDX-001 has 4 imaging studies, 2 biopsies, 3 molecular tests, 2 treatments, 5 assessments → separate fact tables prevent column explosion while all link to same Patient dimension

2. **Normalized mutations**: Single NGS test (molecular_result_sk=3003) detected 5 mutations → stored as 5 rows in `fact_mutations` rather than multi-value text field → enables:
   - "Show VAF trend for EGFR Ex19del over time" (query filters `gene_symbol='EGFR' AND mutation_type='Exon 19 deletion'`)
   - "Alert when T790M appears" (query `WHERE mutation_type='T790M' AND resistance_mutation=TRUE`)

3. **Flexible image linking**: Each imaging study and biopsy has file path columns → dashboard can dynamically load DICOM images, pathology slides, PDF reports

4. **Response assessment integration**: `fact_response_assessments` links to BOTH `fact_imaging_studies` (RECIST measurements) AND `fact_molecular_results` (ctDNA VAF) → single query joins radiographic + molecular progression

5. **Cross-process queries**: Galaxy structure enables questions like "Do patients with EGFR Ex19del have better RECIST response than L858R?" by joining Mutation → MolecularTest → Patient → Treatment → ResponseAssessment → ImagingStudy

#### **Do we need further table splits?**

**YES for some cases**:
- **FACT_METASTATIC_SITES**: M-stage "M1b" could have multiple sites (brain + bone + liver) → normalize into separate rows with anatomical location, lesion size
- **FACT_ADVERSE_EVENTS**: Treatment toxicities (Var_088 - ILD, rash, diarrhea) → separate table with date, grade, relationship to drug

**NO for others**:
- Lab panels (FBC, LFTs) could be further normalized (1 row per lab test) but adds complexity with minimal benefit for 100 patients
- Keeping multi-component labs as columns in `fact_clinical_assessments` is acceptable for MVP

---

## 4. Image File Management Strategy

### 4.1 What You Need to Provide for Image Integration

#### **For Imaging (CT/PET/MRI)**:
Provide any of the following:
1. **DICOM files** (.dcm): Raw imaging data
   - Organize as: `/imaging/<patient_id>/<study_date>/series_001/IM-0001-0001.dcm`
2. **Converted images** (PNG/JPG): Pre-rendered axial slices for quick dashboard display
   - Generate: `dcm2niix` or `pydicom` to extract key slices (e.g., slice with largest tumor)
3. **DICOM metadata CSV**: At minimum, provide a CSV with:
   ```
   patient_id, study_uid, study_date, modality, file_path
   NGDX-001, 1.2.840.xxx, 2020-03-10, CT, /imaging/NGDX-001/baseline/
   ```

#### **For Pathology (Histology slides)**:
1. **Whole-slide images** (.svs, .ndpi, .tiff): High-resolution scanned slides
   - Organize as: `/pathology/<patient_id>/<biopsy_date>/slide_01.svs`
2. **Thumbnail images** (PNG/JPG): Low-res previews for dashboard
3. **Pathology reports** (PDF): Original signed-out reports
   - Path: `/pathology/<patient_id>/<biopsy_date>/report.pdf`

#### **For Molecular Testing (NGS reports)**:
1. **VCF files** (.vcf): Variant Call Format with mutation details
   - Path: `/molecular/<patient_id>/<test_date>/variants.vcf`
2. **NGS report PDFs**: FoundationOne CDx / Guardant360 clinical reports
   - Path: `/molecular/<patient_id>/<test_date>/report.pdf`

### 4.2 Minimum Viable Approach (If No Real Images Available)

**For MVP demonstration**:
1. **Add ID columns to tables** (already in schema above):
   - `dicom_file_path`, `thumbnail_image_path` in `fact_imaging_studies`
   - `pathology_slide_image_path`, `pathology_report_pdf_path` in `fact_biopsies`
   - `vcf_file_path`, `ngs_report_pdf_path` in `fact_molecular_results`

2. **Populate with placeholder paths**:
   ```sql
   UPDATE fact_imaging_studies 
   SET dicom_file_path = '/imaging/' || patient_id || '/study_' || scan_date,
       thumbnail_image_path = '/imaging/' || patient_id || '/thumbnails/axial_slice.png';
   ```

3. **Dashboard behavior**:
   - If file exists → display image viewer
   - If file missing → show placeholder: "📄 Imaging available in PACS (Study UID: 1.2.840...)"
   - Provide "View in PACS" button with deep link to hospital PACS system

### 4.3 Recommended File Structure
```
/data/
  /imaging/
    /NGDX-001/
      /2020-03-10_baseline_CT/
        study_metadata.json
        /series_001/
          IM-0001-0001.dcm
          IM-0001-0002.dcm
        /thumbnails/
          axial_slice_largest_tumor.png
      /2022-05-10_progression_PET/
        ...
  /pathology/
    /NGDX-001/
      /2020-03-12_EBUS_biopsy/
        slide_H&E.svs
        slide_thumbnail.jpg
        pathology_report.pdf
  /molecular/
    /NGDX-001/
      /2020-03-14_tissue_NGS/
        FoundationOne_CDx_report.pdf
        variants.vcf
      /2022-05-14_ctDNA_NGS/
        Guardant360_report.pdf
        variants.vcf
```

---

## 5. Dashboard Data Sufficiency Analysis

### 5.1 Required Dashboard Views → Data Dictionary Mapping

#### ✅ **Patient Summary Panel** - SUFFICIENT
| Dashboard Element           | Data Source Variable         | Available in Data Dict? |
|-----------------------------|------------------------------|-------------------------|
| Demographics                | Var_001-004 (NHS#, age, sex) | ✅ Yes                  |
| Diagnosis date              | Var_017                      | ✅ Yes                  |
| Current stage               | Var_030 (AJCC stage)         | ✅ Yes                  |
| Current treatment regimen   | Var_084, 087 (MDT rec, drug) | ✅ Yes                  |
| Line of therapy             | *Inferred from Var_086-089*  | ⚠️ Needs calculation    |
| Latest ECOG                 | Var_009                      | ⚠️ Baseline only        |

**Gap**: ECOG is only captured at baseline (Var_009). For longitudinal ECOG, need to:
- Add ECOG to `fact_clinical_assessments` (already in schema above)
- Source from clinical notes or assume static unless documented change

---

#### ✅ **Molecular Profile Card** - SUFFICIENT
| Dashboard Element           | Data Source Variable              | Available? |
|-----------------------------|-----------------------------------|------------|
| Primary EGFR mutation       | Var_050 (tissue), Var_074 (ctDNA)| ✅ Yes     |
| Co-mutations (TP53, MET)    | Var_050 (multi-value field)       | ✅ Yes     |
| PD-L1 TPS                   | Var_045                           | ✅ Yes     |
| Actionable mutations        | Var_078 (Tier classification)     | ✅ Yes     |

**No gaps** - all data present.

---

#### ✅ **Disease Timeline** - SUFFICIENT
| Dashboard Element               | Data Source Variable                  | Available? |
|---------------------------------|---------------------------------------|------------|
| Diagnosis date                  | Var_017                               | ✅ Yes     |
| Biopsy date                     | Var_020 (scan), inferred for biopsy   | ⚠️ Partial |
| Treatment start date            | Var_089                               | ✅ Yes     |
| Follow-up imaging dates         | Var_020 (multiple scans)              | ⚠️ Needs time-series structure |
| Serial ctDNA VAF                | Var_075 (VAF %)                       | ⚠️ Single timepoint in CSV    |
| RECIST measurements over time   | Var_092 (sum of lesions)              | ⚠️ Single timepoint in CSV    |

**Gap**: Simulated data CSV has **1 row per patient** → no time-series data.

**Solution for MVP**:
1. **Synthetic time-series generation**: For selected patients (e.g., NGDX-001), manually create 3-5 timepoints:
   ```
   Patient NGDX-001:
   - 2020-03-10: Baseline imaging (tumor 18.5mm), no ctDNA
   - 2020-06-15: Post-surgery imaging (tumor 0mm), ctDNA VAF 0.08%
   - 2020-09-01: 6-month follow-up, ctDNA VAF 0.02%
   - 2021-03-20: 12-month follow-up, tumor 0mm, no ctDNA
   - 2022-05-10: Progression imaging (tumor 35mm), ctDNA VAF 12.4%, T790M detected
   ```

2. **Data entry**: Manually insert rows into `fact_imaging_studies`, `fact_molecular_results`, `fact_response_assessments` for these timepoints

---

#### ⚠️ **Treatment Decision Support** - NEEDS CLINICAL GUIDELINE VALIDATION
| Decision Rule                          | Input Variables                     | Available? |
|----------------------------------------|-------------------------------------|------------|
| EGFR Ex19del/L858R + PD-L1 ≥50% → Osi | Var_050 (EGFR) + Var_045 (PD-L1)    | ✅ Yes     |
| T790M at progression → 3rd-gen TKI     | Var_096 (resistance mutation)       | ✅ Yes     |
| Rising ctDNA VAF → flag progression    | Var_075 (VAF) + time-series         | ⚠️ Needs time-series |

**Gap**: Decision rules are **not in the data dictionary** → need external clinical guidelines (see Section 6).

---

#### ✅ **Alert System** - SUFFICIENT (with calculations)
| Alert                           | Logic                                      | Available? |
|---------------------------------|--------------------------------------------|------------|
| Rising ctDNA VAF (≥2x baseline) | Compare Var_075 across timepoints          | ⚠️ Needs time-series |
| New resistance mutation         | Flag new rows in `fact_mutations`          | ✅ Yes (after data entry) |
| Overdue follow-up tests         | Calculate days since last scan (Var_020)   | ✅ Yes (needs scheduling logic) |

**Implementation**: Alert logic will be **calculated in dashboard backend** (not stored in database).

---

### 5.2 Additional Data Needs for MVP

To create a **realistic dashboard prototype**, you need to provide:

1. **Time-series data for 3-5 patients**:
   - Create CSV with columns: `patient_id, timepoint_date, timepoint_type (baseline/follow-up/progression), imaging_study_id, recist_sum_mm, ctdna_vaf, mutations_detected`
   - Example: 5 rows for NGDX-001 (as shown above)

2. **Treatment history for 3-5 patients**:
   - CSV with: `patient_id, treatment_line, drug_name, start_date, end_date, discontinuation_reason`

3. **Optional: Image files** (if you have access):
   - 1-2 CT scans (DICOM or PNG) for patient NGDX-001
   - 1 pathology slide thumbnail
   - 1 NGS report PDF

**If you don't have these**: I can generate synthetic time-series data for 5 patients based on realistic clinical trajectories.

---

## 6. Clinical Decision Rule References

### ⚠️ DISCLAIMER FOR DASHBOARD

**CRITICAL: Display prominently in red banner on all dashboard pages:**

```
🚨 FOR DEMONSTRATION PURPOSES ONLY 🚨
This clinical decision support logic is a simplified mock implementation 
for proof-of-concept demonstration. It is NOT validated for clinical use 
and must NOT be used for real patient care decisions. All treatment 
recommendations should be made by qualified oncologists following current 
evidence-based guidelines.
```

---

### 6.1 First-Line Treatment Selection

#### **Rule 1: EGFR Ex19del/L858R + Stage IV → Osimertinib**
**Source**: 
- **FLAURA trial** (Soria et al., NEJM 2018): Osimertinib vs 1st-gen EGFR TKIs in treatment-naïve EGFR+ NSCLC
  - Reference: doi:10.1056/NEJMoa1713137
  - Result: Osimertinib superior PFS (18.9 mo vs 10.2 mo, HR 0.46)
- **UK NICE Guidance TA653** (2020): Osimertinib recommended for 1st-line EGFR+ advanced NSCLC
  - URL: https://www.nice.org.uk/guidance/ta653
- **ESMO Guidelines** (Hendriks et al., Ann Oncol 2023): EGFR Ex19del/L858R → osimertinib monotherapy (Evidence: I, A)
  - Reference: doi:10.1016/j.annonc.2022.12.009

**Implementation**:
```python
if (mutation_type in ['Exon 19 deletion', 'L858R'] and 
    ajcc_stage in ['IVA', 'IVB']):
    recommend = "Osimertinib 80mg once daily"
    evidence_level = "Level I (RCT)"
    guideline = "NICE TA653, ESMO 2023"
```

#### **Rule 2: PD-L1 ≥50% → Consider osimertinib + chemotherapy**
**Source**:
- **FLAURA2 trial** (Planchard et al., NEJM 2023): Osimertinib + chemo vs osi monotherapy
  - Reference: doi:10.1056/NEJMoa2310388
  - Result: Combination improved PFS (25.5 mo vs 16.7 mo, HR 0.62)
  - **NOTE**: Not yet in UK NICE guidelines as of 2024 → label as "Emerging evidence"

**Implementation**:
```python
if (mutation_type in ['Exon 19 deletion', 'L858R'] and 
    pdl1_tps >= 50 and 
    ajcc_stage in ['IVA', 'IVB'] and
    ecog <= 1):
    recommend = "Consider: Osimertinib + platinum-pemetrexed (FLAURA2 regimen)"
    evidence_level = "Emerging (Phase III, not yet in NICE guidelines)"
    guideline = "FLAURA2 trial 2023 - discuss in MDT"
```

#### **Rule 3: Uncommon EGFR mutations**
**Source**:
- **ESMO Guidelines** (Hendriks et al., 2023): G719X, L861Q, S768I → consider afatinib (Evidence: III, B)
- **LUX-Lung 2/3/6 trials**: Afatinib efficacy in uncommon EGFR mutations
  - Reference: doi:10.1016/S1470-2045(15)00026-1

**Implementation**:
```python
if mutation_type in ['G719X', 'L861Q', 'S768I']:
    recommend = "Consider afatinib 40mg once daily OR clinical trial"
    evidence_level = "Level III (Retrospective)"
    guideline = "ESMO 2023 - weaker evidence than Ex19del/L858R"
```

---

### 6.2 Progression Monitoring Thresholds

#### **Threshold 1: ctDNA VAF ≥2x from nadir → Molecular progression**
**Source**:
- **CHRYSALIS-2 ctDNA substudy** (Rolfo et al., Lung Cancer 2022): ctDNA dynamics predict clinical progression
  - Reference: doi:10.1016/j.lungcan.2022.01.019
  - Finding: ≥2-fold VAF increase preceded radiographic progression by median 3.7 months
- **TRACERx study** (Abbosh et al., Nature 2017): ctDNA detection predicts relapse in early-stage NSCLC
  - Reference: doi:10.1038/nature22364

**Implementation**:
```python
if current_vaf >= 2 * nadir_vaf:
    alert = "⚠️ Molecular progression warning: ctDNA VAF increased ≥2x from nadir"
    action = "Consider repeat imaging in 4-6 weeks (CHRYSALIS-2 precedent)"
    evidence = "Observational study (Rolfo 2022)"
```

#### **Threshold 2: RECIST progressive disease (≥20% increase + ≥5mm absolute)**
**Source**:
- **RECIST 1.1 Guidelines** (Eisenhauer et al., EJC 2009): Standard response criteria
  - Reference: doi:10.1016/j.ejca.2008.10.026
  - PD definition: ≥20% increase in sum of target lesions + ≥5mm absolute increase

**Implementation**:
```python
if (percent_change_from_nadir >= 20 and 
    absolute_increase_mm >= 5) or new_lesions_present:
    alert = "🔴 Radiographic progressive disease (RECIST 1.1)"
    action = "Consider re-biopsy for resistance mechanism"
    evidence = "RECIST 1.1 (Standard criteria)"
```

---

### 6.3 Resistance Detection & Therapy Switching

#### **Rule 1: T790M on 1st/2nd-gen TKI → Switch to osimertinib**
**Source**:
- **AURA3 trial** (Mok et al., NEJM 2017): Osimertinib vs chemo in T790M+ progression
  - Reference: doi:10.1056/NEJMoa1612674
  - Result: Osimertinib PFS 10.1 mo vs 4.4 mo chemo (HR 0.30)
- **UK NICE TA653** (2020): Osimertinib approved for T790M+ NSCLC after progression on 1st-line EGFR TKI

**Implementation**:
```python
if (resistance_mutation == 'T790M' and 
    current_treatment in ['gefitinib', 'erlotinib', 'afatinib']):
    recommend = "Switch to osimertinib 80mg once daily"
    evidence_level = "Level I (RCT)"
    guideline = "AURA3 trial, NICE TA653"
```

#### **Rule 2: C797S on osimertinib → No approved targeted therapy**
**Source**:
- **ORCHARD trial** (Planchard et al., Lancet Oncol 2024): No standard option for C797S
  - Reference: doi:10.1016/S1470-2045(23)00582-8
  - Recommendation: Platinum-doublet chemotherapy OR clinical trial
- **ESMO Guidelines** (Hendriks et al., 2023): C797S → consider platinum-pemetrexed (Evidence: IV, C)

**Implementation**:
```python
if (resistance_mutation == 'C797S' and 
    current_treatment == 'osimertinib'):
    recommend = "No approved targeted therapy. Options: 1) Platinum-pemetrexed, 2) Clinical trial"
    evidence_level = "Expert opinion (Level IV)"
    guideline = "ESMO 2023 - limited evidence"
```

#### **Rule 3: MET amplification → Add MET inhibitor**
**Source**:
- **TATTON trial** (Oxnard et al., JTO 2020): Osimertinib + savolitinib in MET+ EGFR+ NSCLC
  - Reference: doi:10.1016/j.jtho.2020.03.027
  - Result: ORR 64% (MET amplification cohort)
- **GEOMETRY-E1 trial** (Wu et al., Lancet Resp Med 2023): Osimertinib + tepotinib in MET+ EGFR+ NSCLC
  - Reference: doi:10.1016/S2213-2600(23)00306-0
  - Approved in EU (not yet UK) for MET:CEP7 ratio ≥5

**Implementation**:
```python
if (resistance_mutation == 'MET amplification' and 
    met_cep7_ratio >= 5 and 
    current_treatment == 'osimertinib'):
    recommend = "Consider osimertinib + tepotinib (off-label in UK as of 2024)"
    evidence_level = "Level II (Phase II trial)"
    guideline = "GEOMETRY-E1 trial - discuss in MDT"
```

---

### 6.4 Summary Table: Evidence Levels

| Decision Rule                          | Evidence Level       | Primary Reference        | Guideline Status      |
|----------------------------------------|----------------------|--------------------------|-----------------------|
| Ex19del/L858R → Osimertinib            | Level I (RCT)        | FLAURA (NEJM 2018)       | NICE TA653 (approved) |
| T790M → Osimertinib                    | Level I (RCT)        | AURA3 (NEJM 2017)        | NICE TA653 (approved) |
| ctDNA VAF ≥2x → Alert                  | Level III (Obs)      | Rolfo (Lung Cancer 2022) | Not in guidelines     |
| RECIST PD → Re-biopsy                  | Standard criteria    | RECIST 1.1 (EJC 2009)    | Universal standard    |
| C797S → No targeted therapy            | Level IV (Expert op) | ORCHARD (Lancet Onc 2024)| ESMO 2023 (weak)      |
| MET amp → Add tepotinib                | Level II (Phase II)  | GEOMETRY-E1 (2023)       | Not UK-approved       |

---

## 7. Next Steps for Implementation

### Phase 1: Database Setup (Week 1)
1. Generate SQLite schema from detailed tables above
2. Load 100 patients from `simulated_data.csv` into `dim_patient`, `fact_imaging_studies` (baseline only)
3. Create dimension lookup tables (dim_mutations, dim_drugs, dim_tnm_stage)

### Phase 2: Synthetic Time-Series Data (Week 1-2)
1. Select 5 representative patients with different trajectories:
   - Patient 1: Early-stage, surgery + adjuvant osi, no recurrence (boring but realistic)
   - Patient 2: Stage IV, osi 1st-line, durable response >18 months
   - Patient 3: Stage IV, osi 1st-line, progression at 12 months with T790M (easy resistance)
   - Patient 4: Stage IV, osi 1st-line, progression with C797S + MET amp (complex resistance)
   - Patient 5: Stage IV, uncommon mutation (G719X), afatinib, progression without resistance mutation
2. Manually create 4-6 timepoints per patient for imaging, ctDNA, response assessments

### Phase 3: Dashboard Prototype (Week 2-3)
1. Backend: Python FastAPI with SQLite queries
2. Frontend: React or Streamlit (faster prototyping)
3. Views:
   - Patient selector dropdown
   - Molecular profile card (current mutations, PD-L1)
   - Disease timeline (Plotly scatter plot: x-axis=date, y-axis=VAF, overlays=imaging)
   - Treatment decision support (rule-based logic from Section 6)
   - Alert panel (calculated: VAF trends, overdue tests)

### Phase 4: Image Integration (Optional, Week 3-4)
1. If images available: DICOM viewer integration (OHIF, Cornerstone.js)
2. If not: Placeholder UI with "View in PACS" buttons

---

## 8. Implementation Decisions

### 8.1 Time-Series Data Strategy
**Decision**: Generate synthetic longitudinal data for 5 representative patients.

**Storage Location**: `example_files/mock_simulated/` directory
- Structure: Separate CSV files for each fact table with time-series data
- Files:
  - `example_files/mock_simulated/imaging_studies_timeseries.csv`
  - `example_files/mock_simulated/molecular_results_timeseries.csv`
  - `example_files/mock_simulated/mutations_timeseries.csv`
  - `example_files/mock_simulated/treatments_timeseries.csv`
  - `example_files/mock_simulated/response_assessments_timeseries.csv`
  - `example_files/mock_simulated/clinical_assessments_timeseries.csv`

### 8.2 Image Files Approach
**Decision**: No real image files available for MVP.

**Implementation**:
- Keep all image reference columns in database schema (`dicom_file_path`, `pathology_slide_image_path`, etc.)
- Populate with mock file paths (e.g., `/imaging/NGDX-001/2020-03-10/study.dcm`)
- Dashboard displays placeholder message when image is requested:
  ```
  📄 Imaging Study Available
  Study UID: 1.2.840.113619.2.xxx
  Modality: CT Chest with contrast
  Date: 2020-03-10
  
  [In production: DICOM viewer would display here]
  View in PACS System →
  ```

### 8.3 Clinical Validation
**Decision**: Skip clinical validation for MVP demonstration.

**Implementation**:
- Display prominent red banner disclaimer on all dashboard pages (as specified in Section 6)
- Include evidence levels and references for transparency
- Label rules derived from trials vs. expert opinion

### 8.4 Technology Stack
**Decision**: React frontend + FastAPI backend

**Stack Details**:
- **Backend**: 
  - Python 3.13+ with FastAPI
  - SQLite database
  - SQLAlchemy ORM
  - Pydantic models for API contracts
  
- **Frontend**:
  - React 18+ with TypeScript
  - Vite for build tooling
  - TanStack Query (React Query) for data fetching
  - Recharts or Plotly.js for time-series visualizations
  - Tailwind CSS for styling

- **Deployment**: 
  - Localhost only (http://localhost:3000 frontend, http://localhost:8000 backend)
  - No authentication/RBAC for MVP
  - CORS enabled for local development

### 8.5 Project Structure
```
link_ml/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── database.py          # SQLite connection
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── crud.py              # Database queries
│   │   ├── api/
│   │   │   ├── patients.py      # Patient endpoints
│   │   │   ├── imaging.py       # Imaging endpoints
│   │   │   ├── molecular.py     # Molecular results endpoints
│   │   │   └── decisions.py     # Clinical decision rules
│   │   └── utils/
│   │       └── clinical_rules.py # Treatment decision logic
│   ├── requirements.txt
│   └── clinical_data.db         # SQLite database file
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── PatientSummary.tsx
│   │   │   ├── MolecularProfile.tsx
│   │   │   ├── DiseaseTimeline.tsx
│   │   │   ├── TreatmentDecisions.tsx
│   │   │   └── AlertPanel.tsx
│   │   ├── api/
│   │   │   └── client.ts        # API client functions
│   │   └── types/
│   │       └── index.ts         # TypeScript types
│   ├── package.json
│   └── vite.config.ts
├── example_files/                # All data files
│   ├── data_dictionary.csv       # Original data dictionary
│   ├── simulated_data.csv        # 100 baseline patients
│   └── mock_simulated/           # Synthetic time-series data
│       ├── imaging_studies_timeseries.csv
│       ├── molecular_results_timeseries.csv
│       ├── mutations_timeseries.csv
│       ├── treatments_timeseries.csv
│       ├── response_assessments_timeseries.csv
│       └── clinical_assessments_timeseries.csv
├── scripts/
│   ├── create_schema.py         # Generate SQLite schema
│   ├── load_baseline_data.py    # Load 100 patients from simulated_data.csv
│   ├── generate_timeseries.py   # Create synthetic longitudinal data
│   └── populate_dimensions.py   # Populate lookup tables
└── SYSTEM_SPEC.md               # This file (source of truth)
```

---

## 9. Development Roadmap

### Phase 1: Database Foundation (Days 1-2)
1. ✅ Finalize schema design (COMPLETE)
2. Create `scripts/create_schema.py` - Generate SQLite database with all tables
3. Create `scripts/populate_dimensions.py` - Load lookup tables (dim_mutations, dim_drugs, etc.)
4. Create `scripts/load_baseline_data.py` - Load 100 patients from `simulated_data.csv`
5. Verify: Query database to confirm 100 patients loaded with baseline data

### Phase 2: Synthetic Time-Series Generation (Days 2-3)
1. Create `scripts/generate_timeseries.py` with 5 patient trajectories:
   - **NGDX-001**: Stage IA1 → Surgery → Adjuvant osi → Progression with T790M + MET amp (26 months)
   - **NGDX-015**: Stage IVA → Osi 1st-line → Durable response (18+ months, ongoing)
   - **NGDX-033**: Stage IVB → Osi 1st-line → Progression with T790M (12 months) → Osi 2nd-line
   - **NGDX-047**: Stage IVA → Osi 1st-line → Progression with C797S (15 months) → Chemo
   - **NGDX-082**: Stage IIIC uncommon mutation (G719X) → Afatinib → Progression (9 months)
2. Generate 4-6 timepoints per patient for each fact table
3. Save to `example_files/mock_simulated/` directory as CSV files
4. Load time-series data into database
5. Verify: Query NGDX-001 to see complete longitudinal record

### Phase 3: Backend API (Days 3-5)
1. Setup FastAPI project structure in `backend/`
2. Create SQLAlchemy models matching database schema
3. Implement API endpoints:
   - `GET /api/patients` - List all patients
   - `GET /api/patients/{patient_id}` - Patient summary
   - `GET /api/patients/{patient_id}/imaging` - Imaging timeline
   - `GET /api/patients/{patient_id}/molecular` - Molecular results + mutations
   - `GET /api/patients/{patient_id}/treatments` - Treatment history
   - `GET /api/patients/{patient_id}/response` - Response assessments
   - `GET /api/patients/{patient_id}/timeline` - Integrated timeline for charts
   - `GET /api/patients/{patient_id}/decisions` - Treatment recommendations (calculated)
   - `GET /api/patients/{patient_id}/alerts` - Active alerts (calculated)
4. Implement clinical decision rules in `utils/clinical_rules.py`
5. Test all endpoints with Postman/curl

### Phase 4: Frontend Dashboard (Days 5-8)
1. Setup React + Vite project in `frontend/`
2. Create API client with TanStack Query
3. Implement components:
   - **DisclaimerBanner** (red warning - always visible)
   - **PatientSelector** (dropdown list of 5 patients with time-series data)
   - **PatientSummary** (demographics, current stage, ECOG, treatment)
   - **MolecularProfile** (EGFR mutation, co-mutations, PD-L1, actionable mutations)
   - **DiseaseTimeline** (Recharts line chart: x=date, y=VAF, overlay=imaging markers)
   - **TreatmentDecisions** (rule-based recommendations with evidence levels)
   - **AlertPanel** (rising VAF, new resistance, overdue tests)
   - **ImagePlaceholder** (mock display for imaging/pathology references)
4. Style with Tailwind CSS
5. Connect frontend to backend API

### Phase 5: Integration Testing (Days 8-9)
1. Test all 5 patients across all dashboard views
2. Verify time-series charts render correctly
3. Verify clinical decision rules trigger appropriately
4. Test image placeholders display correct metadata
5. Check alert calculations (VAF trends, overdue tests)

### Phase 6: Documentation (Day 9-10)
1. Create `README.md` with:
   - Setup instructions (install dependencies, run backend, run frontend)
   - API endpoint documentation
   - Database schema diagram
   - Clinical decision rule references
2. Create demo video/screenshots
3. Document known limitations

---

## 10. Success Criteria for MVP

1. ✅ **Database**: SQLite with complete galaxy schema, 100 baseline patients + 5 patients with time-series data
2. ✅ **API**: All endpoints functional, clinical rules implemented with references
3. ✅ **Dashboard**: All 6 views operational for 5 time-series patients
4. ✅ **Visualization**: Disease timeline chart shows VAF trends + imaging overlays
5. ✅ **Decision Support**: Treatment recommendations display with evidence levels and guideline references
6. ✅ **Alerts**: Active alerts calculate correctly (VAF trends, resistance mutations)
7. ✅ **Disclaimer**: Red banner visible on all pages

---

## Next Action

**Immediate next step**: Create database schema and load baseline data.

Command to begin:
```bash
# Create directories
mkdir -p scripts example_files/mock_simulated backend frontend

# Start with schema creation
python scripts/create_schema.py
```

Ready to proceed with Phase 1?