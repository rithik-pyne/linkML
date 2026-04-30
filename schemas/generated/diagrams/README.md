# Clinical Data Model Diagrams

Auto-generated from [clinical_model.yaml](../../clinical_model.yaml)

## Entity-Relationship Diagram

[**clinical_model.mmd**](clinical_model.mmd) - Complete ER diagram with all entities, attributes, and relationships

### Relationships
- **Patient** (1) → (N) Biopsy, ImagingStudy, MolecularTest, Treatment, ClinicalAssessment, ResponseAssessment, Mutation
- **Biopsy** (1) → (N) MolecularTest
- **MolecularTest** (1) → (N) Mutation, ResponseAssessment
- **ImagingStudy** (1) → (N) ResponseAssessment
- **Treatment** (1) → (N) ResponseAssessment

## Per-Entity Class Diagrams

[**mermaid_class/**](mermaid_class/) - Individual class diagrams showing each entity's relationships

## Viewing

- **GitHub**: Auto-renders Mermaid diagrams
- **VS Code**: Install "Markdown Preview Mermaid Support" extension
- **Online**: Copy to https://mermaid.live

## Regeneration

```bash
source .venv/Scripts/activate
gen-erdiagram schemas/clinical_model.yaml -f mermaid > schemas/generated/diagrams/clinical_model.mmd
gen-mermaid-class-diagram schemas/clinical_model.yaml --directory schemas/generated/diagrams/mermaid_class
```
