# Table Reference

## Tables by Domain

### Dimensions (Conformed)
- **Patient** - Core patient demographics and baseline clinical data
- **Treatment** - Treatment lines and drug regimens

### Source Facts (Event Tables)
- **Biopsy** - Tissue/liquid biopsy procedures and pathology results
- **MolecularTest** - NGS test runs and sequencing metadata
- **ImagingStudy** - Radiology scans (CT/PET) and staging data
- **Mutation** - Genomic variants detected per NGS test

### Assessment Facts (Response Tables)
- **ClinicalAssessment** - Clinic visits with labs and ECOG scores
- **ImagingResponse** - RECIST assessments linked to imaging studies
- **MolecularResponse** - ctDNA response tracking linked to molecular tests
- **ClinicalResponse** - Clinical outcome events (progression/resistance)

---

## Hierarchy & Relationships

```
Patient (1)
├─→ Biopsy (many)
│   └─→ MolecularTest (many)
│       ├─→ Mutation (many)
│       └─→ MolecularResponse (1:1)
├─→ ImagingStudy (many)
│   └─→ ImagingResponse (1:1)
├─→ Treatment (many)
│   ├─→ ImagingResponse (many, optional)
│   ├─→ MolecularResponse (many, optional)
│   └─→ ClinicalResponse (many, optional)
├─→ ClinicalAssessment (many)
└─→ ClinicalResponse (many)
```

### Cardinality Notes
- **1:1** - One source record → one response record (ImagingStudy→ImagingResponse, MolecularTest→MolecularResponse)
- **1:many** - Patient has many events; Treatment has many responses
- **Optional** - Response tables can have NULL treatment_id (pre-treatment baselines)