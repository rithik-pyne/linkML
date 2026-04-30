

# Slot: tumor_fraction_percent 



URI: [clinical_model:tumor_fraction_percent](https://uk-cpi.com/clinical_model/tumor_fraction_percent)
Alias: tumor_fraction_percent

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Mutation](Mutation.md) | Individual genomic variant detected in NGS test - normalized to enable time-s... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [Mutation](Mutation.md) |

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
| self | clinical_model:tumor_fraction_percent |
| native | clinical_model:tumor_fraction_percent |




## LinkML Source

<details>
```yaml
name: tumor_fraction_percent
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: tumor_fraction_percent
domain_of:
- Mutation
range: float
minimum_value: 0.0
maximum_value: 100.0

```
</details>