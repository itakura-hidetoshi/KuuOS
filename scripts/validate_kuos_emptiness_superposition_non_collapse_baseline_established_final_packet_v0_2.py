#!/usr/bin/env python3
"""
validate_kuos_emptiness_superposition_non_collapse_baseline_established_final_packet_v0_2.py

Stdlib-only baseline-established-final validator for KuuOS Emptiness Superposition
Non-Collapse v0.2.

It verifies that the public governance chain has reached baseline-established-final
status without expanding authority or weakening prior semantic locks.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FINAL = ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_baseline_established_final_packet_v0_2.yaml"
CONFIRMED = ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_confirmed_baseline_packet_v0_2.yaml"
WORKFLOW = ROOT / ".github" / "workflows" / "emptiness_superposition_noncollapse_validation.yml"
PUBLIC_INDEX = ROOT / "docs" / "PUBLIC_DOCS_INDEX_v0_1.md"
VALIDATION_MATRIX = ROOT / "docs" / "VALIDATION_COVERAGE_MATRIX_v0_1.md"
PUBLIC_RELEASE_MANIFEST = ROOT / "docs" / "PUBLIC_RELEASE_PACKAGE_MANIFEST_v0_1.md"
CHAIN_INDEX = ROOT / "docs" / "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_CHAIN_INDEX_v0_2.md"

REQUIRED_FILES = [
    ROOT / "docs" / "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md",
    ROOT / "docs" / "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_CHAIN_INDEX_v0_2.md",
    ROOT / "RELEASE_NOTES_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_contract_v0_2.yaml",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_release_packet_v0_2.yaml",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_finality_packet_v0_2.yaml",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_established_baseline_packet_v0_2.yaml",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_confirmed_baseline_packet_v0_2.yaml",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_baseline_established_final_packet_v0_2.yaml",
    ROOT / "validation_cases" / "kuos_emptiness_superposition_non_collapse_validation_cases_v0_2.json",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_v0_2.py",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_release_packet_v0_2.py",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_finality_packet_v0_2.py",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_established_baseline_packet_v0_2.py",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_confirmed_baseline_packet_v0_2.py",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_baseline_established_final_packet_v0_2.py",
    ROOT / "formal" / "KUOS" / "Emptiness" / "SuperpositionNonCollapse.lean",
]

FINAL_TOKENS = [
    "kuos_emptiness_superposition_non_collapse_baseline_established_final_packet_v0_2",
    "public_governance_baseline_established_final",
    "candidate_as_superposition_not_sharp_commitment: true",
    "competing_support_blocks_direct_authority_release: true",
    "contextual_collapse_requires_receipt: true",
    "collapse_receipt_remains_conventional: true",
    "validator_pass_structural_not_truth: true",
    "public_review_surface_required: true",
    "dedicated_ci_required: true",
    "overwrite_forbidden: true",
    "same_root_required: true",
    "no_execution_from_baseline_established_final_packet: true",
]

CONFIRMED_TOKENS = [
    "kuos_emptiness_superposition_non_collapse_confirmed_baseline_packet_v0_2",
    "public_governance_baseline_confirmed",
    "no_execution_from_confirmed_baseline_packet: true",
]

EXPOSURE_TOKENS = {
    WORKFLOW: "validate_kuos_emptiness_superposition_non_collapse_confirmed_baseline_packet_v0_2.py",
    PUBLIC_INDEX: "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md",
    VALIDATION_MATRIX: "emptiness-superposition-noncollapse-checks",
    PUBLIC_RELEASE_MANIFEST: "kuos_emptiness_superposition_non_collapse_confirmed_baseline_packet_v0_2.yaml",
    CHAIN_INDEX: "kuos_emptiness_superposition_non_collapse_confirmed_baseline_packet_v0_2.yaml",
}


def require_token(path: pathlib.Path, token: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing file: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    if token not in text:
        errors.append(f"{path.relative_to(ROOT)} missing token: {token}")


def main() -> int:
    errors: list[str] = []

    for file_path in REQUIRED_FILES:
        if not file_path.is_file():
            errors.append(f"missing required artifact: {file_path.relative_to(ROOT)}")

    if FINAL.is_file():
        text = FINAL.read_text(encoding="utf-8")
        for token in FINAL_TOKENS:
            if token not in text:
                errors.append(f"baseline established final packet missing token: {token}")
    else:
        errors.append("missing baseline established final packet")

    if CONFIRMED.is_file():
        confirmed_text = CONFIRMED.read_text(encoding="utf-8")
        for token in CONFIRMED_TOKENS:
            if token not in confirmed_text:
                errors.append(f"confirmed baseline packet missing token: {token}")
    else:
        errors.append("missing confirmed baseline packet")

    for path, token in EXPOSURE_TOKENS.items():
        require_token(path, token, errors)

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS emptiness superposition non-collapse v0.2 baseline established final validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
