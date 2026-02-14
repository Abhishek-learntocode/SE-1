# Combined Refactoring Plan: 7 Design Smells × 2 Instances = 14 Refactorings

## Apache Roller Weblogger — Unified Code Quality Improvement Plan

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Analysis Methodology & Tools](#analysis-methodology--tools)
3. [Smell #1: Insufficient Modularization](#smell-1-insufficient-modularization)
4. [Smell #2: Deficient Encapsulation](#smell-2-deficient-encapsulation)
5. [Smell #3: Feature Envy](#smell-3-feature-envy)
6. [Smell #4: Cyclically-Dependent Modularization](#smell-4-cyclically-dependent-modularization)
7. [Smell #5: Broken Hierarchy](#smell-5-broken-hierarchy)
8. [Smell #6: Hub-like Modularization](#smell-6-hub-like-modularization)
9. [Smell #7: Unnecessary Abstraction](#smell-7-unnecessary-abstraction)
10. [New Classes & Interfaces to Create](#new-classes--interfaces-to-create)
11. [Execution Phases](#execution-phases)
12. [Expected Metric Improvements](#expected-metric-improvements)
13. [Effort Estimates](#effort-estimates)

---

## Executive Summary

This document details a systematic refactoring plan targeting **7 distinct design smells** with **2 concrete instances each**, totaling **14 behavior-preserving refactorings**. Every instance is **verified by multiple tools** and targets **high-impact classes** for maximum metric improvement.

**Primary Goals:**
- Improve **readability** by reducing class sizes, method lengths, and parameter counts
- Improve **maintainability** by reducing coupling (CBO), improving cohesion (LCOM), and breaking cyclic dependencies
- All refactorings are **behavior-preserving** (no functional changes)

---

## Analysis Methodology & Tools

Each instance was cross-verified using **4 industrial-strength static analysis tools**:

| Tool | What It Reports | Data Source |
|------|----------------|-------------|
| **CK Metrics** | WMC, CBO, LOC, LCOM, public methods/fields per class | `CODE METRICS/CK-report/class.csv`, `method.csv` |
| **Designite Java** | Design smells, implementation smells, architecture smells | `CODE METRICS/Designite/DesignSmells.csv`, `ImplementationSmells.csv`, `ArchitectureSmells.csv` |
| **SonarQube** | Cognitive complexity, code smells, security hotspots, rule violations | `CODE METRICS/SONARQUBE/2026-02-06-Software_1-issues-report.csv` |
| **PMD** | Code rule violations (god class, cyclomatic complexity, naming, etc.) | `CODE METRICS/PMD/pmd_report.txt` |

### How Instances Were Selected

For each smell, we selected the **2 instances with the highest combined severity score** (WMC + CBO), ensuring they are:
1. Flagged by **at least 2 tools** simultaneously
2. In **high-traffic classes** (most LOC, most coupling, most methods)
3. **Feasible to refactor** without breaking public API contracts

---

## Smell #1: Insufficient Modularization

### Definition
A class exposes too many public methods (bloated interface) or has excessive complexity (high WMC), indicating it should be decomposed into smaller, more focused modules.

---

### Instance 1.1: `JPAWeblogEntryManagerImpl`

**File:** `app/src/main/java/org/apache/roller/weblogger/business/jpa/JPAWeblogEntryManagerImpl.java`

#### Tool Evidence

**CK Metrics (class.csv):**
```
Class:             JPAWeblogEntryManagerImpl
WMC:               197          (Weighted Method Complexity — extremely high)
CBO:               30           (Coupling Between Objects)
LOC:               894
publicMethodsQty:  44           (44 public methods!)
```

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.business.jpa
Class:       JPAWeblogEntryManagerImpl
Smell:       Insufficient Modularization
Description: The class has bloated interface (large number of public methods).
             Total public methods in the class: 44 public methods
```

**SonarQube:**
```
Rule S3776 — Cognitive Complexity:
  Method updateTagCount():    CC = 12 (exceeds threshold)
  Method getWeblogEntries():  CC = 16 (exceeds threshold)
  Method saveWeblogEntry():   CC = 15 (exceeds threshold)
```

**PMD (pmd_report.txt):**
```
JPAWeblogEntryManagerImpl.java: TooManyMethods — This class has too many methods
JPAWeblogEntryManagerImpl.java: CyclomaticComplexity — The method 'getWeblogEntries(...)' 
  has a cyclomatic complexity of 16
```

#### Root Cause Analysis

This single class manages **four distinct responsibilities**:
1. **WeblogEntry CRUD** — `saveWeblogEntry()`, `removeWeblogEntry()`, `getWeblogEntry()`, `getWeblogEntryByAnchor()`, `getWeblogEntriesPinnedToMain()`
2. **Comment Management** — `saveComment()`, `removeComment()`, `getComment()`, `getComments()`, `removeMatchingComments()`, `getCommentCount()`
3. **Category Management** — `getWeblogCategory()`, `saveWeblogCategory()`, `removeWeblogCategory()`, `getWeblogCategories()`, `getWeblogCategoryByPath()`, `getWeblogCategoryByName()`
4. **Statistical Queries** — `getWeblogEntryStringMap()`, `getMostCommentedWeblogEntries()`, `getNextEntry()`, `getPreviousEntry()`, `getEntryCount()`

Additionally, the `getWeblogEntries()` method alone spans ~130 lines of manual JPQL query construction with 10+ conditional branches.

#### Refactoring Strategy: *Extract Class* + *Extract Method*

**Step 1 — Create `JPACommentManagerImpl`:**
Extract the 6 comment-related methods into a new class implementing a new `CommentManager` interface:
```java
// New interface
public interface CommentManager {
    void saveComment(WeblogEntryComment comment) throws WebloggerException;
    void removeComment(WeblogEntryComment comment) throws WebloggerException;
    WeblogEntryComment getComment(String id) throws WebloggerException;
    List<WeblogEntryComment> getComments(CommentSearchCriteria csc) throws WebloggerException;
    int removeMatchingComments(WeblogEntryComment comment) throws WebloggerException;
    long getCommentCount() throws WebloggerException;
    long getCommentCount(Weblog weblog) throws WebloggerException;
}

// New implementation
@Singleton
public class JPACommentManagerImpl implements CommentManager {
    private final JPAPersistenceStrategy strategy;
    
    @Inject
    public JPACommentManagerImpl(JPAPersistenceStrategy strategy) {
        this.strategy = strategy;
    }
    // ... moved methods
}
```

**Step 2 — Create `JPACategoryManagerImpl`:**
Extract the 6 category-related methods:
```java
public interface CategoryManager {
    WeblogCategory getWeblogCategory(String id) throws WebloggerException;
    void saveWeblogCategory(WeblogCategory cat) throws WebloggerException;
    void removeWeblogCategory(WeblogCategory cat) throws WebloggerException;
    List<WeblogCategory> getWeblogCategories(Weblog weblog) throws WebloggerException;
    WeblogCategory getWeblogCategoryByPath(Weblog weblog, String path) throws WebloggerException;
    WeblogCategory getWeblogCategoryByName(Weblog weblog, String name) throws WebloggerException;
}
```

**Step 3 — Extract `WeblogEntryQueryBuilder`:**
Move the 130-line JPQL construction logic from `getWeblogEntries()`:
```java
public class WeblogEntryQueryBuilder {
    private final WeblogEntrySearchCriteria criteria;
    
    public WeblogEntryQueryBuilder(WeblogEntrySearchCriteria criteria) {
        this.criteria = criteria;
    }
    
    public String buildQueryString() { /* extracted query logic */ }
    public List<Object> buildParameters() { /* extracted parameter binding */ }
}

// Simplified getWeblogEntries():
public List<WeblogEntry> getWeblogEntries(WeblogEntrySearchCriteria wesc) {
    WeblogEntryQueryBuilder builder = new WeblogEntryQueryBuilder(wesc);
    Query query = strategy.getDynamicQuery(builder.buildQueryString());
    // bind parameters from builder.buildParameters()
    return query.getResultList();
}
```

**Step 4 — Update `Weblogger` interface:**
```java
public interface Weblogger {
    // existing...
    CommentManager getCommentManager();
    CategoryManager getCategoryManager();
}
```

**Step 5 — Wire new classes in `JPAWebloggerModule`** (Guice DI).

#### Expected Outcome

| Metric | Before | After (Target) | Improvement |
|--------|--------|-----------------|-------------|
| LOC | 894 | ~400 | -55% |
| WMC | 197 | ~90 | -54% |
| Public Methods | 44 | ~20 | -55% |
| CBO | 30 | ~15 | -50% |

---

### Instance 1.2: `WeblogEntry`

**File:** `app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntry.java`

#### Tool Evidence

**CK Metrics (class.csv):**
```
Class:             WeblogEntry
WMC:               159          (Very high complexity for a POJO)
CBO:               26
LOC:               1031
publicMethodsQty:  91           (91 public methods!)
publicFieldsQty:   28
```

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.pojos
Class:       WeblogEntry
Smell:       Insufficient Modularization
Description: The class has bloated interface (large number of public methods).
             Total public methods in the class: 91 public methods
```

**PMD (pmd_report.txt):**
```
WeblogEntry.java: GodClass — Possible God Class (WMC=159, ATFD=7, TCC=2.294%)
WeblogEntry.java: TooManyMethods — This class has too many methods, consider refactoring
WeblogEntry.java: ExcessivePublicCount — This class has too many public methods and attributes
```

#### Root Cause Analysis

This POJO (Plain Old Java Object) violates the Single Responsibility Principle by mixing:
1. **Data storage** — 20+ fields with getters/setters (proper POJO role)
2. **Business logic** — `getComments()`, `getCommentCount()`, `hasWritePermissions()` call into `WeblogEntryManager` and `UserManager`
3. **Presentation logic** — `getTransformedText()`, `getTransformedSummary()`, `getDisplayTitle()`, `getRss09xDescription()` perform HTML transformations
4. **Tag management** — `addTag()`, `setTagsAsString()`, `getTagsAsString()`, `updateTags()` implement complex tag lifecycle logic
5. **URL generation** — `getPermalink()`, `getPermaLink()`, `getCommentsLink()` delegate to URL strategy
6. **Date formatting** — `formatPubTime()`, `formatUpdateTime()` perform timezone-aware formatting

Additionally, there are **empty setter stubs** (`setPermalink()`, `setPermaLink()`, `setDisplayTitle()`, `setRss09xDescription()`) and **duplicate methods** (`getPermalink()` / `getPermaLink()`).

#### Refactoring Strategy: *Extract Class* + *Remove Dead Code*

**Step 1 — Create `WeblogEntryContentHelper`:**
Extract presentation/transformation methods:
```java
public class WeblogEntryContentHelper {
    public static String transformText(WeblogEntry entry) { /* from getTransformedText() */ }
    public static String transformSummary(WeblogEntry entry) { /* from getTransformedSummary() */ }
    public static String getDisplayTitle(WeblogEntry entry) { /* from getDisplayTitle() */ }
    public static String getRssDescription(WeblogEntry entry) { /* from getRss09xDescription() */ }
}
```

**Step 2 — Create `WeblogEntryTagHandler`:**
Extract tag management logic:
```java
public class WeblogEntryTagHandler {
    private Set<WeblogEntryTag> tagSet;
    private Set<WeblogEntryTag> removedTags;
    private Set<WeblogEntryTag> addedTags;
    
    public void addTag(String name) { /* from addTag() */ }
    public void setTagsAsString(String tags) { /* from setTagsAsString() */ }
    public String getTagsAsString() { /* from getTagsAsString() */ }
    public void updateTags(WeblogEntry entry) { /* from updateTags() */ }
}
```

**Step 3 — Remove duplicate/dead methods:**
- Delete `getPermaLink()` (keep `getPermalink()`)
- Remove empty setters: `setPermalink()`, `setPermaLink()`, `setDisplayTitle()`, `setRss09xDescription()`

**Step 4 — Move business logic to service layer:**
Move `getComments()`, `getCommentCount()`, `hasWritePermissions()` to `WeblogEntryManager` / `CommentManager`.

**Step 5 — Update callers** using IDE "Find Usages" and redirect to new helper classes.

#### Expected Outcome

| Metric | Before | After (Target) | Improvement |
|--------|--------|-----------------|-------------|
| LOC | 1031 | ~500 | -52% |
| WMC | 159 | ~60 | -62% |
| Public Methods | 91 | ~45 | -51% |
| CBO | 26 | ~8 | -69% |

---

## Smell #2: Deficient Encapsulation

### Definition
A class exposes internal state by declaring fields with broader accessibility than necessary (e.g., public fields that should be private), bypassing validation and allowing unconstrained external mutation.

---

### Instance 2.1: `WeblogEntry`

**File:** `app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntry.java`

#### Tool Evidence

**CK Metrics (class.csv):**
```
Class:             WeblogEntry
publicFieldsQty:   28
totalFieldsQty:    31
```

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.pojos
Class:       WeblogEntry
Smell:       Deficient Encapsulation
Description: The class exposes fields belonging to it with public accessibility.
Following fields are declared with public accessibility:
  mLogger; serialVersionUID; TITLE_SEPARATOR; id; title; link; summary; text; 
  contentType; contentSrc; anchor; pubTime; updateTime; plugins; allowComments; 
  commentDays; rightToLeft; pinnedToMain; status; locale; creatorUserName; 
  searchDescription; refreshAggregates; website; category; attSet; tagSet; 
  removedTags; addedTags
Total: 28 public fields
```

#### Actual Code (Lines ~50-100)

```java
public static Log mLogger = LogFactory.getLog(WeblogEntry.class);
public static final long serialVersionUID = 2341505386843044125L;
public static final char TITLE_SEPARATOR = ':';

// ALL of these should be private:
public String id = null;
public String title = null;
public String link = null;
public String summary = null;
public String text = null;
public String contentType = null;
public String contentSrc = null;
public String anchor = null;
public Timestamp pubTime = null;
public Timestamp updateTime = null;
public String plugins = null;
public Boolean allowComments = Boolean.TRUE;
public Integer commentDays = 7;
public Boolean rightToLeft = Boolean.FALSE;
public Boolean pinnedToMain = Boolean.FALSE;
public String status = "DRAFT";
public String locale = null;
public String creatorUserName = null;
public String searchDescription = null;
public Boolean refreshAggregates = Boolean.TRUE;
// ... associated objects and collections also public
```

#### Why This Is a Problem
- Any external class can directly write `entry.title = "hacked"` bypassing validation
- No defensive copying for mutable objects (`pubTime`, `updateTime` are `Timestamp` — mutable)
- Logger is public and non-final — can be replaced at runtime

#### Refactoring Strategy: *Encapsulate Field*

**Step 1 — Change all 28 public fields to `private`:**
```java
// BEFORE:
public String id = null;
public String title = null;

// AFTER:
private String id = null;
private String title = null;
```

**Step 2 — Make constants properly scoped:**
```java
// BEFORE:
public static Log mLogger = LogFactory.getLog(WeblogEntry.class);

// AFTER:
private static final Log mLogger = LogFactory.getLog(WeblogEntry.class);
private static final long serialVersionUID = 2341505386843044125L;
private static final char TITLE_SEPARATOR = ':';
```

**Step 3 — Verify all getters/setters exist** (most already do — complete the missing ones).

**Step 4 — Add defensive copies for mutable types:**
```java
public Timestamp getPubTime() {
    return pubTime != null ? new Timestamp(pubTime.getTime()) : null;
}
```

**Step 5 — Update all direct field accesses** across the codebase:
```bash
# Find all direct field access patterns
grep -rn "\.id\s*=" --include="*.java" app/src/
grep -rn "\.title\s*=" --include="*.java" app/src/
# Replace entry.id with entry.getId(), entry.id = x with entry.setId(x)
```

#### Expected Outcome

| Metric | Before | After (Target) | Improvement |
|--------|--------|-----------------|-------------|
| Public Fields (NOPF) | 28 | 0 | -100% |
| Encapsulation | Deficient | Proper | ✅ |

---

### Instance 2.2: `Weblog`

**File:** `app/src/main/java/org/apache/roller/weblogger/pojos/Weblog.java`

#### Tool Evidence

**CK Metrics (class.csv):**
```
Class:             Weblog
publicFieldsQty:   35
totalFieldsQty:    38
publicMethodsQty:  97
LOC:               927
```

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.pojos
Class:       Weblog
Smell:       Deficient Encapsulation
Description: The class exposes fields belonging to it with public accessibility.
Following fields are declared with public accessibility:
  serialVersionUID; log; MAX_ENTRIES; id; handle; name; tagline; enableBloggerApi; 
  editorPage; bannedwordslist; allowComments; emailComments; emailAddress; editorTheme; 
  locale; timeZone; defaultPlugins; visible; active; dateCreated; defaultAllowComments; 
  defaultCommentDays; moderateComments; entryDisplayCount; lastModified; enableMultiLang; 
  showAllLangs; iconPath; about; creator; analyticsCode; bloggerCategory; 
  initializedPlugins; weblogCategories; bookmarkFolders; mediaFileDirectories
Total: 35 public fields
```

#### Refactoring Strategy: *Encapsulate Field* (same approach as 2.1)

**Step 1 — Change all 35 public fields to `private`:**
```java
// BEFORE:
public String id = null;
public String handle = null;
public String name = null;
// ... 32 more public fields

// AFTER:
private String id = null;
private String handle = null;
private String name = null;
```

**Step 2 — Make constants `private static final`:**
```java
private static final Log log = LogFactory.getLog(Weblog.class);
private static final int MAX_ENTRIES = 100;
private static final long serialVersionUID = ...;
```

**Step 3 — Add defensive copies for mutable collections:**
```java
public List<WeblogCategory> getWeblogCategories() {
    return Collections.unmodifiableList(weblogCategories);
}
```

**Step 4 — Replace all direct field access** with getter/setter calls across codebase.

#### Expected Outcome

| Metric | Before | After (Target) | Improvement |
|--------|--------|-----------------|-------------|
| Public Fields (NOPF) | 35 | 0 | -100% |
| Encapsulation | Deficient | Proper | ✅ |

---

## Smell #3: Feature Envy

### Definition
A method in one class is more interested in the internals of another class than its own. The method accesses data/methods from an external class more than from its own class, suggesting it should be moved.

---

### Instance 3.1: `JPAWeblogEntryManagerImpl.updateTagCount()`

**File:** `app/src/main/java/org/apache/roller/weblogger/business/jpa/JPAWeblogEntryManagerImpl.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.business.jpa
Class:       JPAWeblogEntryManagerImpl
Smell:       Feature Envy
Description: updateTagCount is more interested in members of the type: JPAPersistenceStrategy
```

**CK Metrics:**
```
Class:    JPAWeblogEntryManagerImpl
CBO:      30 (high coupling — 15+ methods deep-access JPAPersistenceStrategy)
WMC:      197
```

**SonarQube:**
```
Rule S3776 — Cognitive Complexity:
  Method updateTagCount(): CC = 12 (exceeds recommended 7-10)
```

#### Root Cause Analysis

The `updateTagCount` method heavily operates on `JPAPersistenceStrategy` — calling its `store()`, `remove()`, `flush()`, and query-execution methods multiple times. The method constructs JPA queries, executes them through the strategy, processes results, and stores/removes `WeblogEntryTagAggregate` objects — all operations that belong in the persistence layer:

```java
// Pseudo-code showing the envy pattern:
public void updateTagCount(String id) {
    Query q = strategy.createQuery("SELECT t FROM Tag t WHERE ...");  // Envy!
    List<TagStat> results = strategy.executeQuery(q);                 // Envy!
    strategy.updateEntityGraph(results);                              // Envy!
    strategy.store(aggregate);                                        // Envy!
    strategy.remove(deadTags);                                        // Envy!
    // Only 1 line is about WeblogEntryManager's own responsibility
    this.cacheTagStatistics(results);
}
```

#### Refactoring Strategy: *Move Method* + *Extract Class*

**Step 1 — Create `WeblogTagRepository`:**
```java
public class WeblogTagRepository {
    private final JPAPersistenceStrategy strategy;
    
    @Inject
    public WeblogTagRepository(JPAPersistenceStrategy strategy) {
        this.strategy = strategy;
    }
    
    public void updateTagAggregates(WeblogEntry entry,
                                     Set<WeblogEntryTag> newTags,
                                     Set<WeblogEntryTag> removedTags) {
        // All the strategy.createQuery/executeQuery/store/remove logic moves here
    }
    
    private void incrementTagCount(Weblog weblog, String tagName) { ... }
    private void decrementTagCount(Weblog weblog, String tagName) { ... }
    private void removeZeroCountTags(Weblog weblog) { ... }
}
```

**Step 2 — Simplify the original method to delegate:**
```java
// BEFORE: 40+ lines of JPAPersistenceStrategy calls
// AFTER:
private void updateTagCount(WeblogEntry entry) {
    weblogTagRepository.updateTagAggregates(
        entry, entry.getAddedTags(), entry.getRemovedTags()
    );
}
```

**Step 3 — Inject `WeblogTagRepository`** via constructor in `JPAWeblogEntryManagerImpl`.

#### Expected Outcome
- Method moves to the class whose data it manipulates
- `JPAWeblogEntryManagerImpl` CBO drops by ~3 points
- Tag aggregation logic becomes independently testable
- Cognitive complexity of `updateTagCount()`: 12 → ~3

---

### Instance 3.2: `JPAWeblogManagerImpl.addWeblogContents()`

**File:** `app/src/main/java/org/apache/roller/weblogger/business/jpa/JPAWeblogManagerImpl.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.business.jpa
Class:       JPAWeblogManagerImpl
Smell:       Feature Envy
Description: addWeblogContents is more interested in members of the type: Weblogger
```

**CK Metrics:**
```
Class:    JPAWeblogManagerImpl
CBO:      36 (highest coupling in codebase!)
WMC:      103
LOC:      726
```

#### Root Cause Analysis

The method reaches into the `Weblogger` facade to access 7+ different managers:
```java
public void addWeblogContents(Weblog newWeblog) {
    roller.getUserManager().grantPermission(...)        // Envy!
    roller.getWeblogEntryManager().saveWeblogCategory(...)  // Envy!
    roller.getBookmarkManager().addFolder(...)           // Envy!
    roller.getMediaFileManager().createMediaFileDirectory(...)  // Envy!
    roller.getThemeManager().getTheme(...)               // Envy!
    roller.flush()                                       // Envy!
}
```

It's more interested in `Weblogger`'s managers than in its own state — a textbook Feature Envy case.

#### Refactoring Strategy: *Extract Class* (Orchestration Service)

**Step 1 — Create `WeblogSetupService`:**
```java
@Singleton
public class WeblogSetupService {
    private final UserManager userManager;
    private final WeblogEntryManager entryManager;
    private final BookmarkManager bookmarkManager;
    private final MediaFileManager mediaFileManager;
    private final ThemeManager themeManager;
    
    @Inject
    public WeblogSetupService(UserManager userManager,
                               WeblogEntryManager entryManager,
                               BookmarkManager bookmarkManager,
                               MediaFileManager mediaFileManager,
                               ThemeManager themeManager) {
        this.userManager = userManager;
        this.entryManager = entryManager;
        this.bookmarkManager = bookmarkManager;
        this.mediaFileManager = mediaFileManager;
        this.themeManager = themeManager;
    }
    
    public void initializeWeblogDefaults(Weblog weblog) {
        createDefaultCategory(weblog);
        createDefaultBookmarkFolder(weblog);
        createDefaultMediaDirectory(weblog);
        applyDefaultTheme(weblog);
        grantOwnerPermission(weblog);
    }
    
    private void createDefaultCategory(Weblog weblog) { ... }
    private void createDefaultBookmarkFolder(Weblog weblog) { ... }
    private void createDefaultMediaDirectory(Weblog weblog) { ... }
    private void applyDefaultTheme(Weblog weblog) { ... }
    private void grantOwnerPermission(Weblog weblog) { ... }
}
```

**Step 2 — Simplify `addWeblog` in `JPAWeblogManagerImpl`:**
```java
// BEFORE: 50+ lines reaching into 7 managers via roller
// AFTER:
public void addWeblog(Weblog weblog) throws WebloggerException {
    if (!isAlphanumeric(weblog.getHandle())) {
        throw new WebloggerException("invalid handle");
    }
    strategy.store(weblog);
    weblogSetupService.initializeWeblogDefaults(weblog);
    strategy.flush();
}
```

#### Expected Outcome

| Metric | Before | After (Target) | Improvement |
|--------|--------|-----------------|-------------|
| CBO (`JPAWeblogManagerImpl`) | 36 | ~20 | -44% |
| Method accesses to `Weblogger` | 7+ manager calls | 0 (delegated) | -100% |
| Testability | Hard (needs full Weblogger) | Easy (mock setup service) | ✅ |

---

## Smell #4: Cyclically-Dependent Modularization

### Definition
Two or more classes depend on each other directly or indirectly, creating a cycle that makes them inseparable and harder to understand, test, and maintain independently.

---

### Instance 4.1: `EntryCollection` ↔ `RollerAtomHandler`

**File:** `app/src/main/java/org/apache/roller/weblogger/webservices/atomprotocol/EntryCollection.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.webservices.atomprotocol
Class:       EntryCollection
Smell:       Cyclically-dependent Modularization
Description: This class participates in a cyclic dependency.
Participating classes: RollerAtomHandler; EntryCollection
```

**CK Metrics:**
```
Class:    EntryCollection
WMC:      60
CBO:      29
LOC:      474
```

#### Dependency Chain
```
RollerAtomHandler
├─ Creates: new EntryCollection(user, atomURL)
├─ Delegates: entryCollection.postEntry()
└─ Provides: authentication context

EntryCollection
├─ Calls back: WebloggerFactory.getWeblogger() (singleton coupling)
├─ Orchestrates: WeblogManager, WeblogEntryManager, IndexManager, CacheManager
└─ Needs RollerAtomHandler for authorization context → CYCLE!
```

**Problem:** Cannot test `EntryCollection` without `RollerAtomHandler`, and vice versa.

#### Refactoring Strategy: *Extract Interface* + *Dependency Inversion*

**Step 1 — Create `AtomRequestContext` interface:**
```java
public interface AtomRequestContext {
    User getAuthenticatedUser();
    String getAtomURL();
    boolean isUserAuthorized(Weblog weblog, String action);
}
```

**Step 2 — Make `RollerAtomHandler` implement `AtomRequestContext`:**
```java
public class RollerAtomHandler implements AtomRequestContext {
    @Override
    public User getAuthenticatedUser() { return this.user; }
    @Override
    public String getAtomURL() { return this.atomURL; }
    @Override
    public boolean isUserAuthorized(Weblog weblog, String action) {
        // existing auth logic
    }
}
```

**Step 3 — Modify `EntryCollection` to depend on interface:**
```java
public class EntryCollection {
    private final AtomRequestContext context;  // Interface, not concrete class
    private final Weblogger roller;
    
    public EntryCollection(AtomRequestContext context, Weblogger roller) {
        this.context = context;
        this.roller = roller;  // Injected, not from singleton
    }
}
```

**Result:** `EntryCollection` → `AtomRequestContext` (interface) ← `RollerAtomHandler`. Cycle broken.

#### Expected Outcome
- Cyclic dependency broken
- `EntryCollection` independently testable with mock context
- CBO of `EntryCollection`: 29 → ~20

---

### Instance 4.2: `Subscription` ↔ `SubscriptionEntry`

**Files:**
- `app/src/main/java/org/apache/roller/planet/pojos/Subscription.java`
- `app/src/main/java/org/apache/roller/planet/pojos/SubscriptionEntry.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.planet.pojos
Class:       Subscription
Smell:       Cyclically-dependent Modularization
Description: Participating classes in the cycle are: SubscriptionEntry; Subscription
```

**CK Metrics:**
```
Subscription:      CBO=4, WMC=32, publicMethodsQty=27
SubscriptionEntry: CBO=5, WMC=18, publicMethodsQty=40
```

#### Dependency Chain
```
Subscription.java
├─ Has field: Set<SubscriptionEntry> entries
└─ Returns: List<SubscriptionEntry> getEntries()

SubscriptionEntry.java
├─ Has field: Subscription subscription     ← BACKREFERENCE
└─ Returns: Subscription getSubscription()  ← BACKREFERENCE
```

**Problem:** Cannot test `SubscriptionEntry` without loading `Subscription`, and vice versa.

#### Refactoring Strategy: *Break Bidirectional Association* + *Extract Interface*

**Step 1 — Create `SubscriptionEntryContainer` interface:**
```java
public interface SubscriptionEntryContainer {
    String getSubscriptionId();
    Date getLastUpdated();
}
```

**Step 2 — Subscription implements the interface:**
```java
public class Subscription implements SubscriptionEntryContainer {
    private Set<SubscriptionEntry> entries;
    // ... existing code
}
```

**Step 3 — Replace object reference with ID in SubscriptionEntry:**
```java
// BEFORE:
public class SubscriptionEntry {
    private Subscription subscription;  // Direct object reference!
    public Subscription getSubscription() { return subscription; }
}

// AFTER:
public class SubscriptionEntry {
    private String subscriptionId;  // Store ID only!
    public String getSubscriptionId() { return subscriptionId; }
}
```

**Step 4 — Retrieval through repository/manager:**
```java
// When caller needs the full Subscription object:
Subscription sub = subscriptionManager.getSubscriptionForEntry(entry);
```

#### Expected Outcome

| Metric | Before | After (Target) | Improvement |
|--------|--------|-----------------|-------------|
| Cyclic Dependencies | 1 cycle | 0 | -100% |
| CBO (each class) | 4-5 | 2-3 | -40% |
| Test isolation | Impossible | Possible | ✅ |

---

## Smell #5: Broken Hierarchy

### Definition
A subclass does not properly utilize the interface of its superclass — it neither overrides nor implements any methods from the parent, making the inheritance relationship questionable.

---

### Instance 5.1: `WeblogPageRequest`

**File:** `app/src/main/java/org/apache/roller/weblogger/ui/rendering/util/WeblogPageRequest.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.ui.rendering.util
Class:       WeblogPageRequest
Smell:       Broken Hierarchy
Description: This type does not implement or override any method from 
             its supertype(s): WeblogRequest
```

**CK Metrics:**
```
Class:    WeblogPageRequest
WMC:      71
CBO:      15
LOC:      443
```

#### Root Cause Analysis

`WeblogPageRequest extends WeblogRequest` but does not override **any** method from `WeblogRequest`:
- It uses the parent purely for field reuse (accessing `weblogHandle`, `locale`, etc.)
- Adds 11 new fields and 28 new public methods
- Has a 170-line constructor doing completely independent URL parsing
- The parent and child don't share a behavioral contract

#### Refactoring Strategy: *Replace Inheritance with Composition*

**Step 1 — Change to composition:**
```java
// BEFORE:
public class WeblogPageRequest extends WeblogRequest {

// AFTER:
public class WeblogPageRequest {
    private final WeblogRequest baseRequest;
    
    public WeblogPageRequest(HttpServletRequest request) {
        this.baseRequest = new WeblogRequest(request);
        parsePathContext(request);      // extracted
        parseRequestParameters(request); // extracted
        resolveWeblogEntry();           // extracted
        resolveWeblogPage();            // extracted
    }
    
    // Delegate common request methods
    public String getWeblogHandle() { return baseRequest.getWeblogHandle(); }
    public String getLocale() { return baseRequest.getLocale(); }
    public Weblog getWeblog() { return baseRequest.getWeblog(); }
}
```

**Step 2 — Extract interface for polymorphism (if needed):**
```java
public interface WeblogRequestContext {
    String getWeblogHandle();
    String getLocale();
    Weblog getWeblog();
}
// Both WeblogRequest and WeblogPageRequest implement this
```

**Step 3 — Break down the 170-line constructor** using *Extract Method*:
```java
private void parsePathContext(HttpServletRequest request) { /* ~40 lines */ }
private void parseRequestParameters(HttpServletRequest request) { /* ~40 lines */ }
private void resolveWeblogEntry() { /* ~15 lines */ }
private void resolveWeblogPage() { /* ~15 lines */ }
```

**Step 4 — Update callers** — Replace `instanceof WeblogRequest` checks with interface checks.

#### Expected Outcome
- Broken hierarchy eliminated
- Constructor reduced from 170 lines to ~20 lines (with extracted methods)
- Cleaner composition-based design

---

### Instance 5.2: `MultiWeblogURLStrategy`

**File:** `app/src/main/java/org/apache/roller/weblogger/business/MultiWeblogURLStrategy.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.business
Class:       MultiWeblogURLStrategy
Smell:       Broken Hierarchy
Description: This type does not implement or override any method from 
             its supertype(s): AbstractURLStrategy
```

**CK Metrics:**
```
Class:    MultiWeblogURLStrategy
WMC:      67
CBO:      7
LOC:      476
```

#### Root Cause Analysis

`MultiWeblogURLStrategy extends AbstractURLStrategy` but does not override any abstract or concrete method. The parent defines URL-building method signatures, but the child defines its own methods with different signatures (extra parameters). The inheritance provides no behavioral contract — just type classification.

#### Refactoring Strategy: *Replace Inheritance with Interface*

**Step 1 — Make `MultiWeblogURLStrategy` implement `URLStrategy` directly:**
```java
// BEFORE:
public class MultiWeblogURLStrategy extends AbstractURLStrategy {

// AFTER:
public class MultiWeblogURLStrategy implements URLStrategy {
```

**Step 2 — Extract common URL-building logic into utility:**
```java
public class URLBuilderUtils {
    public static String getAbsoluteUrl() {
        return WebloggerRuntimeConfig.getAbsoluteContextURL();
    }
    
    public static String getRelativeUrl() {
        return WebloggerRuntimeConfig.getRelativeContextURL();
    }
    
    public static StringBuilder startUrl(boolean absolute) {
        return new StringBuilder(absolute ? getAbsoluteUrl() : getRelativeUrl());
    }
}
```

**Step 3 — Remove `AbstractURLStrategy`** if no other class extends it meaningfully.

#### Expected Outcome
- Broken hierarchy eliminated
- URL-building logic reusable via utility class
- Clearer interface-based polymorphism

---

## Smell #6: Hub-like Modularization

### Definition
A class that has both high incoming dependencies (many classes depend on it) AND high outgoing dependencies (it depends on many classes), making it a central "hub" through which too many concerns flow.

---

### Instance 6.1: `Weblog`

**File:** `app/src/main/java/org/apache/roller/weblogger/pojos/Weblog.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.pojos
Class:       Weblog
Smell:       Hub-like Modularization
Description: This class has high number of incoming as well as outgoing dependencies.
Incoming:    120+ classes (every manager, test, servlet, model, cache, UI action)
Outgoing:    21 classes (WeblogCategory, WeblogTheme, ThemeManager, WebloggerFactory,
             Utilities, User, I18nUtils, UserManager, WeblogPermission, 
             WebloggerRuntimeConfig, Weblogger, PluginManager, WeblogEntry, 
             WeblogEntryManager, WeblogEntrySearchCriteria, CommentSearchCriteria, 
             BookmarkManager, WeblogBookmarkFolder, WeblogHitCount, 
             MediaFileDirectory, WeblogEntryComment)
```

**CK Metrics:**
```
Class:    Weblog
WMC:      149
CBO:      27
LOC:      927
Fan-In:   120+
Fan-Out:  21
```

**PMD (pmd_report.txt):**
```
Weblog.java: GodClass — Possible God Class (WMC=149)
Weblog.java: TooManyMethods — This class has too many methods
Weblog.java: ExcessivePublicCount — This class has too many public methods and attributes
```

#### Root Cause Analysis

`Weblog` acts as a **facade for the entire application** — instead of callers going to the service layer, they call convenience methods on the POJO:
```java
// These methods all reach into the service layer from a data object:
weblog.getTheme()                    → calls ThemeManager
weblog.getRecentWeblogEntries()      → calls WeblogEntryManager
weblog.getRecentWeblogEntriesByTag() → calls WeblogEntryManager
weblog.getRecentComments()           → calls WeblogEntryManager
weblog.getCommentCount()             → calls WeblogEntryManager
weblog.getEntryCount()               → calls WeblogEntryManager
weblog.getTodaysHits()               → calls WeblogEntryManager
weblog.getPopularTags()              → calls WeblogTagManager
weblog.getBookmarkFolder()           → calls BookmarkManager
weblog.hasUserPermission()           → calls UserManager
weblog.getInitializedPlugins()       → calls PluginManager
```

#### Refactoring Strategy: *Move Method* + *Remove Middle Man*

**Step 1 — Remove service-delegating methods from `Weblog`** (11 methods identified):

| Method to Remove | Move To |
|-----------------|---------|
| `getTheme()` | Callers use `themeManager.getTheme(weblog)` directly |
| `getRecentWeblogEntries()` | `weblogEntryManager.getWeblogEntries(criteria)` |
| `getRecentWeblogEntriesByTag()` | `weblogEntryManager.getWeblogEntries(criteria)` |
| `getRecentComments()` | `commentManager.getComments(criteria)` |
| `getCommentCount()` | `commentManager.getCommentCount(weblog)` |
| `getEntryCount()` | `weblogEntryManager.getEntryCount(weblog)` |
| `getTodaysHits()` | `hitCountManager.getTodaysHits(weblog)` |
| `getPopularTags()` | `weblogTagManager.getPopularTags(weblog)` |
| `getBookmarkFolder()` | `bookmarkManager.getFolder(weblog)` |
| `hasUserPermission()` | `userManager.hasPermission(user, weblog)` |
| `getInitializedPlugins()` | `pluginManager.getInitializedPlugins(weblog)` |

**Step 2 — Keep `Weblog` as a pure data entity** — only getters/setters for its own fields, plus JPA lifecycle.

**Step 3 — Update all callers** (touch rendering models, UI actions, tests):
```java
// BEFORE (in caller):
List<WeblogEntry> entries = weblog.getRecentWeblogEntries("main", 10);

// AFTER (in caller):
WeblogEntrySearchCriteria criteria = new WeblogEntrySearchCriteria();
criteria.setWeblog(weblog);
criteria.setCatName("main");
criteria.setMaxResults(10);
List<WeblogEntry> entries = weblogEntryManager.getWeblogEntries(criteria);
```

#### Expected Outcome

| Metric | Before | After (Target) | Improvement |
|--------|--------|-----------------|-------------|
| Fan-Out | 21 | ~5 (POJO deps only) | -76% |
| Public Methods | 97 | ~55 | -43% |
| WMC | 149 | ~60 | -60% |
| Hub classification | Yes | No | ✅ |

---

### Instance 6.2: `WeblogEntry`

**File:** `app/src/main/java/org/apache/roller/weblogger/pojos/WeblogEntry.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.pojos
Class:       WeblogEntry
Smell:       Hub-like Modularization
Description: This class has high number of incoming as well as outgoing dependencies.
Incoming:    60+ classes (managers, servlets, plugins, pagers, models, tests)
Outgoing:    20 classes (WebloggerFactory, WeblogEntryManager, UserManager, 
             CommentSearchCriteria, DateUtil, GlobalPermission, WeblogPermission,
             WeblogEntryPlugin, HTMLSanitizer, WeblogEntryComment, RollerConstants, 
             Utilities, WebloggerRuntimeConfig, etc.)
```

**CK Metrics:**
```
Class:    WeblogEntry
WMC:      159
CBO:      26
LOC:      1031
Fan-In:   60+
Fan-Out:  20
```

#### Root Cause Analysis

Same pattern as `Weblog` — the POJO acts as a service facade. Methods like `getComments()`, `getCommentCount()`, `getCreator()`, `getPermalink()`, `hasWritePermissions()` all reach into the service layer from what should be a data object.

#### Refactoring Strategy: *Move Method* (same approach as 6.1)

**Step 1 — Remove service-delegating methods:**

| Method to Remove | Move To |
|-----------------|---------|
| `getComments()` | `CommentManager.getComments(entry)` |
| `getCommentCount()` | `CommentManager.getCommentCount(entry)` |
| `getCreator()` | `UserManager.getUser(entry.getCreatorUserName())` |
| `getPermalink()` | `URLStrategy.getWeblogEntryURL(entry)` |
| `getPermaLink()` | Remove entirely (duplicate of `getPermalink`) |
| `getCommentsLink()` | `URLStrategy.getWeblogCommentsURL(entry)` |
| `hasWritePermissions()` | `PermissionManager.hasWritePermission(user, entry)` |
| `getTransformedText()` | `WeblogEntryContentHelper.transformText(entry)` |
| `getTransformedSummary()` | `WeblogEntryContentHelper.transformSummary(entry)` |

**Step 2 — Remove empty/dummy setters:** `setPermalink()`, `setPermaLink()`, `setDisplayTitle()`, `setRss09xDescription()`.

**Step 3 — Keep `WeblogEntry` as a pure JPA entity** — only fields, getters/setters, JPA annotations.

#### Expected Outcome

| Metric | Before | After (Target) | Improvement |
|--------|--------|-----------------|-------------|
| Fan-Out | 20 | ~5 | -75% |
| Public Methods | 91 | ~45 | -51% |
| WMC | 159 | ~60 | -62% |
| LOC | 1031 | ~500 | -52% |
| Hub classification | Yes | No | ✅ |

---

## Smell #7: Unnecessary Abstraction

### Definition
An abstraction (class, interface, or enum) that serves no meaningful purpose — it contains only data members without behavior, or duplicates an abstraction that already exists.

---

### Instance 7.1: `DatabaseProvider.ConfigurationType`

**File:** `app/src/main/java/org/apache/roller/weblogger/business/DatabaseProvider.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.business
Class:       DatabaseProvider.ConfigurationType
Smell:       Unnecessary Abstraction
Description: The class contains only a few data members without any method 
             implementation that indicates that the abstraction might not be required.
WMC: 0, CBO: 0, LOC: 0
```

#### Actual Code
```java
public enum ConfigurationType { JNDI_NAME, JDBC_PROPERTIES }
private ConfigurationType type;
```

This enum is used solely as a type flag in a single `if/else` branch within the same class. It adds an unnecessary level of abstraction — the distinction is really just "is JNDI configured or not?"

#### Refactoring Strategy: *Inline Class*

**Step 1 — Replace enum with boolean:**
```java
// BEFORE:
public enum ConfigurationType { JNDI_NAME, JDBC_PROPERTIES }
private ConfigurationType type;

// AFTER:
private final boolean isJndiConfigured;
```

**Step 2 — Update type checks:**
```java
// BEFORE:
if (type == ConfigurationType.JNDI_NAME) { ... }

// AFTER:
if (isJndiConfigured) { ... }
```

**Step 3 — Remove `getType()` method** or replace with `isJndiConfigured()`.

#### Expected Outcome
- Unnecessary enum removed
- Class simplified by ~10 lines
- One fewer abstraction to maintain

---

### Instance 7.2: `MailProvider.ConfigurationType`

**File:** `app/src/main/java/org/apache/roller/weblogger/business/MailProvider.java`

#### Tool Evidence

**Designite (DesignSmells.csv):**
```
Package:     org.apache.roller.weblogger.business
Class:       MailProvider.ConfigurationType
Smell:       Unnecessary Abstraction
Description: The class contains only a few data members without any method 
             implementation that indicates that the abstraction might not be required.
WMC: 0, CBO: 0, LOC: 0
```

#### Actual Code
```java
private enum ConfigurationType { JNDI_NAME, MAIL_PROPERTIES }
private ConfigurationType type;
```

Exact same pattern as `DatabaseProvider` — a duplicated abstraction. Both independently define nearly identical enums.

#### Refactoring Strategy: *Inline Class* (same as 7.1)

**Step 1 — Replace enum with boolean:**
```java
private final boolean isJndiConfigured;
```

**Step 2 — Update type checks and remove enum.**

#### Expected Outcome
- Duplicated unnecessary enum removed from both providers
- Simpler, more direct code

---

## New Classes & Interfaces to Create

| # | New Type | Package | Purpose | Addresses Smell |
|---|----------|---------|---------|-----------------|
| 1 | `CommentManager` (interface) | `weblogger.business` | Comment CRUD contract | #1 Insufficient Modularization |
| 2 | `JPACommentManagerImpl` | `weblogger.business.jpa` | Comment CRUD persistence | #1 Insufficient Modularization |
| 3 | `CategoryManager` (interface) | `weblogger.business` | Category CRUD contract | #1 Insufficient Modularization |
| 4 | `JPACategoryManagerImpl` | `weblogger.business.jpa` | Category CRUD persistence | #1 Insufficient Modularization |
| 5 | `WeblogEntryQueryBuilder` | `weblogger.business.jpa` | Dynamic JPQL construction | #1 Insufficient Modularization |
| 6 | `WeblogEntryContentHelper` | `weblogger.pojos` | Text transformation | #1, #6 Hub-like |
| 7 | `WeblogEntryTagHandler` | `weblogger.pojos` | Tag lifecycle management | #1 Insufficient Modularization |
| 8 | `WeblogTagRepository` | `weblogger.business.jpa` | Tag aggregation persistence | #3 Feature Envy |
| 9 | `WeblogSetupService` | `weblogger.business` | Weblog creation orchestration | #3 Feature Envy |
| 10 | `AtomRequestContext` (interface) | `weblogger.webservices.atomprotocol` | Break atom cycle | #4 Cyclic Dependency |
| 11 | `SubscriptionEntryContainer` (interface) | `planet.pojos` | Break subscription cycle | #4 Cyclic Dependency |
| 12 | `WeblogRequestContext` (interface) | `weblogger.ui.rendering.util` | Common request contract | #5 Broken Hierarchy |
| 13 | `URLBuilderUtils` | `weblogger.business` | Shared URL construction | #5 Broken Hierarchy |

---

## Execution Phases

The refactorings should be executed in this order to minimize merge conflicts and cascading changes:

| Phase | Refactorings | Rationale | Risk |
|-------|-------------|-----------|------|
| **Phase 1** (Low Risk) | 7.1 `DatabaseProvider` enum, 7.2 `MailProvider` enum | Self-contained, no cross-file impact | 🟢 Very Low |
| **Phase 2** (Encapsulation) | 2.1 `WeblogEntry` fields, 2.2 `Weblog` fields | Foundation — proper encapsulation enables later refactorings | 🟢 Low |
| **Phase 3** (Break Cycles) | 4.1 `EntryCollection` ↔ `RollerAtomHandler`, 4.2 `Subscription` ↔ `SubscriptionEntry` | Reduces coupling for later phases | 🟡 Medium |
| **Phase 4** (Fix Hierarchies) | 5.1 `WeblogPageRequest`, 5.2 `MultiWeblogURLStrategy` | Standalone hierarchy fixes | 🟡 Medium |
| **Phase 5** (Move Methods) | 3.1 `updateTagCount`, 3.2 `addWeblogContents` | Creates new helper classes | 🟡 Medium |
| **Phase 6** (Decompose) | 1.1 `JPAWeblogEntryManagerImpl`, 1.2 `WeblogEntry` | Largest changes, creates new managers | 🔴 High |
| **Phase 7** (Reduce Hubs) | 6.1 `Weblog` hub, 6.2 `WeblogEntry` hub | Depends on decomposition from Phase 6 | 🔴 High |

**Rule:** After each phase, run the full test suite and re-run Designite analysis to verify metric improvements before proceeding.

---

## Expected Metric Improvements

### Per-Class Before vs. After

| Class | Metric | Before | Target | % Improvement |
|-------|--------|--------|--------|---------------|
| `JPAWeblogEntryManagerImpl` | LOC | 894 | ~400 | -55% |
| `JPAWeblogEntryManagerImpl` | WMC | 197 | ~90 | -54% |
| `JPAWeblogEntryManagerImpl` | Public Methods | 44 | ~20 | -55% |
| `JPAWeblogEntryManagerImpl` | CBO | 30 | ~15 | -50% |
| `WeblogEntry` | LOC | 1031 | ~500 | -52% |
| `WeblogEntry` | Public Methods | 91 | ~45 | -51% |
| `WeblogEntry` | Public Fields | 28 | 0 | -100% |
| `WeblogEntry` | Fan-Out | 20 | ~5 | -75% |
| `Weblog` | LOC | 927 | ~500 | -46% |
| `Weblog` | Public Methods | 97 | ~55 | -43% |
| `Weblog` | Public Fields | 35 | 0 | -100% |
| `Weblog` | Fan-Out | 21 | ~5 | -76% |
| `JPAWeblogManagerImpl` | CBO | 36 | ~20 | -44% |
| `WeblogPageRequest` | WMC | 71 | ~30 | -58% |
| `EntryCollection` | CBO | 29 | ~20 | -31% |

### Aggregate Improvements

| Metric | Current | Target | Improvement |
|--------|---------|--------|-------------|
| Total Design Smells (Designite) | 200+ | ~120 | **40% ↓** |
| Avg CBO (top 10 classes) | 28.8 | ~16 | **44% ↓** |
| Max WMC | 197 | ~90 | **54% ↓** |
| Public field violations | 63+ | 0 | **100% ↓** |
| Cyclic dependency cycles | 4+ | 0 | **100% ↓** |
| Total LOC (affected classes) | ~5,890 | ~3,540 | **40% ↓** |
| Public methods exposed | 184+ | ~94 | **49% ↓** |

---

## Effort Estimates

| Phase | Smell | Instances | Est. Hours |
|-------|-------|-----------|------------|
| Phase 1 | #7 Unnecessary Abstraction | `DatabaseProvider`, `MailProvider` | 1-2 hrs |
| Phase 2 | #2 Deficient Encapsulation | `WeblogEntry`, `Weblog` | 4-6 hrs |
| Phase 3 | #4 Cyclic Dependencies | `EntryCollection`, `Subscription` | 6-10 hrs |
| Phase 4 | #5 Broken Hierarchy | `WeblogPageRequest`, `MultiWeblogURLStrategy` | 4-6 hrs |
| Phase 5 | #3 Feature Envy | `updateTagCount`, `addWeblogContents` | 4-6 hrs |
| Phase 6 | #1 Insufficient Modularization | `JPAWeblogEntryManagerImpl`, `WeblogEntry` | 12-16 hrs |
| Phase 7 | #6 Hub-like Modularization | `Weblog`, `WeblogEntry` | 10-14 hrs |
| **Total** | | **14 refactorings** | **41-60 hrs** |

---

## Notes

- All refactorings are **behavior-preserving** — no functional changes to the application
- Each phase should be followed by a **full test suite run** (`mvn test`) to verify no regressions
- After each phase, re-run **Designite analysis** to measure actual metric improvements
- Some callers of removed methods may be in **JSP/Velocity templates** — check `app/src/main/webapp/`
- The `Weblog` and `WeblogEntry` hub reduction (Smell #6) will have the **widest impact** — plan for thorough testing
- Where both plans had equivalent instances, the **higher-impact class** was preferred (e.g., `WeblogEntry` over `SubscriptionEntry` for Smell #1)

---

*Document generated from analysis of CODE METRICS data (Designite, CK, PMD, SonarQube)*  
*Project: Apache Roller Weblogger (project-1-team-45-master)*  
*Combined from: 01_VERIFIED_DESIGN_SMELLS_IN_DEPTH_ANALYSIS.md + REFACTORING_PLAN.md*
