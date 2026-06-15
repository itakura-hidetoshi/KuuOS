# KuuOS Adapter Capability Gauge v0.6

## Purpose

v0.6 replaces static adapter priority as the primary selector with a context-local,
evidence-calibrated capability gauge.

```text
source batch
  -> normalized context
  -> adapter capability sections
  -> capability-aware adapter selection
  -> one v0.5 federation cycle
  -> committed effect receipt
  -> capability curvature
  -> updated adapter connection
```

Static registry priority remains available only as a deterministic tie-break.

## Upstream stack

```text
v0.1  Open-Horizon Telos Genesis
v0.2  Open-Horizon Commitment Gauge
v0.3  Active Gauge Intervention Loop
v0.4  Renewable Gauge Supervisor
v0.5  Event Source and Adapter Federation
v0.6  Adapter Capability Gauge
```

v0.6 selects one adapter and delegates exactly one finite cycle to v0.5. The child
cycle continues to use v0.4, v0.3, v0.2, and v0.1 without bypassing their ledgers or
digest bindings.

## Context-local sections

A capability section is keyed by:

```text
federation adapter ID
+
context key
```

The context key is derived from:

- normalized wake kind;
- source kinds;
- source IDs;
- signal kinds.

World-state values and event IDs do not directly define a new capability section.
Thus repeated observations in the same operational context update the same section,
while a resource-change context can retain an independent prior and history.

Each section records:

```text
observation count
selection count
success / partial / blocked counts
mean progress
mean benefit
mean harm
mean recoverability
mean confidence
mean utility
connection coefficient
last capability curvature
cumulative absolute curvature
last effect and evidence digests
```

## Observed utility

The initial v0.6 utility projection is:

```text
U = clamp(
      0.35 * observed_benefit
    + 0.20 * progress_delta
    + 0.20 * recoverability
    + 0.15 * confidence
    + 0.10 * outcome_score
    - 0.50 * observed_harm
)
```

where:

```text
success -> 1.0
partial -> 0.5
blocked -> 0.0
```

This is a calibration coordinate, not a declaration of truth or general competence.
It applies only to the adapter and context section that produced the effect.

## Capability curvature

Let the current capability connection be `A` and the observed utility be `U`.

```text
F_cap = U - A
```

`F_cap` is the discrete capability curvature.

- positive curvature means the observed effect exceeded the current connection;
- negative curvature means it underperformed the current connection;
- zero curvature means the observation was locally flat relative to the estimate.

The update is:

```text
alpha_effective = learning_rate * effect_confidence
A_next = clamp(A + alpha_effective * F_cap)
```

The curvature, prior connection, observed utility, and updated connection are all
appended to the capability holonomy trace.

## Selection score

For an eligible adapter section with `n` observations:

```text
exploration = min(
  max_exploration_bonus,
  exploration_weight / sqrt(n + 1)
)

selection_score =
  connection
  + exploration
  - curvature_penalty * abs(last_curvature)
```

This gives unobserved adapters a finite opportunity to acquire evidence without
allowing exploration to grow without bound.

Candidate ordering is:

1. descending capability selection score;
2. descending static registry priority, only for a tie;
3. adapter ID.

The selected adapter is placed into a derived v0.5 registry in which only that
adapter is enabled for the child cycle.

## Adapter-specific routing

Registry entries may contain:

```text
capability_routing_table
```

After an adapter is selected, this routing table is passed to the child v0.5 plan.
This allows different local adapters to produce meaningfully different observed
effects under the same covariant action while sharing the same effect-receipt
contract.

The initial implementation still accepts only the existing local execution backend:

```text
qi_local_execution_adapter_v0_2
```

No external-network authority is inferred from a high capability score.

## Evidence and calibration binding

A calibration binds:

- capability run ID;
- selected federation adapter ID;
- exact adapter profile digest;
- context key;
- v0.3 effect receipt digest;
- v0.5 federated evidence digest;
- prior connection;
- observed utility;
- effective learning rate;
- capability curvature;
- updated connection;
- updated section and bundle digests.

The v0.5 evidence and v0.3 effect receipt must both validate and must match the child
result before calibration occurs.

## Recovery and replay

The capability ledger uses pending and committed phases.

- a committed capability run replays without another child cycle;
- deterministic child run IDs preserve v0.5 replay behavior;
- the selection packet is persisted before the child cycle;
- a pending run reuses the exact persisted selection;
- processed evidence digests prevent double calibration;
- if a crash occurs after bundle update, calibration can be reconstructed from the
  capability holonomy trace.

Thus one committed effect contributes at most one capability update.

## Outputs

```text
kuuos_adapter_capability_bundle_v0_6.json
kuuos_adapter_capability_selection_v0_6.json
kuuos_adapter_capability_calibration_v0_6.json
kuuos_adapter_capability_state_v0_6.json
kuuos_adapter_capability_receipt_v0_6.json
kuuos_adapter_capability_ledger_v0_6.jsonl
kuuos_adapter_capability_audit_v0_6.jsonl
```

All v0.1-v0.5 artifacts produced by the delegated child cycle remain present.

## Demonstrated adaptation

The integration check defines two local adapters:

```text
adapter A
  static priority: high
  prior connection: 0.72
  local route: hold

adapter B
  static priority: low
  prior connection: 0.55
  local route: advance_tick
```

The observed sequence is:

```text
cycle 1: A selected from prior; blocked effect; negative curvature
cycle 2: B selected through exploration and A's reduced connection; success
cycle 3: B retained from positive calibrated capability
cycle 4: resource-change context creates an independent section; A prior is used
```

This verifies both evidence-driven adapter switching and context locality.

## Formal surface

`formal/KUOS/OpenHorizon/AdapterCapabilityGaugeV0_6.lean` defines:

```lean
capabilityCurvature section observed = observed - section.connection
```

and the affine calibration:

```lean
calibrate alpha section observed
```

It proves:

- calibration is connection plus scaled curvature;
- a flat observation has zero curvature;
- a flat observation preserves the connection;
- full-rate calibration reaches the observation;
- one cycle selects zero or one adapter;
- repeated finite calibration cycles grow the observation history monotonically.

## Next layer

A natural v0.7 is a capability-aware adapter portfolio with shadow comparison:

```text
live selected adapter
+
non-actuating shadow candidates
  -> comparable effect predictions
  -> observed live effect
  -> counterfactual calibration residuals
  -> portfolio connection update
```

Only the live selected adapter would retain intervention authority; shadow candidates
would enrich capability geometry without duplicating effects.
