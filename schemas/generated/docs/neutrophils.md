

# Slot: neutrophils 



URI: [clinical_model:neutrophils](https://uk-cpi.com/clinical_model/neutrophils)
Alias: neutrophils

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












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:neutrophils |
| native | clinical_model:neutrophils |




## LinkML Source

<details>
```yaml
name: neutrophils
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: neutrophils
domain_of:
- ClinicalAssessment
range: float
minimum_value: 0

```
</details>