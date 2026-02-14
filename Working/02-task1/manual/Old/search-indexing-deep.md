# Manual Deep Analysis - Search & Indexing Subsystem

## Scope
Lucene-based indexing/search and the UI search results pipeline.

## Comprehensive Class Inventory
- Full list of classes, interfaces, and enums: `Working/02-task1/manual/search-indexing-classlist.md`
- CK class metrics subset: `Working/02-task1/manual/search-indexing-ckclass.csv`

## Key Packages and Roles

### 1) Search API
- **IndexManager**: interface for indexing and searching operations.
- **SearchResultList / SearchResultMap**: containers for query results.

### 2) Lucene Implementation
- **LuceneIndexManager**: central manager for Lucene directory, consistency markers, and scheduling operations.
- **IndexOperation**: base runnable for Lucene operations.
- **AddEntryOperation / RemoveEntryOperation / ReIndexEntryOperation / RebuildWebsiteIndexOperation**: concrete operations.
- **SearchOperation**: builds and executes queries.

### 3) UI Search Flow
- **SearchServlet**: handles search HTTP requests and delegates to model/pager.
- **SearchResultsModel / SearchResultsFeedModel**: provides search data to templates or feeds.
- **SearchResultsPager / SearchResultsFeedPager**: pagination helper for search results.

## Primary Flow: Search Request
1. **Request handling** in `SearchServlet`.
2. **Search execution** via `IndexManager.search()` / `LuceneIndexManager.search()`.
3. **Model creation** in `SearchResultsModel` or `SearchResultsFeedModel`.
4. **Pagination and rendering** via `SearchResultsPager` and rendering pipeline.

## Design Observations (Manual)
- `LuceneIndexManager` combines configuration, IO, and scheduling logic (multi-responsibility).
- Search results models are tightly coupled to rendering and URL strategy.

## UML
- Manual subsystem UML: `Working/02-task1/manual/uml/search-indexing.puml`
