# Search and Indexing Subsystem (Manual Analysis)

## Key Classes and Interfaces

### IndexManager (business interface)
- **Type**: Manager interface for full-text search.
- **Responsibilities**:
  - Initialize/shutdown search infrastructure.
  - Schedule add/remove/reindex operations for entries and weblogs.
  - Execute search queries and return `SearchResultList`.
- **Collaborators**:
  - `WeblogEntry`, `Weblog`, `URLStrategy`.

### LuceneIndexManager (implementation)
- **Type**: Lucene-based implementation of `IndexManager`.
- **Responsibilities**:
  - Manages index directory, consistency marker, and search enablement.
  - Schedules index operations (add/remove/reindex/rebuild) via operation queue.
  - Executes search and converts Lucene hits into result lists.
  - Manages Lucene reader/writer and concurrency via read/write lock.
- **Collaborators**:
  - Lucene APIs: `IndexReader`, `IndexWriter`, analyzers.
  - `Weblogger`, `WeblogEntryManager` for object access.
  - Operation types: `AddEntryOperation`, `RemoveEntryOperation`, `RebuildWebsiteIndexOperation`, `SearchOperation`.

### IndexOperation (base class)
- **Type**: Abstract runnable for Lucene operations.
- **Responsibilities**:
  - Defines template for executing index operations.
  - Builds Lucene `Document` for a `WeblogEntry` (including comment fields if configured).
  - Manages lifecycle of `IndexWriter` (begin/end writing).
- **Collaborators**:
  - `LuceneIndexManager` for access to index directory and analyzer.
  - `FieldConstants` for schema.

### FieldConstants (schema constants)
- **Type**: Constants class defining Lucene document field names.
- **Responsibilities**:
  - Defines field names used across search and indexing operations.

## Notes
- Indexing uses a background operation model; search uses synchronous execution.
- Index consistency marker triggers rebuild on startup when needed.
