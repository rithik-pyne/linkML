

# Slot: mutation_id 



URI: [clinical_model:mutation_id](https://uk-cpi.com/clinical_model/mutation_id)
Alias: mutation_id

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Mutation](Mutation.md) | Individual genomic variant detected in NGS test - normalized to enable time-s... |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
| Domain Of | [Mutation](Mutation.md) |

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
| self | clinical_model:mutation_id |
| native | clinical_model:mutation_id |




## LinkML Source

<details>
```yaml
name: mutation_id
from_schema: https://ngdx.org/clinical_model
rank: 1000
identifier: true
alias: mutation_id
domain_of:
- Mutation
range: string
required: true

```
</details>