# Mass Gap Two Truths Engine Bridge Index v0.1

This index collects the KuuOS-side bridge surfaces that connect the canonical 4D mass gap proof repository to the KuuOS Two Truths Engine.

## Canonical Proof Source

```text
itakura-hidetoshi/4d-mass-gap
https://github.com/itakura-hidetoshi/4d-mass-gap
```

KuuOS references this repository. KuuOS does not replace it as the canonical Lean proof source.

## Bridge Layer

Formal bridge document:

```text
docs/MASS_GAP_TO_TWO_TRUTHS_ENGINE_FORMAL_BRIDGE_v0_1.md
```

Machine-readable bridge spec:

```text
specs/mass_gap_two_truths_engine_bridge_v0_1.yaml
```

The bridge maps:

```text
canonical mass gap checkpoint
  -> gap-stability carrier
  -> two-truths non-collapse barrier
  -> samvrti excitation admissibility
  -> paramartha non-reification guard
```

## Runtime Layer

Runtime contract document:

```text
docs/TWO_TRUTHS_ENGINE_MASS_GAP_RUNTIME_CONTRACT_v0_1.md
```

Machine-readable runtime spec:

```text
specs/two_truths_engine_mass_gap_runtime_contract_v0_1.yaml
```

Minimal stdlib-only adapter:

```text
examples/two_truths_mass_gap_runtime_adapter_minimal.py
```

The runtime accepts the bridge only as:

```text
bridge_accepted_as_reference_barrier
```

It does not grant final theorem authority or execution authority.

## BeliefOS / DecisionOS HOLD Layer

HOLD bridge document:

```text
docs/MASS_GAP_BELIEF_DECISION_HOLD_BRIDGE_v0_1.md
```

Machine-readable HOLD spec:

```text
specs/mass_gap_belief_decision_hold_bridge_v0_1.yaml
```

Minimal stdlib-only HOLD adapter:

```text
examples/mass_gap_belief_decision_hold_adapter_minimal.py
```

This layer receives the Two Truths Engine mass gap decision as a conservative guard only:

```text
TwoTruthsEngineMassGapDecision
  -> MassGapBeliefEvidenceGuard
  -> MassGapDecisionAdmissibilityGuard
  -> HOLD / REOBSERVE / HANDOVER if boundary is unstable
```

It does not set belief truth, world fact truth, decision release status, final theorem authority, or action authority.

## Validator Layer

Bridge and runtime validator:

```text
scripts/validate_mass_gap_two_truths_engine_bridge_v0_1.py
```

Top-level governance runner includes this validator:

```text
scripts/run_all_governance_full_checks_v0_1.py
```

A dedicated BeliefOS / DecisionOS HOLD validator is planned, but was not added in this update.

## Authority Boundary

Fixed boundary:

```text
canonical Lean proof source: itakura-hidetoshi/4d-mass-gap
KuuOS bridge role: interpretation / governance / reference
bridge authority: reference_only
belief authority: false
world fact authority: false
decision release authority: false
action authority: false
final theorem authority: false
execution authority: false
final release: not opened
public theorem boundary: held
```

## Two Truths Engine Meaning

The mass gap bridge is used by KuuOS as a non-collapse operator:

```text
Delta > 0
  -> paramartha_non_reification_guard
  -> samvrti_excitation_admissibility
  -> two_truths_non_collapse_barrier
  -> BeliefOS / DecisionOS conservative HOLD guard
```

It prevents:

```text
paramartha collapse into nihilistic nothingness
samvrti absolutization into self-subsisting final truth
belief or decision authority expansion from reference-only mass-gap input
```

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
