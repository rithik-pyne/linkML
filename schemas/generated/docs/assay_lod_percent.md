

# Slot: assay_lod_percent 



URI: [clinical_model:assay_lod_percent](https://uk-cpi.com/clinical_model/assay_lod_percent)
Alias: assay_lod_percent

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MolecularTest](MolecularTest.md) | NGS test from tissue or ctDNA - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [MolecularTest](MolecularTest.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |
| Maximum Value | 100 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:assay_lod_percent |
| native | clinical_model:assay_lod_percent |




## LinkML Source

<details>
```yaml
name: assay_lod_percent
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: assay_lod_percent
domain_of:
- MolecularTest
range: float
minimum_value: 0
maximum_value: 100

```
</details>