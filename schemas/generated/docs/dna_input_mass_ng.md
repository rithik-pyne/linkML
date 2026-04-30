

# Slot: dna_input_mass_ng 



URI: [clinical_model:dna_input_mass_ng](https://uk-cpi.com/clinical_model/dna_input_mass_ng)
Alias: dna_input_mass_ng

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
| self | clinical_model:dna_input_mass_ng |
| native | clinical_model:dna_input_mass_ng |




## LinkML Source

<details>
```yaml
name: dna_input_mass_ng
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: dna_input_mass_ng
domain_of:
- MolecularTest
range: float
minimum_value: 0

```
</details>