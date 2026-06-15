#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_horizon_gauge_arbitration_outcome_class_v0_12 import classify_commitment_outcome
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import OUTCOME_VERSION, clamp, outcome_digest

def build_outcome_packet(*, arbitration_run_id: str, cycle_index: int, child_horizon_bundle: Mapping[str, Any], child_horizon_outcome: Mapping[str, Any], decision: Mapping[str, Any], gauge_bundle: Mapping[str, Any], plan: Mapping[str, Any]) -> dict[str, Any]:
    outcome_class = classify_commitment_outcome(
        child_horizon_outcome=child_horizon_outcome,
        decision=decision,
        plan=plan,
    )
    packet = {
        "version": OUTCOME_VERSION,
        "arbitration_run_id": arbitration_run_id,
        "cycle_index": cycle_index,
        "context_key": decision.get("context_key", ""),
        "arbitration_class": decision.get("arbitration_class", ""),
        "commitment_outcome_class": outcome_class,
        "consensus_mode": decision.get("consensus_mode", ""),
        "arbitration_curvature": round(clamp(decision.get("arbitration_curvature")), 6),
        "transported_short_weight": decision.get("transported_short_weight", 0.0),
        "transported_medium_weight": decision.get("transported_medium_weight", 0.0),
        "transported_long_weight": decision.get("transported_long_weight", 0.0),
        "child_policy_mode": child_horizon_outcome.get("child_policy_mode", ""),
        "child_live_domain_action": child_horizon_outcome.get("child_live_domain_action", ""),
        "commitment_progress_score": child_horizon_outcome.get("commitment_progress_score", 0.0),
        "recovery_cost": child_horizon_outcome.get("recovery_cost", 0.0),
        "terminal_section_ratio": child_horizon_outcome.get("terminal_section_ratio", 0.0),
        "child_horizon_bundle_digest": child_horizon_bundle.get("horizon_bundle_digest", ""),
        "child_horizon_outcome_digest": child_horizon_outcome.get("horizon_outcome_digest", ""),
        "child_effect_receipt_digest": child_horizon_outcome.get("child_effect_receipt_digest", ""),
        "source_gauge_bundle_digest": gauge_bundle.get("gauge_bundle_digest", ""),
        "arbitration_decision_digest": decision.get("arbitration_decision_digest", ""),
        "commitment_outcome_is_effect_grounded": True,
        "arbitration_outcome_digest": "",
    }
    packet["arbitration_outcome_digest"] = outcome_digest(packet)
    return packet
