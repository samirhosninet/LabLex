# Tasks: LabLex MVP-2 Professional Results

**Input**: Design documents from `/specs/003-mvp-2-professional-results/`

**Prerequisites**: plan.md (required), spec.md (required)

---

## Phase 1: Setup & DB Schema Upgrades

- [ ] T201 Create database tables: `comparisons`, `comparison_items`, `audit_events`, `idempotency_keys`
- [ ] T202 Generate Alembic migration script for MVP-2 tables: `alembic revision --autogenerate -m "create_mvp2_tables"`
- [ ] T203 Setup Redis caching connection pool helper in `backend/src/core/cache.py`

---

## Phase 2: Execution Control & Quotas (Priority: P1)

- [ ] T204 Implement idempotency middleware or decorator checking `Idempotency-Key` headers in `backend/src/core/idempotency.py`
- [ ] T205 Implement concurrent run and monthly quota checks in `backend/src/core/quotas.py`
- [ ] T206 Implement duplicate run spec configuration detection (409 Conflict) on run submission
- [ ] T207 Implement API rate limiting using Redis token bucket or sliding window algorithm

---

## Phase 3: Run Comparison & Reporting (Priority: P1)

- [ ] T208 Implement metric delta calculations and winner indicators in `backend/src/core/comparison_engine.py`
- [ ] T209 Create comparison CRUD API routes `/api/v1/comparisons` in `backend/src/api/comparisons.py`
- [ ] T210 Implement comparison report exporter utilizing Jinja2 HTML templates in `backend/src/core/report.py`
- [ ] T211 Create result CSV/JSON export endpoints for runs and comparisons

---

## Phase 4: Observability & Heartbeats (Priority: P1)

- [ ] T212 Implement SSE heartbeats sending pings every 15 seconds to keep connections alive
- [ ] T213 Implement SSE replay logic utilizing `Last-Event-ID` header, loading missed events from `run_events` table
- [ ] T214 Create batch runs endpoint `/api/v1/runs/batch`
- [ ] T215 Implement decorator/middleware mapping user requests to `audit_events` table

---

## Phase 5: Next.js Frontend Screens

- [ ] T216 Create Next.js Comparison detail page showing side-by-side metric tables and deltas in `frontend/src/pages/comparisons/[id].tsx`
- [ ] T217 Create Next.js Audit log browser page in `frontend/src/pages/audit/index.tsx`
- [ ] T218 Build Next.js Dashboard widgets showing active counts, monthly quota usage, and recent runs on the home page

---

## Phase 6: Polish & Testing

- [ ] T219 Write unit tests for idempotency engine and comparison calculations
- [ ] T220 Verify all 22 production gates checklist (specifically RLS, rate limits, and audit logs)
- [ ] T221 Commit and push all files to remote GitHub repository
