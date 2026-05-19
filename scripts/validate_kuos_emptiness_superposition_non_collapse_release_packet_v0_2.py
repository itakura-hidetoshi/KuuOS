#!/usr/bin/env python3
"""
validate_kuos_emptiness_superposition_non_collapse_release_packet_v0_2.py

Stdlib-only release packet validator for KuuOS Emptiness Superposition Non-Collapse v0.2.

It checks artifact presence, release-boundary tokens, Makefile target inclusion,
and core governance runner integration. It does not grant truth, proof, clinical,
world, or execution authority.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PACKET = ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_release_packet_v0_2.yaml"
MAKEFILE = ROOT / "Makefile"
CORE_RUNNER = ROOT / "scripts" / "run_core_governance_full_checks_v0_1.py"
REQUIRED_FILES = [
    ROOT / "docs" / "KUOS_EMPTINESS_SUPERPOSITION_NON_COLLAPSE_v0_2.md",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_contract_v0_2.yaml",
    ROOT / "specs" / "kuos_emptiness_superposition_non_collapse_release_packet_v0_2.yaml",
    ROOT / "validation_cases" / "kuos_emptiness_superposition_non_collapse_validation_cases_v0_2.json",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_v0_2.py",
    ROOT / "scripts" / "validate_kuos_emptiness_superposition_non_collapse_release_packet_v0_2.py",
    ROOT / "formal" / "KUOS" / "Emptiness" / "SuperpositionNonCollapse.lean",
]

REQUIRED_PACKET_TOKENS = [
    "kuos_emptiness_superposition_non_collapse_release_packet_v0_2",
    "candidate-as-superposition != sharp conventional commitment",
    "release_packet_not_execution_authority: true",
    "lean_surface_not_completed_external_proof: true",
    "core_runner_includes_v0_2_validator",
    "forbidden_direct_routes_blocked",
    "normalization_checked",
]


def require_text(path: pathlib.Path, token: str, errors: list[str]) -> None:
    if not path.is_file():
        errors.append(f"missing file for token check: {path.relative_to(ROOT)}")
        return
    text = path.read_text(encoding="utf-8")
    if token not in text:
        errors.append(f"{path.relative_to(ROOT)} missing token: {token}")


def main() -> int:
    errors: list[str] = []

    for file_path in REQUIRED_FILES:
        if not file_path.is_file():
            errors.append(f"missing required artifact: {file_path.relative_to(ROOT)}")

    if PACKET.is_file():
        packet_text = PACKET.read_text(encoding="utf-8")
        for token in REQUIRED_PACKET_TOKENS:
            if token not in packet_text:
                errors.append(f"release packet missing token: {token}")
    else:
        errors.append("missing release packet")

    require_text(MAKEFILE, "emptiness-superposition-noncollapse-checks", errors)
    require_text(CORE_RUNNER, "validate_kuos_emptiness_superposition_non_collapse_v0_2.py", errors)

    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print("PASS: KuuOS emptiness superposition non-collapse v0.2 release packet validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
