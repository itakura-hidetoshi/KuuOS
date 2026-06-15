#!/usr/bin/env python3
from typing import Any, Mapping
from runtime.kuuos_delayed_credit_multihorizon_types_v0_11 import plan_digest as child_plan_digest
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import DECISION_VERSION, decision_digest, read_json

def load_recovery_packets(*, run_id: str, pending: Mapping[str, Any], paths: Mapping[str, Any], blockers: list[str]):
    decision = read_json(paths["decision"])
    child_plan = read_json(paths["child_plan"])
    child_license = read_json(paths["child_license"])
    if decision.get("version") != DECISION_VERSION:
        blockers.append("pending_arbitration_decision_version_invalid")
    if decision.get("arbitration_run_id") != run_id:
        blockers.append("pending_arbitration_decision_run_mismatch")
    if decision.get("arbitration_decision_digest") != decision_digest(decision):
        blockers.append("pending_arbitration_decision_digest_invalid")
    if decision.get("arbitration_decision_digest") != pending.get("arbitration_decision_digest"):
        blockers.append("pending_arbitration_decision_binding_mismatch")
    if child_plan.get("horizon_plan_digest") != child_plan_digest(child_plan):
        blockers.append("pending_child_horizon_plan_digest_invalid")
    if child_plan.get("horizon_plan_digest") != pending.get("child_horizon_plan_digest"):
        blockers.append("pending_child_horizon_plan_binding_mismatch")
    if child_license.get("bound_horizon_plan_digest") != child_plan.get("horizon_plan_digest"):
        blockers.append("pending_child_horizon_license_invalid")
    return decision, child_plan, child_license
