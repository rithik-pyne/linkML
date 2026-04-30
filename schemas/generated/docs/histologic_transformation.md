

# Slot: histologic_transformation 



URI: [clinical_model:histologic_transformation](https://uk-cpi.com/clinical_model/histologic_transformation)
Alias: histologic_transformation

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
| self | clinical_model:histologic_transformation |
| native | clinical_model:histologic_transformation |




## LinkML Source

<details>
```yaml
name: histologic_transformation
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: histologic_transformation
domain_of:
- ResponseAssessment
range: boolean

```
</details>