

# Slot: resistance_mutation_detected 



URI: [clinical_model:resistance_mutation_detected](https://uk-cpi.com/clinical_model/resistance_mutation_detected)
Alias: resistance_mutation_detected

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
| self | clinical_model:resistance_mutation_detected |
| native | clinical_model:resistance_mutation_detected |




## LinkML Source

<details>
```yaml
name: resistance_mutation_detected
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: resistance_mutation_detected
domain_of:
- ResponseAssessment
range: boolean

```
</details>