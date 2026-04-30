

# Slot: ecog_baseline 



URI: [clinical_model:ecog_baseline](https://uk-cpi.com/clinical_model/ecog_baseline)
Alias: ecog_baseline

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Patient](Patient.md) | Core patient entity with demographics and baseline clinical data |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](Integer.md) |
| Domain Of | [Patient](Patient.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |
| Maximum Value | 5 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:ecog_baseline |
| native | clinical_model:ecog_baseline |




## LinkML Source

<details>
```yaml
name: ecog_baseline
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: ecog_baseline
domain_of:
- Patient
range: integer
minimum_value: 0
maximum_value: 5

```
</details>