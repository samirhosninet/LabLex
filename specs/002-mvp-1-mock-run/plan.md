# Implementation Plan: LabLex MVP-1 First Mock Run

**Branch**: `002-mvp-1-mock-run` | **Date**: 2026-06-25 | **Spec**: [spec.md](file:///d:/LabLex/specs/002-mvp-1-mock-run/spec.md)

**Input**: Feature specification from `/specs/002-mvp-1-mock-run/spec.md`

## Summary

LabLex MVP-1 First Mock Run builds the core registry and evaluation pipelines. It implements manifest validation, registry APIs, the compatibility checking engine, a Mock Adapter to generate synthetic results, execution gateways with Celery/Redis tasks, JSONPath-driven normalization, Server-Sent Events (SSE) for progress streaming, and Next.js frontend pages (Registry lists, Create Run wizard, and Result Detail).

## Technical Context

**Language/Version**: Python 3.12 (Backend) + TypeScript / Node.js 20 (Frontend)

**Primary Dependencies**: jsonschema, celery, redis, jsonpath-ng, fastapi-sse, jinja2

**Storage**: PostgreSQL (Run metrics, metadata, registry), MinIO (Raw tool outputs, HTML reports)

**Testing**: pytest + pytest-asyncio + mock libraries

**Performance Goals**: End-to-end mock execution under 10 seconds; SSE latency <100ms; JSONPath extraction under 5ms.

**Constraints**: Immutability of locked RunSpecs; no direct subprocess execution in the Mock Adapter.

## Constitution Check

- **External-First Rule**: PASS. The Mock Adapter simulates external tool execution via structured output fixtures and the same Adapter Interface, without hardcoding internal scoring logic or runner engines.
- **22-Gate Compliance**: PASS. Day-1 gating checks (Gates 2, 7, 12, 15, 16, 17, 18, 20) are integrated.

## Project Structure

### Documentation (this feature)

```text
specs/002-mvp-1-mock-run/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Tasks checklist
```

### Source Code Layout

We expand the existing layout:

```text
backend/
├── src/
│   ├── api/
│   │   ├── registry.py      # Manifest CRUD (Tools, Targets, Models, Benchmarks)
│   │   ├── runspecs.py      # RunSpec composition, validation, dry-run, lock
│   │   ├── runs.py          # Trigger runs, fetch logs, cancel
│   │   └── sse.py           # SSE endpoint /api/v1/runs/{id}/events
│   ├── core/
│   │   ├── compatibility.py # Compatibility intersection rules
│   │   ├── normalizer.py    # JSONPath extractor
│   │   └── celery_app.py    # Background task workers
│   ├── adapters/
│   │   ├── base.py          # Abstract Adapter Interface
│   │   └── mock_adapter.py  # Mock Adapter generating synthetic outputs
│   └── main.py
```

```text
frontend/
├── src/
│   ├── pages/
│   │   ├── registry/        # Lists and detail views for registered components
│   │   ├── runs/
│   │   │   ├── create.tsx   # 7-step Create Run wizard
│   │   │   └── [id].tsx     # Real-time SSE Run details & Metrics view
│   │   └── reports/
│   │       └── [id].tsx     # Render and download generated HTML report
```
