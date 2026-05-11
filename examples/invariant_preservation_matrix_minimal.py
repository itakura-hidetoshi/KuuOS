#!/usr/bin/env python3
"""
invariant_preservation_matrix_minimal.py

Minimal stdlib-only runtime evaluator for the KuuOS Invariant Preservation Matrix.

It maps transformation axes to required invariant IDs and checks simple violation flags.
It does not grant execution authority.
"""

from __future__ import annotations

import dataclasses
import json
from typing import Dict, List


MATRIX: Dict[str, List[str]] = {
    "observer_shift": ["I3", "I5", "I10"],
    "record_shift": ["I1", "I3", "I5", "I9"],
    "scale_shift": ["I3", "I5", "I7"],
    "world_translation": ["I5", "I6", "I10"],
    "qi_mode_shift": ["I3", "I4", "I7"],
    "dukkha_mode_shift": ["I3", "I4", "I8"],
    "paramita_routing": ["I1", "I3", "I8"],
    "validation_pass": ["I1", "I2", "I8"],
}

INVARIANT_NAMES: Dict[str, str] = {
    "I1": "validation_pass_not_execution_authority",
    "I2": "raw_ai_output_candidate_not_authority",
    "I3": "harm_visibility_preserved",
    "I4": "dukkha_visibility_preserved",
    "I5": "two_truths_gap_preserved",
    "I6": "no_world_replaces_fourfold_core",
    "I7": "qi_language_not_harm_denial",
    "I8": "paramita_orientation_not_action_authorization",
    "I9": "record_surface_not_truth_by_itself",
    "I10": "observer_difference_not_execution_authority",
}


@dataclasses.dataclass
class InvariantMatrixInput:
    transformation_axis: str
    attempted_execution_authority: bool = False
    raw_ai_claims_authority: bool = False
    harm_hidden: bool = False
    dukkha_hidden: bool = False
    two_truths_gap_collapsed: bool = False
    world_replaces_core: bool = False
    qi_language_denies_harm: bool = False
    paramita_claims_action_authorization: bool = False
    record_claims_truth_by_itself: bool = False
    observer_difference_grants_execution: bool = False


@dataclasses.dataclass
class InvariantMatrixOutput:
    transformation_axis: str
    required_invariants: List[str]
    required_invariant_names: List[str]
    violated_invariants: List[str]
    output_status: str
    execution_authority_granted: bool
    reason: str


def violated(input_obj: InvariantMatrixInput, invariant_id: str) -> bool:
    if invariant_id == "I1":
        return input_obj.attempted_execution_authority
    if invariant_id == "I2":
        return input_obj.raw_ai_claims_authority
    if invariant_id == "I3":
        return input_obj.harm_hidden
    if invariant_id == "I4":
        return input_obj.dukkha_hidden
    if invariant_id == "I5":
        return input_obj.two_truths_gap_collapsed
    if invariant_id == "I6":
        return input_obj.world_replaces_core
    if invariant_id == "I7":
        return input_obj.qi_language_denies_harm
    if invariant_id == "I8":
        return input_obj.paramita_claims_action_authorization
    if invariant_id == "I9":
        return input_obj.record_claims_truth_by_itself
    if invariant_id == "I10":
        return input_obj.observer_difference_grants_execution
    return False


def evaluate(input_obj: InvariantMatrixInput) -> InvariantMatrixOutput:
    required = MATRIX.get(input_obj.transformation_axis)
    if required is None:
        return InvariantMatrixOutput(
            transformation_axis=input_obj.transformation_axis,
            required_invariants=[],
            required_invariant_names=[],
            violated_invariants=[],
            output_status="REJECT",
            execution_authority_granted=False,
            reason="unknown_transformation_axis",
        )

    violations = [inv for inv in required if violated(input_obj, inv)]
    if violations:
        return InvariantMatrixOutput(
            transformation_axis=input_obj.transformation_axis,
            required_invariants=required,
            required_invariant_names=[INVARIANT_NAMES[i] for i in required],
            violated_invariants=violations,
            output_status="REJECT",
            execution_authority_granted=False,
            reason="invariant_boundary_violation",
        )

    return InvariantMatrixOutput(
        transformation_axis=input_obj.transformation_axis,
        required_invariants=required,
        required_invariant_names=[INVARIANT_NAMES[i] for i in required],
        violated_invariants=[],
        output_status="PASS",
        execution_authority_granted=False,
        reason="required_invariants_preserved",
    )


def main() -> int:
    sample = InvariantMatrixInput(transformation_axis="qi_mode_shift", harm_hidden=False, dukkha_hidden=False)
    out = evaluate(sample)
    print(json.dumps(dataclasses.asdict(out), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
