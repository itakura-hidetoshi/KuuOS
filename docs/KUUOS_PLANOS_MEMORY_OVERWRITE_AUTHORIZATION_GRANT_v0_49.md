# PlanOS Memory Overwrite Authorization Grant v0.49

PlanOS v0.49 converts the v0.48 memory overwrite authorization request into a bounded authorization grant.

The layer grants authorization to apply the selected candidate's memory overwrite in a later receipt stage. It does not apply the overwrite itself and grants no truth authority or blocker release.

## Input

The source is `kuuos_planos_memory_overwrite_authorization_request_v0_48`.

The request must be ready, remain bound to the selected candidate, preserve the external commit closeout, and keep memory overwrite unapplied.

## Output

The runtime emits `PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_GRANT_READY` and appends exactly one grant record containing:

- selected candidate id and digest
- source request digest
- exact authorization grant digest
- memory overwrite authorization granted = true
- memory overwrite granted = false

## Required boundary

- grant owned by PlanOS = true
- source memory overwrite authorization request preserved = true
- selected candidate bound to memory overwrite request = true
- external commit preserved = true
- external commit closeout preserved = true
- memory overwrite authorization grant only = true
- memory overwrite authorization requested = true
- memory overwrite authorization granted = true

## Closed boundary

- memory overwrite granted = false
- truth authority granted = false
- blocker release granted = false

## Authority boundary

This artifact authorizes a later bounded memory overwrite receipt. It does not mutate memory, alter truth authority, or release blockers.
