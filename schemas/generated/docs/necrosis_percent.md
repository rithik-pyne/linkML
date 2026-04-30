

# Slot: necrosis_percent 



URI: [clinical_model:necrosis_percent](https://uk-cpi.com/clinical_model/necrosis_percent)
Alias: necrosis_percent

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
| Maximum Value | 100 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:necrosis_percent |
| native | clinical_model:necrosis_percent |




## LinkML Source

<details>
```yaml
name: necrosis_percent
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: necrosis_percent
domain_of:
- Biopsy
range: float
minimum_value: 0
maximum_value: 100

```
</details>