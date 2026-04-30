

# Slot: study_uid 



URI: [clinical_model:study_uid](https://uk-cpi.com/clinical_model/study_uid)
Alias: study_uid

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
### Value Constraints

| Property | Value |
| --- | --- |
| Regex Pattern | `^[0-9.]{1,64}$` |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:study_uid |
| native | clinical_model:study_uid |




## LinkML Source

<details>
```yaml
name: study_uid
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: study_uid
domain_of:
- ImagingStudy
range: string
pattern: ^[0-9.]{1,64}$

```
</details>