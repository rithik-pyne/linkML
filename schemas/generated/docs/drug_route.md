

# Slot: drug_route 



URI: [clinical_model:drug_route](https://uk-cpi.com/clinical_model/drug_route)
Alias: drug_route

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
| self | clinical_model:drug_route |
| native | clinical_model:drug_route |




## LinkML Source

<details>
```yaml
name: drug_route
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: drug_route
domain_of:
- Treatment
range: string

```
</details>