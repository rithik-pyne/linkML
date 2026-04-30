

# Slot: dicom_file_path 



URI: [clinical_model:dicom_file_path](https://uk-cpi.com/clinical_model/dicom_file_path)
Alias: dicom_file_path

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
| self | clinical_model:dicom_file_path |
| native | clinical_model:dicom_file_path |




## LinkML Source

<details>
```yaml
name: dicom_file_path
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: dicom_file_path
domain_of:
- ImagingStudy
range: string

```
</details>