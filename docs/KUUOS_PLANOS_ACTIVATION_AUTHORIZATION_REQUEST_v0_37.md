# PlanOS Activation Authorization Request v0.37

PlanOS v0.37 converts the v0.36 materialization execution receipt into a bounded activation authorization request.

This layer preserves the materialization authorization and materialization execution receipt.

It does not grant activation authorization.

It does not invoke ActOS.

It does not grant execution authority.

## Input

The source input is `kuuos_planos_materialization_execution_receipt_v0_36`.

The source must be ready.

The selected candidate must remain bound to the materialization execution receipt record.

The materialization execution receipt must preserve both materialization authorization and materialization execution.

## Output

The runtime emits `PLANOS_ACTIVATION_AUTHORIZATION_REQUEST_READY` when all source and boundary checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source execution receipt digest
- source authorization grant digest
- activation authorization request record
- receipt digest

## Required boundary

- request owned by PlanOS = true
- source materialization execution receipt preserved = true
- selected candidate bound to execution receipt = true
- materialization execution preserved = true
- activation authorization request only = true
- materialization authorization granted = true
- materialization executed = true

## Closed boundary

- activation authorization granted = false
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
- missing source execution receipt digest
- missing source execution receipt record
- source boundary promotion
- source execution receipt record promotion
- selected candidate id mismatch
- selected candidate digest mismatch

## Authority boundary

This layer is a request layer.

It is not an authorization grant.

It is not an ActOS invocation.

It is not execution authority.

It is not truth authority.

It is not external commit authority.

It is not memory overwrite authority.

It is not blocker release authority.
