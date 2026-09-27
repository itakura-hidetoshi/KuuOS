# KuuOS Qi GitHub Actions Bounded Live-Log Observer v7.0

## Purpose

v7.0 adds a read-only observation layer for GitHub Actions logs.

It deliberately does **not** claim a true streaming transport. The observation model is a bounded polling tail:

```text
exact run + exact HEAD SHA
  -> actions_get(get_workflow_run)
  -> actions_list(list_workflow_jobs)
  -> select current/relevant job
  -> get_job_logs(return_content=true, tail_lines=N)
  -> digest + suffix delta
  -> bounded re-observation
  -> terminal re-observation
  -> optional terminal full-log digest
```

The layer is designed to close the gap between a one-shot CI snapshot and a continuously re-observed CI world while preserving KuuOS authority boundaries.

## Upstream contract

The implementation contract was re-observed against the official `github/github-mcp-server` release `v1.12.2` (published 2026-09-16).

That release exposes the Actions tools required here:

- `actions_get`
- `actions_list`
- `get_job_logs`

and `get_job_logs` includes `return_content` and `tail_lines`.

The runtime does not trust a tag alone. A live plan must supply an immutable
`ghcr.io/github/github-mcp-server@sha256:<digest>` reference, then runtime tool discovery must independently observe all three tools as read-only.

## Authority model

v7.0 is observation-only.

Required properties:

- `read_only = true`
- `lockdown_mode = true`
- exact `expected_head_sha`
- explicit `run_id`
- immutable official GitHub MCP server image
- `actions` as the only toolset
- exactly `actions_get`, `actions_list`, and `get_job_logs` in the tool allowlist
- tool discovery proves every required tool is read-only

No rerun, cancel, merge, branch mutation, issue mutation, or repository write is part of this observer.

Write-capable GitHub Actions operations remain in the existing separately authorized surfaces.

## Log retention

Raw GitHub Actions logs are not written to the receipt or audit JSONL.

The observer persists:

- log digest
- line count
- delta digest
- delta line count
- whether the bounded window rebased
- a bounded latest delta excerpt
- terminal full-log digest when requested

This gives enough evidence to reason about state transitions without turning the KuuOS runtime receipt store into a second CI log archive.

## Exact-head invariant

Before reading any job log, v7.0 re-observes the workflow run with:

```text
actions_get(method=get_workflow_run)
```

The observed `head_sha` must equal the plan's `expected_head_sha`.

A mismatch terminates observation before `actions_list` or `get_job_logs` is called.

This prevents a stale run from being interpreted as evidence for the current theorem or runtime state.

## Job selection

If the plan provides `job_id > 0`, that job is preferred when present.

Otherwise the observer chooses, in order:

1. `in_progress`
2. `queued`
3. `waiting`
4. `pending`
5. latest failed/cancelled/timed-out/action-required job
6. latest remaining job by numeric ID

The job list is freshly re-observed at every polling step, so a workflow moving from setup to validation to terminal jobs can be followed without binding the observer permanently to the first job seen.

## Delta semantics

Let `L_n` be the bounded tail observed at poll `n`.

When `L_n` begins with `L_{n-1}`, the new observation is the suffix:

```text
Delta_n = L_n[len(L_{n-1}):]
```

When the tail window rotates and the prefix relation no longer holds, the observation is marked `window_rebased = true`, and the current bounded tail becomes the delta presentation.

This avoids pretending that a rolling tail is a monotone append-only stream.

## Terminal state

When the run reports `status = completed`, the observer records terminal state.

If `terminal_full_log = true`, it makes one final `get_job_logs` call without `tail_lines` and records only the digest of that full response.

The terminal full log itself is not persisted.

## Statuses

- `QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_TERMINAL`: terminal run observed with no blockers
- `QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_BOUNDED`: poll budget exhausted before terminal state, with no authority failure
- `QI_GITHUB_ACTIONS_BOUNDED_LIVE_LOG_BLOCKED`: authority, tool, exact-head, schema, or transport obstruction

A bounded result is not failure evidence and is not success evidence. It means only that the current observation budget ended before GitHub exposed a terminal run.

## Relationship to existing KuuOS GitHub Actions runtime

The existing KuuOS runtime already contains connector-oriented observation paths for:

- commit workflow runs
- workflow run jobs
- workflow job steps
- workflow job logs
- workflow run artifacts
- rerun requests under separate authority

v7.0 does not replace these. It adds a second, official GitHub MCP Server observation presentation specialized for bounded temporal re-observation and log deltas.

The intended descent is:

```text
existing exact-SHA CI authority
        +
existing GitHub Actions status reobserver
        +
official GitHub MCP actions toolset
        |
        v
bounded live-log observations
        |
        v
terminal exact-head receipt
```

## Validation

The focused checker exercises two cases:

1. an exact-head run progresses from `in_progress` to `completed/success`, with two bounded tails and a terminal full-log digest;
2. a mismatched run HEAD is rejected immediately and no job or log read occurs.

This is a Python/runtime-only change. It does not modify Lean theorem artifacts, so Strict Lean is intentionally not part of this focused validation.
