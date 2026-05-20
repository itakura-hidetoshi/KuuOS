# Physical Quantum Qi Phase Transition Response Governor v0.2Q

Status: CANDIDATE_RUNTIME_SURFACE

Date: 2026-05-20

Repository: itakura-hidetoshi/KuuOS

Runtime kind: Qi phase-transition response route governor

## Purpose

`Physical Quantum Qi Phase Transition Response Governor v0.2Q` advances the Qi implementation from phase-transition detection to governed response routing.

v0.2P established:

```text
QiTransitionTrajectoryCandidate -> phase-transition candidate receipt
```

v0.2Q adds:

```text
QiTrajectoryPhaseTransitionCandidate -> governed response route receipt
```

This gives Qi a boundary-preserving response layer: it can route a phase-transition alert into monitoring, re-observation, consultation monitoring, or consultation deepening without turning the route into diagnosis, prescription, formula selection, triage, or execution.

## Canonical interpretation

- A response route is a candidate governance surface.
- Physician-to-AI clinical consultation remains open by default.
- HOLD and WATCH visibility remain canonical.
- Phase-transition HOLD/WATCH signals deepen observation and consultation before any boundary handover.
- Handover is not default.
- Handover is not forced by metric or alert alone.
- Response receipts are append-only and non-authoritative.

## Input

The input surface is a `QiTrajectoryPhaseTransitionCandidate` from v0.2P.

Required input fields include:

- `phase_pressure_score`
- `critical_slowing_down_score`
- `hysteresis_score`
- `transition_alert_level`
- `recommended_route`
- `hold_visible`
- `watch_visible`
- `consultation_deepening_allowed`
- `physician_ai_consultation_preserved`
- `handover_forced`
- authority boundary flags

## Response routes

The governor may emit:

- `continue_candidate_monitoring`
- `reobserve_and_record`
- `consultation_monitoring_route`
- `consultation_deepening_route`
- `hold_with_physician_ai_consultation_open`

These are candidate response routes, not clinical commands.

## Route policy

The default route policy is:

```text
phase_transition_not_indicated -> continue_candidate_monitoring
phase_transition_possible      -> reobserve_and_record
phase_transition_watch_visible -> consultation_monitoring_route
phase_transition_hold_visible  -> hold_with_physician_ai_consultation_open
```

A HOLD route keeps consultation open. It does not automatically hand over. A boundary handover candidate may be made visible only as a candidate surface when pressure is extreme, but it remains non-default and non-executing.

## OS surfaces

Allowed candidate surfaces:

- `BeliefOS.qi_response_route_candidate`
- `MemoryOS.qi_response_route_receipt_candidate`
- `ReflectionOS.qi_response_risk_review_candidate`
- `PlanOS.qi_response_monitoring_plan_candidate`
- `DecisionOS.qi_response_safety_evaluable_candidate`
- `ClinicalConsultationOS.physician_ai_consultation_open_route_candidate`

## Forbidden reductions

The governor forbids:

- response route claimed as clinical action
- response route claimed as diagnosis
- response route claimed as prescription
- response route claimed as formula selection
- response route claimed as triage
- response route grants execution authority
- response route grants truth authority
- response route grants proof authority
- phase alert forces handover
- metric forces handover
- consultation closed by governor
- doctor-AI consultation blocked
- HOLD visibility erased
- WATCH visibility erased
- non-Markov history erased
- authority created by response

## Clinical consultation boundary

v0.2Q preserves the v0.2L / v0.2M / v0.2N / v0.2O / v0.2P stance:

- physician-to-AI clinical consultation is accepted
- licensed physician consultation is the default path
- phase-transition alerts deepen consultation first
- handover is boundary mode only
- handover is not default
- alert or metric alone does not force handover
- response routes keep clinical reasoning in consultation form unless a separate boundary process is explicitly opened

## Non-authority boundary

This governor does not grant:

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

- Runtime: `src/physical_quantum_qi_phase_transition_response_governor_v0_2Q.py`
- Packet: `examples/physical_quantum_qi_phase_transition_response_governor_packet_v0_2Q.json`
- Validator: `scripts/validate_physical_quantum_qi_phase_transition_response_governor_v0_2Q.py`
- Regression: `tests/test_physical_quantum_qi_phase_transition_response_governor_v0_2Q.py`

## Closure posture

v0.2Q is append-only, same-root, boundary-preserving, and non-destructive. Future updates must be v0.2R+ or v0.3+ additive-only / tighten-only and must not weaken consultation openness, HOLD/WATCH visibility, non-Markov history visibility, candidate-only response status, or the no-authority boundary.
