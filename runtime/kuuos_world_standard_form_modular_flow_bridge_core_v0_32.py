#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_standard_form_modular_flow_bridge_v0_32"
READY = "WORLD_STANDARD_FORM_MODULAR_FLOW_BRIDGE_V0_32_READY"
BLOCKED = "WORLD_STANDARD_FORM_MODULAR_FLOW_BRIDGE_V0_32_BLOCKED"

REQUIRED_COMPONENTS = {
    "complex_hilbert_standard_form_carrier",
    "faithful_star_representation",
    "cyclic_separating_vector_receipt",
    "natural_cone",
    "modular_conjugation",
    "commutant_transport",
    "one_parameter_modular_flow",
    "modular_flow_inverse_law",
    "local_weak_closure_invariance",
    "modular_unitary_implementation",
    "tomita_polar_decomposition_receipt",
    "positive_self_adjoint_modular_operator_receipt",
}

REQUIRED_BOUNDARY = {
    "source_v0_31_exact": True,
    "tomita_operator_external": True,
    "polar_decomposition_external": True,
    "modular_operator_execution_disabled": True,
    "standard_form_theorem_external": True,
    "world_not_identified_with_standard_form_carrier": True,
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
    source_v031_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_standard_form_modular_flow_bridge(plan: Mapping[str, Any]) -> Result:
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
    for field in ("world_model_id", "source_v031_sha256", "formal_module_sha256"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "tomita_operator_constructed_by_runtime",
        "modular_operator_executed",
        "runtime_standard_form_theorem_claimed",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "quarantine_recommended" if blockers else "world_standard_form_modular_flow_bridge_ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v031_sha256": str(plan.get("source_v031_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "tomita_operator_constructed_by_runtime": False,
        "modular_operator_executed": False,
        "runtime_standard_form_theorem_claimed": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v031_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
