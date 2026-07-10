# PlanOS Blocker Release Authorization Grant v0.57

PlanOS v0.57 converts the v0.56 blocker release authorization request into a bounded blocker release authorization grant.

This layer grants blocker release authorization.

It does not release blockers.

## Input

The source input is `kuuos_planos_blocker_release_authorization_request_v0_56`.

The source must be ready.

The selected candidate must remain bound to the blocker release authorization request record.

The source must preserve:

- memory overwrite
- memory overwrite closeout receipt
- closed memory overwrite cycle
- truth authority authorization grant
- recorded truth authority
- closed truth authority cycle
- blocker release authorization request

The source must keep blocker release authorization grant and blocker release closed.

## Output

The runtime emits `PLANOS_BLOCKER_RELEASE_AUTHORIZATION_GRANT_READY` when the source blocker release authorization request checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source blocker release authorization request digest
- blocker release authorization grant record
- receipt digest

## Required boundary

- grant owned by PlanOS = true
- source blocker release authorization request preserved = true
- selected candidate bound to blocker release request = true
- memory overwrite preserved = true
- memory overwrite closeout preserved = true
- cycle closed preserved = true
- truth authority authorization grant preserved = true
- truth authority preserved = true
- truth authority cycle closed preserved = true
- blocker release authorization request preserved = true
- blocker release authorization grant only = true
- blocker release authorization requested = true
- blocker release authorization granted = true

## Closed boundary

- blocker release granted = false

## Authority boundary

This layer grants blocker release authorization without applying blocker release.

The grant recorder itself remains non-authoritative.
