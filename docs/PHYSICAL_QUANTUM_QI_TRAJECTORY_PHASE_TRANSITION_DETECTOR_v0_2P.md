# Physical Quantum Qi Trajectory Phase Transition Detector v0.2P

Status: CANDIDATE_RUNTIME_SURFACE

Date: 2026-05-20

Repository: itakura-hidetoshi/KuuOS

Runtime kind: Qi trajectory phase-transition candidate detector

## Purpose

`Physical Quantum Qi Trajectory Phase Transition Detector v0.2P` advances the Qi implementation from append-only trajectory ledger to phase-transition candidate detection.

v0.2O established:

```text
ordered Qi transition records -> trajectory-level candidate receipt
```

v0.2P adds:

```text
QiTransitionTrajectoryCandidate -> phase-transition candidate receipt
```

This gives the Qi runtime a visible way to detect regime-change signs without turning detection into diagnosis, prescription, proof, truth, or execution authority.

## Canonical interpretation

- Phase transition detection is a non-authoritative runtime candidate.
- It detects regime-change signs without claiming ontology, diagnosis, or action.
- It preserves HOLD and WATCH visibility inherited from the trajectory ledger.
- It keeps non-Markov history primary.
- It keeps tail residue, backflow, transport distortion, and recoverability loss visible.
- It deepens observation and consultation rather than forcing handover.
- Physician-to-AI clinical consultation remains accepted as the default clinical boundary.

## Input

The input surface is a `QiTransitionTrajectoryCandidate` from v0.2O.

Required trajectory signals include:

- `record_count`
- `average_risk_score`
- `latest_risk_score`
- `stability_index`
- `risk_trend`
- `backflow_trend`
- `tail_residue_trend`
- `recoverability_trend`
- `transport_distortion_trend`
- `trajectory_decision`
- `candidate_only`
- `authority_granted`
- `clinical_authority_granted`
- `execution_authority_granted`
- `handover_forced`
- `doctor_ai_consultation_blocked`

## Detection signals

The detector computes candidate-only diagnostics:

- `phase_pressure_score`
- `critical_slowing_down_score`
- `hysteresis_score`
- `increasing_pressure_channels`
- `hold_visible`
- `watch_visible`
- `transition_alert_level`
- `recommended_route`

These values are runtime warning surfaces, not clinical or execution decisions.

## Alert levels

The detector may emit:

- `phase_transition_not_indicated`
- `phase_transition_possible`
- `phase_transition_watch_visible`
- `phase_transition_hold_visible`

## Recommended routes

The detector may recommend:

- `continue_candidate_monitoring`
- `reobserve_before_commit`
- `continue_consultation_with_monitoring`
- `deepen_consultation_and_reobserve`

These recommendations remain non-authoritative. They do not force handover.

## OS surfaces

Allowed candidate surfaces:

- `BeliefOS.qi_phase_transition_candidate`
- `MemoryOS.qi_phase_transition_lineage_note_candidate`
- `ReflectionOS.qi_phase_transition_residue_analysis_candidate`
- `PlanOS.qi_phase_transition_monitoring_route_candidate`
- `DecisionOS.qi_phase_transition_safety_evaluable_candidate`
- `ClinicalConsultationOS.qi_phase_transition_consultation_deepening_candidate`

## Forbidden reductions

The detector forbids:

- phase transition claimed as truth
- phase transition claimed as diagnosis
- phase transition claimed as prescription
- phase transition claimed as formula selection
- phase transition claimed as execution permission
- phase transition forces handover by metric alone
- phase transition closes physician-AI consultation
- HOLD visibility erased
- WATCH visibility erased
- non-Markov history reduced to snapshot
- tail residue hidden
- backflow hidden
- transport distortion hidden
- recoverability loss hidden
- authority created by alert

## Clinical consultation boundary

v0.2P preserves the v0.2L / v0.2M / v0.2N / v0.2O stance:

- physician-to-AI clinical consultation is accepted
- licensed physician consultation is the default path
- red flags and phase-transition alerts deepen consultation first
- handover is boundary mode only
- handover is not default
- phase-transition detection alone does not force handover
- metric shifts open WATCH / HOLD / reobserve / consultation-deepening surfaces

## Non-authority boundary

This detector does not grant:

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

- Runtime: `src/physical_quantum_qi_trajectory_phase_transition_detector_v0_2P.py`
- Packet: `examples/physical_quantum_qi_trajectory_phase_transition_detector_packet_v0_2P.json`
- Validator: `scripts/validate_physical_quantum_qi_trajectory_phase_transition_detector_v0_2P.py`
- Regression: `tests/test_physical_quantum_qi_trajectory_phase_transition_detector_v0_2P.py`

## Closure posture

v0.2P is append-only, same-root, boundary-preserving, and non-destructive. Future updates must be v0.2Q+ or v0.3+ additive-only / tighten-only and must not weaken phase-transition visibility, HOLD visibility, WATCH visibility, non-Markov memory visibility, consultation default, candidate-only status, or the no-authority boundary.
