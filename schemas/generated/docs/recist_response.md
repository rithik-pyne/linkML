

# Slot: recist_response 



URI: [clinical_model:recist_response](https://uk-cpi.com/clinical_model/recist_response)
Alias: recist_response

<!-- no inheritance hierarchy -->





## Applicable Classes

| Name | Description | Modifies Slot |
| --- | --- | --- |
| [ResponseAssessment](ResponseAssessment.md) | Serial treatment response monitoring (RECIST + ctDNA) - multiple rows per pat... |  no  |






## Properties

### Type and Range

| Property | Value |
| --- | --- |
| Range | [RECISTResponseEnum](RECISTResponseEnum.md) |
| Domain Of | [ResponseAssessment](ResponseAssessment.md) |

### Cardinality and Requirements

| Property | Value |
| --- | --- |










## Identifier and Mapping Information





### Schema Source


* from schema: https://ngdx.org/clinical_model




## Mappings

| Mapping Type | Mapped Value |
| ---  | ---  |
| self | clinical_model:recist_response |
| native | clinical_model:recist_response |




## LinkML Source

<details>
```yaml
name: recist_response
from_schema: https://ngdx.org/clinical_model
rank: 1000
alias: recist_response
domain_of:
- ResponseAssessment
range: RECISTResponseEnum

```
</details>