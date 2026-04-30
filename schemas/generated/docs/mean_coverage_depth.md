

# Slot: mean_coverage_depth 



URI: [clinical_model:mean_coverage_depth](https://uk-cpi.com/clinical_model/mean_coverage_depth)
Alias: mean_coverage_depth

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












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:mean_coverage_depth |
| native | clinical_model:mean_coverage_depth |




## LinkML Source

<details>
```yaml
name: mean_coverage_depth
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: mean_coverage_depth
domain_of:
- MolecularTest
range: float
minimum_value: 0

```
</details>