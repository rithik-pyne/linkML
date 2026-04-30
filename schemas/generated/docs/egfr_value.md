

# Slot: egfr_value 



URI: [clinical_model:egfr_value](https://uk-cpi.com/clinical_model/egfr_value)
Alias: egfr_value

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ClinicalAssessment](ClinicalAssessment.md) | Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patie... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [ClinicalAssessment](ClinicalAssessment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |
| Maximum Value | 200 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:egfr_value |
| native | clinical_model:egfr_value |




## LinkML Source

<details>
```yaml
name: egfr_value
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: egfr_value
domain_of:
- ClinicalAssessment
range: float
minimum_value: 0
maximum_value: 200

```
</details>