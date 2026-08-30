# Portfolio Readiness

## Recruiter signal

This repository provides direct evidence of API design, tenant-aware security, transactional persistence, deterministic AI guardrails, responsive product presentation, testing, CI/CD, documentation, and honest architectural tradeoffs.

## Release gates

The release is publishable only when the following results are exact and green on the release commit:

- Backend tests and coverage, Ruff, strict MyPy, and `pip-audit`
- Frontend component tests, ESLint, strict TypeScript, production build, and npm audit
- Desktop and 390-pixel browser checks with no console errors or horizontal overflow
- Container configuration validation and builds when Docker is available
- Current-tree and full-history public safety scans
- GitHub CI and CodeQL, zero actionable security alerts, and protected `main`
- Fresh clone verification from the public GitHub URL

## Privacy statement

The showcase was created as a clean-room implementation. Its entities and credentials are synthetic. Publication checks explicitly reject contact patterns, local user paths, common secret formats, private keys, and forbidden private source identifiers.

## Known limitations

- No real WhatsApp, CRM, LLM, or customer integration
- SQLite and local demo authentication are evaluation boundaries
- Keyword grounding demonstrates policy flow, not semantic retrieval quality
- No claim of production deployment, traffic, revenue, or client adoption

These boundaries strengthen the evidence: every visible claim is reproducible from this repository.
