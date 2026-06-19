#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_von_neumann_bicommutant_bridge_v0_31"
READY = "WORLD_VON_NEUMANN_BICOMMUTANT_BRIDGE_V0_31_READY"
BLOCKED = "WORLD_VON_NEUMANN_BICOMMUTANT_BRIDGE_V0_31_BLOCKED"

REQUIRED_COMPONENTS = {
    "algebraic_commutant",
    "algebraic_bicommutant",
    "source_subset_bicommutant",
    "commutant_antitone",
    "bicommutant_monotone",
    "triple_commutant_reduction",
    "bicommutant_idempotence",
    "local_bicommutant_isotony",
    "spacelike_bicommutant_locality",
    "external_weak_closure_receipt",
}

REQUIRED_BOUNDARY = {
    "source_v0_30_exact": True,
    "weak_operator_topology_external": True,
    "weak_closure_not_constructed_by_runtime": True,
    "bicommutant_theorem_not_claimed_by_runtime": True,
    "world_not_identified_with_von_neumann_carrier": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_execute_unbounded_operator": True,
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
    source_v030_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_von_neumann_bicommutant_bridge(plan: Mapping[str, Any]) -> Result:
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
    for field in ("world_model_id", "source_v030_sha256", "formal_module_sha256"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    forbidden = (
        "weak_operator_topology_modeled_by_runtime",
        "weak_closure_constructed_by_runtime",
        "runtime_bicommutant_theorem_claimed",
        "unbounded_operator_executed",
        "world_updated",
    )
    for field in forbidden:
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "quarantine_recommended" if blockers else "world_von_neumann_bicommutant_bridge_ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v030_sha256": str(plan.get("source_v030_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "weak_operator_topology_modeled_by_runtime": False,
        "weak_closure_constructed_by_runtime": False,
        "runtime_bicommutant_theorem_claimed": False,
        "unbounded_operator_executed": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v030_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
