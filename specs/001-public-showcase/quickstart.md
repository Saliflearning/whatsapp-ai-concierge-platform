# Quick Start Contract

The final release MUST support this sequence from a fresh clone:

1. Copy `.env.example` to `.env` and keep the supplied clearly synthetic demo values.
2. Create a Python 3.12 virtual environment and install backend development dependencies.
3. Run the seed/reset command and start the API.
4. Install exact Node 24 dependencies and start the dashboard.
5. Open the dashboard, submit one grounded message and one handoff message,
   inspect evidence/audit events, and resolve the handoff.
6. Run backend tests/lint/typecheck/audit and frontend tests/lint/typecheck/build.
7. Run the redacted public-safety scanner.

No WhatsApp, model, database, or cloud account may be required. Exact commands
will be finalized and executed during implementation; a fresh-clone audit must
confirm the sequence before publication.
