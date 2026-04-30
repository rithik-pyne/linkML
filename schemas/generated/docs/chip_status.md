

# Slot: chip_status 



URI: [clinical_model:chip_status](https://uk-cpi.com/clinical_model/chip_status)
Alias: chip_status

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
| self | clinical_model:chip_status |
| native | clinical_model:chip_status |




## LinkML Source

<details>
```yaml
name: chip_status
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: chip_status
domain_of:
- Mutation
range: string

```
</details>