# Task 2B - Code Metrics Analysis

## Tools Used
- **SonarQube** (project `Roller`, local server `http://localhost:9000`) for size/complexity/duplication/technical-debt metrics.
  - Version: Community Edition (latest)
  - Analysis command: `mvn clean verify sonar:sonar`
  - Dashboard: http://localhost:9000/dashboard?id=Roller
- **CK Tool** (v0.7.0, Chidamber & Kemerer suite) for class-level OO metrics (WMC, CBO, RFC, DIT, NOC, LCOM).
  - Repository: https://github.com/mauricioaniche/ck
  - Execution: `java -jar ck-0.7.0-jar-with-dependencies.jar <source-path> true 0 false`
  - Output: `Working/03-task2/ckclass.csv` (535 classes) and `Working/03-task2/ckmethod.csv`

**Note:** The assignment suggests CodeMR, Checkstyle, or PMD as examples. We used SonarQube (which encompasses functionality of CheckStyle/PMD) and the specialized CK tool for accurate OOP metrics. This combination provides all required metrics with industry-standard reliability.

## Metrics Selected (6 total)

### 1) Size: Non-comment lines of code (NCLOC)
- **Value**: 66,718 (project-wide)
- **Implication**: Large codebase implies higher maintenance overhead and more surface area for defects. Prioritize refactoring high-churn and high-complexity files first.

### 2) Structural Size: Number of classes
- **Value**: 534 (project-wide)
- **Implication**: Large class count signals a broad domain model and service layer. Architectural consistency and module boundaries become critical.

### 3) Complexity: Cyclomatic Complexity (project-wide)
- **Value**: 9,279
- **Implication**: High complexity suggests many decision paths; unit tests and refactoring should target hotspots to reduce defect risk.

### 4) Complexity: Cognitive Complexity (project-wide)
- **Value**: 7,615
- **Implication**: High cognitive complexity indicates code that is hard to understand/maintain. Refactor long/branchy methods into smaller, focused units.

### 5) Duplication: Duplicated Lines Density
- **Value**: 3.8%
- **Implication**: Moderate duplication can be reduced with shared utilities or refactoring repeated patterns; helps improve maintainability and reduce bug propagation.

### 6) Maintainability: Technical Debt (sqale_index)
- **Value**: 19,507 minutes (SonarQube remediation estimate)
- **Implication**: Significant estimated effort to bring codebase to quality standards. Use as a prioritization guide for refactoring tasks.

## OO (CK) Metrics Plan (Class-level)
- **Required**: WMC, CBO, RFC, DIT, NOC, LCOM (Chidamber & Kemerer suite).
- **Execution**: CK tool run completed; outputs stored in `Working/03-task2/ckclass.csv` and `Working/03-task2/ckmethod.csv`.

### CK Summary (Class-level, n=535)
- **WMC**: avg 18.73 (min 0, max 197), p90 43, p95 61, p99 108
- **CBO**: avg 6.74 (min 0, max 46), p90 15, p95 20, p99 31
- **RFC**: avg 17.81 (min 0, max 190), p90 47, p95 62, p99 113
- **DIT**: avg 1.58 (min 1, max 7), p90 3, p95 3, p99 4
- **NOC**: avg 0.22 (min 0, max 39), p90 0, p95 1, p99 4
- **LCOM**: avg 70.65 (min 0, max 4336), p90 135, p95 299, p99 1114

### CK Implications
- **WMC/RFC**: Long tail indicates classes with many methods and complex behavior; refactor high-percentile classes first.
- **CBO**: Moderate average, but p95/p99 suggest tight coupling in some areas; apply dependency inversion or façade where feasible.
- **DIT/NOC**: Shallow inheritance overall; composition is dominant, which is good for maintainability.
- **LCOM**: High tail values indicate low cohesion in some classes; candidates for class extraction and responsibility split.

## References
- CK tool usage and output details: https://github.com/mauricioaniche/ck
- SonarQube project dashboard: http://localhost:9000/dashboard?id=Roller

## Tool Output Evidence
- **SonarQube Dashboard Screenshot**: `screenshots/sonarqube-dashboard.png` (to be added)
- **CK Metrics Data**: Full dataset available in `ckclass.csv` (535 classes) and `ckmethod.csv`
- **CK Summary Statistics**: Documented in `ck/ck-summary.md`

## How Metrics Were Obtained

### SonarQube Metrics (NCLOC, Complexity, Duplication, Technical Debt):
1. Executed Maven Sonar plugin: `mvn clean verify sonar:sonar`
2. SonarQube server analyzed source code and computed metrics
3. Retrieved via SonarQube Web API:
   ```bash
   curl "http://localhost:9000/api/measures/component?component=Roller&metricKeys=ncloc,classes,complexity,cognitive_complexity,duplicated_lines_density,sqale_index"
   ```
4. Values extracted from JSON response and documented above

### CK Metrics (WMC, CBO, RFC, DIT, NOC, LCOM):
1. Downloaded CK tool JAR from https://github.com/mauricioaniche/ck/releases
2. Executed on compiled classes: `java -jar ck-0.7.0-jar-with-dependencies.jar app/target/classes true 0 false`
3. Tool generated `ckclass.csv` with per-class metrics for 535 classes
4. Computed summary statistics (avg, min, max, percentiles) using data analysis
5. Results documented in CK Summary section above
