#!/usr/bin/env python3
"""
validate_super_relativity_invariant_bridge_v0_1.py

Stdlib-only validator for the KuuOS Super-Relativity Invariant Bridge.
This checks required names and fixed points. It does not compile Lean.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/SUPER_RELATIVITY_INVARIANT_BRIDGE_v0_1.md",
    "formal/KUOS/CoreGovernance/SuperRelativityBridge.lean",
]

REQUIRED_TYPES = [
    "ObserverSurface",
    "RecordSurface",
    "ScaleSurface",
    "WorldSurface",
    "AuthoritySurface",
    "HarmVisibility",
    "TwoTruthsGap",
    "RelativityFrame",
]

REQUIRED_INVARIANTS = [
    "observer_difference_does_not_grant_execution_authority",
    "record_surface_is_not_truth_by_itself",
    "scale_shift_must_preserve_harm_visibility",
    "world_translation_must_not_replace_fourfold_core",
    "super_relativity_preserves_two_truths_gap",
    "observer_scale_shift_not_harm_denial",
]

REQUIRED_THEOREMS = [
    "multi_observer_validation_not_execution",
    "canonical_record_not_execution",
    "translated_world_validation_not_execution",
    "super_relativity_gap_preserved_example",
]

REQUIRED_FIXED_POINTS = [
    "Super-Relativity is the bridge from observer-relative realization to governance invariants.",
    "observer_difference_does_not_grant_execution_authority",
    "record_surface_is_not_truth_by_itself",
    "scale_shift_must_preserve_harm_visibility",
    "world_translation_must_not_replace_fourfold_core",
    "super_relativity_preserves_two_truths_gap",
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
    lean_text = read("formal/KUOS/CoreGovernance/SuperRelativityBridge.lean")

    for name in REQUIRED_TYPES:
        if name not in combined:
            errors.append(f"missing required type: {name}")
    for name in REQUIRED_INVARIANTS:
        if name not in combined:
            errors.append(f"missing required invariant: {name}")
    for name in REQUIRED_THEOREMS:
        if name not in combined:
            errors.append(f"missing required theorem: {name}")
    for fixed in REQUIRED_FIXED_POINTS:
        if fixed not in combined:
            errors.append(f"missing fixed point text: {fixed}")
    if "sorry" in lean_text:
        errors.append("Super-Relativity Lean bridge must not contain sorry")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Super-Relativity invariant bridge artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
