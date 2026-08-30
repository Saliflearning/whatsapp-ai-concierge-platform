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

## Verified release evidence — 2026-08-30

- Public repository: `Saliflearning/whatsapp-ai-concierge-platform`
- Verified implementation/dependency commit: `07e7f127ab3483fdd790a1c9fdf8fab1f2c7e0bf`
- Backend: 22 tests passed; 94.40% branch-aware coverage; Ruff and strict MyPy passed
- Dependencies: `pip-audit`, full npm audit, and production npm audit reported zero known vulnerabilities
- Frontend: component tests, ESLint, strict TypeScript, and Next.js production build passed; `/` and `/demo` rendered as static routes
- Browser: desktop and 390-pixel mobile checks had zero console errors and no horizontal overflow; synthetic screenshots are versioned in `docs/assets/`
- Delivery: backend, frontend, and container GitHub checks passed; CodeQL passed for Python and JavaScript/TypeScript
- Privacy: current tracked tree and complete Git history passed the redacted public safety scanner; a separate public fresh clone repeated both scans and all local quality gates
- GitHub security: protected `main`, secret scanning and push protection, Dependabot security updates, and private vulnerability reporting are enabled
- Alert state at verification: zero open CodeQL, secret-scanning, or Dependabot alerts

The release record intentionally names the verified implementation commit. A later documentation-only merge may advance `main` without changing this tested implementation tree.
