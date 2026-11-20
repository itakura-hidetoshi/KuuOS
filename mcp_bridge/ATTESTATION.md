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


## Reproducible protected Preview POST and canonical v0.49 reconciliation (2026-11-21)

This append-only audit distinguishes independent **external HTTP evidence**,
Python/PG CI, GitHub canonical history, and authority for real ChatGPT events.
The isolated infrastructure checks below do not authorize a Dot subscription.

### Real protected HTTP transport negative tests

- Observed exact Preview deployment:
  `dpl_8xqpXAqCCFvLzruAc41FY45wScvS`,
  source `a8b960b869d28ce39dbff5a7a8588998412b9bbb`,
  with Vercel `READY` and protected application OAuth/events enabled.
- An ephemeral one-vCPU Vercel Sandbox
  `sbx_Sl36nn1LeQmVtDEvxC6CAyFwyAbJ` was created with a network
  allowlist for **only** this preview host, no persistence, and bounded
  runtime. A temporary, Vercel-scoped share cookie was used to reach the
  application through the platform's Preview protection; its token and
  any staging credential were not printed or committed.
- An actual external HTTP GET `/healthz` returned **200 JSON**.
- An actual HTTP **POST** `/api/mcp`, JSON-RPC `initialize`, with no
  OAuth bearer returned **401 JSON**, including
  `WWW-Authenticate: Bearer`. This certifies reachability of the
  application's OAuth rejection boundary, **not** authenticated MCP
  initialization or event discovery by ChatGPT.
- Actual HTTP **POST** to `/api/github`, using a deliberately invalid
  HMAC-SHA256 header, returned **401 JSON**. This certifies
  fail-closed signature rejection through the deployed route,
  **not** a valid signed GitHub event.
- The share-link root GET returned 404 (no application root route),
  and the subsequent authenticated Preview-layer health and POST
  requests succeeded or rejected at the application boundary as
  specified. Do not misrepresent the benign root 404 as a transport
  failure.
- Independent Neon staging SQL after the probe showed zero OAuth
  records, event subscriptions, outbox records and saved state rows;
  no synthetic subscription or valid GitHub delivery was written.
- The Sandbox session was explicitly stopped. No running background
  monitor or task is implied.

### Repeatable least-authority audit

- `mcp_bridge/preview_http_probe.py` is a standard-library-only
  probe that reads a temporary Vercel share URL solely from
  `KUUOS_MCP_PREVIEW_SHARE_URL`; it **never echoes or saves** it.
  It accepts only the exact known project Preview hostname pattern
  and rejects cross-origin redirects, userinfo, extra URL arguments,
  non-HTTPS, or invalid share query strings.
- It checks health, protected-resource OAuth discovery, authorization
  metadata issuer + `S256`, anonymous MCP initialize `401 Bearer`,
  and invalid GitHub signature `401 unauthorized_event`.
  Its output explicitly marks OAuth user authorization, subscription,
  genuine GitHub event, Dot callback and independent GitHub re-check
  as **false**. The probe never creates an OAuth client or sends an
  authorized GitHub event.
- The companion `tests/test_preview_http_probe.py` uses isolated
  simulated HTTP responses to test URL restrictions, negative
  security conditions and the no-authority receipt. It cannot
  replace the real Sandbox observations above.
- Independent exact-head Python/PG run
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44825344783
  was `completed/SUCCESS` at
  `3c5c1484e7dde2aa02a959c2c58bdbf3c4d725a9`,
  with three SUCCESS jobs: Python **243 passed, 12 skipped,
  1 inherited warning**; disposable PostgreSQL **16.16 12/12**
  and **18.7 12/12**.

### Canonical v0.49 synchronization (do not reuse old CI)

- GitHub canonical `main` independently advanced from
  `c9f3987b15adb0bfd818027090efd7ae85203ee4` to
  `005b9ef0471428289b1fb9545f4ac212270df138`,
  adding six Lean→Python v0.49 files. Its six change paths are
  disjoint from the MCP feature changes; no overwrite or theorem
  replacement was required.
- Existing MCP feature branch reconciliation commit
  `e924295c4feb6f73f8701bf815ec73beb4c07cd6`
  has first parent `3c5c1484e7dde2aa02a959c2c58bdbf3c4d725a9`,
  second parent canonical main `005b9ef...`, and the combined
  exact file tree. Main was **not** modified.
- Previous code CI `#44825344783` belongs **only** to the
  preceding HEAD. Run and inspect new completed Python/PG CI
  with exact reconciled HEAD after this append-only source note,
  before claiming v0.49-integrated certification.

### Real event connectivity still not established

The current Vercel Preview remains protected by platform SSO;
its temporary share link is not a stable public MCP address for the
ChatGPT plugin. ChatGPT's supported path is to connect the server
through **Plugins → Add custom MCP server** with an authorized
public HTTPS endpoint, or an approved **Secure MCP Tunnel**. A
user/workspace connection and actual OAuth consent are external
explicit actions, not inferred from Vercel project ownership.

GitHub's webhook administration/secrets API was not accessible
through the available GitHub MCP fetch tool. Treat the source
sender configuration as **unverified**, not proven absent. An
MCP source can only publish user-requested events after a genuine
authenticated ChatGPT `events/subscribe`, callback verification,
matching source event, signed delivery and the Dot's exact independent
GitHub MCP re-observation.

Do not create a pseudo-subscriber, publish fake CI success,
remove deployment protection or promote Preview to Production to
paper over this external authority gate.

`PREVIEW_REAL_HTTP_POST_AUTH_BOUNDARY_CERTIFIED` /
`INVALID_GITHUB_HMAC_401_CERTIFIED` /
`V0_49_RECONCILED_SOURCE_NEEDS_FRESH_CI` /
`BLOCKED_MCP_EVENT_SUBSCRIPTION`.
