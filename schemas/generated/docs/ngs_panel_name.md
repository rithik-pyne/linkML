

# Slot: ngs_panel_name 



URI: [clinical_model:ngs_panel_name](https://uk-cpi.com/clinical_model/ngs_panel_name)
Alias: ngs_panel_name

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MolecularTest](MolecularTest.md) | NGS test from tissue or ctDNA - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [MolecularTest](MolecularTest.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:ngs_panel_name |
| native | clinical_model:ngs_panel_name |




## LinkML Source

<details>
```yaml
name: ngs_panel_name
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: ngs_panel_name
domain_of:
- MolecularTest
range: string

```
</details>