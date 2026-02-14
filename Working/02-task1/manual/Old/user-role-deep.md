# Manual Deep Analysis - User & Role Subsystem

## Scope
Users, roles, permissions, and security integration with Spring Security.

## Comprehensive Class Inventory
- Full list of classes, interfaces, and enums: `Working/02-task1/manual/user-role-classlist.md`
- CK class metrics subset: `Working/02-task1/manual/user-role-ckclass.csv`

## Key Packages and Roles

### 1) Business Layer
- **UserManager**: user CRUD, permission management, and role grants/revokes.
- **JPAUserManagerImpl**: persistence-backed implementation, caches username->id, grants default roles.

### 2) Domain Model
- **User**: profile and credential fields, password reset, permission queries.
- **WeblogPermission / GlobalPermission / RollerPermission**: permission models for weblog and global scopes.
- **UserRole**: role mapping entity.

### 3) Security Integration
- **RollerUserDetailsService**: bridges Roller's user model to Spring Security's `UserDetails`.
  - Handles OpenID and standard username/password paths.
  - Converts Roller roles into Spring authorities.

## Primary Flow: Authentication and Authorization
1. **Spring Security login** calls `RollerUserDetailsService.loadUserByUsername()`.
2. **User lookup** via `UserManager` (OpenID or standard username).
3. **Role mapping** via `UserManager.getRoles()` (deprecated path still used in adapter).
4. **Permission checks** performed by `UserManager.checkPermission()` in domain logic.

## Design Observations (Manual)
- Deprecated role methods coexist with permissions, indicating dual authorization models.
- Domain object `User` relies on `UserManager` for permission checks, coupling model to service layer.

## UML
- Manual subsystem UML: `Working/02-task1/manual/uml/user-role.puml`
