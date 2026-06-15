#!/usr/bin/env python3
from runtime.kuuos_horizon_gauge_arbitration_pending_v0_12 import pending_record
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import append_jsonl


def append_pending(data):
    if data["blockers"] or data["pending"] is not None:
        return data
    values = data["values"]
    append_jsonl(
        data["paths"]["ledger"],
        pending_record(
            packet_id=data["packet_id"],
            run_id=data["run_id"],
            plan=data["plan"],
            source_batch_digest=data["source_batch"],
            previous_horizon_bundle_digest=values["horizon_bundle"].get(
                "horizon_bundle_digest", ""
            ),
            previous_arbitration_state_digest=data["state"].get(
                "arbitration_state_digest", ""
            ),
            previous_arbitration_bundle_digest=data["bundle"].get(
                "arbitration_bundle_digest", ""
            ),
            decision=data["decision"],
            child_plan=data["child_plan"],
            cycle_index=data["cycle_index"],
        ),
    )
    return data
