

# Slot: imaging_study_id 



URI: [clinical_model:imaging_study_id](https://uk-cpi.com/clinical_model/imaging_study_id)
Alias: imaging_study_id

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  yes  |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ImagingStudy](ImagingStudy.md) |
| Domain Of | [ResponseAssessment](ResponseAssessment.md), [ImagingStudy](ImagingStudy.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:imaging_study_id |
| native | clinical_model:imaging_study_id |




## LinkML Source

<details>
```yaml
name: imaging_study_id
from_schema: https://ngdx.org/clinical_model
rank: 1000
identifier: true
alias: imaging_study_id
domain_of:
- ResponseAssessment
- ImagingStudy
range: ImagingStudy
required: true

```
</details>