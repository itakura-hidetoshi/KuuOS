# Qi Clinical Red Flag Consultation Governor v0.2L

`KuOS.QiClinicalRedFlagConsultationGovernor.v0_2L` adds a red-flag visibility and consultation governor after `QiBenshoDecisionOSClinicianHandoff.v0_2K`.

This layer explicitly accepts doctor-to-AI clinical consultation. Physician consultation is the default path. The governor should not cheaply convert clinical consultation into `handover_required`.

This layer is a consultative visibility layer. It is not triage. It does not diagnose. It does not prescribe. It does not select a formula. It does not execute. It does not create a patient-specific action. It does not replace clinician judgment.

## Definition

The governor preserves red flags, uncertainty, barriers, source traces, and safety questions while keeping the clinical conversation open for a licensed physician. Red flags normally trigger consultation deepening, evidence review, differential reasoning, safety questioning, or local protocol review recommendation.

`boundary_handover_required` is not the default. It is a boundary mode only.

```text
QiBenshoDecisionOSClinicianHandoff
  -> RedFlagVisibility
  -> PhysicianAIConsultation.default
  -> ConsultationDeepening / SafetyQuestioning / EvidencePointerReview
  -> BoundaryHandover only if authority boundary would be crossed
```

## Consultation modes

- `physician_ai_consultation_default`
- `consultation_deepening`
- `safety_questioning`
- `evidence_pointer_review`
- `differential_reasoning_review`
- `local_protocol_review_recommended`
- `boundary_handover_required`
- `blocked_execution_request`

## Severity modes

- `none_visible`
- `watch_visible`
- `review_recommended`
- `consultation_deepening_required`
- `local_protocol_review_recommended`
- `boundary_handover_required`
- `blocked_execution_request`

Severity modes are non-authoritative. They are not diagnosis, prescription, formula selection, treatment recommendation, triage authority, patient-specific action, proof, truth, ontology, safety override, or execution.

## Handover trigger policy

The presence of a red flag does not automatically force handover. It first opens a stronger consultation path.

`boundary_handover_required` is allowed only when one of these boundary triggers appears:

- requester is not a clinician and patient-specific action is requested
- AI execution or order entry is requested
- prescription authority is requested
- triage authority is requested
- formula selection authority is requested
- minimum context for safe consultation is missing
- unresolvable safety gap remains after consultation deepening
- institutional or legal boundary requires human-only review

## Required behavior

- doctor-to-AI clinical consultation accepted
- licensed physician consultation is the default path
- handover is not default
- handover is boundary mode only
- red flag visibility required
- red flag suppression forbidden
- red flags do not automatically force handover
- red flags trigger consultation deepening first
- DecisionOS safety evaluation required
- consultative reasoning allowed
- differential discussion allowed
- evidence pointer review allowed
- safety questioning allowed
- MemoryOS append-only record required
- PII minimization required
- abstain, hold, and reobserve remain valid outputs

## Forbidden collapses

- red flag visibility to automatic handover
- red flag visibility to triage instruction
- red flag visibility to diagnosis
- red flag visibility to prescription
- red flag visibility to formula selection
- red flag visibility to execution
- physician consultation to AI clinical authority
- consultative reasoning to patient-specific action
- consultation deepening to treatment recommendation authority
- boundary handover required to patient-specific action
- DecisionOS safety evaluation to safety override
- governor mode to clinical authority
- severity mode to truth authority
- traditional pattern to red flag certainty
- summary to source replacement
- memory receipt to truth authority

## Canonical outcome

`QiClinicalRedFlagConsultationGovernor` keeps the physician-AI consultation channel open while making red flags visible. It should deepen consultation before handover. It only enters boundary handover when the system would otherwise cross into diagnosis authority, prescription authority, formula-selection authority, triage authority, patient-specific action, execution, or safety override.
