# Implementation Plan: LabLex MVP-2 Professional Results

**Branch**: `003-mvp-2-professional-results` | **Date**: 2026-06-25 | **Spec**: [spec.md](file:///d:/LabLex/specs/003-mvp-2-professional-results/spec.md)

---

## Summary

This plan details the technical steps to build **MVP-2: Professional Results**. It implements run comparisons (delta calculations, winner highlights, reporting templates), advanced execution controls (idempotency, run duplicates, quotas, Redis caching), and observability upgrades (SSE Last-Event-ID replay, Heartbeats, Audit Logging, and Batch runs).

---

## Technical Context

- **Caching & Rate Limiting**: Redis is utilized as the key-value store for API rate-limiting, manifest caching, and tracking active concurrent runs.
- **Idempotency**: Implemented using an `idempotency_keys` table in PostgreSQL. When a client sends a header `Idempotency-Key`, the API checks if it has been registered. If yes, it returns the cached response.
- **SSE Heartbeats**: Background thread/task inside the SSE endpoint sending `{"event": "ping"}` heartbeats every 15 seconds to prevent browser timeouts.
- **Audit Logging**: A unified event decorator or middleware capturing tenant actions and appending them to `audit_events` table.

---

## Proposed Project Layout Expansion

```text
backend/
├── src/
│   ├── api/
│   │   ├── comparisons.py   # POST /comparisons, GET /comparisons/{id}
│   │   └── audit.py         # GET /audit-logs
│   ├── core/
│   │   ├── idempotency.py   # Idempotency checks and key storage
│   │   ├── quotas.py        # Quota checking and rate limiting
│   │   ├── cache.py         # Redis manifest caching helper
│   │   └── audit_logger.py  # Audit logging decorator
```

```text
frontend/
├── src/
│   ├── pages/
│   │   ├── comparisons/
│   │   │   ├── index.tsx    # List past comparisons
│   │   │   └── [id].tsx     # Display side-by-side metric tables and deltas
│   │   └── audit/
│   │       └── index.tsx    # View audit logs
```

---

## Constitution Check

- **External-First Rule**: PASS. The comparison engine, report templates, and quotas operate entirely on control plane metadata (run specs, captured JSON metrics, and tenant limits), without implementing any internal scoring or execution logic.
- **22-Gate Compliance**: PASS. Enforces Gate 22 (PostgreSQL Row-Level Security), Gate 11 (API rate-limiting), and Gate 7 (Dry-run structured report validation).
