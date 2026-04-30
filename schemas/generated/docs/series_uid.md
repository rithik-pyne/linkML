

# Slot: series_uid 



URI: [clinical_model:series_uid](https://uk-cpi.com/clinical_model/series_uid)
Alias: series_uid

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
| self | clinical_model:series_uid |
| native | clinical_model:series_uid |




## LinkML Source

<details>
```yaml
name: series_uid
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: series_uid
domain_of:
- ImagingStudy
range: string

```
</details>