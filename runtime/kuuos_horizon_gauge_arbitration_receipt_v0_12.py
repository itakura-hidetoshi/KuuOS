#!/usr/bin/env python3
from __future__ import annotations
import time
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import VERSION

def build_receipt(*, status: str, packet_id: str, run_id: str, cycle_index: int, decision: Mapping[str, Any], outcome: Mapping[str, Any], arbitration_bundle: Mapping[str, Any], child_result: Mapping[str, Any], blockers: list[str], warnings: list[str]) -> dict[str, Any]:
    return {
        "version": VERSION,
        "status": status,
        "packet_id": packet_id,
        "arbitration_run_id": run_id,
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "arbitration_class": outcome.get("arbitration_class", decision.get("arbitration_class", "")),
        "commitment_outcome_class": outcome.get("commitment_outcome_class", ""),
        "consensus_mode": decision.get("consensus_mode", ""),
        "short_dominant_mode": decision.get("short_dominant_mode", ""),
        "medium_dominant_mode": decision.get("medium_dominant_mode", ""),
        "long_dominant_mode": decision.get("long_dominant_mode", ""),
        "arbitration_curvature": decision.get("arbitration_curvature", 0.0),
        "transported_short_weight": decision.get("transported_short_weight", 0.0),
        "transported_medium_weight": decision.get("transported_medium_weight", 0.0),
        "transported_long_weight": decision.get("transported_long_weight", 0.0),
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
        "one_child_horizon_cycle": True,
        "multiple_child_cycle_count": 0,
        "winner_take_all_collapse_count": 0,
        "hard_gate_bypass_count": 0,
        "blockers": blockers,
        "warnings": warnings,
        "epoch": int(time.time()),
    }
