# Task 1 Observations and Assumptions

## Strengths
- Clear separation between Manager interfaces and POJO entities.
- Lucene search isolated behind `IndexManager` interface.
- Reusable criteria objects for queries (e.g., `WeblogEntrySearchCriteria`).

## Weaknesses
- Domain entities call into managers via `WebloggerFactory`, introducing service-layer coupling.
- Large Manager interfaces blend multiple concerns (entries, categories, comments, tags, hit counts).
- Some code paths rely on deprecated role APIs alongside permission checks.

## Assumptions
- UML diagrams model only key classes for the three subsystems and omit minor helper classes.
- Associations shown are conceptual and not necessarily direct field references.
- Package boundaries simplified to highlight subsystem ownership.
