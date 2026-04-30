

# Slot: diagnosis_date 



URI: [clinical_model:diagnosis_date](https://uk-cpi.com/clinical_model/diagnosis_date)
Alias: diagnosis_date

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Patient](Patient.md) | Core patient entity with demographics and baseline clinical data |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Date](Date.md) |
| Domain Of | [Patient](Patient.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:diagnosis_date |
| native | clinical_model:diagnosis_date |




## LinkML Source

<details>
```yaml
name: diagnosis_date
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: diagnosis_date
domain_of:
- Patient
range: date
required: true

```
</details>