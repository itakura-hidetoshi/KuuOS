#!/usr/bin/env python3
from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKET = ROOT / "docs" / "PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_FINALITY_PACKET_v0_2JR.md"

REQUIRED_TOKENS = [
    "Physical Quantum Qi Runtime Evolution Finality Packet v0.2J-R",
    "Status: FINALITY_PACKET_RECORDED",
    "Date: 2026-05-21",
    "Repository: itakura-hidetoshi/KuuOS",
    "Packet kind: Physical Quantum Qi v0.2J-R runtime evolution finality packet",
    "append-only finality surface",
    "does not replace prior contracts, packets, source files, tests, validators, receipts, manifests, governance runners, or future Physical Quantum Qi addenda",
    "Base runtime evolution span: `v0.2J-R`",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_CI_POST_MERGE_RECEIPT_v0_2JR.md",
    "specs/physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json",
    "scripts/validate_physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.py",
    "scripts/check_physical_quantum_qi_runtime_evolution_ci_receipt_v0_2JR.py",
    "scripts/run_all_governance_full_checks_v0_1.py",
    "make physical-quantum-qi-runtime-evolution-checks",
    "make physical-quantum-qi-runtime-evolution-bundle-checks",
    "Physical Quantum Qi Runtime Evolution Validation",
    "PR #27 added the v0.2J-R runtime evolution CI surface.",
    "PR #30 added the v0.2J-R bundle manifest and validator.",
    "PR #30 final PR head: `1ba5aceead95cc3820a0c74bf8bc9f4660526a42`",
    "PR #30 squash merge commit: `027af92cae5ab76c32e685a3fc1f323617343eb8`",
    "PR #30 merged status: `merged`",
    "All Governance Validation — success",
    "Core Governance Validation — success",
    "Qi Motion Chain Validation — success",
    "Physical Quantum Qi Runtime Validation — success",
    "Physical Quantum Qi Deepening Validation — success",
    "Physical Quantum Qi Runtime Evolution Validation — success",
    "Emptiness Two Truths Runtime Audit Validation — success",
    "Emptiness Superposition Non-Collapse Validation — success",
    "GPT GitHub Integration Validation — success",
    "repository-side finality posture",
    "does not claim independent external audit acceptance",
    "`v0.2J`: Qi Bensho treatment route candidate",
    "`v0.2K`: DecisionOS clinician handoff",
    "`v0.2L`: Clinical red flag consultation governor",
    "`v0.2M`: Physical Quantum Qi observation kernel",
    "`v0.2N`: Physical Quantum Qi state transition kernel",
    "`v0.2O`: Physical Quantum Qi transition trajectory ledger",
    "`v0.2P`: Physical Quantum Qi trajectory phase transition detector",
    "`v0.2Q`: Physical Quantum Qi phase transition response governor",
    "`v0.2R`: Physical Quantum Qi response feedback loop",
    "`v0.2J-R`: CI receipt, bundle manifest, validator, and governance integration surface",
    "finality is repository-side validation finality, not clinical authority",
    "finality is integration closure, not theorem truth by itself",
    "finality is append-only and same-root",
    "runtime evolution checks remain validation-only",
    "CI green is integration evidence, not theorem truth",
    "CI green is integration evidence, not clinical authority",
    "bundle manifest records traceability and does not create execution authority",
    "observation and state-transition kernels remain non-authoritative readout surfaces",
    "transition ledgers remain append-only trace surfaces",
    "phase transition detection remains signal classification, not direct action",
    "response governance remains bounded by consultation and non-sovereignty",
    "response feedback remains non-overwriting and non-escalatory",
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
    "memory-overwrite authority",
    "governance-bypass authority",
    "A finality packet records boundary-preserving repository closure, not clinical truth.",
    "A successful CI run is validation evidence, not final theorem truth.",
    "A bundle manifest records traceability and does not grant execution authority.",
    "does not block additive-only / tighten-only v0.2S+ extensions",
    "same-root, append-only, boundary-preserving, non-destructive, and finality-packeted",
]

FORBIDDEN_TOKENS = [
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
    "finality grants clinical authority",
    "finality grants execution authority",
    "finality proves clinical truth",
    "repository finality grants clinical authority",
    "repository finality grants execution authority",
    "bundle manifest grants execution authority",
]


def main() -> int:
    errors: list[str] = []
    if not PACKET.is_file():
        errors.append(f"missing file: {PACKET.relative_to(ROOT)}")
        text = ""
    else:
        text = PACKET.read_text(encoding="utf-8")

    for token in REQUIRED_TOKENS:
        if token not in text:
            errors.append(f"{PACKET.relative_to(ROOT)} missing token: {token}")

    for token in FORBIDDEN_TOKENS:
        if token in text:
            errors.append(f"{PACKET.relative_to(ROOT)} forbidden authority-expansion token: {token}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: Physical Quantum Qi runtime evolution finality packet v0.2J-R checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
