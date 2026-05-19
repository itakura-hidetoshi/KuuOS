# QI Clinical Red Flag Consultation Governor Post-Merge Receipt v0.2L

Status: POST_MERGE_RECEIPT_RECORDED

Date: 2026-05-19

Repository: itakura-hidetoshi/KuuOS

Receipt kind: PR #14 post-merge integration receipt

This receipt records the repository integration of `KuOS.QiClinicalRedFlagConsultationGovernor.v0_2L` after PR #14 was merged. It is an append-only receipt surface. It does not replace the contract, packet, documentation, validator, full governance runner, or future clinical-governance addenda.

## Merge record

- Pull request: `#14`
- Pull request title: `Add Qi clinical red flag consultation governor v0.2L`
- Base before merge: `6cb7bdffc4e4e1fa3a515b58347d4c9f6bebfa40`
- PR head commit: `7f4ca3ec7581d858786c36bd05bec7183120435e`
- Merge commit: `2e7508ae09efa904f841b7c1001a7603831efb36`
- Merged at: `2026-05-19T12:41:02Z`
- Changed files: `5`
- Additions: `795`
- Deletions: `0`

## Observed validation evidence

The final PR head was validated before merge.

- All Governance Validation` — success
- Core Governance Validation` — success
- Emptiness Two Truths Runtime Audit Validation` — success
- Workflow run ID: `26097625870`
- Workflow job ID: `76739528485`
- Job name: `Validate all governance checks`
- Checked commit: `7f4ca3ec7581d858786c36bd05bec7183120435e`
- Branch: `qi-v0-2l-red-flag-handover`

The merge commit `2e7508ae09efa904f841b7c1001a7603831efb36` exists on `main`. This receipt does not claim a separately observed Actions run for the merge commit itself.

## Integrated surfaces

- `docs/QI_CLINICAL_RED_FLAG_HANDOVER_GOVERNOR_v0_2L.md`
- `specs/qi_clinical_red_flag_handover_governor_contract_v0_2L.json`
- `examples/qi_clinical_red_flag_handover_governor_packet_v0_2L.json`
- `scripts/validate_qi_clinical_red_flag_handover_governor_v0_2L.py`
- `scripts/run_all_governance_full_checks_v0_1.py`

## Clinical consultation boundary preserved

The merged v0.2L baseline records these clinical-governance invariants:

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

## Non-authority boundary

This receipt is repository-side traceability evidence only. It does not grant:

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

## Interpretive rule

A successful PR merge is integration evidence, not clinical truth.
A successful PR merge does not grant clinical authority.
A successful PR merge does not grant prescription authority.
A successful PR merge does not grant execution authority.
CI green is evidence, not theorem truth.
Post-merge receipt records repository integration, not independent external audit acceptance.

## Closure posture

The v0.2L receipt is same-root, append-only, boundary-preserving, and non-destructive. Future updates must be additive-only / tighten-only and should use v0.2M+ surfaces rather than rewriting this receipt.
