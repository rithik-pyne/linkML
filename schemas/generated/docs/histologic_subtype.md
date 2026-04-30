

# Slot: histologic_subtype 



URI: [clinical_model:histologic_subtype](https://uk-cpi.com/clinical_model/histologic_subtype)
Alias: histologic_subtype

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
| self | clinical_model:histologic_subtype |
| native | clinical_model:histologic_subtype |




## LinkML Source

<details>
```yaml
name: histologic_subtype
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: histologic_subtype
domain_of:
- Biopsy
range: string

```
</details>