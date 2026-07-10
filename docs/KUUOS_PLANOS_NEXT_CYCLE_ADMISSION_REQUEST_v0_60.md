# PlanOS Next-Cycle Admission Request v0.60

PlanOS v0.60 converts the v0.59 blocker release closeout receipt into a bounded next-cycle admission request.

This layer requests admission to the next cycle.

It does not grant admission or start the next cycle.

## Input

The source input is `kuuos_planos_blocker_release_closeout_receipt_v0_59`.

The source must be ready.

The selected candidate must remain bound to the blocker release closeout receipt record.

The source must preserve:

- memory overwrite
- memory overwrite closeout receipt
- closed memory overwrite cycle
- truth authority authorization grant
- recorded truth authority
- closed truth authority cycle
- blocker release authorization request
- blocker release authorization grant
- recorded blocker release
- closed blocker release cycle

The source must keep next-cycle admission unopened before this request is recorded.

## Output

The runtime emits `PLANOS_NEXT_CYCLE_ADMISSION_REQUEST_READY` when the source blocker release closeout checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source blocker release closeout receipt digest
- next-cycle admission request record
- receipt digest

## Required boundary

- request owned by PlanOS = true
- source blocker release closeout preserved = true
- selected candidate bound to blocker release closeout = true
- memory overwrite preserved = true
- memory overwrite closeout preserved = true
- cycle closed preserved = true
- truth authority authorization grant preserved = true
- truth authority preserved = true
- truth authority cycle closed preserved = true
- blocker release authorization request preserved = true
- blocker release authorization grant preserved = true
- blocker release preserved = true
- blocker release cycle closed preserved = true
- next cycle admission request only = true
- next cycle admission requested = true

## Closed boundary

- next cycle admission granted = false
- next cycle started = false

## Authority boundary

This layer requests next-cycle admission without granting admission or starting the next cycle.

The request recorder itself remains non-authoritative.
