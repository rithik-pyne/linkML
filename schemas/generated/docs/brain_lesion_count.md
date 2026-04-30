

# Slot: brain_lesion_count 



URI: [clinical_model:brain_lesion_count](https://uk-cpi.com/clinical_model/brain_lesion_count)
Alias: brain_lesion_count

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ImagingStudy](ImagingStudy.md) | Imaging study (CT, PET, MRI) with TNM staging - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Integer](Integer.md) |
| Domain Of | [ImagingStudy](ImagingStudy.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:brain_lesion_count |
| native | clinical_model:brain_lesion_count |




## LinkML Source

<details>
```yaml
name: brain_lesion_count
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: brain_lesion_count
domain_of:
- ImagingStudy
range: integer
minimum_value: 0

```
</details>