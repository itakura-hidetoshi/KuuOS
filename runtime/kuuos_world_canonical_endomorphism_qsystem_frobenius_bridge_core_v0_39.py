#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_canonical_endomorphism_qsystem_frobenius_bridge_v0_39"
READY = "WORLD_CANONICAL_ENDOMORPHISM_QSYSTEM_FROBENIUS_BRIDGE_V0_39_READY"
BLOCKED = "WORLD_CANONICAL_ENDOMORPHISM_QSYSTEM_FROBENIUS_BRIDGE_V0_39_BLOCKED"

REQUIRED_COMPONENTS = {
    "typed_inclusion_conjugate_homomorphisms",
    "canonical_endomorphism",
    "dual_canonical_endomorphism",
    "q_system_unit",
    "q_system_multiplication",
    "associativity_and_unit_laws",
    "frobenius_law",
    "specialness_and_star_compatibility",
    "jones_projection_compatibility",
    "standard_invariant_connection",
    "analytic_reconstruction_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_38_exact": True,
    "conjugate_homomorphism_existence_external": True,
    "finite_index_canonical_endomorphism_external": True,
    "standard_conjugate_solution_external": True,
    "q_system_subfactor_equivalence_external": True,
    "categorical_reconstruction_external": True,
    "world_not_identified_with_canonical_endomorphism": True,
    "world_not_identified_with_q_system": True,
    "q_system_read_only_analytic_sidecar": True,
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
    source_v038_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_canonical_endomorphism_qsystem_frobenius_bridge(
    plan: Mapping[str, Any],
) -> Result:
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
    for field in ("world_model_id", "source_v038_sha256", "formal_module_sha256"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "canonical_endomorphism_constructed_by_runtime",
        "q_system_executed_by_runtime",
        "subfactor_reconstruction_claimed_by_runtime",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "blocked" if blockers else "ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v038_sha256": str(plan.get("source_v038_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "canonical_endomorphism_constructed_by_runtime": False,
        "q_system_executed_by_runtime": False,
        "subfactor_reconstruction_claimed_by_runtime": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v038_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
