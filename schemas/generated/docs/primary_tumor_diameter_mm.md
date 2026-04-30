

# Slot: primary_tumor_diameter_mm 



URI: [clinical_model:primary_tumor_diameter_mm](https://uk-cpi.com/clinical_model/primary_tumor_diameter_mm)
Alias: primary_tumor_diameter_mm

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
| Maximum Value | 300 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:primary_tumor_diameter_mm |
| native | clinical_model:primary_tumor_diameter_mm |




## LinkML Source

<details>
```yaml
name: primary_tumor_diameter_mm
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: primary_tumor_diameter_mm
domain_of:
- ImagingStudy
range: float
minimum_value: 0
maximum_value: 300

```
</details>