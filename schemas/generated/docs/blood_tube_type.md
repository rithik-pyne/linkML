

# Slot: blood_tube_type 



URI: [clinical_model:blood_tube_type](https://uk-cpi.com/clinical_model/blood_tube_type)
Alias: blood_tube_type

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Biopsy](Biopsy.md) | Tissue or liquid biopsy procedure - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
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
| self | clinical_model:blood_tube_type |
| native | clinical_model:blood_tube_type |




## LinkML Source

<details>
```yaml
name: blood_tube_type
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: blood_tube_type
domain_of:
- Biopsy
range: string

```
</details>