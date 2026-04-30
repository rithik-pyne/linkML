

# Slot: diagnosis_pathway 



URI: [clinical_model:diagnosis_pathway](https://uk-cpi.com/clinical_model/diagnosis_pathway)
Alias: diagnosis_pathway

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










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:diagnosis_pathway |
| native | clinical_model:diagnosis_pathway |




## LinkML Source

<details>
```yaml
name: diagnosis_pathway
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: diagnosis_pathway
domain_of:
- Patient
range: string

```
</details>