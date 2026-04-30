

# Slot: treatment_line 



URI: [clinical_model:treatment_line](https://uk-cpi.com/clinical_model/treatment_line)
Alias: treatment_line

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](Integer.md) |
| Domain Of | [Treatment](Treatment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |
| Maximum Value | 10 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:treatment_line |
| native | clinical_model:treatment_line |




## LinkML Source

<details>
```yaml
name: treatment_line
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: treatment_line
domain_of:
- Treatment
range: integer
minimum_value: 0
maximum_value: 10

```
</details>