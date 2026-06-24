# Feature Specification: LabLex MVP-1 First Mock Run

**Feature Branch**: `002-mvp-1-mock-run`

**Created**: 2026-06-25

**Status**: Draft

**Input**: User description: "LabLex AI Evaluation Control Plane MVP-1 First Mock Run"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Registry Component Management (Priority: P1)

Developers want to register manifests for their external evaluation tools, targets, models, benchmarks, and result schemas through versioned API endpoints, validate their formats against JSON schemas, and view them in a structured UI list/detail view.

**Why this priority**: Registry is the foundation of the control plane; we cannot compose runs without registered components.

**Independent Test**:
1. Post a new ExternalTool manifest to `POST /api/v1/external-tools`. Verify it is stored and returns a generated ID.
2. Attempt to register a manifest with incorrect schema. Verify that it is rejected with a validation error (`HTTP 422`).
3. Access the Registry UI in the Next.js frontend and verify that the newly registered components are listed.

---

### User Story 2 - RunSpec Composition and Validation (Priority: P1)

Users want to select an ExternalTool, Target, Model, and Benchmark, validate that they are mutually compatible (e.g., target supports the model, tool is compatible with the benchmark), and compose a validated, locked `RunSpec` representing the immutable execution contract.

**Why this priority**: RunSpec immutability ensures reproducibility of evaluation runs.

**Independent Test**:
1. Call `POST /api/v1/runspecs/compose` with a list of components. Verify that a composed `RunSpec` in `composed` state is returned.
2. Call `POST /api/v1/runspecs/{id}/validate`. Verify that compatibility engine runs pings/checks and transitions it to `validated`.
3. Call `POST /api/v1/runspecs/{id}/lock`. Verify that the status becomes `locked` and is now immutable.

---

### User Story 3 - Mock Evaluation Run with Real-Time SSE (Priority: P1)

Users want to start an evaluation run from a locked RunSpec using a Mock Adapter, observe progress events streamed in real-time via Server-Sent Events (SSE), automatically capture raw outputs, normalize them into structured results, and view a metrics detail page and HTML report.

**Why this priority**: Demonstrates the end-to-end evaluation lifecycle and data capturing mechanics of LabLex without needing complex setup of external execution environments.

**Independent Test**:
1. Trigger a run: `POST /api/v1/runs` referencing the locked RunSpec.
2. Listen to `GET /api/v1/runs/{id}/events` and verify that basic lifecycle events (`queued`, `running`, `completed`) are received.
3. Verify that raw outputs (simulated JSON/CSV) are captured in object storage, and a `NormalizedResult` containing parsed score, latency, and tokens is populated.
4. Verify that the UI displays the metric tables and a generated HTML report can be downloaded.

---

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001 (JSON Schema Validation)**: All registry manifests (ExternalTool, Target, Model, Benchmark, Adapter, ResultSchema) MUST be validated against strict JSON schemas.
- **FR-002 (Registry API)**: Provide versioned CRUD endpoints under `/api/v1/` for all registry entities with pagination.
- **FR-003 (Compatibility Engine)**: Implement intersection logic verifying target-model bindings, tool-adapter compatibility, and metric profiles.
- **FR-004 (Mock Adapter)**: Implement a mock adapter that generates predictable, synthetic evaluation outputs in multiple formats (JSON, CSV) without launching real subprocesses.
- **FR-005 (Execution Gateway)**: Implement run status transitions: `created` → `validated` → `queued` → `running` → `completed`/`failed`.
- **FR-006 (Worker Queue)**: Set up Celery/RQ task queues for background run processing.
- **FR-007 (Normalization Engine)**: Implement JSONPath-driven extraction extracting score, latency, and sample results from raw outputs based on `ResultSchema` manifests.
- **FR-008 (SSE Server)**: Implement an SSE endpoint at `/api/v1/runs/{id}/events` streaming lifecycle status changes.
- **FR-009 (UI Registry & Wizard)**: Build Next.js UI lists, detail views, and a step-by-step Create Run wizard.

## Success Criteria *(mandatory)*

- **SC-001**: Running a mock evaluation completes from creation to normalized result in under 30 seconds.
- **SC-002**: Missing required schema fields during normalization transitions status to `normalization_failed` with descriptive warnings.
- **SC-003**: Full pagination is enforced on all list endpoints (defaults to 20 items per page).
