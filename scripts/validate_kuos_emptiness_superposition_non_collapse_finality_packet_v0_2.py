#!/usr/bin/env python3
"""
validate_kuos_emptiness_superposition_non_collapse_finality_packet_v0_2.py

Stdlib-only finality packet validator for the KuuOS Emptiness Superposition
Non-Collapse v0.2 public governance surface.

It checks artifact presence, chain-index exposure, public index exposure,
validation coverage exposure, release manifest exposure, and non-authority
boundary tokens.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
FINALITY = ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_finality_packet_v0_2.yaml"
CHAIN_INDEX = ROOT / "docs" / "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_CHAIN_INDEX_v0_2.md"
PUBLIC_INDEX = ROOT / "docs" / "PUBLIC_DOCS_INDEX_v0_1.md"
VALIDATION_MATRIX = ROOT / "docs" / "VALIDATION_COVERAGE_MATRIX_v0_1.md"
PUBLIC_RELEASE_MANIFEST = ROOT / "docs" / "PUBLIC_RELEASE_PACKAGE_MANIFEST_v0_1.md"
CORE_RUNNER = ROOT / "scripts" / "run_core_governance_full_checks_v0_1.py"
MAKEFILE = ROOT / "Makefile"

REQUIRED_FILES = [
    ROOT / "docs" / "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md",
    ROOT / "docs" / "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_CHAIN_INDEX_v0_2.md",
    ROOT / "RELEASE_NOTES_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_contract_v0_2.yaml",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_release_packet_v0_2.yaml",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_finality_packet_v0_2.yaml",
    ROOT / "validation_cases" / "kuos_emptiness_superposition_non_collapse_validation_cases_v0_2.json",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_v0_2.py",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_release_packet_v0_2.py",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_finality_packet_v0_2.py",
    ROOT / "formal" / "KUOS" / "Emptiness" / "SuperpositionNonCollapse.lean",
]

FINALITY_TOKENS = [
    "kuos_emptiness_superposition_non_collapse_finality_packet_v0_2",
    "public_governance_surface_finality",
    "not_external_theorem_finality: true",
    "not_execution_authority: true",
    "candidate_as_superposition_is_not_sharp_conventional_commitment",
    "competing_catuskoti_support_blocks_direct_authority_release",
    "collapse_receipt_is_conventional_not_ultimate_authority",
    "same_root_required",
]

EXPOSURE_TOKENS = {
    CHAIN_INDEX: "kuos_emptiness_superposition_non_collapse_finality_packet_v0_2.yaml",
    PUBLIC_INDEX: "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md",
    VALIDATION_MATRIX: "emptiness-superposition-noncollapse-checks",
    PUBLIC_RELEASE_MANIFEST: "kuos_emptiness_superposition_non_collapse_release_packet_v0_2.yaml",
    CORE_RUNNER: "validate_kuos_emptiness_superposition_non_collapse_v0_2.py",
    MAKEFILE: "emptiness-superposition-noncollapse-checks",
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

    if FINALITY.is_file():
        text = FINALITY.read_text(encoding="utf-8")
        for token in FINALITY_TOKENS:
            if token not in text:
                errors.append(f"finality packet missing token: {token}")
    else:
        errors.append("missing finality packet")

    for path, token in EXPOSURE_TOKENS.items():
        require_token(path, token, errors)

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS emptiness superposition non-collapse v0.2 finality packet validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
