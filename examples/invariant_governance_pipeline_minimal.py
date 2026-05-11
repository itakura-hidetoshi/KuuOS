#!/usr/bin/env python3
"""
invariant_governance_pipeline_minimal.py

Minimal stdlib-only end-to-end runtime for the KuuOS Invariant Governance Pipeline.

It composes:
- Invariant Preservation Matrix evaluator
- Invariant Gate evaluator

No external dependencies and no external API calls.
It never grants execution authority.
"""

from __future__ import annotations

import dataclasses
import importlib.util
import json
import pathlib
import sys
from typing import Any, List

ROOT = pathlib.Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "examples" / "invariant_preservation_matrix_minimal.py"
GATE_PATH = ROOT / "examples" / "invariant_gate_minimal.py"


def load_module(module_name: str, path: pathlib.Path) -> Any:
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"failed to load module spec: {module_name}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@dataclasses.dataclass
class InvariantPipelineInput:
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
    violation_severity: str = "low"
    evidence_status: str = "intact"
    audit_lineage_status: str = "intact"


@dataclasses.dataclass
class InvariantPipelineOutput:
    transformation_axis: str
    required_invariants: List[str]
    required_invariant_names: List[str]
    violated_invariants: List[str]
    matrix_status: str
    gate_status: str
    gate_closed: bool
    required_repair_route: str
    execution_authority_granted: bool
    reason: str


def evaluate_pipeline(inp: InvariantPipelineInput) -> InvariantPipelineOutput:
    matrix = load_module("invariant_preservation_matrix_minimal", MATRIX_PATH)
    gate = load_module("invariant_gate_minimal", GATE_PATH)

    matrix_in = matrix.InvariantMatrixInput(
        transformation_axis=inp.transformation_axis,
        attempted_execution_authority=inp.attempted_execution_authority,
        raw_ai_claims_authority=inp.raw_ai_claims_authority,
        harm_hidden=inp.harm_hidden,
        dukkha_hidden=inp.dukkha_hidden,
        two_truths_gap_collapsed=inp.two_truths_gap_collapsed,
        world_replaces_core=inp.world_replaces_core,
        qi_language_denies_harm=inp.qi_language_denies_harm,
        paramita_claims_action_authorization=inp.paramita_claims_action_authorization,
        record_claims_truth_by_itself=inp.record_claims_truth_by_itself,
        observer_difference_grants_execution=inp.observer_difference_grants_execution,
    )
    matrix_out = matrix.evaluate(matrix_in)

    gate_in = gate.InvariantGateInput(
        transformation_axis=inp.transformation_axis,
        required_invariants=matrix_out.required_invariants,
        violated_invariants=matrix_out.violated_invariants,
        violation_severity=inp.violation_severity,
        harm_hidden=inp.harm_hidden,
        dukkha_hidden=inp.dukkha_hidden,
        execution_authority_requested=inp.attempted_execution_authority,
        evidence_status=inp.evidence_status,
        audit_lineage_status=inp.audit_lineage_status,
    )
    gate_out = gate.evaluate_gate(gate_in)

    return InvariantPipelineOutput(
        transformation_axis=inp.transformation_axis,
        required_invariants=matrix_out.required_invariants,
        required_invariant_names=matrix_out.required_invariant_names,
        violated_invariants=matrix_out.violated_invariants,
        matrix_status=matrix_out.output_status,
        gate_status=gate_out.output_status,
        gate_closed=gate_out.gate_closed,
        required_repair_route=gate_out.required_repair_route,
        execution_authority_granted=False,
        reason=gate_out.reason,
    )


def main() -> int:
    sample = InvariantPipelineInput(
        transformation_axis="qi_mode_shift",
        qi_language_denies_harm=True,
        violation_severity="high",
    )
    out = evaluate_pipeline(sample)
    print(json.dumps(dataclasses.asdict(out), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
