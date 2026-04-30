

# Slot: resistance_mutation 



URI: [clinical_model:resistance_mutation](https://uk-cpi.com/clinical_model/resistance_mutation)
Alias: resistance_mutation

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Mutation](Mutation.md) | Individual genomic variant detected in NGS test - normalized to enable time-s... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Boolean](Boolean.md) |
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
| self | clinical_model:resistance_mutation |
| native | clinical_model:resistance_mutation |




## LinkML Source

<details>
```yaml
name: resistance_mutation
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: resistance_mutation
domain_of:
- Mutation
range: boolean

```
</details>