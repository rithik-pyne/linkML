

# Slot: visit_type 



URI: [clinical_model:visit_type](https://uk-cpi.com/clinical_model/visit_type)
Alias: visit_type

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ClinicalAssessment](ClinicalAssessment.md) | Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patie... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [ClinicalAssessment](ClinicalAssessment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:visit_type |
| native | clinical_model:visit_type |




## LinkML Source

<details>
```yaml
name: visit_type
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: visit_type
domain_of:
- ClinicalAssessment
range: string

```
</details>