

# Slot: sex 



URI: [clinical_model:sex](https://uk-cpi.com/clinical_model/sex)
Alias: sex

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Patient](Patient.md) | Core patient entity with demographics and baseline clinical data |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [SexEnum](SexEnum.md) |
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
| self | clinical_model:sex |
| native | clinical_model:sex |




## LinkML Source

<details>
```yaml
name: sex
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: sex
domain_of:
- Patient
range: SexEnum

```
</details>