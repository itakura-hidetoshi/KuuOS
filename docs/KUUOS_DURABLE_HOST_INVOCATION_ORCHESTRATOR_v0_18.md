# KuuOS Durable Host Invocation Orchestrator v0.18

## Purpose

Durable Host Invocation Orchestrator v0.18 coordinates multiple resumable jobs and multiple host workers above the single-invocation boundary of v0.17.

v0.18 adds:

- weighted least-served job fairness
- least-served healthy-worker ordering
- finite dispatch capacity and backpressure classification
- stale, draining, degraded, and unhealthy worker exclusion
- structural candidate observation and dead-letter quarantine
- explicit dead-letter release
- digest-bound cycle planning and idempotent cycle replay
- atomic persistence of supervisor and orchestrator state
- append-only cycle receipts and audit history

It does not replace the existing runtime daemon and does not call external connectors from inside runtime.

## Authority split

```text
v0.18 orchestrator
  owns: fair ordering, worker selection, capacity, backpressure, observation, dead-letter metadata
  does not own: job eligibility, lease validity, step execution, operation authority

v0.17 host adapter
  owns: projection eligibility, host license, one-job one-slice invocation, lease claim, persistence receipt

v0.16 supervisor
  owns: job state, step prefix, budget, commands, background ticket lifecycle
```

v0.18 consumes the candidate set emitted by v0.17 projection. It may choose a different eligible candidate for fairness, but it cannot make a blocked candidate eligible.

## Durable orchestrator state

The orchestrator state is separate from the supervisor bundle. It contains only orchestration metadata:

- generation and cycle index
- per-job service counts
- per-job last-served cycle
- per-worker service counts
- per-worker failure counts
- structural candidate observation counters
- append-only dead-letter records
- append-only dead-letter releases
- processed plan digests
- bounded cycle history

The state grants no execution authority and cannot overwrite completed supervisor receipts.

## Worker health

Every worker publishes a digest-bound report containing:

- worker identifier
- observation timestamp and sequence
- operational status
- operation allowlist
- capacity slots
- failure streak

A worker is dispatchable only when:

- the report digest is valid
- the report is fresh under policy TTL
- status is healthy, or degraded is explicitly allowed
- status is not draining or offline
- capacity is positive
- failure streak is below the configured bound
- at least one licensed and registered operation is shared

A worker report is observational. It does not itself claim a job.

## Fairness

For each eligible job `j`, v0.18 computes:

```text
virtual_service(j) = service_count(j) / positive_weight(j)
```

The next job is the minimum of:

1. virtual service
2. last-served cycle
3. job identifier

This is weighted least-served scheduling. A job may be dispatched at most once per orchestrator cycle.

Workers are ordered by:

1. worker service count
2. worker failure count
3. worker identifier

Each worker receives at most one assignment per cycle.

## Backpressure

The cycle plan records:

- queued or reclaimable job count
- eligible job count
- healthy worker count
- dispatch capacity
- deferred eligible count
- backpressure class

Classes are:

- `idle`
- `normal`
- `throttled`
- `saturated`
- `no_healthy_workers`
- `capability_gap_or_blocked`

Dispatch capacity is bounded by the minimum of eligible jobs, healthy workers, and policy maximum assignments.

## Dead-letter quarantine

Only repeated structural candidate defects are eligible for dead-letter observation, including invalid ticket digest, ticket/job mismatch, missing or mismatched checkpoint, invalid job state, or missing next step.

Worker capability gaps, temporary lack of capacity, rate limits, and transient execution errors are not dead-letter reasons.

After the configured observation threshold, v0.18 appends a dead-letter record keyed by job identifier and job-state digest. The supervisor job is not deleted or rewritten. A changed job-state digest is considered a new candidate state.

Release requires an explicit digest-bound operator packet and appends a release record. Past dead-letter history is never removed.

## Two-phase cycle

### Plan

Planning is read-only and binds:

- cycle identifier
- source supervisor bundle digest
- source orchestrator state digest
- policy digest
- host license digest
- worker report digests
- ordered healthy workers
- queue and backpressure metrics

### Execute

Execution consumes one plan. It sequentially invokes v0.17 once per selected worker, up to the policy cap. Every v0.17 call still claims at most one job and runs at most one bounded slice.

A new v0.18 plan is required for every later cycle.

## Replay

The plan digest is the orchestrator-cycle idempotency key. Once recorded, replay returns the current supervisor bundle and orchestrator state without another lease, step, budget charge, service increment, or dead-letter observation.

## Persistence

The file adapter writes supervisor output, orchestrator state, plan, and receipt by atomic JSON replacement. Audit history is append-only JSONL. Input paths are not overwritten by default.

## Acceptance cases

1. Three queued jobs and two healthy workers produce two distinct assignments.
2. A later cycle serves the previously unserved job before already served jobs.
3. One worker and one job are used at most once per cycle.
4. Queue depth beyond capacity is classified as throttled or saturated.
5. Stale, draining, offline, over-failure, or incompatible workers are excluded.
6. Repeated structural candidate defects enter dead-letter quarantine at the exact threshold.
7. Dead-letter release is explicit and append-only.
8. Duplicate plan replay performs no additional work.
9. v0.17 eligibility, license, lease, execution, and replay rules remain binding.
10. Supervisor and orchestrator outputs persist atomically with append-only audit receipts.
