# PlanOS Memory Overwrite Authorization Request v0.48

PlanOS v0.48 converts the v0.47 external commit closeout receipt into a bounded memory overwrite authorization request.

This layer requests memory overwrite authorization.

It does not grant memory overwrite authorization.

It does not perform memory overwrite.

It does not grant truth authority or blocker release authority.

## Input

The source input is `kuuos_planos_external_commit_closeout_receipt_v0_47`.

The source must be ready.

The selected candidate must remain bound to the external commit closeout receipt record.

The source must preserve:

- external commit
- external commit closeout
- cycle closed

The source must keep closed:

- memory overwrite
- truth authority
- blocker release

## Output

The runtime emits `PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_READY` when the source closeout checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source external commit closeout digest
- source external commit receipt digest
- memory overwrite authorization request record
- receipt digest

## Required boundary

- request owned by PlanOS = true
- source external commit closeout preserved = true
- selected candidate bound to external commit closeout = true
- external commit preserved = true
- external commit closeout preserved = true
- cycle closed preserved = true
- memory overwrite authorization request only = true
- memory overwrite authorization requested = true

## Closed boundary

- memory overwrite authorization granted = false
- memory overwrite granted = false
- truth authority granted = false
- blocker release granted = false

## Authority boundary

This layer is a memory overwrite authorization request only.

It is not a memory overwrite authorization grant.

It is not memory overwrite authority.

It is not truth authority.

It is not blocker release authority.
