

# Slot: thumbnail_image_path 



URI: [clinical_model:thumbnail_image_path](https://uk-cpi.com/clinical_model/thumbnail_image_path)
Alias: thumbnail_image_path

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
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
| self | clinical_model:thumbnail_image_path |
| native | clinical_model:thumbnail_image_path |




## LinkML Source

<details>
```yaml
name: thumbnail_image_path
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: thumbnail_image_path
domain_of:
- ImagingStudy
range: string

```
</details>