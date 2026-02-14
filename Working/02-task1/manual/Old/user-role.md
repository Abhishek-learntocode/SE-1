# User and Role Management Subsystem (Manual Analysis)

## Key Classes and Interfaces

### User (entity)
- **Type**: POJO entity representing a user account.
- **Responsibilities**:
  - Stores user identity (username), authentication data (password), profile fields, and activation state.
  - Encodes passwords via `RollerContext` password encoder in `resetPassword`.
  - Checks global permission using `UserManager` through `WebloggerFactory`.
- **Collaborators**:
  - `WebloggerFactory` / `UserManager` for permission checks.
  - `RollerContext` for password encoder.

### UserManager (business interface)
- **Type**: Manager interface for user, role, and permission management.
- **Responsibilities**:
  - CRUD for users.
  - Queries by username, OpenID URL, and status filters.
  - Permission management: grant/revoke weblog permissions, pending permissions, and permission checks.
  - Role management: grant/revoke roles and (deprecated) role queries.
- **Collaborators**:
  - `User`, `Weblog`, `WeblogPermission`, `RollerPermission`.

### JPAUserManagerImpl (implementation)
- **Type**: JPA-backed implementation of `UserManager`.
- **Responsibilities**:
  - Persists users and permissions via `JPAPersistenceStrategy`.
  - Grants default roles on user creation (editor, optionally admin for first user).
  - Caches username -> userId mapping to optimize lookups.
- **Collaborators**:
  - `JPAPersistenceStrategy` for persistence.
  - Named queries on `User` entity.
  - `WebloggerConfig` for configuration flags.

### RollerUserDetailsService (security integration)
- **Type**: Spring Security `UserDetailsService` adapter.
- **Responsibilities**:
  - Bridges Roller user model to Spring Security authentication.
  - Handles OpenID and standard username/password paths.
  - Converts Roller roles to Spring Security authorities.
- **Collaborators**:
  - `WebloggerFactory` / `UserManager` for user lookup and roles.
  - Spring Security `UserDetails` and authority types.

## Notes
- Role checks use deprecated methods (`getRoles`, `hasRole`); primary path is permissions-based checks.
- User entity relies on manager lookup, coupling domain objects to service layer.
