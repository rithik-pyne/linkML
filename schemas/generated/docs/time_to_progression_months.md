

# Slot: time_to_progression_months 



URI: [clinical_model:time_to_progression_months](https://uk-cpi.com/clinical_model/time_to_progression_months)
Alias: time_to_progression_months

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [ResponseAssessment](ResponseAssessment.md) |

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
| self | clinical_model:time_to_progression_months |
| native | clinical_model:time_to_progression_months |




## LinkML Source

<details>
```yaml
name: time_to_progression_months
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: time_to_progression_months
domain_of:
- ResponseAssessment
range: float
minimum_value: 0

```
</details>