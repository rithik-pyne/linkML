

# Slot: m_sites 



URI: [clinical_model:m_sites](https://uk-cpi.com/clinical_model/m_sites)
Alias: m_sites

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
| self | clinical_model:m_sites |
| native | clinical_model:m_sites |




## LinkML Source

<details>
```yaml
name: m_sites
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: m_sites
domain_of:
- ImagingStudy
range: string

```
</details>