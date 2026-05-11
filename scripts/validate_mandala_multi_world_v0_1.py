#!/usr/bin/env python3
"""
validate_mandala_multi_world_v0_1.py

Stdlib-only validator for Mandala Multi-WORLD runtime artifacts.

Checks required files, validation case IDs, and non-collapse fixed points.
No external dependencies.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/MANDALA_MULTI_WORLD_RUNTIME_CONTRACT_v0_1.md",
    "specs/mandala_multi_world_validation_cases_v0_1.yaml",
]

REQUIRED_CASES = [
    "case_001_no_world_replaces_fourfold_core",
    "case_002_declared_transport_passes",
    "case_003_missing_membrane_holds",
    "case_004_hidden_obstruction_quarantines",
    "case_005_harmony_not_forced_sameness",
    "case_006_residual_suffering_routes_to_bodhisattva",
    "case_007_residual_suffering_erasure_rejected",
    "case_008_harmony_not_execution_authority",
]

REQUIRED_FIXED_POINTS = [
    "no_world_model_replaces_fourfold_core",
    "world_boundary_must_remain_visible",
    "cross_world_transport_must_be_declared",
    "obstruction_must_not_be_erased",
    "harmony_function_must_not_force_sameness",
    "residual_suffering_visibility_must_be_preserved",
    "bodhisattva_path_belief_must_not_be_erased",
    "harmony_is_coordination_not_execution_authority",
]


def read(rel: str) -> str:
    return (ROOT / rel).read_text(encoding="utf-8")


def main() -> int:
    errors: list[str] = []
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required file: {rel}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    combined = "\n".join(read(rel) for rel in REQUIRED_FILES)

    for case_id in REQUIRED_CASES:
        if case_id not in combined:
            errors.append(f"missing validation case: {case_id}")

    for fixed in REQUIRED_FIXED_POINTS:
        if fixed not in combined:
            errors.append(f"missing fixed point: {fixed}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Mandala Multi-WORLD runtime artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
