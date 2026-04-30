

# Slot: drug_frequency 



URI: [clinical_model:drug_frequency](https://uk-cpi.com/clinical_model/drug_frequency)
Alias: drug_frequency

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Treatment](Treatment.md) | Treatment line with drug regimen and duration - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [DoseFrequencyEnum](DoseFrequencyEnum.md) |
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
| self | clinical_model:drug_frequency |
| native | clinical_model:drug_frequency |




## LinkML Source

<details>
```yaml
name: drug_frequency
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: drug_frequency
domain_of:
- Treatment
range: DoseFrequencyEnum

```
</details>