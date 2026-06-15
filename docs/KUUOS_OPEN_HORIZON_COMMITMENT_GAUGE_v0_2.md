# KuuOS Open-Horizon Commitment Gauge v0.2

## Purpose

v0.2 realizes open-horizon commitments as a discrete noncommutative gauge system rather than as a task graph.

```text
Telos local section
  + commitment connection
  + effect receipt as curvature
  -> local gauge correction
  -> covariant next action
  -> holonomy-preserving continuation
```

The base manifold is the open-ended context space with coordinates such as telos generation, commitment phase, and effect epoch. A generated goal is represented by a local section over a chart. A commitment defines the local connection used to parallel-transport that section into action. The observed effect measures curvature: mismatch between intended transport and realized consequence.

## Gauge dictionary

| Runtime concept | Gauge-theoretic meaning |
|---|---|
| context / epoch | point on the base manifold |
| generated goal | local section |
| goal kind | local gauge chart |
| commitment | connection / gauge potential |
| bounded action | parallel transport |
| effect receipt | curvature observation |
| repair / replanning | local gauge transformation |
| path-dependent memory | holonomy |
| representation-independent intent | gauge-invariant signature |

No global task graph, edge set, dependency DAG, or winner path is constructed.

## Discrete curvature

The formal interface uses a noncommutative structure group `G` and a discrete gauge potential

```text
A : X -> X -> G
```

with curvature on a triangular transport cycle

```text
F_A(x,y,z) = A(x,y) A(y,z) A(x,z)^-1.
```

Under a gauge transformation `g : X -> G`,

```text
A^g(x,y) = g(x) A(x,y) g(y)^-1
```

and curvature transforms covariantly by conjugation:

```text
F_{A^g}(x,y,z) = g(x) F_A(x,y,z) g(x)^-1.
```

Therefore flatness is gauge invariant. This is formalized in:

```text
formal/KUOS/OpenHorizon/CommitmentGaugeV0_2.lean
```

## Effect as curvature

The runtime derives a bounded curvature norm from:

- observed harm;
- unrealized benefit;
- uncertainty of the receipt;
- loss of recoverability;
- outcome class.

The effect is not merely appended as a new task. It changes the local connection and frame of the same section.

```text
success + complete -> flat_complete
partial            -> scaled_parallel_transport
failure            -> local_repair_gauge
blocked            -> chart_transition
uncertain          -> curvature_reobservation
```

Repeated failure may yield `handover_or_redesign` rather than an unbounded local retry.

## Holonomy and non-Markov memory

Every action-effect cycle appends a holonomy record containing the section, chart, frame after transport, curvature norm, action digest, and effect digest.

The holonomy trace preserves path dependence. Two states with the same current scalar scores are not identified when they arrived through different transport histories.

## Gauge-invariant action selection

Local frame names may change under correction. Selection is based on representation-independent quantities:

- gauge-invariant section signature;
- connection potential;
- curvature pressure;
- waiting age;
- correction urgency;
- plurality relative to the last transported goal.

Changing a local frame does not change the section identity or its gauge-invariant signature.

## Open horizon

Each invocation prepares at most one covariant action. The full horizon is not fixed.

New contiguous Telos generations extend the gauge bundle with additional local sections. Existing outstanding actions remain byte-stable while unrelated sections are added, so an effect receipt remains valid.

When all local sections are flat, handed over, or temporarily absent, the runtime emits:

```text
local_sections_flat_or_empty_horizon_open
```

This is a wakeable open state, not mission termination.

## Outputs

```text
kuuos_open_horizon_commitment_gauge_bundle_v0_2.json
kuuos_open_horizon_commitment_gauge_state_v0_2.json
kuuos_open_horizon_covariant_action_v0_2.json
kuuos_open_horizon_commitment_gauge_receipt_v0_2.json
kuuos_open_horizon_commitment_gauge_ledger_v0_2.jsonl
kuuos_open_horizon_commitment_gauge_audit_v0_2.jsonl
```

## Next layer

The next layer should be `Active Gauge Intervention Loop v0.3`: route the covariant action to a domain adapter, observe the resulting effect, construct an exact curvature receipt, and return it to this runtime.
