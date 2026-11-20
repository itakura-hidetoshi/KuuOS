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


## Real signed challenge over external HTTPS with synthetic MCP subscription (2026-11-21 JST)

This appendix preserves the exact **staging-only** provenance of an actual
signed callback challenge. It certifies real network plumbing, **not**
the existence of a ChatGPT/Dots subscription, a genuine GitHub sender,
or Lean/CI truth from the event payload.

### Starting conditions and source scope

- Canonical `main` at independent GitHub MCP reobservation:
  `005b9ef0471428289b1fb9545f4ac212270df138`. No main merge, new PR, production Vercel
  release or Neon default branch change occurred.
- Existing feature branch
  `feat/kuuos-dots-mcp-ci-event-contract-v0-1-20261120`.
  Last independent Python/PG CI-certified code-and-test HEAD before
  this documentation append:
  `943eb7e89829b7884ad40d9c5bd5f115d7260d7d`,
  [CI #44828362764](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44828362764):
  `completed/SUCCESS`, Python **245 passed / 13 skipped / 1 warning**,
  PostgreSQL 16.16 **13/13**, PostgreSQL 18.7 **13/13**.
- The actual Preview application runtime was deployed from earlier
  source HEAD `a8b960b869d28ce39dbff5a7a8588998412b9bbb`;
  later repository tests and notes are not falsely represented as
  that deployment's source.
- Existing Vercel project
  `prj_iBLTjldWRWTAQ9hQzjlY5n4MkPg2`. Exact tested Preview
  `dpl_J7Hsag13ZnsXx2uoQzGP6V9zZkxZ`, READY,
  `target=null`, URL:
  https://kuuos-chat-work-ffzh9r825-itakurahidetoshi-9224.vercel.app
- Embedded staging OAuth owner secret was rotated only in the
  Preview-sensitive environment slot. The same fresh test credential
  was placed in an ephemeral Vercel Sandbox file with mode 0600.
  No OAuth secret or bearer token was written to GitHub,
  the workbench, transcript receipts or external logs.

### Real external HTTPS callback verification — independent sandbox

- Created a non-persistent, single-vCPU Vercel Sandbox
  `kuuos-mcp-events-callback-20261121-c`,
  session `sbx_DwtRSYEqxVN8M4bCRvXA1d20K6Ej`,
  with a short-lived HTTPS receiver exposed at
  `https://sb-3r0zv1g25qqg.vercel.run/callback`.
  Outbound sandbox network permission was restricted to **only**
  the specific Preview application origin. The receiver accepted
  `POST /callback` only after validating
  `webhook-id`, timestamp freshness, the one-use
  `type=verification` challenge, and the standard
  `webhook-signature` HMAC-SHA256 using its own isolated
  `whsec_` test key. The key was stored only in the
  ephemeral sandbox (0600), not in the repository.
- An initial attempt returned local socket connection refused
  before OAuth initialization. This was a sandbox receiver
  process-lifetime obstruction, **not** an MCP subscription
  rejection. The process was restarted, a local HTTP GET
  `127.0.0.1:8765/health` returned 200, and the outbound
  allowlist was updated from the prior Preview hostname to the
  new exact Preview hostname before retrying.
- The **retry** used actual HTTPS between the sandbox and the
  protected Vercel Preview, with the deployment-scoped
  short-lived Vercel share cookie (not a public MCP URL).
  The network results were:
  - Synthetic OAuth public-client registration: **201**.
  - OAuth authorization and synthetic owner login: **302/302**.
  - Exact `resource` + PKCE `S256` token exchange: **200**.
  - Authenticated MCP `initialize`: **200**, `events`
    capability advertised.
  - Authenticated MCP `events/list`: **200**, including
    `kuuos.github.ci_completed`.
  - Authenticated `events/subscribe`: **200**, actual
    `sub_` receipt for a synthetic filter targeting the
    allowlisted `itakura-hidetoshi/KuuOS` repository.
  - Vercel's callback verifier opened a real outbound
    HTTPS connection to the sandbox's public receiver,
    sent a signed `type=verification` challenge and
    received the exact echoed challenge. The sandbox
    reported **one** signature-verified challenge.
  - Authenticated `events/unsubscribe`: **200**, successful.
  - `POST /revoke` including the explicitly empty
    `client_secret` required by the pinned MCP SDK
    public-client parser: **200**.
  - A subsequent MCP request using the **revoked** new access
    token returned **401**.
- This is a **synthetic subscriber test**. The receiver is
  a temporary sandbox, **not** a ChatGPT callback URL, and
  the event was a verification control message, **not** an
  authentic GitHub completed-CI signal. The application did
  not send a fake completed-CI event into Dots.
- The sandbox was explicitly stopped, with `persistent=false`.
  No daemon, active external callback receiver, or real user
  monitor was left running by this test.

### Independent post-test Neon observation

- Isolated PostgreSQL 18.7 staging branch
  `br-proud-queen-ayak8zsl` was queried under
  the DML-only role after unsubscribe and revoke.
- **0** event subscriptions and **0** outbox records;
  the synthetic test subscription was not left active.
- **1** access and **1** refresh record remain from
  **earlier synthetic OAuth testing**, not from the
  newly revoked test. **2** synthetic OAuth client
  registrations now exist. These historic records have
  not been treated as revoked or deleted. There was
  no destructive SQL cleanup.
- Original/default Neon branch `br-summer-lake-ayfwkun3`
  still had **0** of the four MCP application tables
  on independent read-only query.

### Remaining outer authentication and event-source obstruction

A genuine ChatGPT/Dots「くー」subscription is **not** present.
Official custom MCP server connections are workspace/plan
controlled and require an accessible supported MCP endpoint
or an approved Secure MCP Tunnel and the user's own
OAuth consent. The protected Preview share link and
synthetic owner login are **not** substitutes for those
authorizations. GitHub source-side genuine signed event
configuration remains `NO_DATA` under current GitHub MCP
admin tool limitations.

The next true end-to-end gate remains: actual user-connected
MCP plugin → Dots `events/subscribe` and signed challenge
→ authentic matching GitHub source delivery → Dots callback
receipt → independent GitHub MCP re-observation of exact
repo/HEAD/run/attempt/job/Lean step. Until those receipts
arrive, do not claim background real-time monitoring.

State:
`SYNTHETIC_SIGNED_CALLBACK_HTTPS_CERTIFIED` /
`SYNTHETIC_SUBSCRIBE_UNSUBSCRIBE_REVOKE_CERTIFIED` /
`DOT_REAL_SUBSCRIPTION_UNOBSERVED` /
`GITHUB_AUTHENTIC_SOURCE_UNOBSERVED`.


## Actual staging synthetic signed source → outbox → HTTPS delivery and replay controls (2026-11-21)

This is a strictly append-only record of staging **synthetic** external
transport evidence. The genuine GitHub event origin, user's ChatGPT
custom-plugin connection and Dots callback remain separate obstructions.
An accepted synthetic signal is **never** proof of the claimed CI result.

### Independent source and runtime context

- Canonical `main` at independent GitHub MCP observation:
  `005b9ef0471428289b1fb9545f4ac212270df138`, unchanged by this test.
- Existing feature branch `feat/kuuos-dots-mcp-ci-event-contract-v0-1-20261120`, documentation starting HEAD
  `364ec0837dfe490baa257a79f779ca96f7f91f7c`; the previously independently green CI
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44828362764
  is **completed/SUCCESS** at code/test HEAD
  `943eb7e89829b7884ad40d9c5bd5f115d7260d7d`, Python **245 passed, 13 skipped, warning 1**,
  disposable PostgreSQL 16.16 and 18.7 each **13/13**.
  This network test did not produce new Lean theorem certificates.
- Real Vercel **Preview** application:
  `dpl_DAozdncjzpsCv1W1YpZDPDsmZiRM`, READY,
  `target=null` (not production),
  `https://kuuos-chat-work-bmb9yye3g-itakurahidetoshi-9224.vercel.app`.
  Deployed source HEAD **`a8b960b869d28ce39dbff5a7a8588998412b9bbb`**,
  not the later doc/code HEAD. Its runtime inventory was 21 exact
  source files reused from the previously source-certified Preview.
- The existing Neon project `rough-meadow-33652646` staging branch
  `br-proud-queen-ayak8zsl` (PostgreSQL 18.7) was used with the
  DML-only role `kuuos_events_preview_rw`. The default Neon branch
  `br-summer-lake-ayfwkun3` was not modified.
- For this test only, two **distinct** 128-character
  cryptographically generated secrets for the synthetic OAuth owner
  and GitHub HMAC source were rotated in Vercel's
  **Preview-only sensitive environment variables**.
  The exact same synthetic inputs were supplied privately to an
  ephemeral sandbox. No token, share key, signing secret or
  callback `whsec_` key was copied into the repository,
  workbench, transcript or result receipt.
- A nonpersistent, one-vCPU Vercel Sandbox
  `kuuos-events-signed-delivery-20261121-d`, session
  `sbx_2odIEyjdX4CkZg96Id5TpXIOEFDZ`,
  exposed its temporary HTTPS callback at
  `https://sb-6gunhh4z5b4z.vercel.run/callback`. Egress
  from the sandbox was restricted to the exact application
  Preview hostname. Its own signing key was generated and stored
  only in an ephemeral private file; callbacks were rejected
  unless signed using the Standard Webhooks HMAC-SHA256
  of exact event ID, timestamp and payload bytes.

### Successful actual external HTTPS exchange

The real Preview server, rather than a simulated ASGI TestClient,
returned the following to a synthetic, specifically permitted
OAuth principal and source-event test:

1. Protected Preview health GET **200**, with OAuth, MCP Events
   and separately gated GitHub ingress all loaded.
2. OAuth public client registration **201**, authorization/login
   redirects **302/302**, PKCE authorization-code token exchange
   **200**, authenticated MCP `initialize` **200**, and
   `events/list` **200** showing two approved event names.
3. `events/subscribe` **200**, with a `sub_` receipt
   filtering the allowlisted `itakura-hidetoshi/KuuOS`
   repository and workflow `KuuOS Runtime Full Check`.
   Exactly one signed verification challenge was received,
   verified and echoed over real Sandbox HTTPS before
   the subscription was persisted.
4. A deliberately **synthetic** `workflow_run` notification,
   signed by the test-only Vercel-preview HMAC key, with
   `conclusion=failure`, a synthetic run ID and artificial
   40-character SHA, reached `POST /api/github`.
   HTTP **202**, `accepted=true`, `enqueued=1`,
   `inline_attempted=1`, `delivery_state=delivered`.
   The isolated HTTPS receiver independently verified
   the Standard Webhooks signature and saw **exactly one**
   event delivery. The callback also checked the
   `signal_is_success_evidence=false`,
   `fresh_mcp_reobservation_required=true` and
   `merge_authority_granted=false` boundaries.
   This was **NOT** a real GitHub webhook or an assertion
   that any corresponding CI run exists.
5. Replaying the exact same synthetic signed input and delivery
   ID returned HTTP **202** with
   `delivery_state=no_due_events`, while the independent
   receiver's count remained **one**. No duplicate
   external event was delivered.
6. A separately signed but **nonmatching** synthetic workflow
   (`Lean Formal Validation`) returned HTTP **202**,
   `enqueued=0`, with zero new callback deliveries.
   The allowlisted source workflow did not bypass the
   subscriber's narrower workflow filter.
7. Authenticated `events/unsubscribe` **200**;
   synthetic access-token `POST /revoke` **200** using
   the pinned public-client `client_secret=""` compatibility
   form; post-revocation `events/list` HTTP **401**.
   The synthetic test did not create a Dots subscription.

### Independent real PostgreSQL post-test receipt and cleanup

- Isolated Neon staging SQL after the HTTPS test found
  **zero** subscriptions; **one** outbox row, with
  `state=delivered`, and **zero** rows pending.
  Thus a real transactional outbox delivery existed and its
  terminal state was confirmed independently of the
  callback's self-report. The delivered row is an
  intentionally retained synthetic test artifact.
- Previous synthetic OAuth tests left **one access** and
  **one refresh** record; a total of **three** synthetic
  client registrations remain. The test's newly issued
  access token was revoked. Remaining earlier credentials
  were **not** claimed revoked or deleted.
- The default/production Neon branch still contained **zero**
  KuuOS MCP service tables on read-only SQL reinspection.
- The sandbox session was explicitly **stopped** with
  `persistent=false` and no live callback receiver was
  left running.

### Obstructions and authority

The test source and callback are synthetic, not GitHub/Dots.
No actual GitHub repository webhook sender was configured
or independently observed by the available GitHub MCP
administration tools. No user-owned ChatGPT custom MCP
plugin, approved stable external MCP URL, actual OAuth
consent, authentic Dots `events/subscribe`, or Dots
callback and exact GitHub MCP source/run/attempt/job/Lean
step re-observation has been observed.

Do not upgrade
`SYNTHETIC_SIGNED_SOURCE_HTTPS_DELIVERY_CERTIFIED`
to
`AUTHENTIC_GITHUB_TO_DOTS_CERTIFIED`.

Certification limited to:
`STAGING_SYNTHETIC_EVENTS_E2E_DELIVERED_ONCE`,
`STAGING_REPLAY_DEDUPED`,
`STAGING_WORKFLOW_FILTER_EXCLUSION`,
`STAGING_SUBSCRIPTION_UNSUBSCRIBED`,
`STAGING_OAUTH_TOKEN_REVOKED`.

Persistent obstruction:
`BLOCKED_DOTS_REAL_SUBSCRIPTION_AND_AUTHENTIC_GITHUB_SENDER`.


## Genuine GitHub Actions OIDC sender → stable Vercel staging → Neon source receipts (2026-11-21 JST)

This section is an independently observed transition beyond prior synthetic
Webhook tests: **GitHub Actions actually issued short-lived, RSA-signed
OIDC tokens and delivered claims matching the repository, job, branch,
run and exact HEAD to an HTTPS receiver.** The receiver verified the
GitHub signature and persisted immutable source receipts in Neon.
These are sender identity and job-gate *observation* receipts, **not**
CI theorem verification or Dot delivery authority.

### Exact source and independent CI

- Canonical KuuOS `main` observed HEAD
  `5b0770a3c32c23f5fc6dd69b5f2dcbf09bee7656` (unmodified by this work).
- Existing feature branch
  `feat/kuuos-dots-mcp-ci-event-contract-v0-1-20261120`, exact CI-certified source HEAD
  `eff91784d46e97aeeea3c0b51fbf23901352aa78`.
- Exact integrated CI
  [#44833605981](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44833605981)
  `completed/SUCCESS` at that HEAD, four completed SUCCESS jobs:
  Python **262 passed, 15 skipped, 2 warnings**;
  disposable PostgreSQL **16.16 15/15**;
  disposable PostgreSQL **18.7 15/15**;
  and **Authenticate actual completed validation gates to isolated staging**
  SUCCESS. The last job runs only after the preceding Python and
  matrix PostgreSQL jobs settle, and does not claim that its own
  workflow was terminal before it completed.
- Preceding source verifier exact code
  `290f5f5fd0822e1ad255b8b2949328cb86f6bf8e`
  independently certified by
  [#44832091576](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44832091576):
  `completed/SUCCESS`, three jobs successful;
  Python 260 passed, 13 skipped, 2 warnings;
  disposable PG16/PG18 13/13 each.
- The append-only PostgreSQL source receipt tests were added
  subsequently and passed on source HEAD
  `c140d8e4af01af495d3ee55c8f14f65b657ca4ac`
  with
  [#44832885085](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44832885085):
  Python 260 passed, 15 skipped, two warnings, PG16/18 15/15.

### Staged public HTTPS service independent of original production

- New **dedicated isolated staging Vercel project**
  `kuuos-mcp-oidc-staging`, project ID
  `prj_kPvFkBzOV0deLPxncLOmSO8ViO5O`,
  stable public HTTPS origin
  https://kuuos-mcp-oidc-staging.vercel.app .
  Its accessible MCP endpoint is
  `https://kuuos-mcp-oidc-staging.vercel.app/api/mcp`,
  and independent GitHub OIDC receiver
  `https://kuuos-mcp-oidc-staging.vercel.app/api/github-oidc`.
- To attach a stable production alias **within this isolated staging
  project only**, Vercel deployment target is `production` on
  `kuuos-mcp-oidc-staging`. Do **not** conflate this with
  promotion of the pre-existing `kuuos-chat-work-mcp`
  production project, which was untouched.
- Staging runtime deployment
  `dpl_DQ9nioAF9ZMHv25aeAuFJTHfVNS3`,
  READY with exact deployed source
  `2a364b45102247c83ba6f383ff40e8870725d4d9`
  and the stable alias assigned to that deployment.
  The separate later GitHub CI workflow commit does not
  modify this deployed Python runtime source.
- The new isolated project's environment is its own production
  target. It has 14 separate environment variables: a
  least-privilege DML-only URL to the same **Neon staging branch**
  `br-proud-queen-ayak8zsl`, strict
  `KUUOS_MCP_SCHEMA_MODE=preprovisioned`,
  `KUUOS_MCP_GITHUB_OIDC_ENABLED=true`, exact OIDC
  audience `api://kuuos/KuuOS/mcp-source-oidc-v1`,
  embedded OAuth (required for MCP methods), encrypted
  subscription storage, and `KUUOS_MCP_WRITE_ENABLED=false`.
  The synthetic OAuth owner secret and AES key were created
  privately as Vercel sensitive configuration, not copied
  into GitHub or the evidence workbench. **No actual user
  OAuth login/consent is asserted.**
- Public `/healthz` returned real HTTPS 200 with
  `backend=PostgresStateStore`, `mode=read-only`,
  `oauth_enabled=true`, `mcp_events_adapter_loaded=true`,
  `github_oidc_source_loaded=true`,
  `github_event_ingress_loaded=false`,
  and `write_ready=false`.
  The HMAC GitHub Webhook listener is intentionally disabled
  on this isolated public project; it admits only the strictly
  scoped GitHub-issued OIDC route. The existing protected
  original Vercel project and its Preview configuration were
  not altered.

### True GitHub Actions ID token admission

- `mcp_bridge/kuuos_mcp_bridge/github_oidc_source.py`
  verifies a JWT signed by GitHub's exact JWKS endpoint
  `https://token.actions.githubusercontent.com/.well-known/jwks`
  with **RS256 only**, exact issuer
  `https://token.actions.githubusercontent.com`,
  fixed audience, exact repository string and **numeric repository
  ID 1235298309 / owner ID 216274897**, exact branch ref,
  exact allowlisted `workflow_ref`/workflow name, matching
  event name, SHA, run ID, run attempt and payload.
  The JWT URL, audience and signing key cannot be overridden
  by an untrusted caller. Bad/missing identity fails closed.
- GitHub source workflow
  `.github/workflows/kuuos-mcp-github-oidc-source.yml`
  has only `contents: read` and `id-token: write`,
  and no shared GitHub/Vercel HMAC secret. GitHub supplies
  its own short-lived OIDC bearer through
  `ACTIONS_ID_TOKEN_REQUEST_URL` and
  `ACTIONS_ID_TOKEN_REQUEST_TOKEN`. Tokens are never
  printed, committed or persisted in Neon.
- **Genuine source workflow #44832696689**:
  https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44832696689
  completed/SUCCESS on actual pushed HEAD
  `b6cffd4be56f199e9156991be1607f71e0fa8236`,
  returned HTTP **202** with
  `signed_oidc_accepted=true`, persisted first receipt
  `oidc_673209c6327a874c469f0ab1454f51b82efd955d398f1cc9055ec0819dbcd5ed`.
- **Second genuine source workflow #44833354567**:
  completed/SUCCESS, pushed HEAD
  `2a364b45102247c83ba6f383ff40e8870725d4d9`,
  independently persisted receipt
  `oidc_794ac16277a3aa2d981424f2fd606756787d678b156190847cd45f8d8011f5ac`.
- To prove actual CI-gate signaling, the existing
  `.github/workflows/mcp-bridge-python-validation.yml`
  was extended with a **separate notification job** gated by
  `needs: [validate, postgres-integration]`, limited to
  this feature branch. That job requests its *own* OIDC
  token and sends `kind=ci_jobs_observed`. Source OIDC
  validation requires the different, exact pinned
  CI workflow name and workflow_ref; a push-probe workflow
  token cannot impersonate the CI gate sender.
- **Actual CI-gate notification #44833605981**:
  the Python and PG16/18 job groups completed SUCCESS,
  followed by the real `notify-github-oidc` job
  SUCCESS. The Vercel OIDC validator accepted the exact
  run ID `44833605981` and SHA
  `eff91784d46e97aeeea3c0b51fbf23901352aa78`;
  the original GitHub Actions job reported
  `validate_job_result=success`,
  `postgres_matrix_result=success`,
  and `is_terminal_workflow_conclusion=false`.
  The persistent source receipt is
  `oidc_4d3a098ee027578211051c4ba03966a8073656bc809a408047cd935089fc5351`.
- Independent read-only Neon SQL found **exactly three**
  genuine GitHub-originated OIDC receipts with matching
  repository, workflow_ref, SHA, run ID and timestamps:
  two actual push source observations and one actual
  post-CI-gates source observation. The database enforces
  immutable one-receipt-per-source-run uniqueness; restricted
  application role cannot run DDL.
- The sender identity is **real** and cryptographically checked,
  but notification contents still do **not** certify the entire
  underlying CI run; they carry
  `signal_is_success_evidence=false` and
  `fresh_mcp_reobservation_required=true`.
  GitHub run/job/step state must be independently re-read
  before any future Dot concludes certification or merge.

### Last remaining connected-Dot boundary

- This proves a new genuine outbound **GitHub Actions →
  dedicated public Vercel HTTPS → Neon** path. The prior
  first-principles blocker of sharing a GitHub webhook HMAC
  secret is resolved for the allowlisted OIDC workflow sender.
- **No ChatGPT-installed KuuOS custom MCP plugin, real user OAuth
  consent, Dots「くー」 `events/subscribe`, Dots callback,
  or Dot-triggered independent Lean/CI proof audit has been
  observed.** The dedicated service has OAuth, but its
  login credential is currently a synthetic staging secret;
  it does not establish the account owner's identity.
  Custom MCP connection must be authorized within
  the user's ChatGPT workspace and OAuth login.
- To turn an authentic CI observation into a Dots delivery,
  the true user-connected plugin must subscribe with a
  verified callback. The OIDC source receipt currently
  **records the real signal**, but does not create a Dot
  subscriber or claim the source signal was sent to Dots.
  Current OIDC sender targets the feature branch;
  expanding to the canonical main and broader KuuOS / 4d-mass-gap
  CI workflows still needs explicit reviewed trust-policy scope.
- Original GitHub main, existing Vercel production project
  and the Neon default branch have not been mutated.
  Read-only SQL confirmed **zero** KuuOS MCP service tables
  on the Neon default branch.

Certification:
`GITHUB_AUTHENTIC_OIDC_PUSH_SOURCE_RECEIVED_2` /
`GITHUB_AUTHENTIC_CI_GATES_SOURCE_RECEIVED_1` /
`NEON_APPEND_ONLY_SOURCE_RECEIPTS_3` /
`CI_262_PG16_18_15_SUCCESS`.

Obstruction:
`CHATGPT_DOTS_REAL_SUBSCRIPTION_UNOBSERVED`.

## Independent GitHub Actions / Neon OIDC receipt reconciliation (2026-11-21)

Scope: read-only independent GitHub MCP, Vercel MCP and Neon MCP
observation, with **no ChatGPT/Dots event-subscription claim**. This
documentation append changes neither certified Python source, original
Vercel production, canonical main nor the protected PR.

### Seven actual OIDC source receipts vs independently re-read GitHub runs

Neon project `rough-meadow-33652646`, isolated branch
`br-proud-queen-ayak8zsl`, reported exactly **7** append-only
`kuuos_mcp_github_oidc_source_v1` records. A read-only query obtained
each repository, workflow_ref, ref, head SHA, run ID, attempt and
timestamp, without reading access tokens, private signing material or
JTI hashes. All 7 were independently compared with the exact GitHub
Actions run endpoint using the GitHub MCP connector. Every row matched
`itakura-hidetoshi/KuuOS`, the feature branch,
`run_attempt=1`, and its exact 40-character head SHA.

| Exact GitHub run | Kind | GitHub conclusion |
| --- | --- | --- |
| [#44835215398](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44835215398) | MCP Python/PG validation | completed / SUCCESS |
| [#44835109525](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44835109525) | MCP Python/PG validation | completed / SUCCESS |
| [#44834866136](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44834866136) | MCP Python/PG validation | completed / **FAILURE** |
| [#44834866165](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44834866165) | authentic GitHub OIDC source | completed / SUCCESS |
| [#44833605981](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44833605981) | MCP Python/PG validation | completed / SUCCESS |
| [#44833354567](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44833354567) | authentic GitHub OIDC source | completed / SUCCESS |
| [#44832696689](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44832696689) | authentic GitHub OIDC source | completed / SUCCESS |

**A received cryptographically verified source identity is not a CI success
proof.** The failed CI #44834866136 remains a genuine admitted source
receipt and must not be deleted, filtered or promoted to SUCCESS.
The successful OIDC-source workflow for the same SHA is a distinct run.

### Live staging runtime and subscriber authority check

An actual Vercel MCP GET to
`https://kuuos-mcp-oidc-staging.vercel.app/healthz`
returned HTTP 200 with `backend=PostgresStateStore`,
`oauth_enabled=true`, `mcp_events_adapter_loaded=true`,
`github_oidc_source_loaded=true`,
`github_oidc_delivery_loaded=true` and `write_ready=false`.
This demonstrates a current *staging* runtime and database health read,
not a user OAuth grant, signed event callback or Dot activation.

Staging Neon had **one** event-subscription row at this observation.
Its event is `kuuos.github.ci_gates_observed`; its principal is
`kuuos-owner`, a synthetic staging identity, and the callback host
is a temporary `vercel.run` sandbox, **not** the ChatGPT/Dots callback.
The verification timestamp was
`2026-11-20T23:20:59.452Z` and its finite expiry was
`2026-11-21T00:20:59.452Z`; this record must not be mistaken
for a durable user-owned subscription. No callback URL token or secret
was copied into this report.

The same database held **one** terminal outbox record,
`kuuos.github.ci_completed`, `state=delivered`,
`attempts=1`, `last_http_status=200`. Its distinct event name
is from earlier synthetic ingress testing; it does **not**
establish delivery of the newer authentic OIDC
`kuuos.github.ci_gates_observed` event to Dots.

At the initial source check the feature branch HEAD was
`37eed415a20e8aaaabd220043779881345e451bb`,
whose own validation run
[#44836227181](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44836227181)
was still `queued`. The earlier exact source
`7ef4dfb4096007fd5e9bd2761e96b1fe21861458`
had independently passed
[#44835215398](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44835215398).
No green conclusion or source/deployment equivalence is inferred
for the later source while its own run is pending.

The genuine OIDC event intake is an important independent boundary:
it is not a connected ChatGPT custom KuuOS MCP plugin, real end-user
OAuth consent, an authenticated Dots `events/subscribe` call,
a Dots callback receipt, or a Dot-triggered exact GitHub MCP
job/step/Lean axiom audit. Preserve
`BLOCKED_MCP_EVENT_SUBSCRIPTION` until those separate
receipts are observed. No merge/deployment/write authority follows
from this read-only cross-system reconciliation.

## Real GitHub OIDC CI-gate wake-up to synthetic HTTPS receiver (2026-11-21)

This is a **later independent cross-system re-observation** of a previously
queued validation run. It supplements, and does not overwrite, the earlier
time-scoped observation in the seven-receipt reconciliation.

- The exact-source GitHub Actions
  [#44836227181](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44836227181)
  on `37eed415a20e8aaaabd220043779881345e451bb`
  became **completed/SUCCESS**. Four jobs separately returned SUCCESS:
  Python validation, actual PostgreSQL 16, actual PostgreSQL 18, and
  `Authenticate actual completed validation gates to isolated staging`.
  This authenticates the exact source and CI job results, not Lean/axiom
  certification or Dots receipt.
- An independent read-only query of the isolated Neon staging
  `br-proud-queen-ayak8zsl` then found a **new, eighth**
  immutable GitHub OIDC source receipt for run `44836227181`,
  attempt 1, exact SHA `37eed415a20e8aaaabd220043779881345e451bb`,
  received `2026-11-20T23:27:19.202Z`.
- Crucially, a **separate** PostgreSQL event-outbox query showed
  `name=kuuos.github.ci_gates_observed`,
  `source_run_id=44836227181`, `state=delivered`,
  `attempts=1` and `last_http_status=200`.
  Thus real GitHub-issued OIDC source identity was admitted, matched
  the then-active synthetic subscription, and the actual staging sender
  recorded an HTTP 200 acknowledgment to that subscription's
  external HTTPS receiver. This is not merely a mocked packet.
- The matching subscription had `principal=kuuos-owner` (staging
  synthetic owner), `name=kuuos.github.ci_gates_observed`,
  callback host `sb-7k3jflx6mq8o.vercel.run`, and finite expiry
  `2026-11-21T00:20:59.452Z`. This is a **sandbox callback,
  not a ChatGPT/Dots callback**. No callback signing key,
  complete callback URL, OAuth bearer or credential is recorded.
- The other outbox entry is the earlier synthetic
  `kuuos.github.ci_completed` event, also delivered; keep
  the two event sources and receipts distinct. A 200 outbox status
  alone does not prove the receiving Dot executed an independent audit.
- The current source of truth for genuine terminal CI status is
  GitHub's exact run/job/step API, not a sender-supplied event verdict.
  Canonical main and existing KuuOS production were not changed;
  no new PR was created.

This demonstrates an actual authenticated
**GitHub Actions OIDC → public staging ingress → PostgreSQL exact-ID outbox
→ synthetic HTTPS subscriber 200** transport. It **does not**
demonstrate an installed custom KuuOS plugin, the user's OAuth consent,
a Dots `events/subscribe` call, a Dots webhook callback or
post-wake-up GitHub MCP Lean-proof audit. Retain
`BLOCKED_MCP_EVENT_SUBSCRIPTION` for Dots.


## External OIDC delivery cleanup and final receiver-observation boundary (2026-11-21 JST)

This note is later than the real OIDC CI-gate wake-up receipt immediately above.
Do not overwrite earlier queued or synthetic-source observations.

- True GitHub run
  [#44836227181](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44836227181)
  was independently re-read as `completed/SUCCESS` with all four
  jobs SUCCESS and the exact SHA
  `37eed415a20e8aaaabd220043779881345e451bb`.
  Actual Python result: **270 passed, 16 skipped, 2 warnings**.
  Disposable PostgreSQL 16.16 and 18.7: **16/16** each.
  These tests do not assert Lean theorem axioms.
- Staging Neon `br-proud-queen-ayak8zsl` source OIDC receipt:
  run `44836227181`, attempt 1, same GitHub SHA,
  `received_at=2026-11-20T23:27:19.202Z`,
  `oidc_00270ea715c1122757278ff878dafb30d9db942230cc610485de4a1ae0139cc1`.
  Independent SQL on the event outbox saw
  `kuuos.github.ci_gates_observed` with
  `state=delivered`, `attempts=1`,
  `last_http_status=200`, same run and SHA, and
  `signal_is_success_evidence=false`.
  This is a genuine GitHub identity and an HTTP response receipt,
  **not** a Dots audit or terminal CI conclusion inferred from the event.
- The temporary external `vercel.run` receiver had earlier
  returned a signed challenge response, but by final independent
  read its Python server had ended, and a local GET returned
  `URLError`. Its **separate in-memory per-event count could not
  be recovered**, so the receiver-side independently persisted
  acknowledgment remains `NO_DATA`. The sender's durable HTTP 200
  receipt must not be relabeled as that missing acknowledgment.
- Cleanup of the synthetic subscriber was performed using its
  separate ephemeral OAuth bearer. Real HTTPS
  `events/unsubscribe` **200**, `POST /revoke` **200**,
  and subsequent use of that access token against MCP **401**.
  Independent post-cleanup staging SQL confirmed:
  **0** remaining `ci_gates_observed` subscriptions,
  **1 delivered** and **0 pending** matching outbox rows,
  **1** genuine OIDC receipt for the run. The outbox record
  remains as legitimate append-only test provenance.
- The nonpersistent Vercel Sandbox
  `sbx_IhsJJTbnlC8PoRoEGJMQZaKtV0W2`
  was explicitly `stopped`, not left as an unbounded callback daemon.
  The original Neon default branch
  `br-summer-lake-ayfwkun3` still has **zero**
  KuuOS MCP service tables.
- The stable isolated MCP staging URL remains
  `https://kuuos-mcp-oidc-staging.vercel.app/api/mcp`.
  It still uses **synthetic staging OAuth identity**;
  **no** actual connected ChatGPT KuuOS plugin, user OAuth
  consent, Dots「くー」 `events/subscribe`, Dots webhook
  receipt or Dots-triggered independent GitHub MCP source/job/Lean
  audit is established. The only authentic GitHub-to-HTTPS
  result here is for the synthetic staging subscriber.

State:
`AUTHENTIC_GITHUB_OIDC_TO_OUTBOX_HTTP_200_CERTIFIED` /
`SYNTHETIC_SUBSCRIPTION_REMOVED_AND_TOKEN_REVOKED` /
`RECEIVER_INDEPENDENT_EVENT_COUNTER_NO_DATA` /
`BLOCKED_DOTS_REAL_USER_SUBSCRIPTION`.

## Connected-user plugin boundary and post-unsubscribe regression (2026-11-21)

This is a forward-only readiness observation. It does not claim that the
user's ChatGPT account, a Dot, or a custom plugin has been authenticated.

### Live deployment and current subscription state

- Public **isolated staging**, not original KuuOS production:
  `https://kuuos-mcp-oidc-staging.vercel.app/api/mcp`.
  Its /healthz returned HTTP 200 and showed
  `backend=PostgresStateStore`, `oauth_enabled=true`,
  `mcp_events_adapter_loaded=true`, `github_oidc_source_loaded=true`,
  `github_oidc_delivery_loaded=true`, and `write_ready=false`.
  Production target applies **only within this dedicated staging Vercel
  project**, not to the original production service.
- Independent OAuth protected-resource metadata HTTP 200:
  resource points to this exact HTTPS `/api/mcp` and the only advertised
  scope is `kuuos:read`. OAuth authorization-server metadata HTTP 200
  advertised the same stable issuer, authorization-code flow and PKCE S256.
  **Metadata success is not end-user consent.**
- Independent read-only Neon query of `br-proud-queen-ayak8zsl`
  showed **8** genuinely signed GitHub OIDC source receipts,
  **0** active stored subscriptions (the synthetic subscription was
  deliberately removed), and **2** historical outbox rows.
  The two outbox events are distinct: an earlier synthetic
  `kuuos.github.ci_completed` and a later authentic-source
  `kuuos.github.ci_gates_observed`. Both are sender-side delivery
  receipts, not verified Dots executions.
- Plugin directory discovery for the exact `KuuOS` name returned no
  currently discoverable custom plugin for this Chat session.
  This is **not** evidence that a plugin cannot exist in another
  workspace or be created with authorized workspace controls.

### User-owned registration / authority

OpenAI's current custom MCP connector instructions require an eligible
ChatGPT workspace and web-based creation. The user/workspace must
initiate connection and complete its OAuth consent; the repository,
GitHub MCP, Vercel deployment or a synthesized owner secret cannot
perform this account-bound action in its place.

Official references:
- https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt
- https://developers.openai.com/plugins/build/mcp-events

The implementation-ready connection target is the exact stable HTTPS
endpoint above. The **current embedded owner credential is a synthetic
staging secret** and must not be treated as evidence of the real
account owner. A real identity/consent mechanism and an approved
custom MCP registration remain separate external gates.
After connection, the exact checks are user-authorized
`initialize`→`events/list`→`events/subscribe` signed challenge,
one matching genuine event, one nonmatching event, Dots-specific
callback receipt, independent exact GitHub MCP run/job/Lean-step
re-observation, then unsubscribe/revocation. Without those, retain
`BLOCKED_MCP_EVENT_SUBSCRIPTION`.

### Additional fail-closed regression in the existing feature branch

Python `mcp_bridge/tests/test_oidc_delivery_pipeline.py` gained
`test_unsubscribe_prevents_real_gate_reenqueue_and_cancels_inflight_delivery`,
which constructs two *modeled* verified OIDC source packets with
different run identities, unregisters the synthetic subscriber,
checks that the second packet cannot enqueue an event, and checks
that the earlier queued event cannot send after revocation.
This is a unit regression, **not** a live GitHub or Dots callback.
Code source HEAD `206e09a0abd0c5d4289438657a15b6798b7558ab`;
independent GitHub Actions run
[#44838225375](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44838225375)
was **queued** at the source read; its success is not presumed.

No change to canonical main, pinned Lean mathlib, existing production,
real-user credentials or protected PR #1558 was made by this doc.

## User-owned ChatGPT custom MCP OAuth activation runbook (2026-11-21)

This section prepares **real-user connection**, not a claimed login or
subscription. This is an append-only operations record on the existing
feature branch. Canonical KuuOS main, original Vercel production,
Neon default branch and protected PR are unchanged.

### Source and exact CI boundary

- Security hardening code `bd727479e31bcbbd25be4387af94374f1a4db7dc`
  adds owner-subject checks to stored access tokens, refresh tokens
  and token-pair issuance. It also advertises optional
  `offline_access` for the existing rotating refresh-token flow;
  the default `kuuos:read` and write gate were not loosened.
- CI [#44838983428](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44838983428)
  discovered a failing PostgreSQL 18 integration fixture. Source showed
  the fixture issued `subject=synthetic-ci` against the provider's
  default `owner_subject=kuuos-owner`. The **new fail-closed rule
  correctly rejected that mismatch**. The resulting frozen SDK
  `TokenError` also produced a secondary Python `FrozenInstanceError`
  in exception unwinding; the subject mismatch is the primary cause.
- Corrected test-only exact source
  `cb00a56866b098e5f37769f0ae9cf33cea237f85` explicitly configures
  `owner_subject=synthetic-ci` for that synthetic PostgreSQL revocation
  test. No exception handler or security condition was removed.
  Independent [CI #44839247350](https://github.com/itakura-hidetoshi/KuuOS/actions/runs/44839247350)
  was **queued** on initial inspection. Do not deploy as certified
  until all exact-head Python and PostgreSQL 16/18 jobs complete SUCCESS.

### Secure credential and application ownership boundary

OpenAI custom MCP registration is an **account/workspace action on ChatGPT web**,
not an operation granted by KuuOS GitHub MCP or this isolated staging server.
Its availability depends on the ChatGPT plan and permissions; MCP Events
is tested in Work or with dots after the plugin is connected.

Registration inputs after deployment:
- Name: `KuuOS MCP Events`
- Public HTTPS MCP endpoint:
  `https://kuuos-mcp-oidc-staging.vercel.app/api/mcp`
- Authentication: OAuth against the exact HTTPS issuer
  `https://kuuos-mcp-oidc-staging.vercel.app/`.
- First test only `kuuos:read` and optional `offline_access`;
  keep `KUUOS_MCP_WRITE_ENABLED=false`.

The current embedded login is **single-owner secret authentication**,
not OpenAI or GitHub identity federation. The synthetic staging owner
secret is not known to or consented by the actual account holder.
The account holder must independently set a fresh, password-manager-
generated secret in the existing Vercel
`kuuos-mcp-oidc-staging` project > Settings > Environment Variables >
`KUUOS_MCP_EMBEDDED_AUTH_SECRET` (Production target **of that
isolated staging project only**). Use Vercel's **Secret** type and do
not send or paste the value into this chat, GitHub or logs.

A new secret **alone does not invalidate** tokens issued to the old
synthetic subject. At the same activation the operator must set
`KUUOS_MCP_EMBEDDED_AUTH_SUBJECT` and
`KUUOS_MCP_EVENTS_ALLOWED_SUBJECTS` to the **same new, bounded
account-specific principal** in the isolated project, after reviewing
the eligible connected user. This must be coordinated with a new
deployment of exact-source certified code that enforces the
new subject checks. Existing synthetic token rows remain as retained
historical evidence, but are refused by the new deployed provider.
Never use the synthetic owner secret for real consent.

Vercel environment edits only apply to new deployments. Redeploy the
approved, exact CI-certified Git source to the stable isolated staging
project, confirm its source SHA, GET /healthz and OAuth metadata,
and verify `offline_access` discovery. No automatic writes to the
original `kuuos-chat-work-mcp` production.

### Separate end-to-end user and Dot acceptance

1. In the eligible ChatGPT **web** workspace: Plugins > + >
   Add custom MCP server. Enter the name, HTTPS endpoint and OAuth mode;
   review risk warning, and create the plugin.
2. Complete **real-user** authorization in the browser on the exact
   staging OAuth issuer, using the owner secret they themselves chose
   in Vercel; approve the ChatGPT application. Never supply credentials
   to an assistant.
3. Confirm tool discovery and an authenticated read-only state read;
   inspect the new principal/client in the staging database using
   *non-secret metadata only*. A newly registered client alone is not
   a verified Dots subscription.
4. In a Work chat or Dot, subscribe to the exact authorized GitHub
   CI event. Verify a signed `events/subscribe` callback challenge,
   real GitHub OIDC source admission, matching delivery and receiver-side
   Dot acknowledgment; check a nonmatching exclusion and unsubscribe.
5. Have the awakened Dot independently read exact GitHub
   repo/head/run/attempt/job/Lean step before upgrading any CI result
   to proof certification. No merge/write authority is inherited
   from notifications.

Until steps 2–5 have external receipts:
`BLOCKED_MCP_EVENT_SUBSCRIPTION` /
`REAL_USER_OAUTH_CONSENT_NOT_OBSERVED`.

Official references:
- https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt
- https://developers.openai.com/plugins/build/mcp-events
- https://vercel.com/docs/environment-variables/managing-environment-variables
