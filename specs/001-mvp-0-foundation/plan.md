# Implementation Plan: LabLex MVP-0 Foundation

**Branch**: `001-mvp-0-foundation` | **Date**: 2026-06-25 | **Spec**: [spec.md](file:///d:/LabLex/specs/001-mvp-0-foundation/spec.md)

**Input**: Feature specification from `/specs/001-mvp-0-foundation/spec.md`

## Summary

LabLex MVP-0 Foundation establishes the technical skeleton of the system. This includes the FastAPI backend, Next.js frontend, database migration infrastructure using Alembic, Docker Compose orchestration for local services (PostgreSQL, Redis, MinIO), tenant-scoping and RBAC middleware, a health check endpoint, and a unified error model.

## Technical Context

**Language/Version**: Python 3.12 (Backend) + TypeScript / Node.js 20 (Frontend)

**Primary Dependencies**: FastAPI, Pydantic, SQLAlchemy, Alembic, Uvicorn, Next.js, React, TailwindCSS, PyJWT, passlib, redis-py, boto3

**Storage**: PostgreSQL (Primary Relational DB), Redis (Session cache & rate limiter), MinIO (Object Storage)

**Testing**: pytest (Backend) + Jest/React Testing Library (Frontend)

**Target Platform**: Linux Server / Dockerized Environment

**Project Type**: Multi-service Web Application

**Performance Goals**: API response times <100ms for health check; auth middleware latency <10ms.

**Constraints**: Strict tenant isolation at database query layer; all state-changing endpoints require authentication.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **External-First Rule**: PASS. No internal evaluation, scoring, or execution logic is planned.
- **22-Gate Compliance**: PASS. Day-0 security structures (auth, scoping, error model) are configured to align with Gates 1, 3, 5, 9, 10, 11, and 22.

## Project Structure

### Documentation (this feature)

```text
specs/001-mvp-0-foundation/
├── spec.md              # Feature specification
├── plan.md              # This file
└── tasks.md             # Tasks checklist
```

### Source Code (repository root)

We choose **Option 2: Web application** structure:

```text
backend/
├── alembic/             # Alembic migration scripts
│   └── versions/
├── src/
│   ├── api/             # API Router definitions versioned under /api/v1/
│   │   ├── auth.py
│   │   ├── health.py
│   │   └── router.py
│   ├── core/            # Configuration and security rules
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── errors.py
│   │   └── security.py
│   ├── middleware/      # Scoping and RBAC middleware
│   │   ├── scoping.py
│   │   └── rbac.py
│   ├── models/          # SQLAlchemy Database ORM Models
│   │   ├── tenant.py
│   │   ├── user.py
│   │   └── api_key.py
│   └── main.py          # FastAPI application entrypoint
├── tests/               # Backend tests
└── requirements.txt

frontend/
├── public/
├── src/
│   ├── components/      # Next.js reusable components
│   ├── pages/           # Next.js pages (dashboard, login)
│   └── services/        # Next.js API client services
├── package.json
└── tsconfig.json

docker-compose.yml       # Orchestrates postgres, redis, minio, backend, frontend, worker
.env.example             # Template for local environment variables
```

**Structure Decision**: Standard monorepo layout with decoupled `backend` and `frontend` folders, orchestrated locally using `docker-compose.yml`.

## Complexity Tracking

No violations of project principles. Implementation is kept minimal to satisfy MVP-0 deliverables.
