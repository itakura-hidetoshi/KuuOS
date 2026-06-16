from __future__ import annotations
import time
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import STATE_VERSION, integer, state_digest


def build_state(*, previous: Mapping[str, Any], atlas_run_id: str, cycle_index: int, decision: Mapping[str, Any], outcome: Mapping[str, Any], atlas_bundle: Mapping[str, Any]) -> dict[str, Any]:
    atlas_class = str(decision.get("atlas_class", "isolated_chart"))
    packet = {
        "version": STATE_VERSION,
        "atlas_run_id": atlas_run_id,
        "cycle_index": cycle_index,
        "previous_atlas_state_digest": previous.get("atlas_state_digest", ""),
        "atlas_bundle_digest": atlas_bundle.get("atlas_bundle_digest", ""),
        "atlas_decision_digest": decision.get("atlas_decision_digest", ""),
        "atlas_outcome_digest": outcome.get("atlas_outcome_digest", ""),
        "child_arbitration_bundle_digest": outcome.get("child_arbitration_bundle_digest", ""),
        "child_arbitration_outcome_digest": outcome.get("child_arbitration_outcome_digest", ""),
        "child_effect_receipt_digest": outcome.get("child_effect_receipt_digest", ""),
        "last_atlas_class": atlas_class,
        "last_target_context_key": decision.get("target_context_key", ""),
        "total_cycles": integer(previous.get("total_cycles"), 0) + 1,
        "total_transitions": integer(previous.get("total_transitions"), 0) + integer(decision.get("compatible_chart_count"), 0),
        f"total_{atlas_class}_cycles": integer(previous.get(f"total_{atlas_class}_cycles"), 0) + 1,
        "multiple_local_cycle_count": 0,
        "chart_locality_bypass_count": 0,
        "cocycle_veto_count": 0,
        "epoch": int(time.time()),
    }
    packet["atlas_state_digest"] = state_digest(packet)
    return packet
