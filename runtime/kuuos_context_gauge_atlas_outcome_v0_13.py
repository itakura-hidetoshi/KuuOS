from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_context_gauge_atlas_types_v0_13 import OUTCOME_VERSION, outcome_digest


def build_outcome(*, atlas_run_id: str, cycle_index: int, decision: Mapping[str, Any], local_result: Mapping[str, Any], local_outcome: Mapping[str, Any]) -> dict[str, Any]:
    packet = {
        "version": OUTCOME_VERSION,
        "atlas_run_id": atlas_run_id,
        "cycle_index": cycle_index,
        "target_context_key": decision.get("target_context_key", ""),
        "atlas_class": decision.get("atlas_class", ""),
        "compatible_chart_count": decision.get("compatible_chart_count", 0),
        "atlas_curvature": decision.get("atlas_curvature", 0.0),
        "cocycle_defect": decision.get("cocycle_defect", 0.0),
        "transported_short_weight": decision.get("transported_short_weight", 0.0),
        "transported_medium_weight": decision.get("transported_medium_weight", 0.0),
        "transported_long_weight": decision.get("transported_long_weight", 0.0),
        "child_arbitration_class": local_result.get("arbitration_class", ""),
        "child_commitment_outcome_class": local_result.get("commitment_outcome_class", ""),
        "child_policy_mode": local_result.get("child_policy_mode", ""),
        "child_live_adapter_id": local_result.get("child_live_adapter_id", ""),
        "child_live_domain_action": local_result.get("child_live_domain_action", ""),
        "child_arbitration_bundle_digest": local_result.get("arbitration_bundle_digest", ""),
        "child_arbitration_outcome_digest": local_outcome.get("arbitration_outcome_digest", ""),
        "child_effect_receipt_digest": local_result.get("child_effect_receipt_digest", ""),
        "atlas_decision_digest": decision.get("atlas_decision_digest", ""),
        "effect_grounded_chart_update": True,
        "atlas_outcome_digest": "",
    }
    packet["atlas_outcome_digest"] = outcome_digest(packet)
    return packet
