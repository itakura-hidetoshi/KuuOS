#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_cstar_local_net_bridge_v0_30"
READY = "WORLD_CSTAR_LOCAL_NET_BRIDGE_V0_30_READY"
BLOCKED = "WORLD_CSTAR_LOCAL_NET_BRIDGE_V0_30_BLOCKED"
REQUIRED_COMPONENTS = {
    "complex_cstar_completion",
    "faithful_dense_embedding",
    "noncommutativity_preserved",
    "local_star_subalgebras",
    "local_net_isotony",
    "norm_closed_local_net",
    "closed_net_isotony",
    "algebraic_locality",
    "background_star_algebra",
    "action_star_algebra",
}
REQUIRED_BOUNDARY = {
    "source_v0_29_exact": True,
    "world_not_identified_with_cstar_carrier": True,
    "local_net_read_only_analytic_sidecar": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_construct_cstar_completion": True,
    "runtime_cannot_execute_unbounded_operator": True,
    "runtime_cannot_claim_lean_proof": True,
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
    source_v029_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_cstar_local_net_bridge(plan: Mapping[str, Any]) -> Result:
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
    for field in ("world_model_id", "source_v029_sha256", "formal_module_sha256"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "cstar_completion_constructed_by_runtime",
        "unbounded_operator_executed",
        "runtime_proof_claimed",
        "world_updated",
        "external_actuation_performed",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "quarantine_recommended" if blockers else "world_cstar_local_net_bridge_ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v029_sha256": str(plan.get("source_v029_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "cstar_completion_constructed_by_runtime": False,
        "unbounded_operator_executed": False,
        "runtime_proof_claimed": False,
        "world_updated": False,
        "external_actuation_performed": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v029_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
