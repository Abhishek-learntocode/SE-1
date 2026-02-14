# Task 2 Submission Guide - What to Commit & Submit

**Date:** February 3, 2026

---

## ✅ TASK 2 COMPLETION STATUS: COMPLETE

Your Task 2 is **done correctly** and meets all assignment requirements. Here's the breakdown:

---

## 📋 WHAT YOU NEED TO COMMIT (GitHub)

### Files to Commit:

1. ✅ **`Working/03-task2/02A-design-smells.md`** (43 lines)
   - Contains 7 design smells (exceeds 5-7 requirement)
   - Has SonarQube evidence for each smell
   - Includes UML/code inspection evidence

2. ✅ **`Working/03-task2/02B-metrics.md`** (54 lines)
   - Contains 6 code metrics + CK suite (WMC, CBO, RFC, DIT, NOC, LCOM)
   - States tools used: SonarQube + CK tool
   - Discusses implications for each metric

3. ⚠️ **`Working/03-task2/ckclass.csv`** (Optional but recommended)
   - Raw CK metrics data for 535 classes
   - **Commit this** - proves you ran the tool

4. ⚠️ **`Working/03-task2/ckmethod.csv`** (Optional but recommended)
   - Method-level CK metrics
   - **Commit this** - provides traceability

5. ✅ **`Working/03-task2/ck/ck-summary.md`** (if exists)
   - Summary of CK metrics analysis
   - **Commit if you have it**

### Files NOT Needed for Commit:
- ❌ SonarQube HTML reports (too large, server-based)
- ❌ CheckStyle/PMD XML reports (you didn't use these tools)
- ❌ Tool JAR files (unless custom scripts need them)

---

## 📄 WHAT YOU NEED IN FINAL REPORT (PDF)

The assignment says:
> "submit a report containing your responses for each task"

### For Task 2A (Design Smells):
You need to include in `docs/project1_<team>.pdf`:

1. **Table summarizing 7 design smells:**
   - Smell name
   - Description
   - Affected classes
   - Tool evidence (SonarQube metrics/rules)

2. **Screenshots from SonarQube** showing:
   - WeblogEntry complexity metrics (NCLOC=621, functions=93, complexity=156)
   - Deprecated API warnings (java:S1874 in RollerUserDetailsService)
   - LuceneIndexManager cognitive complexity (59)
   - Overall project dashboard

3. **References to your UML diagrams** showing:
   - Service Locator pattern (WeblogEntry → WebloggerFactory)
   - God Interface (WeblogEntryManager with 43 methods)

### For Task 2B (Code Metrics):
You need to include in the PDF:

1. **Table of 6 main metrics:**
   - NCLOC: 66,718
   - Classes: 534
   - Cyclomatic Complexity: 9,279
   - Cognitive Complexity: 7,615
   - Duplication: 3.8%
   - Technical Debt: 19,507 min

2. **CK Metrics summary table:**
   - WMC, CBO, RFC, DIT, NOC, LCOM
   - Show avg/min/max/percentiles

3. **Screenshot from SonarQube dashboard** showing:
   - Overall project metrics
   - Top complex files

4. **Optional: Screenshot from CK tool** (if you have visualization)

**You DON'T need to include the CSV files in the PDF** - just summarize the data in tables.

---

## 🛠️ HOW YOUR METRICS WERE CALCULATED (Explanation)

### Your Current Approach (CORRECT ✅):

#### For Project-Wide Metrics (NCLOC, Complexity, etc.):
**Tool: SonarQube**
- You ran: `mvn clean verify sonar:sonar`
- SonarQube analyzed the code and calculated:
  - NCLOC (Non-Comment Lines of Code) by parsing Java files
  - Cyclomatic Complexity by counting decision points (if/while/for/case)
  - Cognitive Complexity by analyzing nested logic
  - Duplication by finding similar code blocks
  - Technical Debt by estimating fix time for issues

**How to get these values:**
```bash
# Access SonarQube UI at http://localhost:9000
# Or use SonarQube API:
curl "http://localhost:9000/api/measures/component?component=Roller&metricKeys=ncloc,classes,complexity,cognitive_complexity,duplicated_lines_density,sqale_index"
```

#### For OOP Metrics (CK Suite):
**Tool: CK (Chidamber & Kemerer Java Tool)**
- You ran: `java -jar ck-0.7.0-jar-with-dependencies.jar <source-path> true 0 false`
- The tool analyzed bytecode/source and calculated:
  - **WMC** (Weighted Methods per Class): Sum of method complexities
  - **CBO** (Coupling Between Objects): Number of classes referenced
  - **RFC** (Response For Class): Number of methods invoked
  - **DIT** (Depth of Inheritance Tree): How many levels of inheritance
  - **NOC** (Number of Children): Direct subclasses
  - **LCOM** (Lack of Cohesion): How unrelated are the methods

**Output:** ckclass.csv and ckmethod.csv files

---

## 🔍 TOOLS YOU USED (Assignment Compliance)

### Assignment Says:
> "utilize appropriate tools such as CodeMR, Checkstyle, PMD, or **any other tools deemed suitable**"

### What You Used (CORRECT ✅):
1. **SonarQube** ✅ (Mandatory for Task 2A, also usable for Task 2B)
   - Provides: Size, complexity, duplication, technical debt metrics
   - Industry-standard, reliable, accurate

2. **CK Tool** ✅ (Specifically for OOP metrics)
   - Provides: WMC, CBO, RFC, DIT, NOC, LCOM
   - Academic-standard tool for Chidamber & Kemerer metrics
   - More accurate than general tools for OOP metrics

### Why You DON'T Need CodeMR/CheckStyle/PMD:
- ✅ SonarQube + CK provide **all required metrics**
- ✅ Assignment says "or any other tools deemed suitable"
- ✅ SonarQube is more comprehensive than CheckStyle/PMD
- ✅ CK is the best tool for C&K metrics specifically

**Your tool choice is VALID and APPROPRIATE.**

---

## 📊 WHAT'S MISSING? (Action Items)

### 🚨 CRITICAL - Missing Screenshots:

You need to take screenshots from SonarQube showing:

1. **Project Dashboard:**
   - Overall metrics (NCLOC, complexity, tech debt)
   - File: `sonarqube-dashboard.png`

2. **WeblogEntry Class Metrics:**
   - Shows NCLOC=621, functions=93, complexity=156, cognitive_complexity=99
   - File: `sonarqube-weblogentry.png`

3. **Issues/Code Smells Page:**
   - Shows deprecated API warnings (java:S1874, java:S1133)
   - Shows duplication issues (java:S1192)
   - File: `sonarqube-issues.png`

4. **Top 10 Complex Files:**
   - Shows LuceneIndexManager, WeblogEntry, etc.
   - File: `sonarqube-hotspots.png`

**How to get screenshots:**
1. Open http://localhost:9000
2. Navigate to Roller project
3. Take screenshots of:
   - Dashboard → Overview tab
   - Measures → Complexity → Files
   - Issues → Type: Code Smell
   - Code → WeblogEntry.java → Measures tab

### 📁 Where to Save Screenshots:
```
Working/03-task2/screenshots/
├── sonarqube-dashboard.png
├── sonarqube-weblogentry.png
├── sonarqube-issues.png
└── sonarqube-hotspots.png
```

**Commit these** and reference them in your markdown files!

---

## ✅ FINAL COMMIT CHECKLIST

### Files to Commit NOW:

```
Working/03-task2/
├── 02A-design-smells.md          ✅ READY
├── 02B-metrics.md                ✅ READY
├── ckclass.csv                   ✅ COMMIT (proves tool usage)
├── ckmethod.csv                  ✅ COMMIT (proves tool usage)
├── ck/
│   └── ck-summary.md             ✅ COMMIT (if exists)
└── screenshots/                  🚨 CREATE & COMMIT
    ├── sonarqube-dashboard.png   ❌ MISSING - TAKE NOW
    ├── sonarqube-weblogentry.png ❌ MISSING - TAKE NOW
    ├── sonarqube-issues.png      ❌ MISSING - TAKE NOW
    └── sonarqube-hotspots.png    ❌ MISSING - TAKE NOW
```

### Files to Exclude from Commit:
- ❌ `ck-0.7.0-jar-with-dependencies.jar` (tool binary, 17MB+)
- ❌ Any HTML reports from tools (too large)
- ❌ Temporary analysis files

---

## 🎯 UPDATED ACTION PLAN

### Step 1: Take Screenshots (15 minutes)
```bash
# Start SonarQube if not running
# Access http://localhost:9000
# Take 4 screenshots as listed above
# Save to Working/03-task2/screenshots/
```

### Step 2: Update 02A-design-smells.md (5 minutes)
Add screenshot references:

```markdown
## Evidence Screenshots
- SonarQube Dashboard: `screenshots/sonarqube-dashboard.png`
- WeblogEntry Metrics: `screenshots/sonarqube-weblogentry.png`
- Code Smell Issues: `screenshots/sonarqube-issues.png`
```

### Step 3: Update 02B-metrics.md (5 minutes)
Add screenshot references:

```markdown
## Tool Output Evidence
- SonarQube Dashboard: `screenshots/sonarqube-dashboard.png`
- CK Metrics: See `ckclass.csv` and `ckmethod.csv`
```

### Step 4: Commit Everything (5 minutes)
```bash
git add Working/03-task2/
git commit -m "feat: Add Task 2 screenshots and CK metrics data

- Added SonarQube dashboard screenshots
- Included CK tool outputs (ckclass.csv, ckmethod.csv)
- Documented 7 design smells with evidence
- Analyzed 6 metrics + CK suite (WMC, CBO, RFC, DIT, NOC, LCOM)

Task 2 complete with tool evidence"
git push
```

---

## 📝 ASSIGNMENT COMPLIANCE CHECK

| Requirement | Status | Evidence |
|-------------|--------|----------|
| **Task 2A: 5-7 design smells** | ✅ DONE | 7 smells in 02A-design-smells.md |
| **SonarQube mandatory** | ✅ DONE | Metrics cited, rules referenced |
| **Supplemental tools encouraged** | ✅ DONE | CK tool for OOP metrics |
| **Supporting evidence** | ⚠️ PARTIAL | Needs screenshots |
| **UML analysis evidence** | ✅ DONE | References to Task 1 UMLs |
| **Task 2B: 6 metrics** | ✅ DONE | 6 in 02B-metrics.md |
| **Tools stated** | ✅ DONE | SonarQube + CK documented |
| **OOP (CK) metrics** | ✅ DONE | WMC, CBO, RFC, DIT, NOC, LCOM |
| **Implications discussed** | ✅ DONE | For each metric |
| **Diverse metrics** | ✅ DONE | Size, complexity, duplication, debt, OOP |

**OVERALL: 90% COMPLETE** - Just need screenshots!

---

## 💡 ABOUT CSV FILES

### Should You Commit CSV Files?

**YES - Commit ckclass.csv and ckmethod.csv because:**

1. ✅ **Proves you ran the tool** (assignment compliance)
2. ✅ **Provides traceability** for your metrics claims
3. ✅ **Enables Task 3B comparison** (you'll re-run metrics after refactoring)
4. ✅ **Not too large** (~100-500 KB typical)
5. ✅ **Can be referenced in final report** without including full data

**Example reference in report:**
> "CK metrics were extracted using the CK tool (v0.7.0), analyzing 535 classes. Full data available in `Working/03-task2/ckclass.csv`. Summary statistics show WMC average of 18.73..."

### Files You DON'T Need to Submit/Commit:
- ❌ SonarQube server database
- ❌ Maven target/ directories
- ❌ IDE configuration files
- ❌ Tool JAR files (unless needed for custom scripts)

---

## 🎓 SUMMARY

### What You've Done Right:
✅ Used appropriate tools (SonarQube + CK)  
✅ Identified 7 design smells (exceeds requirement)  
✅ Analyzed 6 diverse metrics + CK suite  
✅ Discussed implications for each metric  
✅ Generated CSV data from CK tool  
✅ Documented tool usage clearly  

### What You Need to Do NOW:
🚨 Take 4 screenshots from SonarQube  
🚨 Save to `Working/03-task2/screenshots/`  
🚨 Update markdown files with screenshot references  
🚨 Commit everything (including CSV files)  

### For Final Report (Later):
📄 Convert markdown content to PDF sections  
📄 Include screenshot images  
📄 Add summary tables for metrics  
📄 Reference CSV files but don't include raw data  

**Time Estimate:** 30 minutes to complete all missing items

---

**Task 2 is 90% done. Take the screenshots and commit - you'll be at 100%!**
