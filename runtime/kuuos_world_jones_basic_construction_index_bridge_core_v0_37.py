#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_jones_basic_construction_index_bridge_v0_37"
READY = "WORLD_JONES_BASIC_CONSTRUCTION_INDEX_BRIDGE_V0_37_READY"
BLOCKED = "WORLD_JONES_BASIC_CONSTRUCTION_INDEX_BRIDGE_V0_37_BLOCKED"

REQUIRED_COMPONENTS = {
    "jones_projection",
    "projection_compression_identity",
    "basic_construction",
    "relative_commutant",
    "finite_quasi_basis",
    "left_reconstruction",
    "right_reconstruction",
    "central_index_element",
    "scalar_jones_index",
    "analytic_index_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_36_exact": True,
    "jones_projection_analytic_construction_external": True,
    "von_neumann_closure_external": True,
    "canonical_trace_external": True,
    "finite_index_theorem_external": True,
    "world_not_identified_with_basic_construction": True,
    "multi_world_noncollapse_preserved": True,
    "two_truths_gap_preserved": True,
    "runtime_cannot_update_world": True,
    "fail_closed": True,
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
    source_v036_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_jones_basic_construction_index_bridge(plan: Mapping[str, Any]) -> Result:
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
    for field in ("world_model_id", "source_v036_sha256", "formal_module_sha256"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "jones_projection_constructed_by_runtime",
        "basic_construction_executed_by_runtime",
        "finite_index_theorem_claimed_by_runtime",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "blocked" if blockers else "ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v036_sha256": str(plan.get("source_v036_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "jones_projection_constructed_by_runtime": False,
        "basic_construction_executed_by_runtime": False,
        "finite_index_theorem_claimed_by_runtime": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v036_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
