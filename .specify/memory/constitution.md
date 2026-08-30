<!--
Sync Impact Report
- Version: template -> 1.0.0
- Added principles: Privacy-Safe Provenance; Truthful Evidence; Test-First Delivery;
  Tenant and Security Boundaries; Recruiter Legibility
- Added sections: Public Showcase Constraints; Delivery and Review Gates
- Removed sections: none
- Templates reviewed: plan-template.md, spec-template.md, tasks-template.md (compatible;
  no template edits required)
- Deferred items: none
-->
# WhatsApp AI Concierge Platform Constitution

## Core Principles

### I. Privacy-Safe Provenance (NON-NEGOTIABLE)

The repository MUST have fresh history and MUST contain only synthetic people,
businesses, conversations, contact details, credentials, screenshots, and data.
No client code, client configuration, production export, private anecdote, or
identifier may be copied from a source repository. Architectural ideas may be
reimplemented from first principles, and their inspiration MUST be described as
production-informed rather than represented as the original production system.

### II. Truthful Evidence

Every recruiter-facing claim MUST map to executable code, a passing test, a
reviewable artifact, or an explicitly labeled design decision. Planned,
simulated, and production capabilities MUST be distinguished. The README MUST
state limitations and MUST NOT imply customer volume, business outcomes,
production usage, or ownership that the public evidence cannot prove.

### III. Test-First Delivery

Behavioral, security, tenant-isolation, and API-contract tests MUST be written
before or with their implementation. A change is incomplete until the relevant
tests fail for the missing behavior, pass after implementation, and the full
quality suite remains green. Builds, linting, dependency audits, and privacy
scans are release gates rather than optional cleanup.

### IV. Tenant and Security Boundaries

Inbound requests MUST be authenticated or cryptographically verified at their
boundary. Tenant identity MUST be explicit and enforced in every data access.
External integrations MUST be represented by narrow interfaces with local fake
adapters as the default. The system MUST fail closed for cross-tenant access,
unapproved knowledge, invalid signatures, missing secrets, and unsupported
operations. Secrets MUST come only from ignored environment files or managed
stores.

### V. Recruiter Legibility

The system MUST be understandable in a 30-second repository scan and runnable
without paid services. Documentation MUST include the problem, architecture,
security model, tested quick start, synthetic demo path, screenshots, design
decisions, tradeoffs, limitations, and verification evidence. Names and
descriptions MUST stay stable and professional; any rename or location change
MUST be propagated to the cross-AI handoff and portfolio backlog.

## Public Showcase Constraints

- The first release is a reference implementation, not a hosted multi-client SaaS.
- The showcase MUST run locally with synthetic seed data and fake provider adapters.
- A real WhatsApp, LLM, database, or cloud account MUST NOT be required for tests.
- Logs and API responses MUST avoid raw secrets and minimize personal data.
- Screenshots MUST be generated from the synthetic demo and visually inspected.
- The repository license decision, vulnerability-reporting path, dependency
  automation, secret scanning, CodeQL, and protected default branch MUST be set
  before publication.
- Source and history scans MUST report categories/counts without copying matched
  personal or secret values into documentation or handoffs.

## Delivery and Review Gates

Work proceeds through specification, plan, ordered tasks, consistency analysis,
test-first implementation, independent fresh-clone audit, and protected pull
request. Each user story MUST remain independently demonstrable. The public
release requires zero unexplained high-confidence secret findings, zero known
production dependency vulnerabilities, green backend/frontend tests, green
lint/type/build checks, responsive browser verification, accurate repository
metadata, and a second privacy/presentation review. Validated static-analysis
false positives may be dismissed only with specific evidence preserved on the
alert; rules MUST NOT be disabled merely to obtain a clean dashboard.

## Governance

This constitution supersedes local convenience and generated template defaults.
Amendments require a documented rationale, a semantic version change, an impact
review of specs/plans/tasks, and a privacy/security review. Pull requests MUST
state how they satisfy these principles. MAJOR versions change or remove a
principle, MINOR versions add or materially expand governance, and PATCH versions
clarify without changing obligations.

**Version**: 1.0.0 | **Ratified**: 2026-08-30 | **Last Amended**: 2026-08-30
