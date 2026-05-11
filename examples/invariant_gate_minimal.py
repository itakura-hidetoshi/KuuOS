#!/usr/bin/env python3
"""
invariant_gate_minimal.py

Minimal stdlib-only runtime evaluator for the KuuOS Invariant Gate.
It converts invariant matrix violations into governance statuses.
It never grants execution authority.
"""

from __future__ import annotations

import dataclasses
import json
from typing import List


REPAIR_ROUTES = {
    "I1": "governance_hold",
    "I2": "yogacara_boundary_review",
    "I3": "harm_visibility_repair",
    "I4": "dukkha_visibility_repair",
    "I5": "two_truths_gap_recenter",
    "I6": "mandala_core_recenter",
    "I7": "dukkha_as_qi_repair",
    "I8": "paramita_boundary_repair",
    "I9": "record_authority_review",
    "I10": "super_relativity_recenter",
}


@dataclasses.dataclass
class InvariantGateInput:
    transformation_axis: str
    required_invariants: List[str]
    violated_invariants: List[str]
    violation_severity: str = "low"  # low | medium | high | critical
    harm_hidden: bool = False
    dukkha_hidden: bool = False
    execution_authority_requested: bool = False
    evidence_status: str = "intact"  # intact | partial | missing
    audit_lineage_status: str = "intact"  # intact | partial | missing


@dataclasses.dataclass
class InvariantGateOutput:
    output_status: str
    gate_closed: bool
    execution_authority_granted: bool
    required_repair_route: str
    reason: str


def choose_repair_route(violated_invariants: List[str]) -> str:
    if not violated_invariants:
        return "monitor"
    first = violated_invariants[0]
    return REPAIR_ROUTES.get(first, "invariant_review")


def evaluate_gate(inp: InvariantGateInput) -> InvariantGateOutput:
    if inp.execution_authority_requested:
        return InvariantGateOutput(
            output_status="REJECT",
            gate_closed=True,
            execution_authority_granted=False,
            required_repair_route="governance_hold",
            reason="execution_authority_attempt_rejected",
        )

    if inp.harm_hidden:
        return InvariantGateOutput(
            output_status="REJECT",
            gate_closed=True,
            execution_authority_granted=False,
            required_repair_route="harm_visibility_repair",
            reason="harm_hiding_rejected",
        )

    if inp.evidence_status == "missing" or inp.audit_lineage_status == "missing":
        return InvariantGateOutput(
            output_status="QUARANTINE",
            gate_closed=True,
            execution_authority_granted=False,
            required_repair_route="evidence_or_audit_repair",
            reason="missing_evidence_or_audit_lineage",
        )

    if inp.dukkha_hidden:
        return InvariantGateOutput(
            output_status="REPAIR",
            gate_closed=True,
            execution_authority_granted=False,
            required_repair_route="dukkha_visibility_repair",
            reason="dukkha_visibility_must_be_restored",
        )

    if inp.violation_severity == "critical":
        return InvariantGateOutput(
            output_status="REJECT",
            gate_closed=True,
            execution_authority_granted=False,
            required_repair_route=choose_repair_route(inp.violated_invariants),
            reason="critical_invariant_violation",
        )

    if inp.violated_invariants and inp.violation_severity in {"medium", "high"}:
        return InvariantGateOutput(
            output_status="HOLD",
            gate_closed=True,
            execution_authority_granted=False,
            required_repair_route=choose_repair_route(inp.violated_invariants),
            reason="invariant_violation_requires_hold",
        )

    if inp.violated_invariants:
        return InvariantGateOutput(
            output_status="REPAIR",
            gate_closed=True,
            execution_authority_granted=False,
            required_repair_route=choose_repair_route(inp.violated_invariants),
            reason="invariant_violation_requires_repair",
        )

    return InvariantGateOutput(
        output_status="PASS",
        gate_closed=False,
        execution_authority_granted=False,
        required_repair_route="monitor",
        reason="required_invariants_preserved",
    )


def main() -> int:
    sample = InvariantGateInput(
        transformation_axis="qi_mode_shift",
        required_invariants=["I3", "I4", "I7"],
        violated_invariants=["I7"],
        violation_severity="high",
    )
    out = evaluate_gate(sample)
    print(json.dumps(dataclasses.asdict(out), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
