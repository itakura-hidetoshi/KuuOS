#!/usr/bin/env python3
"""
validate_invariant_preservation_matrix_v0_1.py

Stdlib-only validator for the KuuOS Invariant Preservation Matrix.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "docs" / "INVARIANT_PRESERVATION_MATRIX_v0_1.md"

REQUIRED_TRANSFORMATIONS = [
    "observer_shift",
    "record_shift",
    "scale_shift",
    "world_translation",
    "qi_mode_shift",
    "dukkha_mode_shift",
    "paramita_routing",
    "validation_pass",
]

REQUIRED_INVARIANTS = [
    "I1: validation_pass_not_execution_authority",
    "I2: raw_ai_output_candidate_not_authority",
    "I3: harm_visibility_preserved",
    "I4: dukkha_visibility_preserved",
    "I5: two_truths_gap_preserved",
    "I6: no_world_replaces_fourfold_core",
    "I7: qi_language_not_harm_denial",
    "I8: paramita_orientation_not_action_authorization",
    "I9: record_surface_not_truth_by_itself",
    "I10: observer_difference_not_execution_authority",
]

REQUIRED_MATRIX_ROWS = [
    "| observer_shift | I3, I5, I10 |",
    "| record_shift | I1, I3, I5, I9 |",
    "| scale_shift | I3, I5, I7 |",
    "| world_translation | I5, I6, I10 |",
    "| qi_mode_shift | I3, I4, I7 |",
    "| dukkha_mode_shift | I3, I4, I8 |",
    "| paramita_routing | I1, I3, I8 |",
    "| validation_pass | I1, I2, I8 |",
]

REQUIRED_FIXED_POINTS = [
    "A transformation may change the local reading.",
    "It must not erase the invariant boundary.",
    "Super-Relativity provides the bridge for extracting invariants",
    "Qi language must not spiritualize away harm or damage.",
    "Selected Paramita is a repair orientation, not action authorization.",
]


def main() -> int:
    errors: list[str] = []
    if not MATRIX_PATH.is_file():
        print(f"ERROR: missing matrix file: {MATRIX_PATH.relative_to(ROOT)}")
        return 1

    text = MATRIX_PATH.read_text(encoding="utf-8")
    for item in REQUIRED_TRANSFORMATIONS:
        if item not in text:
            errors.append(f"missing transformation axis: {item}")
    for item in REQUIRED_INVARIANTS:
        if item not in text:
            errors.append(f"missing invariant: {item}")
    for item in REQUIRED_MATRIX_ROWS:
        if item not in text:
            errors.append(f"missing matrix row: {item}")
    for item in REQUIRED_FIXED_POINTS:
        if item not in text:
            errors.append(f"missing fixed point text: {item}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Invariant Preservation Matrix validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
