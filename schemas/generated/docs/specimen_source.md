

# Slot: specimen_source 



URI: [clinical_model:specimen_source](https://uk-cpi.com/clinical_model/specimen_source)
Alias: specimen_source

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MolecularTest](MolecularTest.md) | NGS test from tissue or ctDNA - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [SpecimenSourceEnum](SpecimenSourceEnum.md) |
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
| self | clinical_model:specimen_source |
| native | clinical_model:specimen_source |




## LinkML Source

<details>
```yaml
name: specimen_source
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: specimen_source
domain_of:
- MolecularTest
range: SpecimenSourceEnum

```
</details>