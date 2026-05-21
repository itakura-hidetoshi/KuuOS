#!/usr/bin/env python3
"""Executable Qi Runtime Binding evaluator v0.1.

This module makes Qi operational for the KuuOS candidate cycle.  It reads a
runtime state dictionary and emits one bounded OS signal:

- QUARANTINE
- BOUNDARY_RECHECK
- HOLD
- REOBSERVE
- LINEAGE_RECHECK
- DELIVERY_RECHECK
- ALLOW_CANDIDATE

The evaluator is deliberately candidate-only.  It never grants truth,
execution, final commitment, memory overwrite, theorem, clinical, or completed
identity authority.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
import json
import sys
from typing import Any, Mapping


class QiSignal(str, Enum):
    ALLOW_CANDIDATE = "ALLOW_CANDIDATE"
    HOLD = "HOLD"
    REOBSERVE = "REOBSERVE"
    LINEAGE_RECHECK = "LINEAGE_RECHECK"
    DELIVERY_RECHECK = "DELIVERY_RECHECK"
    BOUNDARY_RECHECK = "BOUNDARY_RECHECK"
    QUARANTINE = "QUARANTINE"


BOUNDARY_FIELDS = [
    "two_truths_gap",
    "noncollapse_guard",
    "memory_overwrite_blocker",
    "world_identity_blocker",
]
CANDIDATE_MARKER_FIELDS = ["candidate_only", "nonfinal_marker"]
POLICY_FIELDS = [
    "runtime_variation_visible",
    "policy_candidate_receipt",
    "value_witness_receipt",
    "barrier_witness_receipt",
]
LINEAGE_FIELDS = ["receipt_hash", "support_refs", "registry_key"]
DELIVERY_FIELDS = ["view_delivery_receipt", "channel_scope", "acknowledgment_marker"]

FORBIDDEN_AUTHORITY_FIELDS = [
    "truth_commit",
    "execution_commit",
    "memory_overwrite_commit",
    "clinical_commit",
    "theorem_commit",
    "global_truth_object_commit",
    "completed_os_identity_commit",
    "world_identity_commit",
    "silent_pass_commit",
]


@dataclass(frozen=True)
class QiRuntimeReceipt:
    cycle_id: str
    kernel_state: str
    qi_signal: str
    qi_reason: str
    missing_inputs: list[str]
    opened_notices: list[str]
    blocked_boundaries: list[str]
    allowed_projection: list[str]
    grants_execution_authority: bool = False
    grants_truth_authority: bool = False
    grants_final_commitment_authority: bool = False
    grants_memory_overwrite_authority: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _truthy(state: Mapping[str, Any], key: str) -> bool:
    value = state.get(key, False)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "y", "present", "ok", "pass"}
    return bool(value)


def _missing(state: Mapping[str, Any], fields: list[str]) -> list[str]:
    return [field for field in fields if not _truthy(state, field)]


def evaluate_qi_runtime_binding(state: Mapping[str, Any]) -> QiRuntimeReceipt:
    """Evaluate Qi runtime binding for a candidate cycle.

    Ordering is intentional: boundary safety is checked before candidate flow is
    allowed.  Missing policy support asks for re-observation; missing lineage
    support asks for lineage recheck; missing delivery support asks for delivery
    recheck.  A fully visible state emits ALLOW_CANDIDATE, which is still not
    execution/finality authority.
    """
    cycle_id = str(state.get("cycle_id", "unknown-cycle"))
    kernel_state = str(state.get("kernel_state", "candidate"))

    forbidden = [field for field in FORBIDDEN_AUTHORITY_FIELDS if _truthy(state, field)]
    if forbidden:
        return QiRuntimeReceipt(
            cycle_id=cycle_id,
            kernel_state=kernel_state,
            qi_signal=QiSignal.QUARANTINE.value,
            qi_reason="forbidden_authority_projection_present",
            missing_inputs=[],
            opened_notices=["quarantine_notice", "boundary_recheck_request"],
            blocked_boundaries=forbidden,
            allowed_projection=["quarantine_notice", "boundary_recheck_request"],
        )

    missing_boundary = _missing(state, BOUNDARY_FIELDS)
    if missing_boundary:
        return QiRuntimeReceipt(
            cycle_id=cycle_id,
            kernel_state=kernel_state,
            qi_signal=QiSignal.QUARANTINE.value,
            qi_reason="boundary_first_noncollapse_failed",
            missing_inputs=missing_boundary,
            opened_notices=["quarantine_notice", "boundary_recheck_request"],
            blocked_boundaries=missing_boundary,
            allowed_projection=["quarantine_notice", "boundary_recheck_request"],
        )

    missing_markers = _missing(state, CANDIDATE_MARKER_FIELDS)
    if missing_markers:
        return QiRuntimeReceipt(
            cycle_id=cycle_id,
            kernel_state=kernel_state,
            qi_signal=QiSignal.HOLD.value,
            qi_reason="candidate_or_nonfinal_marker_missing",
            missing_inputs=missing_markers,
            opened_notices=["hold_notice", "qi_debt_notice"],
            blocked_boundaries=[],
            allowed_projection=["hold_notice", "qi_debt_notice"],
        )

    missing_policy = _missing(state, POLICY_FIELDS)
    if missing_policy:
        return QiRuntimeReceipt(
            cycle_id=cycle_id,
            kernel_state=kernel_state,
            qi_signal=QiSignal.REOBSERVE.value,
            qi_reason="runtime_policy_flow_support_missing",
            missing_inputs=missing_policy,
            opened_notices=["reobserve_request", "qi_debt_notice"],
            blocked_boundaries=[],
            allowed_projection=["reobserve_request", "qi_debt_notice"],
        )

    missing_lineage = _missing(state, LINEAGE_FIELDS)
    if missing_lineage:
        return QiRuntimeReceipt(
            cycle_id=cycle_id,
            kernel_state=kernel_state,
            qi_signal=QiSignal.LINEAGE_RECHECK.value,
            qi_reason="lineage_flow_support_missing",
            missing_inputs=missing_lineage,
            opened_notices=["lineage_recheck_request", "qi_debt_notice"],
            blocked_boundaries=[],
            allowed_projection=["lineage_recheck_request", "qi_debt_notice"],
        )

    missing_delivery = _missing(state, DELIVERY_FIELDS)
    if missing_delivery:
        return QiRuntimeReceipt(
            cycle_id=cycle_id,
            kernel_state=kernel_state,
            qi_signal=QiSignal.DELIVERY_RECHECK.value,
            qi_reason="projection_delivery_flow_support_missing",
            missing_inputs=missing_delivery,
            opened_notices=["delivery_debt_notice", "qi_debt_notice"],
            blocked_boundaries=[],
            allowed_projection=["delivery_debt_notice", "qi_debt_notice"],
        )

    return QiRuntimeReceipt(
        cycle_id=cycle_id,
        kernel_state=kernel_state,
        qi_signal=QiSignal.ALLOW_CANDIDATE.value,
        qi_reason="all_candidate_flow_inputs_visible_and_nonfinal",
        missing_inputs=[],
        opened_notices=["qi_runtime_binding_receipt"],
        blocked_boundaries=[],
        allowed_projection=["qi_runtime_binding_receipt"],
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: qi_runtime_binding_v0_1.py STATE.json", file=sys.stderr)
        return 2
    path = argv[1]
    with open(path, "r", encoding="utf-8") as f:
        state = json.load(f)
    receipt = evaluate_qi_runtime_binding(state)
    print(json.dumps(receipt.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if receipt.qi_signal != QiSignal.QUARANTINE.value else 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
