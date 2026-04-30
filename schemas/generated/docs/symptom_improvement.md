

# Slot: symptom_improvement 



URI: [clinical_model:symptom_improvement](https://uk-cpi.com/clinical_model/symptom_improvement)
Alias: symptom_improvement

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
| self | clinical_model:symptom_improvement |
| native | clinical_model:symptom_improvement |




## LinkML Source

<details>
```yaml
name: symptom_improvement
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: symptom_improvement
domain_of:
- ResponseAssessment
range: boolean

```
</details>