# KuuOS GitHub Public CI Completion Poller v1.2

## Purpose

This layer makes the `4d-mass-gap -> KuuOS` CI wake-up path operational even when no cross-repository credential has been installed in the source repository.

The preferred low-latency path remains the source-side `repository_dispatch` sender. v1.2 adds a credential-free fallback in the opposite direction:

```text
KuuOS scheduled observer
  -> public GitHub REST read of itakura-hidetoshi/4d-mass-gap
  -> completed PR Lean Fast Check
  -> canonical-base / same-repository-head gate
  -> exact Changed Lean fast check job
  -> exact Run changed Lean fast check step
  -> KuuOS self repository_dispatch
  -> existing KuuOS CI Completion Reentry v1.1
  -> fresh GitHub MCP re-observation required
```

The public poll is a wake-up transport only. It is not promoted into success evidence and it does not replace the v1.1 MCP verification boundary.

## Why the observer lives in KuuOS

GitHub Actions repository tokens are repository-scoped. A `4d-mass-gap` `GITHUB_TOKEN` is not silently reused as authority over KuuOS. Instead, KuuOS reads the public source repository without credentials and, after validating the bounded source identity, uses its own `GITHUB_TOKEN` only to dispatch back into the same KuuOS repository.

This removes the cross-repository secret from the fallback path while preserving repository authority boundaries.

## Poll interval

`.github/workflows/kuuos-mgap-ci-reentry-poller-v1-2.yml` requests the GitHub Actions five-minute cron cadence. GitHub may delay scheduled workflows under platform load, so this is a bounded near-real-time fallback, not a hard real-time guarantee.

Source reads remain unauthenticated. The poller pages through at most 1,000 workflow runs to reach the reviewed checkpoint and reads exact jobs for new candidates. It fails closed if the observed window cannot cover the checkpoint or if
pagination returns duplicate run IDs. A completed run whose conclusion is missing
or malformed also blocks checkpoint advancement rather than being marked
ignored; the same rule applies to malformed job/step conclusion values. Pending runs are included: the cursor stops before the oldest pending run, so a later completion cannot cause that older run to be skipped.

## Source gate

A run can become a wake-up candidate only when all of the following hold:

- workflow name is exactly `PR Lean Fast Check`;
- event is `pull_request`;
- workflow status is `completed` with a terminal conclusion;
- exact head SHA is a 40-hex commit identity;
- PR base is exactly `formal/real-hilbert-uniform-coercive-strong-limit`;
- the PR head belongs to `itakura-hidetoshi/4d-mass-gap` rather than a fork;
- exactly one `Changed Lean fast check` job is present and terminal;
- exactly one `Run changed Lean fast check` step is present and terminal.

A terminal `skipped` exact Lean step is accepted as terminal observation, because infrastructure-only changes can make Lake unnecessary. The workflow conclusion is still carried separately.

## Checkpoint persistence and recovery

Normal polling never bootstraps to the latest run. Missing, malformed, wrong-source,
or wrong-version state fails before source polling or dispatch. The workflow uses
an authoritative JSON checkpoint in the same repository on the dedicated branch
`state/kuuos-mgap-ci-poller-v1-2`, at
`kuuos_mgap_ci_completion_poller_v1_2.json`. It uses the existing `contents: write`
permission only in the live poll job. PR validation remains read-only. No new token,
permission, credential, or external storage service is required.

The state branch and file **must be explicitly provisioned before rollout**. This
repair does not create them, migrate an unreviewed cache watermark, dispatch old
runs, or merge itself. Recover the last trustworthy checkpoint, review the skipped
interval and any already-delivered notifications, and explicitly decide the initial
cursor before installing that checkpoint. A missing checkpoint is an actionable
failure, never a green bootstrap. Do not initialize using the current maximum run
ID merely to make the workflow green. Replaying historical notifications is a
separate operator decision.

A checkpoint has this structure (the example cursor is synthetic, not a recovery
recommendation):

```json
{
  "version": "kuuos_github_public_ci_completion_poller_v1_2",
  "last_processed_run_id": 100,
  "source_repo": "itakura-hidetoshi/4d-mass-gap",
  "source_workflow": "PR Lean Fast Check",
  "canonical_base": "formal/real-hilbert-uniform-coercive-strong-limit"
}
```

Each confirmed dispatch or recorded terminal disposition is checkpointed immediately
with GitHub Contents API blob-SHA compare-and-swap. A failed or uncertain write stops
processing; there is no automatic retry or force update. The next read must observe
the server state. State commits retain the disposition audit history. Ordinary polls
with no progress create no commits. The local state file is only a working copy in
workflow mode. The Actions dependency cache is no longer a source of truth.

This is at-least-once delivery: a process crash or lost response after dispatch but
before a confirmed checkpoint can duplicate the in-flight wake-up. It cannot justify
marking an unsent notification delivered. The receiver still requires fresh MCP
observation and grants no authority. Run-ID deduplication retains the original
one-notification-per-run scope; reruns of an already checkpointed run ID are not a
new notification. Pending older runs intentionally delay newer completions rather
than lose their eventual result.

A terminal cancelled run with a **complete** jobs listing and no exact required job
is recorded as `quarantined`, with reason `cancelled_without_required_job`, and is
not dispatched. This allows later runs to proceed without manufacturing required-job
or success evidence. Missing required jobs on non-cancelled runs, duplicate required
jobs, missing required steps, incomplete API results, and nonterminal checks still
block. Job pages must contain unique positive IDs and match the run ID and head SHA.
The jobs endpoint is pinned to the listed run attempt; explicit attempt mismatches
also block. All returned jobs must be terminal before an absent required job can
be quarantined. Cancelled runs with the exact terminal job and step remain eligible and retain
their cancelled conclusion.

## Validation and rollout limits

Run the offline synthetic regressions with:

```sh
python3 -m unittest discover -s tests -p 'test_kuuos_ci_*.py' -v
```

They cover sender/receiver compatibility, malformed envelopes, state loss/corruption,
partial failure, SHA conflicts, pending completion ordering, pagination, cancellation,
and sanitized errors. Fresh receiver verification additionally requires unique named
jobs and steps, limits required steps to the selected jobs, and rejects nonterminal
selected conclusions. Unconstrained same-repository workflow events retain their
existing behavior. These tests do not establish live delivery, state provisioning,
Lean compilation, mathematical correctness, or successful deployment.

## Self-dispatch

The poller emits the already-supported event type:

`kuuos_ci_completion_v1_1`

Its client payload is a two-property versioned envelope, `{"schema_version": 2, "completion": {...}}`, below GitHub’s limit of ten top-level properties. The complete request is checked to stay below 64 KiB. The v1.1 receiver accepts this envelope and legacy flat senders; malformed or unsupported envelopes fail closed. The completion object includes the source repository, run ID, workflow name, head SHA, branch, workflow conclusion, exact required job and exact required step. It also records:

```text
wakeup_is_success_evidence = false
fresh_mcp_reobservation_required = true
```

The self-dispatch grants neither merge nor write authority.

## Formal boundary

`formal/KuuOSGitHubMCPServerBridgeV0_1/V1_2.lean` defines `PublicPollWakeupGate.SafeWakeup` and proves that a wrong canonical base, fork head, pending workflow, missing exact step, use of the poll signal as success evidence, bypass of v1.1 fresh-MCP re-entry, or derivation of merge/write authority all make the wake-up gate impossible.

## Relationship to source-side sender

When `KUUOS_CI_REENTRY_TOKEN` is eventually configured in `4d-mass-gap`, the source-side sender provides immediate event-driven delivery. This v1.2 poller remains useful as an independent observation fallback. Duplicate wake-up packets are harmless because neither path is authoritative success evidence; downstream exact identity and fresh MCP observation remain mandatory.

## Incident boundary

The observed cache save and later miss used the same default branch, restore prefix,
path, cache-action revision, and runner image. The exact cache-loss cause is not
established by those logs. Dependency caches can be removed and are not durable
processing journals. This repair removes that durability assumption; it does not
claim eviction was the demonstrated cause or reconstruct previously skipped runs.

References:
- https://docs.github.com/en/rest/repos/repos#create-a-repository-dispatch-event
- https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents
- https://docs.github.com/en/actions/reference/workflows-and-actions/dependency-caching
