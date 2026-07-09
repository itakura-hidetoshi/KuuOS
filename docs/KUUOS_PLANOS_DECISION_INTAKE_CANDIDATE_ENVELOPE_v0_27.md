# PlanOS Decision Intake Candidate Envelope v0.27

This layer converts the v0.26 weighted DecisionOS evidence handoff into a DecisionOS intake candidate envelope.

The envelope is still PlanOS-owned and non-authoritative.

It does not decide, select, activate, invoke ActOS, execute, commit externally, overwrite memory, grant truth authority, or release blockers.

## Source

- `kuuos_planos_weighted_decision_evidence_handoff_v0_26`
- required status: `PLANOS_WEIGHTED_DECISION_EVIDENCE_HANDOFF_READY`
- required boundary: DecisionOS evidence only
- required boundary: selection remains owned by DecisionOS

## Runtime

- `runtime/kuuos_planos_decision_intake_candidate_envelope_v0_27.py`

The runtime emits:

- DecisionOS review candidate ids
- probe candidate ids
- barrier candidate ids
- blocked candidate ids
- envelope items
- source handoff digest
- receipt digest

## Boundary

The following are closed:

- decision made = false
- selected candidate committed = false
- activation authorization granted = false
- ActOS invoked = false
- execution granted = false
- truth authority granted = false
- memory overwrite granted = false
- blocker release granted = false
- external commit granted = false

## Formal surface

- `formal/KUOS/PlanOS/DecisionIntakeCandidateEnvelopeV0_27.lean`

The theorem surface records:

- source handoff version preservation
- source evidence-only preservation
- DecisionOS ownership preservation
- review-candidate-only envelope boundary
- no decision, activation, execution, truth, memory overwrite, blocker release, or external commit
- exactly one envelope history record
- exact source digest binding
