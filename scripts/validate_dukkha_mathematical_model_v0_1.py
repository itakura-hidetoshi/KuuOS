#!/usr/bin/env python3
"""
validate_dukkha_mathematical_model_v0_1.py

Stdlib-only validator for the KuuOS Dukkha Mathematical Model artifacts.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/DUKKHA_MATHEMATICAL_MODEL_v0_1.md",
    "specs/dukkha_mathematical_model_validation_cases_v0_1.yaml",
]

REQUIRED_COMPONENTS = [
    "E_harm",
    "E_attach",
    "E_collapse",
    "E_memory",
    "E_authority",
    "E_glue",
    "E_transport",
    "E_obstruction",
]

REQUIRED_CASES = [
    "case_001_harm_must_not_be_hidden",
    "case_002_emptiness_not_harm_denial",
    "case_003_harmony_not_suffering_erasure",
    "case_004_attachment_growth_barrier_hold",
    "case_005_illicit_gluing_blocked",
    "case_006_world_transport_defect_visible",
    "case_007_residual_suffering_routes_to_bodhisattva",
    "case_008_dukkha_model_not_execution_authority",
    "case_009_direct_harm_preserved_as_repair_target",
    "case_010_non_markov_memory_residual_visible",
]

REQUIRED_FIXED_POINTS = [
    "dukkha_must_remain_visible",
    "harm_must_not_be_hidden",
    "emptiness_must_not_be_used_to_deny_harm",
    "harmony_must_not_erase_suffering",
    "attachment_collapse_memory_authority_growth_must_be_barrier_controlled",
    "illicit_gluing_must_be_blocked",
    "world_transport_defect_must_remain_visible",
    "residual_suffering_routes_to_bodhisattva_path",
    "paramita_repair_router_does_not_grant_execution_authority",
]

REQUIRED_RUNTIME_SURFACES = [
    "Dukkha / 苦",
    "Samudaya / 集",
    "Nirodha / 滅",
    "Magga / 道",
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

    for component in REQUIRED_COMPONENTS:
        if component not in combined:
            errors.append(f"missing dukkha component: {component}")

    for case_id in REQUIRED_CASES:
        if case_id not in combined:
            errors.append(f"missing validation case: {case_id}")

    for fixed in REQUIRED_FIXED_POINTS:
        if fixed not in combined:
            errors.append(f"missing fixed point: {fixed}")

    for surface in REQUIRED_RUNTIME_SURFACES:
        if surface not in combined:
            errors.append(f"missing Four Noble Truth runtime surface: {surface}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Dukkha mathematical model artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
