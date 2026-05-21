#!/usr/bin/env python3
"""Qi Total Field normalizer v0.1.

Unifies multiple Qi inputs into the OS-cycle state consumed by Qi Runtime
Binding / Qi Cycle Runner.

This is not a taxonomy layer. It actively normalizes physical/process/runtime/
lineage/boundary/delivery Qi evidence into candidate-flow inputs, then calls the
Qi cycle runner to determine the next OS queue.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
import json
import sys
from typing import Any, Mapping

try:
    from runtime.qi_cycle_runner_v0_1 import QiCycleDecision, run_qi_cycle
    from runtime.qi_process_tensor_v0_1 import enrich_state_with_qi_process_tensor
except ModuleNotFoundError:  # direct script execution from runtime/
    from qi_cycle_runner_v0_1 import QiCycleDecision, run_qi_cycle
    from qi_process_tensor_v0_1 import enrich_state_with_qi_process_tensor


AUTHORITY_FALSE_FIELDS = [
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
BOUNDARY_FIELDS = [
    "two_truths_gap",
    "noncollapse_guard",
    "memory_overwrite_blocker",
    "world_identity_blocker",
]


@dataclass(frozen=True)
class QiTotalFieldResult:
    cycle_id: str
    normalized_qi_state: dict[str, Any]
    qi_cycle_decision: dict[str, Any]
    qi_total_reason: str
    source_support: dict[str, list[str]]
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


def _supporting_fields(state: Mapping[str, Any], fields: list[str]) -> list[str]:
    return [field for field in fields if _truthy(state, field)]


def normalize_qi_total_field(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Normalize total Qi evidence into Qi Runtime Binding input state.

    Boundary fields are copied directly and never repaired by other Qi support.
    Physical and process Qi can support runtime/value/policy fields only when
    candidate/nonfinal markers and boundary visibility are present.
    """
    raw = enrich_state_with_qi_process_tensor(raw)
    normalized: dict[str, Any] = {
        "cycle_id": raw.get("cycle_id", "unknown-cycle"),
        "kernel_state": raw.get("kernel_state", "candidate"),
        "candidate_only": _truthy(raw, "candidate_only"),
        "nonfinal_marker": _truthy(raw, "nonfinal_marker"),
    }

    # Boundary-first: copy as-is. No support source may override failure.
    for field in BOUNDARY_FIELDS:
        normalized[field] = _truthy(raw, field)

    boundary_ok = all(normalized[field] for field in BOUNDARY_FIELDS)
    candidate_surface_ok = bool(normalized["candidate_only"] and normalized["nonfinal_marker"] and normalized["two_truths_gap"])

    physical_support = bool(
        _truthy(raw, "physical_process_visible")
        or _truthy(raw, "thermodynamic_activity_visible")
        or _truthy(raw, "path_integral_weight_visible")
        or _truthy(raw, "recovery_witness_visible")
        or _truthy(raw, "nonmarkov_memory_visible")
    )
    process_support = bool(
        _truthy(raw, "process_tensor_visible")
        or _truthy(raw, "transition_continuity_visible")
        or _truthy(raw, "memory_continuity_visible")
    )

    normalized["runtime_variation_visible"] = bool(
        _truthy(raw, "runtime_variation_visible")
        or (candidate_surface_ok and boundary_ok and (physical_support or process_support))
    )
    normalized["policy_candidate_receipt"] = bool(
        _truthy(raw, "policy_candidate_receipt")
        or (candidate_surface_ok and boundary_ok and process_support)
    )
    normalized["value_witness_receipt"] = bool(
        _truthy(raw, "value_witness_receipt")
        or (candidate_surface_ok and boundary_ok and physical_support)
    )
    normalized["barrier_witness_receipt"] = bool(
        _truthy(raw, "barrier_witness_receipt")
        or (boundary_ok and _truthy(raw, "barrier_witness_visible"))
    )

    normalized["receipt_hash"] = _truthy(raw, "receipt_hash")
    normalized["support_refs"] = _truthy(raw, "support_refs")
    normalized["registry_key"] = _truthy(raw, "registry_key")

    normalized["view_delivery_receipt"] = _truthy(raw, "view_delivery_receipt")
    normalized["channel_scope"] = _truthy(raw, "channel_scope")
    normalized["acknowledgment_marker"] = _truthy(raw, "acknowledgment_marker")

    # Preserve explicit forbidden authority projections as true if present so
    # Qi Runtime Binding can quarantine them.
    for field in AUTHORITY_FALSE_FIELDS:
        normalized[field] = _truthy(raw, field)

    return normalized


def evaluate_qi_total_field(raw: Mapping[str, Any]) -> QiTotalFieldResult:
    raw = enrich_state_with_qi_process_tensor(raw)
    normalized = normalize_qi_total_field(raw)
    decision: QiCycleDecision = run_qi_cycle(normalized)
    support = {
        "physical_qi": _supporting_fields(raw, [
            "physical_process_visible",
            "thermodynamic_activity_visible",
            "path_integral_weight_visible",
            "recovery_witness_visible",
            "nonmarkov_memory_visible",
        ]),
        "process_qi": _supporting_fields(raw, [
            "process_tensor_visible",
            "transition_continuity_visible",
            "memory_continuity_visible",
            "nonmarkov_memory_visible",
        ]),
        "runtime_qi": _supporting_fields(raw, [
            "runtime_variation_visible",
            "policy_candidate_receipt",
            "value_witness_receipt",
            "barrier_witness_receipt",
            "barrier_witness_visible",
        ]),
        "lineage_qi": _supporting_fields(raw, ["receipt_hash", "support_refs", "registry_key", "review_status_visible"]),
        "boundary_qi": _supporting_fields(raw, BOUNDARY_FIELDS),
        "delivery_qi": _supporting_fields(raw, ["view_delivery_receipt", "channel_scope", "acknowledgment_marker", "nonfinal_marker"]),
    }
    return QiTotalFieldResult(
        cycle_id=str(normalized.get("cycle_id", "unknown-cycle")),
        normalized_qi_state=normalized,
        qi_cycle_decision=decision.to_dict(),
        qi_total_reason="normalized_total_qi_field_with_process_tensor_then_ran_qi_cycle",
        source_support=support,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: qi_total_field_v0_1.py RAW_QI_STATE.json", file=sys.stderr)
        return 2
    with open(argv[1], "r", encoding="utf-8") as f:
        raw = json.load(f)
    result = evaluate_qi_total_field(raw)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2, sort_keys=True))
    signal = result.qi_cycle_decision.get("qi_signal")
    return 0 if signal != "QUARANTINE" else 3


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
