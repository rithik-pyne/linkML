

# Slot: ct_mas 



URI: [clinical_model:ct_mas](https://uk-cpi.com/clinical_model/ct_mas)
Alias: ct_mas

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [ImagingStudy](ImagingStudy.md) |

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
| self | clinical_model:ct_mas |
| native | clinical_model:ct_mas |




## LinkML Source

<details>
```yaml
name: ct_mas
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: ct_mas
domain_of:
- ImagingStudy
range: float
minimum_value: 0

```
</details>