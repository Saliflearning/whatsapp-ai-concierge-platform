# Security Model

## Protected assets

- Tenant conversations, approved knowledge, handoffs, and audit evidence
- Message authenticity and event idempotency
- The privacy boundary between this showcase and any non-public system

## Controls

- HMAC-SHA256 verification over the raw webhook body
- Constant-time token and signature comparisons
- Tenant-scoped reads, writes, unique event keys, and hidden cross-tenant misses
- Bounded Pydantic inputs and explicit supported locales
- Fail-closed startup unless synthetic demo mode and all demo credentials are explicit
- Deterministic grounding against approved same-tenant sources
- Human handoff for insufficient evidence and policy-sensitive claims
- Atomic message, decision, handoff, and audit persistence
- Non-root containers, lockfiles, dependency audits, CodeQL, and least-privilege CI
- Current-tree and full-history public safety scans

## Deliberate limitations

This is not a hosted production service. Demo tokens are suitable only for local synthetic use. SQLite, in-memory provider delivery, and deterministic keyword matching prioritize reproducibility and inspectability; production deployment would require managed identity, encrypted durable storage, rate limiting, observability, retention controls, and an approved provider integration.
