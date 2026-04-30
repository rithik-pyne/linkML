

# Slot: clinical_assessment_id 



URI: [clinical_model:clinical_assessment_id](https://uk-cpi.com/clinical_model/clinical_assessment_id)
Alias: clinical_assessment_id

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ClinicalAssessment](ClinicalAssessment.md) | Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patie... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ClinicalAssessment](ClinicalAssessment.md) |
| Domain Of | [ClinicalAssessment](ClinicalAssessment.md) |

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
| self | clinical_model:clinical_assessment_id |
| native | clinical_model:clinical_assessment_id |




## LinkML Source

<details>
```yaml
name: clinical_assessment_id
from_schema: https://ngdx.org/clinical_model
rank: 1000
identifier: true
alias: clinical_assessment_id
domain_of:
- ClinicalAssessment
range: ClinicalAssessment
required: true

```
</details>