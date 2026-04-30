

# Slot: vaf_percent 



URI: [clinical_model:vaf_percent](https://uk-cpi.com/clinical_model/vaf_percent)
Alias: vaf_percent

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
| self | clinical_model:vaf_percent |
| native | clinical_model:vaf_percent |




## LinkML Source

<details>
```yaml
name: vaf_percent
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: vaf_percent
domain_of:
- Mutation
range: float
minimum_value: 0.0
maximum_value: 100.0

```
</details>