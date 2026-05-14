# Mass Gap to Two Truths Engine Formal Bridge v0.1

This document defines the formal KuuOS bridge from the canonical 4D mass gap proof repository to the KuuOS Two Truths Engine.

It is a bridge contract. It does not replace the canonical proof repository and does not open final theorem release.

## Canonical Source

The canonical Lean proof repository is:

```text
itakura-hidetoshi/4d-mass-gap
https://github.com/itakura-hidetoshi/4d-mass-gap
```

Canonical Lean surfaces:

```text
MGAP4D.lean
MGAP4D/Phase3ReleaseGate.lean
MGAP4D/Spectral.lean
MGAP4D/Spectral/GapFormalization.lean
MGAP4D/SpectralGapFormalizationGate.lean
```

KuuOS receives these as referenced proof surfaces, not as locally owned theorem authority.

## Purpose

The purpose of this bridge is to connect the mass gap checkpoint to the Two Truths Engine as a non-collapse operator.

```text
canonical mass gap checkpoint
  -> gap-stability carrier
  -> two-truths non-collapse barrier
  -> samvrti excitation admissibility
  -> paramartha non-reification guard
```

The bridge does not assert that the final public theorem boundary is opened.

## Formal Inputs

The bridge consumes a `CanonicalMassGapCheckpoint` record:

```yaml
CanonicalMassGapCheckpoint:
  canonical_repo: itakura-hidetoshi/4d-mass-gap
  active_root: MGAP4D.lean
  phase3_gate: MGAP4D/Phase3ReleaseGate.lean
  spectral_entrypoint: MGAP4D/Spectral.lean
  spectral_checkpoint: MGAP4D/Spectral/GapFormalization.lean
  spectral_gate: MGAP4D/SpectralGapFormalizationGate.lean
  normalized_gap_value: 33/20
  normalized_gap_value_status: internal_normalized_value
  spectral_gap_formalization_status: CI_green_checkpoint
  final_release_status: not_opened
  public_theorem_boundary: held
```

## Formal Outputs

The bridge produces a `TwoTruthsMassGapBridgeCarrier`:

```yaml
TwoTruthsMassGapBridgeCarrier:
  source_checkpoint: CanonicalMassGapCheckpoint
  bridge_authority: reference_only
  gap_stability_carrier: present
  paramartha_non_reification_guard: active
  samvrti_excitation_admissibility: checkpoint_conditioned
  two_truths_non_collapse_barrier: active
  final_theorem_authority: false
  execution_authority: false
```

## Two Truths Engine Mapping

Let:

```text
P = paramartha side / ultimate-truth side / non-reification side
S = samvrti side / conventional-truth side / effective-world side
Delta = normalized gap carrier received from canonical mass gap checkpoint
```

The bridge imposes the following KuuOS rules:

```text
Delta > 0  =>  P is not collapsed into nihilistic nothingness
Delta > 0  =>  S excitations are gap-stabilized effective appearances
Delta > 0  =>  P != S as operational authority surfaces
Delta > 0  =>  S is not self-subsisting absolute reality
Delta > 0  =>  movement from P to S requires a recordable excitation surface
```

In KuuOS terms:

```text
Emptiness
  -> non-self-subsistence
  -> gap-stabilized conventional excitation
  -> recordable samvrti surface
  -> governed action / interpretation boundary
```

## Guard Semantics

### 1. Paramartha Non-Reification Guard

The bridge prevents the ground/vacuum side from being treated as a self-subsisting object.

```text
paramartha_non_reification_guard = active
```

Meaning:

```text
vacuum / ground phase != independently existing entity
emptiness != nihilistic absence
```

### 2. Samvrti Excitation Admissibility Guard

The bridge allows conventional-world excitations only as conditionally arisen, gap-stabilized, recordable surfaces.

```text
samvrti_excitation_admissibility = checkpoint_conditioned
```

Meaning:

```text
observable excitation != absolute entity
observable excitation = conditioned effective-world appearance
```

### 3. Two Truths Non-Collapse Barrier

The bridge prevents collapse in both directions:

```text
P -> S collapse: forbidden
S -> P collapse: forbidden
```

Meaning:

```text
ultimate side cannot be reduced to conventional operational outputs
conventional side cannot be absolutized as ultimate truth
```

### 4. Authority Separation Guard

The bridge carries reference authority only.

```text
bridge_authority = reference_only
final_theorem_authority = false
execution_authority = false
```

## Boundary Conditions

The following are fixed:

```text
canonical Lean proof source: itakura-hidetoshi/4d-mass-gap
KuuOS bridge role: interpretation / governance / reference
spectral gap formalization: CI green checkpoint in canonical repo
normalized value 33/20: internal normalized value
R1--R7 theorem completions: not claimed here
final release: not opened
public theorem boundary: held
```

## Non-Promotion Rule

The bridge must not promote any of the following into final theorem authority:

- KuuOS interpretation alone
- KuuOS governance document alone
- internal normalized value alone
- artifact path alone
- CI checkpoint alone
- philosophical usefulness alone

## YAML Contract

The machine-readable contract is:

```text
specs/mass_gap_two_truths_engine_bridge_v0_1.yaml
```

## Validator

The standalone structural validator is:

```text
scripts/validate_mass_gap_two_truths_engine_bridge_v0_1.py
```

It checks that the bridge document, canonical repository reference, and YAML contract contain the required non-collapse and authority-separation surfaces.

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
