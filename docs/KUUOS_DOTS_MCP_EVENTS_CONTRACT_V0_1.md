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
