# KuuOS → Dots MCP Events: typed GitHub wake-up contract v0.1

Status: **feature-gated candidate / SDK Python CI verified through earlier HEADs; live GitHub ingress NOT WIRED / NOT SUBSCRIBED / NOT DEPLOYED**.

## Source and epistemic boundaries

This additive Python package implements an opt-in MCP Events adapter and source-side event contract.
It is not the active OpenAI plugin, nor does it automatically register a trusted
GitHub ingress route, persistent outbox or deliver to Dots. Its test result
is not an independent Lean certification. It does not modify KuuOS main, protected
PR #1558, the existing `mcp_bridge` production server, or the Yang–Mills proof.

Code: `mcp_bridge/kuuos_mcp_bridge/github_event_contract.py`.
Checks: `mcp_bridge/tests/test_github_event_contract.py`.

It consumes GitHub Actions `workflow_run: completed` and GitHub
`pull_request: opened|synchronize` envelopes only for:

- `itakura-hidetoshi/KuuOS` (canonical target `main`);
- `itakura-hidetoshi/4d-mass-gap` (formal authoritative base
  `formal/real-hilbert-uniform-coercive-strong-limit`).

CI workflow names for KuuOS are scoped to those listed in the current v1.1
completion re-entry workflow. MGAP uses `PR Lean Fast Check` and carries exact
required job `Changed Lean fast check` and step `Run changed Lean fast check`.
The event itself contains **no job or step verification**. Those must be
independently re-fetched from GitHub MCP for the event's exact run, attempt,
head SHA and repository.

## Lifecycle (target, not yet implemented)

```
GitHub workflow_run.completed / pull_request.synchronize
  → signature-checked GitHub envelope compiler [IMPLEMENTED; ingress ROUTE NOT WIRED]
  → source-side normalized, identity-bound candidate wake-up [TESTED]
  → MCP Events events/list, events/subscribe, events/unsubscribe [OPT-IN HANDLERS TESTED; NOT DEPLOYED]
  → callback verification and encrypted PostgreSQL subscriptions [MODULES TESTED; LIVE DB NOT CONNECTED]
  → Standard Webhooks HTTPS delivery [SAFE POSTER TESTED WITH FAKES; DURABLE OUTBOX MISSING]
  → Dots「くー」wake-up [NOT CONNECTED]
  → exact GitHub MCP re-observation (HEAD/run/job/Lean step/logs/axioms)
  → CodeAI isolated candidate analysis → independent CI
  → append-only evidence receipt; no automatic merge authority
```

The source-side catalog proposal has event names
`kuuos.github.ci_completed` and `kuuos.github.pr_head_updated`. Subscription
filters require an exact repository from the two-repository allowlist.
PR subscriptions may filter by an exact positive PR number. CI subscriptions
may filter by a workflow name. A CI `workflow_run` does **not** prove its PR
identity, even if its commit SHA resembles a PR head, so this v0.1 candidate
**disallows a PR-number filter on CI events**. Reassociate PRs through fresh
GitHub MCP only.

Every generated event carries:

- stable `eventId` bound to repository and run+attempt+head SHA (or PR+action+head SHA);
- `signal_is_success_evidence=false`;
- `fresh_mcp_reobservation_required=true`;
- `merge_authority_granted=false`;
- `write_authority_granted=false`.

`conclusion=success` is a status signal, never the proof of a successful
Lean step. A failed or cancelled run may wake triage but not certify a proof.
Event IDs are stable across retries. A production sender must also persist
exact event body bytes/timestamp for retries, deduplicate on event identity,
and never generate an unrestricted notification loop from its own writes.

## Mandatory gates before any activation

1. Use an authenticated remote MCP endpoint that advertises `events` and
   supports `events/list`, `events/subscribe`, `events/unsubscribe`. The installed
   GitHub MCP connector has not exposed these methods in the current session.
2. Configure **persistent**, access-controlled subscription storage, preferably
   a dedicated PostgreSQL table; do not place callback secrets in GitHub issues,
   PR comments, unencrypted files, or the read-only continuation state.
3. Require authenticated account-bound event subscriptions and explicit filter
   authorization (including downstream read access to the target repository).
4. Verify the `whsec_` signing key (24–64 decoded bytes), signed callback
   verification challenge, strict HTTPS public destination, DNS/IP protections
   against SSRF, revalidation on every outbound connection, no redirects,
   bounded delivery/retries, 410/413 suppression, expiry and secret rotation.
   `validate_delivery_url` in v0.1 performs **only syntactic preflight** and
   is insufficient to authorize any HTTP request.
5. Add a trusted GitHub ingress route with independent signature checking,
   exact source event identity and replay protection. Preserve the existing
   KuuOS v1.1 CI completion re-entry gate and required fresh MCP recheck.
6. Validate the exact deployed commit and subscribed Dot account, run an
   actual `events/list`/subscribe/unsubscribe lifecycle and two deliveries
   (matching and excluded), and observe the Dot's independent CI verification.
   Until these are observed, report `BLOCKED_MCP_EVENT_SUBSCRIPTION`.

## Hosting and authority context (observed 2026-11-20)

- Existing `mcp_bridge` (`mcp>=2,<3`) and `kuuos-chat-work-mcp` Vercel project
  exist and should be reused rather than duplicating production servers.
- At observation, Vercel reported no configured project environment variables.
  The current bridge falls back to a read-only public GitHub Issue #1548
  backend unless PostgreSQL and OAuth are configured.
- KuuOS `workflow_run:completed` ingress v1.1 and MGAP
  `repository_dispatch` wake-up intake exist, but neither presently subscribes
  the Dot through MCP Events.
- KuuOS v1.2 has a five-minute GitHub Actions fallback poller; it is **not**
  a substitute for the requested event-triggered Dot activation.
- Do not initialize a poller checkpoint at the latest run ID merely to make
  it green; historical missing windows must remain obstructions.

## Local checks

Run the focused contract tests from the repository root (no network):

```sh
PYTHONPATH=mcp_bridge python -m pytest -q mcp_bridge/tests/test_github_event_contract.py
```

The contract-only test checks event scope, exact SHA and status, run attempt
identity, PR canonical base and fork exclusion, filter containment,
non-authority fields, callback URL syntax and Standard Webhooks signing.
No external GitHub event, remote subscription, OAuth, callback challenge,
PostgreSQL write, deployed MCP method, or Dot receipt is exercised by this test.

Source documentation: https://developers.openai.com/plugins/build/mcp-events

## Opt-in MCP server integration candidate

The same existing `mcp_bridge/kuuos_mcp_bridge/server.py` now recognizes
`KUUOS_MCP_EVENTS_ENABLED=true` and refuses activation unless OAuth, the
PostgreSQL state backend, exact OAuth subject and repository allowlists and
a base64-encoded 32-byte AES-GCM encryption key are configured:

- `KUUOS_MCP_EVENTS_ALLOWED_SUBJECTS` (comma-separated, no wildcard);
- `KUUOS_MCP_EVENTS_ALLOWED_REPOS` (subset of the two canonical repositories);
- `KUUOS_MCP_EVENTS_ENCRYPTION_KEY` (hosting platform secret; **never commit**).

Source modules:
`github_event_contract.py`, `event_subscriptions.py`,
`event_delivery.py`, `mcp_event_methods.py`,
`event_bootstrap.py`, and `github_event_ingress.py`.
Each has an isolated `mcp_bridge/tests/test_*.py` regression surface.

Source-side ingress checks HMAC-SHA256 on the exact raw GitHub event body,
accepts only allowlisted completed workflows or canonical PR head changes,
and produces a non-authoritative typed event. **It does not install a
public inbound route or perform actual notification delivery.**

The current MCP Python SDK v2 requires an explicitly tested middleware
compatibility shim to expose the `events` capability; upstream issues
document its version-sensitive serialization. Keep that shim version-bound
and do not infer remote plugin discovery from unit tests.

### Outstanding blockers

- A trusted, authenticated source-event ingress route and a durable
  idempotent delivery outbox with bounded retry/claim semantics.
- Real PostgreSQL migrations and multi-worker storage tests, dynamic
  connected-user authorization and token revocation tests.
- An exact SDK Streamable HTTP handshake with live `events` discovery,
  authenticated subscription/unsubscription and signed challenge.
- Authenticated GitHub delivery to the ingress, and one matching and
  one excluded event observed by Dots「くー」.
- Independent GitHub MCP run/job/Lean-step re-observation by the awakened
  Dot. Until then: `BLOCKED_MCP_EVENT_SUBSCRIPTION`.

## Additive hardening evidence, 2026-11-20

This section is append-only, refining earlier incomplete implementation status.
Every CI claim below belongs to its exact source HEAD, not to a later revision.

### Tested feature-gated implementation

- Signed GitHub workflow-run and canonical PR-change intake, including exact
  raw-body HMAC verification on an opt-in auxiliary ASGI route.
- MCP events/list, events/subscribe, and events/unsubscribe over real
  Streamable HTTP JSON-RPC in isolated test fixtures.
- OAuth principal/repository-bound finite subscriptions; PostgreSQL encrypted
  secrets and a bounded, leased, at-least-once delivery outbox.
- TLS hostname validation, DNS/IP pinning, restricted URLs, no redirects,
  signed callback verification, expiry, access revocation and bounded retries.
- Ten-minute old/new Standard Webhooks dual-key rotation window, with additive
  PostgreSQL migration columns and encrypted prior-secret storage.
- Required JSON-RPC error -32015 (CallbackEndpointError, challenge_failed)
  instead of generic SDK exception after failed callback verification.
- Explicit fail-closed activation bound to tested MCP Python SDK 2.3.0.
  OAuth resource-server audience validation is explicitly enabled.

### Independent GitHub Actions Python scope

- HEAD 197fc7551467b496df7bcf3ea20dbbf71ca61ef4: CI #44739934587 SUCCESS,
  isolated ASGI event discovery and subscription lifecycle.
- HEAD deab48fed0b85bb7615fe83a934eefe4e4ea670f: CI #44745034526 SUCCESS.
- HEAD f9fffe6a0841ece79df7a0eb97110246bd12cf8d: CI #44745153473 SUCCESS.
- HEAD ddc407ffc41ad69fd3c0bb680d171dd8391f3215: CI #44745554433 SUCCESS.
- HEAD d0e085d0101a53bed2862a3b4153935f118072c8: CI #44745956994
  completed SUCCESS, 185 Python tests passed; 1 inherited Pydantic/SDK warning.
- The warning remains visible. None of these runs is a Strict Lean proof audit.

### Obstructions still retained

Production project kuuos-chat-work-mcp has not been provisioned with the
necessary authenticated OAuth, PostgreSQL, signing and encryption configuration.
There is no observed live GitHub sender-to-MCP event, registered connected Dot
plugin, live events/subscribe, verified real callback, real Dot wake-up or
subsequent exact-HEAD GitHub MCP CI audit. PostgreSQL multi-worker tests remain
unperformed against a live database. Dots delivery is not assumed from a fake
ASGI callback or a green Python CI. No new PR was created, and canonical main
and protected PR #1558 have not been altered by this test branch.

This work remains BLOCKED_MCP_EVENT_SUBSCRIPTION for actual service activation.
Signing-key rotation support is candidate code until independently exercised
with a real callback. A CI green state does not grant Git merge/deploy authority.

Authoritative profile: https://developers.openai.com/plugins/build/mcp-events

## PostgreSQL integration evidence (append-only, 2026-11-20)

This section refines the earlier observation that PostgreSQL behavior was
previously only tested with isolated mocks. It does not certify Dots operation.

The initial PostgreSQL outbox SQL contained an unqualified id in an UPDATE
FROM candidate RETURNING expression, even though both target and candidate
expose id. The fixed code uses a target-qualified work.id and the rest of
the explicit target work.* column list, without weakening row-lock semantics.

The KuuOS MCP Bridge Python Validation workflow now runs a second job using
a disposable PostgreSQL 16 service container. Credentials, storage and the
database name kuuos_events_ci are test-only and not user production resources.

Exact-head outcomes:

- HEAD b352b13e33b636cd53632d2343cfce67bb9ea8b9, run #44747371895:
  completed FAILURE. Normal Python suite succeeded, four of five actual
  PostgreSQL checks passed. One test incorrectly reused a previously rotated
  signing key and assumed unauthorized unsubscribe would silently succeed.
  This was a test isolation/expectation error, not permission to weaken
  overlapping rotation or ownership checks.
- HEAD e27a0d57f0bfa0fa1690fe7bede0ef9c8619ac44, run #44747680695:
  completed SUCCESS; 185 Python passed, five integration tests skipped in the
  normal job; and five of five real PostgreSQL tests passed in the separate job.
- HEAD 4a11a1bba3d8280fd8a04f80cd1aaa1cbb83567f, run #44748114671:
  completed SUCCESS; 185 Python passed, six integrations skipped without DSN;
  six of six actual PostgreSQL tests passed. The extra test migrates a legacy
  encrypted subscription table without erasing old data and then tests key
  rotation, additive columns and encrypted previous-secret storage.

Actual PostgreSQL-tested scope: encrypted subscriptions, exact owner revoke,
outbox replay identity, transactional lease, expiry reclaim, competing workers,
and pre-rotation schema migration. No live production PostgreSQL or actual Dot
callback was accessed. The red first-run receipt stays historical.

Not completed: Production OAuth/PostgreSQL configuration, connected custom
ChatGPT MCP Events plugin, GitHub webhook to opted-in ingress, real callback
challenge, real Dot wake-up, and exact-run/job/Lean-step GitHub MCP observation
triggered by that wake-up. Status remains BLOCKED_MCP_EVENT_SUBSCRIPTION.

No new PR, canonical main mutation, protected PR mutation, production credential
retrieval, automatic deployment, or periodic polling was performed.

SQL reference: https://www.postgresql.org/docs/current/sql-update.html

## Exact-ID inline event delivery certification (2026-11-20)

Earlier candidate code claimed a globally due outbox event after a new GitHub
signal, which could incorrectly spend the wake-up on an unrelated older
pending event. The sender did not guarantee that the just-arrived CI run would
receive an immediate callback. This was a structural risk observed in the
source, not a claim that a production delivery had failed.

The new flow uses the outbox ID returned by staging the exact signed GitHub
event. In-memory and PostgreSQL stores now implement specific-ID leasing with
a bounded lease, CAS token and SKIP LOCKED for competing workers. A completed
or still-leased ID is not redelivered on a source replay. An unrelated backlog
event is neither silently substituted nor certified as the newly received
event.

When inline delivery is explicitly enabled, the HTTP ingress attempts up to
four newly staged subscription-specific IDs in one invocation. It reports
inline_attempted, remaining_not_attempted and a non-authoritative delivery
state. Beyond the cap, persisted records remain pending; a separate authorized
event-triggered retry/worker is still necessary to guarantee their delivery.
When inline delivery is disabled, a successful enqueue is not a delivery
receipt, and no periodic poller is enabled by this change.

Exact-head independently observed:

- Source HEAD: 515c4eb8c9f3f62aea2a7a935b51bc3feb26cbd4
- GitHub Actions run: 44749573255
- Workflow: KuuOS MCP Bridge Python Validation
- Status: completed / SUCCESS
- Python job: 190 passed, 8 PostgreSQL-scoped skipped, 1 warning
- Ephemeral PostgreSQL 16 job: 8 passed
- Changed files: only Python bridge runtime and tests; no Lean root, import,
  theorem, source signatures, pinned toolchain or mathlib edits
- Test scope: exact-ID priority over backlog, duplicate suppression,
  bounded fanout, exhausted/stale lease safety and competing PostgreSQL
  claimants for the exact same ID

Outstanding independent activation conditions remain: real MCP Events plugin
connection in ChatGPT, production OAuth/PostgreSQL/encryption-key provision,
a signed source event ingress and observed Dot subscription/callback receipt,
plus GitHub MCP exact-HEAD/run/job/Lean-step re-observation after that receipt.

Status: PYTHON_CI_CERTIFIED_IN_SCOPE / BLOCKED_MCP_EVENT_SUBSCRIPTION.
No production deployment, new PR, main write, or merge was performed.

## Production-compatibility and deployment-provenance audit (append-only, 2026-11-20)

This is a new, narrowly scoped observation. It does not retroactively certify
any earlier HEAD, the live Neon data, or a Dots event receipt.

### PostgreSQL major-version compatibility: independently certified

- Candidate workflow-only commit:
  `8bb127a964f768141ddcc55dcd4209615cb8bf27`.
- GitHub Actions run:
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44752493303
- Exact run/head identity: push on
  `feat/kuuos-dots-mcp-ci-event-contract-v0-1-20261120`; completed/SUCCESS.
- Three completed successful jobs: Python bridge (190 passed, 8 skipped,
  1 inherited warning); disposable PostgreSQL 16.16 (8 passed); disposable
  PostgreSQL 18.7 (8 passed).
- The change to `.github/workflows/mcp-bridge-python-validation.yml`
  retains the existing PostgreSQL 16 integration and adds a PostgreSQL 18
  matrix leg, with no Lean files or pinned mathlib touched.
- This certifies only tests against disposable CI service databases. It
  does **not** prove integration with the existing Neon production database.

### Existing production resources: independently re-observed, not activated

- GitHub canonical `main` at this audit:
  `410037a3bd8af5d78defb83e72b65f8b319caf3f`. Feature HEAD is
  not a main merge.
- Vercel project `kuuos-chat-work-mcp` exists, project
  `prj_iBLTjldWRWTAQ9hQzjlY5n4MkPg2`. Environment inventory returned
  zero configured keys and zero hidden production keys; OAuth, database
  and MCP Events runtime activation therefore cannot be certified.
- Existing production deployment
  `dpl_EcXiLn5WFnGna12Yi8oAzedmaLLH` reports READY, but its deployment
  file inventory has only the older seven-file Python package.
  Independently inspected deployed `src/kuuos_mcp_bridge/server.py` lacks
  `KUUOS_MCP_EVENTS_ENABLED`, the new event-method installation and GitHub
  event route. READY is only deployment-platform state, **not** evidence that
  this event-enabled candidate code is in production.
- Neon project `rough-meadow-33652646`, also named
  `kuuos-chat-work-mcp`, reports PostgreSQL major version 18. Its default
  `main` branch `br-summer-lake-ayfwkun3` remains `archived`. An
  existing endpoint is present and idle. No compute was started, branch
  revived, secret read, schema changed or production transaction attempted.
- Vercel integration-configuration enumeration returned 403 forbidden.
  That establishes an **inspection/permission obstruction**, not proof
  that every possible integration is absent. Project connector listing
  returned 404. Neither result certifies a configured Neon↔Vercel binding.

### Remaining separate authority and delivery gates

1. Confirm the intended production authorization boundary, reconnect or
   provision a suitable Neon database securely and configure Vercel
   environment-specific secrets without exposing any credential in GitHub
   records. Do not use disposable CI credentials.
2. Establish a reviewed, exact-source deploy of the event-capable bridge
   to the existing Vercel project, without treating the old READY deployment
   as equivalent source. Keep the backend disabled unless its OAuth,
   repository, signing, encryption, durable outbox and ingress checks pass.
3. In ChatGPT, explicitly connect the custom KuuOS MCP plugin to the correct
   authenticated account; observe `initialize`/events discovery and a real
   `events/subscribe` and signed callback challenge.
4. Observe an authentic matching event, an excluded event, the actual
   callback receipt by Dots「くー」, and the Dot's independent GitHub MCP
   exact-HEAD/run/job/step re-observation; test unsubscribe and revocation.
5. No merge, production deployment, unarchiving, polling substitution or
   unverified Dots-receipt claim is authorized by this CI.

Status: `POSTGRESQL_16_18_CI_CERTIFIED_IN_SCOPE` /
`BLOCKED_MCP_EVENT_SUBSCRIPTION`. Earlier failures and noncertified
boundaries are retained; this entry is additive, not overwriting them.


## Main v0.47 reconciliation, exact-source CI and Neon connectivity (2026-11-20)

This entry adds independent evidence to the earlier receipts without claiming
a production deployment or Dot callback. Earlier CI results apply only to
their own exact HEADs.

### Canonical reconciliation with no overwritten paths

- GitHub main HEAD during this re-entry:
  `a32f6e42733015c82a5cde7a465ecacb429675aa` (v0.47 merged).
- The previous feature branch HEAD was
  `1c59193564844dc5fdb5756568ea41628fdd7c41`.
  From their common base `410037a3bd8af5d78defb83e72b65f8b319caf3f`,
  main modified 16 paths and the feature branch modified/added 28
  distinct paths, with no path intersection.
- Two-parent non-force integration commit:
  `02af37eb547cebd8306d7e863e8560e0a545842f`.
  Parent 1 is the feature HEAD; parent 2 is the main HEAD. The new tree
  combines the unaltered source blobs from both histories.
- The feature branch is now ahead of this main, not behind; main was
  not modified by this operation.

### Server attestation and dependency pin

- `server.py` adds two non-secret runtime indicators under `/healthz`:
  `mcp_events_adapter_loaded` and `github_event_ingress_loaded`.
  They report whether feature-gated handlers were loaded in this server
  process, **not** that ChatGPT subscribed or that any callback was
  received.
- `tests/test_event_health_receipt.py` checks both off/on readings and
  ensures that verified Dot callback or GitHub CI evidence is never
  fabricated as part of the health reply.
- The deployed SDK version requirement in `pyproject.toml` and
  `requirements.txt` is fixed to `mcp==2.3.0`, matching
  `event_bootstrap.MCP_EVENTS_SDK_PIN`. A new regression test checks
  both manifests and the installed distribution.
- Exact code HEAD:
  `f949a96d79fb030315c2ae032aad613b853cf977`.
- Independent GitHub Actions:
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44755769201
  — completed / SUCCESS on that HEAD; all three jobs completed SUCCESS.
  Python: **193 passed, 8 skipped, 1 warning**.
  Disposable PostgreSQL **16.16: 8/8** and **18.7: 8/8**.
- This CI is Python/runtime and database-integration certification,
  not an independent Lean proof or an attestation of running Vercel.

### Existing Neon database: read-only live connectivity confirmed

- Existing Neon project `rough-meadow-33652646`, branch
  `br-summer-lake-ayfwkun3`, database `neondb`.
- A read-only SQL SELECT through the Neon connector succeeded and
  returned PostgreSQL `18.7 (84da7d8)`. An
  `information_schema.tables` count for the two expected MCP Events
  tables was **zero**.
- A subsequent independent branch read reported `current_state=ready`
  (previously `archived`). Thus storage archive alone is no longer
  a connectivity obstruction; this observation does **not** mean the
  schema was initialized or the service can receive events.
- No schema migrations, production event tables, role changes or data
  writes were performed. No connection-string secrets were copied.

### Vercel and Dots remain separate activation gates

- Existing Vercel project `prj_iBLTjldWRWTAQ9hQzjlY5n4MkPg2` has
  no verified event-capable deployment. At fresh observation it still
  had three historical deployments (one production and two previews);
  the new event source was **not deployed**.
- The account's Vercel Git deployment context listed no linked
  Git projects. A candidate file-based preview submission could not
  finish source collection in the available connector operation;
  **no Vercel deployment creation action completed**.
- Prior inventory of the project reported zero configured environment
  keys. The read-only live Neon SQL success must not be promoted to
  a configured Vercel database connection.
- No ChatGPT custom KuuOS MCP plugin connection, OAuth-backed
  `events/subscribe`, signed challenge, real matching/excluded
  callback, or Dot-triggered GitHub MCP exact-run/Lean-step audit
  was observed. Never substitute a scheduled poller or CI-green label
  for an actual event receipt.

Current exact implementation scope:
`MCP_PYTHON_193_PASS_PG16_18_CI_CERTIFIED`.
Production/Dot state:
`BLOCKED_MCP_EVENT_SUBSCRIPTION`.

No main merge, production deployment, new PR, credential disclosure,
or claim of end-to-end wake-up was made in this continuation.


## Vercel preview source artifact and runtime-dependency verification (2026-11-21 JST)

This append-only receipt supersedes neither the earlier failed preview nor its
corrected-build evidence. No claim below is a Dots callback receipt.

### Exact source and independent Python/PostgreSQL CI

- Candidate source HEAD:
  `3b63a2aa73939f7a34be4f3c6fd95dec79c939f5`.
- Exact GitHub Actions run:
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44810353350
  completed / SUCCESS; all three jobs completed successfully.
- Python tests: **194 passed, 8 skipped, one inherited warning**.
  Disposable PostgreSQL 16.16: **8/8 passed**.
  Disposable PostgreSQL 18.7: **8/8 passed**.
- Vercel Python build selected `pyproject.toml` dependencies (not
  automatically the `requirements.txt` fallback). The Postgres driver
  `psycopg[binary]>=3.2,<4` was promoted to the normal project runtime
  dependency without weakening the independent OAuth and Events gates.
  The additional regression test verifies both dependency manifests.

### Exact existing-project Vercel preview delivery

- Project: `kuuos-chat-work-mcp`,
  ID `prj_iBLTjldWRWTAQ9hQzjlY5n4MkPg2`.
- First file-based preview attempt `dpl_GsQfY2Jsfs4Sd4MC6ighTxgJ2gfA`:
  build ERROR with `PYTHON_ENTRYPOINT_NOT_FOUND` because the initial
  18-file request omitted `pyproject.toml`. Its failure remains recorded.
- Corrected 19-file preview
  `dpl_ADTR78tkRjTGvDGAZRhbWSAn98Mr`: READY and Python entrypoint
  resolved; it preceded the base runtime Postgres dependency correction.
- Final **preview**, not production:
  `dpl_FpSXLThDx6VGsDWacg7SCwjYuZL6`.
  URL: https://kuuos-chat-work-1gtrf0opm-itakurahidetoshi-9224.vercel.app
  Vercel status: READY; `target=null` (non-production preview),
  Python 3.12, 20 submitted runtime source files, entrypoint
  `api.mcp:app`. It was built from source HEAD above.
- File-by-file provenance: for the 20 source files under `mcp_bridge/`
  (2 ASGI API files, 16 `kuuos_mcp_bridge` Python modules,
  `pyproject.toml`, and `requirements.txt`), Vercel deployment
  file `uid` equals the SHA-1 digest of the exact source file bytes
  re-fetched from the GitHub fixed commit. **20 of 20 matched**.
  This is a source-artifact hash match, not an executable runtime test.
  The Vercel file-content retrieval can return a truncated base64
  prefix for large source files; SHA-1 UID comparisons used the full
  GitHub source and were checked against the Vercel file inventory,
  rather than falsely treating the truncated base64 as a byte mismatch.
- The Vercel project has protection enabled for previews; unauthenticated
  requests cannot serve as trusted MCP handshake tests. No verified
  `/healthz` HTTP response, OAuth token, live `events/list`,
  `events/subscribe`, or callback event was observed.

### Operational boundary retained

The existing Neon Postgres project `rough-meadow-33652646` default
branch was previously confirmed `ready` by read-only SQL.
The MCP Events tables were not yet provisioned there. The existing
Vercel project reported zero configured environment variable keys,
so no durable OAuth/PostgreSQL subscription was activated. The
custom ChatGPT KuuOS MCP plugin and Dot subscription have not been
connected. The GitHub-signed production event sender remains
unverified. No production DB write, secrets read-back, Vercel
production promotion, GitHub main merge, or new PR was performed.

Result: `PREVIEW_SOURCE_SHA1_20_OF_20_VERIFIED` and
`PYTHON_194_PG16_18_CI_SUCCESS`, while end-to-end status remains
`BLOCKED_MCP_EVENT_SUBSCRIPTION`.

Conditions remaining: protected preview HTTP/MCP handshake under
the authorized client; separated staging auth/database; ChatGPT
plugin OAuth connection; real subscription and signed challenge;
actual matching and excluded deliveries; Dot wake-up followed by
independent exact GitHub run/job/Lean-step re-observation.


## Vercel single-entrypoint signed ingress and final preview attestation (2026-11-21 JST)

This entry is additive. No new PR was opened; the canonical main,
production deployment, credentials, and Neon production data were not changed.

### Actual packaged ASGI entrypoint routing (source/CI certified)

- The Vercel Python project uses the single `pyproject.toml` entrypoint
  `api.mcp:app`. Merely shipping an auxiliary `api/github.py` file
  did not by itself prove that requests to `/api/github` reached the
  canonical signed event route.
- `mcp_bridge/api/mcp.py` now explicitly normalizes
  `/api/github` and `/api/github/` to `/github/events`, within the
  existing ASGI process. This is routing only: the event route still
  demands the exact raw-body GitHub HMAC, repository/workflow
  allowlist, and feature-gated PostgreSQL/OAuth configuration.
- A new actual-entrypoint ASGI regression combines a Streamable HTTP
  MCP initialize request, an accepted signed GitHub CI event, an
  idempotent source replay, and rejection of an invalid signature.
  It does not impersonate a real GitHub webhook or Dots callback.
- Exact code HEAD:
  `48f495a4abad1cb8eb7ed8ada945f3606e362283`.
- Independent Python/PG workflow:
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44811245700
  completed / SUCCESS, three successful jobs:
  Python **195 passed, 8 skipped, 1 warning**;
  PostgreSQL 16.16 **8/8 passed**;
  PostgreSQL 18.7 **8/8 passed**.

### Verified latest deployment source

- Latest safe nonproduction Vercel preview:
  `dpl_8gHBBXzsDu7m1pHAyD4b17r7WKQh`,
  URL https://kuuos-chat-work-i5tbu135s-itakurahidetoshi-9224.vercel.app
  with `target=null` (not promoted to production), state READY,
  Python 3.12 `pyproject.toml` build success.
- The prior preview `dpl_FpSXLThDx6VGsDWacg7SCwjYuZL6` had
  independently verified **20/20** file SHA-1 content matches
  against earlier fixed source HEAD
  `3b63a2aa73939f7a34be4f3c6fd95dec79c939f5`.
- GitHub comparison from that earlier HEAD to the latest code HEAD
  showed only `mcp_bridge/api/mcp.py`,
  `mcp_bridge/tests/test_event_asgi_transport.py`, and this
  documentary file changed. Only `api/mcp.py` belongs to the 20-file
  deployment source inventory.
- The latest Vercel deployment's file inventory has **19 unchanged
  source content SHA-1 UIDs**, and the changed `api/mcp.py`
  Vercel UID `0ae2fdba57afcc31fb0ff0e279326faf2d7deabd` exactly
  equals the newly fetched GitHub file's raw content SHA-1.
  Together with the established 20/20 predecessor match and exact
  GitHub diff, this certifies **20/20 source file identities for the
  latest preview**, subject to the stated SHA-1 hash semantics.
- Neither this source attestation nor the Vercel READY status implies
  a functioning OAuth-backed, event-enabled MCP HTTP service.

### Remaining separate obstructions

- Project `kuuos-chat-work-mcp` still had no configured Vercel
  environment variable keys at read-only observation. Existing Neon
  `neondb` read-only connectivity is available, but Neon Auth is
  not enabled for the existing default branch and event subscription
  tables were not observed.
- The protected preview has not completed an authorized live HTTP
  `initialize`/events discovery; no real ChatGPT custom plugin
  connection, OAuth-backed `events/subscribe` call, signed verification
  challenge, verified callback, GitHub source event intake, or Dot
  exact-run/Lean-step re-observation occurred.
- A green isolated ASGI test is not proof of a production network path.
  Before any activation, use least-privilege Vercel and Neon
  configuration, verify deployed OAuth/resource audience, subscription
  storage, protected signed sender, actual callback, and consumer
  authorization. Never weaken deployment protection as a workaround.

State:
`PREVIEW_SOURCE_20_OF_20_CERTIFIED` /
`PYTHON_195_PG16_18_CI_CERTIFIED` /
`BLOCKED_MCP_EVENT_SUBSCRIPTION`.


## Least-privilege real Neon staging and protected Vercel HTTP attestation (2026-11-21 JST)

This section is append-only and records the verified scope and its boundaries.
It does not retroactively certify prior HEADs or an unobserved Dots callback.

### Exact canonical and source/CI evidence

- Canonical repository `itakura-hidetoshi/KuuOS`, branch `main`:
  `a32f6e42733015c82a5cde7a465ecacb429675aa` at final independent
  GitHub MCP reobservation. No main mutation or PR creation in this work.
- Feature branch `feat/kuuos-dots-mcp-ci-event-contract-v0-1-20261120`.
  Exact latest independently CI-certified Python code HEAD:
  `976d29ec7a8887d506bff8c45d597022ba4bbc60`.
- CI [#44819929671](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44819929671):
  completed/SUCCESS, all three jobs SUCCESS. Python **203 passed,
  11 skipped, one inherited warning**. Disposable PostgreSQL **16.16:
  11/11**, **18.7: 11/11**. The preceding independently certified
  HEAD `f3021214749e3abae0fb1a404d1b3a5f467fe2bc` had
  [#44818431068](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44818431068):
  completed/SUCCESS, Python 203 passed, 10 skipped, and PG16/18
  10/10 each.
- Only Python MCP runtime, isolated tests and these appended documents
  were changed. No Lean theorem, imports, pinned toolchain, mathlib,
  public proof root or mathematical certification were altered.

### Source-level least-privilege schema boundary

- The existing stores `PostgresStateStore`,
  `PostgresSubscriptionStore`, and `PostgresOutboxStore`, and
  `EmbeddedPostgresOAuthProvider`, normally run additive DDL at
  initialization. A genuine Neon `read_write` role restricted
  to the project tables cannot run that DDL: independent errors were
  `permission denied for schema public` and `must be owner of table`.
  These errors were retained rather than broadening application rights.
- New `db_schema_mode.py` permits exactly `migrate` (unchanged
  default) and `preprovisioned` (opt-in). The latter checks required
  PostgreSQL column types, nullability, indexes, primary/unique/check
  constraints, and SELECT/INSERT/UPDATE/DELETE grants using
  **SELECT-only catalog queries**. Missing fields, weakened replay
  constraints, unknown mode, wrong namespace or revoked DML fail
  closed. Application startup performs no schema DDL in this mode.
- Real disposable PostgreSQL 16/18 integration tests create DML-only,
  non-owner roles and verify each preprovisioned store can initialize.
  The event store test exercises an encrypted subscription add/read
  and authorized unsubscribe. The OAuth test verifies the embedded
  provider's table initialization under the same no-DDL authority
  boundary. These tests do not sign a real user into ChatGPT.

### Existing Neon project: isolated real staging evidence

- Neon project `rough-meadow-33652646`
  (`kuuos-chat-work-mcp`, PostgreSQL 18.7).
- Unchanged default production branch `br-summer-lake-ayfwkun3`:
  a fresh **read-only SQL** audit found **zero** of the four MCP
  service tables; it was not migrated or granted access.
- Isolated branch
  `kuuos-mcp-events-staging-20261121`
  (ID `br-proud-queen-ayak8zsl`, parent `br-summer-lake-ayfwkun3`,
  `default=false`, ready) created with 0.25 CU min/max;
  a custom suspend timeout was rejected by the Neon account, and
  no unsupported timeout value was forced.
- Exact additive source schemas were created and catalog-verified
  **on staging only**: `kuuos_mcp_state`,
  `kuuos_mcp_event_subscriptions_v1`,
  `kuuos_mcp_event_outbox_v1`, and `kuuos_mcp_oauth`;
  required indexes and constraints present, and no real subscriptions
  or OAuth client sessions were inserted.
- Staging-only login `kuuos_events_preview_rw` was created with
  scoped `read_write` to `neondb.public`. Independent SQL proved
  SELECT/INSERT/UPDATE/DELETE access to the four tables, with
  `CREATE` on schema `public` absent. Attempts to run schema DDL
  under this role correctly returned SQLSTATE 42501. Role credentials
  were not placed in source, CI logs or the research ledger.

### Existing Vercel project: protected preview, source and live DB

- Existing Vercel project `prj_iBLTjldWRWTAQ9hQzjlY5n4MkPg2`,
  `kuuos-chat-work-mcp`. Two keys were configured for **Preview only**:
  `KUUOS_MCP_DATABASE_URL` as a protected sensitive environment
  variable pointing to the isolated staging branch's DML role,
  and `KUUOS_MCP_SCHEMA_MODE=preprovisioned`. No Production
  environment variables or original production deployment were changed.
  Never print or copy the connection string into GitHub.
- Exact candidate preview
  `dpl_DV2widqsffmPgMKCmPnNRVFyCwxd`,
  URL https://kuuos-chat-work-d5hnb19gl-itakurahidetoshi-9224.vercel.app
  was READY, `target=null` (not production), with Vercel Python 3.12.
  Its Git source metadata identifies the exact CI-certified code HEAD
  above. 21 runtime source-file identities matched the previously
  certified 21-file preview plus the one changed embedded OAuth file's
  GitHub raw SHA-1, independently compared with Vercel's file UID:
  **21/21 source matches**.
- An authenticated, Vercel-protected actual GET `/healthz` returned
  HTTP **200** / JSON:
  `ok=true`, `backend=PostgresStateStore`, `version=0`,
  `mode=read-only`, `write_ready=false`,
  `oauth_enabled=false`, `mcp_events_adapter_loaded=false`,
  `github_event_ingress_loaded=false`, `canonical_sha=null`.
  The server's health handler calls the PostgreSQL state read, so this
  is positive observed **Vercel runtime→Neon staging query** evidence,
  not merely Vercel READY or a fake HTTP client. A temporary
  deployment-scoped protected-view share link was used for the GET;
  no permanent removal of deployment protection is inferred.
- Neither a protected GET nor raw build success establishes
  MCP JSON-RPC initialize/subscribe over authenticated POST.
  No real GitHub signed ingress, callback challenge, ChatGPT
  subscription, Dots delivery, or post-event exact GitHub MCP audit
  has been observed.

### Explicit remaining activation conditions

1. Provision a reviewed staging OAuth issuer and owner/account sign-in
   with actual accepted credentials (either well-scoped embedded OAuth
   secrets and login or verified external OIDC/JWKS). Never synthesize
   an OAuth principal or treat a staging test identity as a user grant.
2. Configure the event subject/repository allowlists, a distinct
   32-byte AES-GCM key, signed GitHub ingress key, and monitored
   callback/retry policy. Do not reuse the database password for
   another cryptographic purpose or grant DDL privileges to the app role.
3. Independently exercise an OAuth-protected MCP initialize,
   `events/list`, `events/subscribe` signed challenge,
   matching and excluded GitHub events, unsubscribe and revocation.
4. Explicitly connect the custom KuuOS MCP plugin to the user's
   ChatGPT account and Dot「くー」; observe a real Dot callback and
   the Dot's independent GitHub MCP exact-source/run/job/Lean-step audit.
   No automated periodic poll or scheduled task is claimed as equivalent.

Certification: `PREVIEW_POSTGRESQL_STAGING_HTTP_200` /
`PREVIEW_SOURCE_21_OF_21` /
`PYTHON_203_PG16_18_11_OF_11_CI_CERTIFIED`.

Live Dots status remains `BLOCKED_MCP_EVENT_SUBSCRIPTION`.


## Independent canonical v0.48 reconciliation and full Python/PG revalidation (2026-11-21)

All entries below are exact-source observations. A green Python CI or a
protected Vercel health response does not authorize a GitHub merge, enable
production events, or prove a real Dots callback.

### Source and certification lineage

- Canonical `main` at reobservation:
  `c9f3987b15adb0bfd818027090efd7ae85203ee4`
  (independent Lean→Python v0.48 integration). No main mutation here.
- Previous feature HEAD:
  `fb33bb6f9ef95699e9c771f24f408cd33a114ebf`
  with independent source-scoped
  [CI #44820742255](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44820742255)
  completed/SUCCESS, Python 203 passed, 12 skipped, warning 1; isolated
  PostgreSQL 16.16/18.7 both 12/12.
- From the prior common main HEAD
  `a32f6e42733015c82a5cde7a465ecacb429675aa`,
  v0.48 main modified six files and this MCP feature modified 37
  **disjoint** paths (intersection zero). The existing feature branch
  received a two-parent, no-force exact-source integration commit
  `38e879c993ea381b6c1c0a0ee3ab85924b888b35`
  (parent 1 former feature HEAD, parent 2 canonical v0.48 main).
  Existing source blobs, Lean theorem statements, imports and pinned
  mathlib remained unchanged by the reconciliation.
- The existing `mcp_bridge/ATTESTATION.md` received an append-only
  evidence note, triggering the Python validation workflow without
  requiring an unrelated full Strict Lean run for a documentation-only
  amendment.
- **Fresh independent exact-head CI**:
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44821680848
  on HEAD `2ba239848ce8d69c4c857ef1c3bdbd5a36cc3e58`,
  `completed/SUCCESS`, three completed SUCCESS jobs:
  Python **203 passed, 12 skipped, 1 warning**;
  disposable PostgreSQL **16.16 12/12**;
  disposable PostgreSQL **18.7 12/12**.
  This is an exact integrated-source Python/PG CI receipt,
  not a fresh Strict Lean proof or production Dots delivery.

### Live deployment and database provenance (separate source scope)

- Vercel project `prj_iBLTjldWRWTAQ9hQzjlY5n4MkPg2`
  retained its original production deployment. Latest independently
  observed *preview* for MCP runtime source HEAD `fb33bb6f...`:
  `dpl_Ga9soGhAUrUJR5jvY6rTizvDKP2a`,
  https://kuuos-chat-work-1dnu3se10-itakurahidetoshi-9224.vercel.app,
  READY, non-production `target=null`. 21/21 runtime source file
  SHA-1 identities were checked against the exact source HEAD.
  The v0.48 reconciliation added **only** distinct non-MCP paths;
  it does not change this existing preview's deployed source or SHA.
  Do not assert that preview's deployment metadata equals the later
  reconciliation commit.
- Protected live Vercel GET `/healthz` was HTTP **200**,
  `backend=PostgresStateStore`, `version=0`, read-only.
  This authenticates a real **Vercel preview→Neon staging state read**.
  The returned `oauth_enabled=false`, `mcp_events_adapter_loaded=false`,
  `github_event_ingress_loaded=false` correctly retain the disabled
  activation state.
- Only the Vercel **Preview** environment has
  `KUUOS_MCP_DATABASE_URL` (sensitive) and
  `KUUOS_MCP_SCHEMA_MODE=preprovisioned`.
  Production environment variables were not modified.
  Neon project `rough-meadow-33652646` default branch
  `br-summer-lake-ayfwkun3` remained unchanged, with zero MCP
  application tables on independent read-only query. Separate staging
  `br-proud-queen-ayak8zsl` contained four source-matched tables
  and the DML-only role `kuuos_events_preview_rw` with no DDL.
- The new strict schema checker requires actual definitions of
  primary keys, composite `UNIQUE(subscription_id,event_id)`,
  attempts and allowed-state CHECK constraints. Fail-closed
  regression tests succeeded on disposable PG16 and PG18.

### Remaining external obstruction: not certified as impossible

The connected ChatGPT custom KuuOS MCP plugin / OAuth principal,
`events/list`, signed `events/subscribe` challenge, authentic
GitHub sender, receiving Dot「くー」 callback, and triggered
GitHub MCP exact repository/head/run/attempt/job/Lean-step audit
have **not** been independently observed. A package build, locally
simulated callback, or hourly poll cannot replace those receipts.

Next permitted progression: configure a verified scoped staging OAuth
issuer and cryptographic keys through protected environment secrets,
then perform true authenticated MCP HTTP POST and real subscription
lifecycle under the connected user's consent. Keep the feature
disabled on production and do not invent principals or tokens.

`CANONICAL_V0_48_RECONCILED` /
`INTEGRATED_MCP_PYTHON_203_PG16_18_12_OF_12_CERTIFIED` /
`PREVIEW_NEON_HTTP_200` /
`BLOCKED_MCP_EVENT_SUBSCRIPTION`.


## Deployment-bound OAuth and live staging MCP Events/ingress receipt (2026-11-21)

This section refines earlier obstructions with independently observed
Preview-only data. It does not certify Dots receipt or permission to merge.

### Source/CI, with explicit nonauthority

- Canonical `main` at source observation:
  `c9f3987b15adb0bfd818027090efd7ae85203ee4`. Only the existing branch
  `feat/kuuos-dots-mcp-ci-event-contract-v0-1-20261120` was modified.
- Exact feature source HEAD: `a8b960b869d28ce39dbff5a7a8588998412b9bbb`.
- Independent GitHub Actions
  [#44822866520](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44822866520):
  completed / SUCCESS at this exact source HEAD. All 3 jobs passed.
  Python **220 passed, 12 PostgreSQL-scoped skipped, 1 SDK warning**;
  disposable PostgreSQL 16.16 **12/12** and 18.7 **12/12**.
- Source hardening: `KUUOS_MCP_OAUTH_ISSUER=vercel-preview` and
  `KUUOS_MCP_OAUTH_RESOURCE_URL=vercel-preview` must be paired;
  Vercel Preview platform system variables supply a specific deployment
  hostname. Unknown/mismatched host, non-preview Vercel environment and
  production hostname fail closed. The untrusted request Host header
  cannot choose the issuer. Existing explicitly configured production
  OAuth URLs remain unchanged.
- New non-secret `/healthz` fields report only whether Vercel system
  URL was provided and which deployment environment is active. They
  are not credentials, connected-principal identity or event receipts.

### Real protected Preview HTTPS and metadata observations

- Existing Vercel project `prj_iBLTjldWRWTAQ9hQzjlY5n4MkPg2`;
  latest staging preview deployment
  `dpl_8xqpXAqCCFvLzruAc41FY45wScvS` is READY, target `null`
  (non-production), with source HEAD above and 21/21 runtime source-file
  UIDs unchanged from the previously verified same source.
- Deployment URL:
  https://kuuos-chat-work-ksyrxn8mm-itakurahidetoshi-9224.vercel.app
- Protected real HTTPS GET `/healthz`: **200**, JSON
  `ok=true`, `backend=PostgresStateStore`,
  `oauth_enabled=true`, `oauth_mode=embedded`,
  `mcp_events_adapter_loaded=true`,
  `github_event_ingress_loaded=true`,
  `write_ready=false`, `vercel_deployment_environment=preview`.
  This is a real Vercel→isolated Neon staging database state read.
- `/.well-known/oauth-protected-resource/api/mcp`:
  real HTTPS **200**, `resource=https://[same deployment]/api/mcp`,
  with `authorization_servers` resolving to that same deployment
  origin. `/.well-known/oauth-authorization-server`: **200**,
  correct issuer/authorize/token/registration URLs on that origin,
  PKCE `code_challenge_methods_supported=["S256"]`.
- GitHub ingress: actual protected HTTP **GET** to `/api/github`
  and `/github/events` returned **405 Method Not Allowed** as
  the registered route is POST-only. This establishes route existence
  and method restriction; it does **not** prove a valid signed
  GitHub POST or external callback delivery.
- Built-in OAuth, encrypted MCP Events subscriptions, and bounded
  exact-outbox-ID inline delivery were enabled only for Preview
  using a distinct, cryptographically generated staging owner
  credential, AES-GCM key and GitHub ingress HMAC secret stored
  as protected Vercel environment secrets. No secret bytes were
  written to GitHub, workbench, output or log. The application
  owner subject `kuuos-owner` is a configured internal candidate,
  **not** independently observed as a logged-in ChatGPT account.
- The Vercel Preview environment has 14 scoped variables. All
  verified configuration changes target only Preview; Production
  deployment and the default Neon database branch are unchanged.
  The isolated Neon branch `br-proud-queen-ayak8zsl` keeps four
  preprovisioned tables and a restricted DML-only application role.
- Independent staging PostgreSQL query after activation returned:
  OAuth records **0**, MCP event subscriptions **0**, outbox
  records **0**, shared state rows **0**.

### Remaining external obstruction and actual acceptance criteria

- The current Vercel Preview has deployment protection; a working
  authorized protected GET via the Vercel connector is **not**
  evidence that ChatGPT's plugin transport can complete an authenticated
  MCP Streamable HTTP POST against this URL.
- No ChatGPT custom KuuOS plugin connection, end-user OAuth login,
  authenticated `events/list`/`events/subscribe`,
  signed callback challenge, GitHub real signed POST, Dot callback
  acknowledgment or Dot-triggered exact-HEAD/run/attempt/job/Lean
  proof re-observation has been independently received.
- Source-side GitHub signing configuration remains absent; a secret
  existing only on the Vercel server does not configure the GitHub
  source sender. Do not claim that a GET 405 proves source delivery.
- Next external actions require a stable, accessible OAuth-protected
  MCP endpoint and explicit user plugin connection, as well as a
  verified signed GitHub source sender. Do not substitute a scheduled
  poll or synthetic webhook for an actual Dots MCP Events receipt.
- Treat the staging-generated OAuth owner credential as an isolated
  test secret, not a permanent user-known login. The end user must
  authenticate/consent through a securely configured identity flow
  before any subscription authority is claimed.

State: `PREVIEW_OAUTH_METADATA_HTTP_200` /
`PREVIEW_EVENTS_AND_SIGNED_INGRESS_LOADED` /
`SOURCE_PYTHON_220_PG16_18_12_OF_12_CERTIFIED` /
`BLOCKED_MCP_EVENT_SUBSCRIPTION`.


## v0.49 exact-head HTTP transport audit, live negative POST and plugin obstruction (2026-11-21)

This is an append-only, exact-source evidence entry. An HTTP rejection
proves a **boundary was enforced**, not that a ChatGPT user was authorized.

### Canonical / feature HEAD and fresh CI

- Canonical KuuOS `main` HEAD:
  `005b9ef0471428289b1fb9545f4ac212270df138` (v0.49).
- Feature reconciliation commit:
  `e924295c4feb6f73f8701bf815ec73beb4c07cd6`, retaining
  first parent `3c5c1484e7dde2aa02a959c2c58bdbf3c4d725a9`
  and second parent `005b9ef0471428289b1fb9545f4ac212270df138`.
  The six newly merged main paths were disjoint from 39 feature paths.
- Source and append-only `mcp_bridge/ATTESTATION.md` HEAD:
  `f1dccf5e1904ee3664ac30c137b9b3c437ce950a`.
- **Independent exact-source CI**:
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44825860586
  `completed/SUCCESS`, three `SUCCESS` jobs.
  Python **243 passed, 12 skipped, one inherited warning**.
  Disposable PostgreSQL **16.16 12/12** and **18.7 12/12**.
  No Strict Lean proof or independent theorem axiom audit is claimed.

### Real protected Vercel HTTP POST verified without user credentials

- Preview deployment
  `dpl_8xqpXAqCCFvLzruAc41FY45wScvS`,
  source `a8b960b869d28ce39dbff5a7a8588998412b9bbb`,
  Vercel `READY`, `target=null` (non-production).
  The HTTP probe was against this exact deployed runtime, not a
  simulated in-memory TestClient or the later v0.49 Git commit.
- An ephemeral, nonpersistent, single-vCPU Vercel Sandbox
  `sbx_Sl36nn1LeQmVtDEvxC6CAyFwyAbJ` with egress restricted to
  this one Vercel deployment host acquired a scoped Vercel temporary
  share cookie. The share URL remained private and was never recorded
  in the source, logs, audit receipt or user-visible output. The
  sandbox was stopped after the test.
- Real HTTPS GET `/healthz`: `200` JSON
  (backend from `PostgresStateStore`).
- Real HTTPS POST `/api/mcp` carrying an `initialize`
  JSON-RPC request **without** an OAuth bearer:
  `401` JSON, `WWW-Authenticate: Bearer`.
  The POST reached the MCP authentication boundary, but no verified
  bearer token was provided and no authenticated MCP result exists.
- Real HTTPS POST `/api/github` with a deliberately invalid
  HMAC-SHA256 signature: `401` JSON. This is true deployment
  network evidence of the signature check; **not** a valid GitHub
  transport event.
- Independent post-probe Neon staging SQL:
  OAuth records **0**, subscriptions **0**, outbox records **0**,
  state rows **0**. No authentic webhook event was accepted and
  no subscription was created by these negative-only probes.

### Reproducibility and authority boundaries

- Existing feature branch gained a standard-library operator script
  `mcp_bridge/preview_http_probe.py`, with an allowlisted Preview
  hostname, strict same-origin redirect handling and an ephemeral
  share URL accepted **only** through the environment.
  It checks protected health, OAuth metadata and PKCE S256, negative
  bearer challenge and invalid GitHub HMAC rejection.
- New `mcp_bridge/tests/test_preview_http_probe.py` covers the
  allowlist, cross-origin rejection, negative cases and receipt
  non-promotion. Offline synthetic responses are marked as such.
- The script returns no connection secrets or bearer tokens, and
  explicitly reports real user authorization, active subscription,
  true GitHub event, Dots callback and post-event GitHub MCP audit as
  `false`. Any output or CI success is **not** a delivery receipt.
- The current protected Vercel Preview uses a temporary share cookie
  for an external test client; this is **not** a stable public MCP URL
  suitable as the ChatGPT plugin connection. The supported connection
  is a user/authorized-workspace configured custom plugin with an
  accessible HTTPS server or Secure MCP Tunnel. The available Chat
  connection tools cannot create that user's custom plugin or
  provide their OAuth login consent.
- GitHub webhook/secrets administration was not readable or writable
  via the available GitHub MCP fetch interface. The GitHub sender
  setup remains **NO_DATA**, rather than assuming absent or configured.
  There is no evidence of a real `events/subscribe` by Dots「くー」
  and no real callback delivery.

**Limited certification**:
`REAL_PREVIEW_HTTP_POST_401_BEARER` /
`INVALID_GITHUB_SIGNATURE_401` /
`V0_49_PYTHON_243_PG16_18_12_OF_12_SUCCESS`.

**External obstruction**:
`BLOCKED_MCP_EVENT_SUBSCRIPTION`.
No canonical main merge, production deploy, production DB mutation
or new PR was performed in this stage.


## Live synthetic OAuth→MCP Events listing and pinned SDK revocation obstruction (2026-11-21)

This is an append-only record of staging-only tests. The OAuth principal
below was a deliberately generated **synthetic test owner**, not a
consenting ChatGPT user, Dots identity, or source of GitHub authority.

### Actual Vercel Preview / Neon OAuth transport success

- Existing Vercel project `prj_iBLTjldWRWTAQ9hQzjlY5n4MkPg2`.
  Preview deployment `dpl_4e9RywUVWnkDAtaZfkfJygydzyVR`,
  https://kuuos-chat-work-cpqnoihhs-itakurahidetoshi-9224.vercel.app,
  was READY with `target=null` and deployed code SHA
  `a8b960b869d28ce39dbff5a7a8588998412b9bbb`.
  This deployed runtime is **not** falsely identified as the later
  Python CI source HEAD.
- An isolated Vercel Sandbox
  `sbx_1vDD6HpdYZJTgPDzDu8Kl1uh6SQ8` used the current protected
  Preview share cookie and an ephemeral, Preview-only owner test
  secret. Network egress was allowlisted to this **one** Preview
  hostname. Neither URL secret, access token, refresh token, PKCE
  verifier, authorization code nor credentials were printed or
  written to GitHub. The Sandbox was **stopped** after observation.
- The genuine network exchange completed:
  dynamic OAuth public-client registration **201**;
  authorization request with exact `resource` and PKCE `S256`
  **302** to the server login;
  synthetic owner fixture login **302** to the registered callback;
  authorization code exchange **200** issuing an access token;
  authenticated JSON-RPC `initialize` over real HTTPS POST **200**;
  authenticated JSON-RPC `events/list` **200**, advertising exactly:
  `kuuos.github.ci_completed` and
  `kuuos.github.pr_head_updated`.
  The authenticated handshake returned the normal
  `tools`/`resources`/`prompts` capabilities plus `events`.
- The synthetic client deliberately did **not** call
  `events/subscribe`, create any callback, or claim a real GitHub
  event. A separate real protected `/healthz` GET and OAuth
  discovery query confirmed OAuth/Events/GitHub ingress were loaded
  and the issuer/resource were bound to the same fixed Preview.
- Independent Neon branch `br-proud-queen-ayak8zsl` (not the
  default branch) retained **one** synthetic OAuth access record,
  **one** public client registration and **one** refresh record.
  No event subscription or delivery outbox records existed.
  DB-reported access expiry was `2026-11-20T23:16:28Z` and refresh
  expiry was `2026-12-20T22:16:28Z`; **expiry metadata is not
  evidence of revocation or a sweep of expired records**.

### HTTP revocation failure and source-backed diagnosis

- During the true staging OAuth flow, public client `POST /revoke`
  without `client_secret` returned **HTTP 400**
  `invalid_request`. This was not reported as a success or silently
  cleared from the audit.
- Upstream MCP Python SDK issue
  https://github.com/modelcontextprotocol/python-sdk/issues/3508
  describes `client_secret: str | None` without a default, which
  Pydantic 2 treats as **required even for public clients**. This
  is consistent with the observed request/response, though the
  pinned parser must be independently tested to claim that exact
  code-level cause.
- Existing bridge `mcp==2.3.0` remained pinned to preserve the
  explicitly version-bound MCP Events capability shim. No
  uncontrolled SDK upgrade or production monkeypatch was applied.
- Exact-source Python/PG CI
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44828011770
  (`323f7e5020ccd9b11d8bccf598922d306404d89d`)
  completed/SUCCESS: Python **245 passed / 12 skipped / 1 warning**;
  PG16.16 and PG18.7 **12/12** each. Added regressions show the
  public-client parser requires explicit empty `client_secret`,
  while the embedded provider invalidates the associated access/
  refresh token pair.
- A further independent CI
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44828362764
  at exact HEAD `943eb7e89829b7884ad40d9c5bd5f115d7260d7d`
  completed/SUCCESS: Python **245 passed / 13 skipped / 1 warning**,
  disposable PG16.16 and PG18.7 **13/13** each.
  Its additional test executes the actual SDK `/revoke` HTTP route
  on a disposable PostgreSQL database with an explicitly empty
  `client_secret`, and verifies access/refresh pair invalidation.
- A subsequent external retry of the synthetic revocation
  handshake was blocked by the execution environment, hence
  **no real Preview token revocation is certified**. Do not claim
  the remaining staging test credentials were revoked; their raw
  values were not saved for reuse.

### External authority boundary

The observed true authenticated `events/list` is a real
**staging synthetic principal**, not the actual user's OAuth consent.
The protected Vercel Preview is not established as a stable public
ChatGPT custom MCP plugin connection. No actual connected plugin,
Dots「くー」 `events/subscribe`, callback verification, GitHub
real signed push, event callback receipt or Dot-initiated independent
GitHub MCP exact-HEAD/run/attempt/job/Lean-step validation exists
in this evidence. GitHub webhook administration still has
`NO_DATA` because the available GitHub MCP connector cannot read
its secrets or webhook settings.

The correct operational distinction is:

`REAL_SYNTHETIC_OAUTH_PKCE_MCP_EVENTS_LIST_CERTIFIED` /
`DISPOSABLE_PG16_18_HTTP_REVOKE_13_OF_13_CI_SUCCESS` /
`REAL_PREVIEW_TOKEN_REVOKE_UNCERTIFIED` /
`DOT_SUBSCRIPTION_AND_CALLBACK_NOT_OBSERVED`.

Production deployment, Production environment variables,
canonical GitHub main, and Neon default branch were not changed.
