# KuuOS Cooperative Execution Supervisor v0.16

## Purpose

Cooperative Execution Supervisor v0.16 turns the v0.15 handoff protocol into an executable, resumable job state machine.

A long task is divided into a finite ordered list of allowlisted operations. The supervisor executes only a bounded slice, persists the resulting job state, emits a status receipt, and releases the foreground prompt. The same checkpoint can then be resumed either by a later foreground instruction or by an explicitly leased background worker.

The design does not claim that every host platform supports concurrent background execution. It provides the durable runtime contract that a background worker can consume when one is available.

## Runtime position

```text
v0.16 Cooperative Execution Supervisor
  -> allowlisted operation registry
  -> bounded execution slices
  -> durable job state
  -> foreground yield
  -> explicit continuation tickets
  -> user command application
v0.15 Resumable Execution Handoff
  -> stop reason, checkpoint, feedback, lease protocol
v0.14 Context Gerbe Coherence
v0.13 Context Gauge Atlas
v0.12 Horizon Gauge Arbitration
v0.11 Delayed Multi-Horizon Credit
```

v0.16 does not alter lower licenses, hard gates, effect authority, replay rules, or gauge semantics.

## Job model

A supervised job contains:

- job identity and source-parent digest
- an ordered immutable step manifest
- current step index
- completed step identifiers
- step receipts
- execution mode: foreground or background
- current supervisor state
- remaining budget
- latest checkpoint and feedback digests
- active continuation ticket
- processed command digests
- generation and job-state digest

Each step contains:

- `step_id`
- `operation_id`
- operation input
- estimated cost units
- maximum attempts
- optional required permission

The manifest digest is immutable after job creation. User scope changes create a new manifest revision rather than rewriting past receipts.

## Allowlisted operation registry

The supervisor never evaluates arbitrary source text, shell strings, or dynamically supplied callables from the job packet.

An external host supplies an allowlisted registry:

```text
operation_id -> trusted executor
```

A step may run only when its `operation_id` exists in that registry. Missing operations produce a visible deterministic block and release the foreground prompt.

## Bounded slice

A slice is limited by all configured bounds:

- maximum steps per slice
- maximum cost per slice
- optional foreground time budget supplied by the host

The supervisor checks cost before starting each step. It never starts a step whose estimate would exceed the slice budget or the remaining job budget.

After a successful foreground slice with unfinished work, the state becomes `foreground_yielded`. The receipt exposes:

- completed work
- next step
- checkpoint
- whether background execution is supported
- permitted user actions

The foreground prompt is then released.

## Step results

A trusted executor returns one of:

- `success`
- `transient_error`
- `deterministic_bug`
- `waiting_external`
- `permission_denied`
- `needs_user_input`
- `cancelled`

v0.16 converts non-success results into a v0.15 observation and delegates pause classification, checkpoint, feedback, and background ticket generation to v0.15.

A successful result records an append-only step receipt containing the input digest, output digest, cost, summary, and attempt count.

## Foreground yield

Foreground yield is not a failure. It means the bounded slice completed safely while the job still has work remaining.

```text
foreground_yielded
  -> checkpoint persisted
  -> feedback emitted
  -> foreground prompt released
  -> user may continue, queue background, revise scope, or cancel
```

Foreground yield never authorizes additional effects by itself.

## Background continuation

When the user or policy selects background continuation, v0.16 creates a continuation ticket bound to:

- job-state digest
- next step
- checkpoint digest
- manifest digest

The ticket uses the v0.15 bounded lease and heartbeat protocol. A worker must claim the ticket before executing a slice.

Each background slice is still bounded. When unfinished, it emits a replacement queued ticket for the next slice. Completion closes the ticket and marks the job completed.

A queued ticket means continuation is durable, not that a worker is currently active.

## User commands

Commands are digest-bound and idempotent. Supported commands include:

- `continue_foreground`
- `queue_background`
- `increase_budget`
- `reduce_scope`
- `retry_now`
- `retry_later`
- `revise_input`
- `grant_permission`
- `provide_input`
- `cancel_job`

A command may change only fields explicitly permitted for the current state. It cannot bypass lower authority or rewrite completed receipts.

## Error and retry policy

Transient errors may use bounded retries through v0.15. Deterministic bugs and invariant violations do not automatically repeat.

A step that reaches its maximum attempts becomes user-guidance-required. The job remains checkpointed and inspectable.

## Persistence and replay

The supervisor bundle stores:

- current jobs
- append-only slice receipts
- append-only step receipts
- continuation tickets
- command ledger
- processed slice digests
- processed command digests

Replaying the same slice or command digest returns the stored result without duplicating effects, receipts, or tickets.

## Required boundaries

- only allowlisted operations may execute
- every slice is finite and bounded
- a step starts only when its estimated cost fits available bounds
- every successful step has a receipt
- every non-success result is handed to v0.15
- every unfinished foreground slice yields the prompt
- background queueing remains explicit and observable
- queued does not mean leased or running
- completed receipts are append-only
- duplicate slices and commands are idempotent
- user commands do not bypass lower authority
- v0.15 and lower semantics remain preserved
- graph semantics remain forbidden

## Initial acceptance cases

1. A three-step foreground job executes one bounded step and yields the prompt.
2. A second foreground command resumes from the next step without repeating the first.
3. Queue-background creates a continuation ticket bound to the current checkpoint.
4. A worker leases the ticket and executes a bounded background slice.
5. A successful final slice completes the job.
6. A transient executor result produces v0.15 retry feedback.
7. A deterministic bug produces `blocked_bug` without blind retry.
8. A missing operation identifier is visible as a deterministic block.
9. Insufficient cost produces a v0.15 budget pause before step execution.
10. Duplicate slice and command commits are idempotent.
