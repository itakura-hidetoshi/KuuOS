#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_module_category_nimrep_tube_center_bridge_v0_41"
READY = "WORLD_MODULE_CATEGORY_NIMREP_TUBE_CENTER_BRIDGE_V0_41_READY"
BLOCKED = "WORLD_MODULE_CATEGORY_NIMREP_TUBE_CENTER_BRIDGE_V0_41_BLOCKED"

REQUIRED_COMPONENTS = {
    "finite_module_label_system",
    "fusion_module_action",
    "nimrep_representation",
    "positive_module_dimension",
    "fundamental_nimrep_graph",
    "ocneanu_cell_conjugation",
    "finite_tube_star_algebra",
    "central_idempotent_system",
    "drinfeld_center_simple_system",
    "forgetful_dimension_formula",
    "drinfeld_center_global_dimension_square",
    "analytic_categorical_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_40_exact": True,
    "module_category_existence_external": True,
    "nimrep_completeness_external": True,
    "ocneanu_cell_existence_external": True,
    "ocneanu_cell_unitarity_external": True,
    "ocneanu_cell_flatness_external": True,
    "tube_cstar_realization_external": True,
    "tube_center_classification_external": True,
    "drinfeld_center_equivalence_external": True,
    "morita_invariance_external": True,
    "drinfeld_center_modularity_external": True,
    "world_not_identified_with_module_category": True,
    "world_not_identified_with_nimrep": True,
    "world_not_identified_with_tube_algebra": True,
    "world_not_identified_with_drinfeld_center": True,
    "module_tube_center_read_only_analytic_sidecar": True,
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
    source_v040_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_module_category_nimrep_tube_center_bridge(
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
        "source_v040_sha256",
        "formal_module_sha256",
    ):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "module_category_constructed_by_runtime",
        "ocneanu_cells_solved_by_runtime",
        "tube_algebra_built_by_runtime",
        "drinfeld_center_reconstructed_by_runtime",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "blocked" if blockers else "ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v040_sha256": str(plan.get("source_v040_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "module_category_constructed_by_runtime": False,
        "ocneanu_cells_solved_by_runtime": False,
        "tube_algebra_built_by_runtime": False,
        "drinfeld_center_reconstructed_by_runtime": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v040_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
