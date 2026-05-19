# QI Clinical Red Flag Consultation Governor Finality Packet v0.2L

Status: FINALITY_PACKET_RECORDED

Date: 2026-05-19

Repository: itakura-hidetoshi/KuuOS

Finality kind: Qi clinical red flag consultation governor baseline finality packet

This packet finalizes the v0.2L baseline as an append-only clinical consultation governance surface. It closes the immediate post-merge receipt loop for PR #14 without claiming clinical authority, execution authority, proof authority, truth authority, or independent external acceptance.

## Finalized baseline

- `KuOS.QiClinicalRedFlagConsultationGovernor.v0_2L`
- Contract: `qi_clinical_red_flag_handover_governor_contract_v0_2L`
- Packet: `qi_clinical_red_flag_handover_governor_packet_v0_2L`
- Validator: `scripts/validate_qi_clinical_red_flag_handover_governor_v0_2L.py`
- Post-merge receipt: `docs/QI_CLINICAL_RED_FLAG_CONSULTATION_GOVERNOR_POST_MERGE_RECEIPT_v0_2L.md`

## Finalized core invariants

- doctor-to-AI clinical consultation accepted
- licensed physician consultation is default path
- handover is not default
- handover is boundary mode only
- red flags do not automatically force handover
- red flags trigger consultation deepening first
- `boundary_handover_required` is boundary mode only
- handover is reserved for authority-boundary violations or unresolvable safety gaps
- consultative reasoning allowed
- differential discussion allowed
- evidence pointer review allowed
- safety questioning allowed
- local protocol review may be recommended
- DecisionOS safety evaluation required
- MemoryOS append-only record required
- PII minimization required
- abstain / hold / reobserve remain valid outputs

## Boundary triggers retained

Boundary handover is allowed only when one of these boundary triggers appears:

- requester is not clinician and patient-specific action is requested
- AI execution or order entry is requested
- prescription authority is requested
- triage authority is requested
- formula selection authority is requested
- minimum context for safe consultation is missing
- unresolvable safety gap remains after consultation deepening
- institutional or legal boundary requires human-only review

## Forbidden collapses retained

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

## Non-authority boundary

This finality packet does not grant:

- diagnosis authority
- prescription authority
- formula-selection authority
- treatment-recommendation authority
- triage authority
- patient-specific action authority
- clinical authority
- execution authority
- proof authority by itself
- truth authority by itself
- ontology authority
- safety-override authority
- memory-overwrite authority
- governance-bypass authority
- external-auditor acceptance
- journal acceptance
- community acceptance

## Finality rule

Finality here means repository baseline closure, not clinical truth.
Finality here means integration closure, not external audit acceptance.
Finality here means append-only reference boundary, not future immutability of the wider Qi clinical governance program.
Future updates must be v0.2M+ additive-only / tighten-only and must not weaken the physician consultation default path.

## Closure posture

The v0.2L finality packet is same-root, append-only, boundary-preserving, and non-destructive.
