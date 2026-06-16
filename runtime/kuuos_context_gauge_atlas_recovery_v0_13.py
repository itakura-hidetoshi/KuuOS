from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import decision_digest, read_json
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import plan_digest as local_plan_digest


def load_pending_packets(*, atlas_run_id: str, pending: Mapping[str, Any], paths: Mapping[str, Any], blockers: list[str]):
    decision = read_json(paths["atlas_decision"])
    local_plan = read_json(paths["atlas_child_plan"])
    local_license = read_json(paths["atlas_child_license"])
    if decision.get("atlas_run_id") != atlas_run_id:
        blockers.append("pending_atlas_decision_run_mismatch")
    if decision.get("atlas_decision_digest") != decision_digest(decision):
        blockers.append("pending_atlas_decision_digest_invalid")
    if decision.get("atlas_decision_digest") != pending.get("atlas_decision_digest"):
        blockers.append("pending_atlas_decision_binding_mismatch")
    if local_plan.get("arbitration_plan_digest") != local_plan_digest(local_plan):
        blockers.append("pending_local_plan_digest_invalid")
    if local_plan.get("arbitration_plan_digest") != pending.get("local_plan_digest"):
        blockers.append("pending_local_plan_binding_mismatch")
    if local_license.get("bound_arbitration_plan_digest") != local_plan.get("arbitration_plan_digest"):
        blockers.append("pending_local_license_invalid")
    return decision, local_plan, local_license
