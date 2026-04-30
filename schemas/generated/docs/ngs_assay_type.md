

# Slot: ngs_assay_type 



URI: [clinical_model:ngs_assay_type](https://uk-cpi.com/clinical_model/ngs_assay_type)
Alias: ngs_assay_type

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MolecularTest](MolecularTest.md) | NGS test from tissue or ctDNA - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [NGSAssayTypeEnum](NGSAssayTypeEnum.md) |
| Domain Of | [MolecularTest](MolecularTest.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:ngs_assay_type |
| native | clinical_model:ngs_assay_type |




## LinkML Source

<details>
```yaml
name: ngs_assay_type
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: ngs_assay_type
domain_of:
- MolecularTest
range: NGSAssayTypeEnum

```
</details>