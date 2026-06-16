from __future__ import annotations
from typing import Any, Mapping
from runtime.kuuos_event_adapter_federation_types_v0_5 import batch_digest
from runtime.kuuos_horizon_gauge_arbitration_types_v0_12 import PLAN_VERSION, REQUIRED_BOUNDARY, plan_digest

ATLAS_ONLY = {
    "version", "atlas_run_id", "atlas_plan_digest",
    "expected_previous_atlas_state_digest",
    "expected_previous_atlas_bundle_digest",
    "minimum_chart_overlap", "target_chart_retention",
    "transition_phase_gain", "plural_atlas_curvature_threshold",
    "max_atlas_holonomy", "max_atlas_outcomes", "boundary",
}


def build_local_plan(*, atlas_plan: Mapping[str, Any], decision: Mapping[str, Any], sources: list[Mapping[str, Any]], root_packet: Mapping[str, Any], registry: Mapping[str, Any], current: Mapping[str, Mapping[str, Any]]) -> dict[str, Any]:
    packet = {key: value for key, value in atlas_plan.items() if key not in ATLAS_ONLY}
    packet.update({
        "version": PLAN_VERSION,
        "arbitration_run_id": str(atlas_plan.get("atlas_run_id", "")) + ":arbitration",
        "expected_source_batch_digest": batch_digest(sources),
        "expected_root_principles_digest": root_packet.get("root_principles_digest", ""),
        "expected_adapter_registry_digest": registry.get("adapter_registry_digest", ""),
        "expected_capability_state_digest": current["capability_state"].get("capability_state_digest", ""),
        "expected_capability_bundle_digest": current["capability_bundle"].get("capability_bundle_digest", ""),
        "expected_source_portfolio_bundle_digest": current["source_portfolio_bundle"].get("portfolio_bundle_digest", ""),
        "expected_experiment_state_digest": current["experiment_state"].get("experiment_state_digest", ""),
        "expected_experiment_bundle_digest": current["experiment_bundle"].get("experiment_bundle_digest", ""),
        "expected_policy_state_digest": current["policy_state"].get("policy_state_digest", ""),
        "expected_policy_bundle_digest": current["policy_bundle"].get("policy_bundle_digest", ""),
        "expected_regret_state_digest": current["regret_state"].get("regret_state_digest", ""),
        "expected_regret_bundle_digest": current["regret_bundle"].get("regret_bundle_digest", ""),
        "expected_horizon_state_digest": current["horizon_state"].get("horizon_state_digest", ""),
        "expected_horizon_bundle_digest": current["horizon_bundle"].get("horizon_bundle_digest", ""),
        "expected_gauge_state_digest": current["gauge_state"].get("gauge_state_digest", ""),
        "expected_gauge_bundle_digest": current["gauge_bundle"].get("gauge_bundle_digest", ""),
        "expected_previous_arbitration_state_digest": current["state"].get("arbitration_state_digest", ""),
        "expected_previous_arbitration_bundle_digest": current["bundle"].get("arbitration_bundle_digest", ""),
        "base_short_horizon_weight": decision.get("transported_short_weight", 0.5),
        "base_medium_horizon_weight": decision.get("transported_medium_weight", 0.3),
        "base_long_horizon_weight": decision.get("transported_long_weight", 0.2),
        "boundary": dict(REQUIRED_BOUNDARY),
    })
    packet["arbitration_plan_digest"] = plan_digest(packet)
    return packet
