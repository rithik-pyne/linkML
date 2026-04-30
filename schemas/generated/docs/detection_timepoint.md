

# Slot: detection_timepoint 



URI: [clinical_model:detection_timepoint](https://uk-cpi.com/clinical_model/detection_timepoint)
Alias: detection_timepoint

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Mutation](Mutation.md) | Individual genomic variant detected in NGS test - normalized to enable time-s... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DetectionTimepointEnum](DetectionTimepointEnum.md) |
| Domain Of | [Mutation](Mutation.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:detection_timepoint |
| native | clinical_model:detection_timepoint |




## LinkML Source

<details>
```yaml
name: detection_timepoint
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: detection_timepoint
domain_of:
- Mutation
range: DetectionTimepointEnum

```
</details>