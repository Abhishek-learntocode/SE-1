# Weblog and Content Subsystem (Manual Analysis)

## Scope
This document manually identifies the core classes and interfaces for weblog/content management.

## Key Classes and Interfaces

### Weblog (entity)
- **Type**: POJO entity representing a weblog/site with metadata and associations.
- **Responsibilities**:
  - Stores weblog properties such as handle, name, settings, comment policies, and locale/timezone.
  - Maintains associations to categories, bookmark folders, and media directories.
  - Provides convenience query helpers (recent entries, recent comments, popular tags, counts) by delegating to managers via `WebloggerFactory`.
- **Collaborators**:
  - `WebloggerFactory` to obtain `WeblogEntryManager`, `BookmarkManager`, `ThemeManager`.
  - `WeblogEntryManager` for queries and counts.
  - `BookmarkManager` for folder retrieval.

### WeblogEntry (entity)
- **Type**: POJO entity for a single blog entry.
- **Responsibilities**:
  - Stores entry content, metadata, status, tags, and category/website association.
  - Renders entry text/summary using entry plugins and sanitization.
  - Checks write permissions via `UserManager` and `WeblogPermission`.
  - Generates anchors for permalinks and exposes display utilities.
- **Collaborators**:
  - `WebloggerFactory` to obtain `UserManager` and `WeblogEntryManager`.
  - `WeblogEntryPlugin` for content rendering.
  - `HTMLSanitizer` for output sanitization.

### WeblogManager (business interface)
- **Type**: Manager interface for weblog/site lifecycle.
- **Responsibilities**:
  - CRUD operations for weblogs.
  - Lists weblogs by filters (enabled/active/date/letter), retrieves users per weblog.
  - Template management for weblogs (custom templates and renditions).
- **Collaborators**:
  - `Weblog`, `User`, `WeblogTemplate`, `CustomTemplateRendition`.

### WeblogEntryManager (business interface)
- **Type**: Manager interface for entries, categories, comments, tags, and hit counts.
- **Responsibilities**:
  - CRUD for entries, categories, comments, hit counts.
  - Query operations: entries by criteria, maps by date, tags, stats, popular lists.
  - Utility operations: create anchor, apply comment defaults, category checks.
- **Collaborators**:
  - `WeblogEntry`, `WeblogCategory`, `WeblogEntryComment`, `WeblogEntrySearchCriteria`, `TagStat`, `StatCount`.

## Notes
- Entities depend on managers via `WebloggerFactory`, so domain objects are not pure POJOs.
- Manager interfaces suggest layered architecture: UI/Service -> Manager -> Persistence.
