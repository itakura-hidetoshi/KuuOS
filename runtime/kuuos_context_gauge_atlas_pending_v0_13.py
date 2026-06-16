from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import LEDGER_VERSION, sha, without


def pending_record(*, packet_id: str, atlas_run_id: str, plan: Mapping[str, Any], source_batch_digest: str, previous_state_digest: str, previous_bundle_digest: str, decision: Mapping[str, Any], local_plan: Mapping[str, Any], cycle_index: int) -> dict[str, Any]:
    packet = {
        "version": LEDGER_VERSION,
        "phase": "pending",
        "packet_id": packet_id,
        "atlas_run_id": atlas_run_id,
        "atlas_plan_digest": plan.get("atlas_plan_digest", ""),
        "source_batch_digest": source_batch_digest,
        "previous_atlas_state_digest": previous_state_digest,
        "previous_atlas_bundle_digest": previous_bundle_digest,
        "atlas_decision_digest": decision.get("atlas_decision_digest", ""),
        "local_plan_digest": local_plan.get("arbitration_plan_digest", ""),
        "cycle_index": cycle_index,
        "pending_digest": "",
    }
    packet["pending_digest"] = sha(without(packet, "pending_digest"))
    return packet
