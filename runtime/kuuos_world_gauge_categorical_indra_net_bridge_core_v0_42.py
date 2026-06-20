#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_gauge_categorical_indra_net_bridge_v0_42"
READY = "WORLD_GAUGE_CATEGORICAL_INDRA_NET_BRIDGE_V0_42_READY"
BLOCKED = "WORLD_GAUGE_CATEGORICAL_INDRA_NET_BRIDGE_V0_42_BLOCKED"

REQUIRED_COMPONENTS = {
    "finite_world_patch_atlas",
    "overlap_relation",
    "operator_algebra_transport",
    "jones_tower_transport",
    "qsystem_transport",
    "sector_fusion_transport",
    "module_nimrep_transport",
    "tube_algebra_transport",
    "drinfeld_center_transport",
    "higher_coherence_two_cells",
    "finite_holonomy_curvature",
    "branch_preserving_transport",
    "history_dependent_nonmarkov_phase",
    "analytic_higher_gauge_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_41_exact": True,
    "normal_star_isomorphism_external": True,
    "pseudofunctor_realization_external": True,
    "stack_descent_external": True,
    "ocneanu_cell_holonomy_external": True,
    "continuum_higher_gauge_field_external": True,
    "tqft_cft_reconstruction_external": True,
    "continuum_nonmarkov_connection_external": True,
    "world_not_identified_with_indra_net": True,
    "world_not_identified_with_gauge_connection": True,
    "world_not_identified_with_holonomy": True,
    "observational_gauge_equivalence_not_world_identity": True,
    "indra_net_read_only_analytic_sidecar": True,
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
    source_v041_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_gauge_categorical_indra_net_bridge(
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
        "source_v041_sha256",
        "formal_module_sha256",
    ):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "indra_gauge_connection_constructed_by_runtime",
        "physical_holonomy_computed_by_runtime",
        "ocneanu_flatness_solved_by_runtime",
        "bulk_topological_theory_reconstructed_by_runtime",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "blocked" if blockers else "ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v041_sha256": str(plan.get("source_v041_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "indra_gauge_connection_constructed_by_runtime": False,
        "physical_holonomy_computed_by_runtime": False,
        "ocneanu_flatness_solved_by_runtime": False,
        "bulk_topological_theory_reconstructed_by_runtime": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v041_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
