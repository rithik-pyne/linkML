

# Slot: study_description 



URI: [clinical_model:study_description](https://uk-cpi.com/clinical_model/study_description)
Alias: study_description

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
| self | clinical_model:study_description |
| native | clinical_model:study_description |




## LinkML Source

<details>
```yaml
name: study_description
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: study_description
domain_of:
- ImagingStudy
range: string

```
</details>