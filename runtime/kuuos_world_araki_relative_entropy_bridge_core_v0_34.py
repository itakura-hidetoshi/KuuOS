#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_araki_relative_entropy_bridge_v0_34"
READY = "WORLD_ARAKI_RELATIVE_ENTROPY_BRIDGE_V0_34_READY"
BLOCKED = "WORLD_ARAKI_RELATIVE_ENTROPY_BRIDGE_V0_34_BLOCKED"

REQUIRED_COMPONENTS = {
    "third_normalized_state",
    "extended_nonnegative_relative_entropy",
    "local_relative_entropy",
    "global_relative_entropy",
    "local_data_processing",
    "self_relative_entropy_zero",
    "three_state_connes_chain_rule",
    "chain_rule_adjoint_reversal",
    "pairwise_cocycle_unitarity",
    "araki_formula_receipt",
    "relative_modular_log_domain_receipt",
    "lower_semicontinuity_receipt",
    "normal_ucp_data_processing_receipt",
    "entropy_zero_faithfulness_receipt",
    "petz_equality_recovery_receipt",
}

REQUIRED_BOUNDARY = {
    "source_v0_33_exact": True,
    "relative_modular_log_external": True,
    "araki_entropy_not_computed_by_runtime": True,
    "normal_ucp_theorem_external": True,
    "petz_recovery_external": True,
    "world_not_identified_with_entropy_carrier": True,
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
    source_v033_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_araki_relative_entropy_bridge(plan: Mapping[str, Any]) -> Result:
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
    for field in ("world_model_id", "source_v033_sha256", "formal_module_sha256"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "relative_modular_log_constructed_by_runtime",
        "araki_entropy_computed_by_runtime",
        "runtime_ucp_theorem_claimed",
        "petz_recovery_constructed_by_runtime",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "quarantine_recommended" if blockers else "world_araki_relative_entropy_bridge_ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v033_sha256": str(plan.get("source_v033_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "relative_modular_log_constructed_by_runtime": False,
        "araki_entropy_computed_by_runtime": False,
        "runtime_ucp_theorem_claimed": False,
        "petz_recovery_constructed_by_runtime": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v033_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
