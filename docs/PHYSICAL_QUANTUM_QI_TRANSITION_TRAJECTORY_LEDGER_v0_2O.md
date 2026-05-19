# Physical Quantum Qi Transition Trajectory Ledger v0.2O

Status: CANDIDATE_RUNTIME_SURFACE

Date: 2026-05-20

Repository: itakura-hidetoshi/KuuOS

Runtime kind: append-only Qi transition trajectory ledger

## Purpose

`Physical Quantum Qi Transition Trajectory Ledger v0.2O` advances the Qi implementation from a single bounded state transition to an append-only trajectory ledger.

v0.2N established:

```text
QiStateCandidate + bounded transition events -> next QiStateCandidate
```

v0.2O adds:

```text
ordered Qi transition records -> trajectory-level candidate receipt
```

This makes Qi runtime evolution auditable as a sequence, not merely a pointwise state update.

## Canonical interpretation

- Qi trajectory is a non-authoritative runtime candidate surface.
- Multiple transition records do not accumulate authority.
- HOLD, WATCH, and CONTINUE remain visible canonical outcomes.
- Worsening is not silently promoted.
- Improvement is not execution permission.
- Source lineage remains first-class.
- Source history must not be erased.
- Non-Markov memory remains primary.
- Backaction remains visible.
- Physician-to-AI clinical consultation remains accepted as the default clinical boundary.

## Required transition record

Each trajectory record must include:

- `sequence_index`
- `transition_id`
- `source_trace`
- `transition_decision`
- `risk_score`
- `lineage_preserved`
- `source_history_replaced`
- `candidate_only`
- `authority_granted`
- `clinical_authority_granted`
- `execution_authority_granted`
- `next_state_candidate`

The `next_state_candidate` must remain a `QiStateCandidate` with bounded Qi metrics.

## Canonical decisions

The ledger accepts only:

- `candidate_continue`
- `candidate_watch`
- `candidate_hold`

At ledger level these project to:

- `trajectory_continue_candidate`
- `trajectory_watch_visible`
- `trajectory_hold_visible`

The ledger deliberately requires WATCH and HOLD examples to remain visible in the fixture so that these are not treated as exceptional or erased outcomes.

## Trajectory diagnostics

The candidate trajectory reports:

- `record_count`
- `continue_count`
- `watch_count`
- `hold_count`
- `average_risk_score`
- `latest_risk_score`
- `stability_index`
- `risk_trend`
- `backflow_trend`
- `tail_residue_trend`
- `recoverability_trend`
- `transport_distortion_trend`
- `latest_qi_runtime_mode`
- `trajectory_decision`

These diagnostics are control candidates, not truth, clinical action, or execution authority.

## OS surfaces

Allowed candidate surfaces:

- `BeliefOS.qi_transition_trajectory_candidate`
- `MemoryOS.qi_trajectory_lineage_ledger_candidate`
- `ReflectionOS.qi_trajectory_residue_analysis_candidate`
- `PlanOS.qi_trajectory_transport_candidate`
- `DecisionOS.qi_trajectory_safety_evaluable_candidate`
- `QiProcessTensor.trajectory_update_surface`

## Forbidden reductions

The runtime forbids:

- trajectory claimed as truth
- trajectory claimed as clinical action
- trajectory grants execution authority
- trajectory grants diagnosis authority
- trajectory grants prescription authority
- trajectory grants formula-selection authority
- trajectory forces handover by metric alone
- authority accumulates across records
- lineage replaced
- source history erased
- current snapshot replaces process history
- backaction erased
- tail residue hidden
- worsening state silently promoted
- hold result silently closed
- watch result silently closed

## Clinical consultation boundary

v0.2O preserves the v0.2L / v0.2M / v0.2N stance:

- physician-to-AI clinical consultation is accepted
- licensed physician consultation is the default path
- red flags deepen consultation first
- handover is boundary mode only
- handover is not default
- metric changes alone do not force handover
- trajectory worsening opens WATCH / HOLD / consultation-deepening surfaces, not automatic handover

## Non-authority boundary

This ledger does not grant:

- diagnosis authority
- prescription authority
- formula-selection authority
- triage authority
- clinical authority
- execution authority
- proof authority
- truth authority
- ontology authority
- commit authority
- memory-overwrite authority
- world-root rewrite authority
- safety-override authority

## Implementation artifacts

- Runtime: `src/physical_quantum_qi_transition_trajectory_ledger_v0_2O.py`
- Packet: `examples/physical_quantum_qi_transition_trajectory_ledger_packet_v0_2O.json`
- Validator: `scripts/validate_physical_quantum_qi_transition_trajectory_ledger_v0_2O.py`
- Regression: `tests/test_physical_quantum_qi_transition_trajectory_ledger_v0_2O.py`

## Closure posture

v0.2O is append-only, same-root, boundary-preserving, and non-destructive. Future updates must be v0.2P+ or v0.3+ additive-only / tighten-only and must not weaken trajectory visibility, HOLD visibility, WATCH visibility, lineage preservation, non-Markov memory visibility, candidate-only status, or the physician consultation default path.
