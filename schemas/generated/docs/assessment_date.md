

# Slot: assessment_date 



URI: [clinical_model:assessment_date](https://uk-cpi.com/clinical_model/assessment_date)
Alias: assessment_date

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ClinicalAssessment](ClinicalAssessment.md) | Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patie... |  no  |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Date](Date.md) |
| Domain Of | [ResponseAssessment](ResponseAssessment.md), [ClinicalAssessment](ClinicalAssessment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:assessment_date |
| native | clinical_model:assessment_date |




## LinkML Source

<details>
```yaml
name: assessment_date
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: assessment_date
domain_of:
- ResponseAssessment
- ClinicalAssessment
range: date
required: true

```
</details>