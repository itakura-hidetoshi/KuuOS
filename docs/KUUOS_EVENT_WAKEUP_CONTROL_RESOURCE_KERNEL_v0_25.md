# KuuOS Event / Wake-up, User Control, and Resource Governor v0.25

## Purpose

v0.25 completes dependency rank 6 of the autonomous-agent architecture:

```text
external trigger
→ control-state check
→ finite resource admission
→ optional model degradation
→ fresh bounded cycle proposal
→ fresh PlanOS / license / ActOS authorization
```

The conversational model is not converted into a hidden daemon. Always-on continuity is supplied by an explicit external event surface and an append-only event ledger.

## Trigger classes

```text
clock_schedule
queue_available
lease_expiry
dependency_completed
resource_replenished
webhook_connector_event
user_command
monitoring_condition
```

Each trigger binds a source identity, event digest, condition, due time, resource request, requested model tier, and bounded cycle duration.

## Wake-up boundary

A successful wake-up creates only a queue proposal for a new cycle.

```text
new bounded cycle
fresh semantic plan required
fresh cycle license required
fresh ActOS authorization required
inherited execution authority = false
queue entry only = true
running = false
verified = false
```

The trigger, wake-up proposal, or status record cannot execute a connector or inherit a previous capability lease.

## User control and status

The foreground user-control path remains available independently of queued work.

Supported commands:

```text
inspect
explain
pause
resume
cancel
reprioritize
revise_mission
revise_constraint
approve_permission
increase_budget
force_replan
release_dead_letter
handover
```

`inspect` and `explain` are read-only status operations. Permission approval records an approval digest but does not execute or activate a plan. Pause, cancel, and handover preempt later wake-ups. Cancel and handover are terminal for autonomous continuation.

The status contract includes:

```text
state
reason
completed work
checkpoint
next condition
resource state
worker state
valid user actions
```

## Resource and model governor

Every mission uses a finite envelope containing:

- governance caps
- current hard limits
- reserve floors
- remaining token, API, cost, storage, and worker budgets
- finite cycle count
- allowed and preferred model tiers
- expiry and renewal policy

A budget update requires independent user-control budget authority and may never exceed immutable governance caps.

Resource decisions are:

```text
ADMIT
DEGRADE_MODEL
RENEWAL_REQUIRED
PAUSE_RESOURCE_EXHAUSTED
REJECT_CONTROL_PAUSED
REJECT_CONTROL_CANCELLED
REJECT_HANDOVER
```

Model degradation is attempted before an unlicensed escalation. Resource exhaustion creates pause, replan, or renewal feedback. A resource-replenishment event never resumes the mission automatically; an authorized `resume` command is required.

## Persistence

```text
event-wakeup-initial.json
event-wakeup-ledger.jsonl
event-wakeup-snapshot.json
```

The ledger is authoritative. Duplicate trigger and control payloads replay idempotently without another append. Stale events are rejected. Snapshot repair is an explicit ledger replay operation.

## Lower-layer preservation

The v0.24 transaction final receipt remains canonical. v0.25 neither rewrites the transaction outcome nor converts effect confirmation into wake-up authority.

Core invariants:

```text
wake-up != authority
queue != running
running != verified
resource replenishment != resume
permission approval != execution
budget increase != self-license
source transaction receipt remains canonical
```

## Formalization

Lean module:

```text
KUOS.OpenHorizon.EventWakeupControlResourceKernelV0_25
```

Final theorem:

```lean
event_wakeup_control_resource_boundary
```

It composes the v0.24 transaction commit boundary with external-trigger, bounded-wake-up, foreground control, finite-resource, and replay-safe persistence boundaries.

## Validation

```bash
PYTHONPATH=. python scripts/check_event_wakeup_control_resource_v0_25.py
PYTHONPATH=. python -m unittest -v tests.test_event_wakeup_control_resource_v0_25
PYTHONPATH=. python scripts/check_transactional_effect_reconciliation_v0_24.py
PYTHONPATH=. python scripts/check_nonmarkov_cognitive_loop_v0_23.py
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true \
  build KUOS.OpenHorizon.EventWakeupControlResourceKernelV0_25
lake -KleanArgs=-DwarningAsError=true \
  -KleanArgs=-DsorryAsError=true build KuuOSFormal
```
