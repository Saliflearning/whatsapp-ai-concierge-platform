# Feature Specification: Privacy-Safe WhatsApp AI Concierge Showcase

**Feature Branch**: `001-public-showcase`

**Created**: 2026-08-30

**Status**: Approved for planning

**Input**: Build a fresh-history, recruiter-ready, runnable showcase of a
multi-tenant WhatsApp AI concierge using only synthetic data and independently
implemented code. Demonstrate grounded answers, policy controls, human handoff,
operator visibility, and engineering evidence without exposing client work.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Safe Grounded Conversation (Priority: P1)

A reviewer sends a synthetic customer message to a demo business and receives
either a grounded answer with evidence or an honest escalation outcome. The
conversation is isolated to that business and recorded in an audit trail.

**Why this priority**: This is the core proof that the platform can orchestrate
a useful, bounded customer interaction rather than merely display architecture.

**Independent Test**: Submit a signed synthetic message, inspect the response,
citation or handoff reason, conversation record, and audit events, and then
verify that another business cannot retrieve them.

**Acceptance Scenarios**:

1. **Given** an approved knowledge source for the selected demo business,
   **When** a relevant message is submitted, **Then** the response cites that
   source and records the decision.
2. **Given** an invalid request signature, **When** a message is submitted,
   **Then** processing is rejected and no conversation is created.
3. **Given** a request that requires a human or lacks approved evidence,
   **When** it is submitted, **Then** the system makes no unsupported promise
   and creates a visible handoff with a reason.
4. **Given** two demo businesses, **When** one business requests the other's
   conversation, **Then** access is denied without revealing its existence.

---

### User Story 2 - Operator Review and Handoff (Priority: P2)

An operator opens a responsive dashboard to review synthetic conversations,
grounding evidence, policy decisions, and handoffs. The operator can resolve a
handoff while preserving an audit record.

**Why this priority**: Recruiters need to see the human-in-the-loop operational
workflow, not only a chatbot endpoint.

**Independent Test**: Load the dashboard on desktop and mobile, inspect one
synthetic conversation and its evidence, resolve its handoff, and verify the
status and audit event update.

**Acceptance Scenarios**:

1. **Given** seeded synthetic conversations, **When** the operator opens the
   dashboard, **Then** summaries, status, locale, grounding, and handoff state
   are understandable without exposing secrets.
2. **Given** an open handoff, **When** the operator resolves it, **Then** the
   handoff changes once, the transition is audited, and another business cannot
   mutate it.
3. **Given** a 390-pixel viewport, **When** the dashboard is used, **Then** all
   primary controls remain reachable without horizontal overflow.

---

### User Story 3 - Reproducible Engineering Evidence (Priority: P3)

A recruiter or engineer understands the system within a short profile scan and
can run the complete synthetic demo and verification suite without paid services
or production credentials.

**Why this priority**: The repository must demonstrate delivery discipline and
architectural judgment in addition to product behavior.

**Independent Test**: Follow the quick start from a fresh clone, run all quality
gates, open the demo, and map every major README claim to code, tests, or an
explicit limitation.

**Acceptance Scenarios**:

1. **Given** a supported local environment, **When** a reviewer follows the
   quick start, **Then** the API, dashboard, seed data, and tests run without a
   third-party account.
2. **Given** the repository landing page, **When** a reviewer scans it for 30
   seconds, **Then** the problem, architecture, stack, security boundaries,
   demo path, screenshots, and limitations are discoverable.
3. **Given** the exact release commit, **When** automated and manual release
   checks run, **Then** no client identifier, personal contact detail, real
   conversation, or high-confidence secret is found.

### Edge Cases

- Duplicate provider event identifiers must not create duplicate messages or handoffs.
- Empty, oversized, or unsupported messages must fail with bounded, non-sensitive errors.
- Unapproved or cross-tenant knowledge must never be cited.
- Unsupported locale input must fall back to a documented default without inventing translation support.
- Repeated handoff resolution must be idempotent.
- Missing runtime secrets must fail closed outside explicit local demo mode.
- Dashboard API failures must show a recoverable state rather than fabricated data.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST accept a synthetic inbound message only after
  request authenticity and input bounds are validated.
- **FR-002**: The system MUST identify a demo business explicitly and enforce
  that boundary for every conversation, knowledge, handoff, and audit operation.
- **FR-003**: The system MUST reject duplicate inbound event identifiers without
  creating duplicate records or side effects.
- **FR-004**: The system MUST answer an in-scope question only from approved
  business knowledge and MUST return the supporting source reference.
- **FR-005**: The system MUST create an honest human handoff for unsupported,
  sensitive, or insufficiently grounded requests and MUST NOT promise future
  asynchronous work.
- **FR-006**: The system MUST record the response route, grounding source,
  policy outcome, and handoff transition in a tenant-scoped audit trail.
- **FR-007**: The system MUST provide synthetic English, French, and Spanish
  demo inputs while clearly labeling language support as bounded examples.
- **FR-008**: Operators MUST be able to list and inspect only their demo
  business's conversations and handoffs.
- **FR-009**: Operators MUST be able to resolve an open handoff idempotently and
  produce an audit event.
- **FR-010**: The dashboard MUST display conversation status, locale, response
  route, grounding evidence, handoff reason, and recent audit events.
- **FR-011**: The dashboard MUST remain usable at desktop and 390-pixel mobile widths.
- **FR-012**: The repository MUST include visibly synthetic seed data and MUST
  run locally without live messaging, model, database, or cloud accounts.
- **FR-013**: External provider boundaries MUST be represented by replaceable
  interfaces whose default implementations are local fakes.
- **FR-014**: The repository MUST include an accurate architecture diagram,
  security model, tested quick start, screenshots, decisions, limitations,
  license decision, and private vulnerability-reporting instructions.
- **FR-015**: Automated verification MUST cover behavior, API contracts,
  tenant isolation, signature validation, dependency risk, secret patterns,
  linting, type safety, builds, and responsive browser behavior.
- **FR-016**: Logs, errors, fixtures, screenshots, and documentation MUST contain
  no real client identifier, personal contact detail, credential, or production data.

### Key Entities

- **Demo Business**: Synthetic tenant identity, display label, default locale,
  and inbound verification configuration.
- **Conversation**: Tenant-owned interaction with messages and current status.
- **Message**: Synthetic inbound or outbound content with locale, direction,
  provider event identifier, and decision metadata.
- **Knowledge Source**: Tenant-owned, approved reference text and public-safe label.
- **Grounding Decision**: Selected source, confidence reason, response route,
  and policy outcome for one inbound message.
- **Handoff**: Tenant-owned escalation with reason, status, and lifecycle times.
- **Audit Event**: Append-only record of a security, policy, or operator transition.
- **Operator Session**: Demo-only tenant-scoped authorization context.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A fresh-clone reviewer completes the documented synthetic demo in
  10 minutes or less without creating a third-party account.
- **SC-002**: All signature, duplicate-event, tenant-isolation, grounding,
  handoff, and audit acceptance scenarios have automated tests and pass.
- **SC-003**: The complete local quality suite and protected CI finish with zero
  test failures, zero lint/type errors, and zero known production dependency vulnerabilities.
- **SC-004**: Desktop and 390-pixel browser checks report no failed application
  requests, no console errors, and no horizontal overflow on recruiter-visible pages.
- **SC-005**: Current-tree and full-history release scans report zero
  high-confidence secrets and zero non-synthetic identity/contact matches.
- **SC-006**: Every major README capability claim links to executable code,
  passing tests, a screenshot, or an explicit limitation.
- **SC-007**: An independent 30-second review identifies the product purpose,
  architecture, core security boundaries, runnable demo, and evidence links.

## Assumptions

- The showcase demonstrates architecture and behavior with synthetic data; it
  does not reproduce the private production deployment.
- Provider delivery, model generation, and managed persistence are extension
  seams rather than live release requirements.
- Demo authorization is intentionally simpler than production identity but
  still enforces tenant separation and is labeled accordingly.
- English, French, and Spanish are bounded fixtures, not a claim of general translation quality.
- Local persistence may be reset between demo runs.
