

# Slot: patient_id 



URI: [clinical_model:patient_id](https://uk-cpi.com/clinical_model/patient_id)
Alias: patient_id

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  yes  |
| [ClinicalAssessment](ClinicalAssessment.md) | Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patie... |  yes  |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  yes  |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  yes  |
| [Biopsy](Biopsy.md) | Tissue or liquid biopsy procedure - multiple rows per patient |  yes  |
| [Patient](Patient.md) | Core patient entity with demographics and baseline clinical data |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Patient](Patient.md) |
| Domain Of | [Patient](Patient.md), [Biopsy](Biopsy.md), [Treatment](Treatment.md), [ResponseAssessment](ResponseAssessment.md), [ClinicalAssessment](ClinicalAssessment.md), [ImagingStudy](ImagingStudy.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |


### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^NGDX-[0-9]{3}$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:patient_id |
| native | clinical_model:patient_id |




## LinkML Source

<details>
```yaml
name: patient_id
from_schema: https://ngdx.org/clinical_model
rank: 1000
identifier: true
alias: patient_id
domain_of:
- Patient
- Biopsy
- Treatment
- ResponseAssessment
- ClinicalAssessment
- ImagingStudy
range: Patient
required: true
pattern: ^NGDX-[0-9]{3}$

```
</details>