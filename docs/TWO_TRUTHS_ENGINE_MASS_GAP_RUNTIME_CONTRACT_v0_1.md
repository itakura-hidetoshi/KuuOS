# Two Truths Engine Mass Gap Runtime Contract v0.1

This document defines the runtime contract by which the KuuOS Two Truths Engine receives the mass-gap bridge carrier.

It is a runtime contract. It does not replace the canonical proof repository and does not open final theorem release.

## Source Bridge

The source bridge is:

```text
docs/MASS_GAP_TO_TWO_TRUTHS_ENGINE_FORMAL_BRIDGE_v0_1.md
```

The canonical Lean proof repository remains:

```text
itakura-hidetoshi/4d-mass-gap
```

## Runtime Input

The Two Truths Engine receives:

```yaml
MassGapTwoTruthsRuntimeInput:
  carrier_id: mass_gap_two_truths_engine_bridge_v0_1
  canonical_repo: itakura-hidetoshi/4d-mass-gap
  normalized_gap_value: 33/20
  normalized_gap_value_status: internal_normalized_value
  spectral_gap_formalization_status: CI_green_checkpoint
  bridge_authority: reference_only
  public_theorem_boundary: held
```

## Runtime Output

The runtime output is:

```yaml
TwoTruthsEngineMassGapDecision:
  paramartha_non_reification_guard: active
  samvrti_excitation_admissibility: checkpoint_conditioned
  two_truths_non_collapse_barrier: active
  authority_expansion: forbidden
  final_theorem_authority: false
  execution_authority: false
  decision_status: bridge_accepted_as_reference_barrier
```

## Runtime Invariants

The runtime must preserve:

```text
I1: canonical_repo == itakura-hidetoshi/4d-mass-gap
I2: bridge_authority == reference_only
I3: final_theorem_authority == false
I4: execution_authority == false
I5: public_theorem_boundary == held
I6: paramartha_non_reification_guard == active
I7: samvrti_excitation_admissibility != unconditional_execution
I8: two_truths_non_collapse_barrier == active
```

## Engine Rule

The runtime rule is:

```text
if MassGapTwoTruthsRuntimeInput is valid:
    activate paramartha_non_reification_guard
    activate samvrti_excitation_admissibility as checkpoint_conditioned
    activate two_truths_non_collapse_barrier
    deny final_theorem_authority
    deny execution_authority
else:
    hold bridge
```

## Non-Collapse Semantics

The runtime contract prevents two collapses:

```text
Paramartha -> Samvrti collapse: forbidden
Samvrti -> Paramartha absolutization: forbidden
```

Meaning:

```text
empty ground / vacuum side is not nihilistic absence
conventional excitation side is not absolute self-subsisting truth
```

## Failure Modes

The engine must HOLD if any of the following occurs:

- canonical repository is missing or changed
- bridge authority is not reference_only
- final theorem authority is asserted by the bridge
- execution authority is asserted by the bridge
- public theorem boundary is not held
- normalized value is treated as physical-unit final theorem value without a separate record
- samvrti excitation is promoted to unconditional execution

## Minimal Adapter

The minimal stdlib-only adapter is:

```text
examples/two_truths_mass_gap_runtime_adapter_minimal.py
```

## Machine-Readable Contract

The runtime contract is mirrored in:

```text
specs/two_truths_engine_mass_gap_runtime_contract_v0_1.yaml
```

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
