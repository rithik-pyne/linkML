

# Slot: molecular_test_id 



URI: [clinical_model:molecular_test_id](https://uk-cpi.com/clinical_model/molecular_test_id)
Alias: molecular_test_id

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Mutation](Mutation.md) | Individual genomic variant detected in NGS test - normalized to enable time-s... |  yes  |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  yes  |
| [MolecularTest](MolecularTest.md) | NGS test from tissue or ctDNA - multiple rows per patient |  yes  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [MolecularTest](MolecularTest.md) |
| Domain Of | [MolecularTest](MolecularTest.md), [Mutation](Mutation.md), [ResponseAssessment](ResponseAssessment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
| Required | Yes |
### Slot Characteristics

| Property | Value |
| --- | --- |
| Identifier | Yes |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:molecular_test_id |
| native | clinical_model:molecular_test_id |




## LinkML Source

<details>
```yaml
name: molecular_test_id
from_schema: https://ngdx.org/clinical_model
rank: 1000
identifier: true
alias: molecular_test_id
domain_of:
- MolecularTest
- Mutation
- ResponseAssessment
range: MolecularTest
required: true

```
</details>