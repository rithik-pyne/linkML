

# Slot: baseline_wbc 



URI: [clinical_model:baseline_wbc](https://uk-cpi.com/clinical_model/baseline_wbc)
Alias: baseline_wbc

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Patient](Patient.md) | Core patient entity with demographics and baseline clinical data |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [Patient](Patient.md) |

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
| self | clinical_model:baseline_wbc |
| native | clinical_model:baseline_wbc |




## LinkML Source

<details>
```yaml
name: baseline_wbc
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: baseline_wbc
domain_of:
- Patient
range: float
minimum_value: 0

```
</details>