

# Slot: treatment_intent 



URI: [clinical_model:treatment_intent](https://uk-cpi.com/clinical_model/treatment_intent)
Alias: treatment_intent

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [TreatmentIntentEnum](TreatmentIntentEnum.md) |
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
| self | clinical_model:treatment_intent |
| native | clinical_model:treatment_intent |




## LinkML Source

<details>
```yaml
name: treatment_intent
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: treatment_intent
domain_of:
- Treatment
range: TreatmentIntentEnum

```
</details>