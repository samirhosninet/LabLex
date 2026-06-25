# Feature Specification: LabLex MVP-2 Professional Results

**Feature Branch**: `003-mvp-2-professional-results`

**Created**: 2026-06-25

**Status**: Draft

---

## User Scenarios & Testing

### User Story 1 - Run Comparison Dashboard (Priority: P1)
Users want to select two completed runs (evaluated using the same tool and benchmark) and view a side-by-side comparison of their metrics, displaying delta columns, winner highlights, and a downloadable comparison HTML/CSV report.

**Why this priority**: The primary value of the control plane is to compare model outputs and select the best performer.

**Independent Test**:
1. Trigger two mock runs for the same tool and benchmark.
2. Call `POST /api/v1/comparisons` passing the two run IDs. Verify it calculates deltas and saves the comparison.
3. Access `GET /api/v1/comparisons/{id}` and confirm that delta calculations and winner indicators (per metric) are correct.

---

### User Story 2 - Execution Control: Idempotency & Quotas (Priority: P1)
Tenant operators want to prevent duplicate run execution, enforce resource quotas (limit active runs and API counts), rate limit requests, and ensure safety via idempotency keys on run creation.

**Why this priority**: Protects backend resources and enforces multi-tenant billing/governance policies.

**Independent Test**:
1. Call `POST /api/v1/runs` with header `Idempotency-Key: key123`. Verify it starts.
2. Call `POST /api/v1/runs` with the same `Idempotency-Key` and verify it returns the same run ID without launching a new task.
3. Exceed tenant run quotas and verify that `POST /api/v1/runs` is rejected with `HTTP 429 Too Many Requests`.

---

### User Story 3 - Run Observability & SSE Replay (Priority: P1)
Developers observing an active evaluation run want to view logs, trace captured files, and reconnect to progress streams via SSE using `Last-Event-ID` if the network disconnects, replaying missed state updates.

**Why this priority**: Ensures network resilience during long runs and provides transparency into execution failures.

**Independent Test**:
1. Start a run and listen to `GET /api/v1/runs/{id}/events`. Disconnect the stream at 30% progress.
2. Reconnect passing `Last-Event-ID` header. Verify that events from 30% onwards are successfully replayed.
3. Fetch logs and raw storage pointers on the Run Detail page.

---

## Functional Requirements

- **FR-201 (Idempotency Engine)**: Implement `Idempotency-Key` checks using Redis/PostgreSQL on run creation endpoints.
- **FR-202 (Duplicate Run Detection)**: Compare `RunSpec` configuration hashes to block duplicate runs with `HTTP 409` if an identical completed run already exists.
- **FR-203 (Tenant Quotas)**: Enforce quotas (concurrent runs, total monthly runs, rate limits) stored in `tenant_quotas` table.
- **FR-204 (SSE Last-Event-ID Replay)**: Persist lifecycle progress events to the `run_events` table and support replaying events using `Last-Event-ID` header.
- **FR-205 (Run Comparison Engine)**: Implement comparison logic calculating differences (deltas) and picking metric winners.
- **FR-206 (Comparison UI)**: Build Next.js comparison UI displaying side-by-side metric tables and delta columns.
- **FR-207 (Report Templates)**: Implement report template rendering support for both single-run and comparison layouts.
- **FR-208 (Audit Logging)**: Record all critical state alterations (locking runspecs, creating runs, updating quotas, deleting manifests) in an `audit_events` table.
- **FR-209 (Redis Caching)**: Add a caching layer using Redis for manifests and tenant quotas to speed up validations.
- **FR-210 (Batch Runs)**: Add batch run creation endpoint `POST /api/v1/runs/batch`.

---

## Success Criteria

- **SC-201**: Identical requests with same `Idempotency-Key` return identical responses within 50ms.
- **SC-202**: Quota enforcement adds less than 5ms overhead to API response time.
- **SC-203**: SSE stream reconnection successfully replays events and recovers status without missing steps.
- **SC-204**: Side-by-side comparison loads and renders in Next.js in under 1 second.
