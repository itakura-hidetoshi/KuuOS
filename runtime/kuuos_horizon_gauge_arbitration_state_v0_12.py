#!/usr/bin/env python3
from __future__ import annotations
import time
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import STATE_VERSION, integer, state_digest

def build_state(*, previous_state: Mapping[str, Any], run_id: str, cycle_index: int, decision: Mapping[str, Any], outcome: Mapping[str, Any], arbitration_bundle: Mapping[str, Any]) -> dict[str, Any]:
    kind = str(outcome.get("commitment_outcome_class", "holding"))
    state = {
        "version": STATE_VERSION,
        "arbitration_run_id": run_id,
        "cycle_index": cycle_index,
        "previous_arbitration_state_digest": previous_state.get("arbitration_state_digest", ""),
        "arbitration_bundle_digest": arbitration_bundle.get("arbitration_bundle_digest", ""),
        "arbitration_decision_digest": decision.get("arbitration_decision_digest", ""),
        "arbitration_outcome_digest": outcome.get("arbitration_outcome_digest", ""),
        "child_horizon_bundle_digest": outcome.get("child_horizon_bundle_digest", ""),
        "child_horizon_outcome_digest": outcome.get("child_horizon_outcome_digest", ""),
        "child_effect_receipt_digest": outcome.get("child_effect_receipt_digest", ""),
        "last_arbitration_class": outcome.get("arbitration_class", ""),
        "last_commitment_outcome_class": kind,
        "total_cycles": integer(previous_state.get("total_cycles"), 0) + 1,
        "total_aligned_cycles": integer(previous_state.get("total_aligned_cycles"), 0) + (outcome.get("arbitration_class") == "aligned_transport"),
        "total_plural_cycles": integer(previous_state.get("total_plural_cycles"), 0) + (outcome.get("arbitration_class") == "plural_transport"),
        f"total_{kind}_cycles": integer(previous_state.get(f"total_{kind}_cycles"), 0) + 1,
        "multiple_child_cycle_count": 0,
        "winner_take_all_collapse_count": 0,
        "hard_gate_bypass_count": 0,
        "epoch": int(time.time()),
    }
    state["arbitration_state_digest"] = state_digest(state)
    return state
