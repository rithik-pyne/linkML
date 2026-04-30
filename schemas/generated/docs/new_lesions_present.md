

# Slot: new_lesions_present 



URI: [clinical_model:new_lesions_present](https://uk-cpi.com/clinical_model/new_lesions_present)
Alias: new_lesions_present

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
| self | clinical_model:new_lesions_present |
| native | clinical_model:new_lesions_present |




## LinkML Source

<details>
```yaml
name: new_lesions_present
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: new_lesions_present
domain_of:
- ResponseAssessment
range: boolean

```
</details>