

# Slot: discontinuation_reason 



URI: [clinical_model:discontinuation_reason](https://uk-cpi.com/clinical_model/discontinuation_reason)
Alias: discontinuation_reason

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DiscontinuationReasonEnum](DiscontinuationReasonEnum.md) |
| Domain Of | [Treatment](Treatment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:discontinuation_reason |
| native | clinical_model:discontinuation_reason |




## LinkML Source

<details>
```yaml
name: discontinuation_reason
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: discontinuation_reason
domain_of:
- Treatment
range: DiscontinuationReasonEnum

```
</details>