

# Slot: assessment_type 



URI: [clinical_model:assessment_type](https://uk-cpi.com/clinical_model/assessment_type)
Alias: assessment_type

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [AssessmentTypeEnum](AssessmentTypeEnum.md) |
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
| self | clinical_model:assessment_type |
| native | clinical_model:assessment_type |




## LinkML Source

<details>
```yaml
name: assessment_type
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: assessment_type
domain_of:
- ResponseAssessment
range: AssessmentTypeEnum

```
</details>