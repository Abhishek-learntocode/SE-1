# Manual Deep Analysis - Weblog & Content Subsystem

## Scope
Covers weblog creation and management, entries, categories, comments, tags, bookmarks, media, templates/themes, and the rendering pipeline (request parsing, model loading, page rendering).

## Comprehensive Class Inventory
- Full list of classes, interfaces, and enums: `Working/02-task1/manual/weblog-content-classlist.md`
- Method-heavy files with full signatures: `Working/02-task1/manual/weblog-content-method-signatures.md`
- CK class metrics subset: `Working/02-task1/manual/weblog-content-ckclass.csv`

## Package Breakdown (Key Responsibilities)

### 1) Business Layer (Managers)
- **WeblogManager**: weblog lifecycle, template CRUD, weblog listings.
- **WeblogEntryManager**: entry/category/comment/tag/hit-count operations (multi-concern manager).
- **BookmarkManager / MediaFileManager / ThemeManager**: specialized managers for bookmarks, media, and themes.
- **JPA* implementations**: persistence-backed managers (e.g., `JPAWeblogEntryManagerImpl`, `JPAWeblogManagerImpl`).

### 2) Domain Model (POJOs)
- **Weblog**: top-level blog entity (settings, preferences, associations to categories, folders, media). Includes convenience query methods that delegate to managers.
- **WeblogEntry**: entry content + metadata + rendering helpers, tag/attribute handling, permission checks, rendering hooks.
- **WeblogEntryComment / WeblogCategory / WeblogEntryTag**: comments, taxonomy, and tag models.
- **Template/Theme entities**: `WeblogTemplate`, `ThemeTemplate`, `Theme`, `WeblogTheme`, etc.

### 3) Rendering Pipeline (UI Rendering)
- **PageServlet**: main request handler; applies caching, parses page request, sets HTTP headers, initializes models, renders via selected renderer.
- **WeblogPageRequest**: parses URL into request context (entry/date/category/tags/page) and resolves heavy objects via managers.
- **ModelLoader**: instantiates configured models via reflection and calls `init()`.
- **PageModel**: common data model (weblog, entry, page, category) injected into template engine.
- **RendererManager / Renderer / VelocityRenderer**: rendering engine abstraction and Velocity implementation.

### 4) Plugins and Themes
- **Entry plugins**: `WeblogEntryPlugin` implementations (e.g., `SmileysPlugin`, `ConvertLineBreaksPlugin`).
- **Comment plugins**: `WeblogEntryCommentPlugin` implementations.
- **Theme system**: `ThemeManagerImpl` + theme metadata/parser + shared/custom theme models.

## Primary Flow: Page Rendering
1. **Request parsing**
   - `PageServlet.doGet()` creates a `WeblogPageRequest` to parse the URL and resolve weblog/page/entry/category data.
2. **Cache and HTTP headers**
   - `PageServlet` computes `lastModified`, handles 304, and checks the page cache.
3. **Model loading**
   - `ModelLoader.loadModels(...)` creates models (e.g., `PageModel`) and calls `init()` with parsed request and other context.
4. **Template rendering**
   - `RendererManager` chooses the appropriate `Renderer` (Velocity).
   - `PageModel` provides template data; `WeblogEntry` applies entry plugins and sanitization.
5. **Output**
   - Rendered HTML is written to response and optionally cached.

## Key Interactions
- **WeblogEntry** uses `WebloggerFactory` to fetch `WeblogEntryManager` and `UserManager` for permissions and anchors.
- **WeblogPageRequest** uses `WeblogEntryManager` and `WeblogManager` to resolve entry, page, and category objects.
- **PageModel** wraps domain objects into wrapper types for template usage.
- **Renderer** uses template language and theme data to output page content.

## Design Observations (Manual)
- High coupling of domain objects to managers via `WebloggerFactory` (service locator pattern).
- Large manager interfaces mixing multiple concerns (entries + categories + comments + tags).
- Rendering pipeline tightly bound to servlet lifecycle and page request parsing.

## UML
- Manual subsystem UML: `Working/02-task1/manual/uml/weblog-content.puml`
