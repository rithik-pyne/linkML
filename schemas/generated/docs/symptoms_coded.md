

# Slot: symptoms_coded 



URI: [clinical_model:symptoms_coded](https://uk-cpi.com/clinical_model/symptoms_coded)
Alias: symptoms_coded

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
| self | clinical_model:symptoms_coded |
| native | clinical_model:symptoms_coded |




## LinkML Source

<details>
```yaml
name: symptoms_coded
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: symptoms_coded
domain_of:
- ClinicalAssessment
range: string

```
</details>