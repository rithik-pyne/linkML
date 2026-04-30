

# Slot: time_to_fractionation_hours 



URI: [clinical_model:time_to_fractionation_hours](https://uk-cpi.com/clinical_model/time_to_fractionation_hours)
Alias: time_to_fractionation_hours

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Biopsy](Biopsy.md) | Tissue or liquid biopsy procedure - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [Biopsy](Biopsy.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:time_to_fractionation_hours |
| native | clinical_model:time_to_fractionation_hours |




## LinkML Source

<details>
```yaml
name: time_to_fractionation_hours
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: time_to_fractionation_hours
domain_of:
- Biopsy
range: float
minimum_value: 0

```
</details>