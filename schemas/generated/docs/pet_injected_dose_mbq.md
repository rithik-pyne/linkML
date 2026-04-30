

# Slot: pet_injected_dose_mbq 



URI: [clinical_model:pet_injected_dose_mbq](https://uk-cpi.com/clinical_model/pet_injected_dose_mbq)
Alias: pet_injected_dose_mbq

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
| self | clinical_model:pet_injected_dose_mbq |
| native | clinical_model:pet_injected_dose_mbq |




## LinkML Source

<details>
```yaml
name: pet_injected_dose_mbq
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: pet_injected_dose_mbq
domain_of:
- ImagingStudy
range: float
minimum_value: 0

```
</details>