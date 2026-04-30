

# Slot: ngs_report_pdf_path 



URI: [clinical_model:ngs_report_pdf_path](https://uk-cpi.com/clinical_model/ngs_report_pdf_path)
Alias: ngs_report_pdf_path

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [MolecularTest](MolecularTest.md) | NGS test from tissue or ctDNA - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [String](String.md) |
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
| self | clinical_model:ngs_report_pdf_path |
| native | clinical_model:ngs_report_pdf_path |




## LinkML Source

<details>
```yaml
name: ngs_report_pdf_path
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: ngs_report_pdf_path
domain_of:
- MolecularTest
range: string

```
</details>