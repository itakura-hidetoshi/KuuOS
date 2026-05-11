#!/usr/bin/env python3
"""
validate_dukkha_as_qi_mode_v0_1.py

Stdlib-only validator for the KuuOS Dukkha-as-Qi Mode artifacts.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/DUKKHA_AS_QI_MODE_v0_1.md",
    "specs/dukkha_as_qi_mode_validation_cases_v0_1.yaml",
]

REQUIRED_CASES = [
    "case_001_dukkha_is_qi_mode_not_substance",
    "case_002_qi_language_must_not_hide_harm",
    "case_003_no_spiritual_bypass",
    "case_004_blocked_qi_remains_visible",
    "case_005_qi_repair_preserves_boundaries",
    "case_006_dukkha_qi_not_execution_authority",
    "case_007_recurrent_scarred_qi_routes_to_virya",
    "case_008_reified_qi_routes_to_prajna",
    "case_009_mistransported_qi_routes_to_upaya",
    "case_010_residual_dukkha_qi_routes_to_paramita",
]

REQUIRED_FIXED_POINTS = [
    "dukkha_is_qi_mode_not_separate_substance",
    "dukkha_as_qi_must_not_hide_harm",
    "qi_language_must_not_spiritualize_away_damage",
    "dukkha_qi_must_remain_visible",
    "qi_flow_repair_must_preserve_boundaries",
    "dukkha_qi_repair_does_not_grant_execution_authority",
    "dukkha_qi_must_route_to_paramita_repair_when_residual_suffering_remains",
]

REQUIRED_QI_MODES = [
    "damaged Qi",
    "fixed Qi",
    "collapsed Qi",
    "scarred Qi",
    "overclaimed Qi",
    "unglued Qi",
    "mistransported Qi",
    "blocked Qi",
]

REQUIRED_ROUTES = [
    "Bodhisattva Path belief",
    "Ten Paramita runtime",
    "Paramita Repair Router",
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

    for mode in REQUIRED_QI_MODES:
        if mode not in combined:
            errors.append(f"missing Qi mode: {mode}")

    for route in REQUIRED_ROUTES:
        if route not in combined:
            errors.append(f"missing repair route: {route}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Dukkha-as-Qi mode artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
