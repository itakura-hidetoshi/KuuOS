#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_bimodule_sector_fusion_category_bridge_v0_40"
READY = "WORLD_BIMODULE_SECTOR_FUSION_CATEGORY_BRIDGE_V0_40_READY"
BLOCKED = "WORLD_BIMODULE_SECTOR_FUSION_CATEGORY_BRIDGE_V0_40_BLOCKED"

REQUIRED_COMPONENTS = {
    "finite_simple_sector_system",
    "tensor_unit_and_duality",
    "fusion_multiplicity",
    "fusion_associativity",
    "frobenius_reciprocity",
    "statistical_dimension",
    "fundamental_bimodule_sector",
    "dual_canonical_decomposition",
    "principal_graph_adjacency",
    "qsystem_standard_invariant_connection",
    "analytic_category_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_39_exact": True,
    "finite_index_bimodule_existence_external": True,
    "connes_fusion_external": True,
    "semisimple_sector_decomposition_external": True,
    "rigid_cstar_tensor_category_external": True,
    "principal_graph_completeness_external": True,
    "paragroup_reconstruction_external": True,
    "world_not_identified_with_bimodule": True,
    "world_not_identified_with_sector_category": True,
    "sector_fusion_read_only_analytic_sidecar": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "fail_closed": True,
}


def digest(value: Any) -> str:
    raw = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
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
    source_v039_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_bimodule_sector_fusion_category_bridge(
    plan: Mapping[str, Any],
) -> Result:
    blockers: list[str] = []
    if plan.get("version") != VERSION:
        blockers.append("version_invalid")
    if plan.get("plan_digest") != plan_digest(plan):
        blockers.append("plan_digest_invalid")
    if set(plan.get("components", [])) != REQUIRED_COMPONENTS:
        blockers.append("components_invalid")
    boundary = (
        plan.get("boundary")
        if isinstance(plan.get("boundary"), Mapping)
        else {}
    )
    for field, expected in REQUIRED_BOUNDARY.items():
        if boundary.get(field) is not expected:
            blockers.append(f"boundary_{field}_invalid")
    for field in (
        "world_model_id",
        "source_v039_sha256",
        "formal_module_sha256",
    ):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "bimodules_constructed_by_runtime",
        "connes_fusion_executed_by_runtime",
        "fusion_category_reconstruction_claimed_by_runtime",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "blocked" if blockers else "ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v039_sha256": str(plan.get("source_v039_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "bimodules_constructed_by_runtime": False,
        "connes_fusion_executed_by_runtime": False,
        "fusion_category_reconstruction_claimed_by_runtime": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v039_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
