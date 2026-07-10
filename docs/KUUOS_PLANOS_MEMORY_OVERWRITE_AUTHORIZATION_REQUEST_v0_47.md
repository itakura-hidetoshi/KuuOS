# PlanOS Memory Overwrite Authorization Request v0.47

PlanOS v0.47 converts the v0.46 external commit receipt into a bounded memory overwrite authorization request.

This layer requests memory overwrite authorization.

It does not grant memory overwrite authorization.

It does not perform memory overwrite.

It does not grant truth authority or blocker release authority.

## Input

The source input is `kuuos_planos_external_commit_receipt_v0_46`.

The source must be ready.

The selected candidate must remain bound to the external commit receipt record.

The source must preserve:

- materialization execution
- activation authorization
- ActOS invocation
- literature grounding
- dynamic planning compute accounting
- selective foresight
- uncertainty calibration
- memory mismatch review
- counterfactual coverage
- cost, safety, and robustness evaluation
- execution authorization grant
- execution receipt
- external commit authorization request
- external commit authorization grant
- external commit receipt

The source must keep closed:

- truth authority
- memory overwrite
- blocker release

## Output

The runtime emits `PLANOS_MEMORY_OVERWRITE_AUTHORIZATION_REQUEST_READY` when the source external commit receipt checks pass.

The output contains:

- selected candidate id
- selected candidate digest
- source external commit receipt digest
- source external commit authorization grant digest
- memory overwrite authorization request record
- receipt digest

## Required boundary

- request owned by PlanOS = true
- source external commit receipt preserved = true
- selected candidate bound to external commit receipt = true
- materialization execution preserved = true
- activation authorization preserved = true
- ActOS invocation preserved = true
- literature grounding preserved = true
- dynamic planning compute accounted = true
- selective foresight preserved = true
- uncertainty calibration preserved = true
- memory mismatch review preserved = true
- counterfactual coverage preserved = true
- cost, safety, and robustness evaluation preserved = true
- execution authorization grant preserved = true
- execution receipt preserved = true
- execution authorization requested = true
- execution authorization granted = true
- execution granted = true
- external commit authorization request preserved = true
- external commit authorization grant preserved = true
- external commit receipt preserved = true
- external commit authorization requested = true
- external commit authorization granted = true
- external commit granted = true
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
