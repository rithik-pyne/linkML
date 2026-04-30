

# Slot: mutation_type 



URI: [clinical_model:mutation_type](https://uk-cpi.com/clinical_model/mutation_type)
Alias: mutation_type

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










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:mutation_type |
| native | clinical_model:mutation_type |




## LinkML Source

<details>
```yaml
name: mutation_type
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: mutation_type
domain_of:
- Mutation
range: string

```
</details>