

# Slot: sum_target_lesions_mm 



URI: [clinical_model:sum_target_lesions_mm](https://uk-cpi.com/clinical_model/sum_target_lesions_mm)
Alias: sum_target_lesions_mm

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
| Maximum Value | 500 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:sum_target_lesions_mm |
| native | clinical_model:sum_target_lesions_mm |




## LinkML Source

<details>
```yaml
name: sum_target_lesions_mm
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: sum_target_lesions_mm
domain_of:
- ResponseAssessment
range: float
minimum_value: 0
maximum_value: 500

```
</details>