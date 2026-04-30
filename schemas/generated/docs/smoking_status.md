

# Slot: smoking_status 



URI: [clinical_model:smoking_status](https://uk-cpi.com/clinical_model/smoking_status)
Alias: smoking_status

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Patient](Patient.md) | Core patient entity with demographics and baseline clinical data |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [SmokingStatusEnum](SmokingStatusEnum.md) |
| Domain Of | [Patient](Patient.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:smoking_status |
| native | clinical_model:smoking_status |




## LinkML Source

<details>
```yaml
name: smoking_status
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: smoking_status
domain_of:
- Patient
range: SmokingStatusEnum

```
</details>