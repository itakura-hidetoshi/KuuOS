# Physical Quantum Qi State Transition Kernel v0.2N

Status: CANDIDATE_RUNTIME_SURFACE

Date: 2026-05-20

Repository: itakura-hidetoshi/KuuOS

Runtime kind: bounded QiStateCandidate transition kernel

## Purpose

`Physical Quantum Qi State Transition Kernel v0.2N` advances the Qi implementation from candidate projection to candidate transition.

The v0.2M kernel produced:

```text
observation event sequence -> non-authoritative QiStateCandidate
```

v0.2N adds:

```text
QiStateCandidate + bounded transition events -> next QiStateCandidate
```

This is the first minimal state-evolution layer for Qi as a runtime object.

## Canonical interpretation

- Qi state is a non-authoritative runtime candidate.
- State transition is bounded.
- State transition is lineage-preserving.
- State transition is non-Markov-history aware.
- Source history must not be replaced by the next candidate.
- Backaction must remain visible.
- Improvement, worsening, watch, and hold are all valid candidate outcomes.
- Hold is not failure.
- Transition does not grant authority.

## Required input

The kernel requires a previous `QiStateCandidate` containing:

- `qi_memory_gain`
- `qi_backflow`
- `qi_env_correlation_credit`
- `qi_temporal_complexity`
- `qi_coherence_margin`
- `qi_recoverability_margin`
- `qi_transport_distortion`
- `qi_tail_residue`
- `qi_runtime_mode`
- candidate-only and authority-false fields

## Transition event requirements

Each transition event must include:

- `transition_id`
- `transition_kind`
- `memory_gain_delta`
- `backflow_delta`
- `env_correlation_delta`
- `temporal_complexity_delta`
- `coherence_delta`
- `recoverability_delta`
- `transport_distortion_delta`
- `tail_residue_delta`
- `backaction_visible`
- `source_trace`

Each delta must be bounded in `[-0.25, 0.25]`.

## Transition outcomes

The transition receipt emits one of:

- `candidate_continue`
- `candidate_watch`
- `candidate_hold`

These are runtime candidate decisions. They do not imply diagnosis, prescription, formula selection, triage, treatment, proof, truth, or execution.

## Runtime modes

The next state candidate may be:

- `monitor_continue`
- `counterflow_watch`
- `stagnation_watch`
- `deficiency_watch`
- `transport_distortion_watch`

These modes are diagnostic control candidates only.

## OS surfaces

Allowed candidate surfaces:

- `BeliefOS.qi_state_transition_candidate`
- `MemoryOS.qi_transition_lineage_record_candidate`
- `ReflectionOS.qi_transition_residue_analysis_candidate`
- `PlanOS.qi_transition_transport_candidate`
- `DecisionOS.qi_transition_safety_evaluable_candidate`
- `QiProcessTensor.transition_update_surface`

## Forbidden reductions

The runtime forbids:

- transition claimed as truth
- transition claimed as clinical action
- transition grants execution authority
- transition grants diagnosis authority
- transition grants prescription authority
- transition grants formula-selection authority
- transition forces handover by metric alone
- lineage replaced
- source history erased
- current snapshot replaces process history
- backaction erased
- tail residue hidden
- worsening state silently promoted
- hold result silently closed

## Clinical consultation boundary

v0.2N preserves the v0.2L/v0.2M stance:

- physician-to-AI clinical consultation is accepted
- licensed physician consultation is the default path
- red flags deepen consultation first
- handover is boundary mode only
- handover is not default
- metric changes alone do not force handover

## Non-authority boundary

This kernel does not grant:

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

- Runtime: `src/physical_quantum_qi_state_transition_kernel_v0_2N.py`
- Packet: `examples/physical_quantum_qi_state_transition_kernel_packet_v0_2N.json`
- Validator: `scripts/validate_physical_quantum_qi_state_transition_kernel_v0_2N.py`
- Regression: `tests/test_physical_quantum_qi_state_transition_kernel_v0_2N.py`

## Closure posture

v0.2N is append-only, same-root, boundary-preserving, and non-destructive. Future updates must be v0.2O+ or v0.3+ additive-only / tighten-only and must not weaken lineage preservation, source-history preservation, non-Markov memory visibility, backaction visibility, candidate-only status, or the physician consultation default path.
