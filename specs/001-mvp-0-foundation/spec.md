# Feature Specification: LabLex MVP-0 Foundation

**Feature Branch**: `001-mvp-0-foundation`

**Created**: 2026-06-25

**Status**: Draft

**Input**: User description: "LabLex AI Evaluation Control Plane MVP-0 Foundation"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Environment Bootstrapping & Health Check (Priority: P1)

Developers and operators want a single command (`docker-compose up`) to spin up all backend, frontend, database, cache, and object storage services, verify that the environment is healthy, and access the FastAPI API documentation.

**Why this priority**: It is the absolute prerequisite for development, testing, and deployment.

**Independent Test**:
1. Run `docker-compose up --build -d` in the repository root.
2. Send a `GET /api/v1/health` request. Verify that the response is `HTTP 200 OK` with JSON showing all services (database, cache) are healthy.
3. Open `http://localhost:8000/docs` in the browser and verify the FastAPI Swagger UI is rendered.

**Acceptance Scenarios**:

1. **Given** a fresh system with Docker installed, **When** running `docker-compose up --build -d`, **Then** containers for `postgres`, `redis`, `minio`, `backend`, `frontend`, and `worker` are successfully launched.
2. **Given** the environment is running, **When** sending a request to `GET /api/v1/health`, **Then** the service returns a `HTTP 200 OK` with structured health status of database and cache.

---

### User Story 2 - User Login and Tenant Scoping (Priority: P1)

Users want to log in, obtain a JWT access token, and perform subsequent authenticated requests which are strictly scoped to their resolved tenant ID.

**Why this priority**: LabLex is a multi-tenant control plane; security boundaries must be enforced from day one.

**Independent Test**:
1. Run the seed script to create a default tenant and admin user.
2. Call `POST /api/v1/auth/login` with admin credentials, get a JWT access token.
3. Access the dashboard via Next.js and confirm that it scopes queries to the user's tenant ID.
4. Try to access resources with a JWT token belonging to another tenant and confirm it is blocked.

**Acceptance Scenarios**:

1. **Given** the default seeded database, **When** calling `POST /api/v1/auth/login` with correct credentials, **Then** return `HTTP 200` with a valid JWT token and tenant metadata.
2. **Given** a request authenticated with a tenant's JWT token, **When** accessing resources, **Then** the tenant scoping middleware injects `tenant_id` and restricts database reads/writes strictly to that tenant.

---

### User Story 3 - Role-Based Access Control (RBAC) (Priority: P2)

Administrators want to enforce that write operations (POST, PUT, PATCH, DELETE) require specific role permissions (Admin or Operator), whereas read operations (GET) are accessible to Read-Only users.

**Why this priority**: Ensures security within a tenant so that unauthorized users cannot modify Tool connections or run configurations.

**Independent Test**:
1. Log in as a Read-Only user.
2. Attempt to create a new resource (e.g., POST request). Verify that the request is rejected with `HTTP 403 Forbidden`.

**Acceptance Scenarios**:

1. **Given** a user with a `Reader` role in a tenant, **When** they make a `POST /api/v1/manifests` call, **Then** return `HTTP 403 Forbidden` with a unified error response.
2. **Given** a user with an `Admin` or `Operator` role, **When** they make a state-changing API request, **Then** the operation is authorized and proceeds.

---

### Edge Cases

- **Token Expiration / Invalidation:** If a JWT token expires, the backend must return `HTTP 401 Unauthorized` following the unified error model.
- **Idempotency Key Collisions:** If duplicate requests are made simultaneously, the backend must handle them gracefully (return conflict).
- **Service Disconnection:** If Redis or Postgres is down, the health check endpoint must report degraded status (`HTTP 503 Service Unavailable`) rather than crashing.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001 (FastAPI Backend)**: The backend MUST be built using FastAPI with structured routers versioned under `/api/v1/`.
- **FR-002 (Next.js Frontend)**: The frontend MUST be structured using Next.js, displaying a dashboard with basic login/auth integration.
- **FR-003 (Docker Compose)**: A single `docker-compose.yml` MUST orchestrate Postgres, Redis, MinIO, Backend, Frontend, and Celery/RQ Worker.
- **FR-004 (Alembic Migrations)**: Database tables MUST be created and migrated using Alembic.
- **FR-005 (Schema Definition)**: The database schema MUST include `tenants`, `users`, `memberships`, and `api_keys` tables.
- **FR-006 (Authentication)**: Backend MUST implement JWT authentication using asymmetric or symmetric signing keys.
- **FR-007 (Tenant Scoping)**: Middleware MUST enforce that every request is scoped by a resolved `tenant_id`.
- **FR-008 (RBAC Enforcement)**: State-changing write endpoints MUST require specific role permissions.
- **FR-009 (Unified Error Model)**: All endpoints MUST return a standard error JSON format: `{ "error": { "code": "...", "message": "...", "details": ... } }`.

### Key Entities

- **Tenant**: Represents an isolated customer workspace containing configurations, runs, and reports.
- **User**: Represents a system user with an email and credentials.
- **Membership**: Links a User to a Tenant with a specific Role (Admin, Operator, Reader).
- **API Key**: Represents a programmatic key used by external tools or scripts to authenticate against the `/api/v1/` routes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Running `docker-compose up` completes build and starts all services in under 5 minutes on a standard developer machine.
- **SC-002**: Health check endpoint returns response in under 50ms.
- **SC-003**: 100% of state-changing routes reject unauthenticated requests with `HTTP 401` or `HTTP 403`.
- **SC-004**: Unit test coverage for auth and scoping middleware is at least 80%.

## Assumptions

- We assume local development utilizes SQLite or a local PostgreSQL instance launched via Docker.
- As outlined in the v1.6.2/v1.6.3 plan, external integrations (mock or real) are out of scope for MVP-0.
