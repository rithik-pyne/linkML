

# Slot: pet_uptake_time_min 



URI: [clinical_model:pet_uptake_time_min](https://uk-cpi.com/clinical_model/pet_uptake_time_min)
Alias: pet_uptake_time_min

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
| self | clinical_model:pet_uptake_time_min |
| native | clinical_model:pet_uptake_time_min |




## LinkML Source

<details>
```yaml
name: pet_uptake_time_min
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: pet_uptake_time_min
domain_of:
- ImagingStudy
range: float
minimum_value: 0

```
</details>