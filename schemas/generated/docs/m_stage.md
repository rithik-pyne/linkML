

# Slot: m_stage 



URI: [clinical_model:m_stage](https://uk-cpi.com/clinical_model/m_stage)
Alias: m_stage

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [MStageEnum](MStageEnum.md) |
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
| self | clinical_model:m_stage |
| native | clinical_model:m_stage |




## LinkML Source

<details>
```yaml
name: m_stage
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: m_stage
domain_of:
- ImagingStudy
range: MStageEnum

```
</details>