#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import LEDGER_VERSION, sha, without

def committed_record(*, packet_id: str, run_id: str, plan: Mapping[str, Any], cycle_index: int, decision: Mapping[str, Any], outcome: Mapping[str, Any], arbitration_bundle: Mapping[str, Any], child_result: Mapping[str, Any], state: Mapping[str, Any]) -> dict[str, Any]:
    row = {
        "version": LEDGER_VERSION,
        "phase": "committed",
        "packet_id": packet_id,
        "arbitration_run_id": run_id,
        "arbitration_plan_digest": plan.get("arbitration_plan_digest", ""),
        "cycle_index": cycle_index,
        "context_key": outcome.get("context_key", ""),
        "arbitration_class": outcome.get("arbitration_class", ""),
        "commitment_outcome_class": outcome.get("commitment_outcome_class", ""),
        "consensus_mode": outcome.get("consensus_mode", ""),
        "short_dominant_mode": decision.get("short_dominant_mode", ""),
        "medium_dominant_mode": decision.get("medium_dominant_mode", ""),
        "long_dominant_mode": decision.get("long_dominant_mode", ""),
        "short_medium_residual": decision.get("short_medium_residual", 0.0),
        "medium_long_residual": decision.get("medium_long_residual", 0.0),
        "short_long_residual": decision.get("short_long_residual", 0.0),
        "arbitration_curvature": outcome.get("arbitration_curvature", 0.0),
        "transported_short_weight": outcome.get("transported_short_weight", 0.0),
        "transported_medium_weight": outcome.get("transported_medium_weight", 0.0),
        "transported_long_weight": outcome.get("transported_long_weight", 0.0),
        "child_policy_mode": child_result.get("child_policy_mode", ""),
        "child_live_adapter_id": child_result.get("child_live_adapter_id", ""),
        "child_live_domain_action": child_result.get("child_live_domain_action", ""),
        "commitment_progress_score": outcome.get("commitment_progress_score", 0.0),
        "recovery_cost": outcome.get("recovery_cost", 0.0),
        "terminal_section_ratio": outcome.get("terminal_section_ratio", 0.0),
        "arbitration_bundle_digest": arbitration_bundle.get("arbitration_bundle_digest", ""),
        "child_horizon_bundle_digest": outcome.get("child_horizon_bundle_digest", ""),
        "child_horizon_outcome_digest": outcome.get("child_horizon_outcome_digest", ""),
        "child_effect_receipt_digest": outcome.get("child_effect_receipt_digest", ""),
        "arbitration_state_digest": state.get("arbitration_state_digest", ""),
        "record_digest": "",
    }
    row["record_digest"] = sha(without(row, "record_digest"))
    return row
