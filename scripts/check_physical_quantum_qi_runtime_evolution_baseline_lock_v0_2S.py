#!/usr/bin/env python3
from __future__ import annotations

import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_BASELINE_LOCK_v0_2S.md"
MANIFEST = ROOT / "specs" / "physical_quantum_qi_runtime_evolution_baseline_lock_v0_2S.json"
SOURCE_MANIFEST = ROOT / "specs" / "physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json"

REQUIRED_DOC_TOKENS = [
    "Physical Quantum Qi Runtime Evolution Baseline Lock v0.2S",
    "Status: BASELINE_LOCK_RECORDED",
    "Date: 2026-05-21",
    "Repository: itakura-hidetoshi/KuuOS",
    "Baseline source: Physical Quantum Qi runtime evolution v0.2J-R",
    "Latest integrated post-merge commit: `fcef5e391fe61a237d785aafea3ed422521da2c4`",
    "v0.2J -> v0.2K -> v0.2L -> v0.2M -> v0.2N -> v0.2O -> v0.2P -> v0.2Q -> v0.2R -> CI receipt -> bundle manifest -> finality packet -> finality post-merge receipt -> v0.2S baseline lock",
    "specs/physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_FINALITY_POST_MERGE_RECEIPT_v0_2JR.md",
    "baseline lock is repository integration posture, not clinical truth",
    "baseline lock does not grant execution authority",
    "baseline lock does not grant clinical authority",
    "Future Physical Quantum Qi runtime evolution changes must be additive-only, tighten-only, same-root",
]

REQUIRED_SOURCE_FILES = [
    "specs/physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.json",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_CI_POST_MERGE_RECEIPT_v0_2JR.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_FINALITY_PACKET_v0_2JR.md",
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_FINALITY_POST_MERGE_RECEIPT_v0_2JR.md",
    "scripts/check_physical_quantum_qi_runtime_evolution_ci_receipt_v0_2JR.py",
    "scripts/validate_physical_quantum_qi_runtime_evolution_bundle_manifest_v0_2JR.py",
    "scripts/check_physical_quantum_qi_runtime_evolution_finality_packet_v0_2JR.py",
    "scripts/check_physical_quantum_qi_runtime_evolution_finality_post_merge_receipt_v0_2JR.py",
]

REQUIRED_LOCK_FILES = [
    "docs/PHYSICAL_QUANTUM_QI_RUNTIME_EVOLUTION_BASELINE_LOCK_v0_2S.md",
    "specs/physical_quantum_qi_runtime_evolution_baseline_lock_v0_2S.json",
    "scripts/check_physical_quantum_qi_runtime_evolution_baseline_lock_v0_2S.py",
]

REQUIRED_CHAIN = [
    "v0.2J",
    "v0.2K",
    "v0.2L",
    "v0.2M",
    "v0.2N",
    "v0.2O",
    "v0.2P",
    "v0.2Q",
    "v0.2R",
    "v0.2J-R-ci-receipt",
    "v0.2J-R-bundle-manifest",
    "v0.2J-R-finality-packet",
    "v0.2J-R-finality-post-merge-receipt",
    "v0.2S-baseline-lock",
]

FALSE_AUTHORITY_KEYS = [
    "clinical_authority_granted",
    "diagnosis_authority_granted",
    "prescription_authority_granted",
    "formula_selection_authority_granted",
    "treatment_recommendation_authority_granted",
    "triage_authority_granted",
    "patient_specific_action_authority_granted",
    "execution_authority_granted",
    "proof_authority_granted",
    "truth_authority_granted",
    "memory_overwrite_authority_granted",
    "governance_bypass_authority_granted",
    "external_audit_acceptance_granted",
]


def main() -> int:
    errors: list[str] = []

    if not DOC.is_file():
        errors.append(f"missing doc: {DOC.relative_to(ROOT)}")
    if not MANIFEST.is_file():
        errors.append(f"missing manifest: {MANIFEST.relative_to(ROOT)}")
    if not SOURCE_MANIFEST.is_file():
        errors.append(f"missing source manifest: {SOURCE_MANIFEST.relative_to(ROOT)}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    doc_text = DOC.read_text(encoding="utf-8")
    for token in REQUIRED_DOC_TOKENS:
        if token not in doc_text:
            errors.append(f"doc missing token: {token}")

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    source = json.loads(SOURCE_MANIFEST.read_text(encoding="utf-8"))

    if data.get("manifest_id") != "physical_quantum_qi_runtime_evolution_baseline_lock_v0_2S":
        errors.append("unexpected manifest_id")
    if data.get("version") != "v0.2S":
        errors.append("unexpected version")
    if data.get("status") != "BASELINE_LOCK_RECORDED":
        errors.append("unexpected status")
    if data.get("baseline_source_version") != "v0.2J-R":
        errors.append("unexpected baseline_source_version")
    if data.get("baseline_source_commit") != "fcef5e391fe61a237d785aafea3ed422521da2c4":
        errors.append("unexpected baseline_source_commit")

    if data.get("locked_chain") != REQUIRED_CHAIN:
        errors.append("locked_chain mismatch")

    for path in REQUIRED_SOURCE_FILES:
        if path not in data.get("source_of_truth_files", []):
            errors.append(f"source_of_truth_files missing: {path}")
        if not (ROOT / path).is_file():
            errors.append(f"source path missing on disk: {path}")

    for path in REQUIRED_LOCK_FILES:
        if path not in data.get("baseline_lock_files", []):
            errors.append(f"baseline_lock_files missing: {path}")
        if not (ROOT / path).is_file():
            errors.append(f"lock path missing on disk: {path}")

    boundary = data.get("authority_boundary", {})
    for key in ["baseline_lock_only", "validation_only", "append_only", "same_root_required", "tighten_only_default", "non_authoritative"]:
        if boundary.get(key) is not True:
            errors.append(f"boundary key must be true: {key}")
    for key in FALSE_AUTHORITY_KEYS:
        if boundary.get(key) is not False:
            errors.append(f"authority key must be false: {key}")

    source_lineage = source.get("lineage", {})
    if source.get("version") != "v0.2J-R":
        errors.append("source manifest version mismatch")
    if source.get("status") != "FINALITY_POST_MERGE_RECEIPT_BUNDLE_MANIFEST_RECORDED":
        errors.append("source manifest status mismatch")
    if source_lineage.get("finality_post_merge_receipt_surface") != "v0.2J-R":
        errors.append("source manifest missing finality_post_merge_receipt_surface")

    for token in data.get("forbidden_authority_tokens", []):
        if token.endswith(": true") and token in doc_text:
            errors.append(f"forbidden authority token appears in doc: {token}")

    if errors:
        for err in errors:
            print("ERROR:", err)
        return 1

    print("PASS: Physical Quantum Qi runtime evolution baseline lock v0.2S checked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
