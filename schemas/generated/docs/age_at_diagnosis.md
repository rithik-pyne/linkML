

# Slot: age_at_diagnosis 



URI: [clinical_model:age_at_diagnosis](https://uk-cpi.com/clinical_model/age_at_diagnosis)
Alias: age_at_diagnosis

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Patient](Patient.md) | Core patient entity with demographics and baseline clinical data |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](Integer.md) |
| Domain Of | [Patient](Patient.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |
| Maximum Value | 130 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:age_at_diagnosis |
| native | clinical_model:age_at_diagnosis |




## LinkML Source

<details>
```yaml
name: age_at_diagnosis
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: age_at_diagnosis
domain_of:
- Patient
range: integer
minimum_value: 0
maximum_value: 130

```
</details>