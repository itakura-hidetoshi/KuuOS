# PlanOS Activation Authorization Grant v0.38

PlanOS v0.38 converts the v0.37 activation authorization request into a bounded activation authorization grant.

This layer preserves materialization authorization and materialization execution.

It grants activation authorization.

It does not invoke ActOS.

It does not grant execution authority.

## Input

The source input is `kuuos_planos_activation_authorization_request_v0_37`.

The source must be ready.

The selected candidate must remain bound to the activation authorization request record.

The source request must preserve materialization authorization and materialization execution while keeping activation authorization closed.

## Output

The runtime emits `PLANOS_ACTIVATION_AUTHORIZATION_GRANT_READY` when all source and boundary checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source activation request digest
- source execution receipt digest
- activation authorization grant record
- receipt digest

## Required boundary

- grant owned by PlanOS = true
- source activation authorization request preserved = true
- selected candidate bound to activation request = true
- materialization execution preserved = true
- activation authorization grant only = true
- materialization authorization granted = true
- materialization executed = true
- activation authorization granted = true

## Closed boundary

- ActOS invoked = false
- execution granted = false
- truth authority granted = false
- memory overwrite granted = false
- blocker release granted = false
- external commit granted = false

## Blockers

The runtime blocks:

- source version mismatch
- source not ready
- missing source activation request digest
- missing source activation request record
- source boundary promotion
- source activation request record promotion
- selected candidate id mismatch
- selected candidate digest mismatch

## Authority boundary

This layer grants activation authorization only.

It is not ActOS invocation.

It is not execution authority.

It is not truth authority.

It is not external commit authority.

It is not memory overwrite authority.

It is not blocker release authority.
