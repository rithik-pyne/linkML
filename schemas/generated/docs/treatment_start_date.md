

# Slot: treatment_start_date 



URI: [clinical_model:treatment_start_date](https://uk-cpi.com/clinical_model/treatment_start_date)
Alias: treatment_start_date

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Date](Date.md) |
| Domain Of | [Treatment](Treatment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:treatment_start_date |
| native | clinical_model:treatment_start_date |




## LinkML Source

<details>
```yaml
name: treatment_start_date
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: treatment_start_date
domain_of:
- Treatment
range: date
required: true

```
</details>