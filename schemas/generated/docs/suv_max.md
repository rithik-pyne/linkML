

# Slot: suv_max 



URI: [clinical_model:suv_max](https://uk-cpi.com/clinical_model/suv_max)
Alias: suv_max

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
| Maximum Value | 50 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:suv_max |
| native | clinical_model:suv_max |




## LinkML Source

<details>
```yaml
name: suv_max
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: suv_max
domain_of:
- ImagingStudy
range: float
minimum_value: 0
maximum_value: 50

```
</details>