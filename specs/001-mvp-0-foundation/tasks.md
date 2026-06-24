# Tasks: LabLex MVP-0 Foundation

**Input**: Design documents from `/specs/001-mvp-0-foundation/`

**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by phase and user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend structure: `backend/src/api/`, `backend/src/core/`, `backend/src/middleware/`, `backend/src/models/`
- [ ] T002 Create frontend structure: `frontend/src/components/`, `frontend/src/pages/`, `frontend/src/services/`
- [ ] T003 [P] Create `.env.example` in root with required config variables (DB, Redis, JWT, MinIO credentials)
- [ ] T004 Create `docker-compose.yml` orchestrating `postgres`, `redis`, `minio`, `backend`, `frontend`
- [ ] T005 [P] Setup backend linting/type-check configs (`pyproject.toml`, `requirements.txt`)
- [ ] T006 [P] Setup frontend linting/tsconfig configs (`package.json`, `tsconfig.json`)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before user stories can run

- [ ] T007 Initialize Alembic in `backend/alembic/` and configure database connection in `env.py`
- [ ] T008 [P] Implement base DB model structure and migration engine in `backend/src/core/database.py`
- [ ] T009 [P] Create configuration loader in `backend/src/core/config.py` loading from `.env`
- [ ] T010 [P] Implement Unified Error Model structure in `backend/src/core/errors.py`
- [ ] T011 Implement Base DB tables: `tenants`, `users`, `memberships`, `api_keys` in `backend/src/models/`
- [ ] T012 Run initial Alembic migration to create base tables: `alembic revision --autogenerate -m "create_base_tables"`

**Checkpoint**: Foundation ready - user story implementation can begin.

---

## Phase 3: User Story 1 - Environment Bootstrapping & Health Check (Priority: P1)

**Goal**: Complete environment setup and health routing

- [ ] T013 Implement health check router in `backend/src/api/health.py` querying DB and Redis health
- [ ] T014 Register health check router in `backend/src/main.py` under `/api/v1/health`
- [ ] T015 Verify health check runs locally via `docker-compose up`

---

## Phase 4: User Story 2 - User Login & Tenant Scoping (Priority: P1)

**Goal**: Enforce authentication and strict tenant boundaries

- [ ] T016 [US2] Implement JWT generation and token decoding utilities in `backend/src/core/security.py`
- [ ] T017 [US2] Implement login router endpoint in `backend/src/api/auth.py`
- [ ] T018 [US2] Create tenant scoping middleware in `backend/src/middleware/scoping.py` injecting `tenant_id` on all authenticated calls
- [ ] T019 [US2] Create database seed script in `backend/src/core/seed.py` for default tenant and admin user
- [ ] T020 [US2] Implement Next.js basic login page and auth service under `frontend/src/pages/login.tsx`

---

## Phase 5: User Story 3 - Role-Based Access Control (RBAC) (Priority: P2)

**Goal**: Restrict write operations based on role permission matrix

- [ ] T021 [US3] Create RBAC middleware in `backend/src/middleware/rbac.py`
- [ ] T022 [US3] Register RBAC checks on all POST, PUT, PATCH, DELETE endpoints in `backend/src/main.py`
- [ ] T023 [US3] Verify that a Reader role receives HTTP 403 on write endpoints

---

## Phase 6: Polish & CI Pipeline

**Purpose**: Validation and final cleanup

- [ ] T024 Write unit tests for scoping middleware and JWT validation under `backend/tests/`
- [ ] T025 Setup GitHub Actions workflow (.github/workflows/ci.yml) to run lint, type-checks, and pytest
- [ ] T026 Verify all 22 production gates criteria are untouched and ready in configuration
- [ ] T027 Run full test suite and confirm 100% pass status
