# PlanOS Materialization Authorization Request v0.33

This layer advances the v0.32 selected candidate materialization preflight into a bounded materialization authorization request.

It is request-only.

It does not authorize materialization.

It does not execute materialization.

It does not authorize activation.

It does not invoke ActOS.

It does not grant execution.

## Source

- source version = `kuuos_planos_selected_candidate_materialization_preflight_v0_32`
- source status = `PLANOS_SELECTED_CANDIDATE_MATERIALIZATION_PREFLIGHT_READY`
- selected candidate remains bound to the materialization preflight record

## Output

The runtime emits:

- selected candidate id
- selected candidate digest
- source preflight digest
- materialization authorization request record
- receipt digest

## Boundary

- request owned by PlanOS = true
- source materialization preflight preserved = true
- selected candidate bound to preflight = true
- materialization authorization request only = true
- materialization authorization granted = false
- materialization executed = false
- activation authorization granted = false
- ActOS invoked = false
- execution granted = false
- truth authority granted = false
- memory overwrite granted = false
- blocker release granted = false
- external commit granted = false

## Governance role

The request is an explicit governance surface between preflight and any future authorization decision.

It separates asking for authorization from granting authorization.

The distinction is machine-readable, runtime-checked, and formally represented.

## Non-authority invariant

A successful v0.33 receipt only proves that a selected candidate has been carried forward into an authorization-request envelope.

It does not prove that the candidate should be materialized.

It does not authorize repository mutation, external effects, clinical action, legal action, or execution.
