

# Slot: nhs_number 



URI: [clinical_model:nhs_number](https://uk-cpi.com/clinical_model/nhs_number)
Alias: nhs_number

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Patient](Patient.md) | Core patient entity with demographics and baseline clinical data |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [Patient](Patient.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^[0-9]{10}$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:nhs_number |
| native | clinical_model:nhs_number |




## LinkML Source

<details>
```yaml
name: nhs_number
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: nhs_number
domain_of:
- Patient
range: string
required: true
pattern: ^[0-9]{10}$

```
</details>