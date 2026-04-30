

# Slot: tissue_sufficiency 



URI: [clinical_model:tissue_sufficiency](https://uk-cpi.com/clinical_model/tissue_sufficiency)
Alias: tissue_sufficiency

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
| self | clinical_model:tissue_sufficiency |
| native | clinical_model:tissue_sufficiency |




## LinkML Source

<details>
```yaml
name: tissue_sufficiency
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: tissue_sufficiency
domain_of:
- Biopsy
range: string

```
</details>