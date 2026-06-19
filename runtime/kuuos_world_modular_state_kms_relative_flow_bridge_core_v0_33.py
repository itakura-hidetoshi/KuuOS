#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_modular_state_kms_relative_flow_bridge_v0_33"
READY = "WORLD_MODULAR_STATE_KMS_RELATIVE_FLOW_BRIDGE_V0_33_READY"
BLOCKED = "WORLD_MODULAR_STATE_KMS_RELATIVE_FLOW_BRIDGE_V0_33_BLOCKED"

REQUIRED_COMPONENTS = {
    "normalized_reference_state",
    "normalized_comparison_state",
    "positive_normal_faithful_state_receipts",
    "positive_inverse_temperature",
    "kms_strip_continuation",
    "kms_real_boundary",
    "kms_imaginary_boundary",
    "reference_modular_stationarity",
    "relative_modular_flow",
    "relative_flow_inverse_law",
    "connes_cocycle",
    "connes_cocycle_unitarity",
    "relative_flow_cocycle_implementation",
    "relative_weak_closure_invariance",
    "relative_tomita_receipts",
    "connes_radon_nikodym_receipt",
}

REQUIRED_BOUNDARY = {
    "source_v0_32_exact": True,
    "kms_analytic_continuation_external": True,
    "relative_tomita_operator_external": True,
    "relative_modular_operator_execution_disabled": True,
    "connes_radon_nikodym_theorem_external": True,
    "world_not_identified_with_modular_state_carrier": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "recommendation_only": True,
    "fail_closed_on_integrity_loss": True,
}


def digest(value: Any) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(raw).hexdigest()


def plan_digest(plan: Mapping[str, Any]) -> str:
    value = dict(plan)
    value.pop("plan_digest", None)
    return digest(value)


@dataclass(frozen=True)
class Result:
    version: str
    status: str
    decision: str
    world_model_id: str
    source_v032_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_modular_state_kms_relative_flow_bridge(plan: Mapping[str, Any]) -> Result:
    blockers: list[str] = []
    if plan.get("version") != VERSION:
        blockers.append("version_invalid")
    if plan.get("plan_digest") != plan_digest(plan):
        blockers.append("plan_digest_invalid")
    if set(plan.get("components", [])) != REQUIRED_COMPONENTS:
        blockers.append("components_invalid")
    boundary = plan.get("boundary") if isinstance(plan.get("boundary"), Mapping) else {}
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")
    for field in ("world_model_id", "source_v032_sha256", "formal_module_sha256"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "kms_continuation_constructed_by_runtime",
        "relative_tomita_constructed_by_runtime",
        "relative_modular_operator_executed",
        "runtime_connes_theorem_claimed",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "quarantine_recommended" if blockers else "world_modular_state_kms_relative_flow_bridge_ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v032_sha256": str(plan.get("source_v032_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "kms_continuation_constructed_by_runtime": False,
        "relative_tomita_constructed_by_runtime": False,
        "relative_modular_operator_executed": False,
        "runtime_connes_theorem_claimed": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v032_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
