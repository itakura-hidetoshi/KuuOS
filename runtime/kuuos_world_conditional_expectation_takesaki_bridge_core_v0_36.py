#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_conditional_expectation_takesaki_bridge_v0_36"
READY = "WORLD_CONDITIONAL_EXPECTATION_TAKESAKI_BRIDGE_V0_36_READY"
BLOCKED = "WORLD_CONDITIONAL_EXPECTATION_TAKESAKI_BRIDGE_V0_36_BLOCKED"

REQUIRED_COMPONENTS = {
    "sufficient_subalgebra",
    "conditional_expectation",
    "range_containment",
    "subalgebra_fixation",
    "idempotence",
    "fixed_point_characterization",
    "two_sided_bimodule_law",
    "state_pair_preservation",
    "petz_recovered_channel_compatibility",
    "modular_invariance",
    "takesaki_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_35_exact": True,
    "normal_ucp_expectation_external": True,
    "weak_closedness_external": True,
    "takesaki_equivalence_external": True,
    "expectation_uniqueness_external": True,
    "world_not_identified_with_sufficient_subalgebra": True,
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
    source_v035_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_conditional_expectation_takesaki_bridge(plan: Mapping[str, Any]) -> Result:
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
    for field in ("world_model_id", "source_v035_sha256", "formal_module_sha256"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "conditional_expectation_constructed_by_runtime",
        "takesaki_theorem_claimed_by_runtime",
        "sufficient_subalgebra_theorem_claimed_by_runtime",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "blocked" if blockers else "ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v035_sha256": str(plan.get("source_v035_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "conditional_expectation_constructed_by_runtime": False,
        "takesaki_theorem_claimed_by_runtime": False,
        "sufficient_subalgebra_theorem_claimed_by_runtime": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v035_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
