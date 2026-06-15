#!/usr/bin/env python3
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import LEDGER_VERSION, sha, without

def pending_record(*, packet_id: str, run_id: str, plan: Mapping[str, Any], source_batch_digest: str, previous_horizon_bundle_digest: str, previous_arbitration_state_digest: str, previous_arbitration_bundle_digest: str, decision: Mapping[str, Any], child_plan: Mapping[str, Any], cycle_index: int) -> dict[str, Any]:
    row = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "packet_id": packet_id,
        "arbitration_run_id": run_id,
        "arbitration_plan_digest": plan.get("arbitration_plan_digest", ""),
        "source_batch_digest": source_batch_digest,
        "previous_horizon_bundle_digest": previous_horizon_bundle_digest,
        "previous_arbitration_state_digest": previous_arbitration_state_digest,
        "previous_arbitration_bundle_digest": previous_arbitration_bundle_digest,
        "arbitration_decision_digest": decision.get("arbitration_decision_digest", ""),
        "child_horizon_plan_digest": child_plan.get("horizon_plan_digest", ""),
        "cycle_index": cycle_index,
        "pending_digest": "",
    }
    row["pending_digest"] = sha(without(row, "pending_digest"))
    return row
