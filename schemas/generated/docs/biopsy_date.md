

# Slot: biopsy_date 



URI: [clinical_model:biopsy_date](https://uk-cpi.com/clinical_model/biopsy_date)
Alias: biopsy_date

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Biopsy](Biopsy.md) | Tissue or liquid biopsy procedure - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Date](Date.md) |
| Domain Of | [Biopsy](Biopsy.md) |

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
| self | clinical_model:biopsy_date |
| native | clinical_model:biopsy_date |




## LinkML Source

<details>
```yaml
name: biopsy_date
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: biopsy_date
domain_of:
- Biopsy
range: date
required: true

```
</details>