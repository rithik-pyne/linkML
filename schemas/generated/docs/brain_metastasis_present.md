

# Slot: brain_metastasis_present 



URI: [clinical_model:brain_metastasis_present](https://uk-cpi.com/clinical_model/brain_metastasis_present)
Alias: brain_metastasis_present

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Boolean](Boolean.md) |
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
| self | clinical_model:brain_metastasis_present |
| native | clinical_model:brain_metastasis_present |




## LinkML Source

<details>
```yaml
name: brain_metastasis_present
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: brain_metastasis_present
domain_of:
- ImagingStudy
range: boolean

```
</details>