

# Slot: mutation_classification 



URI: [clinical_model:mutation_classification](https://uk-cpi.com/clinical_model/mutation_classification)
Alias: mutation_classification

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Mutation](Mutation.md) | Individual genomic variant detected in NGS test - normalized to enable time-s... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [VariantTierEnum](VariantTierEnum.md) |
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
| self | clinical_model:mutation_classification |
| native | clinical_model:mutation_classification |




## LinkML Source

<details>
```yaml
name: mutation_classification
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: mutation_classification
domain_of:
- Mutation
range: VariantTierEnum

```
</details>