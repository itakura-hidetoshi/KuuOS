#!/usr/bin/env python3
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import plan_digest
from runtime.kuuos_horizon_gauge_arbitration_validation_v0_12 import validate_inputs


def apply_digest_guards(data):
    blockers = data["blockers"]
    pending = data["pending"]
    plan = data["plan"]
    if data["replay"] is not None or blockers:
        return data
    if pending is None:
        validate_inputs(
            root_packet=data["root_packet"],
            registry=data["registry"],
            sources=data["sources"],
            upstream=data["upstream"],
            arbitration_state=data["state"],
            arbitration_bundle=data["bundle"],
            plan=plan,
            license_packet=data["license"],
            source_batch_digest=data["source_batch"],
            blockers=blockers,
        )
        return data
    if plan.get("arbitration_plan_digest") != plan_digest(plan):
        blockers.append("arbitration_plan_digest_invalid")
    if pending.get("arbitration_plan_digest") != plan.get("arbitration_plan_digest"):
        blockers.append("pending_arbitration_plan_digest_mismatch")
    if pending.get("source_batch_digest") != data["source_batch"]:
        blockers.append("pending_source_batch_digest_mismatch")
    if pending.get("previous_arbitration_bundle_digest") != plan.get(
        "expected_previous_arbitration_bundle_digest"
    ):
        blockers.append("pending_arbitration_bundle_digest_mismatch")
    return data
