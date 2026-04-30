

# Slot: ecog_status 



URI: [clinical_model:ecog_status](https://uk-cpi.com/clinical_model/ecog_status)
Alias: ecog_status

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ClinicalAssessment](ClinicalAssessment.md) | Longitudinal clinical status (ECOG, symptoms, labs) - multiple rows per patie... |  yes  |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](Integer.md) |
| Domain Of | [ResponseAssessment](ResponseAssessment.md), [ClinicalAssessment](ClinicalAssessment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |
| Maximum Value | 5 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:ecog_status |
| native | clinical_model:ecog_status |




## LinkML Source

<details>
```yaml
name: ecog_status
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: ecog_status
domain_of:
- ResponseAssessment
- ClinicalAssessment
range: integer
minimum_value: 0
maximum_value: 5

```
</details>