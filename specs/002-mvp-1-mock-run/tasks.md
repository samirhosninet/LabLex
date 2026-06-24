# Tasks: LabLex MVP-1 First Mock Run

**Input**: Design documents from `/specs/002-mvp-1-mock-run/`

**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Organization**: Tasks are grouped by phase and user story to enable independent implementation and testing.

## Phase 1: Setup (Shared Infrastructure)

- [ ] T001 Install dependencies: `jsonschema`, `celery`, `jsonpath-ng`, `fastapi-sse` in `backend/requirements.txt`
- [ ] T002 Configure Celery application with Redis broker in `backend/src/core/celery_app.py`
- [ ] T003 Setup Docker Compose updates for Celery background worker service

---

## Phase 2: Foundational (Blocking Prerequisites)

- [ ] T004 Create base JSON Schema documents for all manifests under `backend/src/schemas/`
- [ ] T005 Create database tables: `runs`, `results`, `manifests`, `batches`
- [ ] T006 [P] Generate Alembic migration script for new tables: `alembic revision --autogenerate -m "create_mvp1_tables"`
- [ ] T007 Define abstract Base Adapter interface class in `backend/src/adapters/base.py`

---

## Phase 3: User Story 1 - Registry Component Management (Priority: P1)

- [ ] T008 [US1] Implement JSON Schema validation helper function using `jsonschema`
- [ ] T009 [US1] Create registry CRUD endpoints (`/api/v1/external-tools`, `/api/v1/targets`, etc.) in `backend/src/api/registry.py`
- [ ] T010 [US1] Add pagination helper utilities to list endpoints
- [ ] T011 [US1] Create Next.js registry overview list page in `frontend/src/pages/registry/index.tsx`
- [ ] T012 [US1] Create Next.js detail page for registered tools in `frontend/src/pages/registry/[id].tsx`

---

## Phase 4: User Story 2 - RunSpec Composition and Validation (Priority: P1)

- [ ] T013 [US2] Implement compatibility checking algorithm in `backend/src/core/compatibility.py`
- [ ] T014 [US2] Create RunSpec endpoints in `backend/src/api/runspecs.py` (`/compose`, `/{id}/validate`, `/{id}/lock`)
- [ ] T015 [US2] Enforce RunSpec database immutability rules (locked status check on write)
- [ ] T016 [US2] Implement Dry-Run mock checks endpoint `/api/v1/runspecs/{id}/dry-run`

---

## Phase 5: User Story 3 - Mock Evaluation Run with Real-Time SSE (Priority: P1)

- [ ] T017 [US3] Implement `MockAdapter` in `backend/src/adapters/mock_adapter.py` returning synthetic JSON/CSV outputs
- [ ] T018 [US3] Create Celery task in `backend/src/core/tasks.py` running adapter execution, capturing raw files, and uploading to MinIO
- [ ] T019 [US3] Implement JSONPath parser in `backend/src/core/normalizer.py` mapping raw fields to `NormalizedResult`
- [ ] T020 [US3] Create SSE lifecycle router in `backend/src/api/sse.py` publishing progress events via Redis pub/sub
- [ ] T021 [US3] Create Next.js 7-step Create Run wizard in `frontend/src/pages/runs/create.tsx`
- [ ] T022 [US3] Create Next.js Run Detail page with real-time SSE progress bar and metrics table in `frontend/src/pages/runs/[id].tsx`
- [ ] T023 [US3] Implement HTML single-run report exporter utilizing Jinja2 templates in `backend/src/core/report.py`

---

## Phase 6: Polish & Testing

- [ ] T024 Write unit tests for JSONPath normalizer and compatibility engine
- [ ] T025 Verify all 22 production gates checklist
- [ ] T026 Push all updates to remote GitHub repository
