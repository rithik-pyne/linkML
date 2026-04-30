

# Slot: mutation_hgvs 



URI: [clinical_model:mutation_hgvs](https://uk-cpi.com/clinical_model/mutation_hgvs)
Alias: mutation_hgvs

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Mutation](Mutation.md) | Individual genomic variant detected in NGS test - normalized to enable time-s... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [Mutation](Mutation.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^[cp]\..+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:mutation_hgvs |
| native | clinical_model:mutation_hgvs |




## LinkML Source

<details>
```yaml
name: mutation_hgvs
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: mutation_hgvs
domain_of:
- Mutation
range: string
pattern: ^[cp]\..+$

```
</details>