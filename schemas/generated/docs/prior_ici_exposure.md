

# Slot: prior_ici_exposure 



URI: [clinical_model:prior_ici_exposure](https://uk-cpi.com/clinical_model/prior_ici_exposure)
Alias: prior_ici_exposure

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Boolean](Boolean.md) |
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
| self | clinical_model:prior_ici_exposure |
| native | clinical_model:prior_ici_exposure |




## LinkML Source

<details>
```yaml
name: prior_ici_exposure
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: prior_ici_exposure
domain_of:
- Treatment
range: boolean

```
</details>