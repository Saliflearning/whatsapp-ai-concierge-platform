# ADR 0004: Provider interfaces with a local adapter

**Status:** Accepted

Conversation orchestration depends on a transport protocol. The bundled fake adapter performs no network access, keeping tests deterministic and credentials unnecessary while making a later approved provider adapter an isolated change.
