

# Slot: months_since_last_ici 



URI: [clinical_model:months_since_last_ici](https://uk-cpi.com/clinical_model/months_since_last_ici)
Alias: months_since_last_ici

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [Treatment](Treatment.md) |

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
| self | clinical_model:months_since_last_ici |
| native | clinical_model:months_since_last_ici |




## LinkML Source

<details>
```yaml
name: months_since_last_ici
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: months_since_last_ici
domain_of:
- Treatment
range: float
minimum_value: 0

```
</details>