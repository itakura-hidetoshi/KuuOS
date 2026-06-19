#!/usr/bin/env python3
from __future__ import annotations

from dataclasses import asdict, dataclass
import hashlib
import json
from typing import Any, Mapping

VERSION = "world_petz_recovery_sufficiency_bridge_v0_35"
READY = "WORLD_PETZ_RECOVERY_SUFFICIENCY_BRIDGE_V0_35_READY"
BLOCKED = "WORLD_PETZ_RECOVERY_SUFFICIENCY_BRIDGE_V0_35_BLOCKED"

REQUIRED_COMPONENTS = {
    "coarse_channel",
    "petz_recovery",
    "state_pair_recovery",
    "range_projection",
    "recovered_idempotence",
    "entropy_equality",
    "analytic_receipts",
}

REQUIRED_BOUNDARY = {
    "source_v0_34_exact": True,
    "channel_proof_external": True,
    "recovery_proof_external": True,
    "equality_theorem_external": True,
    "world_not_reduced_to_recovery_carrier": True,
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
    source_v034_sha256: str
    formal_module_sha256: str
    bridge_state_digest: str
    blockers: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def build_world_petz_recovery_sufficiency_bridge(plan: Mapping[str, Any]) -> Result:
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
    for field in ("world_model_id", "source_v034_sha256", "formal_module_sha256"):
        if not str(plan.get(field, "")):
            blockers.append(f"{field}_missing")
    for field in (
        "channel_constructed_by_runtime",
        "recovery_constructed_by_runtime",
        "equality_theorem_claimed_by_runtime",
        "world_updated",
    ):
        if plan.get(field) is not False:
            blockers.append(f"{field}_forbidden")
    decision = "blocked" if blockers else "ready"
    state = {
        "version": VERSION,
        "decision": decision,
        "world_model_id": str(plan.get("world_model_id", "")),
        "source_v034_sha256": str(plan.get("source_v034_sha256", "")),
        "formal_module_sha256": str(plan.get("formal_module_sha256", "")),
        "components": sorted(REQUIRED_COMPONENTS),
        "boundary": REQUIRED_BOUNDARY,
        "channel_constructed_by_runtime": False,
        "recovery_constructed_by_runtime": False,
        "equality_theorem_claimed_by_runtime": False,
        "world_updated": False,
    }
    return Result(
        VERSION,
        BLOCKED if blockers else READY,
        decision,
        state["world_model_id"],
        state["source_v034_sha256"],
        state["formal_module_sha256"],
        digest(state) if not blockers else "",
        blockers,
    )
