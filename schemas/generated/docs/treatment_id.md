

# Slot: treatment_id 



URI: [clinical_model:treatment_id](https://uk-cpi.com/clinical_model/treatment_id)
Alias: treatment_id

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  yes  |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Treatment](Treatment.md) |
| Domain Of | [Treatment](Treatment.md), [ResponseAssessment](ResponseAssessment.md) |

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
| self | clinical_model:treatment_id |
| native | clinical_model:treatment_id |




## LinkML Source

<details>
```yaml
name: treatment_id
from_schema: https://ngdx.org/clinical_model
rank: 1000
identifier: true
alias: treatment_id
domain_of:
- Treatment
- ResponseAssessment
range: Treatment
required: true

```
</details>