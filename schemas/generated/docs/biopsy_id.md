

# Slot: biopsy_id 



URI: [clinical_model:biopsy_id](https://uk-cpi.com/clinical_model/biopsy_id)
Alias: biopsy_id

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Biopsy](Biopsy.md) | Tissue or liquid biopsy procedure - multiple rows per patient |  yes  |
| [MolecularTest](MolecularTest.md) | NGS test from tissue or ctDNA - multiple rows per patient |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Biopsy](Biopsy.md) |
| Domain Of | [Biopsy](Biopsy.md), [MolecularTest](MolecularTest.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:biopsy_id |
| native | clinical_model:biopsy_id |




## LinkML Source

<details>
```yaml
name: biopsy_id
from_schema: https://ngdx.org/clinical_model
rank: 1000
identifier: true
alias: biopsy_id
domain_of:
- Biopsy
- MolecularTest
range: Biopsy
required: true

```
</details>