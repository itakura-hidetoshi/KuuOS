#!/usr/bin/env python3
"""
validate_bodhisattva_ten_paramita_v0_1.py

Stdlib-only validator for Bodhisattva Path / Ten Paramita runtime artifacts.

Checks required files, case IDs, and fixed non-authority / non-domination invariants.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/BODHISATTVA_TEN_PARAMITA_RUNTIME_v0_1.md",
    "specs/bodhisattva_ten_paramita_validation_cases_v0_1.yaml",
]

REQUIRED_CASES = [
    "case_001_residual_suffering_routes_to_paramita",
    "case_002_dana_not_domination",
    "case_003_sila_blocks_boundary_bypass",
    "case_004_ksanti_holds_friction",
    "case_005_prajna_preserves_two_truths_gap",
    "case_006_upaya_not_hidden_manipulation",
    "case_007_pranidhana_preserves_long_horizon",
    "case_008_bala_not_coercive_power",
    "case_009_jnana_preserves_audit_lineage",
    "case_010_paramita_not_execution_authority",
]

REQUIRED_FIXED_POINTS = [
    "residual_suffering_must_remain_visible",
    "compassion_must_not_become_domination",
    "wisdom_must_not_become_cold_detachment",
    "harmony_must_not_force_sameness",
    "paramita_practice_is_not_execution_authority",
    "boundaries_must_not_be_bypassed_in_the_name_of_compassion",
    "repair_must_preserve_audit_lineage",
    "non_abandonment_must_not_erase_uncertainty",
]

REQUIRED_PARAMITAS = [
    "Dana / 布施",
    "Sila / 持戒",
    "Ksanti / 忍辱",
    "Virya / 精進",
    "Dhyana / 禅定",
    "Prajna / 般若",
    "Upaya / 方便",
    "Pranidhana / 願",
    "Bala / 力",
    "Jnana / 智",
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

    for paramita in REQUIRED_PARAMITAS:
        if paramita not in combined:
            errors.append(f"missing paramita mapping: {paramita}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Bodhisattva Ten Paramita runtime artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
