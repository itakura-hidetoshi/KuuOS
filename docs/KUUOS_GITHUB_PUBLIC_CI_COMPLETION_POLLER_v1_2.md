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

The source read is unauthenticated and deliberately small: one recent workflow-run listing per poll, plus job reads only for newly observed canonical candidates.

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

## Bootstrap and deduplication

The first successful poll primes a monotone run-ID state without replaying historical CI. Later polls consider only higher run IDs. The state is retained by the GitHub Actions cache on the KuuOS default branch.

If source observation or KuuOS self-dispatch fails, the poll fails closed and state is not advanced by a successful cache-save step, so the next scheduled run can retry.

## Self-dispatch

The poller emits the already-supported event type:

`kuuos_ci_completion_v1_1`

Its payload includes the source repository, run ID, workflow name, head SHA, branch, workflow conclusion, exact required job and exact required step. It also records:

```text
wakeup_is_success_evidence = false
fresh_mcp_reobservation_required = true
```

The self-dispatch grants neither merge nor write authority.

## Formal boundary

`formal/KuuOSGitHubMCPServerBridgeV0_1/V1_2.lean` defines `PublicPollWakeupGate.SafeWakeup` and proves that a wrong canonical base, fork head, pending workflow, missing exact step, use of the poll signal as success evidence, bypass of v1.1 fresh-MCP re-entry, or derivation of merge/write authority all make the wake-up gate impossible.

## Relationship to source-side sender

When `KUUOS_CI_REENTRY_TOKEN` is eventually configured in `4d-mass-gap`, the source-side sender provides immediate event-driven delivery. This v1.2 poller remains useful as an independent observation fallback. Duplicate wake-up packets are harmless because neither path is authoritative success evidence; downstream exact identity and fresh MCP observation remain mandatory.
