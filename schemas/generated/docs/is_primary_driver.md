

# Slot: is_primary_driver 



URI: [clinical_model:is_primary_driver](https://uk-cpi.com/clinical_model/is_primary_driver)
Alias: is_primary_driver

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
| self | clinical_model:is_primary_driver |
| native | clinical_model:is_primary_driver |




## LinkML Source

<details>
```yaml
name: is_primary_driver
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: is_primary_driver
domain_of:
- Mutation
range: boolean

```
</details>