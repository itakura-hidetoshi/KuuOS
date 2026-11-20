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


## v0.48 canonical reconciliation and least-privilege PostgreSQL staging (2026-11-21)

This entry is additive. It supersedes no older failed receipt. The source,
runtime/CI, Git merge, Vercel deployment and actual Dots callback are separate
assertions, with authority limited to their independently observed scope.

### Latest certified source before canonical v0.48 integration

- GitHub source `fb33bb6f9ef95699e9c771f24f408cd33a114ebf`:
  independent [Python and PostgreSQL CI #44820742255](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44820742255)
  `completed/SUCCESS` on the exact HEAD, all three jobs success.
- Python 203 passed, 12 PostgreSQL-scoped skipped, one known SDK warning;
  disposable PostgreSQL 16.16 and 18.7 each 12/12 passed.
- The code checks a preprovisioned schema's columns, nullability,
  indexes, non-owner application DML grants and **exact catalog-reported
  definitions** of primary/unique/CHECK constraints. In particular,
  `UNIQUE(subscription_id, event_id)` must not silently change its
  columns or order while retaining its name. Invalid constraints fail closed.
- The non-privileged staging DB role is neither a database owner nor
  permitted schema DDL. No application-side migration or automatic grant
  elevation is substituted for valid authority.

### Independent real preview and Neon observation

- Vercel existing project `kuuos-chat-work-mcp`, protected **Preview**,
  deployment `dpl_Ga9soGhAUrUJR5jvY6rTizvDKP2a` built READY from the
  exact candidate SHA above; no production promotion.
- Verified **21/21** source file content SHA-1 identities via Vercel file
  UIDs, five newly changed GitHub blobs and 16 unchanged previously verified
  runtime file UIDs.
- The protected preview's actual HTTPS GET `/healthz` returned HTTP 200
  and observed `backend=PostgresStateStore`, `version=0`,
  `mode=read-only`, with OAuth and MCP Events disabled. This exercises
  a real Vercel→isolated Neon `neondb` state read, **not** an authenticated
  MCP POST, a webhook callback, or a Dot notification.
- Preview-only environment variables: protected staging database URL
  for the DML-only role, and `KUUOS_MCP_SCHEMA_MODE=preprovisioned`.
  The Neon staging branch is `br-proud-queen-ayak8zsl`, derived from
  default `br-summer-lake-ayfwkun3`; the staging branch holds four
  preprovisioned tables. Independent SQL reconfirmed **zero** KuuOS MCP
  service tables on the original/default database branch. Production is
  unchanged.

### Subsequent canonical reconciliation, not an authorization grant

- Canonical main advanced independently to
  `c9f3987b15adb0bfd818027090efd7ae85203ee4` (Lean→Python v0.48).
- Compared from common prior main
  `a32f6e42733015c82a5cde7a465ecacb429675aa`:
  six canonical v0.48 changed files and 37 feature-branch changes had
  **zero overlapping paths**. They were combined into the existing
  feature branch's two-parent commit
  `38e879c993ea381b6c1c0a0ee3ab85924b888b35`,
  preserving both original code source histories. The canonical main
  and protected PR were not mutated.
- Old Python CI success on `fb33bb6f` **does not certify** the new
  two-parent reconciliation commit. Obtain an independent, completed,
  exact-source Python/PG CI before certifying that reconciled HEAD.
  This documentation edit intentionally triggers the existing Python
  bridge-only validation workflow; it must not trigger Strict Lean
  for an unrelated documentation change.

### Uncertified external subscription boundary

No production OAuth, real ChatGPT custom KuuOS MCP plugin connection,
`events/subscribe` with a real authenticated principal, signed callback
challenge, real GitHub matching and excluded event receipt, actual Dot
wake-up or post-wake GitHub exact-run/job/Lean-step audit has been
observed. Any fake or locally mounted callback is test evidence only.

Persist `BLOCKED_MCP_EVENT_SUBSCRIPTION` until actual connected
subscription/callback delivery and independent Dot audit are observed.
