

# Slot: tissue_fixation_hours 



URI: [clinical_model:tissue_fixation_hours](https://uk-cpi.com/clinical_model/tissue_fixation_hours)
Alias: tissue_fixation_hours

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
| self | clinical_model:tissue_fixation_hours |
| native | clinical_model:tissue_fixation_hours |




## LinkML Source

<details>
```yaml
name: tissue_fixation_hours
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: tissue_fixation_hours
domain_of:
- Biopsy
range: float
minimum_value: 0

```
</details>