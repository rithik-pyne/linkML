

# Slot: specimen_type 



URI: [clinical_model:specimen_type](https://uk-cpi.com/clinical_model/specimen_type)
Alias: specimen_type

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Biopsy](Biopsy.md) | Tissue or liquid biopsy procedure - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [SpecimenTypeEnum](SpecimenTypeEnum.md) |
| Domain Of | [Biopsy](Biopsy.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:specimen_type |
| native | clinical_model:specimen_type |




## LinkML Source

<details>
```yaml
name: specimen_type
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: specimen_type
domain_of:
- Biopsy
range: SpecimenTypeEnum

```
</details>