

# Slot: imaging_modality 



URI: [clinical_model:imaging_modality](https://uk-cpi.com/clinical_model/imaging_modality)
Alias: imaging_modality

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [ImagingModalityEnum](ImagingModalityEnum.md) |
| Domain Of | [ImagingStudy](ImagingStudy.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:imaging_modality |
| native | clinical_model:imaging_modality |




## LinkML Source

<details>
```yaml
name: imaging_modality
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: imaging_modality
domain_of:
- ImagingStudy
range: ImagingModalityEnum

```
</details>