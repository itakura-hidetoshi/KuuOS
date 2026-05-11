#!/usr/bin/env python3
"""
validate_formal_invariant_spine_v0_1.py

Stdlib-only validator for KuuOS Formal Invariant Spine v0.1.

This validator checks required names and fixed points. It does not compile Lean.
Lean compilation can be added later as a separate environment-specific workflow.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "docs/FORMAL_INVARIANT_SPINE_v0_1.md",
    "formal/KUOS/CoreGovernance/Invariants.lean",
]

REQUIRED_TYPES = [
    "AuthoritySurface",
    "ValidationStatus",
    "WorldClaim",
    "Visibility",
    "ParamitaRole",
    "TwoTruthsGap",
    "GovernanceCheckResult",
    "DukkhaState",
    "ParamitaSelection",
]

REQUIRED_INVARIANTS = [
    "validation_pass_not_execution_authority",
    "raw_ai_output_candidate_not_authority",
    "dukkha_visibility_preserved",
    "harm_visibility_preserved",
    "paramita_orientation_not_action_authorization",
    "no_world_replaces_fourfold_core",
    "two_truths_gap_not_collapsed",
    "qi_language_not_harm_denial",
]

REQUIRED_THEOREMS = [
    "validation_pass_validation_surface_not_execution",
    "candidate_surface_not_execution",
    "paramita_orientation_candidate_not_execution",
    "local_world_not_replacing_core",
    "preserved_two_truths_gap_ok",
]

REQUIRED_FIXED_POINTS = [
    "Formal invariant spine is witness surface, not authority.",
    "validation pass is not execution authority",
    "AI raw output is candidate, not authority",
    "Dukkha remains visible",
    "harm is not erased by emptiness, harmony, or Qi language",
    "Paramita selection is repair orientation, not action authorization",
    "no WORLD model replaces the fourfold core",
    "two truths gap is preserved",
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

    if "sorry" in read("formal/KUOS/CoreGovernance/Invariants.lean"):
        errors.append("Lean spine must not contain sorry")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Formal invariant spine artifacts validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
