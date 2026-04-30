

# Slot: gene_symbol 



URI: [clinical_model:gene_symbol](https://uk-cpi.com/clinical_model/gene_symbol)
Alias: gene_symbol

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
| Required | Yes |
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^[A-Z0-9-]+$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:gene_symbol |
| native | clinical_model:gene_symbol |




## LinkML Source

<details>
```yaml
name: gene_symbol
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: gene_symbol
domain_of:
- Mutation
range: string
required: true
pattern: ^[A-Z0-9-]+$

```
</details>