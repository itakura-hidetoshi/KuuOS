# KuuOS Resumable Execution Handoff v0.15

## Purpose

Resumable Execution Handoff v0.15 prevents silent stopping.

When execution cannot continue because of cost exhaustion, long external waiting, retry backoff, deterministic bugs, missing permission, or required user input, the runtime must emit an explicit status receipt before yielding the foreground interaction channel.

The receipt answers four questions:

1. What state is the work in?
2. Why did execution stop or pause?
3. What has already been completed and checkpointed?
4. What can resume it, and what may the user choose next?

## Runtime position

v0.15 is an additive liveness and interaction layer above the current execution stack.

It does not change v0.14 gerbe coherence, v0.13 atlas transport, v0.12 horizon arbitration, lower hard gates, licenses, effect authority, or replay rules.

```text
v0.15 Resumable Execution Handoff
  -> observable execution state
  -> durable checkpoint
  -> foreground release receipt
  -> optional background ticket
  -> user guidance surface
v0.14 Context Gerbe Coherence
v0.13 Context Gauge Atlas
v0.12 Horizon Gauge Arbitration
v0.11 Delayed Multi-Horizon Credit
v0.10-v0.2 existing runtime spine
```

## Non-silent execution states

The runtime classifies every observation into one of the following states:

- `running`
- `background_queued`
- `waiting_external`
- `budget_paused`
- `retry_backoff`
- `blocked_bug`
- `permission_blocked`
- `needs_user_input`
- `retry_exhausted`
- `completed`
- `cancelled`

Every state other than `running` releases the foreground prompt after writing a feedback receipt. Paused and blocked states remain observable; they are not converted into an unexplained terminal failure.

## Reason codes

The principal reason codes are:

- `cost_budget_exhausted`
- `external_latency`
- `rate_limited`
- `transient_error`
- `timeout`
- `deterministic_bug`
- `invariant_violation`
- `permission_denied`
- `user_input_required`
- `retry_limit_reached`
- `work_completed`
- `cancelled_by_user`
- `execution_active`

A human-readable summary accompanies every reason code. The summary may describe the failed component, last successful phase, and affected scope, but must not fabricate certainty about an unknown root cause.

## Feedback receipt

Before the foreground interaction channel is yielded, v0.15 emits a digest-bound receipt containing:

- job and attempt identity
- current state and reason code
- current phase
- completed and total work units
- progress fraction
- checkpoint digest
- last successful operation summary
- blocker summary
- resumability
- foreground prompt release status
- background disposition
- resume condition
- retry delay where applicable
- whether user guidance is required
- permitted user actions

Required invariant:

```text
paused_or_blocked(state)
  -> feedback_receipt_present
  -> foreground_prompt_released
```

## Cost exhaustion

When the remaining cost budget is smaller than the estimated next operation plus the configured reserve, execution must not disappear.

The state becomes either:

- `background_queued` when a background worker is available and background handoff is enabled, or
- `budget_paused` when no background worker is available.

The receipt states that the resume condition is `budget_replenished` and offers actions such as increasing the budget, changing scope, continuing manually, or cancelling.

Moving a job to the background does not manufacture budget. A background ticket waiting on budget remains visibly queued with the same resume condition.

## Long waits and external dependencies

When external waiting exceeds the configured foreground threshold, v0.15 may create a background ticket and release the foreground prompt.

The receipt records:

- elapsed wait
- waiting component or dependency
- resume condition `external_dependency_ready`
- optional next check delay

If background execution is not supported, the state remains `waiting_external`, but the prompt is still released and the user can issue other instructions.

## Transient errors and retry backoff

Rate limits, timeouts, and explicitly transient failures may enter bounded exponential backoff.

When background handoff is available, the retry is represented by a durable background ticket. Otherwise the state is `retry_backoff`.

Retry count and next retry delay are visible. Once the configured retry limit is reached, the state becomes `retry_exhausted` and requires user guidance. Infinite silent retry loops are forbidden.

## Deterministic bugs

Deterministic bugs, validation failures, invariant violations, and serialization defects are not automatically retried.

The runtime:

1. records a checkpoint,
2. emits `blocked_bug`,
3. describes the known failure boundary,
4. releases the foreground prompt,
5. offers actions such as inspecting the bug, revising input, applying a patch, reducing scope, or cancelling.

A bug state may be resumable after a changed input or implementation, but background execution is not automatically queued merely to repeat the same deterministic failure.

## Background tickets

A background ticket is a durable continuation request, not a claim that work has already resumed.

Each ticket contains:

- ticket identity
- job and attempt identity
- checkpoint digest
- reason code
- resume condition
- retry delay
- queue status
- lease owner
- lease expiration
- heartbeat time

Ticket states are:

- `queued`
- `leased`
- `completed`
- `failed`
- `cancelled`

A worker must claim a queued ticket using a bounded lease. Heartbeats extend the lease. An expired lease may be reclaimed. This avoids both duplicate execution and permanently invisible stalled workers.

## Foreground release

`foreground_prompt_released = true` means the runtime has completed the handoff transaction and the user-facing interaction may accept new instructions.

It does not mean the underlying platform necessarily supports concurrent execution. Platforms without a background worker must report `background_disposition = unsupported` or `not_queued`, while still returning the checkpoint and status receipt.

## User actions

The receipt provides only actions valid for the current state. Examples include:

- `continue_foreground`
- `queue_background`
- `increase_budget`
- `reduce_scope`
- `retry_now`
- `retry_later`
- `inspect_bug`
- `apply_patch`
- `revise_input`
- `grant_permission`
- `provide_input`
- `cancel_job`

These actions are proposals, not authority escalation. Existing approval and execution boundaries remain in force.

## Persistence and replay

The v0.15 bundle persists:

- latest job status
- append-only feedback history
- append-only checkpoint history
- background queue
- handoff ledger
- processed attempt digests

The same attempt digest is processed at most once. Replaying it returns the stored state without appending duplicate feedback, checkpoints, or background tickets.

## Required boundaries

The implementation must preserve all of the following:

- no silent pause or block
- every non-running state has explicit feedback
- every paused or blocked state releases the foreground prompt
- background queueing is explicit and observable
- background queueing does not imply worker execution
- deterministic bugs are not blindly auto-retried
- retry count and delay are visible
- checkpoints are digest-bound
- background leases are bounded and reclaimable
- duplicate attempts are idempotent
- user actions do not bypass lower authority
- existing v0.14 and lower semantics are not overwritten
- graph semantics remain forbidden

## Formal obligations

The Lean surface should prove:

- every paused state requires feedback
- every paused state requires foreground release
- appending a handoff cycle strictly increases feedback and checkpoint records
- a background ticket has a checkpoint
- bounded progress lies in the closed unit interval
- retry delay is nonnegative

## Initial kernel acceptance cases

The initial kernel must cover:

1. Cost exhaustion with a background worker produces `background_queued`, a checkpoint, feedback, and foreground release.
2. Cost exhaustion without a background worker produces `budget_paused`, feedback, and foreground release.
3. Long external waiting produces an observable background or waiting state.
4. A transient failure produces bounded retry backoff and exposes retry count.
5. A deterministic bug produces `blocked_bug`, no automatic background retry, and user guidance actions.
6. A permission failure produces `permission_blocked`.
7. Required user input produces `needs_user_input`.
8. Duplicate attempt commit is idempotent.
9. A queued ticket can be leased, heartbeated, and reclaimed after lease expiry.
10. No non-running result lacks a feedback receipt or foreground release.
