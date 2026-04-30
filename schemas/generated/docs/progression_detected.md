

# Slot: progression_detected 



URI: [clinical_model:progression_detected](https://uk-cpi.com/clinical_model/progression_detected)
Alias: progression_detected

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Boolean](Boolean.md) |
| Domain Of | [ResponseAssessment](ResponseAssessment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:progression_detected |
| native | clinical_model:progression_detected |




## LinkML Source

<details>
```yaml
name: progression_detected
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: progression_detected
domain_of:
- ResponseAssessment
range: boolean

```
</details>