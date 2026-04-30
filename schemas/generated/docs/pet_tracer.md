

# Slot: pet_tracer 



URI: [clinical_model:pet_tracer](https://uk-cpi.com/clinical_model/pet_tracer)
Alias: pet_tracer

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
| self | clinical_model:pet_tracer |
| native | clinical_model:pet_tracer |




## LinkML Source

<details>
```yaml
name: pet_tracer
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: pet_tracer
domain_of:
- ImagingStudy
range: string

```
</details>