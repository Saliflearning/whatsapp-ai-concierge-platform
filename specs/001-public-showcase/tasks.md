# Tasks: Privacy-Safe WhatsApp AI Concierge Showcase

**Input**: Design documents in `specs/001-public-showcase/`

**Tests**: Required by constitution 1.0.0. Behavioral and security tests precede implementation.

## Phase 1: Setup and Safety Foundation

- [x] T001 Create backend/frontend/docs/scripts directory structure from `plan.md`.
- [x] T002 Add root `.env.example`, `.dockerignore`, `LICENSE.md`, and safe ignore rules.
- [x] T003 [P] Configure Python dependencies, Ruff, MyPy, and pytest in `backend/pyproject.toml` and lock inputs.
- [x] T004 [P] Configure Next.js, TypeScript, ESLint, Vitest, and exact npm lockfile in `frontend/`.
- [x] T005 [P] Implement redacted current/history safety scanner in `scripts/scan_public_safety.py` with scanner tests.
- [x] T006 Add synthetic provenance manifest in `docs/SYNTHETIC_DATA_POLICY.md` and ensure no client source paths are referenced.

**Checkpoint**: Clean installs work and the repository can detect forbidden public content.

## Phase 2: Foundational Domain and Tenant Boundary

- [x] T007 [P] Write domain validation tests for bounded messages/locales/statuses in `backend/tests/test_domain.py`.
- [x] T008 [P] Write SQLite schema/repository tests for tenant isolation, idempotency, approved knowledge, and audit append-only behavior in `backend/tests/test_repository.py`.
- [x] T009 [P] Write authentication tests for demo tokens and HMAC request verification in `backend/tests/test_security.py`.
- [x] T010 Implement Pydantic domain models in `backend/app/domain/models.py` (FR-001, FR-003, FR-007).
- [x] T011 Implement environment/runtime settings that fail closed outside demo mode in `backend/app/core/config.py` (FR-012, FR-016).
- [x] T012 Implement HMAC and tenant-scoped operator authentication in `backend/app/core/security.py` (FR-001, FR-002).
- [x] T013 Implement SQLite schema, transaction helpers, and tenant-scoped repository in `backend/app/repositories/sqlite.py` (FR-002, FR-003, FR-006, FR-008, FR-009).
- [x] T014 Implement deterministic synthetic seed/reset service in `backend/app/services/seed.py` (FR-012, FR-016).
- [x] T015 Implement structured redacted audit logging in `backend/app/services/audit.py` (FR-006, FR-016).

**Checkpoint**: Foundational security and storage tests pass; cross-tenant operations fail closed.

## Phase 3: User Story 1 — Safe Grounded Conversation (P1)

- [x] T016 [P] [US1] Write policy tests for approved grounding, insufficient evidence, sensitive requests, unsupported locale, and no future-work promises in `backend/tests/test_policy.py`.
- [x] T017 [P] [US1] Write API contract tests for health, signed webhook, invalid signature, duplicate event, demo message, and cross-tenant retrieval in `backend/tests/test_api.py`.
- [x] T018 [US1] Implement provider and response-generator interfaces plus local fake adapters in `backend/app/adapters/` (FR-013).
- [x] T019 [US1] Implement approved-knowledge matcher with same-tenant enforcement in `backend/app/services/grounding.py` (FR-004).
- [x] T020 [US1] Implement deterministic conversation policy and bounded English/French/Spanish response templates in `backend/app/services/policy.py` (FR-005, FR-007).
- [x] T021 [US1] Implement orchestration service creating messages, decisions, handoffs, and audit events atomically in `backend/app/services/conversation.py` (FR-003 through FR-007).
- [x] T022 [US1] Implement `/health`, `/webhooks/messages`, and `/api/demo/messages` in `backend/app/api/routes.py` and application wiring in `backend/app/main.py`.
- [x] T023 [US1] Validate User Story 1 independently with contract, tenant, policy, and 100-request local performance checks (SC-002, SC-003).

**Checkpoint**: A signed synthetic message yields either cited evidence or an honest audited handoff.

## Phase 4: User Story 2 — Operator Review and Handoff (P2)

- [x] T024 [P] [US2] Write API tests for conversation list/detail, handoff resolution idempotency, and cross-tenant mutation denial in `backend/tests/test_operator_api.py`.
- [x] T025 [P] [US2] Write frontend component tests for summary cards, evidence display, failure states, and handoff actions in `frontend/tests/`.
- [x] T026 [US2] Implement tenant-scoped conversation/detail/handoff routes in `backend/app/api/operator.py` (FR-008, FR-009).
- [x] T027 [US2] Implement typed API client and demo configuration boundary in `frontend/lib/api.ts` and `frontend/lib/types.ts`.
- [x] T028 [US2] Implement recruiter-facing overview and architecture sections in `frontend/app/page.tsx` and reusable components.
- [x] T029 [US2] Implement interactive demo dashboard with message submission, conversation evidence, audit timeline, and handoff resolution in `frontend/app/demo/` (FR-010).
- [x] T030 [US2] Implement responsive accessible visual system and 390-pixel behavior in `frontend/app/globals.css` and components (FR-011).
- [x] T031 [US2] Run desktop/mobile browser verification; capture only synthetic screenshots in `docs/assets/` (SC-004).

**Checkpoint**: The operator journey works on desktop/mobile and preserves tenant/audit behavior.

## Phase 5: User Story 3 — Reproducible Engineering Evidence (P3)

- [x] T032 [P] [US3] Create accurate README with problem, architecture, stack, demo, evidence, screenshots, decisions, limitations, and license decision (FR-014, SC-006, SC-007).
- [x] T033 [P] [US3] Create Mermaid architecture/data-flow documentation in `docs/architecture.md` and security model in `docs/SECURITY_MODEL.md`.
- [x] T034 [P] [US3] Record ADRs for clean-room provenance, deterministic grounding, SQLite demo persistence, and provider seams in `docs/decisions/`.
- [x] T035 [US3] Finalize and execute `specs/001-public-showcase/quickstart.md` from a clean local state (SC-001).
- [x] T036 [US3] Add Dockerfiles and root `compose.yaml`; verify container build without secrets.
- [x] T037 [US3] Add least-privilege GitHub CI for Python, frontend, container, dependency, CodeQL-compatible, and redacted safety gates in `.github/workflows/ci.yml` (FR-015).
- [x] T038 [US3] Add `SECURITY.md`, Dependabot configuration, badges, and `docs/PORTFOLIO_READINESS.md` with exact verification evidence.

**Checkpoint**: A fresh-clone reviewer can reproduce the full demo and evidence without paid services.

## Phase 6: Protected Release and Portfolio Integration

- [x] T039 Run backend tests/Ruff/MyPy/pip-audit and frontend tests/lint/typecheck/build/npm audit; resolve every actionable finding.
- [x] T040 Run exact current-tree and full-history safety scans for secrets, identity/contact patterns, and forbidden artifacts (SC-005).
- [x] T041 Run Graphify code-only refresh and a five-axis code/security/documentation review.
- [x] T042 Push a review branch, require green protected PR checks, and perform an independent fresh-clone audit from GitHub.
- [x] T043 Rename GitHub repository to `whatsapp-ai-concierge-platform`, update origin/metadata/topics/handoffs, then make public only after all gates pass.
- [x] T044 Enable branch protection, secret scanning/push protection, Dependabot/security updates, CodeQL, and private vulnerability reporting; remediate or evidence-document all alerts.
- [x] T045 Add the verified public flagship and exact evidence to the private
  shared portfolio coordination hub without publishing source locations or identifiers.

## Dependencies and Execution Order

- Phase 1 blocks all implementation.
- Phase 2 blocks both product stories.
- User Story 1 is the API MVP and precedes the dashboard integration.
- User Story 2 may begin frontend tests after API contracts stabilize.
- User Story 3 documentation tasks can run in parallel after the implemented claims exist.
- Publication tasks are strictly last and require all prior checkboxes complete.

## Requirement Coverage

- FR-001–FR-003: T007–T013, T017, T022–T023
- FR-004–FR-007: T016, T019–T023
- FR-008–FR-011: T024–T031
- FR-012–FR-016: T002–T006, T011, T014–T015, T018, T032–T040
- SC-001–SC-007: T023, T031–T045
