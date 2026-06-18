# KuuOS Mission Contract Kernel v0.20

## Status

Implemented mission and commitment plane release above the merged v0.15-v0.19 substrate.

v0.20 implements:

1. Mission Contract Kernel
2. Goal Portfolio and Conflict Arbitration
3. Mission Renewal and Termination Kernel

It does not open execution, tool, network, shell, clinical, theorem, truth, memory-overwrite, or self-modification authority.

## Core distinction

```text
mission persistence != execution license
goal priority != effect authority
execution success != mission success
renewal != automatic continuation
```

The release converts transient intent into immutable, digest-bound mission lineage while preserving every lower execution boundary.

## Mission contract

A mission contract binds:

- mission and lineage identity
- append-only revision and parent contract digest
- issuer and governance root
- purpose
- success criteria
- failure criteria
- invariants
- prohibited outcomes
- finite resource envelope
- requested capability scope
- renewal policy
- user / governance override policy
- evidence authorization policy
- plurality-preserving goal policy
- validity and expiry interval
- non-authority and boundary declarations

The contract is immutable after sealing. Any continuation beyond its renewal boundary creates a successor contract rather than mutating the existing contract.

## Finite resource envelope

Every contract requires finite values for:

```text
max_total_cost
max_cycle_cost
max_cycles_before_renewal
max_active_goals
max_goal_count
reserve_floor
```

Required relations include:

```text
0 < max_cycle_cost <= max_total_cost
0 <= reserve_floor < max_total_cost
0 < max_active_goals <= max_goal_count
0 < max_cycles_before_renewal
```

NaN, infinity, negative cost, and silently unbounded values are rejected.

## Mission lifecycle

States:

```text
proposed
active
paused
renewal_required
completed
terminated
handed_over
```

Terminal states are stable. A terminal mission cannot silently resume.

Lifecycle decisions:

```text
continue
pause
resume
renewal_required
complete
terminate
handover
no_change
```

Each decision is bound to the exact contract and source state digest.

Applied decision digests are stored append-only. Reapplying the same decision returns `REPLAYED` and does not append a second transition.

## Evidence boundary

Mission evidence records:

- exact contract and source state
- source identity and role
- evidence level
- confidence
- success or failure assertion
- invariant or prohibited-outcome observation
- recoverability and handover requirement
- evidence references

Completion, failure, or invariant decisions require an authorized source role, an allowed evidence level, and the configured minimum confidence.

Unconfirmed success or failure evidence pauses the mission rather than becoming terminal truth.

v0.20 does not claim to implement the future v0.22 independent Outcome Verifier. It only enforces authorization and evidence-contract boundaries around supplied verification evidence.

## Commands and control

Mission commands are role-scoped and stale-state-bound.

Supported commands:

```text
pause
resume
terminate
handover
request_renewal
renew
```

Every command requires:

- actor identity
- actor role
- explicit reason
- exact contract digest
- exact source state digest
- role authorization in the mission override policy

A stale or unauthorized command is rejected before transition.

## Goal portfolio

A goal proposal binds:

- mission and contract digest
- objective
- priority weight
- horizon
- expected outcomes
- requested capabilities
- dependencies
- requested finite cost and cycles
- optional exclusive group

The goal proposal grants no effect authority.

Goal portfolio arbitration classifies each goal as:

```text
active
deferred
held
rejected
```

Conflict residues include:

```text
prohibited_outcome_collision
capability_scope_exceeded
dependency_missing
resource_request_exceeds_envelope
exclusive_goal_conflict
exclusive_goal_tie
human_arbitration_required
```

Equal-priority goals in the same exclusive group are held for human arbitration rather than resolved by an arbitrary global winner.

Eligible goals receive normalized weights. When multiple eligible goals exist, the configured plurality floor remains visible. The recommended goal is advisory and has `recommendation_grants_effect_authority = false`.

## Renewal and termination

Renewal requires:

- a mission state bound to the parent contract
- an explicit `renew` command
- an authorized renewal role
- remaining renewal count
- a new validity interval
- a resource envelope compatible with the parent renewal policy

The successor contract contains:

```text
revision = parent revision + 1
parent_contract_digest = exact parent digest
```

The successor state contains the exact predecessor state digest.

When resource increase is not explicitly allowed, a successor contract may not increase total cost, cycle cost, renewal cycle count, active goal capacity, or total goal capacity.

Termination paths include:

- explicit authorized terminate command
- authorized nonrecoverable failure
- authorized invariant breach
- authorized prohibited-outcome evidence

Recoverable authorized failure may hand over instead of terminate.

## Failure states

Representative failures:

```text
mission_ambiguous
success_criteria_missing
contract_validity_window_invalid
resource_envelope_not_finite
authority_scope_forbidden
mission_command_role_not_authorized
command_source_state_stale
evidence_source_state_stale
evidence_success_failure_conflict
success_evidence_not_authorized
mission_transition_forbidden
renewal_role_not_authorized
renewal_limit_reached
renewal_resource_increase_forbidden
goal_count_exceeds_contract
prohibited_outcome_collision
capability_scope_exceeded
human_arbitration_required
mission_contract_digest_invalid
mission_state_digest_invalid
```

## Persistence

The release provides:

- atomic JSON writes
- overwrite protection by default
- explicit overwrite opt-in
- append-only JSONL audit records
- immutable contract and portfolio packets
- append-only state transition history

## v0.19 readiness overlay

The v0.19 architecture manifest remains immutable.

v0.20 adds a digest-bound status overlay that marks these components implemented:

```text
mission_contract_kernel
goal_portfolio_arbitration
mission_renewal_termination
```

Resolved readiness becomes:

```text
implemented: 4
open_gap: 10
partial_gap: 2
next dependency rank: 2
next release: v0.21
```

The next implementation target is the Observation and Belief-State Kernel.

## Validation

Dedicated kernel coverage includes:

- mission construction and digest validation
- finite resource rejection
- authority-scope rejection
- role-scoped commands
- stale command rejection
- authorized and unauthorized evidence
- pause, resume, renewal, completion, termination stability
- replay idempotency
- successor contract lineage
- successor state lineage
- goal plurality and normalized weights
- prohibited outcome rejection
- exclusive-goal human arbitration
- resource-envelope goal hold
- forbidden resource increase
- state tamper rejection
- atomic persistence and append-only audit
- v0.19 readiness overlay resolution

## Formal status

A Lean source surface records bounded resource, non-authority, explicit renewal, and monotonic transition properties.

The source file is proof-facing. It is not theorem authority, and it is only considered compiled when an actual repository Lean environment runs it successfully.
