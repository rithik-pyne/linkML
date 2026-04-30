

# Slot: blood_collection_volume_ml 



URI: [clinical_model:blood_collection_volume_ml](https://uk-cpi.com/clinical_model/blood_collection_volume_ml)
Alias: blood_collection_volume_ml

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [Biopsy](Biopsy.md) | Tissue or liquid biopsy procedure - multiple rows per patient |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [Float](Float.md) |
| Domain Of | [Biopsy](Biopsy.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |
### Value Constraints

| Property | Value |
| --- | --- |
| Minimum Value | 0 |












## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:blood_collection_volume_ml |
| native | clinical_model:blood_collection_volume_ml |




## LinkML Source

<details>
```yaml
name: blood_collection_volume_ml
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: blood_collection_volume_ml
domain_of:
- Biopsy
range: float
minimum_value: 0

```
</details>