# Implementation Plan: Privacy-Safe WhatsApp AI Concierge Showcase

**Branch**: `001-public-showcase` | **Date**: 2026-08-30 | **Spec**: [spec.md](spec.md)

## Summary

Build a clean-room monorepo containing a FastAPI conversation service, SQLite
repository, deterministic grounding/policy engine, signed webhook simulator,
tenant-scoped operator API, and responsive Next.js dashboard. Ship synthetic
seed data, local fake provider adapters, tests, CI, diagrams, screenshots, and
truthful limitations so a recruiter can run and evaluate the system safely.

## Technical Context

**Language/Version**: Python 3.12; TypeScript 5.9; Node.js 24

**Primary Dependencies**: FastAPI 0.141.1, Pydantic 2.13.5, Uvicorn 0.52.4,
Next.js 16.3.3, React 19.2.8, Vitest 4.1.11

**Storage**: Local SQLite through a tenant-scoped repository; synthetic reset/seed

**Testing**: pytest, FastAPI TestClient/httpx, Ruff, MyPy, Vitest, Testing
Library, Playwright smoke/responsive checks, dependency and secret scans

**Target Platform**: Local Windows/macOS/Linux development and Linux containers

**Project Type**: Web application monorepo (API + operator dashboard)

**Performance Goals**: Local synthetic message response under 500 ms p95 for
100 sequential demo requests; dashboard initial render under 2 seconds on local build

**Constraints**: No paid services, live credentials, client code/data, or model
dependency; bounded payloads; explicit tenant on every operation

**Scale/Scope**: Two synthetic tenants, three bounded locales, tens of demo
records; architecture seams documented for managed providers but not claimed implemented

## Constitution Check

*GATE: passed before research; rechecked after design.*

- Privacy-safe provenance: PASS — clean repository and synthetic-only contracts.
- Truthful evidence: PASS — deterministic demo and explicit limitations.
- Test-first delivery: PASS — contract/security tests precede implementation tasks.
- Tenant/security boundaries: PASS — HMAC webhook plus tenant-scoped operator routes.
- Recruiter legibility: PASS — README, diagram, quick start, screenshots, ADRs,
  and release evidence are required tasks.

## Project Structure

### Documentation

```text
specs/001-public-showcase/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/openapi.yaml
├── checklists/requirements.md
└── tasks.md
```

### Source Code

```text
backend/
├── app/
│   ├── api/
│   ├── core/
│   ├── domain/
│   ├── repositories/
│   ├── services/
│   ├── adapters/
│   └── main.py
├── tests/
├── pyproject.toml
└── requirements.txt

frontend/
├── app/
├── components/
├── lib/
├── tests/
└── package.json

docs/
├── architecture.md
├── decisions/
├── assets/
├── SECURITY_MODEL.md
└── PORTFOLIO_READINESS.md

scripts/
├── scan_public_safety.py
└── verify_release.ps1
```

**Structure Decision**: A two-application monorepo makes the API boundary and
operator experience independently testable while keeping one coherent showcase.

## Delivery Phases

1. Foundation and synthetic safety controls.
2. Tenant-scoped storage and signed inbound message path.
3. Grounding, policy, handoff, and audit behavior.
4. Operator APIs and responsive dashboard.
5. Documentation, screenshots, CI/security settings, fresh-clone audit, publication.

## Complexity Tracking

No constitution violations or unjustified components are present. SQLite and
deterministic policies are deliberately simpler than the private production system.
