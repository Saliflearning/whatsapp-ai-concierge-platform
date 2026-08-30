# Research: Privacy-Safe Public Showcase

## Decisions

### Fresh implementation boundary

**Decision**: Implement from the public specification in a new empty repository.
Do not copy source, fixtures, migrations, screenshots, configuration, or prose
from either private WhatsApp repository.

**Rationale**: Both private current branches contain non-placeholder business
contact data, and their histories are unsuitable for publication. A clean-room
implementation gives the public repository an auditable provenance boundary.

### Runtime shape

**Decision**: Use a small web application with a Python API and TypeScript
operator dashboard. Keep all external providers behind interfaces and ship only
local fake adapters.

**Rationale**: This demonstrates backend policy/security work and recruiter-
visible product delivery while remaining runnable without paid services.

### Persistence

**Decision**: Use SQLite through a narrow repository layer for the local demo.
Create/reset the database from synthetic seed definitions.

**Rationale**: SQLite makes tenant isolation, idempotency, lifecycle state, and
audit records executable without implying production-scale managed persistence.

### Conversation intelligence

**Decision**: Use deterministic approved-knowledge matching and policy routes.
No model provider is required in v1.

**Rationale**: The showcase can prove grounding, honesty, evidence, and handoff
behavior without API keys or unverifiable model output. A model adapter remains
an explicit future seam.

### Boundary security

**Decision**: Separate signed inbound webhook simulation from operator/demo APIs.
Webhook requests use HMAC over raw request bytes. Operator routes use synthetic,
tenant-scoped demo credentials and fail closed outside local demo mode.

**Rationale**: This demonstrates both provider authenticity and tenant-scoped
authorization without exposing a production identity design.

### Dependency baseline

**Decision**: Target Python 3.12 and Node 24. Use FastAPI 0.141.1, Pydantic
2.13.5, Uvicorn 0.52.4, Next.js 16.3.3, React 19.2.8, TypeScript 5.9.x,
ESLint 9.39.x, and Vitest 4.1.11, subject to clean install and peer validation.

**Rationale**: Versions were checked against the official Python and npm package
registries on 2026-08-30. TypeScript and ESLint stay on framework-compatible
major versions instead of adopting a newly released incompatible major blindly.

## Rejected alternatives

- Publishing either private repository: rejected because current/history privacy
  cannot be proven safe for a public portfolio.
- Documentation-only architecture repository: rejected because recruiters need
  executable evidence.
- Live WhatsApp/model/Supabase dependencies: rejected because they add secrets,
  cost, fragility, and inflated production implications to the public demo.
- In-memory-only state: rejected because it hides tenant query and lifecycle
  persistence concerns that are valuable engineering evidence.
