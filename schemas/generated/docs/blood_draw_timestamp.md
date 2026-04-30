

# Slot: blood_draw_timestamp 



URI: [clinical_model:blood_draw_timestamp](https://uk-cpi.com/clinical_model/blood_draw_timestamp)
Alias: blood_draw_timestamp

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Biopsy](Biopsy.md) | Tissue or liquid biopsy procedure - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Datetime](Datetime.md) |
| Domain Of | [Biopsy](Biopsy.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:blood_draw_timestamp |
| native | clinical_model:blood_draw_timestamp |




## LinkML Source

<details>
```yaml
name: blood_draw_timestamp
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: blood_draw_timestamp
domain_of:
- Biopsy
range: datetime

```
</details>