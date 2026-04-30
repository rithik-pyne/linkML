

# Slot: drug_dose_mg 



URI: [clinical_model:drug_dose_mg](https://uk-cpi.com/clinical_model/drug_dose_mg)
Alias: drug_dose_mg

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
| self | clinical_model:drug_dose_mg |
| native | clinical_model:drug_dose_mg |




## LinkML Source

<details>
```yaml
name: drug_dose_mg
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: drug_dose_mg
domain_of:
- Treatment
range: float
minimum_value: 0

```
</details>