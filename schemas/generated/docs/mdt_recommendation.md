

# Slot: mdt_recommendation 



URI: [clinical_model:mdt_recommendation](https://uk-cpi.com/clinical_model/mdt_recommendation)
Alias: mdt_recommendation

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
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
| self | clinical_model:mdt_recommendation |
| native | clinical_model:mdt_recommendation |




## LinkML Source

<details>
```yaml
name: mdt_recommendation
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: mdt_recommendation
domain_of:
- Treatment
range: string

```
</details>