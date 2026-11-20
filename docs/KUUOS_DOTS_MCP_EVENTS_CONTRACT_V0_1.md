# KuuOS → Dots MCP Events: typed GitHub wake-up contract v0.1

Status: **candidate / offline-tested / NOT SUBSCRIBED / NOT DEPLOYED**.

## Source and epistemic boundaries

This additive Python module is a source-side contract for a future MCP Events adapter.
It is not the active OpenAI plugin, an `events/list` implementation, a subscription
registry, an event sender, or permission to modify a repository. Its test result
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
  → authenticated, replay-protected ingress [NOT IMPLEMENTED]
  → source-side normalized, identity-bound candidate wake-up [v0.1 TESTED]
  → MCP Events events/list, events/subscribe, events/unsubscribe [NOT IMPLEMENTED]
  → callback verification and persistent subscription [NOT IMPLEMENTED]
  → signed Standard Webhooks delivery [signature helper TESTED; transport NOT IMPLEMENTED]
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
