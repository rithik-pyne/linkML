

# Slot: symptom_severity_grade 



URI: [clinical_model:symptom_severity_grade](https://uk-cpi.com/clinical_model/symptom_severity_grade)
Alias: symptom_severity_grade

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ClinicalAssessment](ClinicalAssessment.md) | Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patie... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](Integer.md) |
| Domain Of | [ClinicalAssessment](ClinicalAssessment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |
| Maximum Value | 5 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:symptom_severity_grade |
| native | clinical_model:symptom_severity_grade |




## LinkML Source

<details>
```yaml
name: symptom_severity_grade
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: symptom_severity_grade
domain_of:
- ClinicalAssessment
range: integer
minimum_value: 0
maximum_value: 5

```
</details>