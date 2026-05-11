#!/usr/bin/env python3
"""
validate_invariant_governance_pipeline_v0_1.py

Stdlib-only validator for the KuuOS Invariant Governance Pipeline.
"""

from __future__ import annotations

import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
PIPELINE_PATH = ROOT / "docs" / "INVARIANT_GOVERNANCE_PIPELINE_v0_1.md"

REQUIRED_FILES = [
    "docs/SUPER_RELATIVITY_INVARIANT_BRIDGE_v0_1.md",
    "docs/FORMAL_INVARIANT_SPINE_v0_1.md",
    "docs/INVARIANT_PRESERVATION_MATRIX_v0_1.md",
    "docs/INVARIANT_GATE_RUNTIME_v0_1.md",
    "examples/invariant_preservation_matrix_minimal.py",
    "examples/invariant_gate_minimal.py",
]

REQUIRED_CHAIN = [
    "Super-Relativity Invariant Bridge",
    "Formal Invariant Spine",
    "Invariant Preservation Matrix",
    "Invariant Gate Runtime",
    "PASS | HOLD | REPAIR | REJECT | QUARANTINE",
    "no execution authority",
]

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

REQUIRED_HARD_CLOSURES = [
    "execution_authority_requested -> REJECT",
    "harm_hidden -> REJECT",
    "critical_invariant_violation -> REJECT",
    "missing_evidence_or_audit_lineage -> QUARANTINE",
]

REQUIRED_GUARDRAILS = [
    "execution authority",
    "clinical authority",
    "proof of truth",
    "proof of Ten'i",
    "permission to hide harm",
    "permission to collapse two truths",
    "permission to replace the fourfold core",
]


def main() -> int:
    errors: list[str] = []
    if not PIPELINE_PATH.is_file():
        print(f"ERROR: missing pipeline file: {PIPELINE_PATH.relative_to(ROOT)}")
        return 1

    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            errors.append(f"missing required linked file: {rel}")

    text = PIPELINE_PATH.read_text(encoding="utf-8")
    for item in REQUIRED_CHAIN:
        if item not in text:
            errors.append(f"missing pipeline chain item: {item}")
    for item in REQUIRED_TRANSFORMATIONS:
        if item not in text:
            errors.append(f"missing transformation axis: {item}")
    for item in REQUIRED_INVARIANTS:
        if item not in text:
            errors.append(f"missing invariant: {item}")
    for item in REQUIRED_HARD_CLOSURES:
        if item not in text:
            errors.append(f"missing hard closure: {item}")
    for item in REQUIRED_GUARDRAILS:
        if item not in text:
            errors.append(f"missing guardrail: {item}")

    if errors:
        for e in errors:
            print(f"ERROR: {e}")
        return 1

    print("PASS: Invariant Governance Pipeline validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
