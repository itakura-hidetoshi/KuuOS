# PlanOS Memory Overwrite Receipt v0.50

PlanOS v0.50 converts the v0.49 memory overwrite authorization grant into a bounded memory overwrite receipt.

This layer records memory overwrite inside the PlanOS authority chain.

It does not grant truth authority or blocker release authority.

## Input

The source input is `kuuos_planos_memory_overwrite_authorization_grant_v0_49`.

The source must be ready.

The selected candidate must remain bound to the memory overwrite authorization grant record.

The source must preserve:

- external commit
- external commit closeout
- memory overwrite authorization grant

The source must keep closed:

- memory overwrite application before this receipt
- truth authority
- blocker release

## Output

The runtime emits `PLANOS_MEMORY_OVERWRITE_RECEIPT_READY` when the source grant checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source memory overwrite authorization grant digest
- source memory overwrite authorization request digest
- memory overwrite receipt record
- receipt digest

## Required boundary

- receipt owned by PlanOS = true
- source memory overwrite authorization grant preserved = true
- selected candidate bound to memory overwrite grant = true
- external commit preserved = true
- external commit closeout preserved = true
- memory overwrite authorization grant preserved = true
- memory overwrite receipt only = true
- memory overwrite authorization requested = true
- memory overwrite authorization granted = true
- memory overwrite granted = true

## Closed boundary

- truth authority granted = false
- blocker release granted = false

## Authority boundary

This layer is a memory overwrite receipt only.

It is not truth authority.

It is not blocker release authority.
