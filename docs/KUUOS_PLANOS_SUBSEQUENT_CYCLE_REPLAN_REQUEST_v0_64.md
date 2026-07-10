# PlanOS Subsequent-Cycle Replan Request v0.64

PlanOS v0.64 converts the v0.63 next-cycle closeout receipt into a bounded subsequent-cycle replan request.

This layer requests replanning for the subsequent cycle.

It does not start candidate generation or request subsequent-cycle admission.

## Input

The source input is `kuuos_planos_next_cycle_closeout_receipt_v0_63`.

The source must be ready.

The selected candidate must remain bound to the next-cycle closeout receipt record.

The source must preserve the complete memory overwrite, truth authority, blocker release, next-cycle admission, start, and closeout chain.

The source must record a closed next cycle with no subsequent-cycle replan request already promoted.

## Output

The runtime emits `PLANOS_SUBSEQUENT_CYCLE_REPLAN_REQUEST_READY` when the source closeout checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source next-cycle closeout receipt digest
- subsequent-cycle replan request record
- receipt digest

## Required boundary

- request owned by PlanOS = true
- source next-cycle closeout receipt preserved = true
- selected candidate bound to next-cycle closeout = true
- memory overwrite and closeout preserved = true
- truth authority and closeout preserved = true
- blocker release and closeout preserved = true
- next-cycle admission request and grant preserved = true
- next-cycle start and closeout receipts preserved = true
- next cycle admission requested = true
- next cycle admission granted = true
- next cycle started = true
- next cycle cycle closed = true
- subsequent cycle replan request only = true
- subsequent cycle replan requested = true

## Closed boundary

- subsequent cycle candidate generation started = false
- subsequent cycle admission requested = false

## Authority boundary

This layer opens only the subsequent-cycle replan request.

The request recorder itself remains non-authoritative.
