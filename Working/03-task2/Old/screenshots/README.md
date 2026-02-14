# Screenshots Needed for Task 2

## Instructions:
Take the following screenshots from your SonarQube server (http://localhost:9000)

### 1. sonarqube-dashboard.png
**Navigate to:** http://localhost:9000/dashboard?id=Roller
**Capture:** 
- Overall project metrics (NCLOC, bugs, vulnerabilities, code smells)
- Technical debt ratio
- Duplications percentage
- Coverage (if available)

### 2. sonarqube-weblogentry.png
**Navigate to:** Code → Browse → WeblogEntry.java → Measures tab
**Capture:**
- NCLOC = 621
- Functions = 93
- Complexity = 156
- Cognitive Complexity = 99

### 3. sonarqube-issues.png
**Navigate to:** Issues → Type: Code Smell → Sort by Severity
**Capture:**
- Deprecated API warnings (java:S1874)
- Duplication issues (java:S1192)
- Other major code smells

### 4. sonarqube-hotspots.png
**Navigate to:** Measures → Complexity → Files (sorted by complexity)
**Capture:**
- Top 10 most complex files
- Should show WeblogEntry, LuceneIndexManager, etc.

---

## Quick Steps:
1. Start SonarQube: (if not running already)
   ```bash
   # Usually auto-starts after mvn sonar:sonar
   # Or manually start the server
   ```

2. Open browser: http://localhost:9000

3. Navigate to Roller project

4. Take screenshots using:
   - Windows: Windows + Shift + S (Snipping Tool)
   - Or use browser screenshot extension

5. Save screenshots to this directory with the exact filenames above

6. Commit with:
   ```bash
   git add Working/03-task2/screenshots/
   git commit -m "docs: Add SonarQube evidence screenshots for Task 2"
   ```

---

## After Adding Screenshots:
Your 02A-design-smells.md and 02B-metrics.md already reference these screenshots.
The assignment requires "supporting evidence from your tool reports" - these screenshots fulfill that requirement.
