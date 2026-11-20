# KuuOS MCP deployment attestation

`kuuos-mcp-attest` verifies the public, non-secret `/healthz` receipt of a deployed KuuOS Chat–Work MCP bridge. It is intentionally independent of the deployment provider and uses only the Python standard library at runtime.

The verifier fails closed unless the health response contains the full contract:

- `ok`
- `mode`
- `backend`
- `version`
- `oauth_enabled`
- `oauth_mode`
- `write_ready`
- `canonical_sha`

It always requires an exact expected canonical SHA. Optional expectations can additionally pin the backend, OAuth mode, OAuth enablement, read/write mode, and write readiness.

Example for a staging deployment that has PostgreSQL and embedded OAuth configured but deliberately keeps write tools disabled:

```bash
kuuos-mcp-attest 'https://staging.example' \
  --expected-canonical-sha '<exact-canonical-sha>' \
  --expected-backend 'PostgresStateStore' \
  --expected-oauth-enabled true \
  --expected-oauth-mode embedded \
  --expected-mode read-only \
  --expected-write-ready false
```

The verifier also enforces internal consistency independent of the requested expectations. Embedded OAuth cannot attest against a non-PostgreSQL backend. `write_ready=true` requires read-write mode, PostgreSQL, and OAuth. OAuth enablement and OAuth mode must agree. The state version must be a non-negative integer.

Remote attestation requires HTTPS. Plain HTTP is accepted only for localhost/loopback when `--allow-http-localhost` is explicitly supplied. Credential-bearing URLs, cross-origin redirects, non-JSON responses, and oversized health receipts are rejected.

The command emits a small JSON receipt containing only the health URL and the non-secret observed fields. On any mismatch it exits non-zero and writes a compact JSON error receipt to stderr.

## Staging observation workflow

`.github/workflows/mcp-staging-attestation.yml` observes the current public Replit staging endpoint from a GitHub-hosted runner whenever MCP bridge code changes. The observation is deliberately non-gating: a stale or temporarily unavailable staging deployment is recorded without invalidating repository code CI. On pull requests the expected canonical SHA is the PR base SHA, so the check asks whether staging is still synchronized with the authoritative base rather than with unmerged code.

The same workflow can be dispatched manually with an arbitrary HTTPS base URL and expected SHA. Production promotion should still require a human- or automation-reviewed successful attestation before write enablement.

## Dots MCP Events activation: additional source-bound gates (2026-11-20)

The legacy `/healthz` verifier above does **not** attest MCP Events
deployment or delivery. In particular, `canonical_sha` is a declared
canonical source reference, not proof that the deployed Python application
contains the new feature-gated modules. Treat deployment source, OAuth,
PostgreSQL, subscription, and Dot callback as independent conditions.

The candidate source is maintained only on
`feat/kuuos-dots-mcp-ci-event-contract-v0-1-20261120`.
After a non-overwriting two-parent reconciliation with canonical
`main=a32f6e42733015c82a5cde7a465ecacb429675aa`, the branch contains
both the existing v0.47 work and the opt-in event bridge. This repository
operation does not release the code or activate a subscription.

Before preparing a deployment, obtain **independent exact-HEAD CI** on
the reconciled branch. The prior completed successful
[CI #44752493303](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44752493303)
certifies only source HEAD
`8bb127a964f768141ddcc55dcd4209615cb8bf27`
(Python 190 passed/8 skipped/1 warning; PostgreSQL 16.16 and 18.7 each
8 passed). It is not a green receipt for the later reconciliation.

A separate **deployed-code inventory** must confirm that the real Python
artifact includes `event_bootstrap.py`, `event_subscriptions.py`,
`event_outbox.py`, `github_event_route.py`,
`mcp_event_methods.py` and `api/github.py`, and that installed
`mcp` equals the feature-gated adapter pin `2.3.0`. Compare exact
source SHA and artifact provenance; do not infer this from Vercel READY,
a matching project name or a `canonical_sha` field alone.

The existing Vercel production project `kuuos-chat-work-mcp`, at
the most recent read-only observation, had zero configured env keys
and a READY **legacy seven-file deployment** lacking the new event
handlers. The existing Neon project with that name has a PostgreSQL 18
default branch reported as `archived`; its production state and
connection were **not** certified by disposable CI PostgreSQL tests.
Do not use CI DB credentials as production secrets or silently switch
to a different database. Existing Vercel integration visibility returned
403 forbidden; retain this as an inspection obstruction.

Before enabling `KUUOS_MCP_EVENTS_ENABLED` or
`KUUOS_MCP_GITHUB_INGRESS_ENABLED` in any production deployment,
review an authenticated and encrypted PostgreSQL backend, actual OAuth
issuer/resource audience and allowed subject/repository ACLs, protected
ingress signing key, AES-GCM key, exact verified build, bounded inline
delivery policy and durable retry worker. Keep write tools disabled
unless separately authorized. Neither feature flag permits bypassing
the Dots plugin connection or callback verification.

The final acceptance test is **end-to-end**:
authenticated MCP initialize with events discovery; actual subscribed
Dots account and signed verification challenge; one matching GitHub
CI signal delivered once, one excluded signal not delivered; Dot's
independent GitHub MCP re-fetch of exact repository/HEAD/run/attempt/
job/Lean step; revocation and unsubscribe. Every callback is a
non-authoritative wake-up; only the independent re-fetch can certify
CI evidence. Do not claim real-time monitoring or merge authority from
a green Python job.

**Until these conditions are observed:**
`BLOCKED_MCP_EVENT_SUBSCRIPTION`. No automatic merge, secret mutation,
database reactivation, production deployment, or fake callback is
authorized by this note.
