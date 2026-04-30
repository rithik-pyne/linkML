

# Slot: progression_type 



URI: [clinical_model:progression_type](https://uk-cpi.com/clinical_model/progression_type)
Alias: progression_type

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ProgressionTypeEnum](ProgressionTypeEnum.md) |
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
| self | clinical_model:progression_type |
| native | clinical_model:progression_type |




## LinkML Source

<details>
```yaml
name: progression_type
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: progression_type
domain_of:
- ResponseAssessment
range: ProgressionTypeEnum

```
</details>