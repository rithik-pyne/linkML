

# Slot: accession_number 



URI: [clinical_model:accession_number](https://uk-cpi.com/clinical_model/accession_number)
Alias: accession_number

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
| self | clinical_model:accession_number |
| native | clinical_model:accession_number |




## LinkML Source

<details>
```yaml
name: accession_number
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: accession_number
domain_of:
- ImagingStudy
range: string

```
</details>