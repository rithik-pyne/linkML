

# Slot: tissue_specimen_category 



URI: [clinical_model:tissue_specimen_category](https://uk-cpi.com/clinical_model/tissue_specimen_category)
Alias: tissue_specimen_category

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
| self | clinical_model:tissue_specimen_category |
| native | clinical_model:tissue_specimen_category |




## LinkML Source

<details>
```yaml
name: tissue_specimen_category
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: tissue_specimen_category
domain_of:
- Biopsy
range: string

```
</details>