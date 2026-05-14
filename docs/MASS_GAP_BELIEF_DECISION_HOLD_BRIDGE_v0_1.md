# Mass Gap BeliefOS / DecisionOS HOLD Bridge v0.1

This document connects the Mass Gap to Two Truths Engine runtime bridge to BeliefOS and DecisionOS HOLD surfaces.

It is a conservative HOLD bridge. It does not create belief truth authority, decision release authority, final theorem authority, or action authority.

## Source Runtime Bridge

The source runtime bridge is:

```text
docs/TWO_TRUTHS_ENGINE_MASS_GAP_RUNTIME_CONTRACT_v0_1.md
```

The canonical proof repository remains:

```text
itakura-hidetoshi/4d-mass-gap
```

## Purpose

The purpose is to route the mass-gap two-truths non-collapse barrier into BeliefOS and DecisionOS as a conservative guard.

```text
MassGapTwoTruthsRuntimeInput
  -> TwoTruthsEngineMassGapDecision
  -> BeliefOS evidence guard
  -> DecisionOS admissibility guard
  -> HOLD / REOBSERVE / HANDOVER if boundary is unstable
```

## BeliefOS Mapping

BeliefOS receives the bridge as `MassGapBeliefEvidenceGuard`:

```yaml
MassGapBeliefEvidenceGuard:
  source_decision: TwoTruthsEngineMassGapDecision
  belief_authority: false
  world_fact_authority: false
  evidence_role: non_collapse_guard
  accepted_status: belief_guard_active
  failure_status: belief_hold
```

BeliefOS may use the bridge to prevent collapse between paramartha and samvrti surfaces.

BeliefOS may not use the bridge to directly set belief truth, world fact truth, memory truth, or final theorem status.

## DecisionOS Mapping

DecisionOS receives the bridge as `MassGapDecisionAdmissibilityGuard`:

```yaml
MassGapDecisionAdmissibilityGuard:
  source_decision: TwoTruthsEngineMassGapDecision
  decision_release_authority: false
  action_authority: false
  admissibility_role: non_collapse_barrier
  accepted_status: decision_guard_active
  failure_status: decision_hold
```

DecisionOS may use the bridge to block premature proceed when the two-truths boundary is unstable.

DecisionOS may not use the bridge to directly authorize action, release a decision, update world state, update belief state, update memory state, or open final theorem status.

## HOLD Rule

BeliefOS / DecisionOS must HOLD when any of the following is true:

```text
canonical_repo != itakura-hidetoshi/4d-mass-gap
bridge_authority != reference_only
public_theorem_boundary != held
final_theorem_authority != false
action_authority != false
paramartha_non_reification_guard != active
samvrti_excitation_admissibility == unconditional_action
two_truths_non_collapse_barrier != active
```

## Conservative Output

When the bridge is accepted, the permitted output is:

```yaml
MassGapBeliefDecisionHoldOutput:
  belief_guard: active
  decision_guard: active
  allowed_effects:
    - prevent_two_truths_collapse
    - request_reobserve_if_boundary_unstable
    - hold_if_authority_expands
    - handover_if_public_theorem_boundary_is_requested
  forbidden_effects:
    - set_belief_truth
    - set_world_fact
    - release_decision
    - perform_action
    - open_final_theorem_boundary
```

## Runtime Adapter

Minimal adapter:

```text
examples/mass_gap_belief_decision_hold_adapter_minimal.py
```

## Machine-Readable Contract

Spec:

```text
specs/mass_gap_belief_decision_hold_bridge_v0_1.yaml
```

## Validator

Validator:

```text
scripts/validate_mass_gap_belief_decision_hold_bridge_v0_1.py
```

## Boundary

Fixed boundary:

```text
belief_authority: false
world_fact_authority: false
decision_release_authority: false
action_authority: false
final_theorem_authority: false
public_theorem_boundary: held
```

## Development Rule

```text
append-only / tighten-only / overwrite-forbidden
```
