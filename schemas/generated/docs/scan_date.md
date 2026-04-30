

# Slot: scan_date 



URI: [clinical_model:scan_date](https://uk-cpi.com/clinical_model/scan_date)
Alias: scan_date

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Date](Date.md) |
| Domain Of | [ImagingStudy](ImagingStudy.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:scan_date |
| native | clinical_model:scan_date |




## LinkML Source

<details>
```yaml
name: scan_date
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: scan_date
domain_of:
- ImagingStudy
range: date
required: true

```
</details>