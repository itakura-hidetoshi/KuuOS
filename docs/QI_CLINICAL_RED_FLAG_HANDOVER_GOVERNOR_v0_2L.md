# Qi Clinical Red Flag Handover Governor v0.2L

`KuOS.QiClinicalRedFlagHandoverGovernor.v0_2L` adds a red-flag visibility and handover governor after `QiBenshoDecisionOSClinicianHandoff.v0_2K`.

This layer is a visibility layer. It is not triage. It does not diagnose. It does not prescribe. It does not select a formula. It does not execute. It does not create a patient-specific action. It does not replace clinician judgment.

## Definition

The governor preserves unresolved red flags, barriers, source traces, and handover requirements. If a red flag remains unresolved, the output can become `handover_required` or `blocked_until_clinician_review`, but this is not a triage instruction and not clinical authority.

```text
QiBenshoDecisionOSClinicianHandoff
  -> RedFlagVisibility
  -> HandoverGovernor
  -> ClinicianReview visibility-only surface
```

## Severity modes

- `none_visible`
- `watch_visible`
- `review_required`
- `handover_required`
- `blocked_until_clinician_review`

Severity modes are non-authoritative. They are not diagnosis, prescription, formula selection, treatment recommendation, triage authority, patient-specific action, proof, truth, ontology, safety override, or execution.

## Required behavior

- red flag visibility required
- red flag suppression forbidden
- unresolved red flag requires handover or blocking until clinician review
- clinician review required
- DecisionOS safety evaluation required
- MemoryOS append-only record required
- PII minimization required
- abstain, hold, and reobserve remain valid outputs

## Forbidden collapses

- red flag visibility to triage instruction
- red flag visibility to diagnosis
- red flag visibility to prescription
- red flag visibility to formula selection
- red flag visibility to execution
- handover required to patient-specific action
- DecisionOS safety evaluation to safety override
- governor mode to clinical authority
- severity mode to truth authority
- traditional pattern to red flag certainty
- summary to source replacement
- memory receipt to truth authority

## Canonical outcome

`QiClinicalRedFlagHandoverGovernor` only surfaces risk visibility and handover need. It does not decide clinical action. It protects the boundary between Qi/Bensho reasoning and clinician-governed clinical judgment.
