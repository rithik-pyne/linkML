

# Slot: test_date 



URI: [clinical_model:test_date](https://uk-cpi.com/clinical_model/test_date)
Alias: test_date

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MolecularTest](MolecularTest.md) | NGS test from tissue or ctDNA - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Date](Date.md) |
| Domain Of | [MolecularTest](MolecularTest.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:test_date |
| native | clinical_model:test_date |




## LinkML Source

<details>
```yaml
name: test_date
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: test_date
domain_of:
- MolecularTest
range: date
required: true

```
</details>