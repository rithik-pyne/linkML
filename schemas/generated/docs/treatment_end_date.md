

# Slot: treatment_end_date 



URI: [clinical_model:treatment_end_date](https://uk-cpi.com/clinical_model/treatment_end_date)
Alias: treatment_end_date

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










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:treatment_end_date |
| native | clinical_model:treatment_end_date |




## LinkML Source

<details>
```yaml
name: treatment_end_date
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: treatment_end_date
domain_of:
- Treatment
range: date

```
</details>