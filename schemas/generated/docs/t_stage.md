

# Slot: t_stage 



URI: [clinical_model:t_stage](https://uk-cpi.com/clinical_model/t_stage)
Alias: t_stage

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [TStageEnum](TStageEnum.md) |
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
| self | clinical_model:t_stage |
| native | clinical_model:t_stage |




## LinkML Source

<details>
```yaml
name: t_stage
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: t_stage
domain_of:
- ImagingStudy
range: TStageEnum

```
</details>