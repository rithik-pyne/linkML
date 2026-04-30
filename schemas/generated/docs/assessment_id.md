

# Slot: assessment_id 



URI: [clinical_model:assessment_id](https://uk-cpi.com/clinical_model/assessment_id)
Alias: assessment_id

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ResponseAssessment](ResponseAssessment.md) |
| Domain Of | [ResponseAssessment](ResponseAssessment.md) |

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
| self | clinical_model:assessment_id |
| native | clinical_model:assessment_id |




## LinkML Source

<details>
```yaml
name: assessment_id
from_schema: https://ngdx.org/clinical_model
rank: 1000
identifier: true
alias: assessment_id
domain_of:
- ResponseAssessment
range: ResponseAssessment
required: true

```
</details>