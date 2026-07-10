# PlanOS Truth Authority Authorization Request v0.52

PlanOS v0.52 converts the v0.51 memory overwrite closeout receipt into a bounded truth authority authorization request.

This layer requests truth authority authorization.

It does not grant truth authority authorization, truth authority, or blocker release authority.

## Input

The source input is `kuuos_planos_memory_overwrite_closeout_receipt_v0_51`.

The source must be ready.

The selected candidate must remain bound to the memory overwrite closeout receipt record.

The source must preserve:

- memory overwrite
- memory overwrite closeout receipt
- closed memory overwrite cycle

The source must keep closed:

- truth authority
- blocker release

## Output

The runtime emits `PLANOS_TRUTH_AUTHORITY_AUTHORIZATION_REQUEST_READY` when the source memory overwrite closeout checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source memory overwrite closeout receipt digest
- truth authority authorization request record
- receipt digest

## Required boundary

- request owned by PlanOS = true
- source memory overwrite closeout preserved = true
- selected candidate bound to memory overwrite closeout = true
- memory overwrite preserved = true
- memory overwrite closeout preserved = true
- cycle closed preserved = true
- truth authority authorization request only = true
- truth authority authorization requested = true

## Closed boundary

- truth authority authorization granted = false
- truth authority granted = false
- blocker release granted = false

## Authority boundary

This layer is a truth authority authorization request only.

It is not a truth authority authorization grant.

It is not truth authority.

It is not blocker release authority.
