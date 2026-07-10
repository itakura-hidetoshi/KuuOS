# PlanOS Blocker Release Authorization Request v0.56

PlanOS v0.56 converts the v0.55 truth authority closeout receipt into a bounded blocker release authorization request.

This layer requests blocker release authorization only.

It does not grant blocker release authorization or release blockers.

## Input

The source input is `kuuos_planos_truth_authority_closeout_receipt_v0_55`.

The source must be ready.

The selected candidate must remain bound to the truth authority closeout receipt record.

The source must preserve:

- memory overwrite
- memory overwrite closeout receipt
- closed memory overwrite cycle
- truth authority authorization grant
- recorded truth authority
- closed truth authority cycle

The source must keep blocker release closed.

## Output

The runtime emits `PLANOS_BLOCKER_RELEASE_AUTHORIZATION_REQUEST_READY` when the source truth authority closeout checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source truth authority closeout receipt digest
- blocker release authorization request record
- receipt digest

## Required boundary

- request owned by PlanOS = true
- source truth authority closeout preserved = true
- selected candidate bound to truth authority closeout = true
- memory overwrite preserved = true
- memory overwrite closeout preserved = true
- cycle closed preserved = true
- truth authority authorization grant preserved = true
- truth authority preserved = true
- truth authority cycle closed preserved = true
- blocker release authorization request only = true
- blocker release authorization requested = true

## Closed boundary

- blocker release authorization granted = false
- blocker release granted = false

## Authority boundary

This layer requests blocker release authorization without granting or applying it.

The request recorder itself remains non-authoritative.
