

# Slot: ct_kvp 



URI: [clinical_model:ct_kvp](https://uk-cpi.com/clinical_model/ct_kvp)
Alias: ct_kvp

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](Integer.md) |
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
| self | clinical_model:ct_kvp |
| native | clinical_model:ct_kvp |




## LinkML Source

<details>
```yaml
name: ct_kvp
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: ct_kvp
domain_of:
- ImagingStudy
range: integer
minimum_value: 0

```
</details>