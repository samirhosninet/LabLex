# LabLex — Final Architecture Plan

**Version:** 1.6.3  
**Date:** 2026-06-25  
**Patch Date:** 2026-06-25  
**Role:** Architecture Plan / Product Constitution / Technical Blueprint  
**Project Name:** LabLex  
**Architecture Principle:** External-First AI Evaluation Control Plane

---

## Changelog: v1.0 → v1.1 → v1.2 → v1.3 → v1.4 → v1.5 → v1.6 → v1.6.1 → 1.6.2 → 1.6.3

### v1.1 Patches (Architecture Foundations)

```text
Patch 1 (Section 25): Normalization Contract
Patch 2 (Section 26): Worker Isolation Architecture
Patch 3 (Section 27): Run Streaming / Real-time Progress
Patch 4 (Section 28): Authentication and Tenant Scoping
Patch 5 (Section 29): Schema Versioning
Patch 6 (Section 30): Extended Connection Testing
Patch 7 (Section 31): Comparison Model
Patch 8 (Section 12): Object Storage Path Convention (inline)
Patch 9 (Section 11): Raw Result Source Tracking (inline)
```

### v1.2 Patches (Operational Readiness)

```text
Patch 10 (Section 33): Idempotency & Duplicate Run Protection
Patch 11 (Section 34): Resource Quotas
Patch 12 (Section 35): RBAC Permission Matrix
Patch 13 (Section 36): Webhook Callback Contract
Patch 14 (Section 27+): SSE Replay / Last-Event-ID (inline update §27)
Patch 15 (Section 38): Artifact & Data Retention Policy
Patch 16 (Section 39): Metric Direction Rules
Patch 17 (Section 40): Manifest Deprecation Policy
Patch 18 (Section 41): Report Provenance & Hash
Patch 19 (Section 25+): normalization_warnings field (inline update §25)
Patch 20 (Section 17+): Run SLO Metrics (inline update §17)
```

### v1.3 Patches (Build Readiness)

```text
Patch 21 (Section 44): Unified Error Model
Patch 22 (Section 45): Testing Architecture
Patch 23 (Section 13+): API Pagination & Filtering Contract (inline update §13)
Patch 24 (Section 46): Caching Architecture
Patch 25 (Section 12+): Database Index Strategy (inline update §12)
Patch 26 (Section 47): Local Development Architecture
Patch 27 (Section 7+): Adapter Interface Contract (inline update §7)
Patch 28 (Section 48): Resilience Architecture
Patch 29 (Section 13+): Batch Operations (inline update §13)
Patch 30 (Section 13+): API Versioning (inline update §13)
Patch 31 (Section 49): Notification Architecture
Patch 32 (Section 6+): EvalEngine Clarification (inline update §6)
Patch 33 (Section 15+): Dashboard Metrics Definition (inline update §15)
Patch 34 (Section 19): MVP Plan Rewrite (full rewrite §19)
Patch 35 (Section 31+): Comparison Winner Rules (inline update §31)
Patch 36 (Section 13+): API Rate Limiting (inline update §13)
Patch 37 (Section 37): Logging Architecture (gap fill)
```

### v1.4 Patches (Production Hardening)

```text
Patch 38 (Section 7+): Adapter cancel() interface (inline update §7)
Patch 39 (Section 8+): Compatibility Declaration Mechanism (inline update §8)
Patch 40 (Section 6+): AgentProfile removal (inline update §6)
Patch 41 (Section 11+): NormalizedResult raw_result_id + runspec_id fields (inline update §11)
Patch 42 (Section 12+): Batches table + table relationships (inline update §12)
Patch 43 (Section 13+): Complete API endpoint list + MetricProfile CRUD (inline update §13)
Patch 44 (Section 14+): Report "Recommendation" → "User Notes" (inline update §14)
Patch 45 (Section 15+): Leaderboard → User-Configured Sort View (inline update §15)
Patch 46 (Section 15+): Create Run UX EvalEngine fix (inline update §15)
Patch 47 (Section 16+): Frontend Security + Presigned URL Enforcement (inline update §16)
Patch 48 (Section 26+): Dead Letter Queue + Graceful Worker Shutdown (inline update §26)
Patch 49 (Section 27+): SSE Event Distribution (inline update §27)
Patch 50 (Section 28+): CSRF Protection + API Key Rotation (inline update §28)
Patch 51 (Section 34+): Atomic Quota Enforcement (inline update §34)
Patch 52 (Section 36+): Webhook opaque tokens (inline update §36)
Patch 53 (Section 46+): Redis High Availability (inline update §46)
Patch 54 (Section 50): Deployment Architecture
Patch 55 (Section 51): Backup & Disaster Recovery
Patch 56 (Section 52): Operational Workflows (re-run, renormalize, tool registration)
```

### v1.5 Patches (Enforcement & Compliance)

```text
Patch 57 (Section 9+):  RunSpec lifecycle enforcement (inline update §9)
Patch 58 (Section 9+):  State-Activity mapping table (inline update §9)
Patch 59 (Section 7+):  Manifest JSON Schema registry (inline update §7)
Patch 60 (Section 7+):  ReportTemplate manifest example (inline update §7)
Patch 61 (Section 12+): Batches table full schema (inline update §12)
Patch 62 (Section 11+): NormalizedResult superseded status (inline update §11)
Patch 63 (Section 36+): Webhook processing flow opaque token fix (inline update §36)
Patch 64 (Section 45+): Cancel + DLQ test scenarios (inline update §45)
Patch 65 (Section 14+): Report generator = data + template only (inline update §14)
Patch 66 (Section 13+): OpenAPI specification commitment (inline update §13)
Patch 67 (Section 53):  Tenant Onboarding & Data Portability
Patch 68 (Section 5+):  User Journey day-2 stories (inline update §5)
```

### v1.6 Patches (Architectural Refinements)

```text
Patch 69 (Section 11+): NormalizedSample data model (inline update §11)
Patch 70 (Section 12+): Database tables update, secret_refs & normalized_samples full schemas (inline update §12)
Patch 71 (Section 16+): KMS Envelope Encryption Flow (inline update §16)
Patch 72 (Section 26+): Docker Adapter Sandboxing and Resource Limits (inline update §26)
Patch 73 (Section 36+): Webhook Fast-Path Redis Cache verification (inline update §36)
Patch 74 (Section 8+): RunSpec Connectivity Pre-check (inline update §8)
Patch 75 (Section 25+): ResultSchema array mapping (inline update §25)
```

### v1.6.1 Patches (Resolution of Blockers & Warnings)

```text
Patch 76 (Section 5+):  Remove EvalEngine selection from User Journey (B1)
Patch 77 (Section 8+):  Model bindings and MetricProfile constraints in Compatibility Engine (B2)
Patch 78 (Section 12+): Update master table list and indexes with missing tables (B3)
Patch 79 (Section 16+): Resolve secret refs KMS encryption vs manager contradiction (B4)
Patch 80 (Section 13+): Unified Core APIs list with /api/v1/ prefix and missing endpoints (B5)
Patch 81 (Section 31+): User-authored recommendation rule in comparisons & reports (B6)
Patch 82 (Section 43):  Authoritative 22-Gate list consolidation (B7, W2, W3)
Patch 83 (Section 9+):  Clarified RunSpec Lifecycle state transitions and command mappings (B8)
Patch 84 (Section 11+): Expanded NormalizedSample schema & table structure (W1)
Patch 85 (Section 7+):  Decoupled Adapter interface context using RunSpecDTO (W4)
```

### v1.6.2 Patches (Strict Contract Alignment)

```text
Patch 86 (Section 28): Clarify SecretRefs single authoritative KMS encryption model (B4)
Patch 87 (Section 13/26/30/36): Standardize all endpoints with /api/v1/ prefix (B5)
Patch 88 (Section 19): Clean 16-gate references to authoritative 22-gate wording (B7)
Patch 89 (Section 54): Correct composition connectivity pre-check step wording (B8)
Patch 90 (Section 0/1/4): Clean stale EvalEngine selection language (W1)
Patch 91 (Section 13/16/28): Clean RLS and artifact scanning language (W2)
```

### v1.6.3 Patches (Component-Agnostic Selection Guardrail)

```text
Patch 92 (Section 0/1/2): Add Component-Agnostic Product Root rule.
Patch 93 (Section 5/15): Replace fixed Create Run sequence with Evaluation Mode + manifest-derived required components.
Patch 94 (Section 21/22): Add acceptance and rejection rules preventing globally required Agent/Model/Benchmark/EvalEngine fields.
Patch 95 (Section 24): Update final architecture statement to emphasize Registry → User Selection → Compatibility → RunSpec → Evidence → Data → Reports as the product root.
```

**Rule:** FULL BUILD APPROVAL granted after v1.6.3 ratification.
**Rule:** No external tool execution before Patches 10–13, 21–26, and 86–91 are implemented.
**Rule:** No SaaS deployment before Patches 11–12, 21–26, 47–53, 57–67, 69–75, 76–85, and 86–91 are implemented.

---

## 0. Executive Decision

LabLex is not an internal benchmark runner, not an internal eval engine, not an agent runtime, and not a model provider.

LabLex is also not rooted in any single Agent, Model, EvalEngine, Benchmark, Tool, Provider, or framework. The product root is the neutral flow: Registry → User Selection → Compatibility → RunSpec → Evidence → Data → Reports.

LabLex is a raw, external-first AI evaluation control plane where users select ExternalTools (with EvalEngine derived as registry metadata from the selected ExternalTool), external agents/targets, models, and benchmarks/test suites. LabLex runs the selected external evaluation flow from inside LabLex, automatically captures the outputs, normalizes the data, compares results, and generates professional reports.

The core flow is:

```text
Choose external components
        ↓
Validate compatibility
        ↓
Create RunSpec
        ↓
Run from LabLex
        ↓
External tool executes
        ↓
LabLex automatically captures outputs
        ↓
Raw + normalized data stored
        ↓
Results, comparison, reports displayed inside LabLex
```

Manual result upload/import is allowed only as a fallback, not as the main user journey.

---

## 1. Product Definition

### 1.1 English Definition

LabLex is a schema-first, external-first AI evaluation control plane. It allows users to register and select external evaluation tools (with EvalEngine derived as registry metadata from the selected ExternalTool), external agents/targets, model providers, models, benchmarks/test suites, adapters, and report templates. LabLex executes the selected external workflow through adapters, captures the outputs automatically, stores raw and normalized results, compares runs, and generates professional data reports.

LabLex is component-agnostic: no Agent, Model, Benchmark, EvalEngine, Tool, or Provider is globally required. Required fields are derived from the selected Evaluation Mode and the selected manifests.

### 1.2 Arabic Definition

LabLex منصة تحكم خارجية-أولًا لتقييم أنظمة الذكاء الاصطناعي. تسمح للمستخدم باختيار أدوات خارجية (مع اشتقاق محرك التقييم EvalEngine كبيانات وصفية من الأداة الخارجية المحددة)، ووكلاء/أهداف، وموديلات، وبنشماركات/سلاسل اختبار، ثم تشغيلها من داخل LabLex، والتقاط النتائج تلقائيًا، وتحويلها إلى بيانات منظمة ومقارنات وتقارير احترافية.

LabLex لا يفترض أن كل تشغيل يحتاج وكيلًا أو موديلًا أو بنشماركًا أو محرك تقييم مستقلًا. الحقول المطلوبة تُستنتج من نوع التقييم والـ manifests المختارة.

---

## 2. Non-Negotiable Architecture Rules

These rules must not be broken:

```text
1. No internal eval engine.
2. No internal benchmark runner.
3. No internal scorer.
4. No internal agent runtime.
5. No internal model provider.
6. No hardcoded product root such as Hermes, Codex, Claude Code, ARC-AGI, Inspect AI, Promptfoo, etc.
7. External tools are registered through manifests/adapters.
8. Results must appear inside LabLex after running from LabLex.
9. Raw outputs must be preserved.
10. Normalized results must be generated for comparison/reporting.
11. Reporting and data are first-class product capabilities.
12. Manual upload/import is optional fallback only.
13. No Agent, Model, Benchmark, EvalEngine, Tool, or Provider may be globally required.
14. Required run components are derived from Evaluation Mode + selected manifests, not hardcoded UI assumptions.
15. The user must see all selected, derived, required, optional, compatibility, and evidence data before RunSpec locking.
```

---

## 3. What LabLex Owns vs What LabLex Does Not Own

### 3.1 LabLex Owns

| Area | Responsibility |
|---|---|
| Registry | External tools, targets, agents, models, benchmarks, adapters, schemas |
| Compatibility | Validate if selected tool/target/model/benchmark can work together |
| RunSpec | Compose a reproducible external execution plan |
| Execution Gateway | Start and monitor external execution |
| Adapter Contracts | Define how external tools are invoked and how outputs are captured |
| Auto-Capture | Collect result files, logs, traces, artifacts automatically |
| Data Layer | Store raw and normalized results |
| Comparison | Compare runs/models/tools/benchmarks |
| Reporting | Generate technical, executive, and audit reports |
| Audit | Record who ran what, with what config, when, and what happened |
| Observability | Track internal run health, adapter errors, timeouts, and failures |

### 3.2 LabLex Does Not Own

| Area | Must Stay External |
|---|---|
| Evaluation logic | External eval tools only |
| Benchmark execution | External benchmark runners only |
| Scoring logic | External scorer or tool output only |
| Agent runtime | External agent/runtime only |
| Model hosting | External provider/local model system only |
| Dataset execution | External tool/runner only |
| ARC solving | External runner/solver only |

---

## 4. System Architecture

```text
Frontend UI
  ↓
LabLex Control API
  ↓
Registry + Compatibility + RunSpec Composer
  ↓
Execution Gateway
  ↓
Adapter Layer
  ├─ HTTP Adapter
  ├─ CLI Adapter
  ├─ Docker Adapter
  ├─ Webhook Adapter
  └─ File/Artifact Adapter
  ↓
External Tools (EvalEngine metadata) / External Agents / Benchmarks / Models
  ↓
Auto-Capture Layer
  ↓
Raw Result Store + Artifact Store
  ↓
Normalization Layer
  ↓
Normalized Result Store
  ↓
Comparison + Reporting + Audit
```

---

## 5. User Journey

### 5.1 Main User Flow

The user should experience LabLex like this:

```text
1. Open LabLex.
2. Create Evaluation Run.
3. Select External Tool.
4. Select Agent/Target/System.
5. Select Model/Provider.
6. Select Benchmark / Test Suite (EvalEngine is displayed as metadata derived from the selected ExternalTool; it is not selectable as an independent runtime entity).
7. LabLex validates compatibility.
8. User clicks Run Evaluation.
9. External tool executes.
10. LabLex captures outputs automatically.
11. Results appear inside LabLex.
12. User opens data, comparison, and reports.
```

### 5.1a Component-Agnostic Selection Law (v1.6.3 addition)

LabLex must not assume that every evaluation run requires an Agent, Model, Benchmark, EvalEngine, or specific Tool.

```text
1. No Agent is globally required.
2. No Model is globally required.
3. No Benchmark is globally required.
4. No EvalEngine is selected as an independent runtime entity.
5. No ExternalTool is hardcoded as the product root.
6. Required fields are derived from:
   - selected Evaluation Mode
   - selected ExternalTool manifest
   - selected Target manifest
   - selected Benchmark manifest
   - selected ResultSchema manifest
   - compatibility declarations
7. Optional fields remain optional metadata unless a manifest declares them required.
8. The UI must explain why each field is required.
9. The UI must show all component metadata, capabilities, versions, compatibility rules, warnings, and evidence expectations before RunSpec locking.
```

Evaluation Modes:

```text
Model Endpoint Evaluation:
  Required may include: ExternalTool, Target, ModelProvider, Model, ResultSchema, MetricProfile.
  Agent may be null.
  Benchmark may be required only if the selected tool/schema declares it required.

Agent / Runtime Evaluation:
  Required may include: ExternalTool, Target(agent/runtime), Benchmark/Test Suite, ResultSchema.
  Model may be required only if the agent/tool manifest exposes or requires model binding.

App / API Evaluation:
  Required may include: ExternalTool, Target(application_endpoint), ResultSchema, MetricProfile.
  Agent and Model may be null.

Existing External Output / Manual Import:
  Required: RawResult input + ResultSchema.
  ExternalTool, Target, Model, Benchmark may be optional metadata unless needed for comparison/reporting.

Custom Flow:
  Required components are fully manifest-driven.
```

### 5.2 Secondary Fallback Flow

Manual result upload is only for cases where a run already happened outside LabLex:

```text
Upload existing output → map/validate schema → normalize → display/report
```

This must not be the primary experience.

### 5.3 Day-2 User Flows (v1.5 addition)

```text
Re-Run:
  1. User views completed run.
  2. Clicks "Run Again."
  3. LabLex creates new RunSpec from current manifest versions.
  4. New run executes, captures, normalizes.
  5. User compares new run vs original.

Renormalize:
  1. User sees normalization_failed on a result.
  2. Fixes the ResultSchema (corrects JSONPath mapping).
  3. Clicks "Renormalize" on the result detail page.
  4. LabLex re-applies schema against the stored RawResult.
  5. New NormalizedResult appears. Original is marked superseded.

Register New Tool:
  1. User clicks "Add Tool" from dashboard.
  2. Wizard guides: tool info → connection → adapter → result schema.
  3. Dry-run validates the full pipeline.
  4. Tool is ready for Create Run flow.

Cancel Run:
  1. User views a running evaluation.
  2. Clicks "Cancel."
  3. LabLex propagates cancellation to the external tool via adapter.
  4. Partial results captured if available.
  5. Run marked as cancelled.
```

---

## 6. Core Domains and Entities

### 6.1 Registry Entities

```text
ExternalTool
ToolConnection
Adapter
Target
ModelProvider
Model
EvalEngine
Benchmark
MetricProfile
ResultSchema
ReportTemplate
```

Note: `AgentProfile` was removed in v1.4. Agent/target metadata is fully covered
by the `Target` entity. Keeping a separate AgentProfile added no value and was
never defined with a manifest, schema, or API endpoint.

### 6.2 Runtime Entities

```text
RunSpec
ToolRun
RunEvent
RawResult
NormalizedResult
MetricValue
Trace
LogStream
Artifact
Comparison
Report
ReportExport
AuditEvent
```

### 6.3 Entity Meaning

| Entity | Meaning |
|---|---|
| ExternalTool | External evaluation or execution tool |
| ToolConnection | Credentials/endpoint/CLI path/docker config for a tool |
| Adapter | Invocation and capture strategy |
| Target | System being evaluated: model endpoint, agent, app, API |
| ModelProvider | Provider metadata, e.g. OpenAI/Anthropic/local/custom |
| Model | Specific model configuration |
| Benchmark | Metadata describing external benchmark/test suite |
| RunSpec | Immutable run plan built from selected components |
| ToolRun | Actual execution instance |
| RawResult | Original output exactly as captured |
| NormalizedResult | Canonical shape used for UI/report/comparison |
| Report | Generated interpretation of data |

### 6.4 EvalEngine Clarification (v1.3 addition)

`EvalEngine` is **not** a separate runtime or execution engine owned by LabLex. It is a registry-only metadata entity that represents the external evaluation framework or methodology an `ExternalTool` uses or wraps.

| Concept | Role |
|---|---|
| ExternalTool | The actual tool registered, connected, and executed (e.g. Promptfoo CLI, Inspect AI) |
| EvalEngine | The framework/methodology the tool implements (e.g. LLM-as-Judge, Assertion-Based) |

Rules:

```text
1. EvalEngine has NO adapter, NO connection, NO execution logic.
2. EvalEngine is informational metadata only — used for filtering, grouping, and comparison scoping.
3. A single ExternalTool may reference multiple EvalEngines.
4. EvalEngine is NEVER selected independently in the Create Run flow.
   The user selects an ExternalTool; the EvalEngine is displayed as metadata.
5. If during implementation the EvalEngine entity adds no value beyond
   what ExternalTool.type provides, it must be removed — not kept as dead weight.
```

EvalEngine Manifest Example:

```yaml
kind: eval_engine
id: llm_as_judge
name: LLM-as-Judge
description: Uses a language model to evaluate outputs against criteria
used_by_tools:
  - promptfoo
  - custom_eval_tool
```

---

## 7. Manifest-First Extension Model

Every external component should be addable through a manifest.

### 7.1 External Tool Manifest Example

```yaml
kind: external_tool
id: promptfoo
name: Promptfoo
type: eval_tool
execution_modes:
  - cli
  - docker
capabilities:
  - create_run
  - capture_json_result
  - capture_logs
outputs:
  result_format: json
  artifacts:
    - logs
    - report_html
```

### 7.2 Target Manifest Example

```yaml
kind: target
id: custom_assistant_api
name: Custom Assistant API
type: application_endpoint
connection:
  mode: http_api
capabilities:
  - chat_completion
  - tool_use
```

### 7.3 Benchmark Manifest Example

```yaml
kind: benchmark
id: support_qa_eval
name: Support QA Eval
type: external_test_suite
owned_by: external_tool
metrics:
  - score
  - accuracy
  - latency_ms
  - cost_usd
```

### 7.4 Adapter Manifest Example

```yaml
kind: adapter
id: cli_json_capture_v1
name: CLI JSON Capture Adapter
mode: cli
input:
  runspec: true
output:
  result_file: result.json
  logs: stdout_stderr
security:
  sandbox_required: true
```

---

### 7.5 Adapter Interface Contract (v1.3 addition)

Every adapter, regardless of type, must implement a single programmatic interface. This is the boundary between LabLex core and the external world.

```text
async execute(context: AdapterExecutionContext) → AdapterResult

AdapterExecutionContext:
  run_id: str
  runspec: RunSpecDTO                     # clean serialized JSON/DTO snapshot, NOT active database ORM model
  tool_connection: ResolvedConnection     # credentials resolved at runtime
  workspace_path: str                      # isolated directory for this run
  timeout_seconds: int
  on_progress: Callable[[ProgressEvent], None]  # SSE callback for real-time updates
  env_vars: dict                           # injected secrets as environment variables
  adapter_config: dict                     # adapter-specific configuration from manifest

Note: To prevent database coupling, Adapters must never import or interact with active database models or ORM entities. The runspec is passed as a serialized DTO snapshot containing all required manifest snapshots.

AdapterResult:
  exit_code: int | None                   # null for HTTP/Webhook adapters
  output_files: list[OutputFile]           # path + content_type + size_bytes
  stdout: str | None
  stderr: str | None
  duration_ms: int
  error: str | None
  metadata: dict                           # adapter-specific metadata

OutputFile:
  path: str
  content_type: str                        # application/json, text/csv, etc.
  size_bytes: int
  checksum: str                            # sha256
async cancel(context: AdapterCancellationContext) → CancelResult

AdapterCancellationContext:
  run_id: str
  reason: str                                # user-initiated, timeout, system
  force: bool                                # false = graceful, true = immediate

CancelResult:
  acknowledged: bool                         # adapter confirmed cancellation
  partial_output_available: bool             # some output was captured before cancel
  error: str | None

Cancellation behavior per adapter type:
  CLI:     SIGTERM → grace_period → SIGKILL (per §26.6)
  Docker:  docker stop → grace_period → docker kill
  HTTP:    call tool's cancel endpoint if declared in manifest, else abandon
  Webhook: mark run as cancelled, ignore future callbacks for this run_id
```

Rules:

```text
1. Any adapter that does not implement this interface is rejected.
2. The interface is the ONLY way LabLex core interacts with external tools.
3. Adapter code must never access LabLex database directly.
4. Adapter code must never import LabLex domain models.
5. All communication is through the context input and result output.
6. on_progress callback is optional — adapters that don’t support progress
   simply never call it.
7. cancel() is optional — adapters that don’t support cancellation
   return CancelResult(acknowledged=false). LabLex still marks the run
   as cancelled but logs a warning that the external tool may still be running.
```

### 7.6 Manifest JSON Schema Registry (v1.5 addition)

Every manifest kind must have a corresponding JSON Schema file. "Validated against JSON Schema" is meaningless without actual schema definitions.

```text
Location: /schemas/manifests/{kind}_v{version}.json

Required schema files:
  external_tool_v1.json
  adapter_v1.json
  result_schema_v1.json
  metric_profile_v1.json
  benchmark_v1.json
  target_v1.json
  report_template_v1.json
  model_provider_v1.json
  model_v1.json

Rules:
  1. Schemas are versioned alongside manifest_version.
  2. New manifest_version requires new schema file.
  3. Schemas are loaded at application startup and cached in memory.
  4. POST /api/v1/manifests validates payload against schema BEFORE storing.
  5. Schema validation errors return 400 with field-level detail (§44.4 rule 9).
  6. Schemas are part of the codebase (not user-editable, not stored in DB).
  7. Compatibility declarations (§8.4) are included in each schema:
       compatible_adapters: { type: array, items: { type: string } }
       compatible_result_schemas: { type: array, items: { type: string } }
  8. All manifests share a common base schema:
       kind: { type: string, enum: [...] }
       id: { type: string, pattern: "^[a-z0-9_]+$" }
       name: { type: string }
       schema_version: { type: string }
       manifest_version: { type: string }
       deprecated: { type: boolean, default: false }
```

### 7.7 ReportTemplate Manifest (v1.5 addition)

```yaml
kind: report_template
id: standard_eval_report_v1
name: Standard Evaluation Report
schema_version: "1.0"
manifest_version: "1.0.0"

format: html                         # html | pdf | markdown
layout: single_run                   # single_run | comparison | batch_summary

sections:
  - id: executive_summary
    title: "Executive Summary"
    type: auto                       # auto-populated from NormalizedResult
    required: true

  - id: metric_table
    title: "Metrics"
    type: metric_grid
    columns: [metric_name, value, unit, direction, threshold, pass_fail]
    required: true

  - id: failure_analysis
    title: "Failure Analysis"
    type: auto
    required: false                  # only if failures exist

  - id: cost_summary
    title: "Cost Summary"
    type: auto
    required: false

  - id: user_notes
    title: "User Notes / Commentary"
    type: user_input                 # user-authored text, NOT generated
    required: false

  - id: evidence_appendix
    title: "Evidence"
    type: raw_output_link
    required: true

branding:
  logo_url: null                     # tenant can override
  color_primary: "#1a1a2e"
  font: "Inter"

rules:
  - "Sections with type: auto are populated from NormalizedResult data only."
  - "Sections with type: user_input are NEVER auto-generated by LabLex."
  - "Report generator applies template to data. It does NOT generate narrative text."
  - "Template is tenant-configurable. Default template provided in seed data."
```

---

## 8. Compatibility Model

Compatibility must be explicit. Do not infer compatibility by name matching.

### 8.1 Compatibility Rules

A run is valid only when:

```text
Tool supports selected adapter.
Adapter supports selected execution mode.
Tool supports selected benchmark or benchmark type.
Target supports selected invocation mode.
Model supports selected target or provider binding.
Result schema is compatible with tool output.
Metric profile can map from captured output.
```

### 8.2 Compatibility Matrix Example

| Tool | Adapter | Target Type | Benchmark Type | Result Schema | Status |
|---|---|---|---|---|---|
| Promptfoo | CLI | API endpoint | prompt test suite | promptfoo_json_v1 | compatible |
| ARC Runner | Docker | agent/runtime | interactive benchmark | arc_result_v1 | compatible |
| Custom HTTP Eval | HTTP | model endpoint | custom suite | generic_eval_v1 | compatible |

### 8.3 Forbidden Compatibility Behavior

```text
No fuzzy adapter matching.
No substring matching.
No default assumption that every model works with every agent.
No hidden fallback adapter.
No automatic execution if validation failed.
```

### 8.4 Compatibility Declaration Mechanism (v1.4 addition)

Compatibility is declared explicitly in manifests, not computed or guessed.

```text
ExternalTool manifest declares:
  compatible_adapters: [cli_json_capture_v1, http_json_v1]
  compatible_benchmarks: [support_qa_eval, custom_*]  # wildcard allowed

Adapter manifest declares:
  compatible_result_schemas: [promptfoo_basic_result_v1]
  compatible_execution_modes: [cli, docker]

ResultSchema manifest declares:
  compatible_tools: [promptfoo, inspect_ai]

Target manifest declares:
  compatible_invocation_modes: [http_api, cli]
```

Compatibility Engine validation sequence:

```text
1. tool.compatible_adapters ∩ [selected_adapter] ≠ ∅
2. adapter.compatible_result_schemas ∩ [selected_schema] ≠ ∅
3. adapter.compatible_execution_modes ∩ [tool.execution_modes] ≠ ∅
4. tool.compatible_benchmarks ∩ [selected_benchmark] ≠ ∅ (if benchmark selected)
5. target.compatible_invocation_modes ∩ [adapter.mode] ≠ ∅
6. model.compatible_targets ∩ [selected_target] ≠ ∅
7. model.provider_id == selected_model_provider_id
8. metric_profile.metrics cover all required ResultSchema metric outputs
9. benchmark.required_metrics ⊆ metric_profile.metrics

Any empty intersection → compatibility_failed:
  {
    "check": "tool_adapter_compatibility",
    "status": "fail",
    "detail": "Tool 'promptfoo' does not declare 'webhook_v1' in compatible_adapters."
  }
```

### 8.5 RunSpec Connectivity Pre-check (v1.6 addition)

Before a RunSpec is transitioned from `composed` to `validated`, the API MUST execute a connectivity pre-check:

1. **Verify Tool Endpoint:** Ping the ToolConnection endpoint with a mock health query (using the connection's health_check_url or execution of `cli --version` command for local executors).
2. **Verify Target Availability:** Ping the Target endpoint (if it is a model provider API endpoint) with a minimal request (e.g., token verification) using the resolved tenant credentials.
3. **Fail-Fast Rule:** If any check fails, reject the transition to `validated`. Return HTTP 400 Bad Request detailing the credential or connection error: "Connectivity validation failed: [details]". This prevents bad runs from entering worker queues.

Rules:

```text
1. No implicit compatibility. If not declared, it is incompatible.
2. Wildcard (*) is allowed only in compatible_benchmarks (tool can work with any).
3. Compatibility declarations are validated when manifest is registered.
   Unknown references emit a warning (not an error) at registration time.
4. Compatibility checks are mandatory before RunSpec is composed.
   POST /api/v1/runspecs/compose fails if any check fails.
```

---

## 9. Execution Gateway

The Execution Gateway is the operational center of LabLex.

### 9.1 Responsibilities

```text
1. Receive validated RunSpec.
2. Resolve tool connection.
3. Resolve adapter.
4. Prepare execution config.
5. Start external run.
6. Monitor status.
7. Capture logs and artifacts.
8. Capture result outputs.
9. Mark run status.
10. Send raw outputs to normalization.
```

### 9.2 Execution Modes

| Mode | Use Case |
|---|---|
| HTTP API | External tool exposes API |
| CLI | Tool installed locally/on worker |
| Docker | Tool needs isolated runtime |
| Webhook | External platform sends callback |
| File Capture | Tool writes files to known location |
| Manual Upload | Fallback only |

### 9.3 Run Lifecycle

```text
created
validated
queued
running
capturing_outputs
normalizing
reporting
completed
failed
cancelled
timeout
internal_error          ← v1.5: added for DLQ/system failures (§26.9)
```

### 9.3a State-Activity Mapping (v1.5 addition)

```text
State               Worker Activity (§26.4)      Transition Trigger
─────────────────   ──────────────────────────   ────────────────────────────
created             —                            POST /api/v1/runs
validated           compose_and_validate (1-2)   compatibility pass
queued              —                            added to worker queue
running             start_execution (3-4)        worker picks up task
capturing_outputs   capture_outputs (6)          external tool reports done
normalizing         normalize_results (7)        raw result stored in S3
reporting           generate_report (9)          normalization complete
completed           finalize_run (10)            all steps succeed
failed              finalize_run (10)            any step produces error
cancelled           cancel propagation (§7.5)    user cancels via API
timeout             finalize_run (10)            wall-clock > max_duration
internal_error      DLQ routing (§26.9)          all retries exhausted

Notes:
  - monitor_run_status (step 5 in §26.4) is a CONTINUOUS ACTIVITY during
    the 'running' state, not a separate state.
  - finalize_run (step 10) is a TRANSITION ACTIVITY that sets the terminal
    state (completed/failed/timeout), not a state itself.
```

### 9.4 RunSpec Lifecycle (v1.5 addition)

RunSpec immutability must be enforced, not just declared.

```text
States: draft → composed → validated → locked → archived

  draft:      RunSpec under construction. Fields can be modified.
              Created by: POST /api/v1/runspecs
  composed:   Structural assembly only (no network calls). All components selected.
              Transition: user calls POST /api/v1/runspecs/compose.
  validated:  Compatibility check + manifest schema validation + permissions + active connectivity pre-checks passed.
              Transition: user calls POST /api/v1/runspecs/{id}/validate.
  locked:     IMMUTABLE. No field can be changed.
              Transition: user calls POST /api/v1/runspecs/{id}/lock after validation passes.
              ToolRun can ONLY be created from a locked RunSpec.
  archived:   All runs from this RunSpec are terminal. Read-only.
              Transition: automatic when last ToolRun reaches terminal state.

Flow & Command Map:
  - compose: POST /api/v1/runspecs/compose -> structures the selected components.
  - validate: POST /api/v1/runspecs/{id}/validate -> runs compatibility intersections + manifest schema checks + active endpoint ping pre-checks (§8.5).
  - dry-run: POST /api/v1/runspecs/{id}/dry-run -> generates a full pre-flight report without executing any external evaluation tool.
  - lock: POST /api/v1/runspecs/{id}/lock -> locks the validated RunSpec (sets status to locked).
  - run: POST /api/v1/runs -> spawns a ToolRun from a locked RunSpec only.

Enforcement:
  1. DB: BEFORE UPDATE trigger on runspecs →
       IF status IN ('locked', 'archived') THEN RAISE 'runspec_immutable'.
  2. API: PUT/PATCH /api/v1/runspecs/{id} → 409 if status != 'draft'.
  3. API: POST /api/v1/runs requires runspec.status = 'locked'.
       If not locked → 400: "RunSpec must be validated and locked before creating a run."
  4. Re-run (§52.1) creates a NEW RunSpec, never reuses a locked one.
```

---

## 10. Auto-Capture Layer

Auto-Capture is the correction to the earlier “manual import” confusion.

### 10.1 Main Rule

Results must appear inside LabLex after the user runs from LabLex.

### 10.2 Captured Objects

```text
stdout
stderr
result.json
result.csv
trace.jsonl
logs
screenshots if any
report artifacts
metadata
exit code
runtime duration
cost if available
latency if available
```

### 10.3 Capture Contract

Every adapter must declare:

```text
where outputs are expected
what format is expected
how to parse success/failure
how to capture logs
how to identify artifacts
how to map raw output to normalized result
```

---

## 11. Result Model

### 11.1 Raw Result

RawResult is the original captured output. It must be immutable.

```json
{
  "run_id": "run_001",
  "source_tool_id": "promptfoo",
  "captured_at": "2026-06-20T00:00:00Z",
  "content_type": "application/json",
  "object_ref": "s3://lablex/{tenant_id}/runs/run_001/raw/raw_001.json",
  "checksum": "sha256:...",
  "source_type": "auto_captured",
  "source_ref": null,
  "captured_by": "capture_worker_v1"
}
```

#### source_type values

```text
auto_captured     — result of a LabLex-initiated run (primary path)
manual_upload     — user uploaded an existing result file (fallback only)
webhook_received  — external platform pushed result via webhook
api_submitted     — programmatic submission via LabLex API
```

This field is mandatory and must be stored on every RawResult row. It is used in audit reports to distinguish auto-captured evidence from manually submitted data.

### 11.2 Normalized Result

NormalizedResult is the canonical data used for UI, comparison, and reports.

```json
{
  "run_id": "run_001",
  "raw_result_id": "raw_001",
  "runspec_id": "rs_001",
  "status": "completed",
  "tool_id": "promptfoo",
  "target_id": "assistant_api",
  "model_id": "claude_sonnet",
  "benchmark_id": "support_qa_eval",
  "result_schema_id": "promptfoo_basic_result_v1",
  "result_schema_version": "1.0.0",
  "adapter_id": "cli_json_capture_v1",
  "adapter_version": "1.0.0",
  "manifest_checksum": "sha256:...",
  "normalization_status": "completed",
  "metrics": {
    "score": 0.86,
    "accuracy": 0.83,
    "latency_ms": 1420,
    "cost_usd": 0.52,
    "error_count": 2
  },
  "summary": {
    "pass": true,
    "failure_reasons": []
  }
}
```

#### normalization_status values

```text
pending              — not yet normalized
completed            — normalization succeeded
normalization_failed — required field missing or mapping error
schema_mismatch      — raw output does not match declared ResultSchema
superseded           — replaced by a newer NormalizedResult via renormalize (§52.2)
```

Any normalization failure must be visible on the Result Detail page. Silent nulls are forbidden.

### 11.3 Normalized Sample (v1.6 addition)

To support detailed comparison matrices and highlight specific failures in the UI, LabLex normalizes individual test-case runs (trials/samples) within the `NormalizedResult`:

```json
{
  "id": "nsmp_001",
  "normalized_result_id": "nres_001",
  "sample_id": "test_case_47",
  "input_text": "Translate 'hello' to French.",
  "expected_output": "Bonjour",
  "output_text": "Bonjour",
  "status": "completed",
  "latency_ms": 320,
  "error_message": null,
  "raw_sample_ref": "$.results[46]",
  "metrics": {
    "score": 1.0,
    "accuracy": 1.0
  },
  "metadata": {
    "category": "translation_basics"
  }
}
```

This structural breakdown allows comparing exact prompt inputs and outputs across multiple models/runs while maintaining a neutral, external-first schema (the system does not execute the test cases or calculate the scores; it only normalizes the external output array).

---

## 12. Data Storage Architecture

### 12.1 PostgreSQL

Use PostgreSQL as the source of truth for structured metadata, normalized results, run states, report metadata, registry entries, and audit logs.

### 12.2 JSONB Usage

Use JSONB for flexible structured fields such as:

```text
manifest body
runspec body
normalized metrics payload
adapter config
schema mapping
report config
normalization_mapping_snapshot
tool_manifest_snapshot
adapter_manifest_snapshot
result_schema_snapshot
```

But do not store everything as JSONB. Keep important filter/sort fields as relational columns.

### 12.3 Object Storage

Use S3-compatible object storage or MinIO locally for:

```text
raw result files
large logs
trace files
artifacts
exports
PDF reports
HTML reports
```

#### Object Storage Path Convention

All paths must follow this tenant-scoped convention:

```text
s3://lablex/{tenant_id}/runs/{run_id}/raw/{raw_result_id}.json
s3://lablex/{tenant_id}/runs/{run_id}/logs/{log_id}.log
s3://lablex/{tenant_id}/runs/{run_id}/traces/{trace_id}.jsonl
s3://lablex/{tenant_id}/runs/{run_id}/artifacts/{artifact_id}/{filename}
s3://lablex/{tenant_id}/reports/{report_id}/exports/report.html
s3://lablex/{tenant_id}/reports/{report_id}/exports/report.pdf
s3://lablex/{tenant_id}/reports/{report_id}/exports/report.csv
```

Rules:
```text
1. Every path must include tenant_id as the first segment.
2. No cross-tenant paths are permitted.
3. Path structure is set at object creation and never changed.
4. Presigned URLs must be scoped to the requesting tenant.
5. Lifecycle policies can be applied per tenant prefix.
```

### 12.4 Database Tables

```text
tenants
users
roles
memberships
api_keys
secret_refs
tenant_quotas
tenant_retention_config
invitations

external_tools
tool_connections
adapters
targets
model_providers
models
eval_engines
benchmarks
metric_profiles
result_schemas
report_templates
manifests
manifest_snapshots

runspecs
runspec_snapshots
tool_runs
run_events
idempotency_keys
raw_results
normalized_results
normalized_samples
metric_values
traces
logs
artifacts

comparisons
comparison_items
reports
report_exports
audit_events
batches
notifications
notification_webhooks
user_notification_preferences
```

### 12.4a Table Relationships (v1.4 addition)

```text
tool_runs:
  runspec_id FK → runspecs.id          — 1 RunSpec : N ToolRuns (re-runs allowed)
  batch_id FK → batches.id (nullable)  — null if not part of a batch

normalized_results:
  raw_result_id FK → raw_results.id    — 1:1 mandatory reference (§25.7 rule 2)
  run_id FK → tool_runs.id

normalized_samples:
  normalized_result_id FK → normalized_results.id (ON DELETE CASCADE)

Manifest tenant scoping:
  manifests table unique constraint: (tenant_id, kind, id)
  NOT global (kind, id). Each tenant owns its own manifests.
  Cross-tenant manifest sharing is post-MVP (import/export).

batches (v1.5 full schema):
  id              UUID PK
  tenant_id       UUID FK → tenants.id        NOT NULL
  status          ENUM(pending, running, completed, partial_failure, failed) NOT NULL
  total_runs      INT NOT NULL
  completed_runs  INT DEFAULT 0
  failed_runs     INT DEFAULT 0
  max_parallel    INT DEFAULT 3
  idempotency_key VARCHAR(255) NULLABLE
  created_by      UUID FK → users.id
  created_at      TIMESTAMPTZ NOT NULL
  updated_at      TIMESTAMPTZ NOT NULL

secret_refs (v1.6 full schema):
  id              UUID PK
  tenant_id       UUID FK → tenants.id        NOT NULL
  name            VARCHAR(255) NOT NULL       — unique per tenant
  encrypted_value TEXT NOT NULL               — ciphertext (AES-GCM-256)
  key_version     VARCHAR(50) NOT NULL        — KMS key version used
  created_at      TIMESTAMPTZ NOT NULL
  updated_at      TIMESTAMPTZ NOT NULL
  UNIQUE(tenant_id, name)

normalized_samples (v1.6.1 full schema):
  id                   UUID PK
  tenant_id            UUID FK → tenants.id        NOT NULL
  normalized_result_id UUID FK → normalized_results.id ON DELETE CASCADE NOT NULL
  sample_id            VARCHAR(255) NOT NULL
  input_text           TEXT NULLABLE
  expected_output      TEXT NULLABLE
  output_text          TEXT NULLABLE
  error_message        TEXT NULLABLE
  raw_sample_ref       VARCHAR(500) NULLABLE       — JSONPath or line pointer
  metrics              JSONB NOT NULL              — key-value metrics payload
  status               ENUM(completed, failed) NOT NULL
  latency_ms           INT NULLABLE
  metadata             JSONB NULLABLE              — custom sample metadata
```

### 12.5 Required Database Indexes (v1.3 addition)

Every table must have indexes that support its primary query patterns. No table ships without indexes.

```text
tool_runs:
  - (tenant_id, status)                   — active run count for quota checks
  - (tenant_id, created_at DESC)           — run listing and pagination
  - (tenant_id, tool_id, status)           — per-tool filtering
  - (runspec_hash, tenant_id)              — duplicate run detection
  - (tenant_id, benchmark_id, model_id)    — comparison candidate queries

normalized_results:
  - (run_id)                               — result lookup by run
  - (tenant_id, created_at DESC)           — listing
  - (tenant_id, tool_id, benchmark_id)     — comparison queries
  - (normalization_status, tenant_id)      — failure monitoring

normalized_samples:
  - (normalized_result_id)                 — lookup by result
  - (tenant_id, status)                    — aggregated sample stats and failures

raw_results:
  - (run_id)                               — raw result lookup
  - (tenant_id, storage_status)            — retention cleanup
  - (tenant_id, source_type)               — source tracking queries

audit_events:
  - (tenant_id, timestamp DESC)            — audit log browsing
  - (resource_type, resource_id)           — resource audit trail
  - (actor_user_id, tenant_id)             — user activity queries

idempotency_keys:
  - (key, tenant_id) UNIQUE                — idempotency lookup
  - (expires_at)                           — cleanup job

run_events:
  - (run_id, id)                           — SSE replay
  - (run_id, event)                        — event type filtering

manifests:
  - (tenant_id, kind, deprecated)          — registry browsing with deprecation filter
  - (kind, id) UNIQUE                      — manifest identity

comparisons:
  - (tenant_id, created_at DESC)           — listing

reports:
  - (tenant_id, created_at DESC)           — listing
  - (tenant_id, storage_status)            — retention queries

batches:
  - (tenant_id, created_at DESC)           — listing
  - (tenant_id, status)                    — active batch monitoring

tool_runs (additional):
  - (batch_id)                             — batch member lookup
  - (runspec_id)                           — re-run history

notifications:
  - (user_id, tenant_id, read, created_at DESC) — user notification feed
  - (tenant_id, event_type)                — event filtering

tenant_quotas:
  - (tenant_id)                            — quota lookup

tenant_retention_config:
  - (tenant_id)                            — retention config lookup

invitations:
  - (tenant_id)                            — tenant invitation listing
  - (token) UNIQUE                         — token verification lookup
```

Rules:

```text
1. No table is deployed to production without its required indexes.
2. Every new query pattern must have a supporting index.
3. Composite indexes must follow the order: equality columns first, range/sort columns last.
4. EXPLAIN ANALYZE must be run on all list queries during development.
5. Indexes are part of Alembic migrations, not afterthoughts.
```

---

## 13. API Architecture

### 13.1 API Style

Use FastAPI with OpenAPI-first discipline.

All endpoints must be documented and stable.

### 13.2 Authentication

Every API request must be authenticated. Two authentication modes:

```text
JWT session token     — for UI users (cookie or Authorization header)
API key               — for programmatic access and adapter callbacks
```

Every write endpoint must enforce:

```text
authenticated actor (user_id or api_key_id)
tenant_id (resolved from token/key)
role permission check
audit event creation
```

All tenant-owned resources must be scoped by tenant_id at query time. Row-Level Security (RLS) on PostgreSQL is a mandatory gate for the SaaS deployment phase (see §43, GATE 22).

### 13.3 Core APIs

All API endpoints MUST be prefixed with `/api/v1/` as the single authoritative API contract.

Rules:
1. Only `/api/v1/*` routes are valid implementation targets.
2. Unversioned endpoint mentions (e.g. in text descriptions or diagrams) are documentation shorthand, not implementation targets. Aliases without versioning must not be built.

```text
POST   /api/v1/manifests/validate
POST   /api/v1/manifests
POST   /api/v1/manifests/batch
GET    /api/v1/manifests

GET    /api/v1/external-tools
POST   /api/v1/external-tools
GET    /api/v1/external-tools/{id}
POST   /api/v1/external-tools/{id}/test-connection

GET    /api/v1/targets
POST   /api/v1/targets
POST   /api/v1/targets/{id}/test-connection

GET    /api/v1/adapters
POST   /api/v1/adapters
POST   /api/v1/adapters/{id}/validate

GET    /api/v1/models
POST   /api/v1/models

GET    /api/v1/benchmarks
POST   /api/v1/benchmarks

GET    /api/v1/result-schemas
POST   /api/v1/result-schemas
POST   /api/v1/result-schemas/{id}/validate

POST   /api/v1/runspecs/compose
POST   /api/v1/runspecs/{id}/validate
POST   /api/v1/runspecs/{id}/dry-run
POST   /api/v1/runspecs/{id}/lock
GET    /api/v1/runspecs/{id}

POST   /api/v1/runs
POST   /api/v1/runs/batch
GET    /api/v1/runs
GET    /api/v1/runs/{id}
POST   /api/v1/runs/{id}/cancel
POST   /api/v1/runs/{id}/rerun
GET    /api/v1/runs/{id}/events                       ← SSE endpoint
GET    /api/v1/runs/{id}/logs
GET    /api/v1/runs/{id}/artifacts

GET    /api/v1/results
GET    /api/v1/results/{run_id}
GET    /api/v1/results/{run_id}/raw
GET    /api/v1/results/{run_id}/normalized
POST   /api/v1/results/{run_id}/renormalize

POST   /api/v1/comparisons
GET    /api/v1/comparisons/{id}

POST   /api/v1/reports
GET    /api/v1/reports/{id}
POST   /api/v1/reports/{id}/export
POST   /api/v1/reports/batch-export

GET    /api/v1/metric-profiles
POST   /api/v1/metric-profiles
GET    /api/v1/metric-profiles/{id}

GET    /api/v1/batches/{batch_id}
GET    /api/v1/batches/{batch_id}/events              ← SSE endpoint

GET    /api/v1/audit-events

GET    /api/v1/notifications
PATCH  /api/v1/notifications/{id}/read
POST   /api/v1/notifications/mark-all-read

GET    /api/v1/api-keys
POST   /api/v1/api-keys
DELETE /api/v1/api-keys/{id}
POST   /api/v1/api-keys/{id}/revoke

GET    /api/v1/admin/dlq
POST   /api/v1/admin/dlq/replay
POST   /api/v1/admin/dlq/{id}/retry
POST   /api/v1/admin/dlq/{id}/discard

POST   /api/v1/webhooks/{webhook_token}               ← Webhook callback receiver

POST   /api/v1/tenant/export
DELETE /api/v1/tenant

GET    /api/v1/health
```

### 13.3a OpenAPI Specification (v1.5 addition)

```text
1. An OpenAPI 3.1 specification file is the single source of truth for API contracts.
2. Location: /docs/openapi.yaml (committed to repository).
3. Spec is auto-generated from code annotations (FastAPI generates this natively).
4. Every PR that changes an API endpoint must update the OpenAPI spec.
5. Contract tests (schemathesis) validate responses against this spec in CI.
6. Breaking changes detected by OpenAPI diff tool before merge.
7. Spec is served at GET /api/v1/docs (Swagger UI) and GET /api/v1/openapi.json.
```

### 13.4 Dry-Run Behavior

`POST /api/v1/runspecs/{id}/dry-run` must:

```text
1. Confirm external-tool connection is reachable.
2. Confirm target is reachable.
3. Confirm adapter is valid and compatible.
4. Confirm result schema is compatible with adapter output.
5. Confirm permissions are valid.
6. NOT execute the external tool.
7. Return a validation report with pass/fail per check.
```

This is the mandatory pre-flight check before any real run.

### 13.5 API Pagination & Filtering Contract (v1.3 addition)

Every list endpoint must support pagination, filtering, and sorting. No unbounded `SELECT *` is permitted.

```text
Query Parameters (all list endpoints):
  ?page=1                                  — page number (1-indexed)
  ?page_size=50                            — items per page (max: 100, default: 50)
  ?sort_by=created_at                      — sort field
  ?order=desc                              — sort order (asc | desc)
  ?cursor=eyJ...                           — cursor-based pagination (preferred over offset)
```

Filtering varies by resource:

```text
GET /api/v1/runs:
  ?status=completed,failed                 — multi-value enum filter
  ?tool_id=promptfoo
  ?model_id=claude_sonnet
  ?benchmark_id=support_qa_eval
  ?created_after=2026-01-01T00:00:00Z
  ?created_before=2026-06-01T00:00:00Z

GET /api/v1/results:
  ?normalization_status=completed
  ?tool_id=promptfoo

GET /reports:
  ?storage_status=active
  ?report_type=comparison
```

Response Envelope:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 50,
    "total_count": 1234,
    "has_next": true,
    "has_previous": false,
    "next_cursor": "eyJ..."
  }
}
```

Rules:

```text
1. Default page_size: 50. Max page_size: 100.
2. Cursor-based pagination is preferred for large datasets.
3. Offset pagination is allowed for small, stable datasets.
4. total_count may be approximate for tables with >100k rows.
5. Empty result: return 200 with data: [] (not 404).
```

### 13.6 API Versioning (v1.3 addition)

All API endpoints must be version-prefixed from day one.

```text
URL pattern: /api/v1/runs, /api/v1/manifests, /api/v1/reports, etc.

Versioning rules:
1. URL path prefix is the primary version indicator.
2. Breaking changes require a new major version (/api/v2/).
3. v1 endpoints maintained for minimum 12 months after v2 launch.
4. Deprecation-Sunset headers added 3 months before removal:
     Deprecation: true
     Sunset: Sat, 01 Jan 2028 00:00:00 GMT
5. Non-breaking additions (new optional fields, new endpoints) do NOT require version bump.
6. Removing a field, changing a field type, or changing response shape = breaking change.
```

### 13.7 API Rate Limiting (v1.3 addition)

Rate limits protect LabLex infrastructure independent of run quotas (Section 34).

```text
Per API key:
  100 requests/minute on all endpoints (default)
  10 requests/minute on POST /api/v1/runs (high-cost operation)

Per authenticated user session:
  300 requests/minute on all endpoints (default)
  20 requests/minute on POST /api/v1/runs

Per IP (unauthenticated):
  20 requests/minute (login/health endpoints only)
```

Response on breach:

```text
HTTP 429 Too Many Requests
Headers:
  Retry-After: 32                          — seconds until limit resets
  X-RateLimit-Limit: 100
  X-RateLimit-Remaining: 0
  X-RateLimit-Reset: 1719849600            — Unix timestamp

Body:
{
  "error": "rate_limit_exceeded",
  "retry_after_seconds": 32,
  "detail": "API key rate limit exceeded. 100 requests/minute."
}
```

Implementation: Redis sliding window counter. Fallback to in-memory counter if Redis is unavailable.

### 13.8 Batch Operations (v1.3 addition)

Batch endpoints are required for professional use cases (e.g. evaluating one benchmark across 10 models).

```text
POST /api/v1/runs/batch
  Body:
  {
    "runspecs": [RunSpec, RunSpec, ...],
    "max_parallel": 3,
    "idempotency_key": "batch_001"
  }
  Response:
  {
    "batch_id": "batch_001",
    "run_ids": ["run_001", "run_002", ...],
    "status": "queued",
    "total": 10,
    "max_parallel": 3
  }

GET /api/v1/batches/{batch_id}
  Response:
  {
    "batch_id": "batch_001",
    "status": "running",
    "progress": { "completed": 4, "running": 3, "queued": 3, "failed": 0 },
    "run_ids": [...]
  }

POST /api/v1/manifests/batch
  Body: { "manifests": [...] }
  Response:
  {
    "results": [
      { "id": "m_001", "status": "created" },
      { "id": "m_002", "status": "error", "error": "schema_invalid" }
    ]
  }

POST /api/v1/reports/batch-export
  Body: { "report_ids": [...], "format": "html" }
  Response: { "export_id": "exp_001", "status": "processing" }
```

Rules:

```text
1. Max batch size: 50 runspecs per batch.
2. Batch operations are subject to the same tenant quota limits.
3. Each run in a batch gets its own idempotency protection.
4. Batch status is queryable via SSE: GET /api/v1/batches/{batch_id}/events.
5. Partial batch failure does NOT cancel remaining runs.
```

---

## 14. Reporting Architecture

Reporting is a core capability, not a polish feature.

### 14.1 Report Types

```text
Single Run Report
Comparison Report
Technical Audit Report
Executive Summary Report
Failure Analysis Report
Cost/Latency Report
Benchmark Summary Report
Model Performance Report
```

### 14.2 Minimum Report Sections

```text
1. Run Summary
2. Selected Components
3. Configuration Snapshot
4. Metrics Summary
5. Cost/Latency/Errors
6. Logs/Artifacts Availability
7. Failure Analysis
8. Comparison if selected
9. User Notes / Commentary (user-authored, NOT LabLex-generated recommendations)
10. Evidence Appendix
```

### 14.2a Report Generator External-First Rule (v1.5 addition)

```text
The Report Generator is a DATA + TEMPLATE engine. It is NOT an interpretation engine.

What it does:
  1. Receives: NormalizedResult data + ReportTemplate manifest.
  2. Applies template sections to data fields (fill slots).
  3. Outputs: formatted document (HTML/PDF/Markdown).

What it MUST NOT do:
  1. Generate narrative text explaining results.
  2. Produce recommendations about which model/tool is better.
  3. Interpret metric values ("this score is good/bad").
  4. Rank, score, or weight models beyond per-metric direction comparison.
  5. Use any ML/NLP to summarize or explain data.

Sections with type: auto (§7.7):
  These render DATA (numbers, tables, charts) from NormalizedResult.
  They do NOT generate explanatory text.
  Example: metric_grid renders a table of metric values.
           failure_analysis renders a list of failure_reasons from data.
           It does NOT explain WHY failures happened.

Sections with type: user_input (§7.7):
  These are user-authored free text.
  LabLex renders them as-is. No modification, no generation.

Violation of this rule = violation of External-First principle.
```

### 14.3 Export Formats

```text
HTML first
JSON export
CSV export
PDF later but planned
```

Do not delay reporting until late project phases.

---

## 15. UI Architecture

### 15.1 Main Navigation

```text
Dashboard
Create Run
Runs
Results
Compare
Reports
External Tools
Registries
Settings
```

### 15.1a Dashboard Metrics (v1.3 addition)

The Dashboard is the first screen the user sees. It must provide immediate operational awareness.

```text
Required Dashboard Widgets:
  1. Active Runs          — real-time count of currently running evaluations
  2. Run Success Rate     — pie chart: completed vs failed vs timed_out (today/week/month toggle)
  3. Recent Runs          — last 10 runs with status, tool, model, duration
  4. Quota Usage          — bar chart: current usage vs tenant limits
  5. Failed Runs          — list of recent failures requiring attention (clickable → Run Detail)
  6. Top Tools by Usage   — ranked list of most-used external tools
  7. Normalization Health — % of runs with normalization_warnings or normalization_failed
  8. Run Volume Trend     — line chart: runs per day over last 30 days

Optional Widgets (post-MVP):
  9. Cost Summary         — total cost_usd across runs (if available)
  10. User-Configured Metric Sort View — user selects metric + direction → sorted
      model list. NOT an auto-generated leaderboard. User MUST choose what metric
      to sort by and confirm the direction. LabLex never auto-ranks models.
```

Rules:

```text
1. Dashboard must load in under 2 seconds.
2. Active Runs widget updates in real-time via SSE or polling (5-second interval).
3. All widgets respect tenant scoping — no cross-tenant data.
4. Empty state: show onboarding guidance ("Register your first External Tool"), not a blank page.
5. Each widget links to its detail page (e.g. Failed Runs → Runs page filtered by status=failed).
```

### 15.2 Create Run UX — Component-Agnostic Flow (v1.6.3 update)

Create Run must not be a fixed Agent → Model → Benchmark pipeline. It is a component-agnostic wizard driven by Evaluation Mode and manifests.

```text
Step 1: Choose Evaluation Mode
        - Model Endpoint
        - Agent / Runtime
        - App / API
        - Existing External Output
        - Custom Evaluation Flow

Step 2: Show Required Components for this mode
        Requirements are derived from the selected Evaluation Mode and manifests.
        The UI must explain why each field is required.

Step 3: User selects components from Registry
        ExternalTool / Target / ModelProvider / Model / Benchmark / MetricProfile / ResultSchema / ReportTemplate.
        Components not required by the selected mode remain optional or hidden as advanced metadata.

Step 4: Show All Component Data
        metadata, capabilities, versions, schemas, compatibility declarations,
        required outputs, expected artifacts, security requirements, and warnings.

Step 5: Validate Compatibility
        Run compatibility intersections, permissions, manifest schemas, and connectivity pre-checks.

Step 6: Generate RunSpec Preview
        Show selected components, derived metadata, required/optional fields,
        manifest snapshots, config hash, schema mappings, evidence plan, and warnings.

Step 7: Lock RunSpec
        Only a validated RunSpec can be locked. Locked RunSpecs are immutable.

Step 8: Run Evaluation
        External execution proceeds only through the selected adapter and only after validation.
```

Forbidden Create Run behavior:

```text
agent_id required globally          — forbidden
model_id required globally          — forbidden
benchmark_id required globally      — forbidden
eval_engine_id selectable directly  — forbidden
hidden default model                — forbidden
hidden default benchmark            — forbidden
hidden default external tool         — forbidden
```

### 15.3 Result Detail Page

```text
Summary cards
Metric table
Charts
Raw output viewer
Normalized result viewer
Logs
Artifacts
Trace/timeline
Report panel
Comparison shortcut
```

### 15.4 UX Anti-Patterns

```text
Do not start user with Adapter selection.
Do not expose low-level manifest details first.
Do not make “manual import” primary.
Do not make the first screen empty without guidance.
Do not use Hermes/Digital State/Prime/Builder/Auditor terminology.
```

---

## 16. Security Architecture

Running external tools is dangerous if not isolated.

### 16.1 Security Rules

```text
1. Store secrets encrypted using KMS envelope encryption (never as plaintext).
2. Restrict CLI execution to controlled workers.
3. Docker execution must be rootless where possible.
4. No privileged containers.
5. Apply seccomp profile for container runs.
6. Add network allowlists for HTTP adapters.
7. Validate webhook signatures.
8. Protect against replay attacks.
9. Timeouts are mandatory.
10. Output size limits are mandatory.
11. Artifact scanning is a mandatory gate before SaaS deployment (§43, GATE 21).
12. Every run must be auditable.
```

### 16.1a Frontend Security (v1.4 addition)

```text
1. Content-Security-Policy header on all pages.
2. External tool outputs rendered in sandboxed iframe or with strict HTML escaping.
   Raw output viewer must NEVER render untrusted HTML directly.
3. CORS policy: allow only CORS_ORIGINS from .env configuration.
4. All user-uploaded content served with Content-Disposition: attachment.
5. SVG uploads blocked or sanitized (XSS vector).
```

### 16.2 Secrets

```text
1. secret_refs table stores encrypted ciphertext values, not plaintext.
2. Local database-level secrets are encrypted at rest using tenant DEK + KMS KEK envelope encryption (§16.6).
3. No external secret manager (like Vault) is required for the MVP or local development.
4. Pluggable backend: Integration with an external Secret Manager (e.g. AWS Secrets Manager or HashiCorp Vault) is supported as an optional post-MVP backend.
```

### 16.3 Multi-Tenancy

For SaaS future-readiness:

```text
All tenant-owned rows must include tenant_id.
Use RBAC early.
PostgreSQL Row-Level Security (RLS) is a mandatory gate for the SaaS deployment phase (see §43, GATE 22).
```

### 16.4 Presigned URL Enforcement (v1.4 addition)

```text
1. Only the API server generates presigned URLs (never workers, never frontend).
2. API validates tenant_id from JWT/API key before generating URL.
3. Presigned URL path must match requesting tenant's {tenant_id} prefix.
4. Presigned URL expiry: 15 minutes (configurable).
5. Presigned URLs are single-use where possible (S3 limitation may prevent this).
6. All presigned URL generations are logged with request_id and tenant_id.
```

### 16.5 API Versioning Rules (v1.6 addition)

```text
1. All routes must be versioned with a major prefix (e.g., /api/v1/...).
2. Major versions are breaking changes; minor updates must be backward compatible.
3. Deprecation policy: provide 2 versions of overlap before removing old endpoints.
4. Versioning must be enforced at the Router level in FastAPI.
```

### 16.6 KMS Envelope Encryption Flow (v1.6 addition)

To secure credentials and sensitive API keys of tenants:

1. **Integration:** LabLex integrates with a Key Management Service (AWS KMS, GCP KMS, or HashiCorp Vault) containing a primary Key Encryption Key (KEK).
2. **Tenant Data Encryption Key (DEK):** Each tenant has a unique DEK generated at tenant creation:
   - The DEK is generated in-memory.
   - The DEK is encrypted using the KMS primary KEK and stored in the database: `tenants.encrypted_dek`.
3. **Secret Encryption:** When storing a credential (e.g. `secret_refs` values):
   - The API decrypts `tenants.encrypted_dek` using KMS to get the plaintext DEK.
   - The secret value is encrypted using AES-256-GCM with the plaintext DEK and a secure random IV.
   - The encrypted ciphertext + IV + KMS key version are stored in the `secret_refs.encrypted_value` column.
   - The plaintext secret and plaintext DEK are immediately scrubbed from memory.
4. **Runtime Injection:** When executing a run:
   - The worker requests the decrypted DEK for the tenant from the API.
   - The worker decrypts the required secret value in-memory, injects it into the `env_vars: dict` parameter of the adapter's `execute()` method, and purges all plaintext key references from memory immediately after starting the subprocess/execution.
5. **Implementation Environments (Local vs. Production):**
   - **Local Development:** Use a local KEK provider backed by `ENCRYPTION_KEY` in the `.env` configuration.
   - **Production:** Use a real KMS/Vault-backed KEK provider.
   - The encryption interface (`KMSProvider` interface) must be identical in both modes, enabling seamless environment-based swapping.

---

## 17. Observability Architecture

LabLex must observe itself.

Track:

```text
run duration
adapter failure rate
external tool timeout rate
normalization failure rate
capture failure rate
report generation time
queue depth
artifact size
API latency
worker health
```

### 17.1 Run SLO Metrics (v1.2 addition)

These metrics are required before any external tool goes live in production:

```text
run_success_rate              — % of runs ending in completed (target: >95%)
p95_run_duration              — 95th percentile run wall-clock time per adapter type
p95_normalization_time        — 95th percentile normalization processing time
report_generation_failure_rate— % of reports that fail to generate
capture_failure_rate          — % of runs where auto-capture fails
tenant_quota_rejection_rate   — % of run requests rejected due to quota limits
normalization_warning_rate    — % of normalized results with non-empty warnings
schema_mismatch_rate          — % of normalizations hitting schema_mismatch status
```

Alert thresholds must be set before production. Missing SLO metrics is a deployment blocker.

Use OpenTelemetry-compatible instrumentation for all metrics.

---

## 18. Recommended Tech Stack

| Layer | Recommended Choice |
|---|---|
| Frontend | Next.js + TypeScript |
| UI | Tailwind + shadcn/ui |
| Charts | Recharts first |
| Backend | FastAPI |
| Validation | Pydantic v2 + JSON Schema |
| API Spec | OpenAPI 3.1 |
| Database | PostgreSQL |
| Migrations | Alembic |
| Cache/Locks | Redis |
| Workers MVP | Worker abstraction + RQ/Celery option |
| Workflow later | Temporal |
| Object Storage | S3-compatible / MinIO local |
| Observability | OpenTelemetry |
| Local Dev | Docker Compose |
| Testing | pytest + Playwright |

---

## 19. MVP Plan (v1.3 Rewrite)

Each MVP phase has explicit deliverables, dependencies, and completion criteria. No phase starts before the previous phase’s criteria are met.

### MVP-0: Foundation (Weeks 1–2)

Dependencies: None.

```text
Deliverables:
  ☐ Project scaffolding: FastAPI backend + Next.js frontend
  ☐ docker-compose.yml: PostgreSQL + Redis + MinIO + backend + frontend + worker
  ☐ .env.example with all required environment variables
  ☐ Alembic migration infrastructure
  ☐ Database schema: tenants, users, memberships, api_keys tables
  ☐ JWT authentication + tenant scoping middleware
  ☐ RBAC middleware with permission checks on all write endpoints
  ☐ Health check endpoint: GET /api/v1/health
  ☐ Seed data script: default tenant + admin user
  ☐ Unified Error Model: all endpoints return consistent error responses
  ☐ CI pipeline: lint + type-check + unit tests

Completion Criteria:
  docker-compose up → login → see empty dashboard with auth working.
  All write endpoints require authentication.
  Tenant A cannot see tenant B data.
  Error responses follow unified format on all endpoints.
```

### MVP-1: First Mock Run (Weeks 3–6)

Dependencies: MVP-0 complete.

```text
Deliverables:
  ☐ Manifest schema validation (JSON Schema)
  ☐ Registry APIs: external_tools, targets, models, benchmarks, adapters, result_schemas
  ☐ Registry UI: list, create, detail pages for all registry entities
  ☐ Compatibility validation engine
  ☐ RunSpec composer API: POST /api/v1/runspecs/compose + POST /api/v1/runspecs/{id}/validate + POST /api/v1/runspecs/{id}/dry-run
  ☐ Mock Adapter implementation (generates synthetic results via Adapter Interface)
      → Mock Adapter is a DEVELOPMENT/TESTING tool only.
      → It simulates an external tool's behavior through the same Adapter Interface.
      → It is NOT an internal eval engine, NOT an internal scorer, NOT a benchmark runner.
      → It must NEVER be used in production as a substitute for real external tools.
      → Its sole purpose: validate the LabLex pipeline before real tools are connected.
  ☐ Execution Gateway: run lifecycle (created → validated → queued → running → completed/failed)
  ☐ Worker infrastructure: task queues with RQ or Celery
  ☐ Auto-capture layer: capture mock adapter output
  ☐ Raw result storage (PostgreSQL + MinIO)
  ☐ Normalization engine: ResultSchema-driven JSONPath extraction
  ☐ Normalized result storage
  ☐ Result Detail Page: summary cards, metric table, raw viewer, normalization warnings
  ☐ SSE streaming: GET /api/v1/runs/{run_id}/events (basic lifecycle events)
  ☐ HTML Report v1: single-run report generation
  ☐ Create Run UI: 7-step wizard
  ☐ API pagination on all list endpoints
  ☐ Database indexes for all primary query patterns
  ☐ Test fixtures: mock raw outputs in multiple formats (JSON, CSV)

Completion Criteria:
  User creates a run with Mock Adapter → sees real-time progress via SSE →
  raw result captured → normalization produces NormalizedResult →
  Result Detail Page shows metrics → HTML Report generated.
  Full cycle works end-to-end in under 30 seconds.
  Missing required field → normalization_failed (not silent null).
```

### MVP-2: Professional Results (Weeks 7–10)

Dependencies: MVP-1 complete. At least 5 successful mock runs exist.

```text
Deliverables:
  ☐ Comparison v1: same_tool_same_benchmark comparisons with metric deltas
  ☐ Comparison UI: side-by-side metric table, delta column, winner indicators
  ☐ Report templates system
  ☐ Comparison Report generation
  ☐ CSV/JSON export for results and comparisons
  ☐ Logs viewer on Result Detail Page
  ☐ Artifacts viewer on Result Detail Page
  ☐ Failure analysis: basic failure reason display
  ☐ Connection test endpoints: all 6 test/validate/dry-run endpoints
  ☐ Audit log: audit_events table + viewer UI
  ☐ Idempotency: Idempotency-Key on POST /api/v1/runs
  ☐ Duplicate run detection with HTTP 409
  ☐ Resource quotas: tenant_quotas enforcement with HTTP 429
  ☐ SSE replay: Last-Event-ID reconnect support + heartbeat
  ☐ Dashboard metrics widgets (Section 15.1a)
  ☐ Batch run creation: POST /api/v1/runs/batch
  ☐ Caching layer: Redis cache for manifests, quotas, and active run counts
  ☐ API rate limiting

Completion Criteria:
  User compares two mock runs → sees winner per metric →
  generates Comparison Report → exports as CSV.
  Duplicate run is rejected with 409.
  Quota breach returns 429 with detail.
  Dashboard shows accurate real-time data.
  SSE reconnects seamlessly after disconnect.
```

### MVP-3: Real Integrations (Weeks 11–16)

Dependencies: MVP-2 complete. All mock-based flows stable.

```text
Deliverables:
  ☐ CLI Adapter: real subprocess execution with workspace isolation
  ☐ HTTP Adapter: real external API calls with retry logic
  ☐ First real external tool integration (Promptfoo or Inspect AI)
  ☐ Docker Adapter: rootless container execution with seccomp
  ☐ Webhook Adapter: inbound processing with HMAC-SHA256 verification
  ☐ CLI timeout policy: SIGTERM → grace → SIGKILL
  ☐ Circuit breaker per external tool
  ☐ PDF export for reports
  ☐ Advanced report types: Technical Audit, Executive Summary, Failure Analysis
  ☐ Manifest deprecation lifecycle (active → deprecated → retired)
  ☐ Report provenance and hash verification
  ☐ Retention policy enforcement (background cleanup job)
  ☐ Metric direction rules in MetricProfile manifests
  ☐ Notification system: in-app notifications for run completion/failure
  ☐ OpenTelemetry instrumentation + SLO metrics + alerting
  ☐ Plugin/Adapter SDK documentation

Completion Criteria:
  User runs a real evaluation with Promptfoo CLI Adapter →
  real results captured and normalized →
  compared with previous runs →
  professional report generated and exported as PDF.
  All v1.4 acceptance criteria (Section 42) are met.
  All 22 production gates (Section 43) are green.
```

---

## 20. Execution Order

```text
1. Architecture constitution
2. Domain model
3. Manifest schemas (with compatibility declarations)
4. Database schema (including batches, relationships)
5. Registry APIs (including MetricProfile CRUD)
6. Compatibility Engine
7. UI skeleton
8. Create Run UI (7-step wizard)
9. Compatibility validation
10. RunSpec composer
11. Mock adapter (with cancel() support)
12. Execution gateway
13. Auto-capture
14. Result normalization
15. Result detail UI
16. Report v1
17. Comparison v1
18. DLQ + worker health + zombie detection
19. Security hardening (CSRF, XSS, presigned URLs)
20. Observability + SLO metrics
21. Real external tool adapter
22. Re-run + renormalize workflows
23. Register New Tool wizard
24. Advanced reports
25. Deployment architecture + CI/CD
26. Backup & DR setup
```

---

## 21. Architecture Acceptance Criteria

LabLex architecture is acceptable only if:

```text
1. User can select external tool/target/model/benchmark.
2. User can click Run Evaluation inside LabLex.
3. External execution happens outside LabLex core logic.
4. LabLex captures outputs automatically.
5. Results appear inside LabLex.
6. Raw outputs are stored immutably.
7. Normalized results are generated.
8. Reports are generated from stored data.
9. Comparisons work across multiple runs.
10. No internal benchmark runner exists.
11. No internal scorer exists.
12. No hardcoded product root exists.
13. Manual import exists only as fallback.
14. No Agent/Model/Benchmark/EvalEngine/Tool/Provider is globally required.
15. Required fields are derived from Evaluation Mode + selected manifests.
16. RunSpec Preview shows selected components, derived metadata, compatibility result, schema mappings, and evidence plan before locking.
```

---

## 22. Hard Rejection Checklist

Reject any implementation that adds:

```text
Hermes as default root
Codex as default root
Claude Code as default root
ARC-AGI as built-in internal benchmark
Inspect AI clone
Promptfoo clone
Internal scoring logic
Internal benchmark execution logic
Internal model gateway
Agent orchestration as core
Digital State terminology
Prime/Builder/Auditor terminology in product UI
Global agent_id required for every run
Global model_id required for every run
Global benchmark_id required for every run
EvalEngine selected as an independent runtime
Hidden default model/provider/tool/benchmark
Fixed Agent → Model → Benchmark pipeline as the only Create Run path
Fuzzy adapter matching
Run without compatibility validation
Result display without raw evidence
Report without config snapshot
```

---

## 23. Sources and Standards Consulted

The architecture is aligned with these public technical sources and standards:

- OpenAPI Specification v3.1.1 — standard language-agnostic interface description for HTTP APIs.
- JSON Schema Draft 2020-12 — schema validation for JSON manifests and result contracts.
- FastAPI official documentation — Python API framework based on type hints and compatible with OpenAPI/JSON Schema.
- PostgreSQL documentation — JSON/JSONB storage, indexing, and Row-Level Security.
- Docker documentation — rootless mode and seccomp profiles for safer container execution.
- Temporal documentation — workflow/activity failure handling and retry patterns.
- OpenTelemetry documentation — collector and telemetry architecture.
- GitHub webhook documentation — validating webhook delivery signatures.
- OWASP API Security Project — API security risks and guidance.
- Amazon S3 lifecycle management — object/artifact lifecycle management.

---

## 24. Final Architecture Statement

LabLex must be built as a neutral, component-agnostic, external-first evaluation control plane.

Its product root is not Agent, Model, EvalEngine, Benchmark, Tool, or Provider.

Its product root is:

```text
Registry
→ User Selection
→ Compatibility
→ RunSpec Preview
→ Evidence Plan
→ External Execution
→ Raw Data
→ Normalized Data
→ Comparison
→ Reports
→ Audit
```

Its core is not evaluation logic. Its core is:

```text
registries
manifests
compatibility
runspecs
external execution
automatic result capture
raw evidence
normalized data
comparison
professional reports
audit
observability
```

If the project stays within these boundaries, it will remain clean, extensible, and commercially understandable.

If it starts embedding agents, benchmarks, scorers, or eval engines internally, it will repeat the previous architecture failure.


---

## 25. Normalization Contract

This is the most critical architectural decision after the external-first identity itself.

### 25.1 Core Rule

LabLex must never normalize external tool output through hardcoded per-tool logic inside application code.

Normalization is owned by **ResultSchema manifests**. All mapping rules are declarative and stored as registered artifacts — not embedded in adapter code, not hardcoded in the normalizer engine.

```text
Adapter      = how to invoke the tool and where to find its outputs
ResultSchema = how to transform those outputs into a LabLex NormalizedResult
```

### 25.2 Normalization Flow

```text
External Tool Output
        ↓
Adapter captures raw output → RawResult (immutable)
        ↓
Normalizer reads: RawResult + ResultSchema
        ↓
JSONPath extractions applied per mapping rules
        ↓
Type coercion applied
        ↓
Enum mapping applied
        ↓
Transforms applied (whitelist only)
        ↓
Missing-field policy applied
        ↓
Validation rules applied
        ↓
NormalizedResult stored (with schema_id, schema_version, checksum)
        ↓
normalization_status: completed | normalization_failed | schema_mismatch
```

### 25.3 ResultSchema Manifest

```yaml
kind: result_schema
schema_version: "1.0.0"
id: promptfoo_basic_result_v1
name: Promptfoo Basic Result Schema
raw_format: json

canonical_target: lablex.normalized_result.v1

mappings:
  status:
    source: "$.status"
    type: string
    required: true
    on_missing: fail_normalization
    enum_map:
      success: completed
      failed: failed
      error: failed

  score:
    source: "$.summary.score"
    type: number
    required: true
    on_missing: fail_normalization

  pass_rate:
    source: "$.summary.passRate"
    type: number
    required: false
    on_missing: null
    transform:
      name: percent_to_ratio

  latency_ms:
    source: "$.stats.avgLatencyMs"
    type: number
    required: false
    on_missing: null

  cost_usd:
    source: "$.stats.totalCostUsd"
    type: number
    required: false
    on_missing: 0

  error_count:
    source: "$.summary.failures"
    type: integer
    required: false
    on_missing: 0

  samples:
    source_array: "$.results"
    required: false
    fields:
      sample_id:
        source: "$.id"
        type: string
        required: true
      input_text:
        source: "$.prompt"
        type: string
        required: false
      output_text:
        source: "$.output"
        type: string
        required: false
      score:
        source: "$.score"
        type: number
        required: false
      status:
        source: "$.status"
        type: string
        required: true
        enum_map:
          pass: completed
          fail: failed
      latency_ms:
        source: "$.latency"
        type: integer
        required: false

artifacts:
  report_file:
    source: "$.artifacts.report"
    required: false

validation:
  required_metrics:
    - score
  allowed_statuses:
    - completed
    - failed
    - canceled
```

### 25.4 Extraction Mechanism

Use **JSONPath (RFC 9535)** for all JSON-format tool outputs.

For CSV-format tool outputs, use column name mapping:

```yaml
mappings:
  score:
    source_column: "eval_score"
    type: number
    required: true
    on_missing: fail_normalization
```

### 25.5 Allowed Transforms

```text
percent_to_ratio     — divide by 100
ratio_to_percent     — multiply by 100
ms_to_seconds        — divide by 1000
seconds_to_ms        — multiply by 1000
round(n)             — round to n decimal places
string_to_lower
string_to_upper
```

No custom code. No eval(). No arbitrary scripts. Any required transform not on this list must be proposed as a new named transform and reviewed.

### 25.6 Missing-Field Policies

```text
fail_normalization   — required field absent → normalization fails
null                 — optional field absent → store null
default:<value>      — optional field absent → store default
warn                 — optional field absent → store null + add warning
```

### 25.7 Non-Negotiable Normalization Rules

```text
1. RawResult is immutable. Never modify it after capture.
2. NormalizedResult must always reference RawResult by ID.
3. NormalizedResult must store:
     result_schema_id
     result_schema_version
     adapter_id
     adapter_version
     manifest_checksum
4. Missing required field → normalization_failed status.
5. Missing optional field → null/default/warning per schema definition.
6. All transforms are whitelist-only.
7. No arbitrary Python/JS code inside mapping definitions.
8. Every normalization failure must be visible on Result Detail page.
9. Silent nulls are forbidden.
10. Fuzzy field matching is forbidden.
```

### 25.8 normalization_warnings Field (v1.2 addition)

`NormalizedResult` must include a `normalization_warnings` column (JSONB array) independent from `normalization_status`. Warnings do not fail normalization but must be surfaced in the UI.

```json
"normalization_warnings": [
  {
    "field": "pass_rate",
    "code": "optional_field_missing",
    "detail": "$.summary.passRate not found in raw output. Stored as null."
  },
  {
    "field": "latency_ms",
    "code": "unit_mismatch_suspected",
    "detail": "Value 0.142 may be in seconds, not ms. Verify adapter output."
  }
]
```

`normalization_warnings: []` means clean normalization with no issues.
`normalization_warnings` is never null — always an array (empty or populated).

---

## 26. Worker Isolation Architecture

### 26.1 Core Rule

No single worker handles all execution types. Worker types are separated by adapter category. This is a security and reliability boundary, not an optimization.

### 26.2 Worker Types

```text
http_worker           — runs HTTP adapter calls against external APIs
cli_worker            — runs CLI adapter: local/remote subprocess execution
docker_worker         — runs Docker adapter: isolated container execution
webhook_worker        — receives and processes inbound webhook callbacks
capture_worker        — collects stdout, stderr, result files, artifacts
normalization_worker  — applies ResultSchema mappings to RawResult
report_worker         — generates reports from NormalizedResult
```

### 26.3 Worker Queue Map

```text
queue:http-runs         → http_worker
queue:cli-runs          → cli_worker
queue:docker-runs       → docker_worker
queue:webhooks          → webhook_worker
queue:capture           → capture_worker
queue:normalization     → normalization_worker
queue:reports           → report_worker
```

### 26.4 Run Execution Sequence (as Activities)

Write each step as an isolated, retryable unit — not as sequential monolith code:

```text
1.  validate_runspec
2.  prepare_workspace
3.  resolve_tool_connection
4.  execute_external_tool       ← dispatched to adapter-type queue
5.  monitor_run_status
6.  capture_outputs             ← capture_worker
7.  persist_raw_result          ← immutable write
8.  normalize_result            ← normalization_worker
9.  generate_report             ← report_worker
10. finalize_run
```

Design these steps so they are portable to Temporal Workflows/Activities when Temporal is introduced. Avoid Celery spaghetti that couples steps.

### 26.5 CLI Adapter Isolation Rules

```text
1. Each run gets its own isolated working directory.
   Path: /run-workspaces/{tenant_id}/{run_id}/
2. No shared temp directories between tenants.
3. No shared temp directories between concurrent runs.
4. Secrets are injected as environment variables at runtime only.
5. Secrets must never appear in logs, stdout, or stderr.
6. Allowed output paths are declared in adapter manifest.
7. No writes outside the run workspace.
8. Max stdout size: enforced (e.g. 100MB default).
9. Max artifact size: enforced (e.g. 500MB default).
10. Max runtime: enforced via timeout policy.
```

### 26.6 CLI Timeout Policy

```text
on timeout:
1. send SIGTERM to subprocess
2. wait grace_period_seconds (default: 10s, configurable per adapter)
3. send SIGKILL
4. mark run as timed_out
5. capture partial stdout/stderr if available
6. do NOT normalize unless a valid raw output file exists
7. emit run.timed_out event to SSE stream
```

### 26.7 Docker Adapter Rules (v1.6 update)

```text
1. No Docker Socket Access: CLI and HTTP Workers MUST NOT mount or have access to /var/run/docker.sock to prevent container breakouts.
2. Sandboxed VM Execution: In production, container runs MUST be delegated to isolated serverless container runtimes (such as AWS Fargate, GCP Cloud Run, or Kubernetes Jobs with gVisor sandboxing) rather than running directly on the worker's shared Docker daemon.
3. Explicit Resource Limits: Every adapter manifest running Docker containers MUST declare resource constraints in its schema:
     cpu_limit: "1.0"      (default, configurable)
     memory_limit: "2Gi"   (default, configurable)
4. No volume mounts outside run workspace.
5. Container image must be declared in adapter manifest and versions must be pinned (no latest tag in production).
6. Network: Restrict to allowlisted hosts declared in the manifest (e.g. openai.com, anthropic.com) unless explicitly declared open.
7. Ephemeral Compute: Node instances running containerized adapter tasks must be clean and terminated immediately upon completion of execution.
```

### 26.8 Temporal Migration Path

MVP uses RQ or Celery for task queuing. Write worker steps as self-contained functions with clear input/output contracts. When Temporal is introduced, each step maps to a Temporal Activity. The workflow DAG (steps 1–10 above) maps to a Temporal Workflow definition. No architecture refactor needed if steps are cleanly separated from the beginning.

### 26.9 Dead Letter Queue Strategy (v1.4 addition)

Every queue must have a corresponding DLQ for messages that fail all retries.

```text
DLQ mapping:
  queue:cli-runs        → dlq:cli-runs
  queue:http-runs       → dlq:http-runs
  queue:docker-runs     → dlq:docker-runs
  queue:webhooks        → dlq:webhooks
  queue:capture         → dlq:capture
  queue:normalization   → dlq:normalization
  queue:reports         → dlq:reports

Rules:
  1. After max_retries (per §48.3) → move to DLQ.
  2. Run status transitions to: internal_error (not stuck in running).
  3. DLQ depth is monitored: alert when depth > 0.
  4. Admin endpoints for DLQ management:
       GET  /api/v1/admin/dlq             — list all DLQ messages
       POST /api/v1/admin/dlq/{id}/retry  — retry a DLQ message
       POST /api/v1/admin/dlq/{id}/discard— discard a DLQ message
  5. DLQ messages retain: original message + error trace + retry count + timestamp.
  6. DLQ retention: 30 days.
```

### 26.10 Graceful Worker Shutdown (v1.4 addition)

```text
On deployment or scale-down:
  1. Worker receives SIGTERM.
  2. Worker stops accepting new tasks from queue.
  3. Worker continues processing current task until completion or timeout.
  4. If current task exceeds grace_period (default: max_run_duration + 60s):
       → Force-cancel the running task.
       → Mark run as internal_error with reason: worker_shutdown.
       → Emit audit event.
  5. Worker exits cleanly.

Rules:
  1. Workers must be stateless — no in-memory state between tasks.
  2. Rolling deployments must ensure minimum worker count per queue.
  3. Kubernetes: use preStop hook + terminationGracePeriodSeconds.
  4. Zombie run detection: cron job checks for runs stuck in 'running'
     beyond 2× their timeout → marks as timed_out + alerts.
```

---

## 27. Run Streaming / Real-time Progress

### 27.1 Core Decision

Use **Server-Sent Events (SSE)** for MVP run progress delivery. SSE is a unidirectional HTTP stream from server to browser, sufficient for LabLex's primary need: delivering run lifecycle updates and logs to the UI without requiring client-to-server communication during a run.

WebSocket is not introduced until interactive control of a running tool is required. That is not an MVP use case.

### 27.2 SSE Endpoint

```text
GET /api/v1/runs/{run_id}/events
Content-Type: text/event-stream
Cache-Control: no-cache
Connection: keep-alive
```

Authentication: same JWT/API key as all other endpoints.

### 27.3 Event Types

```text
run.created
run.validated
run.queued
run.running
run.log                   — log line emitted during execution
run.output_detected       — adapter detected a result file
run.capturing_outputs
run.normalizing
run.reporting
run.completed
run.failed
run.timed_out
run.cancelled
```

### 27.4 Event Format

```json
{
  "id": "evt_00421",
  "event": "run.log",
  "run_id": "run_001",
  "timestamp": "2026-06-20T10:34:21Z",
  "data": {
    "line": "[promptfoo] Running test case 12/50"
  }
}
```

### 27.5 SSE Replay / Last-Event-ID (v1.2 addition)

SSE connections can drop. The client must be able to resume without losing events.

Implementation rules:

```text
1. Every event emitted must have a unique sequential id field.
2. Events are persisted in the run_events table as they are emitted.
3. The SSE endpoint accepts a Last-Event-ID header on reconnect.
4. On reconnect, server replays all events after Last-Event-ID.
5. run_events retention: minimum 7 days after run completes.
6. If Last-Event-ID is absent, stream from first event of run.
```

Heartbeat:

```text
Emit a heartbeat comment every 20 seconds on idle connections:
  : heartbeat

This prevents proxy/load-balancer timeout on long-running evaluations.
```

### 27.6 Fallback for Non-SSE Clients

```text
Primary:   SSE via GET /api/v1/runs/{run_id}/events
Fallback:  Polling via GET /api/v1/runs/{run_id} every 3–5 seconds
```

### 27.7 Conditions for WebSocket Introduction

Only introduce WebSocket when:

```text
1. Interactive terminal session to a running CLI tool is needed.
2. Bidirectional agent control during run execution is needed.
3. Live input injection into a running tool session is needed.
```

None of these are MVP scope.

### 27.8 SSE Event Distribution (v1.4 addition)

With multiple API server instances behind a load balancer, SSE events must reach the correct instance.

```text
Architecture:
  1. Workers publish events to Redis Pub/Sub channel: sse:{run_id}
  2. All API instances subscribe to channels for their connected SSE clients.
  3. When an SSE client connects: API subscribes to sse:{run_id}.
  4. When an SSE client disconnects: API unsubscribes.
  5. Events are also persisted to run_events table (for Last-Event-ID replay).

Alternative (post-MVP):
  Use a dedicated message broker (e.g., NATS, Kafka) if Redis Pub/Sub
  becomes a bottleneck at >1000 concurrent SSE connections.
```

---

## 28. Authentication and Tenant Scoping

### 28.1 Authentication Modes

```text
JWT session token  — for UI users authenticating via browser
API key            — for programmatic access, scripts, adapter callbacks
```

JWT tokens are short-lived. API keys are long-lived and must be revocable.

Secrets for external tools (API keys, CLI tokens, connection strings) are **not** API keys. They are stored as secret_refs, not as raw values.

### 28.1a CSRF Protection (v1.4 addition)

```text
1. JWT cookies must set SameSite=Strict.
2. All state-changing requests (POST, PUT, PATCH, DELETE) from browser sessions
   must include X-CSRF-Token header.
3. CSRF token is generated per session and stored server-side.
4. API key requests are exempt from CSRF (no cookie involved).
5. CORS origin validation on all requests with credentials.
```

### 28.1b API Key Rotation (v1.4 addition)

```text
1. User creates new API key (POST /api/v1/api-keys).
2. Old key enters grace period (default: 7 days).
3. During grace period: both old and new keys work.
4. After grace period: old key is automatically revoked.
5. Immediate revocation always available (POST /api/v1/api-keys/{id}/revoke).
6. Audit event on every key creation, deprecation, and revocation.
```

### 28.2 Required Tables

```text
users
  id, email, name, created_at

tenants
  id, name, plan, created_at

memberships
  id, user_id, tenant_id, role, created_at

api_keys
  id, tenant_id, name, key_hash, scope, last_used_at, created_at, revoked_at

secret_refs
  id, tenant_id, name, encrypted_value, key_version, created_at, updated_at
  (stores AES-GCM-256 ciphertext encrypted via KMS tenant DEK)
```

### 28.3 Tenant Scoping Rules

```text
1. Every authenticated request resolves tenant_id from token/key.
2. All registry queries must filter by tenant_id.
3. All run queries must filter by tenant_id.
4. All result and report queries must filter by tenant_id.
5. No cross-tenant reads or writes permitted at any layer.
6. PostgreSQL Row-Level Security (RLS) is a mandatory gate for the SaaS deployment phase (see §43, GATE 22).
```

### 28.4 Audit Actor Fields

Every audit_event row must include:

```text
actor_user_id     — user who triggered the action (null for system events)
actor_api_key_id  — API key used (null for browser sessions)
tenant_id
action
resource_type
resource_id
timestamp
ip_address
```

### 28.5 Secret Reference Model

Authoritative Model:
1. The `secret_refs` table stores the encrypted ciphertext in the database using KMS envelope encryption (AES-256-GCM with tenant DEK + KMS KEK).
2. External Secret Managers (e.g. AWS Secrets Manager or HashiCorp Vault) are supported as optional post-MVP backends only.
3. Plaintext secrets are never stored in the database or configuration files.
4. At execution time, the worker requests the decrypted DEK from the API, decrypts the ciphertext in-memory, injects the plaintext secret into the execution environment, and immediately scrubs it from memory.

---

## 29. Schema Versioning

### 29.1 Core Rule

All manifests carry explicit version fields. Completed runs store snapshots of all manifests used, ensuring reproducibility even when manifests are later updated or deleted.

### 29.2 Manifest Version Fields

Every manifest must include:

```yaml
schema_version: "1.0.0"     # version of the schema/mapping contract
manifest_version: "1.0.0"   # version of this manifest document
adapter_version: "1.0.0"    # for adapter manifests
```

### 29.3 RunSpec Snapshot Rule

When a RunSpec is composed, it must capture immutable snapshots of:

```text
tool_manifest_snapshot       — full JSON of ExternalTool manifest at run time
adapter_manifest_snapshot    — full JSON of Adapter manifest at run time
result_schema_snapshot       — full JSON of ResultSchema manifest at run time
target_manifest_snapshot     — full JSON of Target manifest at run time
model_manifest_snapshot      — full JSON of Model config at run time
```

These snapshots are stored in `runspec_snapshots` and `manifest_snapshots` tables.

### 29.4 Immutability Law

```text
A completed run must remain fully reproducible even if:
- The original manifest is updated to a new version.
- The original manifest is deleted.
- The ResultSchema changes its mapping rules.
- The Adapter changes its output format.

The run's snapshot is the source of truth for that run's configuration.
```

### 29.5 Version Compatibility Matrix

When a user selects components for a new run, LabLex must check:

```text
adapter_version  compatible with  tool_manifest_version
result_schema_version  compatible with  adapter_version
```

Compatibility is declared explicitly in manifests, not inferred from version numbers.

---

## 30. Extended Connection Testing

### 30.1 Core Rule

Every registered component must be individually testable before it is used in a RunSpec. One test endpoint per component type.

### 30.2 Test Endpoints

```text
POST /api/v1/external-tools/{id}/test-connection
     → connects to tool API or verifies CLI availability

POST /api/v1/targets/{id}/test-connection
     → sends a minimal probe request to the target endpoint

POST /api/v1/adapters/{id}/validate
     → validates adapter manifest structure and declared capabilities

POST /api/v1/result-schemas/{id}/validate
     → validates schema mapping syntax and required field coverage

POST /api/v1/runspecs/{id}/validate
     → validates that selected components are mutually compatible and pings endpoints (§8.5)

POST /api/v1/runspecs/{id}/dry-run
     → full pre-flight without executing the external tool
```

### 30.3 Dry-Run Contract

`POST /api/v1/runspecs/{id}/dry-run` must:

```text
1. Verify external-tool connection is reachable.
2. Verify target is reachable.
3. Verify adapter is valid and declared capabilities match tool.
4. Verify result schema is compatible with adapter output format.
5. Verify output capture paths are configured.
6. Verify tenant has permission to use all selected components.
7. NOT execute the external tool.
8. Return a structured validation report:
     checks: [ { name, status: pass|fail|warning, detail } ]
```

### 30.4 Dry-Run Response Example

```json
{
  "runspec_id": "rs_001",
  "dry_run_status": "pass",
  "checks": [
    { "name": "tool_connection", "status": "pass", "detail": "Promptfoo CLI found at /usr/local/bin/promptfoo" },
    { "name": "target_reachable", "status": "pass", "detail": "HTTP 200 from target probe" },
    { "name": "adapter_valid",    "status": "pass", "detail": "CLI adapter manifest schema valid" },
    { "name": "schema_compatible","status": "pass", "detail": "Result schema maps all required fields" },
    { "name": "permissions",      "status": "pass", "detail": "All components owned by tenant" }
  ]
}
```

---

## 31. Comparison Model

### 31.1 Core Rule

Comparisons operate on **NormalizedResult metrics**. RawResult is used for evidence drill-down only — not as the primary comparison data source.

### 31.2 Supported Comparison Types

```text
same_tool_same_benchmark         — compare model A vs model B on same eval
same_benchmark_different_tools   — compare Promptfoo vs InspectAI on same benchmark
same_model_different_benchmarks  — compare model on benchmark A vs benchmark B
same_target_different_versions   — compare run before/after model update
same_runspec_repeated            — variance analysis across identical runs
```

### 31.3 Compatibility Check for Comparison

Before a comparison is created, LabLex must validate:

```text
1. All runs use normalized metrics.
2. Metrics being compared share compatible units.
3. If result schemas differ, a schema_mismatch_warning is emitted.
4. If tools differ, a tool_mismatch_warning is emitted.
5. User must acknowledge warnings before comparison is saved.
```

### 31.4 Comparison Output Model

```json
{
  "comparison_id": "cmp_001",
  "runs": ["run_001", "run_002"],
  "comparison_type": "same_tool_same_benchmark",
  "metric_deltas": {
    "score":      { "run_001": 0.86, "run_002": 0.79, "delta": -0.07, "direction": "higher_is_better", "winner": "run_001" },
    "latency_ms": { "run_001": 1420, "run_002": 980,  "delta": -440,  "direction": "lower_is_better",  "winner": "run_002" },
    "cost_usd":   { "run_001": 0.52, "run_002": 0.31, "delta": -0.21, "direction": "lower_is_better",  "winner": "run_002" },
    "error_count":{ "run_001": 2,    "run_002": 5,    "delta": +3,    "direction": "lower_is_better",  "winner": "run_001" }
  },
  "warnings": [],
  "summary": {
    "overall_winner": "inconclusive",
    "notes": "run_001 scores higher, run_002 has lower latency and cost"
  }
}
```

`winner` is computed from `metric_direction` declared in MetricProfile (see Section 39). If MetricProfile does not declare a direction for a metric, winner is `null` and a `direction_unknown` warning is emitted.

### 31.4a Overall Winner Rules (v1.3 addition)

```text
1. overall_winner is NEVER computed automatically by LabLex.
2. Per-metric winners are computed from MetricProfile direction declarations.
3. overall_winner is always set to "inconclusive" in the comparison data model.
4. If weighted analysis is needed, the user explicitly configures weights.
   LabLex displays a weighted metric table only.
   Any conclusion or recommendation is user-authored in User Notes (no automated narrative or recommendation generation by LabLex).
5. If a user or report template wants weighted ranking, the weights
   must be explicitly configured in the report_template, not assumed.
6. Rationale: different stakeholders value different metrics.
   Declaring an automatic winner would embed a subjective judgment
   into an objective data layer.
```

### 31.5 Comparison UI Minimum Requirements

```text
Comparison Table     — side-by-side metric rows
Delta Column         — absolute and percentage delta per metric
Winner Indicator     — per-metric best value highlighted
Cost/Quality View    — scatter or radar chart
Failure Comparison   — failure reasons per run
Schema Warning Panel — shown if schemas differ
Export Button        — comparison as JSON, CSV, HTML
```

### 31.6 Hard Rules for Comparison

```text
1. Cannot compare runs where normalization_status ≠ completed.
2. Cannot compare runs with incompatible metric units without warning.
3. Comparison result must link to RawResult of each run for drill-down.
4. Comparison must store a snapshot of metric values at creation time.
   (NormalizedResult may be updated; comparison snapshot must not change.)
```

---

## 32. Architecture Patch Acceptance Criteria

The v1.1 patch criteria are acceptable only when all of the following are true:

```text
Normalization:
  ☐ ResultSchema manifest structure is implemented and validated.
  ☐ JSONPath extraction is working on at least one real adapter.
  ☐ normalization_status is tracked per NormalizedResult.
  ☐ Missing required field produces normalization_failed, not silent null.

Worker Isolation:
  ☐ CLI worker is isolated from HTTP worker at queue level.
  ☐ Each run gets its own workspace directory.
  ☐ SIGTERM → grace → SIGKILL timeout policy is implemented.
  ☐ No secrets appear in logs.

Streaming:
  ☐ GET /api/v1/runs/{run_id}/events returns SSE stream.
  ☐ At minimum run.running, run.log, run.completed, run.failed events work.
  ☐ Polling fallback works via GET /api/v1/runs/{run_id}.

Authentication:
  ☐ Every write endpoint requires authenticated actor.
  ☐ Tenant scoping is enforced on all resource queries.
  ☐ Audit events store actor_user_id and tenant_id.

Schema Versioning:
  ☐ All manifests carry schema_version and manifest_version.
  ☐ RunSpec stores snapshots of all selected component manifests.
  ☐ Completed runs remain reproducible after manifest updates.

Connection Testing:
  ☐ All 6 test/validate/dry-run endpoints are implemented.
  ☐ dry-run returns structured check results, not a boolean.

Comparison:
  ☐ Comparison operates on NormalizedResult metrics only.
  ☐ metric_deltas and winner per metric are computed.
  ☐ Schema mismatch warning is emitted when schemas differ.

Object Storage:
  ☐ All paths follow the tenant-scoped convention.
  ☐ No cross-tenant path access is possible.

Source Tracking:
  ☐ Every RawResult has source_type populated.
  ☐ Manual uploads are distinguishable from auto-captured results in audit.
```

---

## 33. Idempotency & Duplicate Run Protection

### 33.1 Core Problem

External execution is expensive and potentially destructive. If a client retries a run creation request due to a network timeout, LabLex must not launch two identical runs.

### 33.2 Idempotency Key

All run-creating and state-changing endpoints must accept an `Idempotency-Key` header:

```text
POST /api/v1/runs
Header: Idempotency-Key: <client-generated UUID>
```

Rules:

```text
1. Idempotency-Key is client-generated (UUID v4 recommended).
2. LabLex stores the key in idempotency_keys table with:
     key, tenant_id, endpoint, request_hash, response_body, created_at, expires_at
3. If same key is received again within TTL (24 hours default):
     return the original response, do NOT create a new run.
4. If key is absent: proceed normally (no idempotency protection).
5. Idempotency keys expire after TTL and are deleted.
6. Key collision across tenants must be impossible:
     unique constraint on (key, tenant_id).
```

### 33.3 Duplicate Run Detection

Separate from idempotency, detect logical duplicates:

```text
A run is a logical duplicate if, within the last N minutes, the same tenant
submitted a run with identical:
  - tool_id
  - target_id
  - model_id
  - benchmark_id
  - runspec_hash (content hash of full RunSpec)
```

On detection:

```text
Return HTTP 409 with:
{
  "error": "duplicate_run_detected",
  "existing_run_id": "run_001",
  "detail": "An identical run was submitted 2 minutes ago."
}
```

User can override by passing `force: true` in the request body. This override must generate an audit event.

### 33.4 Required Table

```text
idempotency_keys
  id, tenant_id, key, endpoint, request_hash,
  response_status, response_body, created_at, expires_at
```

---

## 34. Resource Quotas

### 34.1 Core Rule

No external tool or tenant can exhaust shared infrastructure without limit. Quotas are enforced before a run is queued.

### 34.2 Quota Dimensions

```text
Per-tenant quotas:
  max_concurrent_runs             — total concurrent active runs (default: 5)
  max_concurrent_cli_runs         — concurrent CLI adapter runs (default: 2)
  max_concurrent_docker_runs      — concurrent Docker adapter runs (default: 2)
  max_runs_per_day                — daily run limit (default: 100)
  max_run_duration_seconds        — wall-clock timeout per run (default: 3600)

Per-run limits (enforced by workers):
  max_stdout_bytes                — default: 100MB
  max_stderr_bytes                — default: 10MB
  max_artifact_size_bytes         — default: 500MB
  max_total_artifacts_per_run     — default: 50
  max_log_lines_per_run           — default: 100,000

Per-adapter limits:
  max_cpu_cores                   — for Docker adapter (default: 2)
  max_memory_mb                   — for Docker adapter (default: 2048)
  max_network_requests_per_run    — for HTTP adapter (default: 1000)
```

### 34.3 Quota Enforcement Point

Quotas are checked at `POST /api/v1/runs` before the RunSpec is queued:

```text
1. Resolve tenant quotas.
2. Count current active runs for tenant.
3. If quota exceeded: return HTTP 429 with quota detail.
4. Else: proceed to queue.
```

### 34.3a Atomic Quota Enforcement (v1.4 addition)

```text
Quota check + increment must be atomic to prevent race conditions:

1. Use Redis INCR on quota:{tenant_id}:active_runs.
2. If INCR result > limit: DECR immediately and reject with 429.
3. On run completion: DECR.
4. If Redis unavailable: use PostgreSQL SELECT FOR UPDATE on tenant_quotas row.
5. Never use check-then-increment as two separate operations.
6. Daily run count uses Redis key with TTL = midnight reset.
```

### 34.4 Quota Rejection Response

```json
{
  "error": "quota_exceeded",
  "quota_name": "max_concurrent_runs",
  "current_value": 5,
  "limit": 5,
  "reset_in_seconds": null,
  "detail": "Tenant has reached the maximum concurrent run limit."
}
```

### 34.5 Required Table

```text
tenant_quotas
  id, tenant_id, quota_name, quota_value, override_value,
  created_at, updated_at
```

Default quotas live in config. Per-tenant overrides live in `tenant_quotas` table.

---

## 35. RBAC Permission Matrix

### 35.1 Core Rule

RBAC must be defined before first API endpoint goes live. "We'll add permissions later" is a deployment blocker.

### 35.2 Roles

```text
owner       — full control over tenant, can manage members, billing, deletion
admin       — full control except tenant deletion and billing
evaluator   — can create and run evaluations, manage tools and registries
viewer      — read-only access to runs, results, and reports
api_runner  — programmatic role for API keys: can create and manage runs only
```

### 35.3 Permission Matrix

| Permission                  | owner | admin | evaluator | viewer | api_runner |
|-----------------------------|:-----:|:-----:|:---------:|:------:|:----------:|
| manage_members              |  ✅   |  ✅   |    ❌     |   ❌   |     ❌     |
| manage_secrets              |  ✅   |  ✅   |    ❌     |   ❌   |     ❌     |
| manage_external_tools       |  ✅   |  ✅   |    ✅     |   ❌   |     ❌     |
| manage_registries           |  ✅   |  ✅   |    ✅     |   ❌   |     ❌     |
| create_runs                 |  ✅   |  ✅   |    ✅     |   ❌   |     ✅     |
| cancel_runs                 |  ✅   |  ✅   |    ✅     |   ❌   |     ✅     |
| view_runs                   |  ✅   |  ✅   |    ✅     |   ✅   |     ✅     |
| view_results                |  ✅   |  ✅   |    ✅     |   ✅   |     ✅     |
| view_raw_results            |  ✅   |  ✅   |    ✅     |   ✅   |     ❌     |
| create_comparisons          |  ✅   |  ✅   |    ✅     |   ❌   |     ❌     |
| view_comparisons            |  ✅   |  ✅   |    ✅     |   ✅   |     ❌     |
| create_reports              |  ✅   |  ✅   |    ✅     |   ❌   |     ❌     |
| export_reports              |  ✅   |  ✅   |    ✅     |   ✅   |     ❌     |
| view_audit_log              |  ✅   |  ✅   |    ❌     |   ❌   |     ❌     |
| manage_api_keys             |  ✅   |  ✅   |    ❌     |   ❌   |     ❌     |
| manage_quotas               |  ✅   |  ❌   |    ❌     |   ❌   |     ❌     |
| delete_tenant               |  ✅   |  ❌   |    ❌     |   ❌   |     ❌     |

### 35.4 Enforcement Rule

Every API endpoint that performs a write or sensitive read must check the calling actor's role against the permission matrix before executing. Failure = HTTP 403 with:

```json
{
  "error": "permission_denied",
  "required_permission": "manage_secrets",
  "actor_role": "evaluator"
}
```

---

## 36. Webhook Callback Contract

### 36.1 Core Problem

Some external tools do not wait for LabLex to poll them — they push results back via webhook. This must be handled securely and explicitly.

### 36.2 Inbound Webhook Endpoint

```text
POST /api/v1/webhooks/{webhook_token}
```

`webhook_token` is a cryptographically random opaque token (minimum 32 characters)
generated per ToolConnection. This prevents URL guessing attacks. The token is
stored in the `tool_connections` table alongside the webhook_secret.

### 36.3 Required Headers from Sender

```text
X-LabLex-Signature: sha256=<hmac_signature>
X-LabLex-Timestamp: <unix_timestamp>
X-LabLex-Event: <event_type>
X-LabLex-Idempotency-Key: <sender_generated_key>
Content-Type: application/json
```

### 36.4 Signature Verification

```text
1. Compute HMAC-SHA256 of (timestamp + "." + raw_request_body)
   using the webhook_secret stored in the ToolConnection.
2. Compare computed signature to X-LabLex-Signature header.
3. If mismatch: return HTTP 401, log security event, do NOT process.
4. If timestamp is older than 5 minutes: return HTTP 400 (replay protection).
5. If X-LabLex-Idempotency-Key was already processed: return HTTP 200
   (idempotent — success, but do not reprocess).
```

### 36.5 Payload Size Limit

```text
Max webhook payload: 10MB.
Larger payloads must be rejected with HTTP 413.
External tool must use file reference (object_url) for large outputs.
```

### 36.6 Event Type Allowlist

Only these event types are accepted from external tools:

```text
tool.run.completed
tool.run.failed
tool.run.progress
tool.result.ready
```

Unknown event types are logged and discarded. Never auto-processed.

### 36.7 Webhook Processing Flow (v1.6 update)

```text
1. Fast-Path Token Resolution & Validation:
   - Identify the webhook_token from the incoming URL callback: /api/v1/webhooks/{webhook_token}.
   - Query Redis Cache (TTL: 24h) first to resolve the metadata:
       Key: webhook:token:{webhook_token}
       Value: { "tenant_id": "...", "tool_connection_id": "...", "webhook_secret": "..." }
   - If Redis miss: Query PostgreSQL to fetch details and populate the Redis cache.
2. Validate Signature: Calculate HMAC-SHA256 of the payload using the resolved webhook_secret and compare it to the X-LabLex-Signature header.
3. Check Replay Protection: Validate timestamp and webhook idempotency key in Redis.
4. Route to Queue: Push payload to webhook_worker queue immediately.
5. Return HTTP 202 Accepted: Return immediately to prevent holding connection pools open during long processing.
6. webhook_worker processing:
     - Identify run from tool_connection_id + payload.
     - Extract result reference or inline data.
     - Trigger capture_worker.
     - Continue normal run lifecycle.
```

---

## 37. Logging Architecture (v1.3 addition)

### 37.1 Core Rule

LabLex must have a structured, queryable logging system separate from external tool logs. LabLex internal logs are operational diagnostics. External tool logs are run artifacts.

### 37.2 Log Categories

```text
application_log      — LabLex internal application events (API requests, errors, warnings)
audit_log            — who did what, when (stored in audit_events table, Section 28)
run_log              — external tool stdout/stderr captured during execution (stored as artifacts)
adapter_log          — adapter-level diagnostics: connection attempts, retries, timeouts
worker_log           — worker lifecycle: task pickup, execution, completion, failure
```

### 37.3 Structured Log Format

All internal logs (application, adapter, worker) must be structured JSON:

```json
{
  "timestamp": "2026-06-20T10:34:21.123Z",
  "level": "ERROR",
  "logger": "lablex.adapter.cli",
  "message": "CLI adapter timeout after 3600s",
  "tenant_id": "tenant_001",
  "run_id": "run_001",
  "adapter_id": "cli_json_capture_v1",
  "trace_id": "trace_abc123",
  "span_id": "span_def456",
  "error_code": "ADAPTER_TIMEOUT",
  "extra": {
    "timeout_seconds": 3600,
    "partial_output_captured": true
  }
}
```

### 37.4 Log Levels

```text
DEBUG    — development only, never in production default
INFO     — normal operations: run started, run completed, manifest registered
WARNING  — recoverable issues: normalization warning, retry attempted, deprecated manifest used
ERROR    — failures: adapter error, normalization failed, connection test failed
CRITICAL — system-level failures: worker crash, database unreachable, storage unavailable
```

### 37.5 Sensitive Data Rules

```text
1. NEVER log secret values, API keys, tokens, or credentials.
2. NEVER log full request/response bodies containing user data.
3. Log secret_ref IDs only, never resolved values.
4. Mask any field matching patterns: *_key, *_secret, *_token, *_password.
5. Run stdout/stderr may contain secrets from external tools —
   these are stored as artifacts with access control, NOT in application logs.
```

### 37.6 Log Correlation

```text
1. Every API request gets a unique request_id (UUID v4).
2. request_id is returned in response header: X-Request-ID.
3. request_id propagates to all downstream workers and adapters.
4. OpenTelemetry trace_id and span_id are included in every log line.
5. run_id is included in all logs related to a run execution.
6. tenant_id is included in all logs for tenant-scoped operations.
```

### 37.7 Log Retention

```text
application_log: 30 days (configurable)
adapter_log:     30 days
worker_log:      30 days
audit_log:       2 years minimum (per Section 38)
run_log:         follows artifact retention policy (per Section 38)
```

---

## 38. Artifact & Data Retention Policy

### 38.1 Core Rule

LabLex must define what it keeps, for how long, and what happens when data expires. No retention policy = unbounded storage cost and compliance risk.

### 38.2 Retention Tiers

```text
run_events (SSE events):
  Retention: 7 days after run completes.
  Action on expiry: delete from run_events table.

raw_results (object storage files):
  Default retention: 90 days.
  Configurable per tenant: 30 / 90 / 180 / 365 days.
  Action on expiry: delete from object storage + mark raw_result as expired.

normalized_results (PostgreSQL rows):
  Default retention: 365 days.
  Configurable per tenant.
  Note: normalized_results can outlive raw_results (metrics stay, raw evidence expires).

logs (object storage):
  Default retention: 30 days.
  Configurable per tenant.

trace files:
  Default retention: 30 days.

artifacts (general):
  Default retention: 90 days.

reports and exports:
  Default retention: 365 days.

audit_events:
  Minimum retention: 2 years. Not configurable downward.
```

### 38.3 Expiry Behavior

```text
1. Expired objects are deleted from object storage.
2. The PostgreSQL row is NOT deleted — it is marked: storage_status: expired.
3. The UI shows "Raw output expired" on Result Detail page.
4. Normalized result and metrics remain visible and usable for comparison.
5. Tenant can configure a longer retention period (within plan limits).
6. Tenant can explicitly delete a run before retention period ends.
```

### 38.4 Required Columns (v1.2 additions to existing tables)

```text
raw_results:
  storage_status: active | expired | deleted
  expires_at

artifacts:
  storage_status: active | expired | deleted
  expires_at

reports:
  storage_status: active | expired | deleted
  expires_at
```

### 38.5 Retention Config Table

```text
tenant_retention_config
  id, tenant_id, resource_type, retention_days, created_at, updated_at
```

---

## 39. Metric Direction Rules

### 39.1 Core Problem

Comparison winner calculation is incorrect without knowing whether higher or lower is better for each metric. A "winner" label on latency_ms requires knowing that lower is better.

### 39.2 Direction Values

```text
higher_is_better   — score, accuracy, pass_rate, throughput
lower_is_better    — latency_ms, cost_usd, error_count, failure_count, p99_latency
neutral            — run_id, timestamp, tool_version (not comparable)
```

### 39.3 MetricProfile Manifest (updated)

```yaml
kind: metric_profile
id: standard_eval_metrics_v1
name: Standard Eval Metrics

metrics:
  score:
    type: number
    unit: ratio
    direction: higher_is_better
    display_format: "%.2f"

  accuracy:
    type: number
    unit: ratio
    direction: higher_is_better
    display_format: "%.2f"

  pass_rate:
    type: number
    unit: percent
    direction: higher_is_better
    display_format: "%.1f%%"

  latency_ms:
    type: number
    unit: milliseconds
    direction: lower_is_better
    display_format: "%.0f ms"

  cost_usd:
    type: number
    unit: usd
    direction: lower_is_better
    display_format: "$%.4f"

  error_count:
    type: integer
    unit: count
    direction: lower_is_better
    display_format: "%d"
```

### 39.4 Winner Calculation Rules

```text
1. For each metric in comparison, resolve direction from MetricProfile.
2. If direction is higher_is_better: winner = run with higher value.
3. If direction is lower_is_better: winner = run with lower value.
4. If direction is neutral or unknown: winner = null.
5. If values are equal: winner = "tie".
6. If metric direction is missing from MetricProfile:
     emit direction_unknown warning.
     set winner = null.
     do NOT guess.
```

### 39.5 Hard Rule

No comparison winner is ever computed without an explicit `direction` declaration in the MetricProfile. Guessing direction based on metric name is forbidden.

---

## 40. Manifest Deprecation Policy

### 40.1 Core Problem

Registry accumulates manifests over time. Old ResultSchemas, old Adapters, and old Benchmarks will coexist with new ones. Without a deprecation model, the registry becomes a graveyard that silently accepts broken selections.

### 40.2 Deprecation Fields (added to all manifests)

```yaml
deprecated: false
deprecated_at: null
replaced_by: null           # id of the replacement manifest
migration_notes: null       # human-readable migration instruction
```

### 40.3 Deprecation States

```text
active        — manifest is current, safe to use
deprecated    — manifest is still functional but should not be used for new runs
              — UI shows a deprecation warning in Create Run flow
retired       — manifest is disabled, cannot be selected for new runs
              — existing RunSpecs that use it can still be read (snapshot preservation)
              — new RunSpec creation with this manifest fails
deleted       — manifest record is soft-deleted, only visible in audit history
```

### 40.4 Compatibility Preservation Rule

```text
A completed run's snapshot must remain readable and its result must remain
reproducible regardless of the deprecation or retirement state of the
manifests it used.

The run_manifest_snapshot is immutable. Deprecation of a manifest
does not invalidate existing run snapshots.
```

### 40.5 Deprecation Workflow

```text
1. Mark manifest as deprecated: deprecated=true, deprecated_at, replaced_by, migration_notes.
2. UI shows warning in Create Run when deprecated manifest is selected.
3. User can still proceed (with confirmation).
4. After grace period (e.g. 30 days), mark as retired.
5. Retired manifests cannot be selected for new runs.
6. After longer period (e.g. 90 days), soft-delete.
7. Snapshot preservation is independent and never affected.
```

---

## 41. Report Provenance & Hash

### 41.1 Core Problem

A Report is a professional artifact that may be shared, exported, or submitted as evidence. Its content must be traceable to the exact run data that produced it, and it must be detectable if tampered with.

### 41.2 Report Provenance Fields

Every Report row must include:

```text
generated_at          — timestamp of generation
generated_by_user_id  — user who triggered generation (null if automated)
source_run_ids        — array of run_ids used as input
source_comparison_id  — comparison_id if comparison report (else null)
normalized_result_ids — array of NormalizedResult IDs used
report_template_id    — template used
report_template_version
report_content_hash   — SHA-256 of the full report content at generation time
report_schema_version — version of the report data structure
```

### 41.3 Report Content Hash

```text
1. After report content is generated and stored, compute SHA-256 of the content.
2. Store as report_content_hash on the Report row.
3. On export, recompute hash and compare to stored hash.
4. If hash mismatch: reject export with:
     { "error": "report_integrity_failure",
       "detail": "Report content does not match stored hash." }
5. Export response headers must include:
     X-LabLex-Report-Hash: sha256=<hash>
```

### 41.4 Regeneration Rule

If a report is regenerated (e.g. template update), it must be stored as a **new report record**, not overwriting the original. The original report with its original hash is preserved in the audit trail.

```text
Report regeneration creates a new Report row.
Original Report row: status = superseded.
Audit event: report.regenerated with old_report_id and new_report_id.
```

---

## 42. v1.6.3 Full Architecture Acceptance Criteria

The v1.6.3 architecture is APPROVED only when all of the following are true:

### v1.1 Criteria (carry-forward)

```text
Normalization:
  ☑ ResultSchema manifest structure implemented and validated.
  ☑ JSONPath extraction working on at least one real adapter.
  ☑ normalization_status tracked per NormalizedResult.
  ☑ Missing required field → normalization_failed, not silent null.

Worker Isolation:
  ☑ CLI worker isolated from HTTP worker at queue level.
  ☑ Each run gets its own workspace directory.
  ☑ SIGTERM → grace → SIGKILL timeout policy implemented.
  ☑ No secrets appear in logs.

Streaming:
  ☑ GET /api/v1/runs/{run_id}/events returns SSE stream.
  ☑ run.running, run.log, run.completed, run.failed events work.
  ☑ Polling fallback works via GET /api/v1/runs/{run_id}.

Authentication:
  ☑ Every write endpoint requires authenticated actor.
  ☑ Tenant scoping enforced on all resource queries.
  ☑ Audit events store actor_user_id and tenant_id.

Schema Versioning:
  ☑ All manifests carry schema_version and manifest_version.
  ☑ RunSpec stores snapshots of all selected component manifests.
  ☑ Completed runs remain reproducible after manifest updates.

Connection Testing:
  ☑ All 6 test/validate/dry-run endpoints implemented.
  ☑ dry-run returns structured check results.

Comparison:
  ☑ Comparison operates on NormalizedResult metrics only.
  ☑ metric_deltas and winner per metric computed.
  ☑ Schema mismatch warning emitted when schemas differ.

Object Storage:
  ☑ All paths follow tenant-scoped convention.
  ☑ No cross-tenant path access possible.

Source Tracking:
  ☑ Every RawResult has source_type populated.
  ☑ Manual uploads distinguishable from auto-captured in audit.
```

### v1.2 New Criteria

```text
Idempotency:
  ☐ Idempotency-Key header accepted on POST /api/v1/runs.
  ☐ Duplicate key within TTL returns original response, no new run created.
  ☐ Logical duplicate detection returns HTTP 409 with existing run_id.
  ☐ force: true override creates audit event.

Resource Quotas:
  ☐ max_concurrent_runs enforced before run is queued.
  ☐ max_run_duration_seconds enforced by worker.
  ☐ max_stdout_bytes enforced by capture_worker.
  ☐ HTTP 429 returned on quota breach with quota detail.

RBAC:
  ☐ All 5 roles implemented (owner, admin, evaluator, viewer, api_runner).
  ☐ Permission check on every write endpoint.
  ☐ HTTP 403 returned with required_permission and actor_role.

Webhooks:
  ☐ POST /api/v1/webhooks/{webhook_token} endpoint exists (opaque token, not guessable IDs).
  ☐ HMAC-SHA256 signature verified before processing.
  ☐ Timestamp replay protection (5 minute window) enforced.
  ☐ Idempotency check on X-LabLex-Idempotency-Key.
  ☐ Max payload 10MB enforced.

SSE Replay:
  ☐ Every SSE event has sequential id field.
  ☐ Last-Event-ID reconnect replays events from run_events table.
  ☐ Heartbeat comment emitted every 20 seconds on idle connections.

Retention:
  ☐ retention policy defined per resource type.
  ☐ storage_status column (active | expired | deleted) on raw_results.
  ☐ Expired raw_results: file deleted, row marked expired (not deleted).
  ☐ audit_events retention minimum 2 years enforced.

Metric Direction:
  ☐ MetricProfile manifests include direction field for every metric.
  ☐ Comparison winner computed from declared direction, not guessed.
  ☐ Missing direction → winner: null + direction_unknown warning.

Deprecation:
  ☐ All manifests support deprecated, deprecated_at, replaced_by fields.
  ☐ UI shows deprecation warning when deprecated manifest selected.
  ☐ Retired manifests cannot be selected for new runs.
  ☐ Completed run snapshots unaffected by deprecation state.

Report Provenance:
  ☐ report_content_hash stored on every Report.
  ☐ Hash recomputed and verified on export.
  ☐ Integrity failure rejects export with error.
  ☐ Report regeneration creates new row, original preserved.

Normalization Warnings:
  ☐ normalization_warnings JSONB array stored on NormalizedResult.
  ☐ Warnings surfaced in UI on Result Detail page.
  ☐ normalization_warnings is always array, never null.

Observability SLOs:
  ☐ run_success_rate metric tracked and alerted.
  ☐ p95_run_duration tracked per adapter type.
  ☐ tenant_quota_rejection_rate tracked.
  ☐ Alert thresholds configured before first production run.
```

### v1.3 New Criteria

```text
Unified Error Model:
  ☐ All API endpoints return consistent error response format.
  ☐ Every error includes error_code, message, request_id, retryable flag.
  ☐ Error categories cover: validation, auth, permission, conflict, quota, adapter, timeout, internal.

API Pagination:
  ☐ All list endpoints support ?page, ?page_size, ?sort_by, ?order.
  ☐ Response envelope includes pagination metadata (total_count, has_next).
  ☐ No unbounded SELECT * in any list endpoint.
  ☐ Max page_size enforced at 100.

API Versioning:
  ☐ All endpoints prefixed with /api/v1/.
  ☐ Breaking change policy documented and enforced.

API Rate Limiting:
  ☐ Redis-based sliding window rate limiting active.
  ☐ HTTP 429 returned with Retry-After header on breach.
  ☐ Rate limits applied per API key and per user session.

Batch Operations:
  ☐ POST /api/v1/runs/batch creates multiple runs.
  ☐ Batch status queryable via GET /api/v1/batches/{batch_id}.
  ☐ Partial batch failure does not cancel remaining runs.

Adapter Interface:
  ☐ All adapters implement the AdapterExecutionContext → AdapterResult interface.
  ☐ Adapter code does not access LabLex database directly.
  ☐ Mock Adapter validates the interface contract.

Database Indexes:
  ☐ All tables have indexes for their primary query patterns.
  ☐ EXPLAIN ANALYZE run on all list queries.
  ☐ Indexes are part of Alembic migrations.

Caching:
  ☐ Redis cache active for manifest lookups and quota counters.
  ☐ HTTP cache headers (ETag, Cache-Control) on appropriate GET endpoints.
  ☐ Cache invalidation works on manifest and report updates.

Logging:
  ☐ All internal logs are structured JSON.
  ☐ request_id propagates through all layers.
  ☐ No secrets appear in any log output.
  ☐ Log correlation with OpenTelemetry trace_id.

Local Development:
  ☐ docker-compose up starts full local environment.
  ☐ Seed data creates default tenant + admin user.
  ☐ .env.example documents all required variables.
  ☐ make setup or equivalent one-command bootstrap works.

Testing:
  ☐ Unit tests cover normalization engine, compatibility validator, quota enforcement, RBAC.
  ☐ Integration tests cover full run pipeline with Mock Adapter.
  ☐ Tenant isolation tests verify cross-tenant data is inaccessible.
  ☐ Contract tests validate API responses against OpenAPI spec.

Resilience:
  ☐ Circuit breaker implemented per external tool.
  ☐ Retry policies defined per adapter type.
  ☐ Graceful degradation on Redis unavailability.

Notifications:
  ☐ In-app notifications for run.completed and run.failed.
  ☐ Notification system does not block run execution.

EvalEngine:
  ☐ EvalEngine entity is metadata-only (no execution logic).
  ☐ EvalEngine is not independently selectable in Create Run flow.

Dashboard:
  ☐ Dashboard shows Active Runs, Success Rate, Recent Runs, Quota Usage.
  ☐ Dashboard loads in under 2 seconds.
  ☐ Empty state shows onboarding guidance.

Comparison Winner:
  ☐ overall_winner is always "inconclusive" in data model.
  ☐ Per-metric winners computed from MetricProfile direction only.
```

### v1.4 New Criteria

```text
CSRF Protection:
  ☐ All state-changing endpoints (POST/PUT/DELETE) enforce CSRF tokens.
  ☐ Secure SameSite=Lax/Strict cookie handling.

Resilience Improvements:
  ☐ Dead Letter Queue (DLQ) for failed worker jobs.
  ☐ Graceful shutdown of workers on sigterm/sigkill events.
  ☐ Zero-downtime deployment strategy validated in staging.

Security Hardening:
  ☐ Presigned S3 URLs for all artifact downloads/uploads.
  ☐ XSS protection via strict Content-Security-Policy (CSP).

Infrastructure:
  ☐ PostgreSQL backup/restore procedures verified.
  ☐ S3 bucket versioning/retention policies set.

Cancellation:
  ☐ POST /api/v1/runs/{id}/cancel endpoint.
  ☐ Cancellation signal propagation to adapter and capture engine.

Compatibility:
  ☐ Declaration-based validation prevents invalid RunSpec creation.
```

### v1.6.1 New Criteria (v1.6.1 addition)

```text
Artifact Scanning:
  ☐ Ephemeral workers execute anti-malware/sanitization checks on all raw results and files before storing them in S3.
  ☐ Admin interface for quarantining contaminated artifacts.

Row-Level Security (RLS):
  ☐ Row-Level Security active in PostgreSQL on all tenant-owned tables (runs, results, manifests, api_keys).
  ☐ RLS policy checks tenant_id matches the current authenticated session.
```

### v1.6.3 New Criteria (Component-Agnostic Selection)

```text
Component-Agnostic Selection:
  ☐ No Agent, Model, Benchmark, EvalEngine, Tool, or Provider is globally required.
  ☐ Create Run starts with Evaluation Mode, not a fixed Agent → Model → Benchmark pipeline.
  ☐ Required fields are derived from selected manifests and compatibility rules.
  ☐ UI explains why each field is required.
  ☐ RunSpec Preview displays selected components, derived metadata, manifest versions, schema mappings, compatibility result, warnings, and evidence plan.
  ☐ EvalEngine remains metadata derived from ExternalTool and is not selectable as an independent runtime.
  ☐ Manual import flow supports optional Agent/Model/Benchmark metadata without forcing it.
```

---

## 43. Final Production Gate

LabLex is ready for first real external tool execution when:

```text
GATE 1  — Architecture:    v1.6.3 acceptance criteria complete (Section 42)
GATE 2  — Normalization:   ResultSchema validated with one real tool output
GATE 3  — Security:        Worker isolation + CSRF + XSS + presigned URL enforcement
GATE 4  — Quotas:          Atomic enforcement with Redis INCR
GATE 5  — Auth:            JWT auth + RBAC + CSRF live on all endpoints
GATE 6  — Idempotency:     POST /api/v1/runs idempotency tested
GATE 7  — Dry-run:         POST /api/v1/runspecs/{id}/dry-run returns structured report
GATE 8  — Observability:   OTel instrumentation + SLO metrics + zombie detection
GATE 9  — Error Model:     All endpoints return unified error responses
GATE 10 — Local Dev:       docker-compose up → full environment running
GATE 11 — Testing:         Unit + integration + tenant isolation + cancel + DLQ tests pass
GATE 12 — Resilience:      Circuit breaker + DLQ + graceful shutdown tested
GATE 13 — Deployment:      Zero-downtime deploy tested in staging
GATE 14 — Backup:          PostgreSQL + S3 backup/restore verified
GATE 15 — Cancellation:    POST /api/v1/runs/{id}/cancel propagates to adapter
GATE 16 — Compatibility:   Declaration-based validation prevents invalid RunSpecs
GATE 17 — RunSpec:         Lifecycle enforcement (locked = immutable) verified
GATE 18 — Schemas:         JSON Schema validation active for all manifest kinds
GATE 19 — Cryptography:    KMS envelope encryption active; secret values encrypted at rest
GATE 20 — Sample Normal:   Detailed test case normalization (normalized_samples) verified in dry-runs
GATE 21 — Scanning:      Artifact scanning active for all captured files (anti-malware & sanitization)
GATE 22 — Row-Level:    PostgreSQL Row-Level Security (RLS) active and verified on all tenant-owned tables
```

No external tool execution proceeds until all 22 gates are green.

---

## 44. Unified Error Model (v1.3 addition)

### 44.1 Core Rule

Every API endpoint must return errors in a consistent, machine-readable format. No endpoint may invent its own error shape.

### 44.2 Error Response Structure

```json
{
  "error_code": "QUOTA_EXCEEDED",
  "error_type": "quota",
  "message": "Tenant has reached maximum concurrent run limit.",
  "details": {
    "quota_name": "max_concurrent_runs",
    "current_value": 5,
    "limit": 5
  },
  "request_id": "req_abc123",
  "trace_id": "trace_xyz",
  "timestamp": "2026-06-20T10:34:21Z",
  "retryable": false,
  "retry_after_seconds": null
}
```

### 44.3 Error Categories

| Category | HTTP Status | error_type | When |
|---|:---:|---|---|
| Bad Input | 400 | validation_error | Invalid request body, missing required field |
| Not Authenticated | 401 | authentication_error | Missing or invalid token/API key |
| No Permission | 403 | permission_error | Role lacks required permission |
| Not Found | 404 | not_found | Resource does not exist or not in tenant scope |
| Conflict | 409 | conflict | Duplicate run, idempotency collision |
| Rate Limited | 429 | rate_limit_error | API rate limit exceeded |
| Quota Exceeded | 429 | quota_error | Tenant quota exceeded |
| External Failure | 502 | adapter_error | External tool returned error or unreachable |
| Timeout | 504 | timeout_error | External tool execution timed out |
| Internal Error | 500 | internal_error | Unexpected server error |

### 44.4 Error Response Rules

```text
1. error_code is machine-readable, UPPER_SNAKE_CASE, and stable across versions.
2. message is human-readable and may change across versions.
3. details is optional structured context (never null — use empty object {}).
4. request_id is always present and matches X-Request-ID response header.
5. trace_id is present when OpenTelemetry is active.
6. retryable indicates whether the client should retry the request.
7. retry_after_seconds is present only when retryable is true.
8. 500 errors must never expose stack traces or internal implementation details.
9. Validation errors (400) must include field-level detail:
   {
     "error_code": "VALIDATION_FAILED",
     "details": {
       "fields": [
         { "field": "tool_id", "error": "required", "message": "tool_id is required" },
         { "field": "timeout", "error": "range", "message": "must be between 1 and 86400" }
       ]
     }
   }
```

---

## 45. Testing Architecture (v1.3 addition)

### 45.1 Core Rule

No feature ships without automated tests. Testing is not a phase — it is a continuous gate.

### 45.2 Test Layers

```text
Unit Tests (pytest):
  — Normalization engine with fixture raw outputs (JSON + CSV)
  — Compatibility validator with known-good and known-bad combinations
  — Quota enforcement logic
  — RBAC permission checks for all role × permission combinations
  — Idempotency key logic
  — Duplicate run detection
  — Metric direction and winner calculation
  — Error response formatting
  — Manifest validation against JSON Schema

Integration Tests (pytest + test database):
  — Mock Adapter → Capture → Normalize → Report full pipeline
  — SSE event delivery and Last-Event-ID replay
  — Webhook signature verification and processing
  — Batch run creation and status tracking
  — Pagination, filtering, sorting on all list endpoints
  — Cache invalidation on manifest update
  — Retention policy enforcement

Tenant Isolation Tests:
  — Tenant A creates resources → Tenant B cannot see/access them
  — Cross-tenant access returns 404 (not 403 — do not reveal existence)
  — Object storage paths are tenant-scoped
  — Audit events are tenant-scoped

Contract Tests:
  — API responses validated against OpenAPI spec (schemathesis or equivalent)
  — ResultSchema manifest validated against JSON Schema
  — Adapter manifest validated against JSON Schema
  — Error responses follow Section 44 format

E2E Tests (Playwright):
  — Create Run → Mock Execution → Result Display
  — Comparison flow: select runs → compare → view deltas
  — Report generation → export as HTML
  — Dashboard loads with data
  — Empty state shows onboarding guidance

Cancellation Tests (v1.5 addition):
  — POST /api/v1/runs/{id}/cancel → adapter cancel() called
  — CLI adapter: SIGTERM sent to external process
  — Cancelled run status = cancelled, partial results captured
  — Cancel on completed run → 409 Conflict

Dead Letter Queue Tests (v1.5 addition):
  — Poison message (malformed RunSpec) → moves to DLQ after max_retries
  — Run status transitions to internal_error (not stuck in running)
  — DLQ admin endpoint lists failed messages
  — DLQ retry re-enqueues message

Renormalize Tests (v1.5 addition):
  — POST /api/v1/results/{run_id}/renormalize creates new NormalizedResult
  — Original NormalizedResult status → superseded
  — Expired RawResult → 410 Gone
  — Comparisons referencing original are unaffected

RunSpec Lifecycle Tests (v1.5 addition):
  — RunSpec in locked state → PUT returns 409
  — POST /api/v1/runs with draft RunSpec → 400
  — POST /api/v1/runs with locked RunSpec → success
  — DB trigger prevents UPDATE on locked RunSpec
```

### 45.3 Test Infrastructure

```text
1. Mock Adapter: built-in adapter that generates synthetic results.
   Supports configurable: success/failure, metric ranges, latency simulation.
   IMPORTANT: Mock Adapter is a test harness, NOT an internal eval engine.
   It exists solely to validate the capture → normalize → report pipeline
   without requiring a real external tool. It must never ship as a
   production evaluation capability.
2. Test fixtures: sample raw outputs from Promptfoo, Inspect AI (anonymized).
3. docker-compose.test.yml: isolated test environment (separate DB, Redis, MinIO).
4. Factory functions: create_tenant(), create_run(), create_manifest() helpers.
5. Tenant isolation helper: run_as_tenant(tenant_id) context manager.
```

### 45.4 Coverage Requirements

```text
1. Minimum 80% line coverage on core modules:
   normalization, compatibility, execution_gateway, quota, rbac.
2. 100% coverage on security-critical paths:
   authentication, authorization, tenant scoping, secret handling.
3. Coverage reports generated on every CI run.
4. Coverage regression (drop > 2%) blocks merge.
```

---

## 46. Caching Architecture (v1.3 addition)

### 46.1 Core Rule

Caching is a performance optimization, not a correctness mechanism. The system must function correctly with an empty or unavailable cache.

### 46.2 Cache Layer 1 — Application Cache (Redis)

```text
Manifest lookups:
  Key: manifest:{tenant_id}:{kind}:{id}
  TTL: 5 minutes
  Invalidation: on manifest update or deletion

Compatibility matrix results:
  Key: compat:{tenant_id}:{hash_of_component_ids}
  TTL: 5 minutes
  Invalidation: on any referenced manifest update

Tenant quota counters:
  Key: quota:{tenant_id}:active_runs
  TTL: none (real-time atomic increment/decrement)
  Invalidation: on run start and run completion

Active run count per tenant:
  Key: runs:active:{tenant_id}
  TTL: 30 seconds
  Invalidation: on run state change

Session data:
  Key: session:{session_id}
  TTL: matches JWT expiry
```

### 46.3 Cache Layer 2 — HTTP Cache Headers

```text
GET /api/v1/reports/{id}:
  ETag: sha256 of report content
  Cache-Control: private, no-cache
  → Client sends If-None-Match, server returns 304 if unchanged

GET /api/v1/results/{run_id}/normalized:
  Cache-Control: private, max-age=300
  → Result is immutable after normalization, safe to cache

GET /api/v1/manifests/{id}:
  Cache-Control: private, max-age=60
  ETag: manifest content hash

Static assets (UI):
  Cache-Control: public, max-age=86400, immutable
```

### 46.4 Cache Invalidation Rules

```text
1. Manifest update → invalidate manifest cache + compatibility cache
2. Run completion → decrement active run count
3. Report regeneration → invalidate report cache + update ETag
4. Tenant quota change → invalidate quota cache
5. User role change → invalidate session cache for affected user
```

### 46.5 What NOT to Cache

```text
1. SSE streams (real-time, never cached)
2. Raw results (served from object storage with presigned URLs)
3. Audit events (append-only, always fresh)
4. Run state during execution (must be real-time)
5. Authentication tokens (validated on every request)
```

### 46.6 Redis Unavailability Fallback

```text
1. Quota checks: fallback to direct DB COUNT query (slower, acceptable).
2. Manifest lookups: fallback to direct DB query.
3. Rate limiting: fallback to in-memory sliding window (per-process, less accurate).
4. Session validation: JWT is self-contained, no Redis dependency.
5. Log WARNING when Redis is unavailable, do NOT fail requests.
```

### 46.7 Redis High Availability (v1.4 addition)

```text
Development:
  Single Redis instance (docker-compose).

Production:
  Redis Sentinel (3 nodes minimum) or managed Redis (e.g., ElastiCache, Cloud Memorystore).

Separation of concerns:
  Redis instance 1 (ephemeral): cache, session, compatibility matrix
    — Loss is tolerable (fallback to DB).
  Redis instance 2 (durable): rate limits, quota counters, circuit breaker state
    — Loss degrades enforcement; use fallback (in-memory / DB).

Rules:
  1. No single Redis instance in production.
  2. Connection pool: max 50 connections per API/worker process.
  3. Redis operations must have 500ms timeout (do not hang on Redis failure).
  4. All Redis keys must have TTL (no unbounded keys except quota counters).
```

---

## 47. Local Development Architecture (v1.3 addition)

### 47.1 Core Rule

Any developer must be able to run LabLex locally with a single command. No external service dependencies beyond Docker.

### 47.2 docker-compose.yml Services

```text
postgres:15          — primary database
redis:7-alpine       — cache, rate limiting, quota counters
minio                — S3-compatible object storage
backend              — FastAPI application
frontend             — Next.js development server
worker               — single worker process handling all queues (dev only)
```

### 47.3 Environment Configuration

```text
.env.example must include (with safe defaults for local dev):

  DATABASE_URL=postgresql://lablex:lablex@localhost:5432/lablex
  REDIS_URL=redis://localhost:6379/0
  S3_ENDPOINT=http://localhost:9000
  S3_ACCESS_KEY=minioadmin
  S3_SECRET_KEY=minioadmin
  S3_BUCKET=lablex
  JWT_SECRET=local-dev-secret-change-in-production
  JWT_EXPIRY_SECONDS=3600
  ENCRYPTION_KEY=local-dev-encryption-key-32bytes!!
  LOG_LEVEL=DEBUG
  ENVIRONMENT=development
  CORS_ORIGINS=http://localhost:3000
```

### 47.4 Seed Data

```text
The seed script (make seed) must create:
  1. Default tenant: "LabLex Local" (tenant_id: local_dev)
  2. Default admin user: admin@lablex.local / password: admin
  3. Mock Adapter manifest (ready to use)
  4. Sample ExternalTool manifest (Promptfoo template)
  5. Sample Target manifest (HTTP API template)
  6. Sample ResultSchema manifest (generic JSON)
  7. Sample MetricProfile manifest (standard_eval_metrics_v1)
  8. Sample Benchmark manifest
  9. Default tenant quota config (generous limits for dev)
```

### 47.5 Bootstrap Commands

```text
make setup           → docker-compose up -d + wait for healthy + migrate + seed
make dev             → start backend + frontend + worker in dev mode with hot-reload
make test            → run full test suite against test database
make test-unit       → run unit tests only
make test-integration → run integration tests only
make migrate         → run Alembic migrations
make seed            → run seed data script
make reset           → drop database + re-migrate + re-seed
make lint            → run linters and type checkers
make clean           → docker-compose down -v (remove all volumes)
```

### 47.6 First-Run Experience

```text
1. Clone repository.
2. Copy .env.example to .env.
3. Run: make setup
4. Open: http://localhost:3000
5. Login: admin@lablex.local / admin
6. See: Dashboard with onboarding guidance.
7. Create first run with Mock Adapter.
8. See: results in under 30 seconds.
```

---

## 48. Resilience Architecture (v1.3 addition)

### 48.1 Core Rule

LabLex must handle external failures gracefully. External tools are unreliable by nature. LabLex must not be brought down by a failing tool.

### 48.2 Circuit Breaker Per External Tool

```text
States:
  closed       — normal operation, requests pass through
  open         — tool is considered unhealthy, requests are rejected immediately
  half-open    — one probe request allowed to test recovery

Transitions:
  closed → open:      after 5 consecutive failures within 5 minutes
  open → half-open:   after 60-second cooldown
  half-open → closed: if probe request succeeds
  half-open → open:   if probe request fails

Behavior when open:
  POST /api/v1/runs with this tool → HTTP 503 with:
  {
    "error_code": "TOOL_CIRCUIT_OPEN",
    "message": "External tool is temporarily unavailable due to repeated failures.",
    "retryable": true,
    "retry_after_seconds": 60
  }

Circuit state stored in Redis. Shared across all workers.
```

### 48.3 Retry Policies Per Adapter Type

```text
HTTP Adapter:
  Retries: 3
  Backoff: exponential (1s, 3s, 9s)
  Retry on: HTTP 429, 502, 503, 504, connection timeout
  Do NOT retry on: HTTP 400, 401, 403, 404, 409

CLI Adapter:
  Retries: 0 (CLI execution is not idempotent by default)
  Exception: if adapter manifest declares idempotent: true, allow 1 retry

Docker Adapter:
  Retries: 1 (container restart)
  Backoff: 5 seconds
  Retry on: container OOM killed, Docker daemon timeout
  Do NOT retry on: non-zero exit code (application error)

Webhook Adapter:
  Retries: N/A (webhook is inbound, external system retries)

Normalization:
  Retries: 1
  Retry on: transient DB error
  Do NOT retry on: schema_mismatch, normalization_failed

Object Storage Write:
  Retries: 3
  Backoff: exponential (500ms, 1.5s, 4.5s)
  Retry on: connection error, timeout, HTTP 500/503
```

### 48.4 Graceful Degradation

```text
Redis unavailable:
  → Quota checks: fallback to DB query (Section 46.6)
  → Rate limiting: fallback to in-memory counter
  → Circuit breaker: fallback to closed (allow requests, log WARNING)
  → Cache: all lookups go to DB directly

Object Storage unavailable:
  → Raw result capture: queue for retry (do NOT fail the run)
  → Report export: return 503 with retry guidance
  → Artifact download: return 503

External tool unresponsive:
  → Timeout policy applies (Section 26.6)
  → Circuit breaker opens after threshold
  → Partial results captured if available

Database unavailable:
  → All requests fail with 503 (no degradation possible)
  → Health check returns unhealthy
  → CRITICAL log emitted
```

---

## 49. Notification Architecture (v1.3 addition)

### 49.1 Core Rule

Users must be informed of important events without polling. Notifications are asynchronous and must never block run execution.

### 49.2 Notification Events

```text
run.completed          — "Run run_001 completed successfully"
run.failed             — "Run run_001 failed: adapter timeout"
run.timed_out          — "Run run_001 timed out after 3600s"
batch.completed        — "Batch batch_001 completed: 8/10 succeeded"
quota.warning          — "You have used 80% of your daily run quota"
quota.exceeded         — "Daily run quota reached. Resets in 4 hours."
manifest.deprecated    — "Adapter cli_json_capture_v1 has been deprecated"
report.ready           — "Report for run_001 is ready to view"
circuit.opened         — "External tool Promptfoo marked as unavailable"
circuit.closed         — "External tool Promptfoo recovered"
```

### 49.3 Notification Channels

```text
MVP:
  In-app notifications (bell icon in UI header)
    — Stored in notifications table
    — Delivered via SSE or polling
    — Mark as read/unread
    — Max 100 unread per user

  Webhook callback (user-configured URL)
    — POST to user-provided URL with event payload
    — HMAC-SHA256 signature on outbound webhooks
    — 3 retries with exponential backoff on failure

Post-MVP:
  Email notifications (opt-in)
  Slack integration (webhook URL)
  Microsoft Teams integration (webhook URL)
```

### 49.4 Notification Preferences

```text
Per-user notification preferences:
  user_notification_preferences
    id, user_id, tenant_id, event_type, channel, enabled, created_at, updated_at

Defaults:
  run.completed      → in-app: ON,  webhook: OFF
  run.failed         → in-app: ON,  webhook: OFF
  quota.warning      → in-app: ON,  webhook: OFF
  manifest.deprecated → in-app: ON, webhook: OFF
```

### 49.5 Required Tables

```text
notifications
  id, tenant_id, user_id, event_type, title, body, data (JSONB),
  read, created_at, read_at

notification_webhooks
  id, tenant_id, url, secret, events (JSONB array), enabled,
  last_delivery_status, created_at, updated_at

user_notification_preferences
  id, user_id, tenant_id, event_type, channel, enabled,
  created_at, updated_at
```

### 49.6 Rules

```text
1. Notification delivery must NEVER block or delay run execution.
2. Failed notification delivery is logged but does not affect run status.
3. Notifications are tenant-scoped.
4. Notification webhooks use the same HMAC-SHA256 signing as inbound webhooks (Section 36).
5. Notification body must not contain secrets or raw credentials.
6. In-app notifications are paginated (50 per page) and sortable by date.
```

---

## 50. Deployment Architecture (v1.4 addition)

### 50.1 Core Rule

LabLex must have a defined production deployment topology. `docker-compose` is for development only.

### 50.2 MVP Production Topology

```text
                        ┌─────────────┐
                        │   CDN       │ ← static frontend assets
                        └──────┬──────┘
                               │
                        ┌──────▼──────┐
                        │ Load Balancer│ ← TLS termination, health checks
                        └──────┬──────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
        ┌─────▼─────┐   ┌─────▼─────┐   ┌─────▼─────┐
        │ API #1    │   │ API #2    │   │ API #N    │  ← stateless, auto-scaled
        └─────┬─────┘   └─────┬─────┘   └─────┬─────┘
              └────────────────┼────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
     ┌─────▼─────┐      ┌─────▼─────┐      ┌─────▼─────┐
     │ PostgreSQL │      │ Redis HA  │      │ S3/MinIO  │
     │ (managed)  │      │ (Sentinel)│      │ (managed) │
     └───────────┘      └───────────┘      └───────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │          │           │          │            │
  ┌─────▼────┐ ┌──▼─────┐ ┌──▼──────┐ ┌─▼────────┐ ┌▼──────────┐
  │cli_worker│ │http_    │ │docker_  │ │normalize_│ │report_    │
  │  ×2      │ │worker×2 │ │worker×2 │ │worker ×2 │ │worker ×1  │
  └──────────┘ └─────────┘ └─────────┘ └──────────┘ └───────────┘
```

### 50.3 Scaling Triggers

```text
API instances:
  Scale up: CPU > 70% sustained 5 minutes
  Scale down: CPU < 30% sustained 15 minutes
  Min: 2 instances, Max: 10 instances

Workers (per type):
  Scale up: queue depth > 10 for 2 minutes
  Scale down: queue depth = 0 for 10 minutes
  Min: 1 per type (except report_worker: 1), Max: 10

PostgreSQL:
  Read replica when connections > 80% pool capacity
  Consider connection pooler (PgBouncer) from day one

Redis:
  Sentinel/Cluster from day one in production
  See §46.7 for HA details
```

### 50.4 Zero-Downtime Deployment

```text
1. Build new container image, tag with git SHA.
2. Rolling update: replace one instance at a time.
3. Health check must pass before old instance is removed.
4. Workers: drain before shutdown (see §26.10).
5. Database migrations: additive-only in v1.x (add column, not alter/drop).
6. Rollback: revert to previous container image (DB migration rollback scripts required).
```

### 50.5 Production Infrastructure Requirements

```text
TLS:
  Mandatory on all external-facing endpoints.
  Certificate management via Let's Encrypt or cloud provider.
  Internal service communication: TLS or private network.

DNS:
  api.lablex.io → Load Balancer
  app.lablex.io → CDN → Frontend

CI/CD:
  Trigger: push to main branch.
  Pipeline: lint → type-check → unit tests → build → integration tests → deploy staging → smoke test → deploy production.
  Rollback: automated on smoke test failure.

Container Orchestration:
  Kubernetes (recommended) or Docker Swarm.
  Helm charts for all services.
  Namespace isolation per environment (staging, production).
```

---

## 51. Backup & Disaster Recovery (v1.4 addition)

### 51.1 Core Rule

Data loss is unacceptable. Every data store must have a backup strategy with defined RPO and RTO.

### 51.2 Backup Targets

```text
PostgreSQL:
  Method: Automated daily full backup + continuous WAL archiving (PITR)
  RPO: 1 hour (point-in-time recovery from WAL)
  RTO: 4 hours
  Retention: 30 daily backups
  Location: separate region or availability zone
  Verification: weekly automated restore test to staging

Object Storage (S3/MinIO):
  Method: Cross-region replication (if using cloud S3)
          or daily rsync to backup location (if using MinIO)
  RPO: 24 hours
  RTO: 8 hours
  Retention: follows artifact retention policy (§38)

Redis:
  Method: RDB snapshots every 15 minutes + AOF for durability
  RPO: 15 minutes
  RTO: 5 minutes (Redis restart with snapshot)
  Note: Redis data is reconstructable from PostgreSQL (cache, counters)
        — full loss is recoverable, just slower.
```

### 51.3 Disaster Recovery Procedure

```text
Database failure:
  1. Failover to read replica (if available).
  2. Restore from latest WAL backup to new instance.
  3. Verify data integrity.
  4. Update connection strings.
  5. Resume operations.

Object storage failure:
  1. Switch to backup storage endpoint.
  2. Presigned URLs regenerated for new endpoint.
  3. Runs in progress may lose partial artifacts → mark as capture_failed.

Full region failure:
  Post-MVP concern. Requires multi-region deployment.
  Strategy: warm standby in secondary region.
```

---

## 52. Operational Workflows (v1.4 addition)

### 52.1 Re-Run Workflow

```text
Endpoint: POST /api/v1/runs/{run_id}/rerun

Behavior:
  1. Load original ToolRun and its RunSpec.
  2. Create NEW RunSpec from CURRENT versions of the same components
     (not from the old snapshot — use fresh manifests).
  3. Create NEW ToolRun linked to the new RunSpec.
  4. The new run references the original: rerun_of: original_run_id.
  5. Compatibility re-validated against current manifests.
  6. If a component was deprecated/retired since original run:
       → return 409 with detail about which component changed.

Rules:
  1. Re-run creates a completely independent run.
  2. Original run's data is untouched.
  3. Re-run is subject to quotas and rate limits.
  4. Audit event: run.rerun with original_run_id.
```

### 52.2 Renormalize Workflow

```text
Endpoint: POST /api/v1/results/{run_id}/renormalize
Body: { "result_schema_id": "updated_schema_v2" }  (optional — defaults to current schema)

Behavior:
  1. Verify RawResult still exists (not expired).
  2. Load RawResult from storage.
  3. Apply the specified (or current) ResultSchema against the RawResult.
  4. Create NEW NormalizedResult row (do not overwrite original).
  5. Original NormalizedResult: status → superseded.
  6. New NormalizedResult references the same RawResult.
  7. Audit event: result.renormalized with old and new normalized_result_ids.

Rules:
  1. RawResult must exist and not be expired (storage_status: active).
  2. Expired RawResult → return 410 Gone: "Raw result has expired."
  3. Renormalize does NOT re-run the external tool.
  4. Renormalize does NOT modify the original NormalizedResult.
  5. Comparisons referencing the original NormalizedResult are unaffected
     (they snapshot metric values at creation time — §31.6 rule 4).
```

### 52.3 Register New Tool Wizard

```text
Guided workflow for onboarding a new external tool:

Step 1: Tool Basic Info
  → Name, type, description, execution_mode (cli/http/docker/webhook)

Step 2: Connection Setup
  → Provide endpoint URL, CLI path, Docker image, or webhook config
  → Test connection: POST /api/v1/external-tools/{id}/test-connection

Step 3: Adapter Selection or Creation
  → Select existing adapter or create new adapter manifest
  → If new: guided adapter manifest builder with defaults per execution_mode
  → Validate: POST /api/v1/adapters/{id}/validate

Step 4: Result Schema Setup
  → Upload sample output from tool
  → Guided JSONPath mapping builder
  → Validate: POST /api/v1/result-schemas/{id}/validate

Step 5: Compatibility Declaration
  → Auto-fill compatible_adapters, compatible_result_schemas
  → Review and confirm

Step 6: Dry Run
  → POST /api/v1/runspecs/{id}/dry-run with mock target
  → Verify full pipeline: connection → execution → capture → normalize

Step 7: Confirmation
  → All manifests saved
  → Tool ready to use in Create Run flow

Note: This wizard is a UI convenience. All steps are individually
achievable via API (for programmatic tool registration).
```

### 52.4 Worker Health & Zombie Detection

```text
Worker heartbeat:
  Every worker sends a heartbeat to Redis every 30 seconds:
    Key: worker:heartbeat:{worker_type}:{worker_id}
    TTL: 90 seconds
  Missing heartbeat → worker considered dead → alert.

Zombie run detection (cron job, every 5 minutes):
  1. Query: SELECT * FROM tool_runs WHERE status = 'running'
            AND updated_at < NOW() - (2 × max_run_duration_seconds)
  2. For each zombie run:
       → Mark as timed_out.
       → Emit audit event: run.zombie_detected.
       → Capture partial results if available.
       → Alert operations team.

Health check endpoint:
  GET /api/v1/health
  Response:
  {
    "status": "healthy",
    "checks": {
      "database": "ok",
      "redis": "ok",
      "object_storage": "ok",
      "workers": {
        "cli_worker": { "count": 2, "healthy": 2 },
        "http_worker": { "count": 2, "healthy": 2 },
        "normalization_worker": { "count": 2, "healthy": 1 }
      }
    }
  }
```

---

### v1.4 New Acceptance Criteria

```text
Adapter Cancellation:
  ☐ cancel() method defined on adapter interface.
  ☐ CLI adapter implements SIGTERM → SIGKILL cancel flow.
  ☐ POST /api/v1/runs/{id}/cancel propagates to adapter.

Compatibility Declaration:
  ☐ Tool manifests declare compatible_adapters.
  ☐ Adapter manifests declare compatible_result_schemas.
  ☐ Compatibility Engine validates intersection before RunSpec composition.

Dead Letter Queue:
  ☐ Every worker queue has a DLQ.
  ☐ Failed messages move to DLQ after max_retries.
  ☐ Run status transitions to internal_error (not stuck).

Worker Operations:
  ☐ Workers drain gracefully on SIGTERM.
  ☐ Zombie run detection cron runs every 5 minutes.
  ☐ Worker heartbeat monitored.

Security:
  ☐ CSRF protection on browser session mutations.
  ☐ XSS protection: raw output viewer sandboxed.
  ☐ Webhook URLs use opaque tokens.
  ☐ Presigned URL generation validates tenant_id.

Data Model:
  ☐ batches table exists with proper indexes.
  ☐ tool_runs has batch_id and runspec_id FKs.
  ☐ NormalizedResult has raw_result_id FK.
  ☐ manifests scoped by (tenant_id, kind, id).
  ☐ MetricProfile CRUD endpoints exist.

Operational Workflows:
  ☐ Re-run endpoint creates new RunSpec from current manifests.
  ☐ Renormalize endpoint re-applies schema to existing RawResult.
  ☐ Register New Tool wizard guides first-time setup.

Scalability:
  ☐ SSE events distributed via Redis Pub/Sub.
  ☐ Quota enforcement is atomic (Redis INCR).
  ☐ Redis HA configured for production.

Deployment:
  ☐ Production topology defined and documented.
  ☐ Zero-downtime deployment procedure tested.
  ☐ Backup strategy with defined RPO/RTO.
  ☐ Health check endpoint reports DB, Redis, S3, worker status.

External-First Boundary:
  ☐ Report section uses "User Notes" not "Recommendation".
  ☐ Metric sort is user-configured, not auto-leaderboard.
  ☐ EvalEngine is NOT independently selectable in Create Run.
```

> **Production Gates:** See §43 for the authoritative 22-gate list.
> All gates must be green before first external tool execution.

---

## 53. Tenant Onboarding & Data Portability (v1.5 addition)

### 53.1 Tenant Onboarding Flow

```text
Self-Service Registration (MVP):
  1. User visits app.lablex.io/signup.
  2. Provides: email, password, tenant name.
  3. Email verification sent.
  4. On verification: tenant created, user assigned 'owner' role.
  5. Default quota config applied.
  6. Redirect to dashboard with onboarding guidance.
  7. Guided: "Register your first tool" wizard (§52.3).

Invitation Flow:
  1. Owner/Admin invites user via email.
  2. Invited user receives link with invitation token.
  3. User creates account (or links existing).
  4. User added to tenant with specified role.
  5. Audit event: member.invited, member.joined.

Required Tables:
  invitations
    id, tenant_id, email, role, token, status (pending/accepted/expired),
    invited_by, created_at, expires_at

Rules:
  1. Invitation tokens expire after 7 days.
  2. One email can belong to multiple tenants (different roles).
  3. Tenant name must be unique.
  4. First user is always 'owner' — cannot be removed.
```

### 53.2 Data Export (GDPR Compliance)

```text
Endpoint: POST /api/v1/tenant/export
Response: { "export_id": "exp_001", "status": "processing" }

Exported Data:
  1. All manifests (YAML)
  2. All RunSpecs (JSON)
  3. All ToolRun metadata (JSON)
  4. All NormalizedResults (JSON)
  5. All RawResults (original files from S3)
  6. All Reports (generated files)
  7. All Audit Events (JSON)
  8. Tenant configuration (quotas, retention, members)

Export Format:
  ZIP archive with directory structure:
    export/
      manifests/
      runspecs/
      runs/
      results/raw/
      results/normalized/
      reports/
      audit/
      config.json

Rules:
  1. Export is asynchronous — may take minutes for large tenants.
  2. Export notification sent when ready (§49).
  3. Export file available for download for 7 days.
  4. Only 'owner' role can trigger export.
  5. Audit event: tenant.data_exported.
```

### 53.3 Tenant Deletion

```text
Endpoint: DELETE /api/v1/tenant
Headers: X-Confirm-Delete: <tenant_name>   (must match exactly)

Deletion Cascade:
  1. All active runs cancelled (via adapter cancel).
  2. All queued runs removed from worker queues.
  3. Grace period: 30 days (tenant marked as 'pending_deletion').
  4. During grace period: tenant is read-only. Owner can cancel deletion.
  5. After grace period:
       - All S3 objects under tenant prefix deleted.
       - All PostgreSQL rows with tenant_id deleted.
       - All Redis keys with tenant_id prefix deleted.
       - Audit events retained for 2 years (legal requirement).
  6. Deletion is irreversible after grace period.

Rules:
  1. Only 'owner' can delete tenant.
  2. Requires X-Confirm-Delete header matching tenant name.
  3. Audit event: tenant.deletion_requested, tenant.deletion_cancelled, tenant.deleted.
  4. All members notified via email when deletion is requested.
```

---

### v1.5 New Acceptance Criteria

```text
RunSpec Lifecycle:
  ☐ RunSpec states (draft → composed → validated → locked → archived) enforced.
  ☐ DB trigger prevents UPDATE on locked/archived RunSpec.
  ☐ POST /api/v1/runs rejects non-locked RunSpec with 400.

State-Activity Mapping:
  ☐ internal_error state added to run lifecycle.
  ☐ State-to-activity mapping documented and implemented.

Manifest Schemas:
  ☐ JSON Schema file exists for every manifest kind.
  ☐ POST /api/v1/manifests validates against schema before storing.
  ☐ Schema validation errors return field-level detail.

ReportTemplate:
  ☐ ReportTemplate manifest defined with sections and branding.
  ☐ Report Generator = data + template only (no narrative generation).

OpenAPI:
  ☐ OpenAPI 3.1 spec auto-generated from FastAPI.
  ☐ Contract tests validate against spec in CI.

Testing:
  ☐ Cancellation test: cancel propagates to adapter.
  ☐ DLQ test: poison message moves to DLQ, run → internal_error.
  ☐ Renormalize test: new NormalizedResult, original → superseded.
  ☐ RunSpec lifecycle test: locked RunSpec rejects updates.

Tenant Operations:
  ☐ Self-service registration flow works.
  ☐ Data export produces complete ZIP archive.
  ☐ Tenant deletion cascade with 30-day grace period.
```

> **Production Gates:** See §43 for the authoritative 22-gate list. All gates must be green before first external tool execution.

---

## 54. Architectural Refinements (v1.6 addition)

### 54.1 Sample-Level (Trial) Normalization
LabLex processes individual test-case (sample/trial) metrics. The normalizer splits raw result arrays and maps them to `normalized_samples` based on `ResultSchema` manifests. This provides granular cross-run comparisons of exact prompt inputs and outputs in the UI without implementing any internal scoring logic.

### 54.2 Sandbox and Resource Quota Enforcement
Workers must never mount `/var/run/docker.sock`. Docker execution is delegated to isolated container runtimes (such as AWS Fargate, GCP Cloud Run, or sandboxed Kubernetes Jobs with gVisor). Every adapter manifest enforces explicit CPU and memory quotas to prevent resource starvation or container breakout.

### 54.3 Webhook Token Cache
Webhook callbacks are validated in-memory by caching the opaque token metadata (webhook_secret, tenant_id, tool_connection_id) in Redis with a 24-hour TTL. This avoids database connection starvation during high-frequency callback spikes. Webhook endpoints return HTTP 202 Accepted immediately.

### 54.4 Secrets Envelope Encryption
Credentials and API keys are stored in `secret_refs` and encrypted at-rest using AES-256-GCM. Decryption is performed in-memory at execution runtime using tenant-specific Data Encryption Keys (DEKs) encrypted by a cloud Key Management Service (KMS) master Key Encryption Key (KEK).

### 54.5 Connectivity Pre-Checks
The RunSpec validation step triggers active credentials and availability pings to external ToolConnections and target model APIs prior to locking the RunSpec. This ensures validation errors are returned immediately to the user rather than failing silently in the queue.

---

### v1.6 New Acceptance Criteria

```text
Sample-Level Normalization:
  ☐ ResultSchema supports mapping arrays of sample results via JSONPath (source_array).
  ☐ normalized_samples database table exists and stores granular test-case input, output, score, and status.
  ☐ Normalization worker inserts mapped samples transactionally alongside the NormalizedResult.

Docker Sandboxing & Limits:
  ☐ CLI and HTTP Workers have zero access to the docker.sock.
  ☐ Production runs execute Docker containers inside isolated container runtimes (such as AWS Fargate or gVisor sandbox).
  ☐ Adapter manifests enforce cpu_limit and memory_limit configurations.

Secrets Protection:
  ☐ secret_refs database table stores encrypted values using AES-GCM-256 with key versions.
  ☐ KMS Envelope Encryption flow is implemented to generate a tenant-specific DEK encrypted by KMS master KEK.

Webhook Resilience:
  ☐ Webhook token metadata is cached in Redis with a 24-hour TTL.
  ☐ Webhook API endpoint utilizes fast-path Redis token resolution to prevent DB connection pool starvation.
  ☐ Webhooks return HTTP 202 Accepted immediately upon queueing.

Connectivity Pre-checks:
  ☐ RunSpec validation step triggers active credentials and availability pings to ToolConnection endpoints to fail-fast on bad credentials.
```

> **Production Gates:** See §43 for the authoritative 22-gate list. All gates must be green before first external tool execution.
