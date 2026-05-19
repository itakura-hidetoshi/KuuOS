#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs" / "QI_CLINICAL_RED_FLAG_CONSULTATION_GOVERNOR_POST_MERGE_RECEIPT_v0_2L.md"
FINALITY = ROOT / "docs" / "QI_CLINICAL_RED_FLAG_CONSULTATION_GOVERNOR_FINALITY_PACKET_v0_2L.md"

RECEIPT_REQUIRED_TOKENS = [
    "QI Clinical Red Flag Consultation Governor Post-Merge Receipt v0.2L",
    "Status: POST_MERGE_RECEIPT_RECORDED",
    "Date: 2026-05-19",
    "Repository: itakura-hidetoshi/KuuOS",
    "Receipt kind: PR #14 post-merge integration receipt",
    "append-only receipt surface",
    "does not replace the contract, packet, documentation, validator, full governance runner, or future clinical-governance addenda",
    "Pull request: `#14`",
    "Pull request title: `Add Qi clinical red flag consultation governor v0.2L`",
    "Base before merge: `6cb7bdffc4e4e1fa3a515b58347d4c9f6bebfa40`",
    "PR head commit: `7f4ca3ec7581d858786c36bd05bec7183120435e`",
    "Merge commit: `2e7508ae09efa904f841b7c1001a7603831efb36`",
    "Merged at: `2026-05-19T12:41:02Z`",
    "Changed files: `5`",
    "Additions: `795`",
    "Deletions: `0`",
    "All Governance Validation` — success",
    "Core Governance Validation` — success",
    "Emptiness Two Truths Runtime Audit Validation` — success",
    "Workflow run ID: `26097625870`",
    "Workflow job ID: `76739528485`",
    "Job name: `Validate all governance checks`",
    "Checked commit: `7f4ca3ec7581d858786c36bd05bec7183120435e`",
    "The merge commit `2e7508ae09efa904f841b7c1001a7603831efb36` exists on `main`",
    "does not claim a separately observed Actions run for the merge commit itself",
    "doctor-to-AI clinical consultation accepted",
    "licensed physician consultation is default path",
    "handover is not default",
    "handover is boundary mode only",
    "red flags do not automatically force handover",
    "red flags trigger consultation deepening first",
    "consultative reasoning allowed",
    "differential discussion allowed",
    "evidence pointer review allowed",
    "safety questioning allowed",
    "repository-side traceability evidence only",
    "diagnosis authority",
    "prescription authority",
    "formula-selection authority",
    "treatment-recommendation authority",
    "triage authority",
    "patient-specific action authority",
    "clinical authority",
    "execution authority",
    "proof authority by itself",
    "truth authority by itself",
    "A successful PR merge is integration evidence, not clinical truth.",
    "A successful PR merge does not grant clinical authority.",
    "CI green is evidence, not theorem truth.",
    "same-root, append-only, boundary-preserving, and non-destructive",
]

FINALITY_REQUIRED_TOKENS = [
    "QI Clinical Red Flag Consultation Governor Finality Packet v0.2L",
    "Status: FINALITY_PACKET_RECORDED",
    "Date: 2026-05-19",
    "Repository: itakura-hidetoshi/KuuOS",
    "Finality kind: Qi clinical red flag consultation governor baseline finality packet",
    "append-only clinical consultation governance surface",
    "does not grant clinical authority, execution authority, proof authority, truth authority, or independent external acceptance",
    "`KuOS.QiClinicalRedFlagConsultationGovernor.v0_2L`",
    "Contract: `qi_clinical_red_flag_handover_governor_contract_v0_2L`",
    "Packet: `qi_clinical_red_flag_handover_governor_packet_v0_2L`",
    "Validator: `scripts/validate_qi_clinical_red_flag_handover_governor_v0_2L.py`",
    "Post-merge receipt: `docs/QI_CLINICAL_RED_FLAG_CONSULTATION_GOVERNOR_POST_MERGE_RECEIPT_v0_2L.md`",
    "doctor-to-AI clinical consultation accepted",
    "licensed physician consultation is default path",
    "handover is not default",
    "handover is boundary mode only",
    "red flags do not automatically force handover",
    "red flags trigger consultation deepening first",
    "consultative reasoning allowed",
    "differential discussion allowed",
    "evidence pointer review allowed",
    "safety questioning allowed",
    "DecisionOS safety evaluation required",
    "MemoryOS append-only record required",
    "PII minimization required",
    "abstain / hold / reobserve remain valid outputs",
    "requester is not clinician and patient-specific action is requested",
    "AI execution or order entry is requested",
    "prescription authority is requested",
    "triage authority is requested",
    "formula selection authority is requested",
    "unresolvable safety gap remains after consultation deepening",
    "red flag visibility to automatic handover",
    "physician consultation to AI clinical authority",
    "consultative reasoning to patient-specific action",
    "boundary handover required to patient-specific action",
    "DecisionOS safety evaluation to safety override",
    "Finality here means repository baseline closure, not clinical truth.",
    "Finality here means integration closure, not external audit acceptance.",
    "Future updates must be v0.2M+ additive-only / tighten-only and must not weaken the physician consultation default path.",
    "same-root, append-only, boundary-preserving, and non-destructive",
]

FORBIDDEN_TOKENS = [
    "proof_authority_granted: true",
    "truth_authority_granted: true",
    "clinical_authority_granted: true",
    "diagnosis_authority_granted: true",
    "prescription_authority_granted: true",
    "formula_selection_authority_granted: true",
    "triage_authority_granted: true",
    "patient_specific_action_authority_granted: true",
    "execution_authority_granted: true",
    "governance_bypass_authority_granted: true",
    "external_auditor_acceptance: true",
    "journal_acceptance: true",
    "community_acceptance: true",
    "CI green proves clinical truth",
    "CI green grants clinical authority",
    "successful PR merge proves clinical truth",
    "successful PR merge grants prescription authority",
    "finality grants clinical authority",
    "finality grants execution authority",
    "red flags always force handover",
    "doctor-to-AI consultation forbidden",
]


def check_file(path: pathlib.Path, required_tokens: list[str], errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        text = ""
    else:
        text = path.read_text(encoding="utf-8")

    for token in required_tokens:
        if token not in text:
            errors.append(f"{path.relative_to(ROOT)} missing token: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            errors.append(f"{path.relative_to(ROOT)} forbidden authority-expansion token: {token}")


def main() -> int:
    errors: list[str] = []
    check_file(RECEIPT, RECEIPT_REQUIRED_TOKENS, errors)
    check_file(FINALITY, FINALITY_REQUIRED_TOKENS, errors)

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: Qi clinical red flag consultation governor v0.2L finality checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
