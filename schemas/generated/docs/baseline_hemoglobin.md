

# Slot: baseline_hemoglobin 



URI: [clinical_model:baseline_hemoglobin](https://uk-cpi.com/clinical_model/baseline_hemoglobin)
Alias: baseline_hemoglobin

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
| self | clinical_model:baseline_hemoglobin |
| native | clinical_model:baseline_hemoglobin |




## LinkML Source

<details>
```yaml
name: baseline_hemoglobin
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: baseline_hemoglobin
domain_of:
- Patient
range: float
minimum_value: 0

```
</details>