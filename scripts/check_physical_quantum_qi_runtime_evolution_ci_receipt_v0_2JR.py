#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "docs" / "PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_CI_POST_MERGE_RECEIPT_v0_2JR.md"

REQUIRED_TOKENS = [
    "Physical Quantum Qi Runtime Evolution CI Post-Merge Receipt v0.2J-R",
    "Status: POST_MERGE_RECEIPT_RECORDED",
    "Date: 2026-05-20",
    "Repository: itakura-hidetoshi/KuuOS",
    "Receipt kind: PR #27 post-merge CI coverage receipt",
    "append-only receipt surface",
    "does not replace the v0.2J-R contracts, packets, source files, tests, validators, governance runners, or future Physical Quantum Qi addenda",
    "Pull request: `#27`",
    "Pull request title: `Add Physical Quantum Qi runtime evolution CI`",
    "Base before merge: `9a119874563be154ee4cb9c8a6372643852ec7a5`",
    "PR head commit: `9aa0eab35e37a1a1ab4ba96337f2c703fd34ed88`",
    "Squash merge commit: `69ad6b54d4c1bde480095fe56c3421aff4d14b2d`",
    "Merged at: `2026-05-20T22:28:37Z`",
    "Changed files: `2`",
    "Additions: `153`",
    "Deletions: `1`",
    "All Governance Validation — success",
    "Core Governance Validation — success",
    "Qi Motion Chain Validation — success",
    "Physical Quantum Qi Runtime Validation — success",
    "Physical Quantum Qi Deepening Validation — success",
    "Physical Quantum Qi Runtime Evolution Validation — success",
    "Emptiness Two Truths Runtime Audit Validation — success",
    "Emptiness Superposition Non-Collapse Validation — success",
    "GPT GitHub Integration Validation — success",
    "Workflow: `Physical Quantum Qi Runtime Evolution Validation`",
    "Workflow run ID: `26193560453`",
    "Job name: `Validate Physical Quantum Qi v0.2J-R runtime evolution`",
    "Job ID: `77067650975`",
    "Checked commit: `9aa0eab35e37a1a1ab4ba96337f2c703fd34ed88`",
    "Result: `success`",
    "The squash merge commit `69ad6b54d4c1bde480095fe56c3421aff4d14b2d` exists on `main`",
    "does not claim independent external audit acceptance",
    "`Makefile`",
    "`.github/workflows/all_governance_validation.yml`",
    "make physical-quantum-qi-runtime-evolution-checks",
    "scripts/validate_qi_bensho_treatment_route_candidate_v0_2J.py",
    "scripts/validate_qi_bensho_decisionos_clinician_handoff_v0_2K.py",
    "scripts/validate_qi_clinical_red_flag_handover_governor_v0_2L.py",
    "scripts/check_qi_clinical_red_flag_consultation_governor_finality_v0_2L.py",
    "scripts/validate_physical_quantum_qi_observation_kernel_v0_2M.py",
    "tests/test_physical_quantum_qi_observation_kernel_v0_2M.py",
    "scripts/validate_physical_quantum_qi_state_transition_kernel_v0_2N.py",
    "tests/test_physical_quantum_qi_state_transition_kernel_v0_2N.py",
    "scripts/validate_physical_quantum_qi_transition_trajectory_ledger_v0_2O.py",
    "tests/test_physical_quantum_qi_transition_trajectory_ledger_v0_2O.py",
    "scripts/validate_physical_quantum_qi_trajectory_phase_transition_detector_v0_2P.py",
    "tests/test_physical_quantum_qi_trajectory_phase_transition_detector_v0_2P.py",
    "scripts/validate_physical_quantum_qi_phase_transition_response_governor_v0_2Q.py",
    "tests/test_physical_quantum_qi_phase_transition_response_governor_v0_2Q.py",
    "scripts/validate_physical_quantum_qi_response_feedback_loop_v0_2R.py",
    "tests/test_physical_quantum_qi_response_feedback_loop_v0_2R.py",
    "runtime evolution checks are validation-only",
    "CI green is integration evidence, not theorem truth",
    "CI green is integration evidence, not clinical authority",
    "v0.2J-R surfaces remain candidate-only where applicable",
    "observation and state-transition kernels remain non-authoritative readout surfaces",
    "transition ledgers remain append-only trace surfaces",
    "phase transition detection remains signal classification, not direct action",
    "response governance remains bounded by consultation and non-sovereignty",
    "response feedback remains non-overwriting and non-escalatory",
    "Physical Quantum Qi runtime evolution does not create diagnosis authority",
    "Physical Quantum Qi runtime evolution does not create prescription authority",
    "Physical Quantum Qi runtime evolution does not create patient-specific action authority",
    "repository-side traceability evidence only",
    "clinical authority",
    "diagnosis authority",
    "prescription authority",
    "formula-selection authority",
    "treatment-recommendation authority",
    "triage authority",
    "patient-specific action authority",
    "execution authority",
    "proof authority by itself",
    "truth authority by itself",
    "A successful PR merge is integration evidence, not clinical truth.",
    "A successful CI run is validation evidence, not final theorem truth.",
    "A workflow covering v0.2J-R preserves the validation boundary; it does not expand the runtime authority boundary.",
    "same-root, append-only, boundary-preserving, and non-destructive",
    "v0.2S+ surfaces or dedicated CI addenda rather than rewriting this receipt",
]

FORBIDDEN_TOKENS = [
    "runtime_authority_granted: true",
    "clinical_authority_granted: true",
    "diagnosis_authority_granted: true",
    "prescription_authority_granted: true",
    "formula_selection_authority_granted: true",
    "treatment_recommendation_authority_granted: true",
    "triage_authority_granted: true",
    "patient_specific_action_authority_granted: true",
    "execution_authority_granted: true",
    "proof_authority_granted: true",
    "truth_authority_granted: true",
    "ontology_authority_granted: true",
    "safety_override_authority_granted: true",
    "memory_overwrite_authority_granted: true",
    "governance_bypass_authority_granted: true",
    "external_auditor_acceptance: true",
    "journal_acceptance: true",
    "community_acceptance: true",
    "CI green proves clinical truth",
    "CI green grants clinical authority",
    "CI green grants execution authority",
    "successful PR merge proves clinical truth",
    "successful PR merge grants clinical authority",
    "successful PR merge grants execution authority",
    "workflow coverage expands runtime authority",
    "phase transition detection grants direct action",
    "response feedback may overwrite memory",
]


def main() -> int:
    errors: list[str] = []
    if not RECEIPT.is_file():
        errors.append(f"missing file: {RECEIPT.relative_to(ROOT)}")
        text = ""
    else:
        text = RECEIPT.read_text(encoding="utf-8")

    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"{RECEIPT.relative_to(ROOT)} missing token: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            errors.append(f"{RECEIPT.relative_to(ROOT)} forbidden authority-expansion token: {token}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: Physical Quantum Qi runtime evolution CI receipt v0.2J-R checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
