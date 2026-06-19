#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_noncommutative_operator_algebra_module_v0_29"
READY = "WORLD_NONCOMMUTATIVE_OPERATOR_ALGEBRA_MODULE_V0_29_READY"
BLOCKED = "WORLD_NONCOMMUTATIVE_OPERATOR_ALGEBRA_MODULE_V0_29_BLOCKED"
REQUIRED_COMPONENTS = {
    "global_faithful_operator_algebra",
    "nontrivial_commutator_submodule",
    "nontrivial_represented_commutator_submodule",
    "local_observable_algebras",
    "relation_bimodules",
    "background_algebra",
    "action_algebra",
}
REQUIRED_BOUNDARY = {
    "world_not_identified_with_operator_carrier": True,
    "relation_not_reduced_to_object_attribute": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_execute_unbounded_operator": True,
    "runtime_cannot_claim_mathematical_proof": True,
    "runtime_cannot_update_world": True,
    "recommendation_only": True,
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
    source_v028_sha256: str
    formal_module_sha256: str
    module_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_noncommutative_operator_algebra_module(plan: Mapping[str, Any]) -> Result:
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
    for field in ("world_model_id", "source_v028_sha256", "formal_module_sha256"):
        value = str(plan.get(field, ""))
        if not value:
            blockers.append(f"{field}_missing")
    if plan.get("operator_executed") is not False:
        blockers.append("operator_execution_forbidden")
    if plan.get("world_updated") is not False:
        blockers.append("world_update_forbidden")
    if plan.get("runtime_proof_claimed") is not False:
        blockers.append("runtime_proof_claim_forbidden")
    decision = "quarantine_recommended" if blockers else "world_noncommutative_operator_algebra_module_ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v028_sha256": str(plan.get("source_v028_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "operator_executed": False,
        "world_updated": False,
        "runtime_proof_claimed": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v028_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
