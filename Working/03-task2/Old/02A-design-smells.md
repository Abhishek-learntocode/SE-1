# Task 2A - Design Smells

This document lists candidate design smells based on UML/code inspection and SonarQube findings.

## Methodology

**Approach:** Tool-assisted analysis with manual verification

1. **Tool Analysis (SonarQube):**
   - Executed: `mvn clean verify sonar:sonar`
   - Server: http://localhost:9000
   - Extracted code smells and hotspots via SonarQube Web API
   - Pulled metrics for complexity, NCLOC, functions, cognitive complexity

2. **Manual Architecture Analysis:**
   - Reviewed UML diagrams from Task 1 (3 subsystems)
   - Identified architectural patterns and anti-patterns
   - Translated code-level smells to design-level smells
   - Used subsystem understanding to identify coupling issues

3. **Verification:**
   - Cross-referenced SonarQube findings with manual code inspection
   - Validated each smell against UML relationships
   - Documented evidence from both tool outputs and manual analysis

**Note:** Per assignment guidance ("Sonarqube or any automated tool is not perfect, so use your own judgment"), this analysis combines automated tool detection with human architectural judgment.

## Smell 1: God Interface / Overloaded Manager Interface
- **Description**: `WeblogEntryManager` bundles responsibilities for entries, categories, comments, tags, and hit counts.
- **Evidence (UML/Code)**: Large interface with multiple concern groups in [WeblogEntryManager.java](app/src/main/java/org/apache/roller/weblogger/business/WeblogEntryManager.java).
- **SonarQube Evidence**: `WeblogEntryManager.java` has **43 methods** (`functions=43`), indicating a large surface area for a single interface.

## Smell 2: Service Locator / Hidden Dependencies
- **Description**: Domain entities (`Weblog`, `WeblogEntry`, `User`) invoke `WebloggerFactory` to access managers, coupling domain to service layer.
- **Evidence (UML/Code)**: [Weblog.java](app/src/main/java/org/apache/roller/weblogger/pojos/Weblog.java), [WeblogEntry.java](app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntry.java), [User.java](app/src/main/java/org/apache/roller/weblogger/pojos/User.java).
- **SonarQube Evidence**: Not directly flagged by a specific rule; supported by manual architecture analysis and UML relationships.

## Smell 3: Large Class / Mixed Responsibilities
- **Description**: `WeblogEntry` handles data, rendering, permissions, and anchor generation.
- **Evidence (UML/Code)**: [WeblogEntry.java](app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntry.java).
- **SonarQube Evidence**: High metrics for `WeblogEntry.java` (Sonar measures: `ncloc=621`, `functions=93`, `complexity=156`, `cognitive_complexity=99`).

## Smell 4: Temporal Coupling / Initialization Logic in Manager
- **Description**: `LuceneIndexManager` combines configuration, consistency checks, directory management, and scheduling operations.
- **Evidence (UML/Code)**: [LuceneIndexManager.java](app/src/main/java/org/apache/roller/weblogger/business/search/lucene/LuceneIndexManager.java).
- **SonarQube Evidence**: High cognitive complexity (`cognitive_complexity=59`, `ncloc=342`). Sonar also reports duplication and resource-handling smells (e.g., `java:S1192`, `java:S2093`) on this class.

## Smell 5: Deprecated Role APIs Coexisting with Permissions
- **Description**: Deprecated role APIs still used in security adapter (`RollerUserDetailsService`) via `getRoles`, suggesting dual authorization models.
- **Evidence (UML/Code)**: [UserManager.java](app/src/main/java/org/apache/roller/weblogger/business/UserManager.java), [RollerUserDetailsService.java](app/src/main/java/org/apache/roller/weblogger/ui/core/security/RollerUserDetailsService.java).
- **SonarQube Evidence**: Sonar rule `java:S1874` flags use of deprecated `getRoles` in `RollerUserDetailsService.java` (line 98). `UserManager.java` also has deprecated sections flagged by `java:S6355` and `java:S1133`.

## Smell 6: Duplication of Sanitization / Rendering
- **Description**: Sanitization occurs inside `render()` and again after `displayContent()` adds read-more link.
- **Evidence (UML/Code)**: [WeblogEntry.java](app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntry.java).
- **SonarQube Evidence**: Not directly flagged; design-level duplication observed in manual review of rendering flow.

## Smell 7: Long Method / Complex Conditional Logic
- **Description**: `displayContent(String)` and `render(String)` include nested conditional paths that can be simplified.
- **Evidence (UML/Code)**: [WeblogEntry.java](app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntry.java).
- **SonarQube Evidence**: Overall class has high cognitive complexity (`cognitive_complexity=99`), supporting the presence of complex methods.

## SonarQube Context
- Project: `Roller` on `http://localhost:9000`
- Analysis already executed; evidence extracted via SonarQube Web API.
